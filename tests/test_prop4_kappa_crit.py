# tests/test_prop4_kappa_crit.py
import sympy as sp
from planetary_polygons.core.hessian import kappa_crit_sympy


def test_kappa_crit_n6_exact():
    """kappa_crit for N=6 must be exactly -1/4."""
    result = kappa_crit_sympy(6)
    assert result == sp.Rational(-1, 4), f"Expected -1/4, got {result}"


def test_kappa_crit_n6_float():
    result = kappa_crit_sympy(6)
    assert abs(float(result) + 0.25) < 1e-10


def test_kappa_crit_returns_sympy_rational():
    result = kappa_crit_sympy(6)
    assert isinstance(result, sp.Rational), f"Expected sympy Rational, got {type(result)}"
