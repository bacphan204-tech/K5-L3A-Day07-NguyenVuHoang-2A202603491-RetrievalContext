"""Run two predeclared retrieval improvements against a fresh same-run baseline."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from benchmark import load_cases, pipeline_input, validate_cases
from dense_retrieval import DEFAULT_DAY6, DenseRetriever, file_hash, load_json
from retrieval_improvements import SentenceReranker, clean_scope_query
from retrieval_metrics import grade_retrieval, summarize


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(day6):
    plan_path = ROOT / "artifacts/dev_improvement_plan.json"
    plan = load_json(plan_path)
    manifest = load_json(ROOT / "benchmark/manifest.json")
    dev_path, corpus_path = ROOT / "benchmark/dev.json", ROOT / "data/day6/chunks.json"
    if file_hash(dev_path) != manifest["question_files_sha256"]["dev.json"] or file_hash(corpus_path) != manifest["corpus_sha256"]:
        raise ValueError("Benchmark/corpus changed")
    cases, inputs, chunks = load_cases(dev_path), load_json(ROOT / "benchmark/dev.inputs.json"), load_json(corpus_path)
    if inputs != [pipeline_input(c) for c in cases] or any(c["split"] != "dev" for c in cases):
        raise ValueError("Invalid dev inputs or label leakage")
    validate_cases(cases, chunks)
    folder = ROOT / "results/part06" / ("dev-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:6])
    folder.mkdir(parents=True, exist_ok=False)
    write(folder / "plan.json", plan)
    write(folder / "provenance.json", {"plan_sha256": file_hash(plan_path), "dev_sha256": file_hash(dev_path),
          "corpus_sha256": file_hash(corpus_path), "test_read_or_run": False,
          "source_sha256": {str(p.relative_to(ROOT)).replace("\\", "/"): file_hash(p) for p in
                            [Path(__file__), ROOT / "src/retrieval_improvements.py", ROOT / "src/dense_retrieval.py", ROOT / "src/retrieval_metrics.py"]}})
    print("DEV ONLY | baseline + 2 experiments | loading E5...", flush=True)
    dense = DenseRetriever(day6)
    if dense.chunks != {c["id"]: c for c in chunks}:
        raise ValueError("Corpus differs")
    reranker = SentenceReranker(dense, file_hash(corpus_path), ROOT / ".local/e5_sentence_bank.json")
    traces = []
    methods = ("dense_original", "clean_scope_dense", "clean_scope_sentence_rerank")
    with (folder / "traces.jsonl").open("w", encoding="utf-8") as stream:
        for i, (case, item) in enumerate(zip(cases, inputs), 1):
            query, filters = item["question"], item.get("filter")
            cleaned = clean_scope_query(query, filters)
            rows, timings, errors, details = {}, {}, {}, {}
            for method, actual in ((methods[0], query), (methods[1], cleaned)):
                started = time.perf_counter()
                try:
                    if method == methods[1] and cleaned == query and methods[0] not in errors:
                        rows[method], timings[method] = rows[methods[0]], timings[methods[0]]
                        details[method] = {"unchanged_query_reuses_baseline": True}
                        continue
                    rows[method] = dense.search(actual, filters=filters, top_k=plan["candidate_k"])
                    details[method] = dict(dense.last_timings)
                except Exception as exc:
                    rows[method] = []
                    errors[method] = {"type": type(exc).__name__, "message": str(exc)}
                timings[method] = time.perf_counter() - started
            started = time.perf_counter()
            try:
                if methods[1] in errors:
                    raise RuntimeError("Clean dense retrieval failed; cannot rerank")
                rows[methods[2]] = reranker.rerank(cleaned, rows[methods[1]], alpha=plan["experiment_2"]["alpha_dense"])
                details[methods[2]] = dict(reranker.last_trace)
            except Exception as exc:
                rows[methods[2]] = []
                errors[methods[2]] = {"type": type(exc).__name__, "message": str(exc)}
            timings[methods[2]] = timings[methods[1]] + time.perf_counter() - started
            for method in methods:
                status = "error" if method in errors else "success"
                row = {"query_id": item["id"], "split": "dev", "method": method, "question": query,
                       "retrieval_query": query if method == methods[0] else cleaned,
                       "query_mode": "original" if method == methods[0] else "scope_prefix_cleanup",
                       "filter": filters, "status": status, "results": rows[method],
                       "query_seconds": timings[method], "timings": details.get(method, {}),
                       "error": errors.get(method), **grade_retrieval(case, rows[method], status)}
                traces.append(row)
                stream.write(json.dumps(row, ensure_ascii=False) + "\n")
                stream.flush()
            print(f"[{i}/{len(cases)}] {item['id']} | query_changed={cleaned != query} | errors={len(errors)}", flush=True)
    metrics = [summarize(traces, m) for m in methods]
    pairs = []
    by_key = {(t["query_id"], t["method"]): t for t in traces}
    for case in cases:
        if not case["answerable"]:
            continue
        base = by_key[(case["id"], methods[0])]
        for method in methods[1:]:
            improved = by_key[(case["id"], method)]
            pairs.append({"query_id": case["id"], "experiment": method,
                          "baseline_hit1": base["hit1"], "experiment_hit1": improved["hit1"],
                          "baseline_hit3": base["hit3"], "experiment_hit3": improved["hit3"],
                          "delta_hit3": int(improved["hit3"]) - int(base["hit3"])})
    write(folder / "paired_changes.json", pairs)
    write(folder / "summary.json", {"metrics": metrics, "plan": plan, "sentence_setup": reranker.setup,
          "dense_startup_seconds": dense.startup_seconds, "test_read_or_run": False,
          "model": dense.embedding_config, "note": "Retrieval-only dev experiments. No context/LLM scoring or final selection.",
          "timing_note": "Unchanged clean query reuses baseline; rerank time includes clean retrieval and a new query embedding. Sentence setup/cache time reported separately.",
          "cost_note": "Local CPU/API cost 0 USD; new sentence embeddings are additional compute, electricity/hardware not measured."})
    lines = ["# Dev retrieval improvement experiments", "", "| Configuration | Hit@1 | Evidence Hit@3 | Errors | Median query ms |", "|---|---:|---:|---:|---:|"]
    for m in metrics:
        def fmt(v): return f"{v['n']}/{v['N']} ({100*v['rate']:.2f}%)" if v["N"] else "N/A"
        ms = f"{1000*m['median_query_seconds']:.2f}" if m["median_query_seconds"] is not None else "N/A"
        line = f"| {m['method']} | {fmt(m['hit1'])} | {fmt(m['evidence_hit3'])} | {m['errors']} | {ms} |"
        lines.append(line)
        print(line)
    lines += ["", "Sentence embedding setup: " + json.dumps(reranker.setup),
              "", "No test data loaded. No context/agent metrics or final configuration selected."]
    (folder / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    write(folder.parent / "latest.json", {"run_directory": str(folder.resolve())})
    failed = any(m["errors"] for m in metrics)
    print(f"\n{'ERRORS_RECORDED' if failed else 'PASS'}: dev experiments complete. Results: {folder}")
    return int(failed)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--day6", type=Path, default=DEFAULT_DAY6)
    args = parser.parse_args()
    sys.exit(run(args.day6))
