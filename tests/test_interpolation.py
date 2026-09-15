import numpy as np

from numerical_methods.interpolation import NaturalCubicSpline, NewtonPolynomial


def test_interpolants_reproduce_nodes():
    nodes = np.linspace(-1, 1, 8)
    values = nodes**2 + np.sin(6 * nodes)
    polynomial = NewtonPolynomial.fit(nodes, values)
    spline = NaturalCubicSpline.fit(nodes, values)
    np.testing.assert_allclose(polynomial(nodes), values, atol=1e-12)
    np.testing.assert_allclose(spline(nodes), values, atol=1e-12)
    assert spline.second_derivatives[0] == 0
    assert spline.second_derivatives[-1] == 0


def test_spline_is_continuous_at_interior_nodes():
    nodes = np.arange(1, 13, dtype=float)
    values = np.array([8.6, 7.0, 6.4, 4.0, 2.8, 1.8, 1.8, 2.1, 3.2, 4.7, 6.2, 7.6])
    spline = NaturalCubicSpline.fit(nodes, values)
    for node in nodes[1:-1]:
        assert abs(spline(node - 1e-8) - spline(node + 1e-8)) < 1e-6
