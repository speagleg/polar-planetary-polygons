"""Tests for Onsager contraction, Sobolev bounds, non-crossing, and τ_bath.

Covers Paper III claims:
- Onsager contraction factor 0.041 at N=7 (line 726)
- Sobolev constant C_S = 0.45 on Bolza surface (lines 712-713)
- Heat-kernel coefficients 0.306, 0.096 (line 713)
- Non-crossing bound R_max = (N²-2)/(4N²) < 1/4 (lines 2498-2506)
- Bath correlation time τ_bath ≤ √2 (lines 3279-3284)
"""
import math
from planetary_polygons.extensions.onsager_selection import (
    bolza_sobolev_bound,
    onsager_contraction,
    non_crossing_bound,
    bath_correlation_time,
    BOLZA_LAMBDA1,
)


# ── Sobolev constant on Bolza ────────────────────────────────────────


class TestBolzaSobolev:
    def test_heat_kernel_coefficient_1(self):
        """λ₁/(4π) ≈ 0.306"""
        coeff1 = BOLZA_LAMBDA1 / (4 * math.pi)
        assert abs(coeff1 - 0.306) < 0.001

    def test_heat_kernel_coefficient_2(self):
        """1/(e·λ₁) ≈ 0.096"""
        coeff2 = 1.0 / (math.e * BOLZA_LAMBDA1)
        assert abs(coeff2 - 0.096) < 0.001

    def test_sup_bound(self):
        """||R - R₀||∞ ≤ 0.90 within basin Var(R)≤2, ||∇R||²≤2"""
        sup_bound, _, _ = bolza_sobolev_bound(var_R=2.0, grad_R_sq=2.0)
        assert abs(sup_bound - 0.90) < 0.01

    def test_sobolev_constant(self):
        """C_S = 0.45"""
        _, C_S, _ = bolza_sobolev_bound(var_R=2.0, grad_R_sq=2.0)
        assert abs(C_S - 0.45) < 0.01

    def test_hoeffding_parameter(self):
        """σ² ≤ 0.80"""
        _, _, sigma_sq = bolza_sobolev_bound(var_R=2.0, grad_R_sq=2.0)
        assert abs(sigma_sq - 0.80) < 0.02

    def test_sup_bound_inside_concavity_domain(self):
        """||R - R₀||∞ < |R₀| = 1 ensures concavity domain not exited"""
        sup_bound, _, _ = bolza_sobolev_bound(var_R=2.0, grad_R_sq=2.0)
        assert sup_bound < 1.0


# ── Onsager contraction factor ───────────────────────────────────────


class TestOnsagerContraction:
    def test_contraction_N7(self):
        """Paper III line 726: contraction = 0.041 at N=7"""
        c = onsager_contraction(7)
        assert abs(c - 0.041) < 0.002

    def test_contraction_N8_tighter(self):
        """N=8 contraction tighter than N=7"""
        c7 = onsager_contraction(7)
        c8 = onsager_contraction(8)
        assert c8 < c7

    def test_contraction_N11(self):
        """N=11 contraction tighter still"""
        c8 = onsager_contraction(8)
        c11 = onsager_contraction(11)
        assert c11 < c8

    def test_contraction_less_than_one(self):
        """Contraction < 1 for all N = 7..20"""
        for N in range(7, 21):
            assert onsager_contraction(N) < 1.0, f"N={N}: contraction >= 1"

    def test_contraction_dominated_by_f_mstar(self):
        """Contraction scales as 1/f(m*,N)² — the dominant factor"""
        for N in range(7, 16):
            m_star = N // 2
            f_mstar = m_star * (N - m_star) / 2
            c = onsager_contraction(N)
            # Contraction is bounded by (1/f)^2 × 2 (generous nonlinear bound)
            assert c < 2 / f_mstar**2, f"N={N}: contraction exceeds bound"


# ── Non-crossing bound ───────────────────────────────────────────────


class TestNonCrossingBound:
    def test_below_quarter_all_N(self):
        """R_max < 1/4 for all N ≥ 3"""
        for N in range(3, 100):
            assert non_crossing_bound(N) < 0.25, f"N={N}: R_max >= 1/4"

    def test_approaches_quarter(self):
        """R_max → 1/4 as N → ∞"""
        assert non_crossing_bound(1000) > 0.2499

    def test_N7_exact(self):
        """R_max(7) = (49-2)/196 = 47/196"""
        assert abs(non_crossing_bound(7) - 47 / 196) < 1e-12

    def test_N3_exact(self):
        """R_max(3) = (9-2)/36 = 7/36"""
        assert abs(non_crossing_bound(3) - 7 / 36) < 1e-12


# ── Bath correlation time ────────────────────────────────────────────


class TestBathCorrelationTime:
    def test_tau_bath_N7(self):
        """N=7 (odd): λ_min = 1, τ = 1"""
        lam, tau = bath_correlation_time(7)
        assert abs(lam - 1.0) < 1e-12
        assert abs(tau - 1.0) < 1e-12

    def test_tau_bath_N8(self):
        """N=8 (even): λ_min = 1/2, τ = √2"""
        lam, tau = bath_correlation_time(8)
        assert abs(lam - 0.5) < 1e-12
        assert abs(tau - math.sqrt(2)) < 1e-12

    def test_tau_bound_all_N(self):
        """τ_bath ≤ √2 for all N = 7..50"""
        for N in range(7, 51):
            _, tau = bath_correlation_time(N)
            assert tau <= math.sqrt(2) + 1e-12, f"N={N}: tau > sqrt(2)"

    def test_odd_even_pattern(self):
        """Odd N → λ=1, even N → λ=1/2"""
        for N in range(7, 30):
            lam, _ = bath_correlation_time(N)
            if N % 2 == 1:
                assert abs(lam - 1.0) < 1e-12, f"N={N} (odd): λ ≠ 1"
            else:
                assert abs(lam - 0.5) < 1e-12, f"N={N} (even): λ ≠ 1/2"

    def test_formula_explicit(self):
        """λ_min = (N - 2⌊N/2⌋ + 1) / 2"""
        for N in range(7, 30):
            m_star = N // 2
            expected = (N - 2 * m_star + 1) / 2
            lam, _ = bath_correlation_time(N)
            assert abs(lam - expected) < 1e-12
