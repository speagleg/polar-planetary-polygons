"""Tests for coupling constants from S³ (GAP E)."""

import pytest
from math import pi


class TestCSCouplings:
    """Chern-Simons coupling constants at level k=1."""

    def test_e8_inverse_coupling(self):
        """E₈ at k=1: 1/g² = 1 + 30 = 31."""
        from planetary_polygons.proofs.coupling_constants import cs_inverse_coupling
        assert cs_inverse_coupling('E8') == 31

    def test_su3_inverse_coupling(self):
        """SU(3) at k=1: 1/g² = 1 + 3 = 4."""
        from planetary_polygons.proofs.coupling_constants import cs_inverse_coupling
        assert cs_inverse_coupling('SU(3)') == 4

    def test_su2_inverse_coupling(self):
        """SU(2) at k=1: 1/g² = 1 + 2 = 3."""
        from planetary_polygons.proofs.coupling_constants import cs_inverse_coupling
        assert cs_inverse_coupling('SU(2)') == 3

    def test_e8_central_charge_is_8(self):
        """E₈ WZW at k=1: c = 248/31 = 8 (exactly)."""
        from planetary_polygons.proofs.coupling_constants import wzw_central_charge
        c = wzw_central_charge('E8')
        assert abs(c - 8.0) < 1e-10

    def test_weinberg_angle(self):
        """sin²θ_W = 3/11 from WZW conformal weights.

        Derived: h_W = 2/3 (SU(2)₁ adjoint), h_Y = 1/4 (U(1) at K_Y=1/2).
        sin²θ = h_Y/(h_Y+h_W) = (1/4)/(1/4+2/3) = (1/4)/(11/12) = 3/11.
        """
        from planetary_polygons.proofs.coupling_constants import weinberg_angle_cs
        sin2 = weinberg_angle_cs()
        assert abs(sin2 - 3.0 / 11.0) < 1e-10


class TestE8ToSMReduction:
    """E₈ → SM coupling reduction at K=0."""

    def test_level_preserved(self):
        """CS level k=1 is preserved at the transition."""
        from planetary_polygons.proofs.coupling_constants import e8_to_sm_coupling_reduction
        result = e8_to_sm_coupling_reduction()
        assert result['e8_level'] == 1
        assert result['sm_level'] == 1
        assert result['level_preserved']

    def test_e8_c_equals_8(self):
        """E₈ central charge c=8 (consistency check)."""
        from planetary_polygons.proofs.coupling_constants import e8_to_sm_coupling_reduction
        result = e8_to_sm_coupling_reduction()
        assert result['e8_c_is_8']

    def test_u1_level_is_one(self):
        """U(1)_Y level k_Y = 1 (compact boson, single-valued holonomy)."""
        from planetary_polygons.proofs.coupling_constants import e8_to_sm_coupling_reduction
        result = e8_to_sm_coupling_reduction()
        assert abs(result['u1_level'] - 1.0) < 1e-10

    def test_coupling_hierarchy(self):
        """Non-abelian SM couplings: 1/g₃² = 4 > 1/g₂² = 3."""
        from planetary_polygons.proofs.coupling_constants import e8_to_sm_coupling_reduction
        result = e8_to_sm_coupling_reduction()
        assert result['su3_inverse_coupling'] > result['su2_inverse_coupling']


class TestSpectralWeinberg:
    """Tests for the spectral derivation of sin²θ_W = 3/11."""

    def test_spectral_denominators_sum_11(self):
        from planetary_polygons.proofs.mark_distribution import spectral_denominators
        assert sum(spectral_denominators(h=30)) == 11

    def test_spectral_weinberg(self):
        from planetary_polygons.proofs.coupling_constants import spectral_weinberg_angle
        sin2 = spectral_weinberg_angle()
        assert abs(sin2 - 3/11) < 1e-15

    def test_weinberg_equals_existing(self):
        """Spectral derivation matches existing CS derivation."""
        from planetary_polygons.proofs.coupling_constants import (
            weinberg_angle_cs, spectral_weinberg_angle,
        )
        assert abs(weinberg_angle_cs() - spectral_weinberg_angle()) < 1e-15

    def test_weinberg_formula(self):
        """sin²θ = (a-1)/(a+N_crit) = (dim-1)/(dim+stability)."""
        a = 4
        n_crit = 7
        assert abs((a - 1) / (a + n_crit) - 3 / 11) < 1e-15


class TestBernoulliCoxeter:
    """Tests for B₄ = B₈ = -1/h(E₈)."""

    def test_b4_equals_b8(self):
        from fractions import Fraction
        from planetary_polygons.proofs.coupling_constants import bernoulli_coxeter
        b4, b8, h = bernoulli_coxeter()
        assert b4 == b8
        assert b4 == Fraction(-1, 30)
        assert h == 30

    def test_zeta_neg3(self):
        """ζ(-3) = -B₄/4 = 1/120 = 1/|I*|."""
        from fractions import Fraction
        from planetary_polygons.proofs.coupling_constants import bernoulli_coxeter
        b4, _, _ = bernoulli_coxeter()
        zeta_neg3 = -b4 / 4
        assert zeta_neg3 == Fraction(1, 120)

    def test_zeta_neg7(self):
        """ζ(-7) = -B₈/8 = 1/240 = 1/roots(E₈)."""
        from fractions import Fraction
        from planetary_polygons.proofs.coupling_constants import bernoulli_coxeter
        _, b8, _ = bernoulli_coxeter()
        zeta_neg7 = -b8 / 8
        assert zeta_neg7 == Fraction(1, 240)
