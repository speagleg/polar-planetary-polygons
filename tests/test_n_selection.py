"""Tests for the N selection principle."""

import pytest
from planetary_polygons.extensions.n_selection import (
    critical_spin, integer_spin_polygons, pell_solutions,
    verify_pell, even_N_integer_spin, n_selection_principle,
)


class TestIntegerSpin:
    def test_j1_at_N4(self):
        j, is_int, _, _ = critical_spin(4)
        assert is_int
        assert int(round(j)) == 1

    def test_j2_at_N7(self):
        j, is_int, _, _ = critical_spin(7)
        assert is_int
        assert int(round(j)) == 2

    def test_no_integer_spin_N5_N6(self):
        for N in [5, 6, 8, 9, 10, 11, 12, 13]:
            _, is_int, _, _ = critical_spin(N)
            assert not is_int, f"N={N} unexpectedly has integer spin"

    def test_only_4_and_7_below_24(self):
        """N=4 and N=7 are the ONLY integer-spin polygons below N=24."""
        results = integer_spin_polygons(23)
        assert results == [(4, 1), (7, 2)]

    def test_N24_is_next_even(self):
        results = integer_spin_polygons(30)
        even_results = [(N, j) for N, j in results if N % 2 == 0]
        assert even_results[0] == (4, 1)
        assert even_results[1] == (24, 8)


class TestPellEquation:
    def test_N7_satisfies_pell(self):
        """7² - 2×5² = 49 - 50 = -1."""
        assert verify_pell(7, 2)

    def test_N41_satisfies_pell(self):
        """41² - 2×29² = 1681 - 1682 = -1."""
        assert verify_pell(41, 14)

    def test_N239_satisfies_pell(self):
        """239² - 2×169² = 57121 - 57122 = -1."""
        assert verify_pell(239, 84)

    def test_first_5_solutions(self):
        """First 5 Pell solutions are (1,0), (7,2), (41,14), (239,84), (1393,492)."""
        sols = pell_solutions(5)
        expected_N = [1, 7, 41, 239, 1393]
        expected_j = [0, 2, 14, 84, 492]
        for (N, _, j), eN, ej in zip(sols, expected_N, expected_j):
            assert N == eN
            assert j == ej

    def test_all_pell_solutions_verify(self):
        for N, _, j in pell_solutions(8):
            if N > 1:
                assert verify_pell(N, j), f"Pell failed at N={N}, j={j}"


class TestEvenN:
    def test_N4_is_first(self):
        results = even_N_integer_spin(10)
        assert results[0] == (4, 1, 1)  # (N, k, j)

    def test_N24_is_second(self):
        results = even_N_integer_spin(10)
        assert results[1] == (24, 6, 8)


class TestSelectionPrinciple:
    def test_N_EW_is_4(self):
        sel = n_selection_principle()
        assert sel['N_EW'] == 4
        assert sel['j_EW'] == 1

    def test_N_grav_is_7(self):
        sel = n_selection_principle()
        assert sel['N_grav'] == 7
        assert sel['j_grav'] == 2

    def test_N_cosmo_is_11(self):
        sel = n_selection_principle()
        assert sel['N_cosmo'] == 11
        assert sel['N_cosmo'] == sel['N_EW'] + sel['N_grav']

    def test_pell_verified(self):
        sel = n_selection_principle()
        assert sel['pell_verified']

    def test_next_solutions_far(self):
        """Next integer-spin polygons (24, 41) are far above N_crit=7."""
        sel = n_selection_principle()
        assert sel['next_even'][0] == 24  # N=24
        assert sel['next_odd_pell'][0] == 41  # N=41

    def test_3_generations(self):
        """3 generations = (N_grav - 1)/2 = 3, derived from Pell."""
        sel = n_selection_principle()
        assert sel['n_generations'] == 3
        assert sel['n_generations'] == (sel['N_grav'] - 1) // 2

    def test_gen_equals_color(self):
        """n_gen = n_color = 3 because N=7 is prime."""
        sel = n_selection_principle()
        assert sel['n_colors'] == 3
        assert sel['gen_equals_color'] is True
