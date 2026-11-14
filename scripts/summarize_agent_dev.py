"""Summarize saved dev traces and completed manual labels; no API calls."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from agent_evaluation import operational_summary, reviews_ready
sys.path.insert(0, str(ROOT / "starter"))
from agent_metrics import aggregate


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path)
    args = parser.parse_args()
    folder = args.run or Path(load(ROOT / "results/part08/latest.json")["run_directory"])
    cases = load(folder / "cases.json")
    chunks = load(ROOT / "data/day6/chunks.json")
    report = {"run_directory": str(folder), "configurations": {}}
    for method in ("dense", "rerank"):
        directory = folder / method
        traces, reviews = load(directory / "traces.json"), load(directory / "reviews.json")
        summary = operational_summary(cases, traces, chunks)
        pending = reviews_ready(cases, traces, reviews)
        entry = {"operational": summary, "pending_review_query_ids": pending, "manual_metrics": None}
        if not pending and len(traces) == len(cases):
            semantic = aggregate(cases, traces, reviews)
            valid_context = [r for r in reviews if next(c for c in cases if c["id"] == r["query_id"])["answerable"]
                             and r["context_grade"] is not None
                             and next(t for t in traces if t["query_id"] == r["query_id"])["status"] != "error"]
            semantic["manual_context_evidence_rate"] = {"n": sum(r["context_grade"] == 2 for r in valid_context), "N": len(valid_context)}
            semantic["manual_context_grade_distribution"] = {str(n): sum(r["context_grade"] == n for r in valid_context) for n in (0, 1, 2)}
            entry["manual_metrics"] = semantic
        report["configurations"][method] = entry
        rate = summary["strict_context_evidence_rate"]
        print(f"{method}: {summary['completed_cases']}/{summary['expected_cases']} completed; statuses={summary['statuses']}; strict context={rate['n']}/{rate['N']}; estimated USD={summary['estimated_api_cost_usd']}; pending semantic reviews={len(pending)}")
    destination = folder / "evaluation_summary.json"
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    split = cases[0]["split"] if cases else "unknown"
    print(f"Saved: {destination}\nNo API called; summarized saved {split} records only. Unfilled semantic labels remain pending.")


if __name__ == "__main__":
    main()
