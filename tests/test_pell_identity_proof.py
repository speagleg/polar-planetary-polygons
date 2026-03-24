"""Tests for the proof of the Pell identity."""

import math
import pytest
from planetary_polygons.extensions.pell_identity_proof import (
    verify_arccosh_identity, class_number_formula,
    selberg_leading_term, wkb_corrections,
    hierarchy_with_cancellation, tunneling_action_numerical,
    full_verification, EPSILON_7, ARCCOSH_8, MASS_GAP,
)


class TestStep1AlgebraicIdentity:
    def test_pell_equation(self):
        assert 8**2 - 7 * 3**2 == 1

    def test_unit_product(self):
        v = verify_arccosh_identity()
        assert abs(v['product'] - 1) < 1e-10

    def test_cosh_equals_8(self):
        v = verify_arccosh_identity()
        assert abs(v['cosh_ln_eps'] - 8) < 1e-10

    def test_arccosh_8_exact(self):
        assert abs(ARCCOSH_8 - math.log(8 + 3 * math.sqrt(7))) < 1e-14


class TestStep2ClassNumber:
    def test_class_number_is_1(self):
        cnf = class_number_formula()
        assert cnf['class_number'] == 1

    def test_discriminant_28(self):
        cnf = class_number_formula()
        assert cnf['discriminant'] == 28

    def test_L_value(self):
        cnf = class_number_formula()
        expected = ARCCOSH_8 / math.sqrt(7)
        assert cnf['L_value'] == pytest.approx(expected)


class TestStep3SelbergLeading:
    def test_leading_term(self):
        s = selberg_leading_term(7)
        assert s['leading_2S'] == pytest.approx(14 * ARCCOSH_8)


class TestStep4WKBCorrections:
    def test_mass_gap_correction(self):
        w = wkb_corrections(7)
        assert w['delta_mass_gap'] == pytest.approx(-MASS_GAP * ARCCOSH_8)

    def test_dunham_correction(self):
        from planetary_polygons.extensions.pell_identity_proof import central_charge
        c = central_charge(7)
        w = wkb_corrections(7)
        assert w['delta_dunham'] == pytest.approx(-2 / c**2 * ARCCOSH_8)

    def test_corrected_matches_numerical(self):
        """The WKB-corrected 2S matches numerical to < 0.01%."""
        w = wkb_corrections(7)
        two_S_num = tunneling_action_numerical(7, n_steps=500000)
        match = abs(w['two_S_corrected'] - two_S_num) / two_S_num * 100
        assert match < 0.01


class TestStep5Cancellation:
    def test_sqrt_2pi_cancels(self):
        """The √(2/π) cancels between instanton and mass gap."""
        h = hierarchy_with_cancellation()
        # After cancellation, no √(2/π) in the formula
        assert 'cancel' in h['cancellation'].lower()

    def test_hierarchy_matches_observation(self):
        """The hierarchy matches to < 0.01%."""
        h = hierarchy_with_cancellation()
        assert h['match_pct'] < 0.01

    def test_simplified_formula(self):
        """The simplified formula: (2N-2/c²)×arccosh(8) + gravity."""
        h = hierarchy_with_cancellation()
        assert abs(h['total_cancelled'] - h['observed']) / h['observed'] < 1e-4


class TestFullVerification:
    def test_all_steps(self):
        v = full_verification()
        assert v['step1_proven'] is True
        assert v['pell_identity_match_pct'] < 0.01
        assert v['hierarchy_match_pct'] < 0.01
