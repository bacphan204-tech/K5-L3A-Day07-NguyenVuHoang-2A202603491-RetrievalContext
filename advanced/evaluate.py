"""Aggregate source-reviewed case labels and test traces without judging answers automatically."""
import hashlib
import json
import argparse
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "advanced"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate(test_name="test", run_name=None, output_name=None, evaluation_scope=None):
    cases = load(HERE / "benchmark" / f"{test_name}.json")
    lock_path = HERE / ("frozen.json" if test_name == "test" else f"frozen-{test_name}.json")
    lock = load(lock_path)
    grades = load(HERE / "benchmark" / f"{test_name}.review.json")
    if lock["gold_sha256"] != hashlib.sha256(
        (HERE / "benchmark" / f"{test_name}.json").read_bytes()
    ).hexdigest():
        raise ValueError("Gold benchmark differs from the frozen test lock.")
    if lock["inputs_sha256"] != hashlib.sha256(
        (HERE / "benchmark" / f"{test_name}.inputs.json").read_bytes()
    ).hexdigest():
        raise ValueError("Test inputs differ from the frozen test lock.")

    grades_by_id = {grade["id"]: grade for grade in grades}
    expected_ids = {case["id"] for case in cases}
    if len(grades) != len(expected_ids) or set(grades_by_id) != expected_ids:
        raise ValueError(f"{test_name}.review.json must contain exactly one reviewed label per test case.")

    run_dir = HERE / "runs" / (run_name or f"{test_name}-vision")
    output = []
    seconds = []
    costs = []
    errors = 0
    for case in cases:
        grade = grades_by_id[case["id"]]
        if grade.get("decision") not in {"pass", "fail"}:
            raise ValueError(f"{case['id']} needs a pass/fail source-review decision.")
        if not grade.get("reason") or not grade.get("source_check"):
            raise ValueError(f"{case['id']} needs a scoring reason and source check.")

        trace_path = run_dir / f"{case['id']}.json"
        trace = load(trace_path) if trace_path.exists() else None
        trace_status = trace.get("status", "missing") if trace else "missing"
        required_fields = ("final", "context", "retrieval_queries", "calls", "usage", "seconds")
        complete_trace = trace is not None and all(field in trace for field in required_fields)
        if trace_status == "success" and complete_trace:
            final = trace["final"]
            complete_trace = (
                isinstance(final, dict)
                and final.get("status") in {"answered", "abstain"}
                and isinstance(final.get("answer"), str)
                and isinstance(final.get("pages"), list)
            )
        system_error = trace_status != "success" or not complete_trace
        if system_error and trace_status == "success":
            trace_status = "incomplete"
        errors += int(system_error)
        passed = grade["decision"] == "pass" and not system_error
        if trace and isinstance(trace.get("seconds"), (int, float)):
            seconds.append(trace["seconds"])
        usage = trace.get("usage", {}) if trace else {}
        cost = usage.get("estimated_api_cost_usd")
        if cost is not None:
            costs.append(cost)
        output.append({
            "id": case["id"],
            "group": case["group"],
            "answerable": case["answerable"],
            "decision": "pass" if passed else "fail",
            "review_decision": grade["decision"],
            "reason": grade["reason"],
            "source_check": grade["source_check"],
            "reviewer": grade.get("reviewer", "unspecified"),
            "trace_status": trace_status,
            "system_error": system_error,
            "seconds": trace.get("seconds") if trace else None,
            "estimated_api_cost_usd": cost,
            "trace_path": str(trace_path.relative_to(ROOT)).replace("\\", "/"),
        })

    groups = {}
    for group in sorted({case["group"] for case in cases}):
        rows = [row for row in output if row["group"] == group]
        groups[group] = {
            "passed": sum(row["decision"] == "pass" for row in rows),
            "total": len(rows),
            "rate": sum(row["decision"] == "pass" for row in rows) / len(rows),
        }

    passed = sum(row["decision"] == "pass" for row in output)
    total = len(output)
    all_costs_known = len(costs) == total
    result = {
        "status": "complete",
        "vision": True,
        "model": lock["model_settings"]["model"],
        "passed": passed,
        "total": total,
        "rate": passed / total if total else 0,
        "required_passes_for_90_percent": (9 * total + 9) // 10,
        "threshold_met": bool(total and passed / total >= 0.9),
        "evaluation_scope": evaluation_scope or "locked benchmark run",
        "errors": errors,
        "mean_seconds_per_case_with_trace": statistics.mean(seconds) if seconds else None,
        "timed_cases": len(seconds),
        "estimated_api_cost_usd": sum(costs) if all_costs_known else None,
        "known_cost_cases": len(costs),
        "by_group": groups,
        "cases": output,
        "review_note": "Pass/fail labels require case-by-case source review; system errors and missing traces always fail.",
    }
    destination = HERE / "reports" / (output_name or f"{test_name}-vision-evaluation.json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items() if key != "cases"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-name", choices=("test", "test-v2"), default="test")
    parser.add_argument("--run-name")
    parser.add_argument("--output-name")
    parser.add_argument("--evaluation-scope")
    args = parser.parse_args()
    evaluate(args.test_name, args.run_name, args.output_name, args.evaluation_scope)
