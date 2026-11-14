"""Real offline E5 + Chroma retrieval over the frozen Day 6 B corpus."""
import argparse
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import shutil
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DAY6 = ROOT.parent / "K5-L3A-Day06-NguyenVuHoang-2A202603491-DataIngestionEngineering"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_hashes(folder):
    return {p.relative_to(folder).as_posix(): file_hash(p)
            for p in sorted(folder.rglob("*")) if p.is_file()}


def snapshot_store(day6):
    """Copy existing vectors/index locally; never open the original Chroma."""
    source = day6 / ".local/chroma"
    local_root = (ROOT / ".local").resolve()
    pointer = local_root / "day6_chroma_active.json"
    candidates = []
    if pointer.is_file():
        active = (local_root / load_json(pointer)["relative_path"]).resolve()
        if not active.is_relative_to(local_root) or active == local_root:
            raise ValueError("Active snapshot must stay inside the Day 7 .local directory")
        candidates.append(active)
    candidates.append(local_root / "day6_chroma")
    for candidate in candidates:
        marker = candidate / "day7_snapshot.json"
        if not marker.is_file() or not (candidate / "chroma.sqlite3").is_file():
            continue
        info = load_json(marker)
        recorded = Path(info["source_path"])
        if not recorded.exists() or not source.exists() or not recorded.samefile(source):
            raise ValueError(f"Snapshot source differs: recorded={recorded}; requested={source}")
        return candidate, info
    if not (source / "chroma.sqlite3").is_file():
        raise FileNotFoundError(f"Day 6 Chroma database is missing: {source}")
    snapshots = local_root / "day6_chroma_snapshots"
    snapshots.mkdir(parents=True, exist_ok=True)
    # Never rename/delete an existing database directory: Windows may hold it open.
    # A unique permanent directory also avoids cleaning up a live Chroma handle.
    target = Path(tempfile.mkdtemp(prefix="snapshot-", dir=snapshots))
    before = tree_hashes(source)
    shutil.copytree(source, target, dirs_exist_ok=True)
    if before != tree_hashes(source) or before != tree_hashes(target):
        raise RuntimeError("Day 6 database changed while copying. Stop the Day 6 demo and retry.")
    info = {"source_path": str(source.resolve()), "source_file_sha256": before,
            "note": "Original Chroma files copied without opening or re-embedding."}
    (target / "day7_snapshot.json").write_text(json.dumps(info, indent=2) + "\n", encoding="utf-8")
    # Publish only a small pointer file after the entire copy has verified.
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".json", dir=local_root, delete=False) as stream:
        json.dump({"relative_path": target.relative_to(local_root).as_posix()}, stream)
        pointer_temp = stream.name
    os.replace(pointer_temp, pointer)
    print(f"Created verified snapshot: {target} (existing database folders left untouched)")
    return target, info


class DenseRetriever:
    def __init__(self, day6=DEFAULT_DAY6):
        started = time.perf_counter()
        day6 = Path(day6).resolve()
        corpus = ROOT / "data/day6"
        report = load_json(corpus / "import_report.json")
        self.embedding_config = report["embedding"]
        self.chunks = {c["id"]: c for c in load_json(corpus / "chunks.json")}
        if len(self.chunks) != report["chunk_count"]:
            raise ValueError("Prepared corpus count does not match import report; rerun part 1")
        if file_hash(day6 / "results/chunks_B.jsonl") != report["input_sha256"]["results/chunks_B.jsonl"]:
            raise ValueError("Day 6 chunks changed since part 1; prepare the corpus again")
        model_path = day6 / ".local/models/multilingual-e5-small"
        model_info = load_json(model_path / "download_info.json")
        if model_info != {"model": self.embedding_config["model"], "revision": self.embedding_config["revision"]}:
            raise ValueError("Local model identity/revision does not match the Day 6 index")
        # Prevent downloads/cache writes outside this project during model loading.
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["TRANSFORMERS_OFFLINE"] = "1"
        os.environ["HF_HOME"] = str(ROOT / ".local/huggingface")
        os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
        from sentence_transformers import SentenceTransformer
        import torch
        import chromadb
        from chromadb.config import Settings
        torch.set_num_threads(min(4, os.cpu_count() or 1))
        self.model = SentenceTransformer(str(model_path), device="cpu", local_files_only=True)
        self.model.max_seq_length = 512
        if self.model.get_embedding_dimension() != self.embedding_config["dimensions"]:
            raise ValueError("Embedding model dimensions do not match the corpus")
        self.store_path, self.snapshot_info = snapshot_store(day6)
        self.client = chromadb.PersistentClient(path=str(self.store_path),
                                               settings=Settings(anonymized_telemetry=False))
        # get_collection intentionally fails instead of creating an empty database.
        self.collection = self.client.get_collection("economics_b", embedding_function=None)
        if self.collection.metadata.get("hnsw:space") != "cosine":
            raise ValueError("Expected the Day 6 cosine collection")
        stored = self.collection.get(include=["documents", "metadatas", "embeddings"])
        if len(stored["ids"]) != len(self.chunks) or set(stored["ids"]) != set(self.chunks):
            raise ValueError("Chroma IDs do not match the prepared corpus")
        for cid, text, metadata, vector in zip(stored["ids"], stored["documents"], stored["metadatas"], stored["embeddings"]):
            c = self.chunks[cid]
            if text != c["text"] or metadata["document_id"] != c["source_id"] or metadata["page"] != c["page"]:
                raise ValueError(f"Chroma text/source/page mismatch: {cid}")
            for key in ("chapter", "printed_page", "original_pdf_page", "start_char", "end_char"):
                if metadata[key] != c["metadata"][key]:
                    raise ValueError(f"Chroma metadata mismatch: {cid}/{key}")
            if len(vector) != 384 or not all(math.isfinite(float(v)) for v in vector):
                raise ValueError(f"Invalid stored vector: {cid}")
            if abs(math.sqrt(sum(float(v) ** 2 for v in vector)) - 1) > 1e-4:
                raise ValueError(f"Stored vector is not L2-normalized: {cid}")
        self.startup_seconds = time.perf_counter() - started
        self.last_timings = {}

    def search(self, query, *, filters=None, top_k=3):
        if not isinstance(query, str) or not query.strip():
            raise ValueError("Question must not be empty")
        if type(top_k) is not int or top_k < 1:
            raise ValueError("top_k must be a positive integer")
        if filters is not None and (set(filters) != {"chapter"} or type(filters["chapter"]) is not int or filters["chapter"] not in (3, 4)):
            raise ValueError("Only chapter 3 or 4 filters are supported")
        started = time.perf_counter()
        prefixed = self.embedding_config["query_prefix"] + query
        if len(self.model.tokenizer(prefixed, truncation=False)["input_ids"]) > 512:
            raise ValueError("Query exceeds 512 tokens; shorten it")
        vector = self.model.encode(prefixed, normalize_embeddings=True, show_progress_bar=False).tolist()
        embedded = time.perf_counter()
        found = self.collection.query(query_embeddings=[vector], n_results=min(top_k, len(self.chunks)),
                                      where=filters or None, include=["documents", "metadatas", "distances"])
        results = []
        for rank, (cid, distance) in enumerate(zip(found["ids"][0], found["distances"][0]), 1):
            results.append({**self.chunks[cid], "rank": rank, "score": 1 - float(distance),
                            "distance": float(distance), "strategy": "dense"})
        self.last_timings = {"embedding_seconds": embedded - started,
                             "vector_search_seconds": time.perf_counter() - embedded,
                             "total_query_seconds": time.perf_counter() - started}
        return results


def main():
    parser = argparse.ArgumentParser(description="Search the economics book using real local E5 + Chroma")
    parser.add_argument("--question", required=True)
    parser.add_argument("--chapter", type=int, choices=(3, 4))
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--day6", type=Path, default=DEFAULT_DAY6)
    parser.add_argument("--output", type=Path, default=ROOT / "results/part02/dense-last.json")
    args = parser.parse_args()
    filters = {"chapter": args.chapter} if args.chapter is not None else None
    trace = {"question": args.question, "strategy": "dense", "filter": filters, "top_k": args.top_k}
    try:
        retriever = DenseRetriever(args.day6)
        results = retriever.search(args.question, filters=filters, top_k=args.top_k)
        trace.update(status="success", results=results, model=retriever.embedding_config,
                     collection="economics_b", corpus_chunk_count=len(retriever.chunks),
                     startup_seconds=retriever.startup_seconds, timings=retriever.last_timings,
                     api_cost_usd=0, cost_note="Local CPU; electricity/hardware costs not measured",
                     packages={p: importlib.metadata.version(p) for p in ("sentence-transformers", "chromadb", "torch")},
                     note="Retrieval demo, not a benchmark score or an LLM-generated answer.")
    except Exception as exc:
        trace.update(status="error", error_type=type(exc).__name__, error=str(exc))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(trace, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        raise
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(trace, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nDENSE RETRIEVAL | {len(retriever.chunks)} chunks | E5 384 dimensions | economics_b")
    print(f"Question: {args.question}\nFilter: {filters}\n")
    for c in results:
        m = c["metadata"]
        print(f"#{c['rank']} | score={c['score']:.4f} | ID={c['id']}")
        print(f"PDF page {c['page']} | printed page {m['printed_page']} | chapter {m['chapter']}")
        print(f"Source: {c['source']}\n{c['text']}\n")
    print(f"PASS: real retrieval completed. Trace: {args.output}")


if __name__ == "__main__":
    main()
