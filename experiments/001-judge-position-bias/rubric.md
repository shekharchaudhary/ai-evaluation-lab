# Pairwise Judge Rubric v0.1

Choose the response that better satisfies the user's request.

Evaluate only these criteria:

1. Correctness: claims are accurate and internally consistent.
2. Relevance: the response directly addresses the request.
3. Completeness: it includes necessary information without inventing requirements.
4. Clarity: it is understandable and appropriately organized.
5. Calibration: uncertainty and limitations are represented honestly.

Do not prefer a response because it appears first, is longer, uses more formatting, or sounds more confident. If neither response is meaningfully better, return `TIE`.

Allowed verdicts: `FIRST`, `SECOND`, `TIE`.

