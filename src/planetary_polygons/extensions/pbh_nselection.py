"""
Primordial black holes from the N-selection phase transition.

The N-selection transition (symmetric → N=11 polygon) is first-order:
  v_N/T_N = √(2 S_BO(11)/c₁₁) = 1.27
  T_N ~ M_poly ≈ 300 TeV
  α ≈ (v_N/T_N)² × (latent heat factor) > 1  (strong)

Bubble collisions during this transition can produce PBHs.
The characteristic mass is set by the horizon mass at T_N:
  M_H(T) ≈ (4π/3) × M_P²/H(T)

At T = 300 TeV: M_PBH ~ 10⁻¹⁶ M☉ (asteroid-mass range).

These are too light for galaxy seeds but are in the
observationally interesting range for PBH dark matter
(not excluded by microlensing).

The EWPT transition at T ~ 100 GeV gives heavier PBHs
(M ~ 10⁻¹⁰ M☉, sub-lunar) but with weaker strength
(v/T_c = 0.84 < 1).
"""

import numpy as np
from math import pi, log, sqrt, exp


# =====================================================================
# Physical constants (natural units: c = ħ = k_B = 1)
# =====================================================================

M_P_GEV = 1.2209e19           # Planck mass in GeV
M_SUN_GEV = 1.116e57          # Solar mass in GeV
M_SUN_KG = 1.989e30           # Solar mass in kg
GEV_TO_KG = 1.783e-27         # 1 GeV = 1.783 × 10⁻²⁷ kg
G_STAR_SM = 106.75            # SM effective relativistic DOFs


# =====================================================================
# PART 1: Horizon mass at temperature T
# =====================================================================

def hubble_rate(T_gev, g_star=G_STAR_SM):
    """Hubble rate H(T) in the radiation era.

    H = √(8π³ g*/90) × T²/M_P
    """
    return sqrt(8 * pi**3 * g_star / 90) * T_gev**2 / M_P_GEV


def horizon_mass_gev(T_gev, g_star=G_STAR_SM):
    """Horizon mass M_H(T) in GeV.

    M_H = (4π/3) × ρ × (1/H)³ = M_P² / H
    (using ρ = 3H²M_P²/(8π) and volume = 4π/(3H³))

    Simplified: M_H = M_P² × √(90/(8π³g*)) / T²
    """
    H = hubble_rate(T_gev, g_star)
    return M_P_GEV**2 / H


def horizon_mass_solar(T_gev, g_star=G_STAR_SM):
    """Horizon mass in solar masses."""
    return horizon_mass_gev(T_gev, g_star) / M_SUN_GEV


def horizon_mass_kg(T_gev, g_star=G_STAR_SM):
    """Horizon mass in kg."""
    return horizon_mass_gev(T_gev, g_star) * GEV_TO_KG


# =====================================================================
# PART 2: N-selection transition parameters
# =====================================================================

def b_exact(N):
    from math import log
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


def nselection_parameters():
    """Parameters of the N-selection phase transition.

    From Paper V:
      v_N/T_N = √(2 S_BO(11)/c₁₁) = √(204.5/126.6) = 1.27
      T_N ~ M_poly ≈ 300 TeV
      2S_BO(11) = 204.5
      c₁₁ = 12 × b(11) = 126.56
    """
    c_11 = 12 * b_exact(11)
    two_S_BO = 204.5  # from Paper V eq.
    v_over_T = sqrt(two_S_BO / c_11)

    T_N_tev = 300.0  # TeV
    T_N_gev = T_N_tev * 1e3  # GeV

    # Phase transition strength parameter α
    # For a strong transition: α ≈ 30/(24π²) × (v/T)² × g_eff
    # Simple estimate: α ≈ (v/T)² / 4 for a generic quartic potential
    alpha = v_over_T**2 / 4  # ≈ 0.4 (moderately strong)

    # More precise: latent heat / radiation density
    # L = (T dΔp/dT - Δp)|_{T_c} ≈ ΔV(T_c) for strong transitions
    # α = L / ρ_rad = L / (π²g*/30 T⁴)
    # For v/T = 1.27: α ~ 0.3-0.5 (model-dependent)

    return {
        'c_11': c_11,
        'two_S_BO': two_S_BO,
        'S_BO': two_S_BO / 2,
        'v_over_T': v_over_T,
        'T_N_gev': T_N_gev,
        'T_N_tev': T_N_tev,
        'alpha': alpha,
    }


def ewpt_parameters():
    """Parameters of the electroweak phase transition.

    From Paper V:
      v/T_c = 0.84
      T_c ~ 100 GeV (electroweak scale)
      2S_BO(7) = 36.548
    """
    c_7 = 12 * b_exact(7)
    two_S_BO = 36.548
    v_over_T = 0.84
    T_c_gev = 100.0

    alpha = v_over_T**2 / 4  # ≈ 0.18

    return {
        'c_7': c_7,
        'two_S_BO': two_S_BO,
        'S_BO': two_S_BO / 2,
        'v_over_T': v_over_T,
        'T_c_gev': T_c_gev,
        'alpha': alpha,
    }


# =====================================================================
# PART 3: PBH mass estimates
# =====================================================================

def pbh_mass_estimate(T_gev, alpha, beta_over_H=10.0, gamma=0.2):
    """Estimate PBH mass from a first-order phase transition.

    M_PBH ≈ γ × M_H × min(1, (H/β)³)

    γ: gravitational collapse efficiency (0.01-0.2)
    β/H: inverse duration (larger = shorter transition = smaller PBHs)
    α: transition strength (larger = more energy in bubble walls)

    For β/H ~ 10 and γ ~ 0.2:
    M_PBH ≈ 0.2 × M_H × 10⁻³ = 2 × 10⁻⁴ M_H
    """
    M_H = horizon_mass_gev(T_gev)
    collapse_fraction = min(1.0, (1.0 / beta_over_H)**3)
    M_PBH = gamma * M_H * collapse_fraction

    return {
        'M_H_gev': M_H,
        'M_H_solar': M_H / M_SUN_GEV,
        'M_H_kg': M_H * GEV_TO_KG,
        'M_PBH_gev': M_PBH,
        'M_PBH_solar': M_PBH / M_SUN_GEV,
        'M_PBH_kg': M_PBH * GEV_TO_KG,
        'gamma': gamma,
        'beta_over_H': beta_over_H,
        'collapse_fraction': collapse_fraction,
    }


def pbh_from_nselection(beta_over_H=10.0, gamma=0.2):
    """PBH mass from the N-selection transition."""
    params = nselection_parameters()
    return pbh_mass_estimate(params['T_N_gev'], params['alpha'],
                             beta_over_H, gamma)


def pbh_from_ewpt(beta_over_H=10.0, gamma=0.2):
    """PBH mass from the EWPT."""
    params = ewpt_parameters()
    return pbh_mass_estimate(params['T_c_gev'], params['alpha'],
                             beta_over_H, gamma)


# =====================================================================
# PART 4: PBH abundance and observational constraints
# =====================================================================

def pbh_abundance_fraction(alpha, beta_over_H):
    """Rough estimate of PBH fraction of dark matter.

    f_PBH = Ω_PBH / Ω_DM

    For bubble collision mechanism:
    f_PBH ~ min(1, α² / (β/H)⁴) × (efficiency factors)

    This is highly model-dependent. We compute the parametric scaling.
    """
    f_raw = alpha**2 / beta_over_H**4
    return min(1.0, f_raw)


def observational_window():
    """PBH mass ranges and observational constraints.

    Returns dict mapping mass ranges to constraint status.
    """
    return {
        'asteroid': {
            'mass_range_solar': (1e-17, 1e-12),
            'mass_range_kg': (2e13, 2e18),
            'constraint': 'weakly constrained; possible DM candidate',
            'probes': ['femtolensing', 'neutron star capture', 'GW'],
        },
        'sub_lunar': {
            'mass_range_solar': (1e-12, 1e-7),
            'mass_range_kg': (2e18, 2e23),
            'constraint': 'microlensing (EROS, Subaru)',
            'probes': ['microlensing', 'dynamical capture'],
        },
        'stellar': {
            'mass_range_solar': (1e-1, 1e2),
            'mass_range_kg': (2e29, 2e32),
            'constraint': 'LIGO/Virgo mergers, microlensing (OGLE)',
            'probes': ['GW mergers', 'microlensing', 'CMB μ-distortion'],
        },
    }


# =====================================================================
# PART 5: Full comparison table
# =====================================================================

def pbh_comparison_table():
    """Compare PBH predictions from both transitions.

    Returns list of dicts with transition name, T, M_H, M_PBH, etc.
    """
    ns = nselection_parameters()
    ew = ewpt_parameters()

    results = []

    for name, T, alpha, v_T in [
        ('N-selection', ns['T_N_gev'], ns['alpha'], ns['v_over_T']),
        ('EWPT', ew['T_c_gev'], ew['alpha'], ew['v_over_T']),
    ]:
        for beta_H in [5, 10, 50]:
            pbh = pbh_mass_estimate(T, alpha, beta_H)
            results.append({
                'transition': name,
                'T_gev': T,
                'v_over_T': v_T,
                'alpha': alpha,
                'beta_over_H': beta_H,
                'M_H_solar': pbh['M_H_solar'],
                'M_PBH_solar': pbh['M_PBH_solar'],
                'M_PBH_kg': pbh['M_PBH_kg'],
                'f_PBH': pbh_abundance_fraction(alpha, beta_H),
            })

    return results


def summary():
    """Print the full PBH prediction summary."""
    ns = nselection_parameters()
    ew = ewpt_parameters()

    print("N-selection transition:")
    print(f"  T = {ns['T_N_tev']:.0f} TeV, v/T = {ns['v_over_T']:.2f}")
    print(f"  S_BO = {ns['S_BO']:.1f}, c₁₁ = {ns['c_11']:.2f}")
    print(f"  M_H = {horizon_mass_solar(ns['T_N_gev']):.2e} M☉")
    print(f"       = {horizon_mass_kg(ns['T_N_gev']):.2e} kg")

    print("\nEWPT:")
    print(f"  T = {ew['T_c_gev']:.0f} GeV, v/T = {ew['v_over_T']:.2f}")
    print(f"  M_H = {horizon_mass_solar(ew['T_c_gev']):.2e} M☉")
    print(f"       = {horizon_mass_kg(ew['T_c_gev']):.2e} kg")

    print("\nPBH mass estimates (γ=0.2):")
    for row in pbh_comparison_table():
        print(f"  {row['transition']:12s} β/H={row['beta_over_H']:2d}  "
              f"M_PBH={row['M_PBH_solar']:.1e} M☉  "
              f"= {row['M_PBH_kg']:.1e} kg  "
              f"f_PBH~{row['f_PBH']:.1e}")
