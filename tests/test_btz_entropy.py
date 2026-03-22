"""Tests for BTZ entropy from palindromic wall-crossing."""

import math
import pytest
from planetary_polygons.extensions.btz_entropy import (
    casimir, b_exact, find_threshold, wall_crossing_entropy,
    one_loop_entropy, entropy_decomposition, wall_crossing_table,
    morse_index_L2, fractional_morse_index, btz_entropy_cardy,
    palindromic_field, BOLZA_EIGENVALUES_TRIVIAL,
)


class TestWallCrossingEntropy:
    def test_even_N_self_paired(self):
        """Even N gives log(2) (self-paired critical mode)."""
        for N in [8, 10, 12, 14]:
            dS, self_paired, _ = wall_crossing_entropy(N)
            assert self_paired is True
            assert abs(dS - math.log(2)) < 1e-14

    def test_odd_N_paired(self):
        """Odd N gives 2*log(2) (paired modes)."""
        for N in [7, 9, 11, 13]:
            dS, self_paired, _ = wall_crossing_entropy(N)
            assert self_paired is False
            assert abs(dS - 2 * math.log(2)) < 1e-14

    def test_pattern_1_or_2_bits(self):
        """Each crossing is exactly 1 or 2 bits."""
        for N in range(7, 20):
            dS, _, _ = wall_crossing_entropy(N)
            bits = dS / math.log(2)
            assert bits == pytest.approx(1.0) or bits == pytest.approx(2.0)


class TestWallCrossingTable:
    def test_cumulative_bits_N12(self):
        """Through N=12: exactly 9 bits (from the user's computation)."""
        rows = wall_crossing_table(N_max=12)
        final_bits = rows[-1][4]
        assert final_bits == pytest.approx(9.0)

    def test_monotonic(self):
        rows = wall_crossing_table(N_max=15)
        for i in range(len(rows) - 1):
            assert rows[i + 1][4] > rows[i][4]

    def test_fields_known(self):
        rows = wall_crossing_table(N_max=12)
        fields = {r[0]: r[3] for r in rows}
        assert "Q(cos(2pi/7))" in fields[7]
        assert "sqrt(2)" in fields[8]
        assert "sqrt(5)" in fields[10]


class TestOneLoopEntropy:
    def test_positive(self):
        """S_1loop > 0 for N >= 7 (N=6 is marginal with ~0 entropy)."""
        for N in range(7, 16):
            S = one_loop_entropy(N)
            assert S > 0

    def test_grows_with_N(self):
        """One-loop entropy grows with N."""
        prev = one_loop_entropy(6)
        for N in range(7, 15):
            curr = one_loop_entropy(N)
            assert curr > prev
            prev = curr


class TestEntropyDecomposition:
    def test_decomposition_sums(self):
        """S_total = S_wc + S_1loop."""
        result = entropy_decomposition(N_min=7, N_max=17)
        assert result['S_total'] == pytest.approx(
            result['S_wc_total'] + result['S_1loop_total'])

    def test_wc_fraction(self):
        """Wall-crossing is a small fraction (~10%) of total."""
        result = entropy_decomposition(N_min=7, N_max=17)
        frac = result['S_wc_total'] / result['S_total']
        assert frac < 0.15  # ~9.3% per user's computation

    def test_11_crossings(self):
        """11 wall-crossings from N=7 to 17."""
        result = entropy_decomposition(N_min=7, N_max=17)
        assert len(result['terms']) == 11

    def test_wc_bits(self):
        """11 crossings: 6 odd (2 bits each) + 5 even (1 bit each) = 17 bits."""
        result = entropy_decomposition(N_min=7, N_max=17)
        # Odd: 7,9,11,13,15,17 = 6 crossings × 2 bits = 12
        # Even: 8,10,12,14,16 = 5 crossings × 1 bit = 5
        # Total = 17 bits
        expected_bits = 6 * 2 + 5 * 1
        assert result['bits_wc'] == pytest.approx(expected_bits)


class TestMorseIndex:
    def test_L2_integer_without_bolza(self):
        """Without Bolza data, tau = integer Morse index."""
        N, rho = 8, 3.0
        tau, n_neg, eigs = morse_index_L2(N, rho, bolza_eigenvalues=None)
        assert tau == float(n_neg)

    def test_L2_with_bolza(self):
        """With Bolza data, tau is a finite positive number."""
        N, rho = 10, 2.0
        tau, n_neg, eigs = morse_index_L2(N, rho, BOLZA_EIGENVALUES_TRIVIAL)
        assert tau >= 0
        assert isinstance(tau, float)

    def test_fractional_at_threshold(self):
        """At threshold, tau should be finite and non-negative."""
        N = 8
        rho_star = find_threshold(N)
        tau, n_neg, closest = fractional_morse_index(N, rho_star)
        assert tau >= 0
        assert isinstance(tau, float)


class TestBTZCardy:
    def test_zero_at_threshold(self):
        assert btz_entropy_cardy(100, E=0) == 0.0

    def test_positive_E(self):
        S = btz_entropy_cardy(100, E=1.0)
        expected = 2 * math.pi * math.sqrt(100 / 6)
        assert S == pytest.approx(expected)


class TestPalindromicField:
    def test_rational_cases(self):
        for N in [3, 4, 6]:
            D, deg, f = palindromic_field(N)
            assert f == "Q"

    def test_golden(self):
        _, _, f = palindromic_field(5)
        assert "sqrt(5)" in f

    def test_silver(self):
        _, _, f = palindromic_field(8)
        assert "sqrt(2)" in f


class TestBolzaEigenvalues:
    def test_first_eigenvalue(self):
        """Bolza first eigenvalue ~ 3.839."""
        assert abs(BOLZA_EIGENVALUES_TRIVIAL[0] - 3.8388872588) < 1e-8

    def test_count(self):
        """We have 25 Bolza eigenvalues."""
        assert len(BOLZA_EIGENVALUES_TRIVIAL) == 25
