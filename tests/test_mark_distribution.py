"""Tests for the I* mark distribution and its identities."""

import pytest
from fractions import Fraction


class TestADEMarks:
    """Tests for ADE affine mark data."""

    def test_e8_marks(self):
        from planetary_polygons.proofs.mark_distribution import ade_marks
        assert ade_marks('E8') == [1, 2, 3, 4, 5, 6, 4, 2, 3]

    def test_e7_marks(self):
        from planetary_polygons.proofs.mark_distribution import ade_marks
        assert ade_marks('E7') == [1, 2, 3, 4, 3, 2, 1, 2]

    def test_e6_marks(self):
        from planetary_polygons.proofs.mark_distribution import ade_marks
        assert ade_marks('E6') == [1, 1, 2, 2, 3, 2, 1]

    def test_e8_coxeter_number(self):
        from planetary_polygons.proofs.mark_distribution import ade_marks
        assert sum(ade_marks('E8')) == 30

    def test_e8_group_order(self):
        from planetary_polygons.proofs.mark_distribution import ade_marks
        m = ade_marks('E8')
        assert sum(d**2 for d in m) == 120


class TestMarkBalance:
    """Tests for the mark-balance identity Σd(d-k₁)=0."""

    def test_e8_balance(self):
        from planetary_polygons.proofs.mark_distribution import mark_balance
        bal, k1 = mark_balance([1, 2, 3, 4, 5, 6, 4, 2, 3])
        assert bal == 0
        assert k1 == Fraction(4)

    def test_e8_pivot_4_unique(self):
        """Pivot k₁ = 4 holds ONLY for E₈ among all exceptional types."""
        from planetary_polygons.proofs.mark_distribution import mark_balance, ade_marks
        for t in ['E6', 'E7']:
            _, k1 = mark_balance(ade_marks(t))
            assert k1 != Fraction(4), f"{t} should NOT have k₁ = 4"
        _, k1_e8 = mark_balance(ade_marks('E8'))
        assert k1_e8 == Fraction(4)

    def test_e6_pivot_is_2(self):
        from planetary_polygons.proofs.mark_distribution import mark_balance
        _, k1 = mark_balance([1, 1, 2, 2, 3, 2, 1])
        assert k1 == Fraction(2)

    def test_e8_gauss_bonnet(self):
        """Mark-balance equivalent to |I*| = 4h (Gauss-Bonnet tiling)."""
        from planetary_polygons.proofs.mark_distribution import ade_marks
        m = ade_marks('E8')
        assert sum(d**2 for d in m) == 4 * sum(m)


class TestVtensorF:
    """Tests for V⊗F = 4×reg(A₅)."""

    def test_icosahedron_vf_equals_roots(self):
        from planetary_polygons.proofs.mark_distribution import vtensor_f_multiplicity
        k = vtensor_f_multiplicity(V=12, F=20, stab_V=5, stab_F=3, group_order=60)
        assert k == 4  # V⊗F = 4 × reg(A₅)
        assert 12 * 20 == 240  # = roots(E₈)

    def test_octahedron_vf(self):
        from planetary_polygons.proofs.mark_distribution import vtensor_f_multiplicity
        k = vtensor_f_multiplicity(V=6, F=8, stab_V=4, stab_F=3, group_order=24)
        assert k == 2  # V⊗F = 2 × reg(S₄)

    def test_tetrahedron_not_regular(self):
        """Tetrahedron: gcd(3,3)=3≠1, so V⊗F is NOT a multiple of reg."""
        from planetary_polygons.proofs.mark_distribution import vtensor_f_multiplicity
        k = vtensor_f_multiplicity(V=4, F=4, stab_V=3, stab_F=3, group_order=12)
        assert k is None


class TestChargeMagnitudeChain:
    """Tests for the iterated charge-magnitude map E₈→E₆→A₃→∅."""

    def test_e8_to_e6(self):
        from planetary_polygons.proofs.mark_distribution import charge_magnitude_map
        target, kernel = charge_magnitude_map([1, 2, 3, 4, 5, 6, 4, 2, 3], pivot=4)
        assert sorted(target) == sorted([1, 1, 1, 2, 2, 2, 3])
        assert kernel == [4, 4]

    def test_e6_to_a3(self):
        from planetary_polygons.proofs.mark_distribution import charge_magnitude_map
        target, kernel = charge_magnitude_map([1, 1, 2, 2, 3, 2, 1], pivot=2)
        assert sorted(target) == [1, 1, 1, 1]
        assert sorted(kernel) == [2, 2, 2]

    def test_full_chain(self):
        from planetary_polygons.proofs.mark_distribution import division_algebra_chain
        chain = division_algebra_chain([1, 2, 3, 4, 5, 6, 4, 2, 3])
        pivots = [step['pivot'] for step in chain]
        assert pivots == [4, 2, 1]
        assert sum(pivots) == 7
        assert 4 * 2 * 1 == 8


class TestPivotUniqueness:
    """Test the uniqueness theorem: (4,2,1) unique with Σ=Π-1."""

    def test_uniqueness(self):
        from planetary_polygons.proofs.mark_distribution import sum_equals_product_minus_one
        solutions = sum_equals_product_minus_one(max_a=20)
        assert solutions == [(4, 2, 1)]

    def test_product_identity(self):
        """Πdᵢ = 6!×4! = 17280."""
        from planetary_polygons.proofs.mark_distribution import ade_marks
        from math import factorial
        m = ade_marks('E8')
        prod = 1
        for d in m:
            prod *= d
        assert prod == factorial(6) * factorial(4)
