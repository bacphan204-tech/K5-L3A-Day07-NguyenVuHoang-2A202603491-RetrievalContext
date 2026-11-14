"""Automatic operational/context checks; never infer semantic review labels."""
from collections import Counter
from retrieval_metrics import evidence_hit


def context_hit(case, trace, chunks):
    if not case["answerable"]:
        return None
    if trace["status"] == "error":
        return False
    ids = set(trace.get("context_ids", []))
    context = trace.get("context", "")
    return any(c["id"] in ids and evidence_hit(c, [g]) and g["evidence"] in context
               for g in case["gold"] for c in chunks)


def review_template(case, trace):
    return {"query_id": case["id"], "status": trace["status"], "answerable": case["answerable"],
            "context_grade": None, "answer_grade": None,
            "citation_support": [None for _ in trace.get("citations", [])],
            "abstention_correct": None, "reason": "", "reviewer": "", "student_confirmed": False}


def operational_summary(cases, traces, chunks):
    by_id = {c["id"]: c for c in cases}
    if len({t["query_id"] for t in traces}) != len(traces):
        raise ValueError("Duplicate query traces")
    successful = [t for t in traces if t["status"] != "error"]
    answerable = [t for t in traces if by_id[t["query_id"]]["answerable"]]
    errors = [t for t in traces if t["status"] == "error"]
    search_counts = [sum(e["event"] == "search" for e in t.get("events", [])) for t in successful]
    total_costs = [t.get("usage", {}).get("estimated_api_cost_usd") for t in traces]
    citation_count = sum(len(t.get("citations", [])) for t in successful)
    id_valid = sum(cid in t.get("context_ids", []) and f"[{cid}]" in t.get("answer", "")
                   for t in successful for cid in t.get("citations", []))
    return {"completed_cases": len(traces), "expected_cases": len(cases),
            "statuses": dict(Counter(t["status"] for t in traces)), "errors": len(errors),
            "tool_use": {"n": sum(n > 0 for n in search_counts), "N": len(successful)},
            "search_count_distribution": dict(sorted(Counter(search_counts).items())),
            "strict_context_evidence_rate": {"n": sum(bool(context_hit(by_id[t["query_id"]], t, chunks)) for t in answerable), "N": len(answerable)},
            "citation_id_checks_only": {"n": id_valid, "N": citation_count},
            "normalized_abstentions": sum(any(e["event"] == "abstention_normalized" for e in t.get("events", [])) for t in traces),
            "model_calls": sum(t.get("usage", {}).get("model_calls", 0) for t in traces),
            "input_tokens": sum(t.get("usage", {}).get("input_tokens", 0) for t in traces),
            "output_tokens": sum(t.get("usage", {}).get("output_tokens", 0) for t in traces),
            "estimated_api_cost_usd": sum(total_costs) if all(c is not None for c in total_costs) else None,
            "total_agent_seconds": sum(t.get("elapsed_seconds", 0) for t in traces),
            "manual_metrics": {"grounded_answer": None, "citation_semantic_validity": None,
                               "abstention_correct": None, "context_grade": None},
            "note": "Partial runs use completed-case denominators; report completion counts. Strict context uses quotes, not semantic review. API errors are separate; usage covers returned responses only."}


def reviews_ready(cases, traces, reviews):
    by_id = {r["query_id"]: r for r in reviews}
    pending = []
    for t in traces:
        if t["status"] == "error":
            continue
        r = by_id.get(t["query_id"])
        if r is None or not r.get("reason") or not r.get("reviewer"):
            pending.append(t["query_id"])
            continue
        valid = isinstance(r.get("citation_support"), list) and len(r["citation_support"]) == len(t["citations"]) and all(type(v) is bool for v in r["citation_support"])
        case = next(c for c in cases if c["id"] == t["query_id"])
        if case["answerable"]:
            valid = valid and type(r.get("answer_grade")) is int and r["answer_grade"] in (0, 1, 2)
            valid = valid and type(r.get("context_grade")) is int and r["context_grade"] in (0, 1, 2)
        else:
            valid = valid and type(r.get("abstention_correct")) is bool
        if not valid:
            pending.append(t["query_id"])
    return pending
