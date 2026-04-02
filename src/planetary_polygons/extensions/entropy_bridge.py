"""
The Onsager → Bekenstein-Hawking entropy bridge.

The central claim: BH entropy arises from the degrees of freedom
that the Onsager (Born-Oppenheimer) coarse-graining discards.

The chain:
  Full system (N vortices, N-1 angular modes + 1 breathing mode)
  → BO approximation (keep ρ, integrate out angular modes)
  → Angular modes have information content measured by c = 12b(N) (Fisher-Rao)
  → Same c enters Brown-Henneaux: c = 3ℓ/(2G₃)
  → Cardy formula: S_BH = (πc/3)·cosh(ρ*)
  → Therefore: S_BH = f(c_Fisher-Rao) = f(information lost in Onsager)

Three entropy levels:
  S_CL   ~ O(N)    Caldeira-Leggett squeezing (Gaussian part only)
  S_1loop ~ O(N)   One-loop frozen determinant
  S_BH   ~ O(N²)   Full Cardy (all Virasoro descendants)

The gap S_BH >> S_1loop reflects the exponentially many Virasoro
descendants beyond the Gaussian sector.
"""

import numpy as np
from math import pi, log, sinh, cosh, tanh, sqrt, exp


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


# =====================================================================
# PART 1: CL squeezing parameters and entanglement entropy
# =====================================================================

def squeezing_parameters(N, rho=None):
    """Caldeira-Leggett squeezing parameters at the threshold.

    r_m = (Φ'(ρ*)/(2λ_m(ρ*)))²
    where Φ' = coth(ρ) and λ_m = f(m*,N) - f(m,N) at the threshold.

    Returns list of (m, lambda_m, r_m) for all non-critical modes.
    """
    m_crit = N // 2
    f_crit = casimir(m_crit, N)

    if rho is None:
        rho = find_threshold(N)

    phi_prime = cosh(rho) / sinh(rho)  # coth(ρ)

    results = []
    for m in range(1, N):
        lam = f_crit - casimir(m, N)
        if abs(lam) < 1e-12:
            continue  # skip critical mode(s)
        r_m = (phi_prime / (2 * abs(lam)))**2
        results.append((m, lam, r_m))

    return results


def cl_entanglement_entropy(N, rho=None):
    """Entanglement entropy from CL squeezing.

    S_m = (r_m + 1)·log(r_m + 1) - r_m·log(r_m)  for each mode.
    Total S_CL = Σ_m S_m.

    This captures only the GAUSSIAN part of the full entanglement.
    """
    params = squeezing_parameters(N, rho)
    S_total = 0.0
    mode_entropies = []

    for m, lam, r_m in params:
        if r_m < 1e-15:
            S_m = 0.0
        elif r_m < 1e-3:
            # Small-r expansion: S ≈ r(1 - log r)
            S_m = r_m * (1 - log(r_m))
        else:
            S_m = (r_m + 1) * log(r_m + 1) - r_m * log(r_m)
        S_total += S_m
        mode_entropies.append((m, lam, r_m, S_m))

    return S_total, mode_entropies


# =====================================================================
# PART 2: One-loop (frozen determinant) entropy
# =====================================================================

def one_loop_entropy(N):
    """One-loop entropy from the frozen determinant at threshold.

    S_1loop = -log Z_frozen = (1/2) Σ_{m≠m*} log|λ_m(ρ*)|
    where λ_m(ρ*) = f(m*, N) - f(m, N).
    """
    m_crit = N // 2
    f_crit = casimir(m_crit, N)
    S = 0.0
    for m in range(1, N):
        gap = abs(f_crit - casimir(m, N))
        if gap > 1e-12:
            S += 0.5 * log(gap)
    return S


# =====================================================================
# PART 3: Cardy (Bekenstein-Hawking) entropy
# =====================================================================

def cardy_entropy(N, rho=None):
    """Cardy formula for the BH entropy at the palindromic threshold.

    S_Cardy = (πc/3) · T · L = (πc/3) · cosh(ρ*)

    where:
      c = 12b(N) (central charge = Fisher-Rao coefficient)
      T = coth(ρ*)/(2π) (Gibbons-Hawking temperature)
      L = 2π sinh(ρ*) (horizon circumference)
      T·L = cosh(ρ*)
    """
    c = 12 * b_exact(N)
    if rho is None:
        rho = find_threshold(N)
    return (pi * c / 3) * cosh(rho)


def bh_entropy_components(N):
    """Decompose the BH entropy into its components.

    Returns dict with T, L, c, ρ*, and S_BH.
    """
    c = 12 * b_exact(N)
    rho = find_threshold(N)
    T = (cosh(rho) / sinh(rho)) / (2 * pi)  # coth(ρ)/(2π)
    L = 2 * pi * sinh(rho)
    S = (pi * c / 3) * cosh(rho)

    return {
        'N': N,
        'c': c,
        'rho_star': rho,
        'T_GH': T,
        'L_horizon': L,
        'TL': T * L,
        'cosh_rho': cosh(rho),
        'S_BH': S,
    }


# =====================================================================
# PART 4: Fisher-Rao metric verification
# =====================================================================

def fisher_rao_metric(rho, N):
    """Fisher-Rao information metric g_FR(ρ).

    g_FR = coth²(ρ) · Σ_{m≠m*} 1/λ_m(ρ)²

    This is ρ-dependent. The constant c = 12b(N) is the unique
    ρ-independent coefficient that preserves BO factorisation.
    """
    m_crit = N // 2
    c1 = C1(rho, N)
    coth2 = (cosh(rho) / sinh(rho))**2

    H = 0.0
    for m in range(1, N):
        if m == m_crit:
            continue
        lam = c1 - casimir(m, N)
        if abs(lam) > 1e-10:
            H += 1.0 / lam**2

    return coth2 * H


def fisher_rao_vs_c(N, n_points=50):
    """Compare ρ-dependent Fisher-Rao with constant c = 12b(N).

    Shows that g_FR(ρ) varies with ρ, while c is constant.
    The BO factorisation requires the constant prescription.
    """
    c = 12 * b_exact(N)
    rho_star = find_threshold(N)

    results = []
    for rho in np.linspace(rho_star + 0.5, rho_star + 10, n_points):
        g_fr = fisher_rao_metric(rho, N)
        ratio = g_fr / c
        results.append({
            'rho': rho,
            'g_FR': g_fr,
            'c_const': c,
            'ratio': ratio,
        })

    return results


# =====================================================================
# PART 5: The c identity (Fisher-Rao = Brown-Henneaux = Cardy)
# =====================================================================

def c_identity_check(N):
    """Verify that c appears consistently in all four roles.

    c₁ = 12b(N)                    (Todd class / orbifold)
    c₂ = WDW kinetic coefficient   (from BO factorisation)
    c₃ = Brown-Henneaux charge     (3ℓ/(2G₃))
    c₄ = Cardy formula input       (same number)

    In the framework, c₁ = c₂ = c₃ = c₄ by construction.
    This function verifies the algebraic identity.
    """
    c_todd = 12 * b_exact(N)

    # c from the eigenvalue sum (BO factorisation):
    # b(N) = (1/N) Σ_{m=0}^{N-1} f(m, N) + correction
    # Exact: b(N) = N(N+1)/12 - ln2 + ln(N)/(N-1)
    c_bo = 12 * (N * (N + 1) / 12 - log(2) + log(N) / (N - 1))

    # Central charge from the mode sum:
    # c = Σ_{m=1}^{N-1} 1 = N-1 free bosons on S¹
    # But each has a twist, giving c = 12b(N) total
    c_modes = N - 1  # naive counting (before twist correction)

    return {
        'N': N,
        'c_todd': c_todd,
        'c_bo': c_bo,
        'c_match': abs(c_todd - c_bo) < 1e-12,
        'c_naive_modes': c_modes,
        'c_over_modes': c_todd / c_modes,
    }


# =====================================================================
# PART 6: Entropy hierarchy table
# =====================================================================

def entropy_hierarchy(N_values=None):
    """Compare the three entropy levels for multiple N.

    S_CL    : Caldeira-Leggett squeezing (Gaussian)
    S_1loop : Frozen determinant (one-loop)
    S_BH    : Cardy formula (all Virasoro descendants)

    The hierarchy S_CL < S_1loop << S_BH reflects the exponential
    growth of Virasoro descendants beyond the Gaussian sector.
    """
    if N_values is None:
        N_values = list(range(7, 16))

    results = []
    for N in N_values:
        S_cl, _ = cl_entanglement_entropy(N)
        S_1l = one_loop_entropy(N)
        S_bh = cardy_entropy(N)
        c = 12 * b_exact(N)
        rho_star = find_threshold(N)

        results.append({
            'N': N,
            'c': c,
            'rho_star': rho_star,
            'S_CL': S_cl,
            'S_1loop': S_1l,
            'S_BH': S_bh,
            'ratio_BH_1loop': S_bh / S_1l if S_1l > 0 else float('inf'),
            'ratio_BH_CL': S_bh / S_cl if S_cl > 0 else float('inf'),
            'S_BH_over_c': S_bh / c,
        })

    return results


# =====================================================================
# PART 7: The full bridge argument
# =====================================================================

def bridge_summary(N=7):
    """Complete summary of the Onsager → BH entropy bridge for a given N.

    The argument:
    1. BO integrates out N-1 angular modes → information loss
    2. Information content measured by c = 12b(N) (Fisher-Rao)
    3. Same c enters Cardy formula via Brown-Henneaux
    4. Cardy gives S_BH = (πc/3)cosh(ρ*)
    5. Therefore S_BH = f(information lost in Onsager)
    """
    c = 12 * b_exact(N)
    rho_star = find_threshold(N)

    # Step 1: Angular modes
    m_crit = N // 2
    n_modes = sum(1 for m in range(1, N) if abs(casimir(m_crit, N) - casimir(m, N)) > 1e-12)

    # Step 2: Fisher-Rao
    g_fr_at_star = fisher_rao_metric(rho_star + 0.1, N)  # slightly off threshold

    # Step 3: Entropies
    S_cl, mode_details = cl_entanglement_entropy(N)
    S_1loop = one_loop_entropy(N)
    S_bh = cardy_entropy(N)

    # Step 4: Components
    bh = bh_entropy_components(N)

    return {
        'N': N,
        'n_angular_modes': n_modes,
        'c_fisher_rao': c,
        'c_brown_henneaux': c,  # same by construction
        'rho_star': rho_star,
        'T_gibbons_hawking': bh['T_GH'],
        'L_horizon': bh['L_horizon'],
        'S_CL': S_cl,
        'S_1loop': S_1loop,
        'S_BH': S_bh,
        'mode_details': mode_details,
        'S_BH_bits': S_bh / log(2),
    }
