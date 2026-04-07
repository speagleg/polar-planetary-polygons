r"""
CS coupling constants and Weinberg angle.

    1/g²(G) = k + h∨(G),  k=1 (Hopf Euler class).
    sin²θ_W = h_Y/(h_Y+h_W) = 3/11 (WZW conformal weights, Paper IV §8).
"""

from math import pi, sqrt
from fractions import Fraction


# Dual Coxeter numbers
DUAL_COXETER = {
    'E8': 30, 'E7': 18, 'E6': 12,
    'SU(3)': 3, 'SU(2)': 2, 'U(1)': 0,
    'SO(10)': 8, 'SU(5)': 5,
}

# Group dimensions
GROUP_DIM = {
    'E8': 248, 'E7': 133, 'E6': 78,
    'SU(3)': 8, 'SU(2)': 3, 'U(1)': 1,
    'SO(10)': 45, 'SU(5)': 24,
}


def cs_inverse_coupling(group, k=1):
    """Chern-Simons inverse coupling: 1/g² = k + h∨(G).

    This is the one-loop exact result for non-abelian CS theory.
    For U(1), h∨ = 0 so 1/g² = k (the bare level).
    """
    return k + DUAL_COXETER[group]


def wzw_central_charge(group, k=1):
    """WZW central charge: c = k × dim(G) / (k + h∨(G))."""
    return k * GROUP_DIM[group] / (k + DUAL_COXETER[group])


def weinberg_angle_cs():
    """sin²θ_W = h_Y/(h_Y+h_W) = (1/4)/(11/12) = 3/11.

    h_W = j(j+1)/(k+h∨) = 2/3 (SU(2)₁, j=1), h_Y = Q²/k_Y = 1/4 (Q=1/2, k_Y=1).
    See Paper IV §8 for the full derivation.
    """
    h_W = Fraction(2, 3)    # j(j+1)/(k+h∨) = 2/3 for SU(2)₁ adjoint
    h_Y = Fraction(1, 4)    # Q²/k_Y = (1/2)²/1 = 1/4 for k_Y=1

    sin2_theta = h_Y / (h_Y + h_W)  # = (1/4)/(11/12) = 3/11
    return float(sin2_theta)


def e8_to_sm_coupling_reduction():
    """Coupling constant reduction from E₈ to SM at the K=0 transition.

    Returns dict with all coupling data.
    """
    # E₈ regime (K > 0)
    e8_inv_g2 = cs_inverse_coupling('E8')
    e8_central_charge = wzw_central_charge('E8')

    # SM regime (K = 0)
    su3_inv_g2 = cs_inverse_coupling('SU(3)')
    su2_inv_g2 = cs_inverse_coupling('SU(2)')
    u1_level = Fraction(1, 1)  # k_Y = 1 (compact boson, single-valued holonomy)

    sin2_theta = weinberg_angle_cs()

    return {
        # E₈ data
        'e8_level': 1,
        'e8_dual_coxeter': DUAL_COXETER['E8'],
        'e8_inverse_coupling': e8_inv_g2,
        'e8_central_charge': e8_central_charge,
        'e8_c_is_8': abs(e8_central_charge - 8.0) < 1e-10,

        # SM data
        'sm_level': 1,
        'su3_inverse_coupling': su3_inv_g2,
        'su2_inverse_coupling': su2_inv_g2,
        'u1_level': float(u1_level),
        'weinberg_angle': sin2_theta,
        'weinberg_exact': '3/11',

        # The bridge
        'level_preserved': True,
        'coupling_split': '31 → (4, 3, K_Y=1/2)',
    }
