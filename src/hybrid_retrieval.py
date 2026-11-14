"""Dense + BM25 reciprocal-rank fusion with explicit candidate/query traces."""
import math
import time

from lexical_retrieval import BM25Retriever, validate_search


def reciprocal_rank_fusion(rankings, *, top_k=3, rrf_k=60):
    if type(top_k) is not int or top_k < 1 or not math.isfinite(rrf_k) or rrf_k <= 0:
        raise ValueError("top_k and rrf_k must be positive")
    merged = {}
    for method, rows in rankings.items():
        seen = set()
        for rank, chunk in enumerate(rows, 1):
            cid = chunk["id"]
            if cid in seen:
                raise ValueError(f"Duplicate ID in {method} ranking: {cid}")
            seen.add(cid)
            if cid not in merged:
                # Keep corpus fields; component scores have a different meaning.
                merged[cid] = {key: chunk[key] for key in ("id", "text", "source_id", "source", "page", "metadata")}
                merged[cid].update(strategy="hybrid", score=0.0, components={})
            entry = merged[cid]
            if entry["text"] != chunk["text"] or entry["source_id"] != chunk["source_id"] or entry["page"] != chunk["page"]:
                raise ValueError(f"Conflicting corpus records for ID {cid}")
            contribution = 1 / (rrf_k + rank)
            entry["score"] += contribution
            entry["components"][method] = {"rank": rank, "score": chunk["score"], "rrf_contribution": contribution}
    ordered = sorted(merged.values(), key=lambda c: (-c["score"], c["id"]))
    return [{**c, "rank": rank} for rank, c in enumerate(ordered[:top_k], 1)]


class HybridRetriever:
    def __init__(self, dense, lexical=None, *, candidate_k=20, rrf_k=60):
        if type(candidate_k) is not int or candidate_k < 1 or not math.isfinite(rrf_k) or rrf_k <= 0:
            raise ValueError("candidate_k and rrf_k must be positive")
        self.dense = dense
        self.lexical = lexical if lexical is not None else BM25Retriever(list(dense.chunks.values()))
        lexical_corpus = {c["id"]: c for c in self.lexical.chunks}
        if lexical_corpus != dense.chunks:
            raise ValueError("Dense and lexical must use exactly the same corpus")
        self.candidate_k, self.rrf_k = candidate_k, rrf_k
        self.last_trace = {}

    def search(self, query, *, filters=None, top_k=3, lexical_query=None):
        validate_search(query, filters, top_k)
        if top_k > self.candidate_k:
            raise ValueError("candidate_k must be at least top_k")
        actual_lexical_query = query if lexical_query is None else lexical_query
        validate_search(actual_lexical_query, filters, top_k)
        started = time.perf_counter()
        dense_rows = self.dense.search(query, filters=filters, top_k=self.candidate_k)
        dense_timings = dict(self.dense.last_timings)
        lexical_rows = self.lexical.search(actual_lexical_query, filters=filters, top_k=self.candidate_k)
        fusion_started = time.perf_counter()
        fused = reciprocal_rank_fusion({"dense": dense_rows, "bm25": lexical_rows}, top_k=top_k, rrf_k=self.rrf_k)
        self.last_trace = {
            "query": query, "lexical_query": actual_lexical_query,
            "query_mode": "original" if lexical_query is None else "user_supplied_lexical_query",
            "filter": filters, "candidate_k_per_method": self.candidate_k, "rrf_k": self.rrf_k,
            "dense_candidates": dense_rows, "bm25_candidates": lexical_rows,
            "dense_timings": dense_timings, "bm25_trace": dict(self.lexical.last_trace),
            "fusion_seconds": time.perf_counter() - fusion_started,
            "total_query_seconds": time.perf_counter() - started,
            "note": "RRF combines rank positions, not raw dense and BM25 scores."}
        return fused
