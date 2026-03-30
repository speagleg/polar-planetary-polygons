"""
Regularized entropy derivative at the palindromic threshold.

PROBLEM: At ρ = ρ*, the critical eigenvalue λ_{m*} = 0, so the one-loop
entropy S = -(1/2) Σ log|λ_m| diverges. The naive dS/dρ → ∞.

SOLUTION: The spectral zeta function regularization excludes zero modes.
The REDUCED determinant det'(H) = Π_{λ ≠ 0} λ is finite. Its derivative
gives the regularized entropy production rate:

    dS'/dρ|_{ρ*} = -(coth(ρ*)/2) × Σ_{m: λ_m ≠ 0, m ≠ 0} 1/λ_m(ρ*)

where λ_m(ρ*) = f(m*,N) - f(m,N) are the spectral gaps.

The zero mode contributes to the SPECTRAL FLOW (a topological
invariant = ±1/2 per simple crossing, the APS eta invariant shift),
not to the absolute value of the determinant.

KEY RESULT: The regularized dS/dρ is FINITE and COMPUTABLE for each N,
given by a purely algebraic spectral sum.
"""

import numpy as np
from math import pi, sin, cos, log, exp, sinh, cosh, tanh, acosh


def casimir(m, N):
    return m * (N - m) / 2.0


def b_exact(N):
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


def find_threshold(N):
    """Palindromic threshold ρ*(N) where λ_{m*} = 0."""
    m_crit = N // 2
    f_crit = casimir(m_crit, N)
    b = b_exact(N)
    target = f_crit - b
    if target > 0:
        return np.arcsinh(exp(target) / 2)
    return None


def spectral_gaps(N):
    """Spectral gaps at the palindromic threshold.

    λ_m(ρ*) = C₁(ρ*) - f(m,N) = f(m*,N) - f(m,N)

    Returns dict: {m: gap} for m with gap ≠ 0, excluding m = 0.
    """
    m_crit = N // 2
    f_crit = casimir(m_crit, N)
    gaps = {}
    for m in range(1, N):
        gap = f_crit - casimir(m, N)
        if abs(gap) > 1e-12:  # Exclude zero modes
            gaps[m] = gap
    return gaps


def spectral_sum(N):
    """The spectral sum Σ' 1/λ_m at the threshold (non-zero modes, m ≠ 0).

    This is the key algebraic quantity:
        σ(N) = Σ_{m: λ_m ≠ 0, m ≥ 1} 1/(f(m*,N) - f(m,N))
    """
    gaps = spectral_gaps(N)
    return sum(1.0 / gap for gap in gaps.values())


def regularized_dS_drho(N):
    """The regularized entropy derivative at the threshold.

    dS'/dρ|_{ρ*} = -(coth(ρ*)/2) × σ(N)

    where σ(N) = Σ' 1/λ_m is the spectral sum.
    """
    rho_star = find_threshold(N)
    if rho_star is None:
        return None, None, None
    sigma = spectral_sum(N)
    coth_rho = 1.0 / tanh(rho_star)
    dS = -(coth_rho / 2) * sigma
    return dS, sigma, rho_star


def spectral_flow_contribution(N):
    """The APS spectral flow at the threshold.

    When an eigenvalue crosses zero (simple crossing), the eta
    invariant shifts by ±1. For the palindromic pair {m*, N-m*}:
    - If m* ≠ N-m* (odd N): TWO eigenvalues cross → spectral flow = ±1
    - If m* = N-m* (even N): ONE eigenvalue crosses → spectral flow = ±1/2

    The spectral flow contributes to the PHASE of det(H), not to |det'(H)|.
    Therefore it does not affect the entropy S' = -(1/2) log|det'|.

    Returns (n_crossings, spectral_flow).
    """
    m_crit = N // 2
    if N % 2 == 0:
        # m* = N/2: single self-palindromic mode, one eigenvalue
        return 1, 0.5
    else:
        # m* ≠ N-m*: palindromic pair, two eigenvalues cross simultaneously
        return 2, 1.0


def verify_old_vs_new(N):
    """Compare the old (hand-waved) and new (derived) dS/dρ values.

    Old: dS/dρ = coth(ρ*)/2
    New: dS/dρ = -(coth(ρ*)/2) × σ(N)

    The old value assumes σ(N) = -1, which is generically false.
    """
    rho_star = find_threshold(N)
    if rho_star is None:
        return None
    coth_rho = 1.0 / tanh(rho_star)

    old_value = coth_rho / 2  # The hand-waved value
    dS_new, sigma, _ = regularized_dS_drho(N)

    return {
        'N': N,
        'rho_star': rho_star,
        'sigma_N': sigma,
        'old_dS': old_value,
        'new_dS': dS_new,
        'ratio': dS_new / old_value if old_value != 0 else None,
    }


if __name__ == "__main__":
    print("=" * 70)
    print("REGULARIZED ENTROPY DERIVATIVE AT PALINDROMIC THRESHOLDS")
    print("=" * 70)
    print()

    print("The spectral sum σ(N) = Σ' 1/(f(m*) - f(m)):")
    print(f"{'N':>4s} {'m*':>4s} {'σ(N)':>10s} {'old dS/dρ':>12s} "
          f"{'new dS/dρ':>12s} {'crossings':>10s}")
    print("-" * 64)

    for N in range(7, 16):
        result = verify_old_vs_new(N)
        if result is None:
            continue
        n_cross, sf = spectral_flow_contribution(N)
        rho_star = result['rho_star']
        coth = 1 / tanh(rho_star)
        print(f"{N:4d} {N//2:4d} {result['sigma_N']:10.4f} "
              f"{result['old_dS']:12.4f} {result['new_dS']:12.4f} "
              f"{n_cross:10d}")

    print()
    print("The spectral gaps for N=7:")
    gaps = spectral_gaps(7)
    for m, gap in sorted(gaps.items()):
        print(f"  m={m}: f(3,7)-f({m},7) = {casimir(3,7):.0f}-{casimir(m,7):.0f} = {gap:.1f}")
    print(f"  σ(7) = Σ 1/gap = {spectral_sum(7):.4f}")

    print()
    print("KEY FINDING:")
    print("  The old value dS/dρ = coth(ρ*)/2 corresponds to σ(N) = -1.")
    print("  The actual σ(N) is N-dependent and NOT equal to -1.")
    print("  The regularized dS/dρ must use the correct spectral sum.")
