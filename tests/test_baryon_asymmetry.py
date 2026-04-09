"""Tests for the baryon asymmetry eta_B = J * K^C(N-1,2) / N."""

import pytest
from math import comb

from planetary_polygons.extensions.baryon_asymmetry import (
    instanton_power, eta_B, full_prediction,
)


class TestInstantonPower:
    def test_instanton_power_value(self):
        """C(6,2) = 15 at N=7."""
        assert instanton_power() == 15

    def test_instanton_power_is_binomial(self):
        """Power = C(N-1, 2) = (N-1)(N-2)/2."""
        N = 7
        assert instanton_power(N) == comb(N - 1, 2)
        assert instanton_power(N) == (N - 1) * (N - 2) // 2


class TestEtaB:
    def test_eta_B_order_of_magnitude(self):
        """eta_B in the range 1e-11 to 1e-8."""
        result = eta_B()
        assert 1e-11 < result < 1e-8

    def test_eta_B_positive(self):
        assert eta_B() > 0

    def test_eta_B_from_explicit_inputs(self):
        """Test with explicit J and K values from the investigation."""
        result = eta_B(J=3.44e-5, K=0.548, N_val=7)
        # 3.44e-5 * 0.548^15 / 7 ≈ 5.96e-10
        assert 1e-10 < result < 1e-9


class TestFullPrediction:
    def test_full_prediction_keys(self):
        result = full_prediction()
        assert 'J' in result
        assert 'K' in result
        assert 'power' in result
        assert 'eta_B' in result
        assert 'eta_obs' in result

    def test_full_prediction_has_match(self):
        result = full_prediction()
        assert 'match_pct' in result
