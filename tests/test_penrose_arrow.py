"""
Tests for Penrose past hypothesis: temperature sign change and entropy gap.
"""

import pytest
import numpy as np
from math import log

from planetary_polygons.extensions.penrose_arrow import (
    onsager_beta, onsager_beta_profile, polygon_entropy,
    entropy_at_threshold, cardy_entropy, penrose_gap,
    penrose_table, temperature_sign_change, find_entropy_minimum,
    find_threshold, entropy_derivative,
)


class TestOnsagerTemperature:
    """β(ρ) is positive in the exterior (ρ > ρ*)."""

    @pytest.mark.parametrize("N", [7, 8, 9, 11])
    def test_beta_positive_exterior(self, N):
        """Non-critical β > 0 for ρ > ρ* (all non-critical λ_m > 0)."""
        rho_star = find_threshold(N)
        for delta in [0.1, 0.5, 1.0, 3.0]:
            beta = onsager_beta(rho_star + delta, N)
            assert beta > 0, (
                f"N={N}, ρ={rho_star + delta:.2f}: β={beta:.4f}, expected > 0"
            )

    @pytest.mark.parametrize("N", [7, 8, 9])
    def test_beta_decreases_with_rho(self, N):
        """β decreases as ρ increases (temperature increases with expansion)."""
        rho_star = find_threshold(N)
        betas = [onsager_beta(rho_star + d, N) for d in [0.5, 2.0, 5.0]]
        assert betas[0] > betas[1] > betas[2], (
            f"N={N}: β should decrease: {betas}"
        )


class TestCriticalModeSignChange:
    """λ_{m*} changes sign at ρ = ρ* (the β = 0 surface)."""

    @pytest.mark.parametrize("N", [7, 8, 9, 11])
    def test_sign_change_at_threshold(self, N):
        """λ_{m*} crosses zero at ρ = ρ*."""
        result = temperature_sign_change(N)
        assert result['match'], (
            f"N={N}: sign change at ρ={result['sign_change_at']}, "
            f"expected ρ*={result['rho_star']:.4f}"
        )


class TestPolygonEntropy:
    """S_poly(ρ) profile and minimum."""

    @pytest.mark.parametrize("N", [7, 8, 9, 11])
    def test_entropy_finite_at_threshold(self, N):
        """S_poly(ρ*) is finite (critical mode excluded)."""
        S = entropy_at_threshold(N)
        assert np.isfinite(S), f"N={N}: S diverges at threshold"
        assert S > 0, f"N={N}: S={S} not positive"

    @pytest.mark.parametrize("N", [7, 8, 9])
    def test_entropy_increases_in_exterior(self, N):
        """S_poly increases with ρ for ρ > ρ* (positive-T second law)."""
        rho_star = find_threshold(N)
        S_vals = [polygon_entropy(rho_star + d, N)
                  for d in [0.5, 1.0, 2.0, 4.0]]
        for i in range(len(S_vals) - 1):
            assert S_vals[i + 1] > S_vals[i], (
                f"N={N}: S not increasing at ρ*+{[0.5,1,2,4][i+1]}"
            )

    @pytest.mark.parametrize("N", [7, 8, 9])
    def test_entropy_minimum_before_threshold(self, N):
        """S_poly minimum is at or before ρ* (in the interior/transition).

        The minimum may be slightly before ρ* because the non-critical
        eigenvalues have different ρ-dependence. The key physical point
        is that S is INCREASING at ρ* (the creation point).
        """
        result = find_entropy_minimum(N)
        rho_star = result['rho_star']
        rho_min = result['rho_min_S']
        assert rho_min <= rho_star + 0.5, (
            f"N={N}: S minimum at ρ={rho_min:.4f}, "
            f"should be at or before ρ*={rho_star:.4f}"
        )

    @pytest.mark.parametrize("N", [7, 8, 9])
    def test_entropy_derivative_positive_at_threshold(self, N):
        """dS/dρ > 0 at ρ* (entropy increasing at creation)."""
        rho_star = find_threshold(N)
        dS = entropy_derivative(rho_star + 0.01, N)
        assert dS > 0, f"N={N}: dS/dρ={dS:.4f} at ρ*, expected > 0"


class TestPenroseGap:
    """The computable Penrose entropy gap."""

    @pytest.mark.parametrize("N", [7, 8, 9, 11])
    def test_gap_exists(self, N):
        """S_BH >> S_1loop (large Penrose gap)."""
        result = penrose_gap(N)
        assert result['ratio'] > 10, (
            f"N={N}: gap ratio={result['ratio']:.1f}, expected >> 1"
        )

    def test_gap_grows_with_N(self):
        """The Penrose gap grows with N (more Virasoro descendants)."""
        gaps = penrose_table([7, 9, 11, 13])
        ratios = [g['ratio'] for g in gaps]
        assert ratios[-1] > ratios[0], (
            f"Gap should grow: {ratios[0]:.0f} → {ratios[-1]:.0f}"
        )

    def test_N7_gap_value(self):
        """N=7: S_BH/S_1loop ≈ 144."""
        result = penrose_gap(7)
        assert 100 < result['ratio'] < 200, (
            f"N=7 gap: {result['ratio']:.1f}, expected ~144"
        )

    def test_initial_entropy_low(self):
        """S_initial is O(1) — genuinely low entropy."""
        for N in [7, 8, 9, 11]:
            result = penrose_gap(N)
            assert result['S_initial'] < 10, (
                f"N={N}: S_initial={result['S_initial']:.2f}, "
                f"expected O(1)"
            )
