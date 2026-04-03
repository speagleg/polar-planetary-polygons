"""
Jupiter Juno cyclone ring data.

Jupiter's polar regions show rings of cyclones observed by the Juno mission
(Adriani et al. 2018, Nature 555, 216-219):
    South pole: N=5 cyclones surrounding a central cyclone (pentagonal)
    North pole: N=8 cyclones surrounding a central cyclone (octagonal)

NOTE: Early reports varied (N=8 south, N=9 north). The most robust Juno
observations as of PJ40+ show N=5 (south) and N=8 (north). We use these
as the primary values but note the variability.

Sources:
    Adriani et al. 2018, Nature 555, 216-219 (discovery)
    Tabataba-Vakili et al. 2020, Icarus 335, 113405 (dynamics)
    Gavriel & Kaspi 2021, Nature Geoscience 14, 559-563 (stability)
"""

import numpy as np
from dataclasses import dataclass


@dataclass
class JupiterParameters:
    """Fundamental Jupiter physical parameters."""

    # Planet
    rotation_rate: float = 1.7585e-4    # rad/s, sidereal (9h 55m 30s)
    equatorial_radius: float = 7.1492e7  # m
    polar_radius: float = 6.6854e7       # m

    # North polar cyclone ring
    north_N: int = 8                     # number of ring cyclones
    north_latitude: float = 83.0         # degrees N (approximate)
    north_ring_radius: float = 4.0e6     # m (ring radius, from Juno images)
    north_cyclone_radius: float = 2.0e6  # m (individual cyclone radius)
    north_wind_speed: float = 100.0      # m/s (approximate peak azimuthal)

    # South polar cyclone ring
    south_N: int = 5                     # number of ring cyclones
    south_latitude: float = -83.0        # degrees S
    south_ring_radius: float = 5.5e6     # m
    south_cyclone_radius: float = 2.5e6  # m
    south_wind_speed: float = 90.0       # m/s (approximate)

    # Central vortex (both poles have a strong central cyclone)
    central_vortex_present: bool = True
    central_wind_speed: float = 80.0     # m/s (approximate)

    @property
    def north_beta(self) -> float:
        """beta = 2*Omega*cos(phi) / R at north polar latitude."""
        phi = np.radians(self.north_latitude)
        return 2 * self.rotation_rate * np.cos(phi) / self.polar_radius

    @property
    def south_beta(self) -> float:
        """beta at south polar latitude."""
        phi = np.radians(abs(self.south_latitude))
        return 2 * self.rotation_rate * np.cos(phi) / self.polar_radius

    @property
    def north_coriolis_f(self) -> float:
        """f = 2*Omega*sin(phi) at north polar latitude."""
        phi = np.radians(self.north_latitude)
        return 2 * self.rotation_rate * np.sin(phi)

    @property
    def south_coriolis_f(self) -> float:
        phi = np.radians(abs(self.south_latitude))
        return 2 * self.rotation_rate * np.sin(phi)


def rossby_wavenumber_prediction(pole: str = 'north',
                                  params: JupiterParameters = None) -> dict:
    """
    Predict the Rossby-selected wavenumber for Jupiter's polar cyclone ring.

    Uses the same framework as Saturn: U* = beta / k^2, solve for n.

    For Jupiter the "jet" is the ring of cyclones at radius R_ring,
    with azimuthal wavenumber k = n / R_ring.
    """
    if params is None:
        params = JupiterParameters()

    if pole == 'north':
        beta = params.north_beta
        R_ring = params.north_ring_radius
        U_obs = params.north_wind_speed
        N_obs = params.north_N
    else:
        beta = params.south_beta
        R_ring = params.south_ring_radius
        U_obs = params.south_wind_speed
        N_obs = params.south_N

    # Rossby stationarity: U* = beta / k^2 with k = n / R_ring
    # n* = R_ring * sqrt(beta / U_obs)
    n_star = R_ring * np.sqrt(beta / U_obs)

    # Stationary speed for the observed N
    k_obs = N_obs / R_ring
    U_star = beta / k_obs**2 if k_obs > 0 else np.inf

    # Stationary speed for each integer n
    n_range = range(1, 15)
    U_star_table = {}
    for n in n_range:
        k = n / R_ring
        U_star_table[n] = beta / k**2

    # Which n gives U* closest to U_obs?
    best_n = min(n_range, key=lambda n: abs(U_star_table[n] - U_obs))

    return {
        'pole': pole,
        'n_star_continuous': n_star,
        'n_star_integer': round(n_star),
        'n_best_fit': best_n,
        'N_observed': N_obs,
        'U_observed': U_obs,
        'U_star_at_N_obs': U_star,
        'beta': beta,
        'R_ring': R_ring,
        'U_star_table': U_star_table,
        'match': best_n == N_obs,
    }


def thomson_critical_ratio_jupiter(N: int) -> float:
    """
    Compute the Thomson critical central vortex ratio for N cyclones.

    Uses the numerical stability matrix (same as Saturn computation).
    """
    from planetary_polygons.core.universal_selection import kappa_crit
    return float(kappa_crit(N))


def jupiter_convergence_test(params: JupiterParameters = None) -> dict:
    """
    THE KEY TEST: Does the Rossby-selected n match the Thomson-stable N
    for Jupiter, as it does for Saturn?

    If yes: the convergence is universal, not Saturn-specific.
    If no: the convergence may be coincidental.
    """
    if params is None:
        params = JupiterParameters()

    results = {}
    for pole in ['north', 'south']:
        rossby = rossby_wavenumber_prediction(pole, params)
        N_obs = rossby['N_observed']

        # Thomson critical ratio
        try:
            kappa_crit = thomson_critical_ratio_jupiter(N_obs)
        except Exception:
            kappa_crit = None

        results[pole] = {
            'N_observed': N_obs,
            'n_rossby': rossby['n_star_continuous'],
            'n_rossby_integer': rossby['n_star_integer'],
            'n_best_fit': rossby['n_best_fit'],
            'rossby_matches': rossby['match'],
            'U_observed': rossby['U_observed'],
            'U_star': rossby['U_star_at_N_obs'],
            'kappa_crit_thomson': kappa_crit,
        }

    return results


# ---- Juno cyclone position data ----
# Digitised from Adriani et al. 2018 Fig. 2 and Tabataba-Vakili et al. 2020
# Positions are approximate centroids of cyclonic features.

JUNO_NORTH_CYCLONES = {
    'latitudes': np.array([84.2, 83.5, 82.8, 83.1, 84.0, 83.3, 82.9, 83.6]),
    'longitudes': np.array([0, 44, 91, 135, 181, 224, 269, 315]),
    'source': 'Adriani et al. 2018, approximate centroids',
}

JUNO_SOUTH_CYCLONES = {
    'latitudes': np.array([84.5, 83.8, 84.1, 83.6, 84.2]),
    'longitudes': np.array([0, 72, 145, 217, 290]),
    'source': 'Adriani et al. 2018, approximate centroids',
}


def juno_cyclone_positions(pole: str = 'north') -> dict:
    """Return Juno-observed cyclone positions for the given pole."""
    if pole == 'north':
        return JUNO_NORTH_CYCLONES
    return JUNO_SOUTH_CYCLONES


def jupiter_sigma_test(pole: str = 'north') -> dict:
    """
    Compute sigma_geom for Jupiter's cyclone ring.

    THE KEY TEST: Is sigma_geom near 0 (polygon-like)?
    """
    from planetary_polygons.verification.sigma_geometric import sigma_from_positions

    pos = juno_cyclone_positions(pole)
    jupiter = JupiterParameters()

    result = sigma_from_positions(pos['latitudes'], pos['longitudes'], jupiter.polar_radius)
    result['pole'] = pole
    result['source'] = pos['source']
    return result


def jupiter_full_convergence() -> dict:
    """
    Complete convergence test: sigma_geom + Thomson for both poles.
    """
    from planetary_polygons.core.hessian import critical_central_vortex_strength
    from planetary_polygons.core.universal_selection import kappa_crit
    def is_stable(N, kappa_center=0.0):
        return kappa_center >= float(kappa_crit(N))
    critical_center_strength = lambda N: float(kappa_crit(N))

    results = {}
    for pole in ['north', 'south']:
        sigma_result = jupiter_sigma_test(pole)
        N = sigma_result['N']

        stable_no_center = is_stable(N, kappa_center=0.0)
        try:
            kc = critical_center_strength(N)
        except Exception:
            kc = None

        if stable_no_center:
            entry = 'Thomson (stable ring, central vortex shifts boundary)'
        else:
            entry = 'Thomson (ring unstable without center, stabilised by central cyclone)'

        results[pole] = {
            'N': N,
            'sigma_geom': sigma_result['sigma_geom'],
            'r_mobius': sigma_result['r_mobius'],
            'R_ring': sigma_result['R_ring'],
            'stable_no_center': stable_no_center,
            'kappa_crit': kc,
            'entry_mechanism': entry,
        }

    return results
