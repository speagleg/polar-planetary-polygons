"""BEC vortex cluster stability. (§6.6)

In Bose-Einstein condensate (BEC) systems, quantised vortex clusters behave
analogously to classical point vortex rings. The stability of an N-vortex
cluster in a BEC is governed by the same Thomson criterion as the classical
problem, but with an additional centrifugal potential term proportional to
the total angular momentum q₀.

Key result (§6.6): For each N, there is a minimum integer angular momentum
q₀_min = max(1, ceil(|κ_crit|)) above which the cluster is stabilised.
The critical coupling κ_crit is the same central-vortex parameter computed
by kappa_crit_sympy in core/hessian.py.

For N=6: κ_crit = -1/4, q₀_min = 1.
For N=8: κ_crit = -1/2, q₀_min = 1.
"""
import numpy as np
from math import ceil


def bec_kappa_crit(N):
    """
    Critical coupling strength for an N-vortex BEC cluster.

    Wraps kappa_crit_sympy and returns the absolute value as a float.
    This is the minimum central vortex strength needed to stabilise the ring.

    Parameters
    ----------
    N : int
        Number of ring vortices.

    Returns
    -------
    float
        |κ_crit(N)| — positive, less than 1 for all N tested.
    """
    from planetary_polygons.core.hessian import kappa_crit_sympy
    return abs(float(kappa_crit_sympy(N)))


def bec_stability_table(N_range=range(5, 10)):
    """
    Stability table for BEC vortex clusters.

    For each N, computes:
      - kappa_crit: the exact critical coupling (negative, from perturbation theory)
      - q0_min: minimum integer angular momentum = max(1, ceil(|kappa_crit|))
      - stable: True (q0_min >= 1 always)

    Parameters
    ----------
    N_range : iterable of int
        N values to compute (default range(5, 10)).

    Returns
    -------
    dict
        Mapping N → {'kappa_crit': float, 'q0_min': int, 'stable': bool}.
    """
    from planetary_polygons.core.hessian import kappa_crit_sympy
    result = {}
    for N in N_range:
        kc = float(kappa_crit_sympy(N))
        kc_abs = abs(kc)
        q0_min = max(1, ceil(kc_abs))
        result[N] = {'kappa_crit': kc, 'q0_min': q0_min, 'stable': q0_min >= 1}
    return result


def bec_frequency_shift(N, q0, omega_rot=1.0):
    """
    Frequency shift of the ring breathing mode due to angular momentum q0.

    In BEC vortex dynamics, the angular momentum quantum number q0 contributes
    a centrifugal frequency shift of q0 / (2π) in units of the trap frequency.

    Parameters
    ----------
    N : int
        Number of ring vortices.
    q0 : int
        Angular momentum quantum number.
    omega_rot : float
        Trap rotation frequency (default 1.0).

    Returns
    -------
    float
        Frequency shift in units of omega_rot.
    """
    return float(q0) / (2 * np.pi) * omega_rot


if __name__ == "__main__":
    for N, d in bec_stability_table().items():
        print(f"N={N}: kc={d['kappa_crit']:.4f}, q0_min={d['q0_min']}")
