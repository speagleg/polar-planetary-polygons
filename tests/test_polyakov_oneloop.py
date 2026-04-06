"""Tests for the Polyakov one-loop correction to sigma/Lambda^2."""

import pytest
from math import pi, sqrt, exp

from planetary_polygons.proofs.polyakov_oneloop import (
    monopole_action,
    determinant_prefactor,
    dressed_fugacity,
    tree_level_string_tension,
    seeley_dewitt_a1,
    seeley_dewitt_a2,
    correction_A_spectral,
    correction_B_zero_mode,
    correction_C_interaction,
    one_loop_correction,
    verify_a2_exact,
    correction_budget,
)


class TestTreeLevel:
    def test_monopole_action(self):
        S = monopole_action(k=1, K=-1)
        assert abs(S - 5*pi/3) < 1e-12

    def test_prefactor(self):
        pf = determinant_prefactor(5*pi/3)
        assert abs(pf - (5/6)**1.5) < 1e-10

    def test_fugacity(self):
        S = 5*pi/3
        pf = (5/6)**1.5
        y = dressed_fugacity(S, pf)
        assert abs(y - 0.00405) < 0.0001

    def test_tree_string_tension(self):
        r = tree_level_string_tension()
        assert abs(r['sigma_over_Lambda2'] - 5.97) < 0.03


class TestSeeleyDeWitt:
    def test_a1_on_H2(self):
        assert abs(seeley_dewitt_a1(-1) - (-1/3)) < 1e-12

    def test_a2_on_H2(self):
        assert abs(seeley_dewitt_a2(-1) - 4/135) < 1e-12

    def test_a2_exact_rational(self):
        v = verify_a2_exact()
        assert v['verified']
        assert v['numerator'] == 4
        assert v['denominator'] == 135

    def test_a2_positive(self):
        """a_2 > 0 on any constant-curvature surface (K^2 > 0)."""
        for K in [-2, -1, -0.5, 0.5, 1, 2]:
            assert seeley_dewitt_a2(K) > 0


class TestCorrections:
    def test_A_spectral_negative(self):
        """Spectral correction decreases fugacity (more fluctuations)."""
        delta_A, _ = correction_A_spectral()
        assert delta_A < 0

    def test_B_zero_mode_positive(self):
        """Zero-mode correction increases fugacity (larger moduli space)."""
        delta_B = correction_B_zero_mode()
        assert delta_B > 0

    def test_B_dominates_A(self):
        """Zero-mode correction dominates spectral correction."""
        delta_A, _ = correction_A_spectral()
        delta_B = correction_B_zero_mode()
        assert abs(delta_B) > abs(delta_A)

    def test_C_interaction_positive(self):
        """Monopole interaction enhances confinement."""
        rel_C = correction_C_interaction()
        assert rel_C > 0

    def test_C_small(self):
        """Interaction correction is a few percent."""
        rel_C = correction_C_interaction()
        assert rel_C < 0.05


class TestOneLoopResult:
    def test_closes_gap(self):
        r = one_loop_correction()
        assert r['closes_gap']

    def test_within_lattice_error(self):
        r = one_loop_correction()
        assert r['within_lattice_error']

    def test_corrected_above_tree(self):
        r = one_loop_correction()
        assert r['sigma_corrected'] > r['sigma_tree']

    def test_correction_positive(self):
        budget = correction_budget()
        assert budget['total_shift'] > 0

    def test_correction_order_10_percent(self):
        """Total correction should be O(10%) — not negligible, not huge."""
        budget = correction_budget()
        assert 1 < budget['total_shift_percent'] < 20
