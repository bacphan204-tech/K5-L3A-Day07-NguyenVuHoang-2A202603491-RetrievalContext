"""Separate evaluator labels from the allowlisted inputs sent to the pipeline."""
import json
from pathlib import Path
import unicodedata


def load_cases(path):
    cases = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(cases, list) or not cases:
        raise ValueError("Benchmark must be a nonempty JSON array")
    return cases


def pipeline_input(case):
    """Never forward gold, answerability, expected answers or review notes."""
    result = {key: case[key] for key in ("id", "split", "question")}
    if case.get("filter"):
        result["filter"] = dict(case["filter"])
    return result


def validate_cases(cases, chunks):
    ids, questions = set(), set()
    counts = {s: {"answerable": 0, "unanswerable": 0} for s in ("dev", "test")}
    resolutions = {}
    for case in cases:
        cid = case.get("id")
        question = case.get("question")
        if not isinstance(cid, str) or not cid.strip() or cid in ids:
            raise ValueError("Missing or duplicate case ID")
        if not isinstance(question, str) or not question.strip():
            raise ValueError(f"{cid}: missing question")
        normalized = " ".join(unicodedata.normalize("NFC", question).casefold().split())
        if normalized in questions:
            raise ValueError(f"{cid}: duplicate question across benchmark splits")
        ids.add(cid)
        questions.add(normalized)
        split = case.get("split")
        if split not in counts or type(case.get("answerable")) is not bool:
            raise ValueError(f"{cid}: invalid split/answerable")
        filters = case.get("filter", {})
        if filters and (set(filters) != {"chapter"} or type(filters["chapter"]) is not int or filters["chapter"] not in (3, 4)):
            raise ValueError(f"{cid}: invalid chapter filter")
        if filters and not case.get("filter_provenance"):
            raise ValueError(f"{cid}: filter requires query/user provenance")
        kind = "answerable" if case["answerable"] else "unanswerable"
        counts[split][kind] += 1
        if case["answerable"]:
            if not case.get("expected_answer") or not case.get("gold"):
                raise ValueError(f"{cid}: missing expected answer/gold")
            resolutions[cid] = []
            for g in case["gold"]:
                if not isinstance(g.get("evidence"), str) or not g["evidence"].strip():
                    raise ValueError(f"{cid}: missing evidence quote")
                matches = [c["id"] for c in chunks if c["source_id"] == g.get("source_id")
                           and c["page"] == g.get("page") and g["evidence"] in c["text"]
                           and (not filters or c["metadata"]["chapter"] == filters["chapter"])]
                if not matches:
                    raise ValueError(f"{cid}: evidence not contained in a chunk with matching source/page/filter")
                resolutions[cid].append({"page": g["page"], "chunk_ids": matches})
        else:
            if case.get("gold") or case.get("expected_answer"):
                raise ValueError(f"{cid}: unanswerable case must not contain an answer/gold")
            if case.get("expected_behavior") != "search_and_abstain" or not case.get("absence_reason"):
                raise ValueError(f"{cid}: missing abstention behavior/reason")
            review = case.get("absence_review", {})
            if not review.get("search_terms") or not review.get("inspection_pages") or not review.get("reasoning"):
                raise ValueError(f"{cid}: document absence review is required")
    return {"counts": counts, "evidence_resolutions": resolutions}


def validate_minimums(counts):
    for split, required in (("dev", 15), ("test", 5)):
        if counts[split]["answerable"] < required or counts[split]["unanswerable"] < 2:
            raise ValueError(f"{split}: benchmark does not meet Day 7 minimum counts")
