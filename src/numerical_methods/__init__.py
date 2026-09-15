"""Numerical algorithms used in the three practical sheets."""

from .floating_point import machine_epsilon
from .interpolation import NaturalCubicSpline, NewtonPolynomial
from .roots import bisection, newton
from .series import arcsin_pi, leibniz_pi

__all__ = [
    "NaturalCubicSpline",
    "NewtonPolynomial",
    "arcsin_pi",
    "bisection",
    "leibniz_pi",
    "machine_epsilon",
    "newton",
]
