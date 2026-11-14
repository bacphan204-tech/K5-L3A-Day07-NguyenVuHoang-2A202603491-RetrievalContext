"""Offline protocol checks only; these are not real-model quality scores."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from book_agent import run_book_agent, pack_context, validate_final
from llm_client import read_settings, public_settings, ResponsesClient

CID = "a" * 24
CHUNK = {"id": CID, "source": "book.pdf", "page": 36, "text": "Job seekers supply labor."}


class FakeClient:
    def __init__(self, actions):
        self.actions, self.requests = iter(actions), []
    def call(self, messages, tools, force_tool=None):
        self.requests.append(messages)
        name, args = next(self.actions)
        return {"type": "function_call", "call_id": "call-1", "name": name, "arguments": json.dumps(args)}, args
    def usage(self):
        return {"test_only": True}


class FakeRetriever:
    def search(self, query, *, filters, top_k):
        return [CHUNK]


class BookAgentTests(unittest.TestCase):
    def test_search_then_cited_answer_has_bounded_actual_context(self):
        client = FakeClient([("search_book", {"query": "labor supply"}),
                             ("finish_answer", {"status": "answered", "answer": f"Người tìm việc [{CID}]", "citations": [CID]})])
        result = run_book_agent("Ai cung ứng lao động?", client, FakeRetriever(), budget=100)
        self.assertEqual(result["status"], "answered")
        self.assertLessEqual(len(result["context"]), 100)
        self.assertEqual(result["context_ids"], [CID])
        self.assertEqual(sum(e["event"] == "search" for e in result["events"]), 1)

    def test_invalid_citation_is_error_not_fake_success_or_abstention(self):
        with self.assertRaises(ValueError):
            validate_final({"status": "answered", "answer": "Claim [" + "b"*24 + "]", "citations": ["b"*24]}, [CID])

    def test_abstention_does_not_keep_unsupported_claims(self):
        final = validate_final({"status": "abstain", "answer": "Not enough evidence, but maybe 10%", "citations": []}, [])
        self.assertEqual(final["status"], "abstain")
        self.assertNotIn("10%", final["answer"])

    def test_explicit_abstain_can_have_empty_raw_answer(self):
        result = validate_final({"status": "abstain", "answer": "", "citations": []}, [])
        self.assertEqual(result["status"], "abstain")
        self.assertTrue(result["answer"])

    def test_only_model_selected_context_citations_get_inline_formatting(self):
        raw = {"status": "answered", "answer": "Claim.", "citations": [CID]}
        result = validate_final(raw, [CID])
        self.assertEqual(result["answer"], f"Claim. [{CID}]")
        self.assertEqual(raw["answer"], "Claim.")
        with self.assertRaises(ValueError):
            validate_final(raw, [])
        with self.assertRaises(ValueError):
            validate_final({**raw, "answer": "Claim [" + "b"*24 + "]"}, [CID])

    def test_abstention_citations_are_normalized_with_raw_decision_preserved(self):
        raw = {"status": "abstain", "answer": "Evidence is insufficient.", "citations": [CID]}
        client = FakeClient([("search_book", {"query": "minimum wage Vietnam 2026"}), ("finish_answer", raw)])
        result = run_book_agent("What is the exact wage?", client, FakeRetriever())
        self.assertEqual(result["status"], "abstain")
        self.assertEqual(result["citations"], [])
        self.assertEqual(result["normalization"]["removed_citations"], [CID])
        final_event = next(e for e in result["events"] if e["event"] == "answer")
        self.assertEqual(final_event["model_final"], raw)
        self.assertEqual(raw["citations"], [CID])

    def test_context_deduplicates_and_does_not_cut_chunks(self):
        text, ids = pack_context([CHUNK, CHUNK], 100)
        self.assertEqual(ids, [CID])
        self.assertEqual(pack_context([CHUNK], 1), ("", []))

    def test_missing_key_and_redacted_public_settings(self):
        with tempfile.TemporaryDirectory() as temp, patch.dict("os.environ", {}, clear=True):
            path = Path(temp) / ".env"
            path.write_text("OPENAI_API_KEY=\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Missing OPENAI_API_KEY"):
                read_settings(path)
            path.write_text("OPENAI_API_KEY=test-only-secret\n", encoding="utf-8")
            settings = read_settings(path)
            self.assertNotIn("test-only-secret", json.dumps(public_settings(settings)))

    def test_native_api_request_and_trace_do_not_contain_authorization(self):
        settings = {"api_key": "test-only-secret", "base_url": "https://api.openai.com/v1", "model": "test-model",
                    "timeout_seconds": 1, "max_output_tokens": 200}
        response = {"status": "completed", "output": [{"type": "function_call", "name": "probe", "call_id": "c1", "arguments": '{"ok":true}'}],
                    "usage": {"input_tokens": 10, "output_tokens": 5}}
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def read(self): return json.dumps(response).encode()
        client = ResponsesClient(settings)
        with patch("llm_client.urlopen", return_value=Response()) as request:
            call, args = client.call([{"role": "user", "content": "probe"}], [], force_tool="probe")
        self.assertEqual(args, {"ok": True})
        self.assertEqual(request.call_args.args[0].get_header("Authorization"), "Bearer test-only-secret")
        self.assertNotIn("test-only-secret", json.dumps(client.calls))
        self.assertIsNone(client.usage()["estimated_api_cost_usd"])


if __name__ == "__main__":
    unittest.main()
