"""Root-finding and fixed-point experiments for practical sheet 2."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from math import cos, exp, isfinite, sin, sqrt

ScalarFunction = Callable[[float], float]


@dataclass(frozen=True)
class IterationResult:
    value: float | None
    iterations: int
    error_bound: float | None
    converged: bool
    reason: str
    history: tuple[float, ...]


def target_function(x: float) -> float:
    return sin(x * x) + 1.1 - exp(-x)


def target_derivative(x: float) -> float:
    return 2 * x * cos(x * x) + exp(-x)


def target_second_derivative(x: float) -> float:
    return 2 * cos(x * x) - 4 * x * x * sin(x * x) - exp(-x)


def bisection(
    function: ScalarFunction, left: float, right: float, tolerance: float
) -> IterationResult:
    """Bisection with the a priori interval-width error guarantee."""
    if tolerance <= 0 or right <= left:
        raise ValueError("invalid interval or tolerance")
    f_left, f_right = function(left), function(right)
    if f_left * f_right >= 0:
        raise ValueError("interval endpoints must have opposite signs")
    history: list[float] = []
    while (right - left) / 2 >= tolerance:
        middle = (left + right) / 2
        history.append(middle)
        f_middle = function(middle)
        if f_middle == 0:
            return IterationResult(middle, len(history), 0.0, True, "exact root", tuple(history))
        if f_left * f_middle < 0:
            right, f_right = middle, f_middle
        else:
            left, f_left = middle, f_middle
    value = (left + right) / 2
    history.append(value)
    return IterationResult(
        value,
        len(history),
        (right - left) / 2,
        True,
        "interval-width bound satisfied",
        tuple(history),
    )


def newton(
    function: ScalarFunction,
    derivative: ScalarFunction,
    initial: float,
    tolerance: float,
    derivative_lower_bound: float,
    max_iterations: int = 100,
) -> IterationResult:
    """Newton iteration stopped using |f(x)|/m as an absolute-error bound."""
    if tolerance <= 0 or derivative_lower_bound <= 0:
        raise ValueError("bounds must be positive")
    current = initial
    history = [current]
    for iteration in range(1, max_iterations + 1):
        slope = derivative(current)
        if slope == 0:
            return IterationResult(
                None, iteration - 1, None, False, "zero derivative", tuple(history)
            )
        current -= function(current) / slope
        history.append(current)
        bound = abs(function(current)) / derivative_lower_bound
        if bound < tolerance:
            return IterationResult(
                current, iteration, bound, True, "residual bound satisfied", tuple(history)
            )
    return IterationResult(current, max_iterations, bound, False, "iteration limit", tuple(history))


def cubic(x: float) -> float:
    return x**3 + 4 * x**2 - 10


def fixed_point_maps() -> dict[str, ScalarFunction]:
    return {
        "g1": lambda x: x - x**3 - 4 * x**2 + 10,
        "g2": lambda x: sqrt(10 / x - 4 * x),
        "g3": lambda x: 0.5 * sqrt(10 - x**3),
        "g4": lambda x: sqrt(10 / (4 + x)),
        "g5": lambda x: (2 * x**3 + 4 * x**2 + 10) / (3 * x**2 + 8 * x),
    }


def fixed_point(
    mapping: ScalarFunction,
    initial: float = 1.5,
    tolerance: float = 1e-12,
    max_iterations: int = 200,
    divergence_limit: float = 1e12,
) -> IterationResult:
    """Run an iteration first, recording convergence, domain failure or divergence."""
    current = initial
    history = [current]
    for iteration in range(1, max_iterations + 1):
        try:
            following = mapping(current)
        except (ValueError, ZeroDivisionError, OverflowError) as exc:
            return IterationResult(
                None,
                iteration - 1,
                None,
                False,
                f"domain/arithmetic failure: {type(exc).__name__}",
                tuple(history),
            )
        if not isfinite(following) or abs(following) > divergence_limit:
            return IterationResult(
                None, iteration, None, False, "numerical divergence", tuple(history)
            )
        history.append(following)
        if abs(following - current) < tolerance and abs(cubic(following)) < tolerance:
            return IterationResult(
                following,
                iteration,
                abs(following - current),
                True,
                "successive iterates and residual below tolerance",
                tuple(history),
            )
        current = following
    return IterationResult(current, max_iterations, None, False, "iteration limit", tuple(history))
