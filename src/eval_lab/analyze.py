from __future__ import annotations

import argparse
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


LABELS = {"A", "B", "TIE"}
ORDERS = {"AB", "BA"}


@dataclass(frozen=True)
class JudgeRun:
    case_id: str
    order: str
    verdict: str

    def canonical_verdict(self) -> str:
        """Map the displayed first/second verdict back to original A/B labels."""
        if self.order not in ORDERS:
            raise ValueError(f"unsupported order: {self.order}")
        if self.verdict not in {"FIRST", "SECOND", "TIE"}:
            raise ValueError(f"unsupported verdict: {self.verdict}")
        if self.verdict == "TIE":
            return "TIE"
        if self.order == "AB":
            return "A" if self.verdict == "FIRST" else "B"
        return "B" if self.verdict == "FIRST" else "A"


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON") from exc
    return rows


def paired_predictions(runs: Iterable[JudgeRun]) -> dict[str, dict[str, str]]:
    paired: dict[str, dict[str, str]] = {}
    for run in runs:
        if run.order not in ORDERS:
            raise ValueError(f"unsupported order: {run.order}")
        case = paired.setdefault(run.case_id, {})
        if run.order in case:
            raise ValueError(f"duplicate {run.order} result for {run.case_id}")
        case[run.order] = run.canonical_verdict()
    incomplete = [case_id for case_id, values in paired.items() if set(values) != ORDERS]
    if incomplete:
        raise ValueError(f"missing paired order for: {', '.join(sorted(incomplete))}")
    return paired


def rate(values: Iterable[bool]) -> float:
    items = list(values)
    return sum(items) / len(items) if items else 0.0


def bootstrap_interval(values: list[bool], samples: int = 5000, seed: int = 17) -> tuple[float, float]:
    if not values:
        return 0.0, 0.0
    rng = random.Random(seed)
    estimates = []
    for _ in range(samples):
        draw = [values[rng.randrange(len(values))] for _ in values]
        estimates.append(rate(draw))
    estimates.sort()
    return estimates[int(samples * 0.025)], estimates[int(samples * 0.975)]


def analyze(dataset: list[dict], run_rows: list[dict]) -> dict:
    labels = {row["id"]: row["human_preference"] for row in dataset}
    invalid = {label for label in labels.values() if label not in LABELS}
    if invalid:
        raise ValueError(f"unsupported human labels: {sorted(invalid)}")

    runs = [JudgeRun(row["case_id"], row["order"], row["verdict"]) for row in run_rows]
    paired = paired_predictions(runs)
    if set(paired) != set(labels):
        raise ValueError("dataset and result case IDs do not match")

    flips = [orders["AB"] != orders["BA"] for orders in paired.values()]
    ab_agreement = [paired[case_id]["AB"] == label for case_id, label in labels.items()]
    ba_agreement = [paired[case_id]["BA"] == label for case_id, label in labels.items()]

    first_choices = 0
    non_ties = 0
    for row in run_rows:
        if row["verdict"] != "TIE":
            non_ties += 1
            first_choices += row["verdict"] == "FIRST"

    flip_low, flip_high = bootstrap_interval(flips)
    return {
        "cases": len(labels),
        "flip_rate": rate(flips),
        "flip_rate_95pct_bootstrap_ci": [flip_low, flip_high],
        "human_agreement_ab": rate(ab_agreement),
        "human_agreement_ba": rate(ba_agreement),
        "first_position_preference": first_choices / non_ties if non_ties else 0.0,
        "flipped_case_ids": sorted(case_id for case_id, orders in paired.items() if orders["AB"] != orders["BA"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze paired-order judge results")
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(analyze(load_jsonl(args.dataset), load_jsonl(args.results)), indent=2))


if __name__ == "__main__":
    main()

