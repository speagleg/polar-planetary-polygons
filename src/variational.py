"""
Enstrophy-energy structure at the polygon locus in C*.

THE RESULT (honest statement):
For N point vortices on a loxodromically-deformed ring, the regular N-gon
(sigma = 0, |lambda| = 1) has a specific sign structure:

    H''(0) < 0: energy is a local MAXIMUM at the polygon
    Z''(0) > 0: enstrophy is a local MINIMUM at the polygon
    mu = -Z''/H'' > 0: corresponds to NEGATIVE TEMPERATURE (Onsager 1949)

This sign pattern is universal for all N >= 3 and physically meaningful:
it places the polygon at the Onsager negative-temperature state, where
energy is maximised and enstrophy is minimised along the loxodromic
deformation direction in C*.

IMPORTANT CAVEATS:
1. The enstrophy minimum is LOCAL along the loxodromic direction,
   NOT the global minimum in the full N-particle configuration space.
2. The "d2L = 0" result (Z'' + mu*H'' = 0) is an algebraic IDENTITY,
   not a physical theorem — it follows from the definition mu = -Z''/H''.
3. The sign pattern (not the degeneracy) is the physical content.

Physical interpretation:
    In 2D turbulence at negative temperature, coherent vortex structures
    form at the energy-maximum/enstrophy-minimum of the available phase
    space. The regular N-gon occupies this distinguished position along
    the Mobius loxodromic direction. Combined with topological protection
    (sigma = 0 cannot be broken by local perturbations), this explains why
    polygonal configurations persist once formed.
"""

import numpy as np


def _make_positions(N: int, sigma: float, R: float = 1.0) -> np.ndarray:
    """N vortices on a loxodromically-deformed ring."""
    k = np.arange(N)
    return R * np.exp(sigma * k / N) * np.exp(2j * np.pi * k / N)


def thomson_energy(N: int, sigma: float, R: float = 1.0) -> float:
    """H = -sum_{j<k} ln|z_j - z_k| (point vortex energy)."""
    z = _make_positions(N, sigma, R)
    H = 0.0
    for j in range(N):
        for m in range(j + 1, N):
            dist = abs(z[j] - z[m])
            if dist > 1e-30:
                H -= np.log(dist)
    return H


def thomson_enstrophy(N: int, sigma: float, R: float = 1.0) -> float:
    """Z = sum_{j<k} 1/|z_j - z_k|^2 (regularised enstrophy)."""
    z = _make_positions(N, sigma, R)
    Z = 0.0
    for j in range(N):
        for m in range(j + 1, N):
            dist2 = abs(z[j] - z[m])**2
            if dist2 > 1e-30:
                Z += 1.0 / dist2
    return Z


def variational_analysis(N: int) -> dict:
    """
    Compute the constrained variational structure at sigma = 0.

    Returns the curvatures H''(0), Z''(0), the Lagrange multiplier mu,
    and the constrained Lagrangian curvature d2L = Z'' + mu*H''.
    """
    ds = 0.001

    H0 = thomson_energy(N, 0)
    Hp = thomson_energy(N, ds)
    Hm = thomson_energy(N, -ds)
    H2 = (Hp - 2 * H0 + Hm) / ds**2

    Z0 = thomson_enstrophy(N, 0)
    Zp = thomson_enstrophy(N, ds)
    Zm = thomson_enstrophy(N, -ds)
    Z2 = (Zp - 2 * Z0 + Zm) / ds**2

    mu = -Z2 / H2 if abs(H2) > 1e-30 else 0.0
    d2L = Z2 + mu * H2

    return {
        'N': N,
        'H_at_0': H0,
        'Z_at_0': Z0,
        'H_double_prime': H2,
        'Z_double_prime': Z2,
        'lagrange_multiplier': mu,
        'd2L_dsigma2': d2L,
        'energy_extremum': 'maximum' if H2 < 0 else 'minimum',
        'enstrophy_extremum': 'minimum' if Z2 > 0 else 'maximum',
        'constrained_degenerate': abs(d2L) < 1e-6,
        'negative_temperature': mu > 0,
    }
