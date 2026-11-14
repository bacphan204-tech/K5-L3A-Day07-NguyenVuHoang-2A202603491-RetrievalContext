"""Separate actual context evidence, operational status and semantic labels."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from agent_evaluation import context_hit, review_template, operational_summary, reviews_ready


class AgentEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.chunk = {"id": "c", "source_id": "book", "page": 1, "text": "Full evidence."}
        self.case = {"id": "q", "answerable": True, "gold": [{"source_id": "book", "page": 1, "evidence": "Full evidence."}]}
        self.trace = {"query_id": "q", "status": "answered", "answer": "Claim [c]", "citations": ["c"],
                      "context": "Full evidence.", "context_ids": ["c"], "events": [{"event": "search"}],
                      "usage": {"estimated_api_cost_usd": 0.01}}

    def test_candidate_only_evidence_is_not_actual_context(self):
        self.assertTrue(context_hit(self.case, self.trace, [self.chunk]))
        self.assertFalse(context_hit(self.case, {**self.trace, "context_ids": []}, [self.chunk]))
        self.assertFalse(context_hit(self.case, {**self.trace, "context": "Truncated text"}, [self.chunk]))

    def test_semantic_labels_stay_pending_even_when_ids_are_valid(self):
        review = review_template(self.case, self.trace)
        self.assertEqual(review["citation_support"], [None])
        self.assertEqual(reviews_ready([self.case], [self.trace], [review]), ["q"])
        summary = operational_summary([self.case], [self.trace], [self.chunk])
        self.assertEqual(summary["citation_id_checks_only"], {"n": 1, "N": 1})
        self.assertIsNone(summary["manual_metrics"]["grounded_answer"])

    def test_errors_and_unanswerable_not_reported_as_quality_success(self):
        error = {**self.trace, "status": "error"}
        self.assertFalse(context_hit(self.case, error, [self.chunk]))
        self.assertIsNone(context_hit({"answerable": False}, self.trace, [self.chunk]))
        summary = operational_summary([self.case], [error], [self.chunk])
        self.assertEqual(summary["tool_use"], {"n": 0, "N": 0})
        self.assertEqual(summary["errors"], 1)


if __name__ == "__main__":
    unittest.main()
