"""Asserts the Havelock Lagrangian eigenvalue formula against numerical diagonalization.

Theorem (Paper I §6.2, thm:constrained-min):

    lambda_m^+ = (N - 1) - m(N - m) / 2
    lambda_m^- = m(N - m) / 2         for m = 1, ..., N - 1,

on the unit ring with mu_L = -(N - 1) / 4.

Verified here against a direct numerical diagonalization of the Lagrangian
Hessian projected onto the normalized mode-m (radial, tangential) basis, for
N in [3, 12] to 1e-2 (finite-difference precision). The full derivation is in
docs/rigor-sandbox/item1-constrained-min/derivation.tex with every algebraic
step verified to 30 decimal digits via sympy in numerical_check.py.
"""

from __future__ import annotations

import numpy as np
import pytest

from planetary_polygons.core.hessian import (
    ngon_positions,
    numerical_hessian,
    thomson_energy,
)


def _mode_m_block_eigenvalues(N: int, m: int) -> tuple[float, float]:
    """Eigenvalues of the mode-m 2x2 Lagrangian block in the (radial, tangential) basis.

    Returns (lower, upper) — not labeled by +/- since the labeling depends on
    whether m(N-m)/2 exceeds (N-1) - m(N-m)/2, which flips at m(N-m) = N - 1.
    """
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

    def _unit(v: np.ndarray) -> np.ndarray:
        n = np.linalg.norm(v)
        return v / n if n > 0 else v

    e_r, e_t = _unit(e_r), _unit(e_t)
    block = np.array([
        [e_r @ L_lagr @ e_r, e_r @ L_lagr @ e_t],
        [e_t @ L_lagr @ e_r, e_t @ L_lagr @ e_t],
    ])
    evals = np.linalg.eigvalsh(block)
    return float(evals[0]), float(evals[1])


TOLERANCE = 1e-2  # finite-difference precision of numerical_hessian (eps=1e-5)


@pytest.mark.parametrize("N", range(3, 13))
def test_trace_identity(N):
    """lambda^+ + lambda^- = N - 1 for every mode m."""
    for m in range(1, N):
        lo, hi = _mode_m_block_eigenvalues(N, m)
        assert abs((lo + hi) - (N - 1)) < TOLERANCE, (
            f"N={N}, m={m}: trace {lo + hi} != {N - 1}"
        )


@pytest.mark.parametrize("N", range(3, 13))
def test_havelock_formula(N):
    """Both block eigenvalues match ((N-1) - m(N-m)/2, m(N-m)/2) for each mode."""
    for m in range(1, N):
        lo, hi = _mode_m_block_eigenvalues(N, m)
        pred = sorted([(N - 1) - m * (N - m) / 2.0, m * (N - m) / 2.0])
        obs = sorted([lo, hi])
        assert abs(obs[0] - pred[0]) < TOLERANCE, (
            f"N={N}, m={m}: lower {obs[0]} != {pred[0]}"
        )
        assert abs(obs[1] - pred[1]) < TOLERANCE, (
            f"N={N}, m={m}: upper {obs[1]} != {pred[1]}"
        )


def test_canonical_cases_from_rigor_spec():
    """The three canonical cases from docs/PAPER1_RIGOR_REWRITE_SPEC.md."""
    for N, m, exp_a, exp_b in [
        (5, 2, 1.0, 3.0),
        (7, 3, 0.0, 6.0),
        (11, 5, -5.0, 15.0),
    ]:
        lo, hi = _mode_m_block_eigenvalues(N, m)
        obs = sorted([lo, hi])
        exp = sorted([exp_a, exp_b])
        assert abs(obs[0] - exp[0]) < TOLERANCE, f"N={N}, m={m}: lower {obs[0]}"
        assert abs(obs[1] - exp[1]) < TOLERANCE, f"N={N}, m={m}: upper {obs[1]}"


def test_off_diagonal_vanishes():
    """The rt cross entry (e_r^T L_lagr e_t) is numerically zero for every (N, m).

    This is Lemma lem:offdiag of the derivation: sum_j (alpha_j^2 - alpha_{j+p}^2) = 0.
    """
    for N in range(3, 13):
        theta = 2.0 * np.pi * np.arange(N) / N
        pos = ngon_positions(N, 1.0)
        H_full = numerical_hessian(thomson_energy, pos)
        dim = 2 * N
        mu_L = -(N - 1) / 4.0
        L_lagr = H_full - 2.0 * mu_L * np.eye(dim)
        for m in range(1, N):
            amp = np.cos(2.0 * np.pi * m * np.arange(N) / N)
            e_r = np.zeros(dim)
            e_r[:N] = amp * np.cos(theta)
            e_r[N:] = amp * np.sin(theta)
            e_t = np.zeros(dim)
            e_t[:N] = -amp * np.sin(theta)
            e_t[N:] = amp * np.cos(theta)
            e_r = e_r / np.linalg.norm(e_r)
            e_t = e_t / np.linalg.norm(e_t)
            cross = float(e_r @ L_lagr @ e_t)
            assert abs(cross) < TOLERANCE, f"N={N}, m={m}: H_rt = {cross}"
