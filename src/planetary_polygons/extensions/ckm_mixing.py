r"""
CKM mixing matrix from the Havelock Yukawa texture.

The 3×3 Yukawa matrix has 4 texture zeros from Z₇ charge conservation
(m_i - m_j + m_H ≡ 0 mod 7). The nonzero entries are determined by
Randall-Sundrum profile overlaps on H².

CKM = U_up† × U_down where U_up, U_down diagonalize the up-type
and down-type mass matrices.

Predictions (zero free parameters):
  - Near-diagonal structure ✓
  - |V_us| ≈ 0.21 (observed: 0.224, 8% off)
  - Cabibbo angle θ_C ≈ 12° (observed: 13°, 8% off)
  - Hierarchical: |V_us| >> |V_cb| >> |V_ub| ✓
  - J = 0 (all Yukawa entries are real from KK phases)
    CP violation requires the fractional CS level (§baryogenesis)
"""

import numpy as np
from math import sqrt, exp, sinh, pi


def rs_profile(c, rho_star, n_steps=10000):
    """Normalized RS profile at IR brane on H²."""
    drho = rho_star / n_steps
    integral = 0
    for i in range(1, n_steps):
        rho = i * drho
        f_unnorm = exp((0.5 - c) * rho)
        integral += f_unnorm**2 * sinh(rho) * drho
    A = 1.0 / sqrt(integral) if integral > 0 else 0
    return A * exp((0.5 - c) * rho_star)


def yukawa_texture(N=7, higgs_pair_idx=2):
    """The Yukawa texture from KK charge conservation mod N."""
    pairs = [(m, N - m) for m in range(1, (N + 1) // 2)]
    higgs_modes = list(pairs[higgs_pair_idx])
    texture = np.zeros((len(pairs), len(pairs)), dtype=int)
    for i in range(len(pairs)):
        for j in range(len(pairs)):
            for m_i in pairs[i]:
                for m_j in pairs[j]:
                    for m_H in higgs_modes:
                        if (m_i - m_j + m_H) % N == 0:
                            texture[i, j] = 1
    return texture


def build_yukawa(mu4_L, rho_star=1.734, N=7):
    """Build 3×3 Yukawa matrix for given isospin mass mu4_L."""
    pairs = [(1, 6), (2, 5), (3, 4)]
    texture = yukawa_texture(N)
    Y = np.zeros((3, 3))
    for i, (m1i, _) in enumerate(pairs):
        mu7_i = abs(m1i - 3)
        c_L = sqrt(mu7_i**2 + mu4_L**2)
        f_L = rs_profile(c_L, rho_star)
        for j, (m1j, _) in enumerate(pairs):
            mu7_j = abs(m1j - 3)
            c_R = sqrt(mu7_j**2 + 1.5**2)
            f_R = rs_profile(c_R, rho_star)
            if texture[i, j]:
                Y[i, j] = f_L * f_R
    return Y


def ckm_matrix(rho_star=1.734):
    """Compute the CKM matrix from the Havelock Yukawa texture.

    Returns dict with the CKM matrix, masses, and mixing parameters.
    """
    v = 246.22

    Y_up = build_yukawa(0.5, rho_star)
    Y_down = build_yukawa(1.5, rho_star)
    M_up = v * Y_up
    M_down = v * Y_down

    def diag(M):
        MdM = M.T @ M
        evals, evecs = np.linalg.eigh(MdM)
        idx = np.argsort(evals)
        return np.sqrt(np.maximum(evals[idx], 0)), evecs[:, idx]

    m_up, U_up = diag(M_up)
    m_down, U_down = diag(M_down)
    V = U_up.T @ U_down

    theta_C = float(np.arcsin(abs(V[0, 1])))
    J = float(np.imag(V[0, 0] * V[1, 1] * np.conj(V[0, 1]) * np.conj(V[1, 0])))

    return {
        'V': np.abs(V),
        'V_complex': V,
        'm_up': m_up,
        'm_down': m_down,
        'V_us': float(abs(V[0, 1])),
        'V_cb': float(abs(V[1, 2])),
        'V_ub': float(abs(V[0, 2])),
        'V_ud': float(abs(V[0, 0])),
        'V_tb': float(abs(V[2, 2])),
        'theta_C_deg': float(np.degrees(theta_C)),
        'J': J,
        'texture': yukawa_texture(),
        'is_hierarchical': float(abs(V[0, 1])) > float(abs(V[1, 2])) > float(abs(V[0, 2])),
        'is_near_diagonal': float(abs(V[0, 0])) > 0.9 and float(abs(V[2, 2])) > 0.9,
    }
