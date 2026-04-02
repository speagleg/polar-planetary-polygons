"""
Radion inflation power spectrum: does the inflection point enhance small-scale power?

The radion potential:
  V(σ) = N²/(8σ²) - c₁₁/(12σ) + Λσ

has an inflection point at σ_infl ≈ 4.3 (N=11) where V'' = 0.
Near the inflection point, slow-roll breaks down (ultra-slow-roll),
and the power spectrum can be significantly enhanced.

KEY QUESTION: Is the enhancement on galactic scales (k ~ 1-100 Mpc⁻¹)?
If so, it could explain the JWST early massive galaxy anomaly.
If not, the framework has the same problem as standard ΛCDM.

The scale that exits the horizon at e-fold N_e is:
  k(N_e) = k_pivot × exp(N_e_pivot - N_e)

where N_e is counted from the END of inflation.
Large scales (CMB, k ~ 0.05 Mpc⁻¹) exit at N_e ~ 50-60.
Galactic scales (k ~ 1-100 Mpc⁻¹) exit at N_e ~ 43-48.
"""

import numpy as np
from math import pi, log, sqrt, exp


# =====================================================================
# Physical constants
# =====================================================================

M_P = 1.0  # Planck mass in reduced Planck units (M_P = 1/√(8πG))


# =====================================================================
# PART 1: Radion potential and derivatives
# =====================================================================

def b_exact(N):
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


def radion_potential(sigma, N=11, c_N=None, Lambda=None):
    """Radion potential V(σ) = N²/(8σ²) - c_N/(12σ) + Λσ.

    Parameters normalised so that V(σ_min) ≈ Λ × σ_min (the CC).
    """
    if c_N is None:
        c_N = 12 * b_exact(N)
    if Lambda is None:
        # Normalise so that V(σ_min) gives correct CC
        # For now use Λ = 1 (will cancel in slow-roll ratios)
        Lambda = 1.0

    return N**2 / (8 * sigma**2) - c_N / (12 * sigma) + Lambda * sigma


def radion_V_prime(sigma, N=11, c_N=None, Lambda=None):
    """V'(σ) = -N²/(4σ³) + c_N/(12σ²) + Λ."""
    if c_N is None:
        c_N = 12 * b_exact(N)
    if Lambda is None:
        Lambda = 1.0
    return -N**2 / (4 * sigma**3) + c_N / (12 * sigma**2) + Lambda


def radion_V_double_prime(sigma, N=11, c_N=None, Lambda=None):
    """V''(σ) = 3N²/(4σ⁴) - c_N/(6σ³)."""
    if c_N is None:
        c_N = 12 * b_exact(N)
    if Lambda is None:
        Lambda = 1.0
    return 3 * N**2 / (4 * sigma**4) - c_N / (6 * sigma**3)


def radion_V_triple_prime(sigma, N=11, c_N=None, Lambda=None):
    """V'''(σ) = -3N²/σ⁵ + c_N/(2σ⁴)."""
    if c_N is None:
        c_N = 12 * b_exact(N)
    if Lambda is None:
        Lambda = 1.0
    return -3 * N**2 / sigma**5 + c_N / (2 * sigma**4)


def inflection_point(N=11, c_N=None):
    """σ_infl where V'' = 0."""
    if c_N is None:
        c_N = 12 * b_exact(N)
    # V'' = 3N²/(4σ⁴) - c_N/(6σ³) = 0
    # → σ = 9N²/(2c_N)
    return 9 * N**2 / (2 * c_N)


def potential_minimum(N=11, c_N=None, Lambda=None):
    """σ_min where V' = 0 (approximate, for large Λσ dominance)."""
    if c_N is None:
        c_N = 12 * b_exact(N)
    if Lambda is None:
        Lambda = 1.0
    # V' = -N²/(4σ³) + c_N/(12σ²) + Λ = 0
    # For large σ: Λ dominates, so σ_min is where the σ⁻² and σ⁻³ terms balance Λ
    # Numerical solution
    from scipy.optimize import brentq
    try:
        sigma_min = brentq(lambda s: radion_V_prime(s, N, c_N, Lambda), 0.5, 10.0)
    except Exception:
        # Fallback: approximate
        sigma_min = (N**2 / (4 * Lambda))**(1.0/3)
    return sigma_min


# =====================================================================
# PART 2: Slow-roll parameters
# =====================================================================

def slow_roll_epsilon(sigma, N=11, c_N=None, Lambda=None):
    """First slow-roll parameter ε = (M_P²/2)(V'/V)²."""
    V = radion_potential(sigma, N, c_N, Lambda)
    Vp = radion_V_prime(sigma, N, c_N, Lambda)
    if abs(V) < 1e-30:
        return float('inf')
    return 0.5 * (Vp / V)**2


def slow_roll_eta(sigma, N=11, c_N=None, Lambda=None):
    """Second slow-roll parameter η = M_P² V''/V."""
    V = radion_potential(sigma, N, c_N, Lambda)
    Vpp = radion_V_double_prime(sigma, N, c_N, Lambda)
    if abs(V) < 1e-30:
        return float('inf')
    return Vpp / V


def slow_roll_xi2(sigma, N=11, c_N=None, Lambda=None):
    """Third slow-roll parameter ξ² = M_P⁴ V'V'''/(V²)."""
    V = radion_potential(sigma, N, c_N, Lambda)
    Vp = radion_V_prime(sigma, N, c_N, Lambda)
    Vppp = radion_V_triple_prime(sigma, N, c_N, Lambda)
    if abs(V) < 1e-30:
        return float('inf')
    return Vp * Vppp / V**2


def spectral_index(sigma, N=11, c_N=None, Lambda=None):
    """n_s = 1 - 6ε + 2η."""
    eps = slow_roll_epsilon(sigma, N, c_N, Lambda)
    eta = slow_roll_eta(sigma, N, c_N, Lambda)
    return 1 - 6 * eps + 2 * eta


def spectral_running(sigma, N=11, c_N=None, Lambda=None):
    """dn_s/dlnk = 16εη - 24ε² - 2ξ²."""
    eps = slow_roll_epsilon(sigma, N, c_N, Lambda)
    eta = slow_roll_eta(sigma, N, c_N, Lambda)
    xi2 = slow_roll_xi2(sigma, N, c_N, Lambda)
    return 16 * eps * eta - 24 * eps**2 - 2 * xi2


def tensor_to_scalar(sigma, N=11, c_N=None, Lambda=None):
    """r = 16ε."""
    return 16 * slow_roll_epsilon(sigma, N, c_N, Lambda)


# =====================================================================
# PART 3: E-fold computation (σ → N_e mapping)
# =====================================================================

def efolds_from_sigma(sigma_start, sigma_end, N=11, c_N=None, Lambda=None,
                      n_steps=10000):
    """Number of e-folds from σ_start to σ_end.

    N_e = ∫ V/(V') dσ  (in the slow-roll approximation)

    σ decreases from σ_start (large, beginning) to σ_end (small, end).
    """
    if c_N is None:
        c_N = 12 * b_exact(N)
    if Lambda is None:
        Lambda = 1.0

    sigma_vals = np.linspace(sigma_start, sigma_end, n_steps)
    integrand = np.array([
        radion_potential(s, N, c_N, Lambda) / abs(radion_V_prime(s, N, c_N, Lambda))
        if abs(radion_V_prime(s, N, c_N, Lambda)) > 1e-30 else 0.0
        for s in sigma_vals
    ])
    Ne = np.trapz(np.abs(integrand), sigma_vals)
    return abs(Ne)


def sigma_at_efold(N_e_target, sigma_end, N=11, c_N=None, Lambda=None,
                   sigma_max=20.0, n_steps=10000):
    """Find σ corresponding to a given number of e-folds before end.

    σ(N_e) such that ∫_{σ(N_e)}^{σ_end} V/V' dσ = N_e_target.
    """
    if c_N is None:
        c_N = 12 * b_exact(N)
    if Lambda is None:
        Lambda = 1.0

    sigma_vals = np.linspace(sigma_end, sigma_max, n_steps)
    Ne_cumulative = np.zeros(n_steps)

    for i in range(1, n_steps):
        ds = sigma_vals[i] - sigma_vals[i - 1]
        V = radion_potential(sigma_vals[i], N, c_N, Lambda)
        Vp = radion_V_prime(sigma_vals[i], N, c_N, Lambda)
        if abs(Vp) > 1e-30:
            Ne_cumulative[i] = Ne_cumulative[i - 1] + abs(V / Vp) * ds
        else:
            Ne_cumulative[i] = Ne_cumulative[i - 1]

    # Interpolate to find σ at N_e_target
    idx = np.searchsorted(Ne_cumulative, N_e_target)
    if idx >= n_steps:
        return sigma_vals[-1]
    if idx == 0:
        return sigma_vals[0]
    # Linear interpolation
    frac = (N_e_target - Ne_cumulative[idx - 1]) / (
        Ne_cumulative[idx] - Ne_cumulative[idx - 1] + 1e-30)
    return sigma_vals[idx - 1] + frac * (sigma_vals[idx] - sigma_vals[idx - 1])


# =====================================================================
# PART 4: Power spectrum as a function of scale
# =====================================================================

def power_spectrum_profile(N=11, c_N=None, Lambda=None, Ne_total=50,
                           n_points=200):
    """Compute n_s(k), running(k), and relative power enhancement.

    Maps each e-fold number N_e to a wavenumber k:
      k(N_e) = k_pivot × exp(N_e_pivot - N_e)

    Returns dict with profiles.
    """
    if c_N is None:
        c_N = 12 * b_exact(N)
    if Lambda is None:
        Lambda = 1.0

    sigma_infl = inflection_point(N, c_N)

    # Find σ_end where ε = 1 (end of inflation)
    sigma_test = np.linspace(1.0, sigma_infl * 2, 1000)
    eps_test = [slow_roll_epsilon(s, N, c_N, Lambda) for s in sigma_test]

    # Find where inflation can occur (ε < 1)
    # The inflection point is where η → 0 and inflation is most efficient
    # σ_end is where ε → 1 (inflation ends)
    sigma_end = 1.35  # approximate minimum, where slow roll ends

    # Compute σ for each N_e
    Ne_vals = np.linspace(1, Ne_total, n_points)
    results = []

    for Ne in Ne_vals:
        sigma = sigma_at_efold(Ne, sigma_end, N, c_N, Lambda)
        eps = slow_roll_epsilon(sigma, N, c_N, Lambda)
        eta = slow_roll_eta(sigma, N, c_N, Lambda)
        ns = spectral_index(sigma, N, c_N, Lambda)
        running = spectral_running(sigma, N, c_N, Lambda)
        r = tensor_to_scalar(sigma, N, c_N, Lambda)

        # k relative to pivot (N_e_pivot = 50 for k_pivot = 0.05 Mpc⁻¹)
        Ne_pivot = Ne_total
        ln_k_ratio = Ne_pivot - Ne  # ln(k/k_pivot)
        k_over_pivot = exp(ln_k_ratio)

        # Power spectrum enhancement relative to scale-invariant
        # P(k)/P(k_pivot) ≈ (k/k_pivot)^{n_s(k)-1}
        # More precisely: P ∝ V/ε, so
        V = radion_potential(sigma, N, c_N, Lambda)
        V_pivot = radion_potential(
            sigma_at_efold(Ne_total, sigma_end, N, c_N, Lambda),
            N, c_N, Lambda)
        eps_pivot = slow_roll_epsilon(
            sigma_at_efold(Ne_total, sigma_end, N, c_N, Lambda),
            N, c_N, Lambda)

        # P(k)/P(k_pivot) = (V/ε) / (V_pivot/ε_pivot)
        if eps > 1e-30 and eps_pivot > 1e-30:
            power_ratio = (V / eps) / (V_pivot / eps_pivot)
        else:
            power_ratio = 1.0

        results.append({
            'Ne': Ne,
            'sigma': sigma,
            'epsilon': eps,
            'eta': eta,
            'n_s': ns,
            'running': running,
            'r': r,
            'k_over_pivot': k_over_pivot,
            'power_ratio': power_ratio,
        })

    return results


# =====================================================================
# PART 5: JWST-relevant scales
# =====================================================================

def jwst_assessment(N=11, c_N=None, Lambda=None, Ne_total=50):
    """Assess whether the radion potential helps with the JWST anomaly.

    JWST finds ~5× more massive galaxies at z > 10 than ΛCDM predicts.
    This requires ~20-30% enhancement in P(k) at k ~ 1-100 Mpc⁻¹.

    Galactic scales correspond to:
      k ~ 1 Mpc⁻¹: Ne ≈ Ne_total - ln(1/0.05) ≈ Ne_total - 3 ≈ 47
      k ~ 100 Mpc⁻¹: Ne ≈ Ne_total - ln(100/0.05) ≈ Ne_total - 7.6 ≈ 42

    So we need enhancement at Ne ≈ 42-47.
    """
    if c_N is None:
        c_N = 12 * b_exact(N)
    if Lambda is None:
        Lambda = 1.0

    sigma_infl = inflection_point(N, c_N)
    sigma_end = 1.35

    # Check n_s and power at galactic scales
    galactic_Ne = [42, 44, 46, 48]
    pivot_Ne = Ne_total

    sigma_pivot = sigma_at_efold(pivot_Ne, sigma_end, N, c_N, Lambda)
    eps_pivot = slow_roll_epsilon(sigma_pivot, N, c_N, Lambda)
    V_pivot = radion_potential(sigma_pivot, N, c_N, Lambda)

    results = []
    for Ne in galactic_Ne:
        sigma = sigma_at_efold(Ne, sigma_end, N, c_N, Lambda)
        eps = slow_roll_epsilon(sigma, N, c_N, Lambda)
        eta = slow_roll_eta(sigma, N, c_N, Lambda)
        ns = spectral_index(sigma, N, c_N, Lambda)
        V = radion_potential(sigma, N, c_N, Lambda)
        k_mpc = 0.05 * exp(pivot_Ne - Ne)

        if eps > 1e-30 and eps_pivot > 1e-30:
            power_ratio = (V / eps) / (V_pivot / eps_pivot)
        else:
            power_ratio = 1.0

        results.append({
            'Ne': Ne,
            'k_mpc': k_mpc,
            'sigma': sigma,
            'n_s': ns,
            'epsilon': eps,
            'eta': eta,
            'power_ratio': power_ratio,
            'enhancement_pct': (power_ratio - 1) * 100,
        })

    # Is there enough enhancement?
    max_enhancement = max(r['enhancement_pct'] for r in results)
    jwst_needed = 20  # percent enhancement needed

    return {
        'scales': results,
        'sigma_infl': sigma_infl,
        'max_enhancement_pct': max_enhancement,
        'jwst_needed_pct': jwst_needed,
        'helps_jwst': max_enhancement > jwst_needed,
    }


# =====================================================================
# PART 6: Slow-roll profile (visualisation data)
# =====================================================================

def slow_roll_profile(N=11, c_N=None, Lambda=None, sigma_min=1.5,
                      sigma_max=15.0, n_points=200):
    """Compute slow-roll parameters across the full field range.

    Shows how ε, η, n_s vary from large σ through the inflection point
    down to the minimum.
    """
    if c_N is None:
        c_N = 12 * b_exact(N)
    if Lambda is None:
        Lambda = 1.0

    sigma_vals = np.linspace(sigma_min, sigma_max, n_points)
    results = []

    for sigma in sigma_vals:
        eps = slow_roll_epsilon(sigma, N, c_N, Lambda)
        eta = slow_roll_eta(sigma, N, c_N, Lambda)
        ns = spectral_index(sigma, N, c_N, Lambda)
        running = spectral_running(sigma, N, c_N, Lambda)
        V = radion_potential(sigma, N, c_N, Lambda)

        results.append({
            'sigma': sigma,
            'V': V,
            'epsilon': eps,
            'eta': eta,
            'n_s': ns,
            'running': running,
        })

    return results
