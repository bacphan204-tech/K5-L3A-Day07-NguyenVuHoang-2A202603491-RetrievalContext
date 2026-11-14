"""Run two real agents on dev only, checkpoint every case, stop on provider errors."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from agent_evaluation import operational_summary, review_template
from benchmark import load_cases, pipeline_input, validate_cases
from book_agent import PROMPT_VERSION, VALIDATOR_VERSION, run_book_agent
from dense_retrieval import DEFAULT_DAY6, DenseRetriever, file_hash, load_json
from agent_retriever import BookRetriever
from llm_client import ResponsesClient, public_settings, read_settings


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def refresh(folder, method, cases, chunks):
    directory = folder / method
    traces = [load_json(p) for p in sorted((directory / "traces").glob("*.json"))]
    write(directory / "traces.json", traces)
    write(directory / "operational_summary.json", operational_summary(cases, traces, chunks))
    reviews_path = directory / "reviews.json"
    old = {r["query_id"]: r for r in load_json(reviews_path)} if reviews_path.is_file() else {}
    by_id = {c["id"]: c for c in cases}
    reviews = [old.get(t["query_id"], review_template(by_id[t["query_id"]], t)) for t in traces]
    write(reviews_path, reviews)
    split_name = cases[0]["split"].upper() if cases else "UNKNOWN"
    lines = [f"# {split_name} agent review — {method}", "", "Unfilled review labels are pending, not zero scores.", ""]
    for t in traces:
        c = by_id[t["query_id"]]
        lines += [f"## {c['id']}", "", c["question"], "", f"Status: {t['status']}", "",
                  "Expected answer/behavior: " + c.get("expected_answer", c.get("absence_reason", "")), "",
                  "Agent answer: " + t.get("answer", ""), "", "Citation IDs: " + json.dumps(t.get("citations", [])), "",
                  "Gold source evidence: " + json.dumps(c.get("gold", []), ensure_ascii=False), "",
                  "Final context:", "", "```text", t.get("context", ""), "```", ""]
    (directory / "review_packet.md").write_text("\n".join(lines), encoding="utf-8")
    return traces


def run(args):
    settings = read_settings()
    cases, inputs = load_cases(ROOT / "benchmark/dev.json"), load_json(ROOT / "benchmark/dev.inputs.json")
    chunks_path = ROOT / "data/day6/chunks.json"
    chunks, manifest = load_json(chunks_path), load_json(ROOT / "benchmark/manifest.json")
    if inputs != [pipeline_input(c) for c in cases] or any(c["split"] != "dev" for c in cases):
        raise ValueError("Invalid dev inputs/label isolation")
    if file_hash(chunks_path) != manifest["corpus_sha256"] or file_hash(ROOT / "benchmark/dev.json") != manifest["question_files_sha256"]["dev.json"]:
        raise ValueError("Corpus/dev benchmark changed")
    validate_cases(cases, chunks)
    config = {"split": "dev", "methods": ["dense", "rerank"], "llm": public_settings(settings),
              "prompt_version": PROMPT_VERSION, "validator_version": VALIDATOR_VERSION, "max_searches": 3, "top_k": 5, "candidate_k": 20,
              "context_budget_chars": 5000, "corpus_sha256": file_hash(chunks_path),
              "dev_sha256": file_hash(ROOT / "benchmark/dev.json"), "test_read_or_run": False,
              "source_sha256": {p.name: file_hash(p) for p in [Path(__file__), ROOT / "src/book_agent.py", ROOT / "src/agent_retriever.py", ROOT / "src/llm_client.py", ROOT / "src/retrieval_improvements.py", ROOT / "src/dense_retrieval.py"]}}
    if args.resume:
        folder = args.resume.resolve()
        if load_json(folder / "config.json") != config:
            raise ValueError("Cannot resume after model/prompt/code/corpus/config changes; start a new run")
    else:
        folder = ROOT / "results/part08" / ("dev-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:6])
        folder.mkdir(parents=True, exist_ok=False)
        write(folder / "config.json", config)
        write(folder / "cases.json", cases)
    write(ROOT / "results/part08/latest.json", {"run_directory": str(folder)})
    print(f"DEV AGENT | 17 cases x 2 configurations | API calls are billed.\nResults: {folder}", flush=True)
    print("Loading E5 and shared sentence cache once...", flush=True)
    dense = DenseRetriever(args.day6)
    retrievers = {"dense": BookRetriever(dense, "dense"), "rerank": BookRetriever(dense, "rerank")}
    write(folder / "local_setup.json", {"dense_startup_seconds": dense.startup_seconds, "sentence_setup": retrievers["rerank"].reranker.setup})
    made = 0
    stop = False
    for index, (case, item) in enumerate(zip(cases, inputs), 1):
        for method in ("dense", "rerank"):
            trace_path = folder / method / "traces" / (item["id"] + ".json")
            if trace_path.is_file():
                existing = load_json(trace_path)
                if existing["status"] != "error" or not args.retry_errors:
                    continue
                # Preserve the failed attempt, including any token usage.
                previous = trace_path.parent / ("attempt-" + uuid.uuid4().hex[:8])
                previous.mkdir()
                write(previous / trace_path.name, existing)
                review_path = folder / method / "reviews.json"
                if review_path.is_file():
                    write(review_path, [r for r in load_json(review_path) if r["query_id"] != item["id"]])
            print(f"[{index}/17] {method} {item['id']} ...", flush=True)
            client = ResponsesClient(settings)
            result = run_book_agent(item["question"], client, retrievers[method], filters=item.get("filter"),
                                    max_searches=3, top_k=5, budget=5000)
            result.update(query_id=item["id"], split="dev", retrieval=method, model_calls=client.calls,
                          llm_config=public_settings(settings), prompt_version=PROMPT_VERSION)
            write(trace_path, result)
            refresh(folder, method, cases, chunks)
            made += 1
            print(f"  {result['status']} | calls={result['usage']['model_calls']} | estimated USD={result['usage']['estimated_api_cost_usd']}", flush=True)
            if result["status"] == "error":
                provider_error = result.get("error_type") == "ConnectionError" or "OpenAI HTTP" in result.get("error", "")
                print("Error recorded: " + result.get("error", ""), flush=True)
                if provider_error:
                    print("Stopped after provider error to avoid repeating a failing paid request.", flush=True)
                    stop = True
                    break
            if args.limit and made >= args.limit:
                stop = True
                break
        if stop:
            break
    complete = True
    all_attempted = True
    all_summaries = {}
    for method in ("dense", "rerank"):
        traces = refresh(folder, method, cases, chunks)
        s = operational_summary(cases, traces, chunks)
        all_summaries[method] = s
        complete = complete and len(traces) == len(cases) and s["errors"] == 0
        all_attempted = all_attempted and len(traces) == len(cases)
    archived = [load_json(p) for p in folder.glob("*/traces/attempt-*/*.json")]
    all_costs = [s["estimated_api_cost_usd"] for s in all_summaries.values()] + [t.get("usage", {}).get("estimated_api_cost_usd") for t in archived]
    write(folder / "operational_summary.json", {"all_cases_attempted": all_attempted, "complete_without_errors": complete, "configurations": all_summaries,
          "semantic_reviews_pending": True, "test_read_or_run": False,
          "archived_attempts": len(archived),
          "estimated_total_api_cost_including_archived_attempts": sum(all_costs) if all(c is not None for c in all_costs) else None,
          "retry_cost_note": "Configuration totals cover latest case traces; overall estimate includes archived attempts. Requests without returned usage can still have unknown billable cost."})
    label = "PASS" if complete else ("COMPLETE_WITH_ERRORS" if all_attempted else "PARTIAL")
    print(f"\n{label}: agent dev run saved. {folder}")
    print("Semantic grades are pending; inspect each review_packet.md and fill reviews.json. No test has run.")
    return int(any(s["errors"] for s in all_summaries.values()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--day6", type=Path, default=DEFAULT_DAY6)
    parser.add_argument("--resume", type=Path)
    parser.add_argument("--retry-errors", action="store_true")
    parser.add_argument("--limit", type=int, help="Optional number of new case/configuration runs for a smoke check")
    args = parser.parse_args()
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be positive")
    sys.exit(run(args))
