"""Reproducible experiments and figures for all practical sheets."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .floating_point import machine_epsilon
from .interpolation import (
    NaturalCubicSpline,
    NewtonPolynomial,
    natural_spline_error_bound,
    polynomial_error_bound,
)
from .roots import (
    bisection,
    fixed_point,
    fixed_point_maps,
    newton,
    target_derivative,
    target_function,
    target_second_derivative,
)
from .series import arcsin_pi, leibniz_pi

TOLERANCES = (1e-5, 1e-10, 1e-15)


def practical_1() -> dict:
    return {
        "machine_epsilon": machine_epsilon(),
        "numpy_epsilon": float(np.finfo(float).eps),
        "arcsin_series": {str(tol): asdict(arcsin_pi(tol)) for tol in TOLERANCES},
        "leibniz_series": {str(tol): asdict(leibniz_pi(tol)) for tol in TOLERANCES},
    }


def root_interval() -> tuple[float, float]:
    """Amplitude-0.1 bracket for the smallest root found on the relevant domain."""
    return (-0.2, -0.1)


def practical_2() -> dict:
    left, right = root_interval()
    grid = np.linspace(left, right, 20_001)
    derivative_min = float(np.min(np.abs([target_derivative(x) for x in grid])))
    second_values = np.array([target_second_derivative(x) for x in grid])
    bisected = bisection(target_function, left, right, 5e-9)
    # F(left)*F''(left)>0 selects the standard safe Newton endpoint.
    initial = left if target_function(left) * target_second_derivative(left) > 0 else right
    newton_result = newton(target_function, target_derivative, initial, 5e-9, derivative_min)
    fixed = {name: asdict(fixed_point(mapping)) for name, mapping in fixed_point_maps().items()}
    return {
        "interval": [left, right],
        "endpoint_values": [target_function(left), target_function(right)],
        "derivative_minimum": derivative_min,
        "second_derivative_range": [float(second_values.min()), float(second_values.max())],
        "bisection": asdict(bisected),
        "newton": asdict(newton_result),
        "fixed_point": fixed,
    }


def interpolation_function(x):
    return x**2 + np.sin(6 * x)


def practical_3() -> dict:
    nodes = np.linspace(-1, 1, 8)
    values = interpolation_function(nodes)
    polynomial = NewtonPolynomial.fit(nodes, values)
    spline = NaturalCubicSpline.fit(nodes, values)
    targets = [0.1, 0.9]
    point_results = {}
    for point in targets:
        true = float(interpolation_function(point))
        p_value, s_value = polynomial(point), spline(point)
        point_results[str(point)] = {
            "true": true,
            "polynomial": p_value,
            "spline": s_value,
            "polynomial_actual_error": abs(true - p_value),
            "spline_actual_error": abs(true - s_value),
            "polynomial_error_bound": polynomial_error_bound(point, nodes, 6**8),
            "spline_error_bound": natural_spline_error_bound(nodes[1] - nodes[0], 6**4),
        }
    months = np.arange(1, 13, dtype=float)
    evaporation = np.array([8.6, 7.0, 6.4, 4.0, 2.8, 1.8, 1.8, 2.1, 3.2, 4.7, 6.2, 7.6])
    evaporation_polynomial = NewtonPolynomial.fit(months, evaporation)
    evaporation_spline = NaturalCubicSpline.fit(months, evaporation)
    return {
        "nodes": nodes.tolist(),
        "values": values.tolist(),
        "newton_coefficients": polynomial.coefficients.tolist(),
        "spline_second_derivatives": spline.second_derivatives.tolist(),
        "spline_system": [array.tolist() for array in spline.system()],
        "point_estimates": point_results,
        "evaporation_newton_coefficients": evaporation_polynomial.coefficients.tolist(),
        "evaporation_spline_second_derivatives": evaporation_spline.second_derivatives.tolist(),
        "evaporation_spline_system": [array.tolist() for array in evaporation_spline.system()],
    }


def save_figures(directory: str | Path) -> None:
    destination = Path(directory)
    destination.mkdir(parents=True, exist_ok=True)
    plt.style.use("seaborn-v0_8-whitegrid")

    x = np.linspace(-1.2, 1.2, 1200)
    plt.figure(figsize=(8, 4.5))
    plt.axhline(0, color="black", linewidth=0.8)
    plt.plot(x, [target_function(value) for value in x], label=r"$F(x)$")
    plt.axvspan(-0.2, -0.1, color="#f59e0b", alpha=0.2, label=r"$I=[-0.2,-0.1]$")
    plt.xlabel("x")
    plt.ylabel("F(x)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(destination / "tp2_root_separation.png", dpi=180)
    plt.close()

    nodes = np.linspace(-1, 1, 8)
    values = interpolation_function(nodes)
    polynomial = NewtonPolynomial.fit(nodes, values)
    spline = NaturalCubicSpline.fit(nodes, values)
    dense = np.linspace(-1, 1, 1200)
    true = interpolation_function(dense)
    fig, axes = plt.subplots(2, 1, figsize=(8, 7), sharex=True)
    axes[0].plot(dense, true, label="f", linewidth=2)
    axes[0].plot(dense, polynomial(dense), label="polinomio p")
    axes[0].plot(dense, spline(dense), label="spline s")
    axes[0].scatter(nodes, values, color="black", s=18, label="nos")
    axes[0].legend(ncol=2)
    axes[0].set_ylabel("valor")
    axes[1].semilogy(dense, np.maximum(abs(true - polynomial(dense)), 1e-17), label="|f-p|")
    axes[1].semilogy(dense, np.maximum(abs(true - spline(dense)), 1e-17), label="|f-s|")
    axes[1].set_xlabel("x")
    axes[1].set_ylabel("erro absoluto")
    axes[1].legend()
    fig.tight_layout()
    fig.savefig(destination / "tp3_function_interpolation.png", dpi=180)
    plt.close(fig)

    months = np.arange(1, 13, dtype=float)
    evaporation = np.array([8.6, 7.0, 6.4, 4.0, 2.8, 1.8, 1.8, 2.1, 3.2, 4.7, 6.2, 7.6])
    polynomial = NewtonPolynomial.fit(months, evaporation)
    spline = NaturalCubicSpline.fit(months, evaporation)
    dense = np.linspace(1, 12, 1200)
    plt.figure(figsize=(8, 4.5))
    plt.scatter(months, evaporation, color="black", label="medicoes", zorder=3)
    plt.plot(dense, polynomial(dense), label="polinomio (grau 11)")
    plt.plot(dense, spline(dense), label="spline cubico natural", linewidth=2)
    plt.xlabel("mes")
    plt.ylabel("evaporacao (polegadas)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(destination / "tp3_evaporation.png", dpi=180)
    plt.close()


def run_all(output: str | Path = "results", figures: str | Path = "figures") -> dict:
    destination = Path(output)
    destination.mkdir(parents=True, exist_ok=True)
    result = {
        "practical_1": practical_1(),
        "practical_2": practical_2(),
        "practical_3": practical_3(),
    }
    (destination / "results.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    save_figures(figures)
    return result
