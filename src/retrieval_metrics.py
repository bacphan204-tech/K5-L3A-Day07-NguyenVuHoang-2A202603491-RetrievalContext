"""Strict evidence metrics, kept outside retrieval and model inputs."""
import statistics


def evidence_hit(chunk, gold):
    return any(chunk["source_id"] == g["source_id"] and chunk["page"] == g["page"]
               and g["evidence"] in chunk["text"] for g in gold)


def grade_retrieval(case, results, status="success"):
    if not case["answerable"]:
        return {"hit1": None, "hit3": None, "retrieval_applicable": False}
    return {"hit1": status == "success" and bool(results) and evidence_hit(results[0], case["gold"]),
            "hit3": status == "success" and any(evidence_hit(c, case["gold"]) for c in results[:3]),
            "retrieval_applicable": True}


def summarize(traces, method):
    rows = [t for t in traces if t["method"] == method]
    eligible = [t for t in rows if t["retrieval_applicable"]]
    successful = [t for t in rows if t["status"] == "success"]
    def metric(key):
        n, total = sum(bool(t[key]) for t in eligible), len(eligible)
        return {"n": n, "N": total, "rate": n / total if total else None}
    durations = [t["query_seconds"] for t in successful]
    return {"method": method, "queries": len(rows), "successful_queries": len(successful),
            "errors": len(rows) - len(successful), "answerable_errors": sum(t["status"] == "error" for t in eligible),
            "hit1": metric("hit1"), "evidence_hit3": metric("hit3"),
            "empty_results": sum(not t["results"] for t in successful),
            "median_query_seconds": statistics.median(durations) if durations else None,
            "total_query_seconds": sum(durations), "api_cost_usd": 0,
            "context_evidence_rate": None, "agent_metrics": None,
            "error_policy": "Fixed answerable denominator; retrieval errors count as misses and are reported separately."}
