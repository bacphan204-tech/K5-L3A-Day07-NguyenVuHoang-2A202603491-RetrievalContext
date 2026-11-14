"""Integration checks against the real local Day 6 vectors (not benchmark scores)."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from dense_retrieval import DEFAULT_DAY6, DenseRetriever, tree_hashes


def main():
    retriever = DenseRetriever()
    sample = retriever.collection.get(limit=1, include=["embeddings"])
    result = retriever.collection.query(query_embeddings=[sample["embeddings"][0].tolist()],
                                        n_results=1, include=["distances"])
    if result["ids"][0][0] != sample["ids"][0] or abs(result["distances"][0][0]) > 1e-5:
        raise AssertionError("Stored vector cannot retrieve itself with cosine distance near zero")
    cases = []
    for question, filters, k in (("Ai cung ứng lao động?", {"chapter": 4}, 3),
                                  ("Giá trần là gì?", {"chapter": 3}, 3),
                                  ("Giá và lượng cân bằng là gì?", None, 5)):
        rows = retriever.search(question, filters=filters, top_k=k)
        if len(rows) != k or len({r["id"] for r in rows}) != k:
            raise AssertionError("Unexpected result count or duplicate IDs")
        if filters and any(r["metadata"]["chapter"] != filters["chapter"] for r in rows):
            raise AssertionError("Chapter filter was not respected")
        if any(r["text"] != retriever.chunks[r["id"]]["text"] for r in rows):
            raise AssertionError("Returned text differs from the prepared corpus")
        cases.append({"question": question, "filter": filters, "top_k": k,
                      "results": rows, "timings": dict(retriever.last_timings)})
    for query, filters, k in (("", None, 3), ("q", {"chapter": 5}, 3), ("q", None, 0)):
        try:
            retriever.search(query, filters=filters, top_k=k)
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid input was not rejected")
    unchanged = tree_hashes(DEFAULT_DAY6 / ".local/chroma") == retriever.snapshot_info["source_file_sha256"]
    if not unchanged:
        raise AssertionError("Original Day 6 database differs from the snapshot input hashes")
    report = {"status": "passed", "corpus_chunk_count": len(retriever.chunks),
              "stored_vector_self_match": True, "filters_and_schema": True,
              "invalid_inputs_rejected": True, "day6_database_files_unchanged": True,
              "cases": cases, "note": "Real-vector integration checks; not held-out quality evaluation."}
    output = ROOT / "results/part02/integration-check.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: real vectors, self-match, chapter filters, input validation, unchanged Day 6 database.\nReport: {output}")


if __name__ == "__main__":
    main()
