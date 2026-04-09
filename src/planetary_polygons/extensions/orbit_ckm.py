"""Orbit-based CKM matrix from the Bernoulli-Havelock backbone.

Derives all 5 CKM observables from N=7 using:
- Frobenius orbit assignment: up=QR={1,2,4}, down=QNR={6,5,3}
- Bernoulli instanton phases: aL=1/7, aR=5/42, aH=2/21
- Unified conformal dimensions: c = 1/2 + lambda/N
- Correct RS IR-brane overlap: F_IR with exp(+x) denominator
- LEFT rotation CKM: V = U_L_up^dag * U_L_down from YY^dag
- Instanton correction: s13 = s13_tree * K^(N-1)
"""

import numpy as np
from math import pi, sqrt, atan, degrees, asin, log, exp, sin
import cmath

from planetary_polygons.extensions.bernoulli_havelock import (
    SIGMA_0, N_CRIT, BERNOULLI_PHASES,
    conformal_dim_unified, F_IR, instanton_fugacity,
)

N = N_CRIT
UP_L = [1, 2, 4]    # QR(7) = quadratic residues mod 7
DN_L = [6, 5, 3]    # QNR(7) = quadratic non-residues, ordered by Casimir
HIGGS = [3, 4]       # Higgs modes (straddle both orbits)


def build_orbit_yukawa(L_modes, sigma=SIGMA_0):
    """Build 3x3 complex Yukawa with Bernoulli instanton phases.

    Each entry sums over R modes {L_j, N-L_j} and Higgs {3,4}.
    Selection rule: mL - mR + mH = 0 mod N.
    Phase: exp(2*pi*i*(aL*mL + aR*mR + aH*mH)/N).
    Magnitude: F_IR(c(mL), sigma) * F_IR(c(mR), sigma).
    """
    aL = float(BERNOULLI_PHASES['aL'])
    aR = float(BERNOULLI_PHASES['aR'])
    aH = float(BERNOULLI_PHASES['aH'])

    n = len(L_modes)
    Y = np.zeros((n, n), dtype=complex)

    for i in range(n):
        mL = L_modes[i]
        for j in range(n):
            mL_j = L_modes[j]
            for mR in [mL_j, N - mL_j]:
                for mH in HIGGS:
                    if (mL - mR + mH) % N == 0:
                        c_L = float(conformal_dim_unified(mL, N))
                        c_R = float(conformal_dim_unified(mR, N))
                        f_L = F_IR(c_L, sigma)
                        f_R = F_IR(c_R, sigma)
                        phase = np.exp(2j * pi * (aL * mL + aR * mR + aH * mH) / N)
                        Y[i, j] += f_L * f_R * phase
    return Y


def diag_left(Y):
    """Diagonalize YY^dag to get LEFT rotation U_L.

    CKM uses LEFT rotations: V = U_L_up^dag * U_L_down.
    YY^dag = U_L * diag(m_i^2) * U_L^dag.

    Returns (mass_eigenvalues, U_L) sorted by ascending eigenvalue.
    """
    MMd = Y @ Y.conj().T
    evals, evecs = np.linalg.eigh(MMd)
    idx = np.argsort(evals)
    return np.sqrt(np.maximum(evals[idx], 0)), evecs[:, idx]


def instanton_correction(s13_tree, K, N_val=N):
    """s13_corrected = s13_tree * K^(N-1).

    The power N-1 = 6 comes from the total instanton winding:
    w_up = (N-1)/2 = 3 (max gap in QR = {1,2,4})
    w_dn = (N-1)/2 = 3 (max gap in QNR = {6,5,3})
    w_total = w_up + w_dn = N-1 = 6.
    """
    return s13_tree * K ** (N_val - 1)


def unitarity_triangle(V):
    """Extract unitarity triangle angles from CKM matrix V.

    alpha = arg(-V_td V_tb* / (V_ud V_ub*))
    beta  = arg(-V_cd V_cb* / (V_td V_tb*))
    gamma = arg(-V_ud V_ub* / (V_cd V_cb*))
    """
    alpha = degrees(cmath.phase(
        -V[2, 0] * V[2, 2].conjugate() / (V[0, 0] * V[0, 2].conjugate())))
    beta = degrees(cmath.phase(
        -V[1, 0] * V[1, 2].conjugate() / (V[2, 0] * V[2, 2].conjugate())))
    gamma = degrees(cmath.phase(
        -V[0, 0] * V[0, 2].conjugate() / (V[1, 0] * V[1, 2].conjugate())))
    return alpha, beta, gamma


def ckm_matrix(sigma=SIGMA_0):
    """Compute the full CKM matrix and all observables.

    Returns dict with V, mixing angles, Jarlskog, UT angles, CP phase.
    """
    K = instanton_fugacity(N)

    Y_up = build_orbit_yukawa(UP_L, sigma)
    Y_dn = build_orbit_yukawa(DN_L, sigma)

    m_up, U_L_up = diag_left(Y_up)
    m_dn, U_L_dn = diag_left(Y_dn)

    V = U_L_up.conj().T @ U_L_dn

    s12 = float(abs(V[0, 1]))
    s23 = float(abs(V[1, 2]))
    s13_tree = float(abs(V[0, 2]))
    s13_corrected = instanton_correction(s13_tree, K)

    J_tree = float(np.imag(
        V[0, 0] * V[1, 1] * V[0, 1].conjugate() * V[1, 0].conjugate()))

    alpha, beta, gamma = unitarity_triangle(V)

    delta_CKM = degrees(atan(sqrt(N)))

    # Corrected Jarlskog using s13_corrected
    c12 = sqrt(1 - s12 ** 2)
    c23 = sqrt(1 - s23 ** 2)
    c13c = sqrt(1 - s13_corrected ** 2)
    J_corrected = s12 * s23 * s13_corrected * c12 * c23 * c13c ** 2 * sin(atan(sqrt(N)))

    return {
        'V': V,
        's12': s12,
        's23': s23,
        's13_tree': s13_tree,
        's13_corrected': s13_corrected,
        'J': J_corrected,
        'J_tree': J_tree,
        'alpha': alpha,
        'beta': beta,
        'gamma': gamma,
        'delta_CKM': delta_CKM,
        'K': K,
        'm_up': m_up,
        'm_dn': m_dn,
    }
