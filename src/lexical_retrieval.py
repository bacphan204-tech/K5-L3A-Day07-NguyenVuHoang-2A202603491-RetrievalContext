"""BM25 over the same Day 6 B chunks; no model, translation or gold labels."""
from collections import Counter
import math
import re
import time
import unicodedata


def tokenize(text):
    return re.findall(r"\w+", unicodedata.normalize("NFC", text).casefold())


def validate_search(query, filters, top_k):
    if not isinstance(query, str) or not query.strip():
        raise ValueError("Question must not be empty")
    if type(top_k) is not int or top_k < 1:
        raise ValueError("top_k must be a positive integer")
    if filters is not None and (set(filters) != {"chapter"} or type(filters["chapter"]) is not int or filters["chapter"] not in (3, 4)):
        raise ValueError("Only chapter 3 or 4 filters are supported")


class BM25Retriever:
    def __init__(self, chunks, *, k1=1.5, b=0.75):
        started = time.perf_counter()
        if not chunks or len({c["id"] for c in chunks}) != len(chunks):
            raise ValueError("Corpus must be nonempty with unique chunk IDs")
        if not math.isfinite(k1) or k1 <= 0 or not math.isfinite(b) or not 0 <= b <= 1:
            raise ValueError("BM25 requires k1 > 0 and 0 <= b <= 1")
        self.chunks, self.k1, self.b = list(chunks), k1, b
        self.counts = [Counter(tokenize(c["text"])) for c in chunks]
        self.lengths = [sum(counts.values()) for counts in self.counts]
        self.avg_length = sum(self.lengths) / len(self.lengths)
        if self.avg_length == 0:
            raise ValueError("Corpus has no searchable terms")
        df = Counter(term for counts in self.counts for term in counts)
        self.idf = {term: math.log1p((len(chunks) - count + 0.5) / (count + 0.5))
                    for term, count in df.items()}
        self.index_seconds = time.perf_counter() - started
        self.last_trace = {}

    def search(self, query, *, filters=None, top_k=3):
        validate_search(query, filters, top_k)
        started = time.perf_counter()
        terms = sorted(set(tokenize(query)))
        results = []
        for chunk, counts, length in zip(self.chunks, self.counts, self.lengths):
            if filters and chunk["metadata"]["chapter"] != filters["chapter"]:
                continue
            matched = [term for term in terms if counts.get(term, 0)]
            score = sum(self.idf[term] * counts[term] * (self.k1 + 1) /
                        (counts[term] + self.k1 * (1 - self.b + self.b * length / self.avg_length))
                        for term in matched)
            if score > 0:
                results.append({**chunk, "score": score, "strategy": "bm25", "matched_terms": matched})
        results.sort(key=lambda c: (-c["score"], c["id"]))
        selected = [{**c, "rank": rank} for rank, c in enumerate(results[:top_k], 1)]
        self.last_trace = {"query": query, "query_tokens": terms,
                           "tokens_in_corpus": [t for t in terms if t in self.idf],
                           "matching_chunk_count": len(results), "k1": self.k1, "b": self.b,
                           "index_seconds": self.index_seconds,
                           "search_seconds": time.perf_counter() - started}
        return selected
