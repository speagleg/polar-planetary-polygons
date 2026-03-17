"""Tests for the generalised geometric sigma observable."""

import numpy as np
import pytest

from sigma_geometric import sigma_geom, sigma_from_positions


class TestSigmaGeom:
    def test_perfect_hexagon_gives_zero(self):
        z = np.exp(2j * np.pi * np.arange(6) / 6)
        assert sigma_geom(z) == pytest.approx(0.0, abs=1e-10)

    def test_perfect_pentagon_gives_zero(self):
        z = np.exp(2j * np.pi * np.arange(5) / 5)
        assert sigma_geom(z) == pytest.approx(0.0, abs=1e-10)

    def test_perfect_octagon_gives_zero(self):
        z = np.exp(2j * np.pi * np.arange(8) / 8)
        assert sigma_geom(z) == pytest.approx(0.0, abs=1e-10)

    def test_perturbed_hexagon_positive(self):
        z = np.exp(2j * np.pi * np.arange(6) / 6).copy()
        z[0] *= 1.1
        assert sigma_geom(z) > 0.01

    def test_spiral_gives_large_sigma(self):
        r_vals = np.exp(0.3 * np.arange(6))
        theta_vals = np.pi / 3 * np.arange(6)
        z = r_vals * np.exp(1j * theta_vals)
        assert sigma_geom(z) > 0.1

    def test_rotation_invariant(self):
        z = np.exp(2j * np.pi * np.arange(6) / 6).copy()
        z[0] *= 1.1
        z_rotated = z * np.exp(1j * 0.7)
        assert sigma_geom(z) == pytest.approx(sigma_geom(z_rotated), rel=1e-6)

    def test_scale_invariant(self):
        z = np.exp(2j * np.pi * np.arange(6) / 6).copy()
        z[0] *= 1.1
        z_scaled = z * 5.0
        assert sigma_geom(z) == pytest.approx(sigma_geom(z_scaled), rel=1e-6)


class TestSigmaFromPositions:
    def test_lat_lon_to_sigma(self):
        lats = np.full(8, 83.0)
        lons = np.arange(8) * 45.0
        result = sigma_from_positions(lats, lons, R_planet=7.15e7)
        assert result['sigma_geom'] == pytest.approx(0.0, abs=1e-3)
        assert result['N'] == 8

    def test_uneven_radii_nonzero(self):
        """Cyclones at different latitudes give nonzero sigma (different radii)."""
        lats = np.array([83.0, 81.0, 83.0, 81.0, 83.0])
        lons = np.array([0, 72, 144, 216, 288])
        result = sigma_from_positions(lats, lons, R_planet=7.15e7)
        assert result['sigma_geom'] > 0.01
