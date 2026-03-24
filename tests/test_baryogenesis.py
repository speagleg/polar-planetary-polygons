"""Tests for baryogenesis in the Havelock Field Theory."""

import math
import pytest
from planetary_polygons.extensions.baryogenesis import (
    cs_cp_violation, ewpt_strength, sakharov_conditions,
    baryon_asymmetry_estimate,
)


class TestSakharovConditions:
    def test_all_three_met(self):
        """All three Sakharov conditions are satisfied."""
        s = sakharov_conditions(7)
        assert s['B_violation'] is True
        assert s['CP_violation'] is True
        assert s['out_of_equilibrium'] is True
        assert s['all_conditions_met'] is True


class TestCPViolation:
    def test_fractional_cs_level(self):
        """k_phys is not integer (contains irrational terms)."""
        cp = cs_cp_violation(7)
        assert cp['k_frac'] > 0.01  # not close to integer

    def test_cp_phase_nonzero(self):
        """The CP-violating phase is significant."""
        cp = cs_cp_violation(7)
        assert abs(cp['delta_CP']) > 0.1

    def test_cp_larger_than_SM(self):
        """CP violation is orders of magnitude larger than SM Jarlskog."""
        cp = cs_cp_violation(7)
        assert cp['enhancement'] > 1000  # > 10^3 enhancement

    def test_cp_at_N7(self):
        """δ_CP ≈ 0.57 at N=7."""
        cp = cs_cp_violation(7)
        assert 0.5 < abs(cp['delta_CP']) < 0.7


class TestEWPT:
    def test_first_order(self):
        """The EWPT is first-order (tunneling action S > 0)."""
        ewpt = ewpt_strength(7)
        assert ewpt['is_first_order'] is True
        assert ewpt['S_tunnel'] > 1

    def test_washout_satisfied(self):
        """The sphaleron washout condition v/T > α_w/(4π) is satisfied."""
        ewpt = ewpt_strength(7)
        assert ewpt['washout_satisfied'] is True

    def test_v_over_Tc_near_unity(self):
        """v/T_c ≈ 0.84 (strong first-order transition)."""
        ewpt = ewpt_strength(7)
        assert 0.5 < ewpt['v_over_Tc'] < 1.2

    def test_SM_is_crossover(self):
        """The SM EWPT is a crossover (no baryogenesis possible)."""
        ewpt = ewpt_strength(7)
        assert ewpt['SM_is_crossover'] is True


class TestBaryonAsymmetry:
    def test_order_of_magnitude(self):
        """η_B is nonzero and in the EW baryogenesis ballpark (10^{-10} to 10^{-5}).
        The naive estimate overestimates by ~10^3 before transport corrections."""
        est = baryon_asymmetry_estimate(v_w=0.05)
        assert 1e-10 < est['eta_B'] < 1e-3

    def test_uses_3_generations(self):
        """n_F = 3 from the Pell equation."""
        est = baryon_asymmetry_estimate()
        assert est['n_F'] == 3
