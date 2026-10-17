# Experiment 001: Position Bias in Pairwise LLM Judging

## Research question

Does a pairwise evaluator change its preferred answer when the same answers are shown in reverse order?

## Why this matters

Pairwise LLM judges are often used to compare prompts, models, and product changes. If presentation order changes the verdict, an apparent improvement may be an evaluator artifact rather than a real quality difference.

## Hypothesis

A judge that has not been explicitly calibrated and tested will prefer the first-displayed answer more often than chance and will reverse some judgments after answer order is swapped.

## Method

1. Create response pairs with a blinded human preference label.
2. Present every pair in original (`AB`) and swapped (`BA`) order.
3. Map `FIRST`/`SECOND` judgments back to the original A/B identities.
4. Measure flip rate, human agreement by order, and first-position preference.
5. Inspect every flipped case instead of relying only on the aggregate score.

## Current evidence

The repository currently contains:

- A 12-case seed dataset intended to exercise the harness
- Human preference labels authored for the seed cases
- A deterministic first-position-biased control evaluator result
- Tests and an analysis command

The control is intentionally flawed: it always selects the first-displayed answer. It is not evidence about any LLM. It verifies that the analysis can expose maximally order-sensitive evaluation behavior.

## Metrics

- **Flip rate:** fraction of cases whose canonical A/B verdict changes after swapping order
- **Human agreement (AB and BA):** fraction matching the human label in each presentation order
- **First-position preference:** fraction of non-tie runs selecting the first-displayed response
- **Case-level failures:** IDs of every flipped case

## Reproduce

From the repository root:

```bash
PYTHONPATH=src python3 -m eval_lab.analyze \
  --dataset experiments/001-judge-position-bias/dataset.jsonl \
  --results experiments/001-judge-position-bias/results/biased_control.jsonl
```

## Next run

Use a versioned LLM judge with a fixed rubric and structured output. Repeat each order multiple times, record latency and cost, and compare with the human labels. No conclusion about LLM position bias will be published until that run is complete.

## Threats to validity

- The seed dataset is small and authored rather than sampled from production.
- A single human label is not a strong ground truth.
- Cases cover general answer quality, not a specific production distribution.
- Ties and near-ties may amplify apparent instability.
- Results will depend on the judge model, version, prompt, and sampling settings.
