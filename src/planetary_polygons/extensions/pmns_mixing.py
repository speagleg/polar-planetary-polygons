"""PMNS neutrino mixing from CKM-PMNS complementarity.

The CKM uses the index-3 subgroup QR = {1,2,4} of (Z/7Z)*.
The PMNS uses the index-2 subgroup {1,6} (pairs).
The identity arctan(1/2) + arctan(1/3) = pi/4 connects them.

Predictions:
  theta_12 = pi/4 - theta_C  (complementarity)
  theta_23 = pi/4             (pair symmetry = democratic mixing)
  sin^2(theta_13) = (1/2)*sin^2(theta_C)  (index-2 factor)
  delta_CP = arctan(sqrt(7))  (same Gauss sum as CKM)
"""

from math import pi, sqrt, atan, asin, sin, cos, degrees

from planetary_polygons.extensions.bernoulli_havelock import SIGMA_0, N_CRIT


def complementarity_identity():
    """Verify arctan(1/2) + arctan(1/3) = pi/4.

    Proof: tan(a+b) = (1/2 + 1/3)/(1 - 1/6) = (5/6)/(5/6) = 1 -> a+b = pi/4.
    """
    return abs(atan(0.5) + atan(1.0 / 3) - pi / 4) < 1e-14


def reactor_angle(s12_ckm):
    """sin^2(theta_13^PMNS) = (1/2) * sin^2(theta_C).

    The factor 1/2 comes from the index-2 subgroup (pairs have 2 elements).
    """
    return 0.5 * s12_ckm ** 2


def pmns_angles(s12_ckm=None, sigma=SIGMA_0):
    """PMNS predictions from the Z_7 backbone.

    If s12_ckm not provided, computes it from orbit_ckm.
    """
    if s12_ckm is None:
        from planetary_polygons.extensions.orbit_ckm import ckm_matrix
        result = ckm_matrix(sigma)
        s12_ckm = result['s12']

    N = N_CRIT
    theta_C = asin(s12_ckm)

    # CKM-PMNS complementarity: theta_12 + theta_C = pi/4
    theta_12 = pi / 4 - theta_C

    # Pair symmetry: maximal atmospheric mixing
    theta_23 = pi / 4

    # Reactor angle from index-2 subgroup
    sin2_13 = reactor_angle(s12_ckm)
    theta_13 = asin(sqrt(sin2_13))

    # CP phase from same Gauss sum
    delta_CP = atan(sqrt(N))

    return {
        's12_ckm': s12_ckm,
        'theta_12_rad': theta_12,
        'theta_12_deg': degrees(theta_12),
        'theta_23_rad': theta_23,
        'theta_23_deg': degrees(theta_23),
        'theta_13_rad': theta_13,
        'theta_13_deg': degrees(theta_13),
        'sin2_theta_13': sin2_13,
        'delta_CP_rad': delta_CP,
        'delta_CP_deg': degrees(delta_CP),
    }
