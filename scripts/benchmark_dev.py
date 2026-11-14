"""Run original-query dense/BM25/hybrid on DEV ONLY; never open test files."""
import argparse
from datetime import datetime, timezone
import importlib.metadata
import json
from pathlib import Path
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from benchmark import load_cases, pipeline_input, validate_cases
from dense_retrieval import DEFAULT_DAY6, DenseRetriever, file_hash, load_json
from hybrid_retrieval import reciprocal_rank_fusion
from lexical_retrieval import BM25Retriever
from retrieval_metrics import grade_retrieval, summarize


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(day6, output, candidate_k=20, rrf_k=60):
    if type(candidate_k) is not int or candidate_k < 3 or not 0 < rrf_k < float("inf"):
        raise ValueError("candidate_k must be >= 3 and rrf_k must be finite and positive")
    corpus_path = ROOT / "data/day6/chunks.json"
    dev_path = ROOT / "benchmark/dev.json"
    input_path = ROOT / "benchmark/dev.inputs.json"
    manifest = load_json(ROOT / "benchmark/manifest.json")
    if file_hash(corpus_path) != manifest["corpus_sha256"] or file_hash(dev_path) != manifest["question_files_sha256"]["dev.json"]:
        raise ValueError("Corpus/dev labels changed since benchmark preparation")
    cases, inputs, chunks = load_cases(dev_path), load_json(input_path), load_json(corpus_path)
    if any(c["split"] != "dev" for c in cases) or inputs != [pipeline_input(c) for c in cases]:
        raise ValueError("Dev input mismatch, wrong split or evaluator-label leakage")
    checked = validate_cases(cases, chunks)
    if checked["counts"]["dev"]["answerable"] < 15 or checked["counts"]["dev"]["unanswerable"] < 2:
        raise ValueError("Dev benchmark needs at least 15 answerable and 2 unanswerable cases")
    output.mkdir(parents=True, exist_ok=False)
    config = {"split": "dev", "query_mode": "original", "ranking_cutoff": 3,
              "candidate_k_per_method": candidate_k, "rrf_k": rrf_k,
              "bm25": {"k1": 1.5, "b": 0.75}, "corpus_sha256": file_hash(corpus_path),
              "dev_sha256": file_hash(dev_path), "dev_inputs_sha256": file_hash(input_path),
              "test_read_or_run": False, "context_or_agent_run": False,
              "source_sha256": {str(p.relative_to(ROOT)).replace("\\", "/"): file_hash(p) for p in
                                [Path(__file__), ROOT / "src/dense_retrieval.py", ROOT / "src/lexical_retrieval.py",
                                 ROOT / "src/hybrid_retrieval.py", ROOT / "src/retrieval_metrics.py"]}}
    write(output / "config.json", config)
    lexical = BM25Retriever(chunks)
    dense, startup_error = None, None
    print(f"DEV ONLY | {len(cases)} questions | {len(chunks)} chunks | loading E5...", flush=True)
    try:
        dense = DenseRetriever(day6)
        if dense.chunks != {c["id"]: c for c in chunks}:
            raise ValueError("Dense and BM25 corpus differ")
    except Exception as exc:
        startup_error = {"type": type(exc).__name__, "message": str(exc)}
    traces, reviews = [], []
    with (output / "traces.jsonl").open("w", encoding="utf-8") as stream:
        for index, (case, item) in enumerate(zip(cases, inputs), 1):
            # Only this allowlisted input reaches the retrievers.
            question, filters = item["question"], item.get("filter")
            results, errors, times, details = {}, {}, {}, {}
            for method in ("dense", "bm25"):
                start = time.perf_counter()
                try:
                    if method == "dense":
                        if startup_error:
                            raise RuntimeError(f"Dense initialization failed: {startup_error}")
                        results[method] = dense.search(question, filters=filters, top_k=candidate_k)
                        details[method] = dict(dense.last_timings)
                    else:
                        results[method] = lexical.search(question, filters=filters, top_k=candidate_k)
                        details[method] = dict(lexical.last_trace)
                except Exception as exc:
                    results[method] = []
                    errors[method] = {"type": type(exc).__name__, "message": str(exc)}
                times[method] = time.perf_counter() - start
            fusion_started = time.perf_counter()
            if errors:
                results["hybrid"] = []
                errors["hybrid"] = {"type": "ComponentError", "message": "Component failed; no silent dense/lexical fallback", "components": errors.copy()}
            else:
                results["hybrid"] = reciprocal_rank_fusion(results, top_k=candidate_k, rrf_k=rrf_k)
            fusion_seconds = time.perf_counter() - fusion_started
            times["hybrid"] = times["dense"] + times["bm25"] + fusion_seconds
            details["hybrid"] = {"fusion_seconds": fusion_seconds, "reuses_component_candidates": True,
                                 "dense_query_seconds": times["dense"], "bm25_query_seconds": times["bm25"]}
            for method in ("dense", "bm25", "hybrid"):
                status = "error" if method in errors else "success"
                row = {"query_id": item["id"], "split": "dev", "question": question, "filter": filters,
                       "method": method, "status": status, "query_mode": "original",
                       "results": results[method], "query_seconds": times[method], "timings": details.get(method, {}),
                       "error": errors.get(method), **grade_retrieval(case, results[method], status)}
                traces.append(row)
                stream.write(json.dumps(row, ensure_ascii=False) + "\n")
                stream.flush()
                reviews.append({"query_id": case["id"], "method": method, "answerable": case["answerable"],
                                "strict_hit1": row["hit1"], "strict_hit3": row["hit3"],
                                "manual_evidence_supported": None, "supporting_chunk_ids": [],
                                "reason": "", "reviewer": "", "student_confirmed": False})
            print(f"[{index}/{len(cases)}] {item['id']} | " + " | ".join(
                f"{m}: error" if m in errors else f"{m}: {len(results[m])} candidates" for m in ("dense", "bm25", "hybrid")), flush=True)
    metrics = [summarize(traces, m) for m in ("dense", "bm25", "hybrid")]
    summary = {"config": config, "metrics": metrics, "dense_startup_error": startup_error,
               "dense_startup_seconds": dense.startup_seconds if dense is not None else None,
               "bm25_index_seconds": lexical.index_seconds,
               "packages": {p: importlib.metadata.version(p) for p in ("chromadb", "sentence-transformers", "torch")},
               "timing_note": "Hybrid sums dense + BM25 + fusion; component candidates shared in this run. Startup separate. No independent repeated timing trials.",
               "quality_note": "Strict quote matching only; draft AI-authored labels awaiting student confirmation. Empty retrieval is not abstention.",
               "cost_note": "Local API cost 0 USD; electricity/hardware costs not measured. No LLM called."}
    write(output / "summary.json", summary)
    write(output / "manual_reviews.json", reviews)
    lines = ["# Dev retrieval — original queries", "", "| Method | Hit@1 | Evidence Hit@3 | Errors | Median query (ms) |", "|---|---:|---:|---:|---:|"]
    for m in metrics:
        def fmt(metric):
            return f"{metric['n']}/{metric['N']} ({100 * metric['rate']:.2f}%)" if metric["N"] else "N/A"
        ms = f"{1000*m['median_query_seconds']:.2f}" if m["median_query_seconds"] is not None else "N/A"
        line = f"| {m['method']} | {fmt(m['hit1'])} | {fmt(m['evidence_hit3'])} | {m['errors']} | {ms} |"
        lines.append(line)
        print(line)
    lines += ["", "15 answerable cases form the retrieval denominator; 2 unanswerable cases are traced separately.",
              "Errors count as misses in the fixed denominator and are reported explicitly.",
              "No context/agent/citation/abstention metrics have been measured. No test inputs or labels were loaded.",
              "See summary.json for configuration, costs, timing limitations and trace provenance."]
    (output / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    write(output.parent / "latest.json", {"run_directory": str(output.resolve())})
    failed = any(m["errors"] for m in metrics)
    print(f"\n{'ERRORS_RECORDED' if failed else 'PASS'}: dev retrieval run complete. Results: {output}")
    return 1 if failed else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--day6", type=Path, default=DEFAULT_DAY6)
    parser.add_argument("--candidate-k", type=int, default=20)
    parser.add_argument("--rrf-k", type=float, default=60)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = args.output or ROOT / "results/part05" / ("dev-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:6])
    sys.exit(run(args.day6, output, args.candidate_k, args.rrf_k))
