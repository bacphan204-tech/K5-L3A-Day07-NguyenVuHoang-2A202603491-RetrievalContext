"""Verify transformations retain scope and reranking preserves source evidence."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from retrieval_improvements import clean_scope_query, sentence_spans, combine_sentence_scores


class ImprovementTests(unittest.TestCase):
    def test_only_matching_explicit_scope_is_removed(self):
        q = "Theo chương 3, giá trần là gì?"
        self.assertEqual(clean_scope_query(q, {"chapter": 3}), "giá trần là gì?")
        self.assertEqual(clean_scope_query(q), q)
        self.assertEqual(clean_scope_query(q, {"chapter": 4}), q)
        q34 = "Theo chương 34, giá trần là gì?"
        self.assertEqual(clean_scope_query(q34, {"chapter": 3}), q34)
        self.assertEqual(clean_scope_query("Theo chương 3", {"chapter": 3}), "Theo chương 3")

    def test_sentence_offsets_and_decimal_values_survive(self):
        text = "  The price is $1.40 per gallon. Next sentence!  Last fragment "
        spans = sentence_spans(text)
        self.assertEqual(len(spans), 3)
        self.assertEqual(spans[0]["text"], "The price is $1.40 per gallon.")
        for span in spans:
            self.assertEqual(text[span["start"]:span["end"]], span["text"])

    def test_rerank_uses_preset_weights_and_keeps_original_text(self):
        candidates = [{"id": "a", "text": "source A", "score": 0.9, "rank": 1},
                      {"id": "b", "text": "source B", "score": 0.8, "rank": 2}]
        scores = {"a": {"score": 0.2}, "b": {"score": 0.9}}
        result = combine_sentence_scores(candidates, scores)
        self.assertEqual(result[0]["id"], "b")
        self.assertAlmostEqual(result[0]["score"], 0.85)
        self.assertEqual(result[0]["text"], "source B")
        self.assertEqual(result[0]["dense_rank"], 2)
        self.assertEqual(candidates[0]["rank"], 1)


if __name__ == "__main__":
    unittest.main()
