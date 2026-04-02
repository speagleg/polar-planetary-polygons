"""Tests for Penrose Weyl curvature and arrow alignment."""

import pytest
import numpy as np
from planetary_polygons.extensions.penrose_weyl import (
    weyl_squared_regular, weyl_thermal, weyl_profile,
    arrow_alignment, penrose_decomposition,
)


class TestWeylCurvature:

    @pytest.mark.parametrize("N", [7, 9, 11])
    def test_weyl_zero_at_threshold(self, N):
        """Regular polygon has zero Weyl curvature."""
        from planetary_polygons.extensions.penrose_weyl import find_threshold
        rho_star = find_threshold(N)
        assert weyl_squared_regular(rho_star, N) == 0.0

    @pytest.mark.parametrize("N", [7, 9, 11])
    def test_weyl_positive_exterior(self, N):
        """Weyl curvature is positive in the exterior."""
        from planetary_polygons.extensions.penrose_weyl import find_threshold
        rho_star = find_threshold(N)
        W2 = weyl_thermal(rho_star + 1.0, N)
        assert W2 > 0

    @pytest.mark.parametrize("N", [7, 9])
    def test_weyl_monotone_increasing(self, N):
        """Weyl curvature increases with ρ in the exterior."""
        rho_vals, W2_vals, _ = weyl_profile(N, n_points=20)
        assert np.all(np.diff(W2_vals) > -1e-6)


class TestArrowAlignment:

    @pytest.mark.parametrize("N", [7, 9, 11])
    def test_all_arrows_aligned(self, N):
        """Entropy, Weyl, and expansion all increase together."""
        result = arrow_alignment(N)
        assert result['all_aligned']

    @pytest.mark.parametrize("N", [7, 9, 11])
    def test_entropy_increasing(self, N):
        result = arrow_alignment(N)
        assert result['entropy_increasing']

    @pytest.mark.parametrize("N", [7, 9, 11])
    def test_weyl_increasing(self, N):
        result = arrow_alignment(N)
        assert result['weyl_increasing']


class TestPenroseDecomposition:

    @pytest.mark.parametrize("N", [7, 9, 11])
    def test_initial_entropy_low(self, N):
        d = penrose_decomposition(N)
        assert d['S_initial'] < 10

    @pytest.mark.parametrize("N", [7, 9, 11])
    def test_gap_large(self, N):
        d = penrose_decomposition(N)
        assert d['gap_ratio'] > 100

    def test_weyl_initial_zero(self):
        d = penrose_decomposition(7)
        assert d['W2_initial'] == 0.0

    def test_weyl_grows(self):
        d = penrose_decomposition(7)
        assert d['W2_at_rho_plus_1'] > 0
