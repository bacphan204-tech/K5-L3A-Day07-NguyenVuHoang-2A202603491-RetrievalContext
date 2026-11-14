"""Persist explicit source-read AI review decisions, never claim student confirmation."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from dense_retrieval import file_hash, load_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--decisions", type=Path, required=True)
    args = parser.parse_args()
    decisions = load_json(args.decisions)
    cases = {c["id"]: c for c in load_json(args.run / "cases.json")}
    split = next(iter(cases.values()))["split"]
    for method in ("dense", "rerank"):
        traces = {t["query_id"]: t for t in load_json(args.run / method / "traces.json")}
        rows = []
        for entry in decisions[method]:
            suffix, context_grade, answer_grade, support, reason, *extra = entry
            cid = suffix if suffix in cases else f"d7-{split}-{suffix}"
            case, trace = cases[cid], traces[cid]
            if len(support) != len(trace["citations"]):
                raise ValueError(f"{method}/{cid}: citation label count differs")
            row = {"query_id": cid, "answerable": case["answerable"], "status": trace["status"],
                   "context_grade": context_grade, "answer_grade": answer_grade, "citation_support": support,
                   "abstention_correct": extra[0] if extra else None, "reason": reason,
                   "reviewer": decisions["reviewer"], "student_confirmed": False,
                   "source_trace_sha256": file_hash(args.run / method / "traces" / f"{cid}.json"),
                   "review_decisions_sha256": file_hash(args.decisions)}
            rows.append(row)
        if set(traces) != {r["query_id"] for r in rows}:
            raise ValueError("Missing or extra semantic reviews")
        (args.run / method / "reviews.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PASS: explicit AI source-read labels saved; student_confirmed remains false.")


if __name__ == "__main__":
    main()
