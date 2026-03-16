"""
Generalised geometric sigma observable for N features on a ring.

Given N points (vortex centers, jet vertices, or cyclone positions) arranged
approximately on a ring, sigma_geom measures how much the configuration
deviates from a perfect regular N-gon.

    sigma_geom = 0: perfect polygon (|lambda| = 1 in Mobius space)
    sigma_geom > 0: distorted polygon or spiral (|lambda| > 1)

The observable is:
    sigma_geom = (1/N) * sum_k |ln|z_k / z_k^ideal||

where z_k^ideal are the vertices of the best-fit regular N-gon.
This is rotation-invariant and scale-invariant by construction.

Works for ANY N: hexagons (Saturn, N=6), octagons (Jupiter north, N=8),
pentagons (Jupiter south, N=5), etc.
"""

import numpy as np
from scipy.optimize import minimize_scalar


def sigma_geom(z: np.ndarray) -> float:
    """
    Compute the geometric sigma for N complex positions.

    sigma_geom = (1/N) * sum |ln|z_k / z_k^ideal||

    where z_k^ideal is the best-fit regular N-gon (same mean radius,
    optimal rotation to minimise sigma).

    Parameters
    ----------
    z : np.ndarray
        Complex positions of N features.

    Returns
    -------
    float
        sigma_geom >= 0. Zero for a perfect regular N-gon.
    """
    N = len(z)
    if N < 3:
        return 0.0

    radii = np.abs(z)
    R_mean = np.mean(radii)
    if R_mean < 1e-30:
        return 0.0

    z_norm = z / R_mean

    def sigma_at_phi(phi):
        z_ideal = np.exp(2j * np.pi * np.arange(N) / N + 1j * phi)
        log_ratios = _matched_log_ratios(z_norm, z_ideal)
        return np.mean(np.abs(log_ratios))

    result = minimize_scalar(sigma_at_phi, bounds=(-np.pi, np.pi),
                              method='bounded')
    return float(result.fun)


def _matched_log_ratios(z_actual: np.ndarray, z_ideal: np.ndarray) -> np.ndarray:
    """
    Match actual positions to ideal vertices (allowing cyclic permutation)
    and return ln|z_actual / z_ideal| for the best matching.
    """
    N = len(z_actual)
    best_ratios = None
    best_total = np.inf
    for shift in range(N):
        z_shifted = np.roll(z_ideal, shift)
        ratios = np.log(np.abs(z_actual) / np.abs(z_shifted))
        total = np.sum(np.abs(ratios))
        if total < best_total:
            best_total = total
            best_ratios = ratios
    return best_ratios


def sigma_from_positions(latitudes: np.ndarray, longitudes: np.ndarray,
                          R_planet: float) -> dict:
    """
    Compute sigma_geom from (latitude, longitude) positions on a sphere.

    Converts to stereographic projection (complex plane) centered on the pole,
    then computes sigma_geom.

    Parameters
    ----------
    latitudes : np.ndarray
        Planetographic latitudes in degrees (positive = north).
    longitudes : np.ndarray
        Longitudes in degrees.
    R_planet : float
        Planetary radius in meters.

    Returns
    -------
    dict with 'sigma_geom', 'N', 'R_ring', 'z_stereo', 'r_mobius'.
    """
    N = len(latitudes)

    lat_rad = np.radians(np.abs(latitudes))
    lon_rad = np.radians(longitudes)
    r_stereo = R_planet * np.tan(np.pi / 4 - lat_rad / 2)
    z = r_stereo * np.exp(1j * lon_rad)

    sig = sigma_geom(z)
    R_ring = np.mean(np.abs(z))

    return {
        'sigma_geom': sig,
        'N': N,
        'R_ring': R_ring,
        'z_stereo': z,
        'r_mobius': np.exp(sig),
    }
