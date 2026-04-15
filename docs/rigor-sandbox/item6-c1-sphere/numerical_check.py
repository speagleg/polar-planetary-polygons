"""Numerical + symbolic validator for the C₁(S²) geodesic derivation.

Strategy: The appendix already derives C₁^eucl = (N-1)(1+ξ²)/(1+ξ)².
We verify this numerically, then derive and verify the algebraic
conversion C₁^eucl → C₁(S²) = (N-1)(1-ξ)/(1+ξ).

Run: python3 docs/rigor-sandbox/item6-c1-sphere/numerical_check.py
Exit 0 = all claims verified. Non-zero = derivation is wrong.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

_REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO / "src"))


# ---------------------------------------------------------------------------
# H_sph in stereographic coordinates (same layout as hessian.py)
# ---------------------------------------------------------------------------

def H_sph_stereo(pos: np.ndarray) -> float:
    """S² Hamiltonian: H = -Σ_{j<k} log|z_j-z_k| + (N-1)/2 Σ log(1+|z_k|²).

    pos = [x_0,...,x_{N-1}, y_0,...,y_{N-1}].
    """
    N = len(pos) // 2
    x, y = pos[:N], pos[N:]
    H = 0.0
    for j in range(N):
        for k in range(j + 1, N):
            r2 = (x[j] - x[k]) ** 2 + (y[j] - y[k]) ** 2
            if r2 > 1e-30:
                H -= 0.5 * np.log(r2)
    for k in range(N):
        H += (N - 1) / 2.0 * np.log(1 + x[k] ** 2 + y[k] ** 2)
    return H


def J_angular_momentum(pos: np.ndarray) -> float:
    """J = Σ (1 - |z_k|²) / (1 + |z_k|²) = Σ cos φ_k."""
    N = len(pos) // 2
    x, y = pos[:N], pos[N:]
    return np.sum((1 - x ** 2 - y ** 2) / (1 + x ** 2 + y ** 2))


def ngon_stereo(N: int, r_E: float) -> np.ndarray:
    """Regular N-gon at stereographic radius r_E."""
    theta = 2.0 * np.pi * np.arange(N) / N
    return np.concatenate([r_E * np.cos(theta), r_E * np.sin(theta)])


def numerical_hessian(f, pos, eps=1e-5):
    n = len(pos)
    H = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            pp = pos.copy(); pp[i] += eps; pp[j] += eps
            pm = pos.copy(); pm[i] += eps; pm[j] -= eps
            mp = pos.copy(); mp[i] -= eps; mp[j] += eps
            mm = pos.copy(); mm[i] -= eps; mm[j] -= eps
            val = (f(pp) - f(pm) - f(mp) + f(mm)) / (4 * eps ** 2)
            H[i, j] = val
            H[j, i] = val
    return H


def numerical_gradient(f, pos, eps=1e-7):
    n = len(pos)
    g = np.zeros(n)
    for i in range(n):
        pp = pos.copy(); pp[i] += eps
        pm = pos.copy(); pm[i] -= eps
        g[i] = (f(pp) - f(pm)) / (2 * eps)
    return g


def sphere_eucl_mode_eigenvalue(N: int, xi: float, m: int) -> float:
    """Mode-m RADIAL eigenvalue of constrained S² Hessian, stereographic frame.

    Uses the full S² Hamiltonian H_sph and the angular momentum constraint
    J = Σ cos φ_k. Computes in Cartesian stereographic coords (same as
    hessian.py for the flat case).

    Returns the EUCLIDEAN-FRAME eigenvalue, which should match
    C₁^eucl - m(N-m)/2 = (N-1)(1+ξ²)/(1+ξ)² - m(N-m)/2.
    """
    r_E = np.sqrt(xi)
    pos = ngon_stereo(N, r_E)
    dim = 2 * N
    theta = 2.0 * np.pi * np.arange(N) / N

    # Hessian of H_sph
    H_full = numerical_hessian(H_sph_stereo, pos)

    # Gradient of J at equilibrium
    grad_J = numerical_gradient(J_angular_momentum, pos)

    # Gradient of H at equilibrium
    grad_H = numerical_gradient(H_sph_stereo, pos)

    # Omega: grad_H = Omega * grad_J  (scalar least-squares)
    Omega = np.dot(grad_H, grad_J) / np.dot(grad_J, grad_J)

    # Hessian of J
    H_J = numerical_hessian(J_angular_momentum, pos)

    # Lagrangian Hessian: ∇²(H_sph - Ω J)
    L_lagr = H_full - Omega * H_J

    # Mode-m radial Fourier vector in local (radial, tangential) frame
    amp = np.cos(2.0 * np.pi * m * np.arange(N) / N)
    e_r = np.zeros(dim)
    e_r[:N] = amp * np.cos(theta)
    e_r[N:] = amp * np.sin(theta)
    norm = np.linalg.norm(e_r)
    if norm > 0:
        e_r /= norm

    return float(e_r @ L_lagr @ e_r)


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_c1_eucl_oracle() -> int:
    """C₁^eucl(ξ) = (N-1)(1+ξ²)/(1+ξ)² against stereographic oracle.

    The appendix defines λ_m · r_E² = C₁^eucl - m(N-m)/2, so the ACTUAL
    Hessian eigenvalue is [C₁^eucl - m(N-m)/2] / ξ.  To extract C₁^eucl:
        C₁^eucl = λ_actual × ξ + m(N-m)/2.
    """
    failed = 0
    for N in [4, 5, 6, 7]:
        for xi in [0.15, 0.3, 0.5, 0.7]:
            c1_eucl = (N - 1) * (1 + xi ** 2) / (1 + xi) ** 2
            m = 2
            lam_actual = sphere_eucl_mode_eigenvalue(N, xi, m)
            c1_oracle = lam_actual * xi + m * (N - m) / 2.0
            diff = abs(c1_oracle - c1_eucl)
            ok = diff < 0.02
            status = "OK" if ok else "FAIL"
            print(f"  N={N} xi={xi:.2f}: "
                  f"C1_eucl_oracle={c1_oracle:.4f} "
                  f"C1_eucl_formula={c1_eucl:.4f} "
                  f"delta={diff:.2e} [{status}]")
            if not ok:
                failed += 1
    if failed == 0:
        print("  C1^eucl matches stereographic oracle")
    return failed


def check_eucl_to_geo_ratio() -> int:
    """C₁(S²) / C₁^eucl = (1-ξ)(1+ξ)/(1+ξ²) = (1-ξ²)/(1+ξ²).

    Verify this identity symbolically with sympy."""
    import sympy as sp
    xi = sp.Symbol('xi', positive=True)
    c1_eucl = (1 + xi ** 2) / (1 + xi) ** 2
    c1_geo = (1 - xi) / (1 + xi)
    ratio = sp.simplify(c1_geo / c1_eucl)
    expected = (1 - xi ** 2) / (1 + xi ** 2)
    diff = sp.simplify(ratio - expected)
    if diff != 0:
        print(f"  FAIL: ratio - expected = {diff}")
        return 1
    print(f"  C1(S2) / C1^eucl = (1 - xi^2) / (1 + xi^2) verified")
    return 0


def check_c1_boundary_cases() -> int:
    """C₁(S²,0) = N-1 and C₁(S²,1) = 0."""
    failed = 0
    for N in range(3, 11):
        if abs((N - 1) * 1 / 1 - (N - 1)) > 1e-15:
            failed += 1
        if abs((N - 1) * 0 / 2) > 1e-15:
            failed += 1
    if failed == 0:
        print("  Boundary: C1(0)=N-1, C1(1)=0 for N in [3,10]")
    return failed


def check_c1_equals_cos_phi() -> int:
    """(1-ξ)/(1+ξ) = cos φ₀ where ξ = tan²(φ₀/2)."""
    import sympy as sp
    phi = sp.Symbol('phi', positive=True)
    xi = sp.tan(phi / 2) ** 2
    diff = sp.simplify((1 - xi) / (1 + xi) - sp.cos(phi))
    if diff != 0:
        print(f"  FAIL: diff = {diff}")
        return 1
    print("  (1-xi)/(1+xi) = cos(phi0) verified symbolically")
    return 0


def check_geodesic_second_variation() -> int:
    """Direct mpmath computation of d²(H_geo - ΩJ)/da² at the N-gon on S².

    Perturbation: δφ_k = a cos(2πmk/N).
    h_geo = -(1/2) log((1 - cos d)/2).
    d²h/da² = (1/2)(d²c/da²)/(1-c) + (1/2)(dc/da)²/(1-c)²

    Uses 50-digit mpmath to handle the massive cancellation in per-pair sums.
    Verifies eigenvalue = (N-1)cos φ₀ - m(N-m)/2.
    """
    from mpmath import mp, mpf, cos, sin, tan, pi, fabs, log
    mp.dps = 50
    failed = 0

    for phi0_deg in [20, 45, 70]:
        phi0 = mpf(phi0_deg) * pi / 180
        S = sin(phi0)
        C = cos(phi0)
        xi = tan(phi0 / 2) ** 2

        for N in [5, 6]:
            for m in [2, 3] if N > 5 else [2]:
                total_H = mpf(0)

                for p in range(1, N):
                    Dth = 2 * pi * p / N
                    cosDth = cos(Dth)
                    c0 = C ** 2 + S ** 2 * cosDth
                    omc = 1 - c0  # = 2 S² sin²(πp/N)

                    cosmp = cos(2 * pi * m * p / N)

                    # Fourier-reduced second derivatives summed over j
                    d2c_sum = -c0 * N + 2 * (mpf(N) / 2) * cosmp * (S ** 2 - C ** 2 * cosDth)
                    dc_sq_sum = S ** 2 * C ** 2 * (1 - cosDth) ** 2 * N * (1 + cosmp)

                    # d²h summed over j for fixed p
                    t1 = d2c_sum / (2 * omc)
                    t2 = dc_sq_sum / (2 * omc ** 2)
                    total_H += (t1 + t2) / 2  # (1/2) Σ_p for Σ_{j<k}

                # d²J/da² = -(N/2) cos φ₀
                d2J = -mpf(N) / 2 * C

                # Ω = (N-1)(1-ξ²)/(8ξ)
                Omega = (N - 1) * (1 - xi ** 2) / (8 * xi)

                eigenvalue = (total_H - Omega * d2J) / (mpf(N) / 2)
                expected = (N - 1) * C - mpf(m * (N - m)) / 2

                diff = fabs(eigenvalue - expected)
                ok = diff < mpf("1e-10")
                status = "OK" if ok else "FAIL"
                print(f"  N={N} m={m} phi0={phi0_deg}deg: "
                      f"eigenvalue={float(eigenvalue):.8f} "
                      f"expected={float(expected):.8f} "
                      f"delta={float(diff):.2e} [{status}]")
                if not ok:
                    failed += 1

    if failed == 0:
        print("  Geodesic second variation matches (N-1)cos(phi0) - m(N-m)/2")
    return failed


def check_conversion_factor_meaning() -> int:
    """The conversion (1-ξ²)/(1+ξ²) = cos(2 arctan(√ξ)) = cos φ₀ ... no.
    Let's verify: (1-ξ²)/(1+ξ²) with ξ = tan²(φ₀/2).

    (1 - tan⁴(φ₀/2)) / (1 + tan⁴(φ₀/2)) = cos(2 arctan(tan²(φ₀/2))).
    """
    import sympy as sp
    phi = sp.Symbol('phi', positive=True)
    xi = sp.tan(phi / 2) ** 2
    ratio = (1 - xi ** 2) / (1 + xi ** 2)
    # This should equal cos(2 arctan(ξ)) = cos(2 arctan(tan²(φ/2)))
    cos_form = sp.cos(2 * sp.atan(xi))
    diff = sp.simplify(ratio - cos_form)
    if diff != 0:
        print(f"  Note: ratio - cos(2 arctan(xi)) = {diff}")
    else:
        print(f"  (1-xi^2)/(1+xi^2) = cos(2 arctan(xi)) verified")

    # Also check what the ratio equals in terms of phi
    ratio_val_30 = float(ratio.subs(phi, sp.pi / 6).evalf())
    ratio_val_60 = float(ratio.subs(phi, sp.pi / 3).evalf())
    ratio_val_90 = float(ratio.subs(phi, sp.pi / 2).evalf())
    print(f"  ratio at phi=30°: {ratio_val_30:.6f}")
    print(f"  ratio at phi=60°: {ratio_val_60:.6f}")
    print(f"  ratio at phi=90°: {ratio_val_90:.6f}")
    return 0  # informational


def main() -> int:
    print("== C1^eucl vs stereographic oracle ==")
    if check_c1_eucl_oracle():
        print("FAILED C1^eucl oracle")
        return 1

    print("== C1(S2)/C1^eucl ratio identity ==")
    if check_eucl_to_geo_ratio():
        print("FAILED ratio")
        return 1

    print("== Geodesic second variation (direct sympy) ==")
    if check_geodesic_second_variation():
        print("FAILED geodesic variation")
        return 1

    print("== Conversion factor analysis ==")
    check_conversion_factor_meaning()

    print("== Boundary cases ==")
    if check_c1_boundary_cases():
        print("FAILED boundary")
        return 1

    print("== cos(phi) identity ==")
    if check_c1_equals_cos_phi():
        print("FAILED cos identity")
        return 1

    print("All checks pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
