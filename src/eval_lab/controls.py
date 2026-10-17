from __future__ import annotations


def first_position_verdict(order: str) -> str:
    """Intentionally biased control that always selects the first-displayed answer."""
    if order not in {"AB", "BA"}:
        raise ValueError(f"unsupported order: {order}")
    return "FIRST"
