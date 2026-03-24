"""Tests for the electroweak hierarchy from the hybrid instanton."""

import math
import pytest
from planetary_polygons.extensions.hierarchy import (
    hierarchy_decomposition, why_10_to_17, pi_bridge,
    tunneling_action, find_threshold_BO, V_BO,
    EPSILON_7, EPSILON_2, MASS_GAP_ASYMP, M_P_OVER_MEW,
)


class TestHierarchyDecomposition:
    def test_log_match_within_01_percent(self):
        """ln(M_P/M_EW) matches to < 0.01% in the log."""
        h = hierarchy_decomposition()
        assert h['log_match_pct'] < 0.01

    def test_ratio_match_within_1_percent(self):
        """M_P/M_EW matches to < 0.2%."""
        h = hierarchy_decomposition()
        assert h['ratio_match_pct'] < 0.2

    def test_higgs_vev_prediction(self):
        """Predicts v within 0.2% of 246.22 GeV."""
        h = hierarchy_decomposition()
        assert h['v_match_pct'] < 0.2

    def test_pell_identity(self):
        """2S_BO + √(2/π)×ln(ε₇) = 14×ln(ε₇) to < 0.02%."""
        h = hierarchy_decomposition()
        assert h['pell_match_pct'] < 0.02

    def test_three_components_sum(self):
        """The three components sum to the total."""
        h = hierarchy_decomposition()
        expected = h['S_bounce'] + h['mass_gap_term'] + h['gravity_term']
        assert h['total_log'] == pytest.approx(expected)

    def test_instanton_dominates(self):
        """The instanton contributes > 90% of the Pell exponent."""
        h = hierarchy_decomposition()
        assert h['instanton_fraction'] > 0.90

    def test_mass_gap_is_correction(self):
        """The mass gap contributes < 10% of the Pell exponent."""
        h = hierarchy_decomposition()
        assert h['mass_gap_fraction'] < 0.10
        assert h['mass_gap_fraction'] > 0.04  # but not negligible


class TestInstanton:
    def test_tunneling_action_positive(self):
        """The tunneling action is positive for N=7."""
        S = tunneling_action(7)
        assert S > 10

    def test_bounce_is_2S(self):
        """The bounce action is exactly twice the tunneling action."""
        S = tunneling_action(7)
        h = hierarchy_decomposition()
        assert h['S_bounce'] == pytest.approx(2 * S, rel=1e-4)

    def test_threshold_N7(self):
        """The BO threshold for N=7 is around ρ* ≈ 1.73."""
        rho = find_threshold_BO(7)
        assert 1.5 < rho < 2.0

    def test_potential_negative_below_threshold(self):
        """V_BO < 0 for ρ < ρ*."""
        rho_star = find_threshold_BO(7)
        for rho in [0.1, 0.5, 1.0, rho_star - 0.1]:
            assert V_BO(rho, 7) < 0

    def test_potential_positive_above_threshold(self):
        """V_BO > 0 for ρ > ρ*."""
        rho_star = find_threshold_BO(7)
        for rho in [rho_star + 0.1, 3.0, 5.0]:
            assert V_BO(rho, 7) > 0


class TestMassGap:
    def test_asymptotic_value(self):
        """√(2/π) = 0.79788..."""
        assert MASS_GAP_ASYMP == pytest.approx(math.sqrt(2 / math.pi))

    def test_mass_gap_times_ln_eps7(self):
        """√(2/π) × ln(ε₇) ≈ 2.209."""
        val = MASS_GAP_ASYMP * math.log(EPSILON_7)
        assert 2.2 < val < 2.3


class TestAnthropicBound:
    def test_N7_gives_moderate_hierarchy(self):
        """N=7 gives hierarchy ~10^17 (moderate, allows atoms)."""
        results = why_10_to_17()
        n7 = [r for r in results if r['N_grav'] == 7][0]
        assert 16 < n7['log10'] < 18
        assert n7['viable'] is True

    def test_N41_gives_extreme_hierarchy(self):
        """N=41 gives hierarchy ~10^99 (no atoms possible)."""
        results = why_10_to_17()
        n41 = [r for r in results if r['N_grav'] == 41][0]
        assert n41['log10'] > 90
        assert n41['viable'] is False

    def test_only_N7_viable(self):
        """N=7 is the ONLY Pell graviton with a viable hierarchy."""
        results = why_10_to_17()
        viable = [r for r in results if r['viable']]
        assert len(viable) == 1
        assert viable[0]['N_grav'] == 7


class TestPiBridge:
    def test_eps2_pi_approx_eps7(self):
        """(1+√2)^π ≈ 8+3√7 to better than 0.03%."""
        pb = pi_bridge()
        assert pb['match_pct'] < 0.03

    def test_pell_identity_algebraic(self):
        """ε₇ × (8-3√7) = 1."""
        eps_inv = 8 - 3 * math.sqrt(7)
        assert EPSILON_7 * eps_inv == pytest.approx(1.0)
