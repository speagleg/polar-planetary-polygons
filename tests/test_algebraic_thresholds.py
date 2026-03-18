# tests/test_algebraic_thresholds.py
from fractions import Fraction
import math
import numpy as np
from planetary_polygons.extensions.algebraic_thresholds import (
    _squarefree_part,
    h2_threshold_polynomial,
    h2_stability_threshold,
    h2_threshold_table,
    sphere_stability_threshold,
    sphere_threshold_table,
)
from planetary_polygons.extensions.h2_stability import XI_STAR_78, C1_h2_exact


# ── squarefree helper ─────────────────────────────────────────────────────────

def test_squarefree_part_perfect_squares():
    assert _squarefree_part(4) == 1
    assert _squarefree_part(9) == 1
    assert _squarefree_part(576) == 1   # 24², N=10 discriminant


def test_squarefree_part_primes():
    assert _squarefree_part(7) == 7
    assert _squarefree_part(6) == 6
    assert _squarefree_part(11) == 11


def test_squarefree_part_composite():
    assert _squarefree_part(63) == 7    # 9*7
    assert _squarefree_part(252) == 7   # 4*63 = 4*9*7
    assert _squarefree_part(96) == 6    # 16*6


# ── H² threshold polynomial ───────────────────────────────────────────────────

def test_h2_polynomial_n8():
    """N=8: should give −ξ² + 16ξ − 1 = 0, i.e. (A_int, B_int) = (−1, 16)."""
    A, B = h2_threshold_polynomial(8)
    # Polynomial A·ξ² + B·ξ + A = 0 → ξ² − 16ξ + 1 = 0 after dividing by A
    assert A < 0
    assert B > 0
    # Monic: B/|A| = 16
    assert abs(B / abs(A) - 16.0) < 1e-10


def test_h2_polynomial_n9():
    """N=9: ξ² − 10ξ + 1 = 0, ratio B/|A| = 10."""
    A, B = h2_threshold_polynomial(9)
    assert abs(B / abs(A) - 10.0) < 1e-10


def test_h2_polynomial_n10():
    """N=10: 7ξ² − 50ξ + 7 = 0, ratio B/|A| = 50/7."""
    A, B = h2_threshold_polynomial(10)
    assert abs(B / abs(A) - 50.0 / 7.0) < 1e-10


def test_h2_polynomial_roots_satisfy_equation():
    """Both roots of A·ξ² + B·ξ + A = 0 should satisfy the polynomial."""
    for N in range(8, 14):
        A, B = h2_threshold_polynomial(N)
        disc = B * B - 4 * A * A
        assert disc > 0, f"N={N}: non-positive discriminant"
        sqrt_disc = math.sqrt(disc)
        xi1 = (-B + sqrt_disc) / (2 * A)
        xi2 = (-B - sqrt_disc) / (2 * A)
        for xi in [xi1, xi2]:
            residual = A * xi ** 2 + B * xi + A
            assert abs(residual) < 1e-8, f"N={N}: root {xi:.6f} residual={residual:.2e}"


# ── H² stability threshold values ────────────────────────────────────────────

def test_h2_threshold_n7_zero():
    """N=7 is marginally stable at flat limit — ξ* = 0."""
    xi_star, D, field = h2_stability_threshold(7)
    assert xi_star == 0.0
    assert field == 'Q'


def test_h2_threshold_n8_matches_known():
    """ξ*(8) = 8 − 3√7 = XI_STAR_78 (the known 7→8 threshold)."""
    xi_star, D, field = h2_stability_threshold(8)
    assert abs(xi_star - XI_STAR_78) < 1e-12
    assert D == 7
    assert field == 'Q(sqrt(7))'


def test_h2_threshold_n8_satisfies_C1_condition():
    """At ξ* the critical eigenvalue C₁(H², ξ*) = m(N-m)/2 exactly (N=8, m=4)."""
    xi_star, _, _ = h2_stability_threshold(8)
    C1 = C1_h2_exact(8, xi_star)
    T_half = 4 * 4 / 2.0   # m(N-m)/2 = 8
    assert abs(C1 - T_half) < 1e-10, f"C1={C1:.12f} != T_half={T_half}"


def test_h2_threshold_n9_field_Q_sqrt6():
    """9→10 transition lives in Q(√6)."""
    _, D, field = h2_stability_threshold(9)
    assert D == 6
    assert field == 'Q(sqrt(6))'


def test_h2_threshold_n9_satisfies_C1_condition():
    """At ξ*(9), C₁ = m(N-m)/2 = 4·5/2 = 10."""
    xi_star, _, _ = h2_stability_threshold(9)
    C1 = C1_h2_exact(9, xi_star)
    T_half = 4 * 5 / 2.0
    assert abs(C1 - T_half) < 1e-10, f"C1={C1:.10f} != {T_half}"


def test_h2_threshold_n10_rational():
    """N=10: discriminant squarefree=1, so ξ* ∈ Q (field = Q)."""
    xi_star, D, field = h2_stability_threshold(10)
    assert D == 1
    assert field == 'Q'
    assert abs(xi_star - 1.0 / 7.0) < 1e-12


def test_h2_threshold_n10_satisfies_C1_condition():
    """At ξ*(10) = 1/7, C₁ = m(N-m)/2 = 25/2."""
    xi_star, _, _ = h2_stability_threshold(10)
    C1 = C1_h2_exact(10, xi_star)
    T_half = 5 * 5 / 2.0   # = 12.5
    assert abs(C1 - T_half) < 1e-10


def test_h2_threshold_all_satisfy_C1_condition():
    """For N = 8..16, ξ*(N) satisfies C₁(H², ξ*) = floor(N/2)·(N−floor(N/2))/2."""
    for N in range(8, 17):
        xi_star, _, _ = h2_stability_threshold(N)
        assert xi_star > 0, f"N={N}: expected positive ξ*"
        m = N // 2
        T_half = m * (N - m) / 2.0
        C1 = C1_h2_exact(N, xi_star)
        assert abs(C1 - T_half) < 1e-8, f"N={N}: C1={C1:.10f} != T_half={T_half}"


# ── H² threshold table: algebraic field pattern ──────────────────────────────

def test_h2_threshold_table_even_field_pattern():
    """
    Even N: discriminant squarefree = squarefree(N-1).
    Examples: N=8→7, N=10→1(=sq_free(9)), N=12→11, N=14→13, N=16→15.
    """
    expected = {8: 7, 10: 1, 12: 11, 14: 13, 16: 15}
    rows = {r['N']: r for r in h2_threshold_table(16)}
    for N, D_exp in expected.items():
        assert rows[N]['disc_squarefree'] == D_exp, \
            f"N={N}: expected D={D_exp}, got {rows[N]['disc_squarefree']}"


def test_h2_threshold_table_odd_field_pattern():
    """
    Odd N > 7: discriminant squarefree = squarefree(N-3).
    Examples: N=9→6, N=11→2(=sq_free(8)), N=13→10, N=15→3(=sq_free(12)).
    """
    expected = {9: 6, 11: 2, 13: 10, 15: 3}
    rows = {r['N']: r for r in h2_threshold_table(16)}
    for N, D_exp in expected.items():
        assert rows[N]['disc_squarefree'] == D_exp, \
            f"N={N}: expected D={D_exp}, got {rows[N]['disc_squarefree']}"


# ── S² thresholds ─────────────────────────────────────────────────────────────

def test_sphere_threshold_n3():
    xi = sphere_stability_threshold(3)
    assert xi == Fraction(1, 3), f"N=3: expected 1/3, got {xi}"


def test_sphere_threshold_n4():
    xi = sphere_stability_threshold(4)
    assert xi == Fraction(1, 5), f"N=4: expected 1/5, got {xi}"


def test_sphere_threshold_n5():
    xi = sphere_stability_threshold(5)
    assert xi == Fraction(1, 7), f"N=5: expected 1/7, got {xi}"


def test_sphere_threshold_n6():
    xi = sphere_stability_threshold(6)
    assert xi == Fraction(1, 19), f"N=6: expected 1/19, got {xi}"


def test_sphere_threshold_n7_none():
    """N=7 is marginally stable (ξ_crit = 0), curvature immediately destabilizes."""
    assert sphere_stability_threshold(7) is None


def test_sphere_threshold_n8_none():
    """N=8 is unstable even in flat limit (ξ_crit < 0)."""
    assert sphere_stability_threshold(8) is None


def test_sphere_threshold_satisfies_C1_condition():
    """
    For N ≤ 6, at ξ_crit on S², C₁(S², ξ_crit) = m(N-m)/2 exactly.
    C₁(S², ξ) = (N-1)(1-ξ)/(1+ξ).
    """
    from fractions import Fraction as F
    for N in range(3, 7):
        xi = sphere_stability_threshold(N)
        assert xi is not None
        m = N // 2
        T_half = F(m * (N - m), 2)
        C1 = F(N - 1) * (1 - xi) / (1 + xi)
        assert C1 == T_half, f"N={N}: C1={C1} != T_half={T_half}"


def test_sphere_table_only_le6_positive():
    """Only N ≤ 6 have non-None S² thresholds."""
    for row in sphere_threshold_table(12):
        N, xi = row['N'], row['xi_crit']
        if N <= 6:
            assert xi is not None and xi > 0, f"N={N}: expected positive threshold"
        else:
            assert xi is None, f"N={N}: expected None, got {xi}"


def test_sphere_threshold_decreasing_in_N():
    """S² thresholds decrease with N for N = 3, 4, 5, 6."""
    thresholds = [sphere_stability_threshold(N) for N in range(3, 7)]
    for i in range(len(thresholds) - 1):
        assert thresholds[i] > thresholds[i + 1], \
            f"threshold not decreasing: xi({3+i})={thresholds[i]}, xi({4+i})={thresholds[i+1]}"
