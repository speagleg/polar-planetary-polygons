"""Tests for the variational principle on C*."""

import numpy as np
import pytest

from variational import (
    thomson_energy, thomson_enstrophy, variational_analysis,
)


class TestThomsonFunctionals:
    def test_energy_at_sigma_0(self):
        """Energy is finite and negative at sigma=0."""
        H = thomson_energy(6, 0.0)
        assert np.isfinite(H)
        assert H < 0

    def test_enstrophy_at_sigma_0(self):
        """Enstrophy is finite and positive at sigma=0."""
        Z = thomson_enstrophy(6, 0.0)
        assert Z > 0

    def test_energy_is_maximum_at_sigma_0(self):
        """Energy is a local MAXIMUM at sigma=0 for all N."""
        for N in [5, 6, 8]:
            result = variational_analysis(N)
            assert result['energy_extremum'] == 'maximum'

    def test_enstrophy_is_minimum_at_sigma_0(self):
        """Enstrophy is a local MINIMUM at sigma=0 for all N."""
        for N in [5, 6, 8]:
            result = variational_analysis(N)
            assert result['enstrophy_extremum'] == 'minimum'


class TestEnstrophyEnergySignStructure:
    def test_opposite_curvatures(self):
        """Energy maximum (H''<0) and enstrophy minimum (Z''>0) for all N."""
        for N in [3, 4, 5, 6, 7, 8, 9]:
            result = variational_analysis(N)
            assert result['H_double_prime'] < 0, f"N={N}: H'' should be negative"
            assert result['Z_double_prime'] > 0, f"N={N}: Z'' should be positive"

    def test_negative_temperature(self):
        """Lagrange multiplier mu = -Z''/H'' > 0 (negative temperature) for all N."""
        for N in [5, 6, 8]:
            result = variational_analysis(N)
            assert result['negative_temperature'], \
                f"N={N}: mu = {result['lagrange_multiplier']}, expected > 0"

    def test_d2L_is_identity(self):
        """d2L = Z'' + mu*H'' = 0 is an algebraic identity, not a physical result."""
        # This test documents that d2L = 0 is TAUTOLOGICAL:
        # mu = -Z''/H'' makes Z'' + mu*H'' = 0 by construction.
        # The physical content is in the SIGN PATTERN (H''<0, Z''>0),
        # not in the constrained curvature.
        for N in [5, 6, 8]:
            result = variational_analysis(N)
            assert result['constrained_degenerate']  # True by identity

    def test_universal_across_N(self):
        """The degenerate structure holds for N = 3 through 9."""
        for N in range(3, 10):
            result = variational_analysis(N)
            assert result['constrained_degenerate'], f"Failed for N={N}"
            assert result['negative_temperature'], f"Failed for N={N}"
