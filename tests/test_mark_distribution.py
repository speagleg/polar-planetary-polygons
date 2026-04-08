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
