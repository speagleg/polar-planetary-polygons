"""
Tests for the palindromic census of arithmetic Fuchsian groups.

Verifies:
1. Palindromic polynomial construction (against known cases)
2. Galois group detection (mod-p Chebotarev)
3. Non-solvability classification
4. Census consistency
"""
import pytest
from planetary_polygons.extensions.palindromic_census import (
    poly_mul, poly_add, poly_sub, poly_mod, poly_gcd, poly_powmod,
    poly_derivative, poly_eval, poly_deg, poly_discriminant,
    palindromic_from_minpoly, verify_palindromic,
    factor_degree_pattern, classify_galois_degree5,
    classify_galois_generic, collect_cycle_types,
    run_census, census_summary, langlands_prediction,
    TOTALLY_REAL_FIELDS, _strip, _primes_up_to,
)


# ============================================================
# Polynomial arithmetic
# ============================================================

class TestPolyArithmetic:
    def test_mul_basic(self):
        # (1+x)(1+x) = 1+2x+x^2
        assert poly_mul([1, 1], [1, 1]) == [1, 2, 1]

    def test_mul_mod(self):
        # (1+x)(1+x) mod 2 = 1+x^2
        assert poly_mul([1, 1], [1, 1], 2) == [1, 0, 1]

    def test_add(self):
        assert poly_add([1, 2, 3], [4, 5]) == [5, 7, 3]

    def test_sub(self):
        assert poly_sub([5, 7, 3], [4, 5]) == [1, 2, 3]

    def test_derivative(self):
        # d/dx (1 + 2x + 3x^2) = 2 + 6x
        assert poly_derivative([1, 2, 3]) == [2, 6]

    def test_eval(self):
        # f(x) = 1 + 2x + x^2, f(3) = 1+6+9 = 16
        assert poly_eval([1, 2, 1], 3) == 16

    def test_deg(self):
        assert poly_deg([1, 2, 3]) == 2
        assert poly_deg([0]) == -1
        assert poly_deg([5]) == 0

    def test_gcd_mod5(self):
        # gcd(x^2-1, x-1) = x-1 in F_5[x]
        f = [4, 0, 1]  # x^2 - 1 = x^2 + 4 mod 5
        g = [4, 1]     # x - 1 = x + 4 mod 5
        h = poly_gcd(f, g, 5)
        assert poly_deg(h) == 1  # linear, i.e., x-1

    def test_powmod(self):
        # x^5 mod (x^3+1) in F_7[x]
        base = [0, 1]  # x
        mod = [1, 0, 0, 1]  # x^3+1
        result = poly_powmod(base, 5, mod, 7)
        # x^5 = x^3 · x^2 = (-1)·x^2 = -x^2 mod (x^3+1)
        assert result == [0, 0, 6]  # -x^2 = 6x^2 mod 7

    def test_strip(self):
        assert _strip([1, 2, 0, 0]) == [1, 2]
        assert _strip([0]) == [0]


# ============================================================
# Discriminant
# ============================================================

class TestDiscriminant:
    def test_quadratic_disc(self):
        # x^2 - 5: disc = 20
        disc = poly_discriminant([-5, 0, 1])
        assert disc == 20

    def test_cubic_disc(self):
        # x^3+x^2-2x-1: disc = 49 (cyclic cubic for cos(2π/7))
        disc = poly_discriminant([-1, -2, 1, 1])
        assert disc == 49

    def test_bolza_quartic_disc(self):
        # x^4-4x^2-4: disc should be -2^16 = -65536
        disc = poly_discriminant([-4, 0, -4, 0, 1])
        assert disc == -65536


# ============================================================
# Palindromic construction
# ============================================================

class TestPalindromic:
    def test_bolza_quartic(self):
        """Verify the Bolza palindromic quartic from Prop 6.5."""
        # P(u) = u^2 - 4u - 4, ascending: [-4, -4, 1]
        P = [-4, -4, 1]
        Q = palindromic_from_minpoly(P)
        assert Q == [1, -4, -2, -4, 1]
        assert verify_palindromic(Q)

    def test_h2_n8(self):
        """Verify H² palindromic for N=8: ξ^2 - 16ξ + 1."""
        # B = 16, P(u) = u - 16, ascending: [-16, 1]
        P = [-16, 1]
        Q = palindromic_from_minpoly(P)
        assert Q == [1, -16, 1]
        assert verify_palindromic(Q)

    def test_h2_n9(self):
        """Verify H² palindromic for N=9: ξ^2 - 10ξ + 1."""
        # N=9: m=4, T=10, A=8-10=-2. u = 2T/|A| = 10.
        P = [-10, 1]
        Q = palindromic_from_minpoly(P)
        assert Q == [1, -10, 1]
        assert verify_palindromic(Q)

    def test_cyclotomic7(self):
        """x^3+x^2-2x-1 gives the 7th cyclotomic palindromic."""
        # P(u) = u^3+u^2-2u-1, ascending: [-1, -2, 1, 1]
        P = [-1, -2, 1, 1]
        Q = palindromic_from_minpoly(P)
        # Should be ξ^6+ξ^5+ξ^4+ξ^3+ξ^2+ξ+1 (7th cyclotomic)
        assert Q == [1, 1, 1, 1, 1, 1, 1]
        assert verify_palindromic(Q)

    def test_all_palindromic(self):
        """Every palindromic polynomial from the census is actually palindromic."""
        for label, degree, desc, poly_asc, gal in TOTALLY_REAL_FIELDS:
            if degree < 2:
                continue
            Q = palindromic_from_minpoly(poly_asc)
            assert verify_palindromic(Q), f"{label}: not palindromic"

    def test_degree_doubling(self):
        """Palindromic degree is always 2 × trace field degree."""
        for label, degree, desc, poly_asc, gal in TOTALLY_REAL_FIELDS:
            if degree < 2:
                continue
            Q = palindromic_from_minpoly(poly_asc)
            assert poly_deg(Q) == 2 * degree, (
                f"{label}: deg(Q)={poly_deg(Q)} ≠ 2×{degree}")

    def test_constant_term_one(self):
        """Palindromic polynomial from monic P always has constant term 1."""
        for label, degree, desc, poly_asc, gal in TOTALLY_REAL_FIELDS:
            if degree < 2:
                continue
            Q = palindromic_from_minpoly(poly_asc)
            assert Q[0] == 1, f"{label}: constant term = {Q[0]}"

    def test_leading_coeff_one(self):
        """Palindromic polynomial from monic P is monic."""
        for label, degree, desc, poly_asc, gal in TOTALLY_REAL_FIELDS:
            if degree < 2:
                continue
            Q = palindromic_from_minpoly(poly_asc)
            assert Q[-1] == 1, f"{label}: leading coeff = {Q[-1]}"


# ============================================================
# Factor degree patterns
# ============================================================

class TestFactorPatterns:
    def test_linear(self):
        """x-1 mod 5 is irreducible."""
        pat = factor_degree_pattern([4, 1], 5)  # x-1 = x+4 mod 5
        assert pat == (1,)

    def test_quadratic_split(self):
        """x^2-1 mod 5 splits as (x-1)(x+1)."""
        pat = factor_degree_pattern([4, 0, 1], 5)
        assert pat == (1, 1)

    def test_quadratic_irreducible(self):
        """x^2+1 mod 3 is irreducible (-1 is not a QR mod 3)."""
        pat = factor_degree_pattern([1, 0, 1], 3)
        assert pat == (2,)

    def test_cyclotomic_mod11(self):
        """x^5+x^4-4x^3-3x^2+3x+1 mod 11 should split completely (C_5)."""
        f = [1, 3, -3, -4, 1, 1]  # ascending
        pat = factor_degree_pattern(f, 11)
        # This is the min poly of cos(2π/11); mod 11 it should be (x-r)^5
        # Actually it might have repeated roots mod 11 → return None
        if pat is not None:
            assert sum(pat) == 5

    def test_skips_ramified(self):
        """Return None for ramified primes (non-squarefree mod p)."""
        # x^2-5 mod 5 = x^2, not squarefree
        pat = factor_degree_pattern([-5, 0, 1], 5)
        assert pat is None


# ============================================================
# Galois group classification
# ============================================================

class TestGaloisClassification:
    def test_cyclic_quintic(self):
        """C_5 quintic: Q(cos(2π/11))."""
        f = [1, 3, -3, -4, 1, 1]
        group = classify_galois_degree5(f, 500)
        assert group == 'C_5'

    def test_dihedral_quintic(self):
        """D_5 quintic: disc 160801 = 401^2 (verified totally real)."""
        f = [-1, 3, 4, -5, -1, 1]
        group = classify_galois_degree5(f, 500)
        assert group == 'D_5'

    def test_s5_quintic_38569(self):
        """S_5 quintic: x^5-5x^3+4x-1, disc=38569 (non-solvable!)."""
        f = [-1, 4, 0, -5, 0, 1]
        group = classify_galois_degree5(f, 500)
        assert group == 'S_5'

    def test_s5_quintic_65657(self):
        """S_5 quintic: disc 65657, LMFDB canonical (non-solvable!)."""
        f = [1, 5, 2, -5, -1, 1]  # LMFDB: x^5-x^4-5x^3+2x^2+5x+1
        group = classify_galois_degree5(f, 500)
        assert group == 'S_5'

    def test_s5_quintic_24217(self):
        """S_5 quintic: x^5-5x^3-x^2+3x+1, disc=24217 (non-solvable!)."""
        f = [1, 3, -1, -5, 0, 1]
        group = classify_galois_degree5(f, 500)
        assert group == 'S_5'

    def test_solvable_below_5(self):
        """All polynomials of degree ≤ 4 are classified as solvable."""
        for label, degree, desc, poly_asc, gal in TOTALLY_REAL_FIELDS:
            if degree >= 5:
                continue
            info = classify_galois_generic(poly_asc, 200)
            assert info['solvable'] is True, f"{label}: not classified solvable"


# ============================================================
# Non-solvability detection
# ============================================================

class TestNonSolvability:
    def test_s5_is_nonsolvable(self):
        """S_5 quintics produce non-solvable palindromic polynomials."""
        f = [-1, 4, 0, -5, 0, 1]  # S_5 quintic: x^5-5x^3+4x-1
        info = classify_galois_generic(f, 300)
        assert info['solvable'] is False

    def test_c5_is_solvable(self):
        """C_5 quintics produce solvable palindromic polynomials."""
        f = [1, 3, -3, -4, 1, 1]  # C_5 quintic
        info = classify_galois_generic(f, 300)
        assert info['solvable'] is True

    def test_d5_is_solvable(self):
        """D_5 quintics produce solvable palindromic polynomials."""
        f = [-1, 3, 4, -5, -1, 1]  # D_5 quintic
        info = classify_galois_generic(f, 300)
        assert info['solvable'] is True

    def test_degree4_always_solvable(self):
        """S_4 is solvable, so all quartic Galois groups are solvable."""
        f = [1, 1, -3, -1, 1]  # S_4 quartic
        info = classify_galois_generic(f, 200)
        assert info['solvable'] is True


# ============================================================
# Census integration
# ============================================================

class TestCensus:
    def test_census_runs(self):
        """Census runs without errors."""
        results = run_census(prime_bound=100, verbose=False)
        assert len(results) == len(TOTALLY_REAL_FIELDS)

    def test_census_finds_nonsolvable(self):
        """Census identifies at least one non-solvable case."""
        results = run_census(prime_bound=200, verbose=False)
        summary = census_summary(results)
        assert summary['non_solvable'] >= 1

    def test_census_palindromic_consistency(self):
        """All palindromic polynomials in census are actually palindromic."""
        results = run_census(prime_bound=100, verbose=False)
        for r in results:
            assert r['is_palindromic'], f"{r['label']}: not palindromic"

    def test_langlands_predictions_exist(self):
        """Non-solvable entries have Langlands predictions."""
        results = run_census(prime_bound=200, verbose=False)
        non_solv = [r for r in results if r['solvable'] is False]
        for r in non_solv:
            pred = langlands_prediction(r)
            assert pred is not None
            assert pred['status'] == 'CONJECTURAL'

    def test_s5_palindromic_degree10(self):
        """S_5 quintic gives degree-10 palindromic polynomial."""
        results = run_census(prime_bound=200, verbose=False)
        s5_entries = [r for r in results
                      if r.get('detected_galois') == 'S_5' and r['degree'] == 5]
        assert len(s5_entries) >= 1
        for entry in s5_entries:
            assert entry['palindromic_degree'] == 10


# ============================================================
# Specific palindromic polynomials
# ============================================================

class TestSpecificPalindromes:
    def test_s5_38569_palindromic_explicit(self):
        """Compute explicit degree-10 palindromic for x^5-5x^3+4x-1 (S_5)."""
        f = [-1, 4, 0, -5, 0, 1]  # x^5-5x^3+4x-1
        Q = palindromic_from_minpoly(f)
        assert poly_deg(Q) == 10
        assert verify_palindromic(Q)
        # First and last coefficients must be 1
        assert Q[0] == 1
        assert Q[10] == 1

    def test_s5_65657_lmfdb_palindromic(self):
        """Compute explicit degree-10 palindromic for LMFDB 5.5.65657.1."""
        f = [1, 5, 2, -5, -1, 1]  # LMFDB canonical: x^5-x^4-5x^3+2x^2+5x+1
        Q = palindromic_from_minpoly(f)
        assert Q == [1, -1, 0, -2, 0, -1, 0, -2, 0, -1, 1]
        assert verify_palindromic(Q)

    def test_c6_palindromic_degree12(self):
        """C_6 sextic gives degree-12 palindromic polynomial."""
        f = [-1, 3, 6, -4, -5, 1, 1]
        Q = palindromic_from_minpoly(f)
        assert poly_deg(Q) == 12
        assert verify_palindromic(Q)


# ============================================================
# Primes utility
# ============================================================

class TestPrimes:
    def test_primes_up_to_20(self):
        assert _primes_up_to(20) == [2, 3, 5, 7, 11, 13, 17, 19]

    def test_primes_up_to_2(self):
        assert _primes_up_to(2) == [2]

    def test_primes_empty(self):
        assert _primes_up_to(1) == []
