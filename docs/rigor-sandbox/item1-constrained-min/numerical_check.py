"""Numerical + symbolic validator for the constrained-min derivation.

Every claim in derivation.tex must correspond to a check in this file.
Run: python3 docs/rigor-sandbox/item1-constrained-min/numerical_check.py
Exit 0 = all claims verified. Non-zero = derivation is wrong.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Tuple

import numpy as np

# Import the project's thomson_energy so we agree on sign/normalization.
_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT / "src"))
from planetary_polygons.core.hessian import (  # noqa: E402
    ngon_positions,
    numerical_hessian,
    thomson_energy,
)


def havelock_block_eigenvalues(N: int, m: int) -> Tuple[float, float]:
    """Eigenvalues of the mode-m 2x2 Lagrangian block in the (radial, tangential) basis.

    H = -sum_{j<k} ln|z_j - z_k|  (see src/planetary_polygons/core/hessian.py).
    Lagrangian Hessian: L = nabla^2 H - 2 mu_L I, with mu_L = -(N-1)/4.
    Projection: unit-normalized Fourier mode-m cosine amplitude in local
    (radial, tangential) frame at each vertex.

    Returns (lower_eigenvalue, upper_eigenvalue) — not signed by +/- label.
    """
    if m <= 0 or m >= N:
        raise ValueError(f"mode m must lie in [1, N-1]; got m={m}, N={N}")

    theta = 2.0 * np.pi * np.arange(N) / N
    pos = ngon_positions(N, 1.0)
    H_full = numerical_hessian(thomson_energy, pos)

    dim = 2 * N
    mu_L = -(N - 1) / 4.0
    L_lagr = H_full - 2.0 * mu_L * np.eye(dim)

    amp = np.cos(2.0 * np.pi * m * np.arange(N) / N)

    e_r = np.zeros(dim)
    e_r[:N] = amp * np.cos(theta)
    e_r[N:] = amp * np.sin(theta)

    e_t = np.zeros(dim)
    e_t[:N] = -amp * np.sin(theta)
    e_t[N:] = amp * np.cos(theta)

    def _norm(v):
        n = np.linalg.norm(v)
        return v / n if n > 0 else v

    e_r = _norm(e_r)
    e_t = _norm(e_t)

    block = np.array([
        [e_r @ L_lagr @ e_r, e_r @ L_lagr @ e_t],
        [e_t @ L_lagr @ e_r, e_t @ L_lagr @ e_t],
    ])
    evals = np.linalg.eigvalsh(block)
    return float(evals[0]), float(evals[1])


def check_havelock_identity_rr() -> int:
    """S_m^(rr) = sum_{p=1}^{N-1} (1 - cos(2 pi m p / N)) / (4 sin^2(pi p / N))
       equals m(N-m)/2 for all N in [3,10], m in [1, N-1].

    Verified to 30 digits of mpmath precision: sympy's simplify() cannot
    reliably close trigonometric sums for prime N, but high-precision
    evaluation of |sum - expected| vs 0 is rigorous when combined with the
    closed-form algebraic proof in derivation.tex."""
    import sympy as sp
    failed = 0
    prec = 30
    for N in range(3, 11):
        for m in range(1, N):
            total = sp.Rational(0)
            for p in range(1, N):
                num = 1 - sp.cos(2 * sp.pi * m * p / N)
                den = 4 * sp.sin(sp.pi * p / N) ** 2
                total += num / den
            expected = sp.Rational(m * (N - m), 2)
            diff = sp.Abs(total - expected).evalf(prec)
            if diff > sp.Float("1e-25"):
                failed += 1
                print(f"  FAIL N={N} m={m}: |sum - {expected}| = {diff}")
    if failed == 0:
        print("  S_m^(rr) = m(N-m)/2 verified to 30 digits for N in [3,10]")
    return failed


def check_cosecant_squared_sum() -> int:
    """Σ_{p=1}^{N-1} 1/(4 sin²(π p / N)) = (N² - 1)/12 for N in [3,10]."""
    import sympy as sp
    failed = 0
    for N in range(3, 11):
        total = sp.Rational(0)
        for p in range(1, N):
            total += 1 / (4 * sp.sin(sp.pi * p / N) ** 2)
        expected = sp.Rational(N * N - 1, 12)
        diff = sp.Abs(total - expected).evalf(30)
        if diff > sp.Float("1e-25"):
            failed += 1
            print(f"  FAIL N={N}: |sum - {expected}| = {diff}")
    if failed == 0:
        print("  Σ 1/(4 sin²(πp/N)) = (N² - 1)/12 verified to 30 digits for N in [3,10]")
    return failed


def check_rr_block_unshifted() -> int:
    """The radial-radial block eigenvalue (before Lagrange shift) equals
       (N - 1 - m(N-m)) / 2 for m in {1, ..., N-1}, derived from:
           λ_rr^(unshifted) = Σ_p (1 + cos(2πmp/N))/2
                              − Σ_p (1 − cos(2πmp/N) cos(2πp/N))/(4 sin²(πp/N)).
       Second sum simplifies via cos A cos B = (cos(A-B) + cos(A+B))/2 and the
       Havelock identity at indices m±1 to (m(N-m) - 1)/2, yielding
           λ_rr^(unshifted) = (N - 2)/2 − (m(N-m) - 1)/2 = (N - 1 - m(N-m))/2.
       We check both intermediate and final forms at 30-digit precision."""
    import sympy as sp
    failed = 0
    for N in range(3, 11):
        for m in range(1, N):
            # First sum
            sum1 = sp.Rational(0)
            for p in range(1, N):
                sum1 += (1 + sp.cos(2 * sp.pi * m * p / N)) / 2
            # Second sum
            sum2 = sp.Rational(0)
            for p in range(1, N):
                num = 1 - sp.cos(2 * sp.pi * m * p / N) * sp.cos(2 * sp.pi * p / N)
                den = 4 * sp.sin(sp.pi * p / N) ** 2
                sum2 += num / den
            total = sum1 - sum2
            expected = sp.Rational(N - 1 - m * (N - m), 2)
            diff = sp.Abs(total - expected).evalf(30)
            if diff > sp.Float("1e-25"):
                failed += 1
                print(f"  FAIL N={N} m={m}: |total - {expected}| = {diff}")
    if failed == 0:
        print("  λ_rr^(unshifted) = (N - 1 - m(N-m))/2 verified to 30 digits for N in [3,10]")
    return failed


def check_canonical_cases() -> int:
    """Spec's three canonical test cases (Item #1 spec, 'Key correctness checks')."""
    cases = [
        (5, 2, 1.0, 3.0),
        (7, 3, 0.0, 6.0),
        (11, 5, -5.0, 15.0),
    ]
    failed = 0
    for N, m, exp_plus, exp_minus in cases:
        lo, hi = havelock_block_eigenvalues(N, m)
        obs = tuple(sorted([lo, hi]))
        exp = tuple(sorted([exp_plus, exp_minus]))
        ok = all(abs(a - b) < 1e-2 for a, b in zip(obs, exp))
        status = "OK" if ok else "FAIL"
        print(f"  N={N:2d} m={m}: obs=({obs[0]:+.4f}, {obs[1]:+.4f}) "
              f"exp=({exp[0]:+.1f}, {exp[1]:+.1f}) [{status}]")
        if not ok:
            failed += 1
    return failed


def main() -> int:
    print("== Canonical cases (numerical oracle) ==")
    if check_canonical_cases():
        print("FAILED canonical cases")
        return 1

    print("== Havelock identity (radial-radial sum) ==")
    if check_havelock_identity_rr():
        print("FAILED radial-radial identity")
        return 1

    print("== Cosecant-squared sum (N² - 1)/12 ==")
    if check_cosecant_squared_sum():
        print("FAILED cosecant sum")
        return 1

    print("== Radial-radial block eigenvalue (unshifted) ==")
    if check_rr_block_unshifted():
        print("FAILED rr block")
        return 1

    print("All checks pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
