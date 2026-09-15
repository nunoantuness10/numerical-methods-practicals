from numerical_methods.roots import (
    bisection,
    cubic,
    fixed_point,
    fixed_point_maps,
    newton,
    target_derivative,
    target_function,
)


def test_bisection_and_newton_find_same_root():
    bisected = bisection(target_function, -0.2, -0.1, 5e-9)
    newton_result = newton(target_function, target_derivative, -0.2, 5e-9, 0.7)
    assert bisected.converged and newton_result.converged
    assert abs(bisected.value - newton_result.value) < 1e-7


def test_fixed_point_experiment_records_each_map():
    results = {name: fixed_point(mapping) for name, mapping in fixed_point_maps().items()}
    assert set(results) == {"g1", "g2", "g3", "g4", "g5"}
    assert results["g4"].converged
    assert results["g5"].converged
    assert abs(cubic(results["g5"].value)) < 1e-12
