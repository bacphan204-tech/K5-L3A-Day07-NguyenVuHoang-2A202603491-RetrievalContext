"""Ranking/filter/fusion checks using small explicit relevance examples."""
import math
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from lexical_retrieval import BM25Retriever
from hybrid_retrieval import reciprocal_rank_fusion


def chunk(cid, text, chapter=3, score=1):
    return {"id": cid, "text": text, "source_id": "book", "source": "book.pdf", "page": 1,
            "metadata": {"chapter": chapter}, "score": score}


class BM25Tests(unittest.TestCase):
    def setUp(self):
        self.rows = [chunk("labor", "individuals supply labor workers", 4),
                     chunk("goods", "supply demand goods price", 3),
                     chunk("long", "labor " + "unrelated " * 100, 4)]
        self.index = BM25Retriever(self.rows)

    def test_length_normalization_and_case(self):
        results = self.index.search("LABOR?!", top_k=3)
        self.assertEqual([c["id"] for c in results], ["labor", "long"])
        self.assertEqual(results[0]["matched_terms"], ["labor"])
        # Closed-form BM25 score for one term, rather than a copied ranking result.
        avg = (4 + 4 + 101) / 3
        expected = math.log(1 + 1.5 / 2.5) * 2.5 / (1 + 1.5 * (0.25 + 0.75 * 4 / avg))
        self.assertAlmostEqual(results[0]["score"], expected)

    def test_filter_keeps_global_index_statistics(self):
        all_rows = self.index.search("supply", top_k=3)
        filtered = self.index.search("supply", filters={"chapter": 4}, top_k=3)
        self.assertEqual([c["id"] for c in filtered], ["labor"])
        self.assertEqual(filtered[0]["score"], next(c["score"] for c in all_rows if c["id"] == "labor"))

    def test_unknown_terms_and_invalid_inputs(self):
        self.assertEqual(self.index.search("zzzznotincorpus"), [])
        for kwargs in ({"top_k": 0}, {"filters": {"chapter": 5}}, {"filters": {"chapter": True}}):
            with self.assertRaises(ValueError):
                self.index.search("labor", **kwargs)
        with self.assertRaises(ValueError):
            self.index.search(" ")


class FusionTests(unittest.TestCase):
    def test_ranks_combine_without_adding_incompatible_scores(self):
        a, b, c = chunk("a", "alpha", score=0.9), chunk("b", "beta", score=0.8), chunk("c", "gamma", score=9000)
        result = reciprocal_rank_fusion({"dense": [a, b], "bm25": [c, {**b, "score": 8000}]})
        self.assertEqual([r["id"] for r in result], ["b", "a", "c"])
        self.assertAlmostEqual(result[0]["score"], 2 / 62)
        self.assertEqual(result[0]["components"]["bm25"]["score"], 8000)

    def test_empty_lexical_preserves_dense_order(self):
        result = reciprocal_rank_fusion({"dense": [chunk("b", "beta"), chunk("a", "alpha")], "bm25": []})
        self.assertEqual([r["id"] for r in result], ["b", "a"])
        self.assertEqual(reciprocal_rank_fusion({"dense": [], "bm25": []}), [])

    def test_duplicate_and_conflicting_records_are_rejected(self):
        a = chunk("a", "alpha")
        with self.assertRaises(ValueError):
            reciprocal_rank_fusion({"dense": [a, a]})
        with self.assertRaises(ValueError):
            reciprocal_rank_fusion({"dense": [a], "bm25": [{**a, "text": "different text"}]})


if __name__ == "__main__":
    unittest.main()
