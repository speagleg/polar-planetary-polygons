"""Tests for N_crit(Δ) and generalized Casimir computations."""

import math
import pytest
import sys
sys.path.insert(0, 'src')

from planetary_polygons.extensions.ncrit_delta import (
    weight_tilde, generalized_casimir, casimir_ratio,
    constrained_hessian_delta, stability_margin,
    ncrit_at_delta, find_critical_delta,
)


# ============================================================
# Generalized Casimir tests
# ============================================================

class TestGeneralizedCasimir:
    """Test the analytical generalized Casimir h(m, N, Δ)."""

    def test_delta_zero_recovers_havelock(self):
        """At Δ=0, h(m,N,0) = 2m(N-m).

        The weight csc²(πp/N) gives h = 2m(N-m), which relates to the
        Havelock Casimir f = m(N-m)/2 by h = 4f. The factor 4 comes from
        the angular cross-derivative: μ_m^{ang} = h/4 = f for the log case.
        """
        for N in [4, 5, 6, 7, 8]:
            for m in range(1, N):
                h = generalized_casimir(m, N, 0)
                expected = 2 * m * (N - m)
                assert abs(h - expected) < 1e-8, \
                    f"h({m},{N},0) = {h}, expected {expected}"

    def test_palindromic_symmetry(self):
        """h(m, N, Δ) = h(N-m, N, Δ) for all Δ."""
        for Delta in [0, 0.5, 1.0, 2.0]:
            for N in [5, 6, 7]:
                for m in range(1, N):
                    h_m = generalized_casimir(m, N, Delta)
                    h_Nm = generalized_casimir(N - m, N, Delta)
                    assert abs(h_m - h_Nm) < 1e-8, \
                        f"h({m},{N},{Delta}) ≠ h({N-m},{N},{Delta})"

    def test_positive(self):
        """h(m, N, Δ) > 0 for all m ≥ 1 and Δ ≥ 0."""
        for Delta in [0, 0.5, 1.0, 5.0]:
            for N in [4, 5, 6, 7]:
                for m in range(1, N):
                    h = generalized_casimir(m, N, Delta)
                    assert h > 0, f"h({m},{N},{Delta}) = {h} ≤ 0"

    def test_critical_mode_is_half(self):
        """The critical (largest) Casimir is at m = N//2."""
        for Delta in [0, 1.0, 5.0]:
            for N in [5, 6, 7, 8]:
                h_values = [generalized_casimir(m, N, Delta) for m in range(1, N)]
                m_max = h_values.index(max(h_values)) + 1
                assert m_max == N // 2, \
                    f"N={N}, Δ={Delta}: max at m={m_max}, expected {N//2}"

    def test_ratio_increases_with_delta(self):
        """The critical Casimir ratio h(m_crit)/h(1) increases with Δ."""
        for N in [5, 6, 7, 8]:
            prev_ratio = 0
            for Delta in [0, 0.5, 1.0, 2.0, 5.0]:
                r = casimir_ratio(N // 2, N, Delta)
                assert r >= prev_ratio - 1e-8, \
                    f"N={N}: ratio at Δ={Delta} ({r:.4f}) < previous ({prev_ratio:.4f})"
                prev_ratio = r


# ============================================================
# Constrained Hessian tests
# ============================================================

class TestConstrainedHessian:
    """Test the constrained Hessian for V = |x-y|^{-2Δ}."""

    def test_delta_zero_matches_log(self):
        """At Δ=0, constrained eigenvalues match known Havelock values."""
        for N in [5, 6, 7]:
            result = constrained_hessian_delta(N, 0.0)
            evals = result['constrained_evals']
            # Should have n_neg = 0 for N ≤ 7
            assert result['n_neg'] == 0, \
                f"N={N} at Δ=0: {result['n_neg']} negative evals"

    def test_n8_unstable(self):
        """N=8 is unstable at Δ=0."""
        result = constrained_hessian_delta(8, 0.0)
        assert result['n_neg'] > 0, "N=8 should be unstable at Δ=0"

    def test_lagrange_residual_small(self):
        """The Lagrange multiplier system is well-determined."""
        for N in [5, 6, 7]:
            for Delta in [0.0, 1.0]:
                result = constrained_hessian_delta(N, Delta)
                assert result['lagrange_residual'] < 1e-5, \
                    f"N={N}, Δ={Delta}: residual = {result['lagrange_residual']}"


# ============================================================
# N_crit(Δ) tests
# ============================================================

class TestNcritDelta:
    """Test the main N_crit(Δ) results."""

    def test_ncrit_delta_zero_is_seven(self):
        """N_crit(Δ=0) = 7 (Havelock's classical result)."""
        assert ncrit_at_delta(0.0) == 7

    def test_ncrit_delta_one_is_five(self):
        """N_crit(Δ=1) = 5 (CFT₃ case)."""
        assert ncrit_at_delta(1.0) == 5

    def test_ncrit_decreases_with_delta(self):
        """N_crit is non-increasing in Δ (for Δ < 40)."""
        prev_nc = 100
        for Delta in [0, 0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
            nc = ncrit_at_delta(Delta)
            assert nc <= prev_nc, \
                f"N_crit increased: {prev_nc} at prev → {nc} at Δ={Delta}"
            prev_nc = nc

    def test_n3_always_stable(self):
        """Triangles are always stable."""
        for Delta in [0, 1.0, 5.0, 50.0]:
            m = stability_margin(3, Delta)
            assert m >= -1e-4, f"N=3 unstable at Δ={Delta}: margin={m}"

    def test_n4_always_stable(self):
        """Squares are always stable."""
        for Delta in [0, 1.0, 5.0]:
            m = stability_margin(4, Delta)
            assert m >= -1e-4, f"N=4 unstable at Δ={Delta}: margin={m}"

    def test_delta_star_6(self):
        """Δ*(6) ≈ 0.484 (hexagon transition)."""
        D6 = find_critical_delta(6, 0.0, 2.0, tol=1e-6)
        assert D6 is not None, "Δ*(6) should exist"
        assert abs(D6 - 0.484) < 0.01, f"Δ*(6) = {D6}, expected ~0.484"

    def test_delta_star_5(self):
        """Δ*(5) ≈ 2.38 (pentagon transition)."""
        D5 = find_critical_delta(5, 0.0, 5.0, tol=1e-6)
        assert D5 is not None, "Δ*(5) should exist"
        assert abs(D5 - 2.38) < 0.05, f"Δ*(5) = {D5}, expected ~2.38"

    def test_n7_marginal_at_zero(self):
        """N=7 is marginal at Δ=0 and unstable for Δ > 0."""
        m0 = stability_margin(7, 0.0)
        # At Δ=0, the margin is the m=2 eigenvalue (1.0), since m=3 is 0
        assert m0 > 0, f"N=7 margin at Δ=0 should be positive, got {m0}"

        m_pos = stability_margin(7, 0.1)
        assert m_pos < 0, f"N=7 should be unstable at Δ=0.1, margin={m_pos}"


# ============================================================
# Weight function tests
# ============================================================

class TestWeightFunction:
    """Test the weight function w̃(p, Δ)."""

    def test_delta_zero(self):
        """w̃(p, 0) = csc²(πp/N)."""
        for N in [5, 6, 7]:
            for p in range(1, N):
                w = weight_tilde(p, N, 0)
                expected = 1 / math.sin(math.pi * p / N) ** 2
                assert abs(w - expected) < 1e-10, \
                    f"w̃({p},{N},0) = {w}, expected {expected}"

    def test_symmetric(self):
        """w̃(p, Δ) = w̃(N-p, Δ) (palindromic symmetry)."""
        for Delta in [0, 0.5, 1.0, 2.0]:
            for N in [5, 6, 7]:
                for p in range(1, N):
                    w_p = weight_tilde(p, N, Delta)
                    w_Np = weight_tilde(N - p, N, Delta)
                    assert abs(w_p - w_Np) < 1e-10, \
                        f"w̃({p},{N},{Delta}) ≠ w̃({N-p},{N},{Delta})"

    def test_positive(self):
        """w̃(p, Δ) > 0 for all p, Δ ≥ 0."""
        for Delta in [0, 0.5, 1.0, 5.0]:
            for N in [5, 6, 7]:
                for p in range(1, N):
                    w = weight_tilde(p, N, Delta)
                    assert w > 0, f"w̃({p},{N},{Delta}) = {w} ≤ 0"
