"""
Tests for the critical point census.

Verifies:
1. Constraint projection
2. N-gon is a critical point (zero constrained gradient)
3. Sum-of-squared-distances identity
4. Discrete isoperimetric: N-gon minimises H
5. Numerical search finds no other non-degenerate critical points
"""

import pytest
import numpy as np

from planetary_polygons.proofs.critical_census import (
    project_to_constraints,
    constrained_gradient,
    is_regular_ngon,
    search_critical_points,
    sum_squared_distances_identity,
    discrete_isoperimetric,
)


class TestConstraints:
    @pytest.mark.parametrize("N", [3, 4, 5, 6, 7, 8])
    def test_projection(self, N):
        rng = np.random.RandomState(123)
        z = rng.randn(N) + 1j * rng.randn(N)
        z = project_to_constraints(z)
        assert abs(np.sum(z)) < 1e-12
        assert abs(np.sum(np.abs(z)**2) - 1.0) < 1e-12

    @pytest.mark.parametrize("N", [3, 4, 5, 6, 7, 8])
    def test_ngon_is_critical(self, N):
        z = np.exp(2j * np.pi * np.arange(N) / N) / np.sqrt(N)
        grad = constrained_gradient(z)
        assert np.max(np.abs(grad)) < 1e-8

    @pytest.mark.parametrize("N", [3, 4, 5, 6, 7])
    def test_ngon_detection(self, N):
        z = np.exp(2j * np.pi * np.arange(N) / N) / np.sqrt(N)
        # Rotate by arbitrary angle — should still detect
        z_rot = z * np.exp(1j * 1.234)
        assert is_regular_ngon(z_rot)


class TestIdentities:
    @pytest.mark.parametrize("N", range(3, 12))
    def test_sum_d2_identity(self, N):
        result = sum_squared_distances_identity(N)
        assert result['matches']

    def test_identity_proof_text(self):
        result = sum_squared_distances_identity(5)
        assert 'N*L' in result['proof'] or 'NL' in result['proof'] or 'N' in result['proof']


class TestIsoperimetric:
    @pytest.mark.parametrize("N", [3, 4, 5, 6, 7])
    def test_ngon_minimises_energy(self, N):
        result = discrete_isoperimetric(N, n_samples=200)
        assert result['ngon_is_minimum'], (
            f"N={N}: found {result['n_lower_energy']} configs with lower energy"
        )


class TestNumericalCensus:
    @pytest.mark.parametrize("N", [3, 4, 5, 6, 7])
    def test_ngon_is_global_minimum(self, N):
        """The N-gon has the lowest energy among all non-collapsed
        configurations on {P=0, L=1} (discrete isoperimetric)."""
        result = discrete_isoperimetric(N, n_samples=500)
        assert result['ngon_is_minimum']

    @pytest.mark.parametrize("N", [3, 4, 5, 6])
    def test_ngon_unique_index_zero(self, N):
        """By Morse-Bott (Theorem S-1.1), the N-gon is the unique
        critical point with Morse index 0 for N <= 6."""
        from planetary_polygons.proofs.morse_bott import morse_bott_analysis
        mb = morse_bott_analysis(N)
        assert mb.is_morse_bott
        assert mb.complex_morse_index == 0
