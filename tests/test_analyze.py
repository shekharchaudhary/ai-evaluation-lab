import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from eval_lab.analyze import JudgeRun, analyze, paired_predictions
from eval_lab.controls import first_position_verdict


class JudgeRunTests(unittest.TestCase):
    def test_canonicalizes_swapped_order(self):
        self.assertEqual(JudgeRun("x", "BA", "FIRST").canonical_verdict(), "B")
        self.assertEqual(JudgeRun("x", "BA", "SECOND").canonical_verdict(), "A")

    def test_requires_both_orders(self):
        with self.assertRaisesRegex(ValueError, "missing paired order"):
            paired_predictions([JudgeRun("x", "AB", "FIRST")])

    def test_detects_position_bias(self):
        dataset = [
            {"id": "one", "human_preference": "A"},
            {"id": "two", "human_preference": "B"},
        ]
        results = [
            {"case_id": "one", "order": "AB", "verdict": "FIRST"},
            {"case_id": "one", "order": "BA", "verdict": "FIRST"},
            {"case_id": "two", "order": "AB", "verdict": "FIRST"},
            {"case_id": "two", "order": "BA", "verdict": "FIRST"},
        ]
        report = analyze(dataset, results)
        self.assertEqual(report["flip_rate"], 1.0)
        self.assertEqual(report["first_position_preference"], 1.0)
        self.assertEqual(report["human_agreement_ab"], 0.5)
        self.assertEqual(report["human_agreement_ba"], 0.5)

    def test_first_position_control_is_intentionally_biased(self):
        self.assertEqual(first_position_verdict("AB"), "FIRST")
        self.assertEqual(first_position_verdict("BA"), "FIRST")


if __name__ == "__main__":
    unittest.main()
