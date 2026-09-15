"""Floating-point experiments for practical sheet 1."""

from __future__ import annotations


def machine_epsilon() -> float:
    """Return the smallest eps for which 1 + eps is distinguishable from 1."""
    epsilon = 1.0
    while 1.0 + epsilon / 2.0 != 1.0:
        epsilon /= 2.0
    return epsilon
