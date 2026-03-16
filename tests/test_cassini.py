"""Tests for Cassini wind profile data and measurements."""

import numpy as np
import pytest

from spiral_hexagon.data.cassini_winds import (
    load_cassini_profile, measure_delta_U, measure_hexagon_epsilon,
)


@pytest.fixture
def profile():
    return load_cassini_profile()


class TestCassiniProfile:
    def test_peak_speed_range(self, profile):
        """Peak jet speed should be 110-130 m/s."""
        assert 110 < profile.peak_speed < 130

    def test_peak_latitude_range(self, profile):
        """Peak should be near 76-77 deg N."""
        assert 75 < profile.peak_latitude < 78

    def test_halfwidth_range(self, profile):
        """Jet half-width should be 1-4 degrees."""
        assert 1.0 < profile.jet_halfwidth_deg < 4.0

    def test_callable(self, profile):
        """Profile is callable at arbitrary latitudes."""
        U = profile(76.0)
        assert 100 < U < 130

    def test_profile_shape(self, profile):
        """Wind speed decreases away from peak."""
        U_peak = profile(profile.peak_latitude)
        U_far = profile(70.0)
        assert U_far < U_peak

    def test_logpolar_conversion(self, profile):
        """Log-polar conversion produces valid arrays."""
        rho, U = profile.to_logpolar()
        assert len(rho) == len(U)
        assert np.all(np.isfinite(rho))


class TestDeltaUMeasurement:
    def test_measurement_keys(self):
        """measure_delta_U returns all expected keys."""
        result = measure_delta_U()
        expected = ['U_observed', 'U_star', 'delta_U',
                    'delta_U_over_Ustar', 'gaussian_relative_rms']
        for key in expected:
            assert key in result

    def test_U_star_positive(self):
        result = measure_delta_U()
        assert result['U_star'] > 0

    def test_delta_U_positive(self):
        """Observed jet is faster than stationary speed."""
        result = measure_delta_U()
        assert result['delta_U'] > 0

    def test_ratio_order_of_magnitude(self):
        """delta_U/U* should be O(0.1)."""
        result = measure_delta_U()
        assert 0.01 < result['delta_U_over_Ustar'] < 1.0

    def test_gaussian_fit_reasonable(self):
        """Gaussian approximation should fit within 20% RMS."""
        result = measure_delta_U()
        assert result['gaussian_relative_rms'] < 0.20


class TestHexagonEpsilon:
    def test_epsilon_range(self):
        """Observed epsilon should be 0.01 - 0.20."""
        result = measure_hexagon_epsilon()
        assert 0.01 < result['epsilon_observed'] < 0.20

    def test_regular_hexagon_reference(self):
        """Regular hexagon epsilon = 1 - sqrt(3)/2 ~ 0.134."""
        result = measure_hexagon_epsilon()
        assert result['epsilon_regular_hexagon'] == pytest.approx(
            1 - np.sqrt(3)/2, rel=1e-10
        )
