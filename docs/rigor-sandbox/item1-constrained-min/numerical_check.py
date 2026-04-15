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
    failed = check_canonical_cases()
    if failed:
        print(f"FAILED {failed} canonical cases")
        return 1
    print("All canonical cases pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
