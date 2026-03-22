"""Tests for the number-theoretic gravity partition function."""

import math
import pytest
from planetary_polygons.extensions.gravity_partition import (
    b_exact, casimir, frozen_determinant_log, gravitational_action,
    gravity_partition_function, palindromic_polynomial_discriminant,
    legendre_symbol, visibility_pattern, selberg_contribution,
    assembly_map_table, organize_by_field, full_analysis,
)


class TestCasimir:
    def test_casimir_values(self):
        assert casimir(1, 6) == 2.5
        assert casimir(2, 6) == 4.0
        assert casimir(3, 6) == 4.5

    def test_casimir_symmetric(self):
        for N in range(4, 12):
            for m in range(1, N):
                assert abs(casimir(m, N) - casimir(N - m, N)) < 1e-14


class TestBExact:
    def test_b3(self):
        """b(3) = 3*4/12 - log(2) + log(3)/2."""
        expected = 1.0 - math.log(2) + math.log(3) / 2
        assert abs(b_exact(3) - expected) < 1e-14

    def test_b_positive(self):
        for N in range(3, 25):
            assert b_exact(N) > 0

    def test_b_monotonic(self):
        """b(N) is strictly increasing."""
        for N in range(3, 24):
            assert b_exact(N + 1) > b_exact(N)

    def test_b_asymptotic(self):
        """b(N) ~ N^2/12 for large N."""
        for N in [20, 50, 100]:
            ratio = b_exact(N) / (N**2 / 12)
            assert abs(ratio - 1) < 0.2  # within 20%


class TestTraceFields:
    def test_rational_cases(self):
        for N in [3, 4, 6]:
            D, deg, field = palindromic_polynomial_discriminant(N)
            assert D == 1
            assert deg == 1
            assert field == "Q"

    def test_golden_ratio(self):
        for N in [5, 10]:
            D, deg, field = palindromic_polynomial_discriminant(N)
            assert D == 5
            assert deg == 2
            assert "sqrt(5)" in field

    def test_silver_ratio(self):
        D, deg, field = palindromic_polynomial_discriminant(8)
        assert D == 2
        assert deg == 2
        assert "sqrt(2)" in field

    def test_heptagon_cubic(self):
        D, deg, field = palindromic_polynomial_discriminant(7)
        assert deg == 3


class TestFrozenDeterminant:
    def test_even_N_formula(self):
        """Z_frozen = 2^{3(N-2)/4} / (N-3)!! for even N."""
        for N in [4, 6, 8, 10, 12]:
            log_Z = frozen_determinant_log(N)
            # Direct computation
            expected = 3 * (N - 2) / 4 * math.log(2)
            k = N - 3
            while k > 0:
                expected -= math.log(k)
                k -= 2
            assert abs(log_Z - expected) < 1e-12

    def test_N4(self):
        """Z_frozen(4) = 2^{3/2} / 1 = 2*sqrt(2)."""
        log_Z = frozen_determinant_log(4)
        assert abs(math.exp(log_Z) - 2 * math.sqrt(2)) < 1e-10

    def test_positive(self):
        for N in range(3, 15):
            log_Z = frozen_determinant_log(N)
            assert math.exp(log_Z) > 0


class TestGravitationalAction:
    def test_genus_zero(self):
        for N in range(3, 15):
            assert abs(gravitational_action(N) - b_exact(N)) < 1e-14

    def test_genus_one(self):
        for N in range(3, 10):
            I = gravitational_action(N, genus=1)
            assert abs(I - b_exact(N)) < 1e-10  # genus 1: no extra area


class TestPartitionFunction:
    def test_convergence(self):
        """Z converges: N=3..6 captures >99% of Z."""
        Z_total, terms = gravity_partition_function(N_max=20)
        Z_6 = sum(t[6] for t in terms[:4])  # N=3,4,5,6
        assert Z_6 / Z_total > 0.99

    def test_Z_value(self):
        """Z ~ 1.33."""
        Z_total, terms = gravity_partition_function(N_max=20)
        assert 1.0 < Z_total < 2.0

    def test_low_N_dominates(self):
        """N=3,4 together dominate the partition function."""
        Z_total, terms = gravity_partition_function(N_max=20)
        N34_frac = (terms[0][6] + terms[1][6]) / Z_total
        assert N34_frac > 0.5  # N=3,4 together > 50%

    def test_super_exponential_decay(self):
        """The tail sum decays super-exponentially: Z(N>8)/Z < 0.02%."""
        Z_total, terms = gravity_partition_function(N_max=20)
        Z_tail = sum(t[6] for t in terms if t[0] > 8)
        assert Z_tail / Z_total < 2e-4  # < 0.02%


class TestFieldOrganization:
    def test_rational_dominates(self):
        """Q (rational) field captures >90% of Z."""
        Z_total, terms = gravity_partition_function(N_max=20)
        fields = organize_by_field(terms)
        Z_Q = sum(e[2] for e in fields.get("Q", []))
        assert Z_Q / Z_total > 0.90

    def test_golden_ratio_second(self):
        """Q(sqrt(5)) is the leading non-rational correction."""
        Z_total, terms = gravity_partition_function(N_max=20)
        fields = organize_by_field(terms)
        Z_Q5 = sum(e[2] for e in fields.get("Q(sqrt(5))", []))
        Z_Q2 = sum(e[2] for e in fields.get("Q(sqrt(2))", []))
        assert Z_Q5 > Z_Q2  # golden > silver


class TestAssemblyMap:
    def test_c_near_N_squared(self):
        """c = 12*b(N) ~ N^2 at leading order."""
        rows = assembly_map_table(N_max=20)
        for N, b, c, N_sq, diff in rows:
            # c - N^2 = O(N)
            assert abs(diff) < 2 * N

    def test_c_monotonic(self):
        rows = assembly_map_table(N_max=20)
        for i in range(len(rows) - 1):
            assert rows[i + 1][2] > rows[i][2]


class TestSelberg:
    def test_large_N_negligible(self):
        """Selberg correction negligible for N >= 8."""
        for N in range(8, 15):
            l_0, Z_sel = selberg_contribution(N)
            assert Z_sel > 0.99

    def test_N5_correction(self):
        """N=5 has a measurable Selberg correction."""
        l_0, Z_sel = selberg_contribution(5)
        assert Z_sel < 0.95  # ~0.85


class TestLegendre:
    def test_qr_five(self):
        """5 is a QR mod primes p = 1 mod 5."""
        assert legendre_symbol(5, 11) == 1  # 11 = 1 mod 5
        assert legendre_symbol(5, 3) == -1

    def test_visibility(self):
        vis, invis = visibility_pattern(5, 50)
        assert len(vis) > 0
        assert len(invis) > 0


class TestFullAnalysis:
    def test_runs(self):
        results = full_analysis(N_max=12)
        assert results['Z_total'] > 1.0
        assert len(results['terms']) == 10  # N=3..12
        assert 'Q' in results['field_fractions']
        assert results['field_fractions']['Q'] > 0.9

    def test_convergence_table(self):
        results = full_analysis(N_max=12)
        for N, cum in results['convergence']:
            assert 0 < cum <= 1.0001
        # Last entry should be ~1
        assert results['convergence'][-1][1] > 0.999
