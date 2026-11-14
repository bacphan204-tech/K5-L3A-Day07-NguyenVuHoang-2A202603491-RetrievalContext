"""Validate and lock the advanced benchmark before its first test run."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "advanced"
sys.path.insert(0, str(ROOT / "src"))
from llm_client import read_settings


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def runtime_settings():
    settings = read_settings()
    settings["max_output_tokens"] = 2400
    return {
        "model": settings["model"],
        "timeout_seconds": settings["timeout_seconds"],
        "max_output_tokens": settings["max_output_tokens"],
        "endpoint_sha256": digest_text(settings["base_url"]),
    }


def digest_text(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def validate_split(split, test_name="test"):
    benchmark_name = "dev" if split == "dev" else test_name
    benchmark_path = HERE / "benchmark" / f"{benchmark_name}.json"
    inputs_path = HERE / "benchmark" / f"{benchmark_name}.inputs.json"
    cases = load(benchmark_path)
    inputs = load(inputs_path)
    if not isinstance(cases, list) or not isinstance(inputs, list):
        raise ValueError(f"{benchmark_name} benchmark and inputs must be JSON arrays.")
    if len({case.get("id") for case in cases}) != len(cases):
        raise ValueError(f"{benchmark_name} benchmark contains duplicate or missing IDs.")

    answerable = [case for case in cases if case.get("answerable") is True]
    unanswerable = [case for case in cases if case.get("answerable") is False]
    counts = Counter(case.get("group") for case in cases)
    if split == "dev":
        if len(answerable) < 15 or len(unanswerable) < 3:
            raise ValueError("Dev requires at least 15 answerable and 3 unanswerable cases.")
    else:
        minimums = {
            "table": 6,
            "diagram": 5,
            "chart": 5,
            "multi_hop": 4,
            "text": 4,
            "unanswerable": 6,
        }
        if len(cases) < 30 or len(answerable) < 24 or len(unanswerable) < 6:
            raise ValueError("Test requires at least 30 cases: 24 answerable and 6 unanswerable.")
        for group, minimum in minimums.items():
            if counts[group] < minimum:
                raise ValueError(f"Test group {group!r} has fewer than {minimum} cases.")

    for case in answerable:
        if not case.get("question") or not case.get("expected_answer"):
            raise ValueError(f"{case.get('id')} is missing its question or gold answer.")
        if not case.get("gold_pages") or not case.get("evidence_description"):
            raise ValueError(f"{case.get('id')} is missing source evidence.")
        if case.get("group") == "multi_hop" and len(set(case["gold_pages"])) < 2:
            raise ValueError(f"{case.get('id')} does not require evidence from two distinct pages.")
    for case in unanswerable:
        if not case.get("question") or not case.get("absence_reason"):
            raise ValueError(f"{case.get('id')} is missing its absence rationale.")

    expected_inputs = [
        {"id": case["id"], "question": case["question"], "group": case["group"]}
        for case in cases
    ]
    if inputs != expected_inputs:
        raise ValueError(f"{benchmark_name}.inputs.json must contain only the published questions and groups.")
    return cases, counts


def create_lock(test_name="test"):
    lock_path = HERE / ("frozen.json" if test_name == "test" else f"frozen-{test_name}.json")
    if lock_path.exists():
        raise FileExistsError(f"{lock_path.relative_to(ROOT)} already exists; refusing to replace the test lock.")

    dev, _ = validate_split("dev")
    test, _ = validate_split("test", test_name)
    dev_questions = {case["question"].strip().casefold() for case in dev}
    if any(case["question"].strip().casefold() in dev_questions for case in test):
        raise ValueError("Dev and test contain an identical question.")

    manifest = load(ROOT / "data" / "advanced" / "manifest.json")
    corpus = ROOT / "data" / "advanced" / "economics-120-pages.pdf"
    pages = load(ROOT / "data" / "advanced" / "pages.json")
    chunks = load(ROOT / "data" / "advanced" / "chunks.json")
    if manifest.get("physical_pages", 0) < 100:
        raise ValueError("Advanced corpus must contain at least 100 pages.")
    if manifest.get("indexed_text_pages", 0) < 100:
        raise ValueError("At least 100 pages must be text-indexed.")
    if len(pages) != manifest["physical_pages"] or len(chunks) != manifest["chunks"]:
        raise ValueError("Advanced page/chunk counts do not match the corpus manifest.")
    if len(manifest.get("original_page_mapping", [])) != manifest["physical_pages"]:
        raise ValueError("Original PDF page mapping is incomplete.")
    if digest(corpus) != manifest.get("sha256"):
        raise ValueError("Advanced PDF hash does not match its manifest.")

    lock = {
        "lock_version": 1,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "vision": True,
        "model_settings": runtime_settings(),
        "retrieval": {
            "method": "BM25 over page chunks; reciprocal-rank fusion over up to three model queries",
            "candidate_depth": 40,
            "rrf_constant": 60,
            "context_pages": 6,
            "figure_table_reference_boost": 1,
            "visual_context": "full-page source images rendered at 1.3x",
        },
        "inputs_sha256": digest(HERE / "benchmark" / f"{test_name}.inputs.json"),
        "gold_sha256": digest(HERE / "benchmark" / f"{test_name}.json"),
        "chunks_sha256": digest(ROOT / "data" / "advanced" / "chunks.json"),
        "pages_sha256": digest(ROOT / "data" / "advanced" / "pages.json"),
        "source_pdf_sha256": digest(corpus),
        "code_sha256": {
            "workflow.py": digest(HERE / "workflow.py"),
            "llm_client.py": digest(ROOT / "src" / "llm_client.py"),
            "lexical_retrieval.py": digest(ROOT / "src" / "lexical_retrieval.py"),
        },
        "test_count": len(test),
    }
    lock_path.write_text(json.dumps(lock, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Frozen {len(test)} {test_name} cases; vision={lock['vision']}; model={lock['model_settings']['model']}.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-name", choices=("test", "test-v2"), default="test")
    create_lock(parser.parse_args().test_name)
