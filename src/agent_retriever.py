"""Shared retrieval adapter for interactive and benchmark agent runs."""
from pathlib import Path
from dense_retrieval import ROOT, file_hash
from retrieval_improvements import SentenceReranker, clean_scope_query


class BookRetriever:
    def __init__(self, dense, method="rerank", *, reranker=None, candidate_k=20):
        if method not in ("dense", "rerank") or candidate_k < 1:
            raise ValueError("Invalid retrieval configuration")
        self.dense, self.method, self.candidate_k = dense, method, candidate_k
        self.reranker = None
        if method == "rerank":
            self.reranker = reranker if reranker is not None else SentenceReranker(
                dense, file_hash(ROOT / "data/day6/chunks.json"), ROOT / ".local/e5_sentence_bank.json")
        self.last_trace = {}

    def search(self, query, *, filters=None, top_k=5):
        if top_k > self.candidate_k:
            raise ValueError("top_k must not exceed candidate_k")
        cleaned = clean_scope_query(query, filters) if self.reranker else query
        rows = self.dense.search(cleaned, filters=filters, top_k=self.candidate_k)
        if self.reranker:
            rows = self.reranker.rerank(cleaned, rows)
        self.last_trace = {"model_search_query": query, "retrieval_query": cleaned, "method": self.method,
                           "candidates": rows, "dense_timings": dict(self.dense.last_timings),
                           "rerank_trace": dict(self.reranker.last_trace) if self.reranker else None}
        return rows[:top_k]
