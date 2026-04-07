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
