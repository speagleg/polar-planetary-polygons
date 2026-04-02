"""
Tests for dimensional uniqueness: polynomial eigenvalues only in d=2.
"""

import pytest
import numpy as np
from math import pi, log
from fractions import Fraction

from planetary_polygons.extensions.dimensional_uniqueness import (
    hessian_kernel, havelock_eigenvalue_dim, eigenvalue_spectrum,
    ramanujan_csc2_sum, verify_ramanujan_identity,
    csc_power_sum, polynomial_fit_residual,
    exact_havelock_polynomial, havelock_exact,
    dimensional_comparison, full_dimension_table,
    holomorphicity_check, dimension_count,
)


class TestRamanujanIdentity:
    """The csc² sum identity: Σ [1-cos(2πpm/N)]/sin²(πp/N) = 2m(N-m)."""

    @pytest.mark.parametrize("N", [5, 7, 8, 10, 12, 15])
    def test_identity_holds(self, N):
        """Ramanujan identity verified to machine precision."""
        _, max_err = verify_ramanujan_identity(N)
        assert max_err < 1e-10, (
            f"N={N}: Ramanujan identity error {max_err:.2e}"
        )

    @pytest.mark.parametrize("N,m", [(7, 1), (7, 3), (10, 5), (12, 4)])
    def test_specific_values(self, N, m):
        """Spot-check specific (N, m) pairs."""
        num, exact, err = ramanujan_csc2_sum(m, N)
        assert err < 1e-10, f"N={N}, m={m}: sum={num:.6f}, exact={exact}"


class TestD2Polynomial:
    """d=2 eigenvalues are exactly λ_m = (N-1) - m(N-m)/2."""

    @pytest.mark.parametrize("N", [5, 7, 8, 10, 12, 15])
    def test_matches_exact_formula(self, N):
        """λ_m^{(d=2)} matches (N-1) - m(N-m)/2 to machine precision."""
        max_dev = 0.0
        for m in range(1, N):
            lam_num = havelock_eigenvalue_dim(m, N, d=2)
            lam_exact = exact_havelock_polynomial(m, N)
            dev = abs(lam_num - lam_exact)
            max_dev = max(max_dev, dev)
        assert max_dev < 1e-10, (
            f"N={N}: max deviation {max_dev:.2e} from polynomial"
        )

    @pytest.mark.parametrize("N", [5, 7, 8, 10])
    def test_polynomial_fit_exact(self, N):
        """Degree-2 polynomial fit has zero residual for d=2."""
        result = polynomial_fit_residual(N, d=2, degree=2)
        assert result['is_polynomial'], (
            f"N={N}: residual {result['max_residual']:.2e}"
        )

    @pytest.mark.parametrize("N", [5, 7, 8])
    def test_exact_rational(self, N):
        """Eigenvalues are exactly rational (Fraction arithmetic)."""
        for m in range(1, N):
            lam = havelock_exact(m, N)
            assert isinstance(lam, Fraction)
            lam_float = exact_havelock_polynomial(m, N)
            assert abs(float(lam) - lam_float) < 1e-14


class TestD3NotPolynomial:
    """d=3 eigenvalues are NOT polynomial in m."""

    @pytest.mark.parametrize("N", [7, 8, 10, 12])
    def test_d3_not_polynomial_deg2(self, N):
        """Degree-2 fit has significant residual for d=3."""
        result = polynomial_fit_residual(N, d=3, degree=2)
        assert not result['is_polynomial'], (
            f"N={N}: d=3 should NOT be polynomial "
            f"(residual={result['max_residual']:.2e})"
        )

    @pytest.mark.parametrize("N", [7, 10])
    def test_d3_residual_much_larger_than_d2(self, N):
        """d=3 residual >> d=2 residual."""
        r2 = polynomial_fit_residual(N, d=2, degree=2)['max_residual']
        r3 = polynomial_fit_residual(N, d=3, degree=2)['max_residual']
        assert r3 > 1e6 * r2 or (r2 < 1e-10 and r3 > 0.01), (
            f"N={N}: d=3 residual ({r3:.2e}) should be >> d=2 ({r2:.2e})"
        )


class TestD4NotPolynomial:
    """d=4 eigenvalues are NOT polynomial in m."""

    @pytest.mark.parametrize("N", [7, 10])
    def test_d4_not_polynomial(self, N):
        result = polynomial_fit_residual(N, d=4, degree=2)
        assert not result['is_polynomial'], (
            f"N={N}: d=4 should NOT be polynomial"
        )


class TestCscPowerSums:
    """csc^α sums: polynomial for α=2, non-polynomial for α≠2."""

    @pytest.mark.parametrize("N", [7, 10])
    def test_alpha2_polynomial(self, N):
        """α=2: Σ [1-cos]/sin² = 2m(N-m) (polynomial)."""
        for m in range(1, N):
            num = csc_power_sum(m, N, alpha=2)
            exact = 2 * m * (N - m)
            assert abs(num - exact) < 1e-8, (
                f"N={N}, m={m}: sum={num:.4f}, expected {exact}"
            )

    @pytest.mark.parametrize("N", [7, 10])
    def test_alpha3_not_polynomial(self, N):
        """α=3: Σ [1-cos]/sin³ is NOT polynomial in m."""
        m_vals = list(range(1, N))
        sums = [csc_power_sum(m, N, alpha=3) for m in m_vals]
        # Check second differences are NOT constant
        if len(sums) >= 3:
            diffs2 = [sums[i] - 2 * sums[i + 1] + sums[i + 2]
                      for i in range(len(sums) - 2)]
            variance = np.var(diffs2)
            assert variance > 0.01, (
                f"N={N}: α=3 second differences too constant "
                f"(var={variance:.2e})"
            )


class TestDimensionalComparison:
    """Cross-dimensional comparison: only d=2 is polynomial."""

    @pytest.mark.parametrize("N", [7, 10])
    def test_only_d2_polynomial(self, N):
        """Among d=2,3,4: only d=2 gives polynomial eigenvalues."""
        results = dimensional_comparison(N)
        assert results[2]['is_polynomial'], f"N={N}: d=2 should be polynomial"
        assert not results[3]['is_polynomial'], f"N={N}: d=3 should NOT be"
        assert not results[4]['is_polynomial'], f"N={N}: d=4 should NOT be"

    def test_residual_gap(self):
        """d=2 residual ~ 0; d=3,4 residuals >> 0."""
        results = dimensional_comparison(10)
        r2 = results[2]['max_residual']
        r3 = results[3]['max_residual']
        r4 = results[4]['max_residual']
        assert r2 < 1e-8, f"d=2 residual: {r2:.2e}"
        assert r3 > 0.01, f"d=3 residual: {r3:.2e}"
        assert r4 > 0.01, f"d=4 residual: {r4:.2e}"


class TestHolomorphicity:
    def test_d2_holomorphic(self):
        assert holomorphicity_check()['d2']['holomorphic'] is True

    def test_d3_not_holomorphic(self):
        assert holomorphicity_check()['d3']['holomorphic'] is False


class TestDimensionCount:
    def test_total(self):
        result = dimension_count()
        assert result['total_spacetime'] == 4
        assert result['base_dim'] + result['fiber_dim'] + result['time_dim'] == 4
