"""
Jupiter verification: test the Mobius framework on Juno cyclone data.

The key question: do Jupiter's cyclone rings sit at |lambda| ~ 1,
confirming the Mobius framework is universal across planets?
"""

import numpy as np
from planetary_polygons.data.jupiter import (
    JupiterParameters, jupiter_full_convergence,
    rossby_wavenumber_prediction,
)


def verify_jupiter_convergence(verbose: bool = True) -> dict:
    """Full Jupiter convergence test with comparison to Saturn."""
    result = jupiter_full_convergence()

    if verbose:
        print("=" * 65)
        print("JUPITER CONVERGENCE TEST: Is |lambda|=1 universal?")
        print("=" * 65)

        for pole in ['north', 'south']:
            r = result[pole]
            print(f"\n  {pole.upper()} POLE (N = {r['N']}):")
            print(f"    sigma_geom = {r['sigma_geom']:.4f}")
            print(f"    r = exp(sigma) = {r['r_mobius']:.4f}")
            print(f"    |r - 1| = {abs(r['r_mobius'] - 1):.4f}")
            print(f"    Thomson stable (no center): {r['stable_no_center']}")
            if r['kappa_crit'] is not None:
                print(f"    kappa_crit = {r['kappa_crit']:.4f}")
            print(f"    Entry mechanism: {r['entry_mechanism']}")

        print(f"\n  ROSSBY TEST (known to fail for Jupiter):")
        for pole in ['north', 'south']:
            rossby = rossby_wavenumber_prediction(pole)
            print(f"    {pole}: n* = {rossby['n_star_continuous']:.2f} "
                  f"(observed N = {rossby['N_observed']}, match = {rossby['match']})")

        print(f"\n  SATURN COMPARISON:")
        print(f"    Saturn: Rossby + Thomson converge at n=6, sigma~0.5")
        print(f"    Jupiter: Thomson only (Rossby fails), sigma from geometry")

        north_near_1 = abs(result['north']['r_mobius'] - 1) < 0.5
        south_near_1 = abs(result['south']['r_mobius'] - 1) < 0.5
        print(f"\n  VERDICT:")
        print(f"    North |lambda|~1? {north_near_1} (sigma={result['north']['sigma_geom']:.4f})")
        print(f"    South |lambda|~1? {south_near_1} (sigma={result['south']['sigma_geom']:.4f})")
        if north_near_1 and south_near_1:
            print(f"    => |lambda|=1 IS universal across planets and mechanisms")
        else:
            print(f"    => Results require further analysis")

    result['north_near_1'] = abs(result['north']['r_mobius'] - 1) < 0.5
    result['south_near_1'] = abs(result['south']['r_mobius'] - 1) < 0.5
    return result


def jupiter_timescale_ratio(verbose: bool = True) -> dict:
    """
    Injection-to-restoring timescale ratio for Jupiter's N=8 polar cyclone ring.

    Uses Juno (Adriani et al. 2018) observed parameters. A ratio >> 1 supports
    dynamical maintenance of the ring against dissipation.

    Physical picture:
    - Restoring: ring oscillates at ω_osc = sqrt(λ_eff) * Ω_ring
    - Injection: tropospheric heat flux (7.5 W/m²) replenishes kinetic energy
    - Ratio τ_inject/τ_restore >> 1 means the ring is easy to maintain

    Returns
    -------
    dict with keys: T_orb_days, tau_restore_days, tau_inject_days, ratio,
                    R_ring_m, kappa_m2s
    """
    N = 8
    r_cyc = 2.5e6      # cyclone radius, m (Adriani 2018)
    V_max = 100.0      # peak wind, m/s
    lat = np.radians(84)  # ring latitude
    R_J = 71492e3      # Jupiter equatorial radius, m

    R_ring = R_J * np.cos(lat)
    kappa = 2 * np.pi * r_cyc * V_max  # circulation per cyclone
    A_cyc = np.pi * r_cyc**2

    # Orbital period of the ring
    Omega = kappa * (N - 1) / (4 * np.pi * R_ring**2)
    T_orb = 2 * np.pi / Omega

    # Restoring timescale: 1/ω_osc, λ_eff ≈ 3 (central estimate with κ₀/κ=1)
    lam_eff = 3.0
    omega_osc = np.sqrt(lam_eff) * Omega
    tau_restore = 1.0 / omega_osc

    # Injection timescale: tropospheric KE / interior heat flux power
    F_heat = 7.5      # W/m², Jupiter interior heat flux
    rho_tropo = 0.2   # kg/m³
    H_tropo = 40e3    # m, effective tropospheric depth
    E_KE = 0.5 * rho_tropo * H_tropo * A_cyc * V_max**2
    P_inject = F_heat * A_cyc
    tau_inject = E_KE / P_inject

    ratio = tau_inject / tau_restore

    result = {
        'R_ring_m': R_ring,
        'kappa_m2s': kappa,
        'T_orb_days': T_orb / 86400,
        'tau_restore_days': tau_restore / 86400,
        'tau_inject_days': tau_inject / 86400,
        'ratio': ratio,
        'lam_eff': lam_eff,
    }

    if verbose:
        print(f"Ring radius:               {R_ring/1e6:.2f} × 10⁶ m")
        print(f"Circulation κ:             {kappa:.3e} m²/s")
        print(f"Orbital period T_orb:      {result['T_orb_days']:.1f} days")
        print(f"Restoring τ (λ_eff={lam_eff:.0f}): {result['tau_restore_days']:.1f} days")
        print(f"Injection τ (tropo):       {result['tau_inject_days']:.0f} days")
        print(f"Ratio τ_inject/τ_restore:  {ratio:.0f}")

    return result
