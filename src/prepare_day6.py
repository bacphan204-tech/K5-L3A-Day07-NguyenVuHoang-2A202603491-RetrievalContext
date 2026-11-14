"""Import the frozen Day 6 B corpus without changing the source project.

Run from the Day 7 root: python -X utf8 src/prepare_day6.py
Only corpus data is imported; old benchmark answers never enter this export.
"""
import argparse
import hashlib
import importlib
import importlib.util
import json
import shutil
import sys
from collections import Counter
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DAY6 = ROOT.parent / "K5-L3A-Day06-NguyenVuHoang-2A202603491-DataIngestionEngineering"


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_day6_pages(day6):
    """Load the sibling project's package explicitly, without sys.path ambiguity."""
    package_path = day6 / "starter/src"
    name = "_day6_" + hashlib.sha256(str(day6).encode()).hexdigest()[:12]
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(
            name, package_path / "__init__.py", submodule_search_locations=[str(package_path)])
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load Day 6 package: {package_path}")
        package = importlib.util.module_from_spec(spec)
        sys.modules[name] = package
        spec.loader.exec_module(package)
    ingestion = importlib.import_module(name + ".ingestion")
    return [asdict(p) for p in ingestion.load_corpus(day6)]


def prepare(day6, output):
    day6, output = day6.resolve(), output.resolve()
    if output == day6 or day6 in output.parents:
        raise ValueError("Output must be outside the Day 6 project")
    manifest_path = day6 / "data/manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    config_path = day6 / "artifacts/strategies.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    chunk_path = day6 / "results/chunks_B.jsonl"
    page_path = day6 / "data/processed/pages.jsonl"
    pdf = day6 / manifest["source_path_or_url"]
    if sha256(pdf) != manifest["snapshot"]["sha256"]:
        raise ValueError("Day 6 PDF does not match the recorded SHA-256")
    # Offsets refer to normalized text, not the raw extraction JSONL.
    # Reuse the original normalizer rather than subtly changing its rules.
    pages = load_day6_pages(day6)
    by_page = {p["page"]: p for p in pages}
    if len(by_page) != len(pages) or len(pages) != manifest["selected_page_count"]:
        raise ValueError("Duplicate or unexpected source pages")
    raw = read_jsonl(chunk_path)
    chunks, seen = [], set()
    for c in raw:
        cid, metadata = c["chunk_id"], c["metadata"]
        if cid in seen or not c["text"].strip():
            raise ValueError(f"Duplicate ID or empty chunk: {cid}")
        seen.add(cid)
        page = by_page[c["page"]]
        if c["document_id"] != manifest["source_id"] or c["document_id"] != page["document_id"]:
            raise ValueError(f"Source mismatch: {cid}")
        if c["source"] != page["source"] or page["text"][metadata["start_char"]:metadata["end_char"]] != c["text"]:
            raise ValueError(f"Text/source/offset mismatch: {cid}")
        if metadata["chapter"] not in (3, 4) or metadata["chapter"] != page["metadata"]["chapter"]:
            raise ValueError(f"Chapter mismatch: {cid}")
        chunks.append({"id": cid, "text": c["text"], "source_id": c["document_id"],
                       "source": "data/day6/economics-chapters-3-4.pdf",
                       "page": c["page"], "metadata": {**metadata, "day6_source": c["source"]}})
    if not chunks or set(by_page) != {c["page"] for c in chunks}:
        raise ValueError("Chunks must cover all selected source pages")
    output.mkdir(parents=True, exist_ok=True)
    # Keep a fixed citation path; custom output is for inspection/export only.
    write_json(output / "chunks.json", chunks)
    write_json(output / "pages.json", pages)
    shutil.copyfile(pdf, output / pdf.name)
    shutil.copyfile(manifest_path, output / "source_manifest.json")
    shutil.copyfile(day6 / "data/excerpt_page_map.csv", output / "excerpt_page_map.csv")
    shutil.copyfile(config_path, output / "day6_strategies.json")
    report = {
        "strategy": "B", "chunk_count": len(chunks), "content_pages": len(pages),
        "physical_pdf_pages": manifest["snapshot"]["total_physical_pages"],
        "chunks_by_chapter": dict(sorted(Counter(str(c["metadata"]["chapter"]) for c in chunks).items())),
        "embedding": {"model": config["model"], "revision": config["model_revision"],
                      "dimensions": 384, "query_prefix": "query: ", "document_prefix": "passage: ",
                      "normalize_embeddings": True},
        "vector_store": {"backend": config["vector_store"], "collection": "economics_b",
                         "metric": config["metric"],
                         "day6_database_file_exists": (day6 / ".local/chroma/chroma.sqlite3").is_file(),
                         "opened_or_queried": False},
        "checks": {"unique_ids": True, "source_page_offsets_match": True,
                   "all_content_pages_covered": True, "pdf_hash_matches": True},
        "input_sha256": {str(p.relative_to(day6)).replace("\\", "/"): sha256(p)
                         for p in (manifest_path, config_path, chunk_path, page_path, pdf,
                                   day6 / "starter/src/ingestion.py", day6 / "starter/src/models.py")},
        "benchmark_imported": False,
        "note": "Corpus import only. This is not a retrieval benchmark or a live database check."
    }
    write_json(output / "import_report.json", report)
    return report


def main():
    parser = argparse.ArgumentParser(description="Prepare Day 7 corpus from Day 6 strategy B")
    parser.add_argument("--day6", type=Path, default=DEFAULT_DAY6)
    args = parser.parse_args()
    report = prepare(args.day6, ROOT / "data/day6")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("\nPASS: Day 6 B corpus is ready in data/day6. No benchmark/model run performed.")


if __name__ == "__main__":
    main()
