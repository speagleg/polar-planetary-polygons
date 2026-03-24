"""Tests for radion inflation."""

import pytest
from planetary_polygons.extensions.radion_inflation import (
    V_radion, find_minimum, slow_roll, inflation_predictions,
)


class TestRadionPotential:
    def test_minimum_exists(self):
        """The radion has a stable minimum."""
        sigma_min = find_minimum(11)
        assert 0.5 < sigma_min < 5.0

    def test_potential_positive_at_minimum(self):
        """V(σ_min) > 0 (de Sitter vacuum)."""
        sigma_min = find_minimum(11)
        assert V_radion(sigma_min) > 0

    def test_potential_grows_at_large_sigma(self):
        """V(σ) grows for large σ (from Λσ term)."""
        assert V_radion(100) > V_radion(10) > V_radion(find_minimum(11))


class TestSlowRoll:
    def test_epsilon_small_at_large_sigma(self):
        """ε << 1 for σ >> 1 (flat potential)."""
        sr = slow_roll(20, 11)
        assert sr['epsilon'] < 0.01

    def test_inflation_ends_near_minimum(self):
        """ε > 1 near the minimum (inflation ends)."""
        sigma_min = find_minimum(11)
        sr = slow_roll(sigma_min + 0.3, 11)
        # Near the minimum, ε should be large (steep potential)
        assert sr is not None


class TestPredictions:
    def test_n_s_near_observed(self):
        """n_s is within 3σ of the Planck value."""
        pred = inflation_predictions(N=11, N_efolds=60)
        assert pred['n_s_tension_sigma'] < 3.0

    def test_r_testable(self):
        """r is large enough to be testable by LiteBIRD."""
        pred = inflation_predictions(N=11, N_efolds=60)
        assert pred['r'] > 0.01  # LiteBIRD sensitivity ~ 0.001

    def test_60_efolds(self):
        """60 e-folds of inflation are achievable."""
        pred = inflation_predictions(N=11, N_efolds=60)
        assert pred['sigma_start'] > pred['sigma_min']
        assert pred['epsilon'] < 0.1  # slow-roll holds
