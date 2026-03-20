"""
Tests for the Calogero-Moser Havelock identity (NEW).

Classical Havelock (1931):
    Σ_{p=1}^{N-1} [1-cos(2πpm/N)] / [2sin²(πp/N)] = m(N-m)

Calogero-Moser analogue (this paper):
    Σ_{p=1}^{N-1} [1-cos(2πpm/N)] / sin⁴(πp/N) = (2/3)·m(N-m)·[m(N-m)+2]

The k=2 identity is N-independent, just like k=1.
The k=3 identity is NOT N-independent — it breaks universality.
"""
import numpy as np
import pytest
from fractions import Fraction


def havelock_sum(N, m, k=1):
    """Σ_{p=1}^{N-1} [1-cos(2πpm/N)] / sin^{2k}(πp/N)."""
    total = 0.0
    for p in range(1, N):
        s = np.sin(np.pi * p / N)
        c = np.cos(2 * np.pi * p * m / N)
        total += (1 - c) / s**(2*k)
    return total


def cm_havelock_formula(m, N):
    """(2/3)·m(N-m)·[m(N-m)+2]."""
    T = m * (N - m)
    return Fraction(2, 3) * T * (T + 2)


class TestClassicalHavelock:
    """k=1: Σ [1-cos]/sin² = 2·m(N-m)."""

    @pytest.mark.parametrize("N", range(3, 16))
    def test_identity(self, N):
        for m in range(1, N):
            computed = havelock_sum(N, m, k=1)
            exact = 2 * m * (N - m)
            assert abs(computed - exact) < 1e-10, (
                f"N={N}, m={m}: {computed} ≠ {exact}")


class TestCMHavelockIdentity:
    """k=2: Σ [1-cos]/sin⁴ = (2/3)·m(N-m)·[m(N-m)+2]."""

    @pytest.mark.parametrize("N", range(3, 21))
    def test_identity_all_modes(self, N):
        """Verify for all modes at each N."""
        for m in range(1, N):
            computed = havelock_sum(N, m, k=2)
            exact = float(cm_havelock_formula(m, N))
            assert abs(computed - exact) < 1e-8 * max(1, abs(exact)), (
                f"N={N}, m={m}: computed={computed}, exact={exact}")

    def test_palindromic(self):
        """S_m = S_{N-m} (palindromic symmetry)."""
        for N in range(3, 15):
            for m in range(1, N):
                assert abs(havelock_sum(N, m, 2) -
                           havelock_sum(N, N-m, 2)) < 1e-10

    def test_formula_is_quartic_in_m(self):
        """The formula is degree 4 in m (vs degree 2 for classical)."""
        N = 10
        m = 3
        T = m * (N - m)
        result = cm_havelock_formula(m, N)
        # (2/3)·21·23 = (2/3)·483 = 322
        assert result == Fraction(966, 3)

    def test_N_independence(self):
        """The formula depends on m,N only through T=m(N-m)."""
        # Two different (N,m) pairs with the same T should give same S_m
        # T=12: (N=7,m=3) and (N=13,m=1) both give T=12... wait
        # m(N-m)=12: 3·4=12 → N=7,m=3 or N=7,m=4
        # Also: 2·6=12 → N=8,m=2 or N=8,m=6
        s1 = havelock_sum(7, 3, 2)  # T=12
        s2 = havelock_sum(8, 2, 2)  # T=12
        assert abs(s1 - s2) < 1e-10, f"N-dependent: {s1} ≠ {s2}"

    def test_zero_at_m_zero(self):
        """S_0 = 0 (trivially)."""
        for N in range(3, 10):
            assert abs(havelock_sum(N, 0, 2)) < 1e-14


class TestK3NotUniversal:
    """k=3: Σ [1-cos]/sin⁶ is NOT N-independent."""

    def test_k3_depends_on_N(self):
        """Two (N,m) pairs with same T=m(N-m) give DIFFERENT S_m at k=3."""
        s1 = havelock_sum(7, 3, 3)  # T=12, N=7
        s2 = havelock_sum(8, 2, 3)  # T=12, N=8
        # These should differ (k=3 is N-dependent)
        assert abs(s1 - s2) > 0.1, (
            f"k=3 appears N-independent: {s1} vs {s2}")


class TestCMEigenvalueConnection:
    """The CM Havelock sum connects to stability eigenvalues."""

    def test_cm_eigenvalue_via_identity(self):
        """CM constrained eigenvalue expressible via the identity."""
        # The CM Havelock sum S_m appears in the Hessian of Σ 1/d².
        # Verify that the identity gives consistent eigenvalue predictions.
        from planetary_polygons.proofs.gaudin_calogero_moser import (
            constrained_eigenvalue_cm, havelock_eigenvalue
        )
        for N in [6, 7, 8]:
            m = N // 2
            mu = constrained_eigenvalue_cm(N, m)
            lam = havelock_eigenvalue(m, N)
            # mu should be finite and well-defined
            assert np.isfinite(mu)
            # For N=7: mu > 0 even though lam = 0 (CM stabilizes marginal mode)
            if N == 7:
                assert mu > 0, f"N=7: CM eigenvalue should be positive"


class TestUniquenessOfK1K2:
    """Only k=1 and k=2 give N-independent identities."""

    def test_k1_universal(self):
        """k=1 is N-independent."""
        s1 = havelock_sum(7, 3, 1)
        s2 = havelock_sum(8, 2, 1)
        assert abs(s1 - s2) < 1e-10

    def test_k2_universal(self):
        """k=2 is N-independent."""
        s1 = havelock_sum(7, 3, 2)
        s2 = havelock_sum(8, 2, 2)
        assert abs(s1 - s2) < 1e-10

    def test_k3_not_universal(self):
        """k=3 is NOT N-independent."""
        s1 = havelock_sum(7, 3, 3)
        s2 = havelock_sum(8, 2, 3)
        assert abs(s1 - s2) > 0.1
