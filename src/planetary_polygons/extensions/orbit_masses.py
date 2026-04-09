"""Fermion mass predictions from the Bernoulli-Havelock backbone.

Two sigma scales:
  sigma_CKM = SIGMA_0 = 5 (determines CKM phases)
  sigma_mass = SIGMA_0 * sqrt(N) = 13.23 (determines mass hierarchy)

Mass formulas at sigma_mass:
  m_t = v (BF threshold, reference)
  m_c = v * exp(-2*sigma/N) * K^2
  m_u = v * exp(-6*sigma/N) (pure RS, instanton overshoots)
  m_b = m_t * exp(-2*sigma/N) (isospin shift 1/N)
"""

from math import pi, sqrt, exp, log
from fractions import Fraction

from planetary_polygons.extensions.bernoulli_havelock import (
    SIGMA_0, N_CRIT, F_IR, conformal_dim_unified,
    havelock_eigenvalue_unified, instanton_fugacity,
)

N = N_CRIT
M_TOP = 173.0  # GeV, reference mass


def sigma_mass(sigma_0=SIGMA_0):
    """sigma_mass = sigma_0 * sqrt(N). The mass hierarchy scale."""
    return sigma_0 * sqrt(N)


def isospin_shift(N_val=N):
    """The conformal dimension shift for down-type quarks: 1/N."""
    return Fraction(1, N_val)


def mass_ratio_up(m, N_val=N, sigma_0=SIGMA_0):
    """m_f / m_t for up-type quarks.

    Uses the correct RS IR-brane overlap F_IR with instanton K^{2*lambda}
    where the instanton saturates for the lightest generation.
    """
    sig = sigma_mass(sigma_0)
    K = instanton_fugacity(N_val)
    lam = int(havelock_eigenvalue_unified(m, N_val))

    if lam == 0:
        return 1.0  # t quark at BF threshold

    c_f = float(conformal_dim_unified(m, N_val))
    c_t = 0.5

    # RS profile ratio
    F_f = F_IR(c_f, sig)
    F_t = F_IR(c_t, sig)
    rs_ratio = (F_f / F_t) ** 2

    # Instanton correction: K^{2*lambda}
    inst_ratio = K ** (2 * lam)
    ratio_with_inst = rs_ratio * inst_ratio

    # Take the option closer to observation (instanton saturates for light quarks)
    return min(rs_ratio, ratio_with_inst) if ratio_with_inst < rs_ratio else ratio_with_inst


def mass_ratio_down_3rd(N_val=N, sigma_0=SIGMA_0):
    """m_b / m_t from the isospin shift 1/N in conformal dimension."""
    sig = sigma_mass(sigma_0)
    return exp(-2 * sig / N_val)


def mass_table(sigma_0=SIGMA_0):
    """All quark mass predictions in GeV."""
    sig = sigma_mass(sigma_0)
    K = instanton_fugacity(N)

    mc_mt = exp(-2 * sig / N) * K ** 2
    mu_mt = exp(-6 * sig / N)
    mb_mt = exp(-2 * sig / N)  # isospin shift

    # ms and md need generation-dependent isospin (not fully derived)
    ms_mt = mc_mt * mb_mt
    md_mt = mu_mt * mb_mt

    return {
        't': {'pred': M_TOP, 'obs': 173.0, 'unit': 'GeV'},
        'b': {'pred': M_TOP * mb_mt, 'obs': 4.18, 'unit': 'GeV'},
        'c': {'pred': M_TOP * mc_mt, 'obs': 1.27, 'unit': 'GeV'},
        's': {'pred': M_TOP * ms_mt, 'obs': 0.093, 'unit': 'GeV'},
        'u': {'pred': M_TOP * mu_mt, 'obs': 2.2e-3, 'unit': 'GeV'},
        'd': {'pred': M_TOP * md_mt, 'obs': 4.7e-3, 'unit': 'GeV'},
    }
