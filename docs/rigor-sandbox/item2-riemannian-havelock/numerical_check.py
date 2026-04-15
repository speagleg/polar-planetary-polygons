"""Numerical + symbolic validator for the Riemannian Havelock universality.

Claim: on S² (and H²), the tangential eigenvalue of the constrained
Hessian at mode m is exactly m(N-m)/(2ξ), independent of the surface
curvature. This is because the tangential projection of ∇²(W - ΩJ)
equals the flat-plane Lagrange shift (N-1)/(2ξ), which is mode-independent.

Key intermediate results verified:
1. ê_t^T ∇²W ê_t = (N-1)/(1+ξ) on S² (mode-independent)
2. ê_t^T ∇²J ê_t = -4/(1+ξ)² on S² (mode-independent)
3. ê_t^T ∇²(W-ΩJ) ê_t = (N-1)/(2ξ) on S² (= flat Lagrange shift)
4. Combined: tangential eigenvalue = m(N-m)/(2ξ) (universal)

Run: python3 docs/rigor-sandbox/item2-riemannian-havelock/numerical_check.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

_REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO / "src"))


# ---------------------------------------------------------------------------
# Reuse H_sph, J, Hessian infrastructure from Item #6
# ---------------------------------------------------------------------------

def H_sph(pos):
    N = len(pos) // 2; x, y = pos[:N], pos[N:]
    H = 0.0
    for j in range(N):
        for k in range(j + 1, N):
            r2 = (x[j] - x[k]) ** 2 + (y[j] - y[k]) ** 2
            if r2 > 1e-30: H -= 0.5 * np.log(r2)
    for k in range(N):
        H += (N - 1) / 2.0 * np.log(1 + x[k] ** 2 + y[k] ** 2)
    return H


def W_confining(pos):
    N = len(pos) // 2; x, y = pos[:N], pos[N:]
    return (N - 1) / 2.0 * np.sum(np.log(1 + x ** 2 + y ** 2))


def J_angular(pos):
    N = len(pos) // 2; x, y = pos[:N], pos[N:]
    return np.sum((1 - x ** 2 - y ** 2) / (1 + x ** 2 + y ** 2))


def num_hess(f, pos, eps=1e-5):
    n = len(pos); H = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            pp = pos.copy(); pp[i] += eps; pp[j] += eps
            pm = pos.copy(); pm[i] += eps; pm[j] -= eps
            mp = pos.copy(); mp[i] -= eps; mp[j] += eps
            mm = pos.copy(); mm[i] -= eps; mm[j] -= eps
            v = (f(pp) - f(pm) - f(mp) + f(mm)) / (4 * eps ** 2)
            H[i, j] = v; H[j, i] = v
    return H


def num_grad(f, pos, eps=1e-7):
    n = len(pos); g = np.zeros(n)
    for i in range(n):
        pp = pos.copy(); pp[i] += eps
        pm = pos.copy(); pm[i] -= eps
        g[i] = (f(pp) - f(pm)) / (2 * eps)
    return g


def tangential_projection(N, xi, m, hessian_matrix):
    """Compute ê_t^T M ê_t for mode-m tangential vector at ring radius √ξ."""
    theta = 2 * np.pi * np.arange(N) / N
    amp = np.cos(2 * np.pi * m * np.arange(N) / N)
    dim = 2 * N
    e_t = np.zeros(dim)
    e_t[:N] = -amp * np.sin(theta)
    e_t[N:] = amp * np.cos(theta)
    e_t /= np.linalg.norm(e_t)
    return float(e_t @ hessian_matrix @ e_t)


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_W_tangential_mode_independent() -> int:
    """ê_t^T ∇²W ê_t = (N-1)/(1+ξ) for all m (mode-independent)."""
    failed = 0
    for N in [5, 6, 7]:
        for xi in [0.2, 0.5]:
            r_E = np.sqrt(xi)
            theta = 2 * np.pi * np.arange(N) / N
            pos = np.concatenate([r_E * np.cos(theta), r_E * np.sin(theta)])
            HW = num_hess(W_confining, pos)
            expected = (N - 1) / (1 + xi)
            for m in range(2, N - 1):
                val = tangential_projection(N, xi, m, HW)
                diff = abs(val - expected)
                if diff > 0.01:
                    failed += 1
                    print(f"  FAIL N={N} xi={xi} m={m}: W_tt={val:.4f} expected={expected:.4f}")
    if failed == 0:
        print("  ê_t^T ∇²W ê_t = (N-1)/(1+ξ) verified (mode-independent)")
    return failed


def check_J_tangential_mode_independent() -> int:
    """ê_t^T ∇²J ê_t = -4/(1+ξ)² for all m (mode-independent)."""
    failed = 0
    for N in [5, 6, 7]:
        for xi in [0.2, 0.5]:
            r_E = np.sqrt(xi)
            theta = 2 * np.pi * np.arange(N) / N
            pos = np.concatenate([r_E * np.cos(theta), r_E * np.sin(theta)])
            HJ = num_hess(J_angular, pos)
            expected = -4 / (1 + xi) ** 2
            for m in range(2, N - 1):
                val = tangential_projection(N, xi, m, HJ)
                diff = abs(val - expected)
                if diff > 0.01:
                    failed += 1
                    print(f"  FAIL N={N} xi={xi} m={m}: J_tt={val:.4f} expected={expected:.4f}")
    if failed == 0:
        print("  ê_t^T ∇²J ê_t = -4/(1+ξ)² verified (mode-independent)")
    return failed


def check_W_minus_OmegaJ_equals_flat_shift() -> int:
    """ê_t^T ∇²(W - ΩJ) ê_t = (N-1)/(2ξ) = flat-plane Lagrange shift."""
    failed = 0
    for N in [5, 6, 7]:
        for xi in [0.15, 0.3, 0.5, 0.7]:
            r_E = np.sqrt(xi)
            theta = 2 * np.pi * np.arange(N) / N
            pos = np.concatenate([r_E * np.cos(theta), r_E * np.sin(theta)])

            HW = num_hess(W_confining, pos)
            HJ = num_hess(J_angular, pos)
            gH = num_grad(H_sph, pos)
            gJ = num_grad(J_angular, pos)
            Omega = np.dot(gH, gJ) / np.dot(gJ, gJ)

            M = HW - Omega * HJ
            expected = (N - 1) / (2 * xi)

            for m in [2, 3]:
                val = tangential_projection(N, xi, m, M)
                diff = abs(val - expected)
                ok = diff < 0.05
                if not ok:
                    failed += 1
                    print(f"  FAIL N={N} xi={xi} m={m}: (W-ΩJ)_tt={val:.4f} "
                          f"expected={expected:.4f}")
    if failed == 0:
        print("  ê_t^T ∇²(W-ΩJ) ê_t = (N-1)/(2ξ) verified (= flat Lagrange shift)")
    return failed


def check_tangential_eigenvalue_universal() -> int:
    """Full tangential eigenvalue = m(N-m)/(2ξ) on S² for all (N, ξ, m)."""
    failed = 0
    for N in [4, 5, 6, 7]:
        for xi in [0.15, 0.3, 0.5, 0.7]:
            r_E = np.sqrt(xi)
            theta = 2 * np.pi * np.arange(N) / N
            pos = np.concatenate([r_E * np.cos(theta), r_E * np.sin(theta)])
            HH = num_hess(H_sph, pos)
            HJ = num_hess(J_angular, pos)
            gH = num_grad(H_sph, pos)
            gJ = num_grad(J_angular, pos)
            Omega = np.dot(gH, gJ) / np.dot(gJ, gJ)
            L = HH - Omega * HJ

            for m in range(2, N - 1):
                val = tangential_projection(N, xi, m, L)
                expected = m * (N - m) / (2 * xi)
                diff = abs(val - expected)
                ok = diff < 0.05
                if not ok:
                    failed += 1
                    print(f"  FAIL N={N} xi={xi} m={m}: λ_t={val:.4f} "
                          f"expected={expected:.4f}")
    if failed == 0:
        print("  Tangential eigenvalue = m(N-m)/(2ξ) verified universally on S²")
    return failed


def check_sympy_tangential_projection() -> int:
    """Symbolic verification that the tangential projection of ∇²W at vertex k
    gives (N-1)/(1+ξ) (the sin²θ cos²θ cross terms cancel exactly)."""
    import sympy as sp

    xi, theta = sp.symbols('xi theta', positive=True)
    N_sym = sp.Symbol('N', integer=True, positive=True)

    # ∂²W_k/∂x² = (N-1)/(1+ξ) - 2(N-1)ξ cos²θ/(1+ξ)²
    Wxx = (N_sym - 1) / (1 + xi) - 2 * (N_sym - 1) * xi * sp.cos(theta) ** 2 / (1 + xi) ** 2
    Wyy = (N_sym - 1) / (1 + xi) - 2 * (N_sym - 1) * xi * sp.sin(theta) ** 2 / (1 + xi) ** 2
    Wxy = -2 * (N_sym - 1) * xi * sp.sin(theta) * sp.cos(theta) / (1 + xi) ** 2

    # Tangential projection: sin²θ Wxx - 2sinθcosθ Wxy + cos²θ Wyy
    proj = (sp.sin(theta) ** 2 * Wxx
            - 2 * sp.sin(theta) * sp.cos(theta) * Wxy
            + sp.cos(theta) ** 2 * Wyy)
    proj_simplified = sp.simplify(proj)
    expected = (N_sym - 1) / (1 + xi)

    diff = sp.simplify(proj_simplified - expected)
    if diff != 0:
        print(f"  FAIL: tangential projection of ∇²W = {proj_simplified}, not {expected}")
        return 1
    print("  Symbolic: sin²θ Wxx - 2sinθcosθ Wxy + cos²θ Wyy = (N-1)/(1+ξ)")
    return 0


def main() -> int:
    print("== W tangential mode-independence ==")
    if check_W_tangential_mode_independent():
        return 1

    print("== J tangential mode-independence ==")
    if check_J_tangential_mode_independent():
        return 1

    print("== W-ΩJ tangential = flat Lagrange shift ==")
    if check_W_minus_OmegaJ_equals_flat_shift():
        return 1

    print("== Tangential eigenvalue universality ==")
    if check_tangential_eigenvalue_universal():
        return 1

    print("== Symbolic tangential projection ==")
    if check_sympy_tangential_projection():
        return 1

    print("All checks pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
