"""Tests for the Standard Model gauge group from the polygon hierarchy."""

import math
import pytest
from planetary_polygons.extensions.standard_model_gauge import (
    casimir, spin_j, trace_field_degree,
    galois_action_on_pairs, su3_from_galois, su2_from_cs,
    u1_from_kk, weinberg_angle, two_force_unification,
    standard_model_table,
)


class TestGraviton:
    def test_j2_at_N7(self):
        """j = 2 at N=7 (the graviton)."""
        assert spin_j(3, 7) == pytest.approx(2.0)

    def test_j1_at_N4(self):
        """j = 1 at N=4 (the gauge boson)."""
        assert spin_j(2, 4) == pytest.approx(1.0)

    def test_j2_unique_to_N7(self):
        """j = 2 at the critical mode occurs ONLY at N=7."""
        for N in range(3, 31):
            if N == 7:
                continue
            m = N // 2
            j = spin_j(m, N)
            assert abs(j - 2.0) > 0.01, f"N={N} also has j=2!"


class TestSU3:
    def test_trace_field_degree_7(self):
        """K₇ has degree 3 over Q."""
        assert trace_field_degree(7) == 3

    def test_galois_cyclic_permutation(self):
        """Gal(K₇/Q) = Z/3Z cyclically permutes the 3 pairs."""
        ga = galois_action_on_pairs(7)
        assert ga['n_pairs'] == 3
        assert ga['is_cyclic_permutation'] is True

    def test_su3_emerges(self):
        result = su3_from_galois(7)
        assert result['gauge_group'] == 'SU(3)'
        assert result['trace_field_degree'] == 3

    def test_three_colors(self):
        """3 palindromic pairs = 3 colors."""
        result = su3_from_galois(7)
        assert len(result['pairs']) == 3
        assert result['casimirs'] == [3.0, 5.0, 6.0]


class TestSU2:
    def test_j1_is_adjoint(self):
        result = su2_from_cs(4)
        assert result['is_adjoint'] is True
        assert result['dim_rep'] == 3
        assert result['gauge_group'] == 'SU(2)'


class TestU1:
    def test_kk(self):
        result = u1_from_kk()
        assert result['gauge_group'] == 'U(1)'


class TestWeinbergAngle:
    def test_3_over_11(self):
        """sin²θ_W = 3/11 at the polygon scale."""
        result = weinberg_angle(4)
        assert result['sin2_theta_W'] == pytest.approx(3 / 11)

    def test_closer_than_su5(self):
        """Our prediction is closer to experiment than SU(5) GUT."""
        result = weinberg_angle(4)
        assert result['discrepancy_pct'] < result['su5_discrepancy_pct']

    def test_between_experiment_and_su5(self):
        """3/11 is between experiment (0.231) and SU(5) (0.375)."""
        result = weinberg_angle(4)
        assert 0.231 < result['sin2_theta_W'] < 0.375


class TestTwoForceUnification:
    def test_complete(self):
        result = two_force_unification()
        assert result['gauge_group'] == 'SU(3) × SU(2) × U(1)'
        assert result['force_1']['N'] == 7
        assert result['force_2']['N'] == 4

    def test_unification_field(self):
        result = two_force_unification()
        assert 'ζ₅₆' in result['unification_field']


class TestStandardModelTable:
    def test_table(self):
        table = standard_model_table()
        assert len(table) == 13  # N=3..15
        # N=4 is gauge boson
        n4 = [r for r in table if r['N'] == 4][0]
        assert n4['j_integer'] == 1
        # N=7 is graviton
        n7 = [r for r in table if r['N'] == 7][0]
        assert n7['j_integer'] == 2
