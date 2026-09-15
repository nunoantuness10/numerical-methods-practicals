"""Two series for pi with explicit truncation guarantees."""

from __future__ import annotations

from dataclasses import dataclass
from math import pi


@dataclass(frozen=True)
class SeriesResult:
    approximation: float | None
    terms: int
    error_bound: float
    absolute_error: float | None
    computed: bool
    note: str = ""


def arcsin_pi(tolerance: float) -> SeriesResult:
    """Approximate pi using 6*arcsin(1/2), bounding the positive tail."""
    if not 0 < tolerance < 1:
        raise ValueError("tolerance must lie between 0 and 1")
    term = 3.0  # k=0, including the outer factor 6
    total = 0.0
    k = 0
    while True:
        total += term
        ratio = ((2 * k + 1) ** 2 / (2 * (k + 1) * (2 * k + 3))) * 0.25
        next_term = term * ratio
        # Every subsequent ratio is below 1/4, so the remaining positive tail
        # is bounded by a geometric series beginning with next_term.
        bound = next_term / 0.75
        if bound < tolerance:
            return SeriesResult(total, k + 1, bound, abs(pi - total), True)
        term = next_term
        k += 1


def leibniz_required_terms(tolerance: float) -> int:
    """Smallest n for which the alternating-series bound 4/(2n+1) < tolerance."""
    if not 0 < tolerance < 1:
        raise ValueError("tolerance must lie between 0 and 1")
    n = int((4.0 / tolerance - 1.0) // 2.0) + 1
    while 4.0 / (2 * n + 1) >= tolerance:
        n += 1
    return n


def leibniz_pi(tolerance: float, max_terms: int = 5_000_000) -> SeriesResult:
    """Approximate pi by the Leibniz series or report that the run is infeasible."""
    required = leibniz_required_terms(tolerance)
    if required > max_terms:
        return SeriesResult(
            None,
            required,
            4.0 / (2 * required + 1),
            None,
            False,
            f"The rigorous bound requires {required:,} terms; limit is {max_terms:,}.",
        )
    # Kahan summation reduces avoidable accumulation error without changing terms.
    total = 0.0
    compensation = 0.0
    for k in range(required):
        value = 4.0 * (1.0 if k % 2 == 0 else -1.0) / (2 * k + 1)
        corrected = value - compensation
        updated = total + corrected
        compensation = (updated - total) - corrected
        total = updated
    return SeriesResult(
        total,
        required,
        4.0 / (2 * required + 1),
        abs(pi - total),
        True,
    )
