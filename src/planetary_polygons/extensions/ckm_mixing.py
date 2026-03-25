r"""
CKM mixing matrix from the Havelock Yukawa texture.

The 3×3 Yukawa matrix has 4 texture zeros from Z₇ charge conservation
(m_i - m_j + m_H ≡ 0 mod 7). The nonzero entries are determined by:
1. RS profile overlaps on H² (normalized with sinh(ρ) metric measure)
2. KK winding phases: exp(i × 2π × w × frac(k_phys))
3. Localization-dependent CS instanton phase: φ = -θ_CS × (2c_L - 1)

The CKM phase δ is determined non-perturbatively by the APS eta
invariant of the massive Dirac operator on H²:
  η(m) = tanh(πm),  m = c - 1/2
from Im ψ(1/2 + im) = (π/2)tanh(πm) — the same digamma function
as the Havelock kernel.

The BF-crossing mode (gen 3, m=3, μ₇=0) contributes 92.6% of the
eta invariant difference. With the SL(2,R) weight factor Δw = 2:

  δ_CKM = (1/2) log cosh(π) = 70.2°  (observed: 69° ± 3°)

Predictions (no adjustable parameters):
  |V_us| = 0.237 (obs: 0.224, 6% off)
  θ_C = 13.7° (obs: 13.0°, 5% off)
  δ = 70.2° (obs: 69°, 1.2° off)  ← from integrated scattering phase
  J = 3.5 × 10⁻⁵ (obs: 3.0 × 10⁻⁵, 17% off)  ← from perturbative CKM
  |V_us| >> |V_cb| >> |V_ub| ✓ (Wolfenstein hierarchy)
"""

import numpy as np
from math import sqrt, exp, sinh, pi, log


def b_exact(N):
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


def eta_invariant_phase(N=7, mu4_up=0.5, mu4_down=1.5):
    """CKM phase from the integrated scattering phase on H² (exact).

    The digamma identity Im psi(1/2 + im) = (pi/2)*tanh(pi*m) gives
    the scattering phase density of the massive Dirac operator on H².
    Integrating over the BF crossing range m in [0, Delta_m]:

      delta = integral_0^{Delta_m} Im psi(1/2 + im) dm
            = (1/2) log cosh(pi * Delta_m)

    where Delta_m = mu4_down - mu4_up = 3/2 - 1/2 = 1 (the T3 split).
    This gives delta = (1/2) log cosh(pi) = 70.2 deg (observed 69 +/- 3).

    The same digamma function generates the Havelock eigenvalue kernel.

    Returns dict with delta, mode breakdown, and consistency checks.
    """
    from math import tanh, sin, cosh
    c_N = 12 * b_exact(N)
    k_phys = c_N / 6 - N / 2
    k_frac = k_phys - int(k_phys)
    theta_CS = 2 * pi * k_frac

    # The BF crossing range
    delta_m = mu4_down - mu4_up  # = 1 for the T3 split

    # The prediction: delta = (1/2) log cosh(pi * delta_m)
    delta_rad = 0.5 * log(cosh(pi * delta_m))
    delta_deg = float(delta_rad * 180 / pi)
    sin_delta = sin(delta_rad)

    # Mode-by-mode scattering phase density (tanh is the DENSITY, not the integral)
    pairs = [(1, 6), (2, 5), (3, 4)]
    mode_contributions = []
    total_delta_eta = 0.0
    for gen, (m1, m2) in enumerate(pairs):
        for m in [m1, m2]:
            mu7 = abs(m - 3)
            c_up = sqrt(mu7**2 + mu4_up**2)
            c_dn = sqrt(mu7**2 + mu4_down**2)
            eta_up = tanh(pi * (c_up - 0.5))
            eta_dn = tanh(pi * (c_dn - 0.5))
            d_eta = eta_dn - eta_up
            total_delta_eta += d_eta
            mode_contributions.append({
                'mode': m, 'mu7': mu7, 'gen': gen + 1,
                'c_up': c_up, 'c_dn': c_dn,
                'eta_up': eta_up, 'eta_dn': eta_dn,
                'd_eta': d_eta,
                'bf_crossing': c_up < 1.0 < c_dn,
            })

    bf_mode = [mc for mc in mode_contributions if mc['bf_crossing']]
    bf_delta_eta = bf_mode[0]['d_eta'] if bf_mode else 0.0

    # J consistency check (uses OBSERVED mixing angles — not a prediction)
    s12, s23, s13 = 0.2243, 0.0422, 0.0036
    c12 = sqrt(1 - s12**2)
    c23 = sqrt(1 - s23**2)
    c13 = sqrt(1 - s13**2)
    J_check = s12 * s23 * s13 * c12 * c23 * c13**2 * sin_delta

    return {
        'delta_rad': delta_rad,
        'delta_deg': delta_deg,
        'sin_delta': sin_delta,
        'delta_m': delta_m,
        'theta_CS_rad': theta_CS,
        'theta_CS_deg': float(theta_CS * 180 / pi),
        'bf_delta_eta': bf_delta_eta,
        'total_delta_eta': total_delta_eta,
        'bf_fraction': bf_delta_eta / total_delta_eta if total_delta_eta > 0 else 0,
        'J_check': J_check,
        'mode_contributions': mode_contributions,
    }


def rs_profile(c, rho_star, n_steps=5000):
    """Normalized RS profile at IR brane on H² (with sinh metric)."""
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


def build_yukawa_complex(mu4_L, rho_star=1.734, N=7):
    """Build 3×3 COMPLEX Yukawa with KK winding + localization phases.

    Each entry includes:
    1. RS profile magnitude: f_L(c_L) × f_R(c_R)
    2. KK winding phase: exp(i × 2π × w × frac(k_phys))
    3. Localization phase: exp(i × (-θ_CS × (2c_L - 1)))
    """
    c_N = 12 * b_exact(N)
    k_phys = c_N / 6 - N / 2
    k_frac = k_phys - int(k_phys)
    theta_CS = 2 * pi * k_frac

    pairs = [(1, 6), (2, 5), (3, 4)]
    higgs_modes = [3, 4]

    Y = np.zeros((3, 3), dtype=complex)
    for i, (m1i, m2i) in enumerate(pairs):
        for j, (m1j, m2j) in enumerate(pairs):
            for mi in [m1i, m2i]:
                for mj in [m1j, m2j]:
                    for mH in higgs_modes:
                        if (mi - mj + mH) % N == 0:
                            w = (mi - mj + mH) // N
                            mu7_i = abs(mi - 3)
                            c_L = sqrt(mu7_i**2 + mu4_L**2)
                            f_L = rs_profile(c_L, rho_star)
                            mu7_j = abs(mj - 3)
                            c_R = sqrt(mu7_j**2 + 1.5**2)
                            f_R = rs_profile(c_R, rho_star)
                            # KK winding phase
                            phase_kk = 2 * pi * w * k_frac
                            # Localization-dependent CS phase
                            phase_loc = -theta_CS * (2 * c_L - 1)
                            Y[i, j] += f_L * f_R * np.exp(1j * (phase_kk + phase_loc))
    return Y


def ckm_matrix(rho_star=1.734):
    """Compute the CKM matrix with localization-dependent CS phases.

    Returns dict with CKM matrix, masses, and mixing parameters.
    """
    v = 246.22

    Y_up = build_yukawa_complex(0.5, rho_star)
    Y_down = build_yukawa_complex(1.5, rho_star)
    M_up = v * Y_up
    M_down = v * Y_down

    def diag(M):
        MdM = M.conj().T @ M
        evals, evecs = np.linalg.eigh(MdM)
        idx = np.argsort(evals)
        return np.sqrt(np.maximum(evals[idx], 0)), evecs[:, idx]

    m_up, U_up = diag(M_up)
    m_down, U_down = diag(M_down)
    V = U_up.conj().T @ U_down

    theta_C = float(np.arcsin(abs(V[0, 1])))
    J = float(np.imag(V[0, 0] * V[1, 1] * np.conj(V[0, 1]) * np.conj(V[1, 0])))
    delta = float(-np.angle(V[0, 2]))

    # Jarlskog-derived delta: sin δ = J / (s12 s23 s13 c12 c23 c13²)
    s12 = float(abs(V[0, 1]))
    s23 = float(abs(V[1, 2]))
    s13 = float(abs(V[0, 2]))
    c12 = sqrt(1 - s12**2)
    c23 = sqrt(1 - s23**2)
    c13 = sqrt(1 - s13**2)
    denom = s12 * s23 * s13 * c12 * c23 * c13**2
    sin_delta = J / denom if denom > 1e-15 else 0.0
    delta_J = float(np.degrees(np.arcsin(np.clip(sin_delta, -1.0, 1.0))))

    # What delta would be with observed mixing angles
    # J_max = s12 s23 s13 c12 c23 c13² (at delta=90°) for observed values
    s12o, s23o, s13o = 0.2243, 0.0422, 0.0036
    c12o = sqrt(1 - s12o**2)
    c23o = sqrt(1 - s23o**2)
    c13o = sqrt(1 - s13o**2)
    J_max_obs = s12o * s23o * s13o * c12o * c23o * c13o**2
    # Our J / J_max: how close are we to maximal CP violation?
    j_ratio = abs(J) / J_max_obs if J_max_obs > 0 else 0.0
    # With J_obs = 3.0e-5 (the measured value):
    J_obs = 3.0e-5
    sin_delta_with_Jobs = J_obs / J_max_obs if J_max_obs > 0 else 0.0
    delta_corrected = float(np.degrees(np.arcsin(
        np.clip(sin_delta_with_Jobs, -1.0, 1.0))))

    return {
        'V': np.abs(V),
        'V_complex': V,
        'm_up': m_up,
        'm_down': m_down,
        'V_us': s12,
        'V_cb': s23,
        'V_ub': s13,
        'V_ud': float(abs(V[0, 0])),
        'V_tb': float(abs(V[2, 2])),
        'theta_C_deg': float(np.degrees(theta_C)),
        'J': J,
        'delta_rad': delta,
        'delta_deg': float(np.degrees(delta)),
        'delta_from_J_deg': delta_J,
        'sin_delta': sin_delta,
        'delta_if_Vcb_correct': delta_corrected,
        'J_ratio_to_max': j_ratio,
        'texture': yukawa_texture(),
        'is_hierarchical': s12 > s23 > s13,
        'is_near_diagonal': float(abs(V[0, 0])) > 0.9 and float(abs(V[2, 2])) > 0.9,
    }
