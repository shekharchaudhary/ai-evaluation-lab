# Evaluation foundations — 2026-10-17

## What I learned

An evaluation is not just a score. It is a claim about system behavior supported by a dataset, an expected behavior, a measurement method, and stated limitations.

LLM-based systems can fail at several layers: input interpretation, retrieval, reasoning, generation, tool use, and product policy. A useful evaluation should identify the failing layer rather than compress every problem into one quality number.

Automated graders are themselves models of desired behavior. They need evaluation too. Pairwise ordering, response length, rubric wording, ambiguous labels, and correlated graders can all distort conclusions.

## Working principles

- Evaluate early and continuously.
- Prefer task-specific cases over generic benchmarks.
- Use human labels to calibrate automated graders.
- Use pairwise or categorical decisions where possible, but test their biases.
- Keep raw outputs so aggregate metrics can be audited.
- Treat disagreement and negative results as information.

## Open questions

- What level of human–judge agreement is sufficient for different decisions?
- How should an evaluator express uncertainty or abstain?
- How many repetitions are needed to characterize judge instability?
- How should rare, severe risk failures be weighted against common minor errors?
- When do multiple graders provide independent evidence versus correlated confidence?

## Next action

Use Experiment 001 to validate the measurement harness, then execute a real, versioned LLM judge run only after the rubric and human-label protocol are frozen.

