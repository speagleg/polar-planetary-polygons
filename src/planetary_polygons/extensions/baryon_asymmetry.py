"""Baryon asymmetry: eta_B = J * K^C(N-1,2) / N.

The formula combines:
  J = Jarlskog invariant (from CKM backbone, CP violation)
  K^15 = K^C(6,2) (instanton suppression per mass matrix entry)
  1/N = fractional baryon number from Z_7 orbifold

C(N-1, 2) = 15 = number of independent off-diagonal entries
in the 6x6 mass matrix of the N-1 nontrivial Z_7 modes.
"""

from math import comb

from planetary_polygons.extensions.bernoulli_havelock import (
    SIGMA_0, N_CRIT, instanton_fugacity,
)

N = N_CRIT
ETA_B_OBS = 6.12e-10  # Planck 2018


def instanton_power(N_val=N):
    """C(N-1, 2) = (N-1)(N-2)/2 = 15 at N=7."""
    return comb(N_val - 1, 2)


def eta_B(J=None, K=None, N_val=N, sigma=SIGMA_0):
    """Baryon asymmetry: eta_B = J * K^{C(N-1,2)} / N."""
    if K is None:
        K = instanton_fugacity(N_val)
    if J is None:
        from planetary_polygons.extensions.orbit_ckm import ckm_matrix
        result = ckm_matrix(sigma)
        J = result['J']

    power = instanton_power(N_val)
    return J * K ** power / N_val


def full_prediction(sigma_0=SIGMA_0):
    """Complete baryon asymmetry with all intermediate values."""
    from planetary_polygons.extensions.orbit_ckm import ckm_matrix
    result = ckm_matrix(sigma_0)
    J = result['J']
    K = result['K']
    power = instanton_power()
    prediction = J * K ** power / N

    return {
        'J': J,
        'K': K,
        'power': power,
        'eta_B': prediction,
        'eta_obs': ETA_B_OBS,
        'match_pct': (prediction / ETA_B_OBS - 1) * 100,
    }
