"""Ask the real OpenAI-powered book agent, or check API configuration first."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from llm_client import ResponsesClient, read_settings, public_settings
from book_agent import run_book_agent, tool, PROMPT_VERSION


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--question")
    parser.add_argument("--chapter", type=int, choices=(3, 4))
    parser.add_argument("--check-config", action="store_true")
    parser.add_argument("--check-api", action="store_true")
    parser.add_argument("--retrieval", choices=("dense", "rerank"), default="rerank")
    parser.add_argument("--max-searches", type=int, default=3)
    parser.add_argument("--budget", type=int, default=5000)
    args = parser.parse_args()
    try:
        settings = read_settings()
    except ValueError as exc:
        print(f"CONFIG ERROR: {exc}")
        return 1
    client = ResponsesClient(settings)
    if args.check_config:
        print(json.dumps({"status": "PASS", "key_configured": True, "config": public_settings(settings), "api_called": False}, indent=2))
        return 0
    folder = ROOT / "results/part07" / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:6])
    folder.mkdir(parents=True, exist_ok=False)
    result = {}
    try:
        if args.check_api:
            probe = tool("connection_ok", "Confirm the API connection and tool calling work.", {"ok": {"type": "boolean"}})
            call, values = client.call([{"role": "user", "content": "Call connection_ok with ok=true."}], [probe], force_tool="connection_ok")
            if values != {"ok": True}:
                raise ValueError("API probe did not return ok=true")
            result = {"status": "success", "check": "API and native tool calling", "usage": client.usage()}
        else:
            if not args.question:
                raise ValueError("Provide --question, --check-config or --check-api")
            from dense_retrieval import DenseRetriever, file_hash
            from agent_retriever import BookRetriever
            print("Loading local E5/Chroma; LLM generation uses OpenAI API...", flush=True)
            dense = DenseRetriever()
            retriever = BookRetriever(dense, args.retrieval)
            result = run_book_agent(args.question, client, retriever, filters={"chapter": args.chapter} if args.chapter else None,
                                    max_searches=args.max_searches, budget=args.budget)
            result["retrieval"] = args.retrieval
            result["embedding"] = dense.embedding_config
            result["corpus_sha256"] = file_hash(ROOT / "data/day6/chunks.json")
    except Exception as exc:
        result = {"status": "error", "error_type": type(exc).__name__, "error": str(exc), "usage": client.usage()}
    result["llm_config"] = public_settings(settings)
    result["model_calls"] = client.calls
    result["prompt_version"] = PROMPT_VERSION
    trace = folder / "trace.json"
    trace.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nSTATUS: {result['status']}")
    print(result.get("answer") or result.get("error") or "API connection and tool calling succeeded.")
    print("Usage: " + json.dumps(result.get("usage"), ensure_ascii=False))
    print(f"Trace: {trace}")
    return int(result["status"] == "error")


if __name__ == "__main__":
    sys.exit(main())
