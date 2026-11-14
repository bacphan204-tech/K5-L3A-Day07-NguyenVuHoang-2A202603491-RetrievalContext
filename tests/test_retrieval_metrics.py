"""Ensure fixed cutoffs/denominators and source evidence checks are honest."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from retrieval_metrics import evidence_hit, grade_retrieval, summarize


class RetrievalMetricTests(unittest.TestCase):
    def setUp(self):
        self.case = {"answerable": True, "gold": [{"source_id": "book", "page": 2, "evidence": "full evidence"}]}
        self.good = {"source_id": "book", "page": 2, "text": "The full evidence here."}
        self.wrong = {**self.good, "page": 1}

    def test_hit_requires_source_and_page_and_whole_quote(self):
        self.assertTrue(evidence_hit(self.good, self.case["gold"]))
        self.assertFalse(evidence_hit(self.wrong, self.case["gold"]))
        self.assertFalse(evidence_hit({**self.good, "text": "evidence"}, self.case["gold"]))

    def test_evidence_at_rank_four_is_not_hit_three(self):
        score = grade_retrieval(self.case, [self.wrong] * 3 + [self.good])
        self.assertFalse(score["hit1"])
        self.assertFalse(score["hit3"])
        self.assertTrue(grade_retrieval(self.case, [self.wrong, self.good])["hit3"])

    def test_unanswerable_excluded_and_errors_keep_fixed_denominator(self):
        rows = []
        for case, results, status in ((self.case, [self.good], "success"),
                                       (self.case, [], "error"),
                                       ({"answerable": False}, [], "success")):
            rows.append({"method": "dense", "status": status, "results": results,
                         "query_seconds": 0.1, **grade_retrieval(case, results, status)})
        result = summarize(rows, "dense")
        self.assertEqual(result["hit1"], {"n": 1, "N": 2, "rate": 0.5})
        self.assertEqual(result["errors"], 1)
        self.assertEqual(result["successful_queries"], 2)
        self.assertIsNone(result["context_evidence_rate"])
        self.assertIsNone(rows[-1]["hit1"])


if __name__ == "__main__":
    unittest.main()
