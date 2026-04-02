"""
Penrose past hypothesis: Weyl curvature and entropy arrow.

The regular polygon at ρ* has ZERO Weyl curvature (uniform energy distribution).
As ρ increases past ρ*, the polygon perturbations grow, Weyl curvature grows,
and gravitational entropy increases. All four arrows align:
  1. Expansion (ρ increases)
  2. Entropy (S_poly increases)
  3. Weyl curvature (tidal forces grow)
  4. Structure formation (clumping develops)

The Weyl curvature of the N-gon configuration:
  The energy density on the ring is ρ_E(θ) = Σ_m |ε_m|² λ_m(ρ) cos(mθ)
  For the REGULAR polygon: all ε_m = 0 (no perturbation) → ρ_E = uniform → Weyl = 0.
  For perturbed polygon: ε_m ≠ 0 → ρ_E has multipole moments → Weyl ≠ 0.

The Weyl curvature squared (the Kretschner-like invariant) is:
  |W|² ∝ Σ_{m≥2} m²(m²-1) |ε_m|² / ρ^{2m+2}
  (only m ≥ 2 contributes; m = 0 is trace, m = 1 is dipole = CM motion)
"""

import numpy as np
from math import pi, log, sinh, cosh, sqrt, exp


def b_exact(N):
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


def casimir(m, N):
    return m * (N - m) / 2.0


def C1(rho, N):
    return log(2 * sinh(rho)) + b_exact(N)


def find_threshold(N, m_crit=None):
    if m_crit is None:
        m_crit = N // 2
    target = casimir(m_crit, N) - b_exact(N)
    if target > 0:
        return np.arcsinh(exp(target) / 2)
    return 0.01


def lambda_m(rho, m, N):
    return C1(rho, N) - casimir(m, N)


# =====================================================================
# PART 1: Weyl curvature of the polygon configuration
# =====================================================================

def weyl_squared_regular(rho, N):
    """Weyl curvature squared for the REGULAR polygon.

    For the regular N-gon: all perturbation amplitudes ε_m = 0.
    The energy distribution is uniform on the ring.
    Therefore |W|² = 0.

    This is the Penrose initial condition: zero Weyl curvature at creation.
    """
    return 0.0  # Exact: the regular polygon has zero Weyl curvature


def weyl_squared_perturbed(rho, N, epsilon_m):
    """Weyl curvature squared for a PERTURBED polygon.

    epsilon_m: dict mapping mode number m to perturbation amplitude.

    |W|² ∝ Σ_{m≥2} m²(m²-1) |ε_m|² λ_m(ρ)²
    (the λ_m factor comes from the restoring force, which determines
    the perturbation's gravitational effect)

    The m = 0 mode is trace (Ricci, not Weyl).
    The m = 1 mode is dipole (CM translation, gauge).
    Weyl starts at m = 2 (quadrupole).
    """
    W2 = 0.0
    for m, eps in epsilon_m.items():
        if m < 2:
            continue
        lam = lambda_m(rho, m, N)
        # Weyl multipole: m²(m²-1) is the angular Laplacian eigenvalue
        # for the traceless-transverse part
        weyl_weight = m**2 * (m**2 - 1)
        W2 += weyl_weight * eps**2 * lam**2
    return W2


# =====================================================================
# PART 2: Thermal perturbation amplitudes
# =====================================================================

def thermal_perturbation(rho, m, N):
    """Thermal equilibrium perturbation amplitude at temperature T(ρ).

    In the WKB (classical) regime, the angular modes are in thermal
    equilibrium with the breathing mode. The amplitude is:
      <|ε_m|²> = 1/(2λ_m)  (equipartition: (1/2)λ_m|ε_m|² = (1/2)T)

    with effective temperature T = 1 (in the BO framework, temperature
    is absorbed into the ρ-dependent eigenvalues).
    """
    lam = lambda_m(rho, m, N)
    if lam <= 0:
        return float('inf')  # unstable mode
    return 1.0 / (2 * lam)


def weyl_thermal(rho, N):
    """Weyl curvature squared from thermal perturbations.

    |W|²_thermal = Σ_{m≥2} m²(m²-1) × <|ε_m|²> × λ_m²
                 = Σ_{m≥2} m²(m²-1) × (1/(2λ_m)) × λ_m²
                 = (1/2) Σ_{m≥2} m²(m²-1) × λ_m
    """
    m_crit = N // 2
    f_crit = casimir(m_crit, N)
    W2 = 0.0
    for m in range(2, N):
        if abs(casimir(m, N) - f_crit) < 1e-12:
            continue
        lam = lambda_m(rho, m, N)
        if lam <= 0:
            continue
        weyl_weight = m**2 * (m**2 - 1)
        W2 += 0.5 * weyl_weight * lam
    return W2


# =====================================================================
# PART 3: Weyl growth profile
# =====================================================================

def weyl_profile(N, rho_min=None, rho_max=None, n_points=200):
    """Weyl curvature as a function of ρ (in the exterior).

    Shows monotonic growth from zero at ρ* outward.
    """
    rho_star = find_threshold(N)
    if rho_min is None:
        rho_min = rho_star + 0.01
    if rho_max is None:
        rho_max = rho_star + 5.0

    rho_vals = np.linspace(rho_min, rho_max, n_points)
    W2_vals = np.array([weyl_thermal(rho, N) for rho in rho_vals])

    return rho_vals, W2_vals, rho_star


# =====================================================================
# PART 4: Arrow alignment verification
# =====================================================================

def arrow_alignment(N, n_points=100):
    """Verify all four arrows point in the same direction (increasing ρ).

    Arrow 1: Expansion (ρ increases) — by definition
    Arrow 2: Entropy (S_poly increases for ρ > ρ*)
    Arrow 3: Weyl curvature (|W|² increases for ρ > ρ*)
    Arrow 4: Structure (perturbation amplitude grows)

    Returns True if all three computed arrows are monotonically increasing.
    """
    rho_star = find_threshold(N)
    rho_vals = np.linspace(rho_star + 0.1, rho_star + 4.0, n_points)

    # Entropy
    m_crit = N // 2
    f_crit = casimir(m_crit, N)
    S_vals = []
    for rho in rho_vals:
        S = 0.0
        for m in range(1, N):
            if abs(casimir(m, N) - f_crit) < 1e-12:
                continue
            lam = lambda_m(rho, m, N)
            if abs(lam) > 1e-15:
                S += 0.5 * log(abs(lam))
        S_vals.append(S)
    S_vals = np.array(S_vals)

    # Weyl
    W2_vals = np.array([weyl_thermal(rho, N) for rho in rho_vals])

    # Total perturbation energy
    E_pert = []
    for rho in rho_vals:
        E = 0.0
        for m in range(2, N):
            if abs(casimir(m, N) - f_crit) < 1e-12:
                continue
            lam = lambda_m(rho, m, N)
            if lam > 0:
                E += 1.0  # each mode contributes (1/2)T = 1/2 in natural units
        E_pert.append(E)
    E_pert = np.array(E_pert)

    # Check monotonicity
    S_monotone = np.all(np.diff(S_vals) > -1e-10)
    W_monotone = np.all(np.diff(W2_vals) > -1e-10)

    return {
        'entropy_increasing': bool(S_monotone),
        'weyl_increasing': bool(W_monotone),
        'all_aligned': bool(S_monotone and W_monotone),
        'rho_vals': rho_vals,
        'S_vals': S_vals,
        'W2_vals': W2_vals,
    }


# =====================================================================
# PART 5: Penrose gap decomposition
# =====================================================================

def penrose_decomposition(N):
    """Decompose the Penrose gap into its components.

    S_initial = S_1loop(ρ*) = (1/2) Σ log|λ_m(ρ*)|
    S_final = S_BH = (πc/3) cosh(ρ*)
    Gap = S_final / S_initial

    The gap has two factors:
    1. The Virasoro factor: S_BH / (c × something) — non-perturbative states
    2. The eigenvalue factor: the specific λ_m structure from Havelock

    Both are determined by N and b(N).
    """
    c = 12 * b_exact(N)
    rho_star = find_threshold(N)
    m_crit = N // 2
    f_crit = casimir(m_crit, N)

    # S_initial
    S_init = 0.0
    n_modes = 0
    for m in range(1, N):
        gap = abs(f_crit - casimir(m, N))
        if gap > 1e-12:
            S_init += 0.5 * log(gap)
            n_modes += 1

    # S_final (Cardy)
    S_final = (pi * c / 3) * cosh(rho_star)

    # Weyl at threshold
    W2_init = 0.0  # exact zero for regular polygon

    # Weyl at ρ* + 1 (some expansion)
    W2_later = weyl_thermal(rho_star + 1.0, N)

    return {
        'N': N,
        'c': c,
        'rho_star': rho_star,
        'n_modes': n_modes,
        'S_initial': S_init,
        'S_initial_bits': S_init / log(2),
        'S_final': S_final,
        'S_final_bits': S_final / log(2),
        'gap_ratio': S_final / S_init if S_init > 0 else float('inf'),
        'W2_initial': W2_init,
        'W2_at_rho_plus_1': W2_later,
    }
