# tests/test_n7_bifurcation.py
from fractions import Fraction
import numpy as np
from planetary_polygons.extensions.n7_bifurcation import (
    quartic_exact_n7,
    unconstrained_quartic,
    constrained_quartic_n7,
    constrained_quartic_exact,
    constraint_correction_n7,
    constraint_correction_exact,
    alpha_0_n7,
    alpha_0_exact,
)


def test_quartic_exact_n7():
    q = quartic_exact_n7()
    assert abs(float(q) - 153/7) < 1e-10, f"Expected 153/7={153/7:.6f}, got {float(q):.6f}"


def test_unconstrained_quartic_z7_symmetry():
    """Both m=3 and m=4 give the same quartic for N=7."""
    q3 = unconstrained_quartic(7, 3)
    q4 = unconstrained_quartic(7, 4)
    assert abs(q3 - q4) < 1e-6, f"Z_7 symmetry broken: q3={q3:.4f}, q4={q4:.4f}"
    assert abs(q3 - 153/7) < 0.5, f"Expected ≈21.86, got {q3:.4f}"


def test_constrained_quartic_n7():
    q = constrained_quartic_n7()
    assert 19.0 < q < 20.5, f"Expected ≈19.47, got {q:.4f}"


def test_constraint_correction_n7():
    c = constraint_correction_n7()
    assert 1.5 < c < 3.5, f"Expected ≈2.39, got {c:.4f}"


def test_alpha_0_n7():
    a = alpha_0_n7()
    assert 3.0 < a < 3.6, f"Expected ≈3.24, got {a:.4f}"


def test_constrained_quartic_exact():
    """Exact constrained quartic is 135/7 via log-scaling identity."""
    q = constrained_quartic_exact()
    assert q == Fraction(135, 7), f"Expected 135/7, got {q}"


def test_constraint_correction_exact():
    """Constraint correction is exactly 18/7 = 153/7 - 135/7."""
    c = constraint_correction_exact()
    assert c == Fraction(18, 7), f"Expected 18/7, got {c}"
    assert quartic_exact_n7() - constrained_quartic_exact() == c


def test_alpha_0_exact():
    """Exact α₀ = 45/14."""
    a = alpha_0_exact()
    assert a == Fraction(45, 14), f"Expected 45/14, got {a}"


def test_richardson_matches_exact():
    """Richardson estimate agrees with exact 135/7 to within 0.005."""
    exact = float(constrained_quartic_exact())
    numerical = constrained_quartic_n7()
    assert abs(numerical - exact) < 0.005, (
        f"Richardson {numerical:.6f} deviates from exact {exact:.6f} "
        f"by {abs(numerical-exact):.6f}"
    )
