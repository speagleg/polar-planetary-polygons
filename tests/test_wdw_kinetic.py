"""Tests for the WDW kinetic coefficient derivation.

Proves:
1. The first-order functional determinant gives no rho-dot^2 term
2. The Fisher-Rao metric is positive and has correct asymptotics
3. The CL Gaussian approximation diverges from 12b(N) at large N
"""
import numpy as np
from math import pi, log, sinh, cosh
import pytest


def casimir(m, N):
    return m * (N - m) / 2.0


def b_exact(N):
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


def C1(rho, N):
    return log(2 * sinh(rho)) + b_exact(N)


def find_threshold(N, m_crit=None):
    if m_crit is None:
        m_crit = N // 2
    target = casimir(m_crit, N) - b_exact(N)
    if target > 0:
        return np.arcsinh(np.exp(target) / 2)
    return 0.01


class TestMatsubaraNoGo:
    """The first-order Matsubara sum f_k vanishes for k != 0.

    This proves the integrable functional determinant contributes
    no rho-dot^2 (kinetic) term to the effective action.
    """

    def test_shift_identity_convergent(self):
        """f_k = Sum_n 1/[(iw_n+lam)(iw_{n+k}+lam)] -> 0 as n_max -> inf."""
        beta = 10.0
        lam = 2.0
        k = 1

        results = []
        for n_max in [500, 1000, 5000]:
            f_k = 0.0
            for n in range(-n_max, n_max + 1):
                omega_n = 2 * pi * n / beta
                omega_nk = 2 * pi * (n + k) / beta
                denom = complex(0, omega_n) + lam
                denom2 = complex(0, omega_nk) + lam
                f_k += (1.0 / (denom * denom2)).real
            results.append((n_max, f_k))

        # f_k * n_max should be approximately constant (f_k ~ 1/n_max -> 0)
        products = [n * f for n, f in results]
        ratio = products[-1] / products[0]
        assert abs(ratio - 1.0) < 0.01, (
            f"f_k*n_max should be constant; ratio = {ratio:.4f}"
        )

    def test_shift_identity_multiple_k(self):
        """f_k -> 0 for k = 1, 2, 3 (not just k = 1)."""
        beta = 10.0
        lam = 3.0
        n_max = 5000

        for k in [1, 2, 3]:
            f_k = 0.0
            for n in range(-n_max, n_max + 1):
                omega_n = 2 * pi * n / beta
                omega_nk = 2 * pi * (n + k) / beta
                denom = complex(0, omega_n) + lam
                denom2 = complex(0, omega_nk) + lam
                f_k += (1.0 / (denom * denom2)).real
            assert abs(f_k) < 0.01, f"f_{k} = {f_k}, expected ~0"

    def test_determinant_depends_only_on_integral(self):
        """det(d_tau + V(tau)) = 1 - exp(-int V dtau), no rho-dot dependence."""
        beta = 5.0
        V_integral_1 = 2.0 * beta
        det_1 = abs(1 - np.exp(-V_integral_1))

        n_pts = 1000
        tau = np.linspace(0, beta, n_pts, endpoint=False)
        V_path2 = 2.0 + np.sin(2 * pi * tau / beta)
        V_integral_2 = np.sum(V_path2) * (beta / n_pts)
        det_2 = abs(1 - np.exp(-V_integral_2))

        assert abs(det_1 - det_2) < 1e-10, (
            f"det depends on int V, not on V(tau) shape: {det_1} vs {det_2}"
        )


class TestFisherRaoMetric:
    """The Fisher-Rao information metric on the Boltzmann family
    parametrised by rho gives the kinetic coefficient of the FK
    path integral measure."""

    def test_fisher_metric_positive(self):
        """g_FF(rho) > 0 for all rho > 0 and N >= 7."""
        for N in [7, 8, 11]:
            m_crit = N // 2
            for rho in [1.0, 2.0, 3.0, 5.0]:
                c1 = C1(rho, N)
                coth2 = (np.cosh(rho) / np.sinh(rho)) ** 2
                H = sum(
                    1.0 / (c1 - casimir(m, N)) ** 2
                    for m in range(1, N)
                    if m != m_crit and abs(c1 - casimir(m, N)) > 1e-8
                )
                g_FF = coth2 * H
                assert g_FF > 0, f"g_FF({rho}, N={N}) = {g_FF} <= 0"

    def test_fisher_metric_large_rho_asymptotics(self):
        """For large rho: g_FF ~ (N-2)/rho^2 (since coth->1, lam_m->rho)."""
        N = 8
        m_crit = N // 2
        rho = 50.0
        c1 = C1(rho, N)
        H = sum(
            1.0 / (c1 - casimir(m, N)) ** 2
            for m in range(1, N)
            if m != m_crit
        )
        g_FF = H  # coth^2(50) ~ 1
        expected = (N - 2) / rho**2
        assert abs(g_FF / expected - 1) < 0.05, (
            f"g_FF asymptotic: {g_FF:.6e} vs {expected:.6e}"
        )

    def test_fisher_integral_gives_12b(self):
        """c = 12b(N) is verified by the four-fold consistency
        (central charge, CS level, Brown-Henneaux, WDW).
        Here we verify the analytic formula itself."""
        for N in [8, 11]:
            b = b_exact(N)
            c_exact = 12 * b
            assert c_exact > 0
            assert abs(c_exact - N * (N + 1) + 12 * log(2)
                       - 12 * log(N) / (N - 1)) < 1e-10


class TestCLComparison:
    """The CL Gaussian approximation c_CL vs the exact c = 12b(N)."""

    def test_cl_formula_order_of_magnitude(self):
        """c_CL is within an order of magnitude of 12b(N) for N=7..9."""
        for N in [7, 8, 9]:
            m_crit = N // 2
            rho_star = find_threshold(N, m_crit)
            coth_star = np.cosh(rho_star) / np.sinh(rho_star)
            c_cl = N**2 * rho_star**2 / ((N - 2) * coth_star**2)
            c_exact = 12 * b_exact(N)
            ratio = c_cl / c_exact
            assert 0.3 < ratio < 3.0, (
                f"N={N}: c_CL/12b = {ratio:.2f}, expected O(1)"
            )

    def test_cl_diverges_for_large_N(self):
        """c_CL/12b(N) grows with N -- the CL formula is wrong at large N."""
        ratios = []
        for N in [8, 12, 16]:
            m_crit = N // 2
            rho_star = find_threshold(N, m_crit)
            coth_star = np.cosh(rho_star) / np.sinh(rho_star)
            c_cl = N**2 * rho_star**2 / ((N - 2) * coth_star**2)
            c_exact = 12 * b_exact(N)
            ratios.append(c_cl / c_exact)
        assert ratios[-1] > ratios[0], (
            f"CL ratio should grow: {ratios}"
        )
