"""Freeze a dev-selected pipeline, then run its untouched test with a baseline."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from agent_retriever import BookRetriever
from benchmark import pipeline_input, validate_cases
from book_agent import PROMPT_VERSION, VALIDATOR_VERSION, run_book_agent
from dense_retrieval import DenseRetriever, file_hash, load_json
from llm_client import ResponsesClient, public_settings, read_settings
from retrieval_metrics import grade_retrieval, summarize
from agent_dev import refresh, write

LOCK = ROOT / "benchmark/frozen.json"
OUT = ROOT / "results/final/test"


def fingerprints():
    paths = list((ROOT / "src").glob("*.py")) + [Path(__file__), ROOT / "benchmark/dev.json", ROOT / "benchmark/test.json",
            ROOT / "benchmark/test.inputs.json", ROOT / "data/day6/chunks.json"]
    return {p.relative_to(ROOT).as_posix(): file_hash(p) for p in sorted(paths)}


def freeze():
    if LOCK.exists():
        raise ValueError("An experiment is already frozen; do not overwrite it after test")
    folder = Path(load_json(ROOT / "results/part08/latest.json")["run_directory"])
    evaluation = load_json(folder / "evaluation_summary.json")
    configs = evaluation["configurations"]
    if any(v["pending_review_query_ids"] or v["manual_metrics"] is None for v in configs.values()):
        raise ValueError("Complete dev source reviews before selection")
    def rank(method):
        entry = configs[method]
        semantic = entry["manual_metrics"]
        citations = semantic["citation_validity"]
        context = semantic["manual_context_evidence_rate"]
        return (-semantic["grounded_answer"]["mean"], -(citations["n"]/citations["N"] if citations["N"] else 0),
                -(context["n"]/context["N"]), entry["operational"]["total_agent_seconds"], method)
    selected = sorted(configs, key=rank)[0]
    lock = {"frozen_at_utc": datetime.now(timezone.utc).isoformat(), "selected_method": selected,
            "baseline_method": "dense", "dev_run": str(folder.relative_to(ROOT)),
            "dev_evaluation_sha256": file_hash(folder / "evaluation_summary.json"),
            "selection_rule": "Highest dev grounded-answer mean, then semantic citation rate, manual context rate, lower agent time, then method name. This rule is documented at final selection after exploratory dev, before running test; not a preregistered dev study.",
            "reviewer": "Codex AI; same assistant helped implement system", "student_confirmed": False,
            "llm": public_settings(read_settings()), "prompt_version": PROMPT_VERSION, "validator_version": VALIDATOR_VERSION,
            "max_searches": 3, "top_k": 5, "candidate_k": 20, "context_budget_chars": 5000,
            "fingerprints": fingerprints(), "test_model_run_before_freeze": False,
            "scope": "Basic Day 7 only; no optional 100-page advanced challenge"}
    write(LOCK, lock)
    print(f"FROZEN: selected {selected} from reviewed dev; no test model call yet.")


def test():
    lock = load_json(LOCK)
    if fingerprints() != lock["fingerprints"]:
        raise ValueError("Frozen pipeline/benchmark/corpus changed; cannot run this held-out test")
    settings = read_settings()
    if public_settings(settings) != lock["llm"]:
        raise ValueError("LLM settings differ from frozen selection")
    cases, inputs = load_json(ROOT / "benchmark/test.json"), load_json(ROOT / "benchmark/test.inputs.json")
    chunks = load_json(ROOT / "data/day6/chunks.json")
    validate_cases(cases, chunks)
    if any(c["split"] != "test" for c in cases) or inputs != [pipeline_input(c) for c in cases]:
        raise ValueError("Test inputs do not match allowlisted labels")
    methods = list(dict.fromkeys([lock["baseline_method"], lock["selected_method"]]))
    OUT.mkdir(parents=True, exist_ok=True)
    write(OUT / "config.json", {**lock, "split": "test", "methods": methods})
    write(OUT / "cases.json", cases)
    print(f"FROZEN TEST | {len(cases)} cases x {len(methods)} agents | no tuning", flush=True)
    dense = DenseRetriever()
    retrievers = {method: BookRetriever(dense, method) for method in methods}
    # Original-query retrieval is measured separately from agent-written queries.
    retrieval_file = OUT / "original_query_retrieval.json"
    if not retrieval_file.exists():
        ranking_traces = []
        for case, item in zip(cases, inputs):
            for method in methods:
                rows = retrievers[method].search(item["question"], filters=item.get("filter"), top_k=20)
                ranking_traces.append({"query_id": item["id"], "method": method, "split": "test", "question": item["question"],
                    "status": "success", "results": rows, "query_seconds": dense.last_timings["total_query_seconds"],
                    "query_mode": "original" if method == "dense" else "scope_prefix_cleanup", **grade_retrieval(case, rows)})
        write(retrieval_file, ranking_traces)
        write(OUT / "retrieval_summary.json", [summarize(ranking_traces, m) for m in methods])
    for i, (case, item) in enumerate(zip(cases, inputs), 1):
        for method in methods:
            path = OUT / method / "traces" / f"{item['id']}.json"
            if path.exists():
                continue
            print(f"[{i}/{len(cases)}] {method} {item['id']} ...", flush=True)
            client = ResponsesClient(settings)
            result = run_book_agent(item["question"], client, retrievers[method], filters=item.get("filter"),
                max_searches=lock["max_searches"], top_k=lock["top_k"], budget=lock["context_budget_chars"])
            result.update(query_id=item["id"], split="test", retrieval=method, model_calls=client.calls,
                          llm_config=public_settings(settings), prompt_version=PROMPT_VERSION)
            write(path, result)
            refresh(OUT, method, cases, chunks)
            print(f"  {result['status']} | calls={result['usage']['model_calls']} | estimated USD={result['usage']['estimated_api_cost_usd']}", flush=True)
    for method in methods:
        refresh(OUT, method, cases, chunks)
    print(f"TEST SAVED: {OUT}. Review every answer/context/citation; retain all failures.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("freeze", "test", "verify-lock"))
    args = parser.parse_args()
    if args.stage == "freeze": freeze()
    elif args.stage == "test": test()
    else:
        if fingerprints() != load_json(LOCK)["fingerprints"]:
            raise ValueError("Frozen files changed")
        print("PASS: pipeline/benchmark/corpus hashes match frozen selection")
