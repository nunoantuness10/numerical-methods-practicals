from math import pi

import numpy as np

from numerical_methods.floating_point import machine_epsilon
from numerical_methods.series import arcsin_pi, leibniz_pi, leibniz_required_terms


def test_machine_epsilon_matches_binary64():
    assert machine_epsilon() == np.finfo(float).eps


def test_arcsin_series_respects_requested_errors():
    for tolerance in (1e-5, 1e-10, 1e-15):
        result = arcsin_pi(tolerance)
        assert result.computed
        assert result.error_bound < tolerance
        assert abs(pi - result.approximation) < tolerance


def test_leibniz_reports_infeasible_precisions():
    assert leibniz_pi(1e-5).computed
    assert not leibniz_pi(1e-10).computed
    assert leibniz_required_terms(1e-10) > 19_000_000_000
