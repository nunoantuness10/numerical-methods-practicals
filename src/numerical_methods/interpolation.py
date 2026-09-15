"""Newton interpolation and natural cubic splines built from first principles."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

Array = np.ndarray


@dataclass(frozen=True)
class NewtonPolynomial:
    nodes: Array
    coefficients: Array

    @classmethod
    def fit(cls, nodes, values) -> NewtonPolynomial:
        x = np.asarray(nodes, dtype=float)
        coefficients = np.asarray(values, dtype=float).copy()
        if x.ndim != 1 or len(x) != len(coefficients) or len(np.unique(x)) != len(x):
            raise ValueError("nodes must be distinct and match the values")
        # In-place divided-difference table; coefficients[j] becomes f[x0,...,xj].
        for order in range(1, len(x)):
            coefficients[order:] = (coefficients[order:] - coefficients[order - 1 : -1]) / (
                x[order:] - x[:-order]
            )
        return cls(x, coefficients)

    def __call__(self, points):
        points = np.asarray(points, dtype=float)
        result = np.full_like(points, self.coefficients[-1], dtype=float)
        for index in range(len(self.coefficients) - 2, -1, -1):
            result = self.coefficients[index] + (points - self.nodes[index]) * result
        return float(result) if result.ndim == 0 else result


@dataclass(frozen=True)
class NaturalCubicSpline:
    nodes: Array
    values: Array
    second_derivatives: Array

    @classmethod
    def fit(cls, nodes, values) -> NaturalCubicSpline:
        x = np.asarray(nodes, dtype=float)
        y = np.asarray(values, dtype=float)
        if x.ndim != 1 or len(x) != len(y) or len(x) < 2 or np.any(np.diff(x) <= 0):
            raise ValueError("nodes must be strictly increasing and match the values")
        size = len(x)
        matrix = np.zeros((size, size))
        right = np.zeros(size)
        matrix[0, 0] = matrix[-1, -1] = 1.0  # M0 = Mn = 0 (natural conditions)
        steps = np.diff(x)
        for index in range(1, size - 1):
            matrix[index, index - 1] = steps[index - 1]
            matrix[index, index] = 2 * (steps[index - 1] + steps[index])
            matrix[index, index + 1] = steps[index]
            right[index] = 6 * (
                (y[index + 1] - y[index]) / steps[index]
                - (y[index] - y[index - 1]) / steps[index - 1]
            )
        moments = np.linalg.solve(matrix, right)
        return cls(x, y, moments)

    def system(self) -> tuple[Array, Array]:
        """Return the linear system A M = b used for the spline moments."""
        size = len(self.nodes)
        matrix = np.zeros((size, size))
        right = np.zeros(size)
        matrix[0, 0] = matrix[-1, -1] = 1.0
        steps = np.diff(self.nodes)
        for index in range(1, size - 1):
            matrix[index, index - 1] = steps[index - 1]
            matrix[index, index] = 2 * (steps[index - 1] + steps[index])
            matrix[index, index + 1] = steps[index]
            right[index] = 6 * (
                (self.values[index + 1] - self.values[index]) / steps[index]
                - (self.values[index] - self.values[index - 1]) / steps[index - 1]
            )
        return matrix, right

    def __call__(self, points):
        scalar = np.ndim(points) == 0
        points = np.atleast_1d(np.asarray(points, dtype=float))
        if np.any(points < self.nodes[0]) or np.any(points > self.nodes[-1]):
            raise ValueError("spline evaluation outside interpolation interval")
        indices = np.searchsorted(self.nodes, points, side="right") - 1
        indices = np.clip(indices, 0, len(self.nodes) - 2)
        left, right = self.nodes[indices], self.nodes[indices + 1]
        width = right - left
        a = (right - points) / width
        b = (points - left) / width
        result = (
            a * self.values[indices]
            + b * self.values[indices + 1]
            + (
                (a**3 - a) * self.second_derivatives[indices]
                + (b**3 - b) * self.second_derivatives[indices + 1]
            )
            * width**2
            / 6
        )
        return float(result[0]) if scalar else result


def polynomial_error_bound(point: float, nodes: Array, derivative_max: float) -> float:
    """Lagrange remainder bound M/(n+1)! product |x-x_i|."""
    from math import factorial

    nodes = np.asarray(nodes, dtype=float)
    return float(derivative_max * np.prod(np.abs(point - nodes)) / factorial(len(nodes)))


def natural_spline_error_bound(step: float, fourth_derivative_max: float) -> float:
    """Classical uniform-mesh natural cubic spline bound 5 M4 h^4 / 384."""
    return 5 * fourth_derivative_max * step**4 / 384
