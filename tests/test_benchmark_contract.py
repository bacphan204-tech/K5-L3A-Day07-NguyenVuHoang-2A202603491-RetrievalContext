"""Guard evaluator-label isolation, evidence provenance and split integrity."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from benchmark import pipeline_input, validate_cases, validate_minimums


class BenchmarkContractTests(unittest.TestCase):
    def setUp(self):
        self.chunk = {"id": "c1", "text": "A price ceiling is a legal maximum price.",
                      "source_id": "book", "page": 26, "metadata": {"chapter": 3}}
        self.case = {"id": "dev-1", "split": "dev", "question": "Theo chương 3, giá trần là gì?",
                     "answerable": True, "expected_answer": "Mức giá tối đa hợp pháp.",
                     "gold": [{"source_id": "book", "page": 26, "evidence": "legal maximum price"}],
                     "filter": {"chapter": 3}, "filter_provenance": "Chapter stated in question",
                     "review_status": "private evaluator notes"}

    def test_only_allowlisted_fields_reach_pipeline(self):
        exposed = pipeline_input(self.case)
        self.assertEqual(set(exposed), {"id", "split", "question", "filter"})
        exposed["filter"]["chapter"] = 4
        self.assertEqual(self.case["filter"]["chapter"], 3)

    def test_matching_words_on_wrong_page_are_not_evidence(self):
        bad = deepcopy(self.case)
        bad["gold"][0]["page"] = 27
        with self.assertRaisesRegex(ValueError, "source/page/filter"):
            validate_cases([bad], [self.chunk])
        good = validate_cases([self.case], [self.chunk])
        self.assertEqual(good["evidence_resolutions"]["dev-1"][0]["chunk_ids"], ["c1"])

    def test_duplicate_question_across_splits_is_rejected(self):
        other = {**self.case, "id": "test-1", "split": "test"}
        with self.assertRaisesRegex(ValueError, "duplicate question"):
            validate_cases([self.case, other], [self.chunk])

    def test_unanswerable_requires_document_scope_review(self):
        case = {"id": "u1", "split": "dev", "question": "What is the 2026 rate?",
                "answerable": False, "expected_behavior": "search_and_abstain",
                "absence_reason": "No location/year data"}
        with self.assertRaisesRegex(ValueError, "absence review"):
            validate_cases([case], [self.chunk])
        case["absence_review"] = {"search_terms": ["2026"], "inspection_pages": [26],
                                  "reasoning": "Generic textbook definition, no dated market data"}
        self.assertEqual(validate_cases([case], [self.chunk])["counts"]["dev"]["unanswerable"], 1)

    def test_insufficient_split_counts_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "minimum"):
            validate_minimums({"dev": {"answerable": 15, "unanswerable": 2},
                               "test": {"answerable": 4, "unanswerable": 2}})


if __name__ == "__main__":
    unittest.main()
