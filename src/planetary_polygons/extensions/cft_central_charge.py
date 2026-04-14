"""
Derivation of the central charge c = 12 b(N) of the polygon-gravity boundary CFT.

GOAL: Prove rigorously (not by matching) that the polygon system's associated CFT
has central charge c = 12 b(N), where
    b(N) = N(N+1)/12 - log 2 + log(N)/(N-1).

STRATEGY: Three independent computational routes should give the same c:

(A) Z_polygon(β) in the harmonic/action-angle approximation.
    Computed from the Havelock eigenvalue spectrum.
    High-T expansion gives c via Cardy/thermal entropy.

(B) Z_CS(level k) on the Seifert manifold H² ×_N S^1 with N Wilson lines.
    Witten 1989 formula for SU(2)_k, analytic continuation to SL(2,R).
    Involves Reidemeister torsion, Gauss product sin(πm/N) factors.

(C) Reidemeister / analytic torsion of the twisted Laplacian on the Seifert manifold,
    computed via Cheeger-Müller. This connects (A) to (B).

PHASE 1 (this file): explicit computation of each of (A), (B), (C), and verification
that they match at k = 2 b(N), c = 12 b(N).
"""
from __future__ import annotations

from math import cos, cosh, log, pi, sin, sinh
from typing import Callable

import numpy as np


# ======================================================================
# Polygon data: Havelock eigenvalues, b(N), mean Casimir
# ======================================================================

def havelock_eigenvalues(N: int, xi: float = 0.0) -> list[float]:
    """Havelock eigenvalues λ_m = C_1(ξ) - m(N-m)/2 on H² at Poincaré coord ξ.

    Returns the N-2 non-critical eigenvalues (excluding m* = ⌊N/2⌋ and, for
    odd N, the palindromic partner N-m*).
    """
    if xi == 0:
        C1 = N - 1
    else:
        C1 = (N - 1) * (1 + xi**2) / (1 - xi) ** 2

    m_star = N // 2
    partner = N - m_star
    result = []
    for m in range(1, N):
        if m == m_star or m == partner:
            continue
        lam = C1 - m * (N - m) / 2
        if lam > 0:
            result.append(lam)
    return result


def b_N(N: int) -> float:
    """Polygon self-energy constant."""
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


def mean_casimir(N: int) -> float:
    """<f(m,N)> = (1/(N-1)) Σ_{m=1}^{N-1} m(N-m)/2."""
    return sum(m * (N - m) / 2 for m in range(1, N)) / (N - 1)


# ======================================================================
# ROUTE A: Z_polygon via action-angle harmonic approximation
# ======================================================================

def Z_polygon_harmonic(N: int, beta: float, xi: float = 0.0) -> float:
    """Harmonic partition function of the polygon angular modes.

    Z = Π_m 1/(2 sinh(β λ_m / 2))

    for the non-critical modes (at the stability threshold, the m* mode drops out).
    """
    eigs = havelock_eigenvalues(N, xi)
    if not eigs:
        return 1.0  # No non-critical modes
    log_Z = 0.0
    for lam in eigs:
        log_Z -= log(2 * sinh(beta * lam / 2))
    return np.exp(log_Z)


def log_Z_polygon(N: int, beta: float, xi: float = 0.0) -> float:
    """log Z_polygon in harmonic approximation."""
    eigs = havelock_eigenvalues(N, xi)
    return -sum(log(2 * sinh(beta * lam / 2)) for lam in eigs)


def log_Z_polygon_high_T(N: int, beta: float, xi: float = 0.0) -> float:
    """Leading high-T expansion: Z ~ Π 1/(β λ_m), log Z ~ -Σ log(β λ_m)."""
    eigs = havelock_eigenvalues(N, xi)
    return -sum(log(beta * lam) for lam in eigs)


def extract_cardy_central_charge(N: int) -> float:
    """Extract c from the high-T behavior of Z_polygon.

    Cardy formula for 1D system on a circle of length L:
        log Z(β) ~ (π c L) / (6 β)  as β → 0

    But for a FINITE-DOF system (N-2 harmonic modes), log Z ~ (N-2) log(1/β),
    which is NOT the Cardy linear-in-1/β behavior.

    So the polygon system is NOT a CFT in the Cardy sense — its central charge
    must come from a different route (e.g., the Selberg/CS identification).
    """
    # Numerical test: fit log Z ~ a/β + b log(1/β) + c
    betas = [0.01, 0.02, 0.04, 0.08]
    logZs = [log_Z_polygon(N, b) for b in betas]
    # Fit: logZ = A/β + B log(1/β) + C
    # This has 3 params, 4 data points.
    from scipy.optimize import curve_fit

    def model(beta, A, B, C):
        return A / beta + B * np.log(1.0 / beta) + C

    popt, _ = curve_fit(model, betas, logZs, p0=[0, len(havelock_eigenvalues(N)), 0])
    A, B, C = popt
    # If A ≈ 0, then the polygon is NOT Cardy-type → c_Cardy is not well-defined
    # B should be the # of harmonic DOF = N-2 (4 at N=7)
    return A, B, C


# ======================================================================
# ROUTE B: Z_CS on Seifert manifold via Witten/Verlinde
# ======================================================================

def Z_CS_SU2_Seifert(N: int, k: int) -> float:
    """SU(2)_k Chern-Simons partition function on H² ×_N S¹ with N Wilson lines.

    For the trivial Wilson lines (j=1/2 fundamental in the Z_N-symmetric configuration),
    this reduces to a specific product over SU(2)_k characters.

    Witten 1989: for SU(2)_k CS on S³ with N unknot Wilson lines in the fundamental rep,
        Z = (2/(k+2))^{1/2} Σ_j S_{0j}^{N} where S_{0j} = √(2/(k+2)) sin(π(2j+1)/(k+2))

    On H² ×_N S¹ (Seifert), the structure is more complex. We use the Reidemeister
    torsion route: Z_CS = τ_an^{-1/2}.
    """
    # Verlinde modular S-matrix: S_{jj'} = √(2/(k+2)) sin(π(2j+1)(2j'+1)/(k+2))
    # For trivial Wilson line (j=0): S_{00} = √(2/(k+2)) sin(π/(k+2))
    # Partition function on S² × S¹ with no insertions: Z = 1 (pure CS)
    # With N insertions at Z_N-symmetric points: involves fusion rules

    # Simpler: for SU(2)_k on S³ with N unknots in j=1/2:
    # Z ∝ Σ_j S_{0j}^N / S_{00}^{N-1} by Witten's formula
    # For our Seifert setup, I'll compute this sum and see if it matches polygon.

    def S(j1, j2):
        return (2 / (k + 2)) ** 0.5 * sin(pi * (2 * j1 + 1) * (2 * j2 + 1) / (k + 2))

    total = 0.0
    for j in range(k + 1):
        j_half = j / 2  # j runs over 0, 1/2, 1, 3/2, ..., k/2
        term = S(0, j_half) ** N / S(0, 0) ** (N - 1)
        total += term
    return total


# ======================================================================
# ROUTE C: Reidemeister / analytic torsion
# ======================================================================

def reidemeister_torsion_seifert(N: int, rho_eigenvalues: list[complex]) -> float:
    """Reidemeister torsion for Seifert manifold H² ×_N S¹ with flat connection ρ.

    For a Seifert fibration with monodromy ρ:
        τ_R = Π_eigenvalues (2 sin(π arg(λ)/2))^a

    For SL(2,R) flat connection with holonomy = Z_N rotation:
    eigenvalues of ρ are e^{±2πi m/N} for m = 1, ..., N-1.
    """
    # For trivial flat connection: ρ = identity, torsion depends on H¹, H²
    # For non-trivial Z_N flat connection: eigenvalues are ω^m, ω^{-m} for ω = e^{2πi/N}
    result = 1.0
    for m in range(1, N):
        # Each rotation angle contributes 2 sin(πm/N)
        result *= 2 * sin(pi * m / N)
    # Gauss product: Π sin(πm/N) = N/2^{N-1}, so Π 2 sin(πm/N) = 2^{N-1} × N/2^{N-1} = N
    return result


# ======================================================================
# Diagnostic: what IS the natural central charge from each route?
# ======================================================================

def diagnose_central_charge_candidates(N: int) -> dict:
    """Compute various candidate definitions of the polygon 'central charge'."""
    out = {}
    b = b_N(N)
    out["b(N)"] = b
    out["12 b(N)"] = 12 * b
    out["mean Casimir × 12"] = 12 * mean_casimir(N)
    out["Σ log λ_m"] = sum(log(lam) for lam in havelock_eigenvalues(N))
    out["Σ λ_m"] = sum(havelock_eigenvalues(N))
    out["log τ_R"] = log(reidemeister_torsion_seifert(N, []))
    # Cardy attempt
    try:
        A, B, C = extract_cardy_central_charge(N)
        out["Cardy A (1/β coeff)"] = A
        out["Cardy B (log 1/β coeff)"] = B
    except Exception as e:
        out["Cardy"] = f"failed: {e}"
    return out


# ======================================================================
# THREE-WAY VERIFICATION (Pipelines A + B + C)
# ======================================================================

def verify_three_way(N: int, tol: float = 1e-8) -> dict:
    """Verify three-way agreement: c_A = c_B = c_C = 12 b(N).

    Returns dict with pipeline values and agreement status.
    """
    from planetary_polygons.extensions.cft_kirchhoff_anomaly import (
        central_charge_pipeline_C,
    )
    from planetary_polygons.extensions.cft_liouville_action import (
        central_charge_pipeline_A,
    )
    from planetary_polygons.extensions.cft_spectral_zeta import (
        central_charge_pipeline_B,
    )

    c_A = central_charge_pipeline_A(N)
    c_B = central_charge_pipeline_B(N)
    c_C = central_charge_pipeline_C(N)
    c_ref = 12 * b_N(N)

    agree = (abs(c_A - c_ref) < tol and
             abs(c_B - c_ref) < tol and
             abs(c_C - c_ref) < tol)

    return {
        "N": N,
        "c_ref": c_ref,
        "c_A (TZ saddle)": c_A,
        "c_B (spectral zeta)": c_B,
        "c_C (Kirchhoff)": c_C,
        "max_deviation": max(abs(c_A - c_ref), abs(c_B - c_ref), abs(c_C - c_ref)),
        "agreement": agree,
    }


if __name__ == "__main__":
    print("=" * 70)
    print("Central charge diagnostics: what does c = 12 b(N) actually mean?")
    print("=" * 70)
    for N in [3, 5, 7, 11]:
        print(f"\n--- N = {N} ---")
        diag = diagnose_central_charge_candidates(N)
        for key, val in diag.items():
            if isinstance(val, float):
                print(f"  {key}: {val:.4f}")
            else:
                print(f"  {key}: {val}")
