"""Two preset dev experiments: clean redundant scope text, then sentence rerank."""
import json
from pathlib import Path
import re
import time


def clean_scope_query(question, filters=None):
    """Only remove an explicit chapter prefix already supplied as a filter."""
    match = re.match(r"^\s*Theo\s+chương\s+([34])\b\s*[,;:\-]?\s*", question, re.IGNORECASE)
    if match and filters and filters.get("chapter") == int(match.group(1)):
        cleaned = question[match.end():].strip()
        if cleaned:
            return cleaned
    return question


def sentence_spans(text):
    ends = [m.end() for m in re.finditer(r'[.!?][”"\']?\s+', text)] + [len(text)]
    start = 0
    result = []
    for end in ends:
        raw = text[start:end]
        left = start + len(raw) - len(raw.lstrip())
        right = end - (len(raw) - len(raw.rstrip()))
        if right > left:
            result.append({"text": text[left:right], "start": left, "end": right})
        start = end
    return result


def combine_sentence_scores(candidates, sentence_scores, *, alpha=0.5, top_k=20):
    if not 0 <= alpha <= 1 or top_k < 1:
        raise ValueError("alpha must be in [0,1] and top_k must be positive")
    output = []
    for c in candidates:
        best = sentence_scores[c["id"]]
        output.append({**c, "strategy": "dense_sentence_rerank", "dense_score": c["score"],
                       "dense_rank": c["rank"], "best_sentence": best,
                       "score": alpha * c["score"] + (1 - alpha) * best["score"]})
    output.sort(key=lambda c: (-c["score"], c["id"]))
    return [{**c, "rank": rank} for rank, c in enumerate(output[:top_k], 1)]


class SentenceReranker:
    def __init__(self, dense, corpus_sha256, cache_path):
        import numpy as np
        started = time.perf_counter()
        self.np, self.dense = np, dense
        self.spans = {cid: sentence_spans(c["text"]) for cid, c in dense.chunks.items()}
        unique_texts = sorted({s["text"] for spans in self.spans.values() for s in spans})
        key = {"corpus_sha256": corpus_sha256, "model": dense.embedding_config,
               "sentence_policy": "punctuation-space-v1", "texts": unique_texts}
        cache_path = Path(cache_path)
        cached = json.loads(cache_path.read_text(encoding="utf-8")) if cache_path.is_file() else None
        if cached and cached["key"] == key:
            vectors = np.asarray(cached["vectors"], dtype=np.float32)
            cache_used = True
        else:
            print(f"Encoding {len(unique_texts)} source sentences locally (first run only)...", flush=True)
            prefixed = [dense.embedding_config["document_prefix"] + text for text in unique_texts]
            tokens = dense.model.tokenizer(prefixed, truncation=False)["input_ids"]
            if any(len(ids) > 512 for ids in tokens):
                raise ValueError("Sentence exceeds 512 tokens; do not silently truncate")
            vectors = dense.model.encode(prefixed, normalize_embeddings=True, batch_size=16, show_progress_bar=True)
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_text(json.dumps({"key": key, "vectors": vectors.tolist()}) + "\n", encoding="utf-8")
            cache_used = False
        if vectors.shape != (len(unique_texts), 384) or not np.isfinite(vectors).all():
            raise ValueError("Invalid sentence vector cache")
        if not np.allclose(np.linalg.norm(vectors, axis=1), 1, atol=1e-4):
            raise ValueError("Sentence vectors must be L2-normalized")
        self.vectors = vectors
        self.text_index = {text: i for i, text in enumerate(unique_texts)}
        self.setup = {"unique_sentences": len(unique_texts), "cache_used": cache_used,
                      "setup_seconds": time.perf_counter() - started,
                      "cache_path": str(cache_path), "new_document_embeddings": 0 if cache_used else len(unique_texts)}
        self.last_trace = {}

    def rerank(self, query, candidates, *, alpha=0.5):
        started = time.perf_counter()
        if not candidates:
            self.last_trace = {"query": query, "candidate_count": 0, "rerank_seconds": 0,
                               "query_embedding_recomputed": False}
            return []
        prefixed = self.dense.embedding_config["query_prefix"] + query
        if len(self.dense.model.tokenizer(prefixed, truncation=False)["input_ids"]) > 512:
            raise ValueError("Rerank query exceeds 512 tokens")
        vector = self.dense.model.encode(prefixed, normalize_embeddings=True, show_progress_bar=False)
        scores = {}
        for chunk in candidates:
            spans = self.spans[chunk["id"]]
            similarities = self.vectors[[self.text_index[s["text"]] for s in spans]] @ vector
            best = int(self.np.argmax(similarities))
            scores[chunk["id"]] = {**spans[best], "score": float(similarities[best]),
                                    "page_start_char": chunk["metadata"]["start_char"] + spans[best]["start"],
                                    "note": "Most similar sentence; not a human evidence-support label"}
        results = combine_sentence_scores(candidates, scores, alpha=alpha, top_k=len(candidates))
        self.last_trace = {"query": query, "alpha_dense": alpha, "alpha_sentence": 1 - alpha,
                           "rerank_seconds": time.perf_counter() - started,
                           "candidate_count": len(candidates), "query_embedding_recomputed": True}
        return results
