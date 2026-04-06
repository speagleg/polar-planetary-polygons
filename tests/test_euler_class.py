"""
Tests for the equivariant Euler class sign change at N=7->8.
"""

import pytest
from planetary_polygons.proofs.euler_class import (
    negative_modes,
    zero_modes,
    euler_class_degree,
    euler_class_transition_table,
    topological_obstruction,
)


class TestNegativeModes:
    @pytest.mark.parametrize("N", [3, 4, 5, 6])
    def test_no_negative_modes_small_N(self, N):
        assert negative_modes(N) == []

    def test_n7_no_negative_but_zero(self):
        assert negative_modes(7) == []
        assert zero_modes(7) == [3, 4]

    def test_n8_negative_modes(self):
        assert negative_modes(8) == [3, 4, 5]

    def test_n9_negative_modes(self):
        assert negative_modes(9) == [3, 4, 5, 6]

    @pytest.mark.parametrize("N", range(8, 20))
    def test_negative_count_is_N_minus_5(self, N):
        assert len(negative_modes(N)) == N - 5


class TestEulerClass:
    @pytest.mark.parametrize("N", [3, 4, 5, 6])
    def test_trivial_for_small_N(self, N):
        assert euler_class_degree(N) == 0

    def test_degenerate_at_7(self):
        assert zero_modes(7) == [3, 4]
        # Euler class is undefined at N=7

    @pytest.mark.parametrize("N", range(8, 16))
    def test_nontrivial_for_large_N(self, N):
        assert euler_class_degree(N) > 0
        assert euler_class_degree(N) == N - 5


class TestTransition:
    def test_transition_table(self):
        table = euler_class_transition_table(12)
        for row in table:
            if row['N'] <= 6:
                assert 'TRIVIAL' in row['status']
            elif row['N'] == 7:
                assert 'DEGENERATE' in row['status']
            else:
                assert 'NON-TRIVIAL' in row['status']

    def test_sign_change_exactly_at_7(self):
        """The Euler class changes from trivial to non-trivial
        at N=7, with N=7 as the unique singular transition."""
        obs_6 = topological_obstruction(6)
        obs_7 = topological_obstruction(7)
        obs_8 = topological_obstruction(8)

        assert obs_6['has_obstruction'] == False
        assert obs_7['has_obstruction'] is None  # degenerate
        assert obs_8['has_obstruction'] == True


class TestPalindromicPairs:
    @pytest.mark.parametrize("N", range(8, 16))
    def test_palindromic_pairing(self, N):
        """Negative modes come in palindromic pairs {m, N-m}."""
        neg = negative_modes(N)
        for m in neg:
            assert (N - m) in neg, f"N={N}: mode {m} negative but {N-m} not"

    @pytest.mark.parametrize("N", range(8, 16))
    def test_obstruction_has_pairs(self, N):
        obs = topological_obstruction(N)
        assert obs['has_obstruction']
        pairs = obs['palindromic_pairs']
        assert len(pairs) > 0
        for m, partner in pairs:
            assert m + partner == N
