# AI Evaluation Lab

Reproducible experiments about whether AI systems—and the evaluators used to measure them—can be trusted.

This repository is a public learning record. It publishes hypotheses, datasets, rubrics, raw results, negative findings, limitations, and changes in understanding. Planned work is labeled as planned; results are labeled by the evaluator that produced them.

## Research tracks

- LLM-as-judge reliability and bias
- RAG retrieval-versus-generation failure attribution
- Risk-category evaluations
- Evaluation-system failure modes
- Human calibration and evaluator abstention

## Experiments

| Experiment | Research question | Evidence | Status |
|---|---|---|---|
| [001: Position bias](experiments/001-judge-position-bias/README.md) | Does swapping answer order change a judge's preference? | Paired-order dataset, analysis harness, first-position control | Harness complete; real LLM run planned |

## Principles

1. Separate observed results from hypotheses.
2. Version datasets, prompts, rubrics, models, and parameters.
3. Calibrate automated judges against human labels.
4. Report slices and severe failures, not only aggregate scores.
5. Publish negative results and threats to validity.
6. Make every reported result reproducible.

## Quick start

Requires Python 3.11+ and no third-party packages.

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m eval_lab.analyze \
  --dataset experiments/001-judge-position-bias/dataset.jsonl \
  --results experiments/001-judge-position-bias/results/biased_control.jsonl
```

The included result file comes from a deterministic **first-position-biased control**, not an LLM. Its purpose is to prove that the analysis detects order-sensitive behavior before paid model runs are added.

## Planned next step

Run the same paired-order protocol with a versioned LLM judge, repeat each ordering, and compare it with the human preference labels. The report will include flip rate, agreement, first-position preference, uncertainty, cost, latency, and case-level failures.

## Responsible reporting

This repository does not claim universal model quality or safety. Every conclusion is limited to its dataset, rubric, judge, model version, and execution conditions.
