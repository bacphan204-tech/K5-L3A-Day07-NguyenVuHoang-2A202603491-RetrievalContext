"""Revalidate saved model decisions offline; preserve the original run unchanged."""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from book_agent import VALIDATOR_VERSION, validate_final
from dense_retrieval import file_hash, load_json
from agent_evaluation import operational_summary
from agent_dev import write, refresh


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    args = parser.parse_args()
    source = args.run.resolve()
    config = load_json(source / "config.json")
    if config["split"] != "dev":
        raise ValueError("This command handles dev traces only")
    cases, chunks = load_json(source / "cases.json"), load_json(ROOT / "data/day6/chunks.json")
    folder = ROOT / "results/part08" / ("revalidated-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:6])
    folder.mkdir(parents=True, exist_ok=False)
    write(folder / "config.json", {**config, "validator_version": VALIDATOR_VERSION, "revalidation_only": True,
                                   "original_run": str(source), "original_config_sha256": file_hash(source / "config.json"),
                                   "validator_sha256": file_hash(ROOT / "src/book_agent.py")})
    write(folder / "cases.json", cases)
    changed = []
    hashes = {}
    summaries = {}
    for method in ("dense", "rerank"):
        for path in sorted((source / method / "traces").glob("*.json")):
            trace = load_json(path)
            if trace["split"] != "dev":
                raise ValueError("Non-dev trace encountered")
            hashes[str(path.relative_to(source)).replace("\\", "/")] = file_hash(path)
            decisions = [e for e in trace.get("events", []) if e["event"] == "model_tool_call" and e["tool"] == "finish_answer"]
            is_validation_error = trace["status"] == "error" and trace.get("error_type") == "ValueError" and decisions
            if is_validation_error:
                try:
                    final = validate_final(decisions[-1]["arguments"], trace.get("context_ids", []))
                    if not any(e["event"] == "search" for e in trace["events"]):
                        raise ValueError("Cannot recover a final answer without retrieval")
                except ValueError:
                    pass
                else:
                    trace = deepcopy(trace)
                    trace["original_validation_error"] = {"status": trace["status"], "error_type": trace.pop("error_type"), "error": trace.pop("error")}
                    trace.update(final)
                    trace["validator_version"] = VALIDATOR_VERSION
                    trace["events"].append({"event": "offline_final_revalidation", "validator_version": VALIDATOR_VERSION,
                                             "model_final": decisions[-1]["arguments"], "normalization": final.get("normalization")})
                    changed.append({"method": method, "query_id": trace["query_id"], "new_status": trace["status"], "normalization": final.get("normalization")})
            trace["revalidation_provenance"] = {"source_trace": str(path), "source_sha256": file_hash(path), "new_api_calls": 0,
                                                 "usage_note": "Token usage/cost is inherited from the original run, not additional spending."}
            write(folder / method / "traces" / path.name, trace)
        traces = refresh(folder, method, cases, chunks)
        summaries[method] = operational_summary(cases, traces, chunks)
    write(folder / "revalidation_log.json", {"changes": changed, "source_trace_sha256": hashes,
                                             "new_api_calls": 0, "additional_api_cost_usd": 0,
                                             "note": "Derived validation output, not a fresh model run or semantic grading. Original traces unchanged; manual labels reset for review."})
    all_attempted = all(s["completed_cases"] == len(cases) for s in summaries.values())
    complete = all_attempted and all(s["errors"] == 0 for s in summaries.values())
    write(folder / "operational_summary.json", {"all_cases_attempted": all_attempted, "complete_without_errors": complete,
          "configurations": summaries, "semantic_reviews_pending": True, "revalidation_only": True,
          "additional_api_cost_usd": 0, "test_read_or_run": False})
    write(ROOT / "results/part08/latest.json", {"run_directory": str(folder)})
    for change in changed:
        print(f"Revalidated {change['method']} {change['query_id']} -> {change['new_status']}")
    print(f"{'PASS' if complete else 'ERRORS_REMAIN'}: offline revalidation saved: {folder}\nNo API called. Original run preserved. Semantic review still required.")


if __name__ == "__main__":
    main()
