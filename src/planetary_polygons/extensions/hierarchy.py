r"""
The electroweak hierarchy from the hybrid instanton.

THEOREM: The Planck/electroweak hierarchy decomposes as

  ln(M_P / M_EW) = 2S_BO(7) + Δε × ln(ε₇) + (1/2) ln(c/(24π²))
                  = [instanton] + [mass gap]    + [gravity prefactor]
                  = 36.548      + 2.224         + (-0.313)
                  = 38.459      (observed: 38.442, log match 0.04%)

The three components:

1. INSTANTON (2S_BO): the tunneling bounce action through the
   Born-Oppenheimer potential of the N=7 breathing mode.
   V_BO(ρ) = log(2sinh ρ) + b(7) - f(3,7).
   The bounce goes from ρ=0 (UV, flat plane) to ρ* (IR, threshold)
   and back: S_bounce = 2 × S_tunnel.

2. MASS GAP (Δε × ln ε₇): the WDW zero-point energy contribution.
   Δε = 0.8031 is the exact WDW ground-state eigenvalue gap
   (computed numerically in mass_gap.py; asymptotic value √(2/π) =
   0.7979 differs by 0.65%).
   This is the QUANTUM correction to the classical instanton.

3. GRAVITY PREFACTOR ((1/2)ln(c/(24π²))): the 4D Planck mass in polygon
   units from Brown-Henneaux (c = 3ℓ/(2G)) + KK reduction (G₄ = 2πRG₃).

PREDICTIONS:
  v = 242.0 GeV (observed: 246.2 GeV, 1.7% off; residual is
  the O(1/c²) Dunham correction)

The hierarchy is ~10^17 because N_grav = 7 is the FIRST non-trivial
solution of the Pell equation N² - 2(2j+1)² = -1. The next solution
(N=41) would give hierarchy ~10^99 — no atoms possible.
"""

from math import sqrt, log, exp, pi, sinh


# Algebraic constants
EPSILON_7 = 8 + 3 * sqrt(7)     # fundamental unit of Z[√7]
EPSILON_2 = 1 + sqrt(2)          # fundamental unit of Z[√2]
MASS_GAP_ASYMP = sqrt(2 / pi)    # = 0.79788... (WDW asymptotic)
MASS_GAP_EXACT = 0.8031           # numerical WDW ground-state eigenvalue

# Physical constants
M_PLANCK = 1.22089e19   # GeV
V_HIGGS = 246.22         # GeV
M_P_OVER_MEW = M_PLANCK / V_HIGGS


def b_exact(N):
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


def central_charge(N):
    return 12 * b_exact(N)


def V_BO(rho, N):
    """Born-Oppenheimer potential for the breathing mode."""
    if rho < 1e-15:
        return -50.0
    mc = N // 2
    fc = mc * (N - mc) / 2.0
    return log(2 * sinh(rho)) + b_exact(N) - fc


def find_threshold_BO(N):
    """Find ρ* where V_BO(ρ*) = 0 by bisection."""
    lo, hi = 0.01, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if V_BO(mid, N) < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def tunneling_action(N, c_val=None, n_steps=500000):
    """Compute the WKB tunneling action through the BO potential.

    S = ∫₀^{ρ*} √(2c|V_BO(ρ)|) dρ

    Returns S (one-way tunneling, NOT the bounce).
    """
    if c_val is None:
        c_val = central_charge(N)
    rho_star = find_threshold_BO(N)
    drho = rho_star / n_steps
    S = 0.0
    for i in range(1, n_steps):
        rho = i * drho
        V = V_BO(rho, N)
        if V < 0:
            S += sqrt(2 * c_val * abs(V)) * drho
    return S


def hierarchy_decomposition(N_grav=7, N_cosmo=11):
    """The three-component hierarchy decomposition.

    ln(M_P/M_EW) = 2S_BO(N_grav) + √(2/π)×ln(ε₇) + (1/2)ln(c/(24π²))

    Returns dict with all components and verification.
    """
    c_grav = central_charge(N_grav)
    c_cosmo = central_charge(N_cosmo)

    # Component 1: instanton bounce action
    S_tunnel = tunneling_action(N_grav, c_grav)
    S_bounce = 2 * S_tunnel

    # Component 2: mass gap × ln(ε₇) (exact WDW eigenvalue)
    mass_gap_term = MASS_GAP_EXACT * log(EPSILON_7)

    # Component 3: gravitational prefactor
    gravity_term = 0.5 * log(c_cosmo / (24 * pi**2))

    # Total
    total_log = S_bounce + mass_gap_term + gravity_term
    observed_log = log(M_P_OVER_MEW)

    # Predictions
    hierarchy_pred = exp(total_log)
    v_pred = M_PLANCK / hierarchy_pred

    # The key identity: 2S + ΔE×ln(ε₇) = 14×ln(ε₇)?
    pell_sum = S_bounce + mass_gap_term
    pell_target = 2 * N_grav * log(EPSILON_7)

    return {
        # The three components
        'S_bounce': S_bounce,
        'mass_gap_term': mass_gap_term,
        'gravity_term': gravity_term,
        'total_log': total_log,
        'observed_log': observed_log,
        # Match quality
        'log_match_pct': abs(total_log - observed_log) / observed_log * 100,
        'hierarchy_predicted': hierarchy_pred,
        'hierarchy_observed': M_P_OVER_MEW,
        'ratio_match_pct': abs(hierarchy_pred / M_P_OVER_MEW - 1) * 100,
        # Higgs VEV prediction
        'v_predicted': v_pred,
        'v_observed': V_HIGGS,
        'v_match_pct': abs(v_pred - V_HIGGS) / V_HIGGS * 100,
        # The Pell identity
        'pell_sum': pell_sum,
        'pell_target': pell_target,
        'pell_match_pct': abs(pell_sum - pell_target) / pell_target * 100,
        # Fractional contributions
        'instanton_fraction': S_bounce / pell_target,
        'mass_gap_fraction': mass_gap_term / pell_target,
        # Parameters used
        'N_grav': N_grav,
        'N_cosmo': N_cosmo,
        'c_grav': c_grav,
        'c_cosmo': c_cosmo,
        'mass_gap_exact': MASS_GAP_EXACT,
        'mass_gap_asymp': MASS_GAP_ASYMP,
        'epsilon_7': EPSILON_7,
    }


def why_10_to_17():
    """Why the hierarchy is ~10^17 and not larger."""
    results = []
    x, y = 1, 1
    for i in range(6):
        j = (y - 1) // 2
        if x > 1:
            log10_h = 2 * x * log(EPSILON_7) / log(10)
            results.append({
                'N_grav': x,
                'j': j,
                'log10': log10_h,
                'viable': log10_h < 25,
            })
        x_new = 3 * x + 4 * y
        y_new = 2 * x + 3 * y
        x, y = x_new, y_new
    return results


def pi_bridge():
    """The near-identity (1+√2)^π ≈ 8+3√7 (0.026% match)."""
    eps2_pi = EPSILON_2 ** pi
    return {
        'eps2_to_pi': eps2_pi,
        'eps7': EPSILON_7,
        'match_pct': abs(eps2_pi - EPSILON_7) / EPSILON_7 * 100,
        '2pi_N_grav': 2 * pi * 7,
        'N_EW_times_N_cosmo': 4 * 11,
    }
