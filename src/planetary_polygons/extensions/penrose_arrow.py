"""
Penrose past hypothesis from the Onsager temperature sign change.

The tunneling threshold ρ* is the β = 0 surface — the boundary between
negative temperature (interior, ordered polygon) and positive temperature
(exterior, disordered). The universe is created at this transition.

Key results:
  β(ρ) = (1/2) Σ_{m≠m*} 1/λ_m(ρ)  (Onsager microcanonical temperature)
  S_poly(ρ) = (1/2) Σ_{m≠m*} log|λ_m(ρ)|  (polygon entropy)

At ρ = ρ*:
  - β diverges (λ_{m*} → 0 if included in sum)
  - S_poly is at its minimum for the positive-T regime
  - The entropy gap S_BH/S_1loop ≈ 144 (N=7) is the computable Penrose gap

The arrow of time = the direction of increasing ρ (expansion),
driven by the positive-temperature second law.
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


def lambda_m(rho, m, N):
    return C1(rho, N) - casimir(m, N)


# =====================================================================
# PART 1: Onsager temperature β(ρ)
# =====================================================================

def onsager_beta(rho, N, include_critical=False):
    """Onsager microcanonical inverse temperature.

    β(ρ) = (1/2) Σ_{m≠m*} 1/λ_m(ρ)

    For ρ > ρ*: all λ_m > 0 (m ≠ m*), so β > 0 (positive temperature)
    For ρ < ρ*: λ_{m*} < 0; if included, β can change sign

    The non-critical modes always have λ_m > 0 for ρ > ρ*, so the
    non-critical β is always positive in the exterior.

    If include_critical=True, includes the critical mode (diverges at ρ*).
    """
    m_crit = N // 2
    f_crit = casimir(m_crit, N)
    c1 = C1(rho, N)
    beta = 0.0

    for m in range(1, N):
        if m == m_crit and not include_critical:
            continue
        # Skip paired critical mode for odd N
        if not include_critical and abs(casimir(m, N) - f_crit) < 1e-12:
            continue
        lam = c1 - casimir(m, N)
        if abs(lam) < 1e-15:
            return float('inf') if lam >= 0 else float('-inf')
        beta += 1.0 / lam

    return 0.5 * beta


def onsager_beta_profile(N, rho_min=None, rho_max=None, n_points=200):
    """Compute β(ρ) profile across the threshold.

    Returns (rho_values, beta_values, rho_star).
    Shows the sign change at ρ* when critical mode is included.
    """
    rho_star = find_threshold(N)
    if rho_min is None:
        rho_min = max(0.1, rho_star - 2.0)
    if rho_max is None:
        rho_max = rho_star + 5.0

    rho_vals = np.linspace(rho_min, rho_max, n_points)

    # Non-critical β (always positive in exterior)
    beta_noncrit = []
    for rho in rho_vals:
        beta_noncrit.append(onsager_beta(rho, N, include_critical=False))

    return rho_vals, np.array(beta_noncrit), rho_star


# =====================================================================
# PART 2: Polygon entropy S_poly(ρ)
# =====================================================================

def polygon_entropy(rho, N):
    """Polygon entropy at geodesic radius ρ.

    S_poly(ρ) = (1/2) Σ_{m≠m*} log|λ_m(ρ)|

    Excludes critical mode(s) (which diverge at ρ*).
    """
    m_crit = N // 2
    f_crit = casimir(m_crit, N)
    c1 = C1(rho, N)
    S = 0.0

    for m in range(1, N):
        if abs(casimir(m, N) - f_crit) < 1e-12:
            continue
        lam = c1 - casimir(m, N)
        if abs(lam) > 1e-15:
            S += 0.5 * log(abs(lam))

    return S


def entropy_profile(N, rho_min=None, rho_max=None, n_points=200):
    """Compute S_poly(ρ) profile across the threshold.

    Returns (rho_values, S_values, rho_star).
    """
    rho_star = find_threshold(N)
    if rho_min is None:
        rho_min = max(0.1, rho_star - 2.0)
    if rho_max is None:
        rho_max = rho_star + 5.0

    rho_vals = np.linspace(rho_min, rho_max, n_points)
    S_vals = np.array([polygon_entropy(rho, N) for rho in rho_vals])

    return rho_vals, S_vals, rho_star


def entropy_at_threshold(N):
    """S_poly at ρ = ρ* (the initial gravitational entropy).

    This is the one-loop entropy from the frozen determinant:
    S_1loop = (1/2) Σ_{m≠m*} log|f(m*,N) - f(m,N)|
    """
    m_crit = N // 2
    f_crit = casimir(m_crit, N)
    S = 0.0
    for m in range(1, N):
        gap = abs(f_crit - casimir(m, N))
        if gap > 1e-12:
            S += 0.5 * log(gap)
    return S


def cardy_entropy(N):
    """S_BH = (πc/3) cosh(ρ*) — the maximum gravitational entropy."""
    c = 12 * b_exact(N)
    rho_star = find_threshold(N)
    return (pi * c / 3) * cosh(rho_star)


# =====================================================================
# PART 3: The Penrose gap
# =====================================================================

def penrose_gap(N):
    """The computable Penrose entropy gap.

    Returns (S_initial, S_final, ratio, N).
    S_initial = S_1loop(ρ*) — gravitational entropy at creation
    S_final = S_BH — maximum gravitational entropy (Cardy)
    ratio = S_final / S_initial — the Penrose gap
    """
    S_initial = entropy_at_threshold(N)
    S_final = cardy_entropy(N)
    ratio = S_final / S_initial if S_initial > 0 else float('inf')
    return {
        'N': N,
        'S_initial': S_initial,
        'S_final': S_final,
        'ratio': ratio,
        'S_initial_bits': S_initial / log(2),
        'S_final_bits': S_final / log(2),
    }


def penrose_table(N_values=None):
    """Penrose gap for multiple N values."""
    if N_values is None:
        N_values = list(range(7, 16))
    return [penrose_gap(N) for N in N_values]


# =====================================================================
# PART 4: Temperature sign change verification
# =====================================================================

def critical_mode_contribution(rho, N):
    """The critical mode's contribution to β.

    λ_{m*}(ρ) = C₁(ρ) - f(m*, N)
    1/λ_{m*} → ±∞ at ρ = ρ*

    Sign: positive for ρ > ρ* (normal), negative for ρ < ρ* (inverted).
    """
    m_crit = N // 2
    lam = lambda_m(rho, m_crit, N)
    return lam


def temperature_sign_change(N, n_points=200):
    """Verify the temperature sign change at ρ*.

    The critical eigenvalue λ_{m*}:
    - Positive for ρ > ρ* → normal population → positive-T contribution
    - Zero at ρ = ρ* → divergence (β = 0 surface)
    - Negative for ρ < ρ* → inverted population → negative-T contribution

    Returns dict with profiles and transition point.
    """
    rho_star = find_threshold(N)
    rho_vals = np.linspace(max(0.1, rho_star - 2.0), rho_star + 3.0, n_points)

    lam_crit = np.array([critical_mode_contribution(rho, N) for rho in rho_vals])

    # Find zero crossing
    sign_changes = []
    for i in range(len(lam_crit) - 1):
        if lam_crit[i] * lam_crit[i + 1] < 0:
            # Linear interpolation
            rho_cross = rho_vals[i] - lam_crit[i] * (
                rho_vals[i + 1] - rho_vals[i]
            ) / (lam_crit[i + 1] - lam_crit[i])
            sign_changes.append(rho_cross)

    return {
        'rho_star': rho_star,
        'sign_change_at': sign_changes[0] if sign_changes else None,
        'match': abs(sign_changes[0] - rho_star) < 0.01 if sign_changes else False,
        'rho_vals': rho_vals,
        'lam_crit': lam_crit,
    }


# =====================================================================
# PART 5: Entropy derivative (verifies minimum at ρ*)
# =====================================================================

def entropy_derivative(rho, N):
    """dS_poly/dρ = (coth ρ / 2) Σ_{m≠m*} 1/λ_m(ρ).

    At ρ*: the non-critical modes all have λ_m > 0, so dS/dρ > 0.
    This means S is INCREASING at ρ* — the minimum is at or just before ρ*.
    """
    m_crit = N // 2
    f_crit = casimir(m_crit, N)
    c1 = C1(rho, N)
    coth_rho = cosh(rho) / sinh(rho)

    total = 0.0
    for m in range(1, N):
        if abs(casimir(m, N) - f_crit) < 1e-12:
            continue
        lam = c1 - casimir(m, N)
        if abs(lam) > 1e-15:
            total += 1.0 / lam

    return (coth_rho / 2) * total


def find_entropy_minimum(N, n_points=500):
    """Find the ρ where S_poly is minimised.

    Should be at or near ρ* (the creation point).
    """
    rho_star = find_threshold(N)
    rho_min = max(0.1, rho_star - 3.0)
    rho_max = rho_star + 5.0
    rho_vals = np.linspace(rho_min, rho_max, n_points)
    S_vals = np.array([polygon_entropy(rho, N) for rho in rho_vals])

    idx_min = np.argmin(S_vals)
    return {
        'rho_min_S': rho_vals[idx_min],
        'S_min': S_vals[idx_min],
        'rho_star': rho_star,
        'near_threshold': abs(rho_vals[idx_min] - rho_star) < 1.0,
    }
