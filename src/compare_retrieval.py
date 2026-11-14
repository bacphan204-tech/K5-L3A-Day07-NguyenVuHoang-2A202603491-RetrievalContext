"""Compare three real retrieval methods; no benchmark labels are read."""
import argparse
import json
from pathlib import Path
import time

from dense_retrieval import DEFAULT_DAY6, ROOT, DenseRetriever, file_hash, load_json
from hybrid_retrieval import HybridRetriever
from lexical_retrieval import BM25Retriever, validate_search


def main():
    parser = argparse.ArgumentParser(description="Compare dense, BM25 and hybrid on the economics corpus")
    parser.add_argument("--question", required=True)
    parser.add_argument("--chapter", type=int, choices=(3, 4))
    parser.add_argument("--method", choices=("all", "dense", "bm25", "hybrid"), default="all")
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--candidate-k", type=int, default=20)
    parser.add_argument("--rrf-k", type=float, default=60)
    parser.add_argument("--lexical-query", help="Optional explicit English keywords; logged separately from the original query")
    parser.add_argument("--day6", type=Path, default=DEFAULT_DAY6)
    parser.add_argument("--output", type=Path, default=ROOT / "results/part03/compare-last.json")
    args = parser.parse_args()
    filters = {"chapter": args.chapter} if args.chapter is not None else None
    lexical_query = args.question if args.lexical_query is None else args.lexical_query
    trace = {"question": args.question, "filter": filters, "requested_method": args.method,
             "top_k": args.top_k, "candidate_k": args.candidate_k, "rrf_k": args.rrf_k,
             "lexical_query": lexical_query,
             "query_mode": "original" if args.lexical_query is None else "user_supplied_lexical_query"}
    try:
        validate_search(args.question, filters, args.top_k)
        validate_search(lexical_query, filters, args.top_k)
        if args.candidate_k < args.top_k:
            raise ValueError("candidate_k must be at least top_k")
        started = time.perf_counter()
        chunks_path = ROOT / "data/day6/chunks.json"
        chunks = load_json(chunks_path)
        lexical = BM25Retriever(chunks)
        outputs = {}
        if args.method == "bm25":
            outputs["bm25"] = lexical.search(lexical_query, filters=filters, top_k=args.top_k)
            trace["bm25_trace"] = dict(lexical.last_trace)
        else:
            dense = DenseRetriever(args.day6)
            trace["embedding"] = dense.embedding_config
            trace["dense_startup_seconds"] = dense.startup_seconds
            if args.method == "dense":
                outputs["dense"] = dense.search(args.question, filters=filters, top_k=args.top_k)
                trace["dense_timings"] = dict(dense.last_timings)
            else:
                hybrid = HybridRetriever(dense, lexical, candidate_k=args.candidate_k, rrf_k=args.rrf_k)
                fused = hybrid.search(args.question, filters=filters, top_k=args.top_k, lexical_query=args.lexical_query)
                if args.method == "all":
                    outputs["dense"] = hybrid.last_trace["dense_candidates"][:args.top_k]
                    outputs["bm25"] = hybrid.last_trace["bm25_candidates"][:args.top_k]
                outputs["hybrid"] = fused
                trace["pipeline_trace"] = hybrid.last_trace
        trace.update(status="success", outputs=outputs, corpus_chunk_count=len(chunks),
                     corpus_sha256=file_hash(chunks_path), elapsed_including_startup_seconds=time.perf_counter() - started,
                     api_cost_usd=0, cost_note="Local execution; electricity/hardware costs not measured",
                     note="Manual retrieval comparison, not a benchmark quality score or LLM answer.")
    except Exception as exc:
        trace.update(status="error", error_type=type(exc).__name__, error=str(exc))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(trace, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        raise
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(trace, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nRETRIEVAL COMPARISON | {len(chunks)} chunks | query mode: {trace['query_mode']}")
    print(f"Question: {args.question}\nLexical query: {lexical_query}\nFilter: {filters}")
    for method, rows in outputs.items():
        print(f"\n=== {method.upper()} | {len(rows)} results ===")
        if not rows:
            print("No matching lexical terms. Vietnamese words may not occur in the English book.")
        for c in rows:
            print(f"#{c['rank']} | score={c['score']:.6f} | ID={c['id']}")
            print(f"PDF page {c['page']} | printed page {c['metadata']['printed_page']} | chapter {c['metadata']['chapter']}")
            print(f"Source: {c['source']}")
            if "components" in c:
                print("Component ranks: " + ", ".join(f"{m}={v['rank']}" for m, v in c["components"].items()))
            print(c["text"] + "\n")
    print(f"PASS: comparison completed. Trace: {args.output}")


if __name__ == "__main__":
    main()
