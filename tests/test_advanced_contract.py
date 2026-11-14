import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "advanced"))
from freeze import validate_split


class AdvancedBenchmarkContractTests(unittest.TestCase):
    def test_dev_and_test_splits_meet_case_and_input_contracts(self):
        dev, _ = validate_split("dev")
        test, _ = validate_split("test")
        self.assertGreaterEqual(sum(case["answerable"] for case in test), 24)
        self.assertGreaterEqual(sum(not case["answerable"] for case in test), 6)
        self.assertGreaterEqual(len(test), 30)

        self.assertGreaterEqual(sum(case["answerable"] for case in dev), 15)
        self.assertGreaterEqual(sum(not case["answerable"] for case in dev), 3)

    def test_every_multi_hop_case_requires_distinct_pages(self):
        for split in ("dev", "test"):
            cases, _ = validate_split(split)
            for case in cases:
                if case["group"] == "multi_hop":
                    with self.subTest(case=case["id"]):
                        self.assertGreaterEqual(len(set(case["gold_pages"])), 2)


if __name__ == "__main__":
    unittest.main()
