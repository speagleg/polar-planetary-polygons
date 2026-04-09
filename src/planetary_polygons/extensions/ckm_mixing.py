r"""
CKM mixing matrix from the Havelock Yukawa texture.

The 3×3 Yukawa matrix has 4 texture zeros from Z₇ charge conservation
(m_i - m_j + m_H ≡ 0 mod 7). The nonzero entries are determined by:
1. RS profile overlaps on H² (normalized with sinh(ρ) metric measure)
2. KK winding phases: exp(i × 2π × w × frac(k_phys))
3. Localization-dependent CS instanton phase: φ = -θ_CS × (2c_L - 1)

The CKM phase δ is the product of three independent factors:
1. The fractional Chern-Simons phase from N=7: θ_CS = 2π × frac(k_phys)
2. The Plancherel density of the Dirac operator on H² at the BF-crossing
   endpoint: tanh(π × 1) = tanh(π) ≈ 0.9963 (Bolte-Stiepan 2006; Bär 2000)
3. The SL(2,R) weight factor Δw = 2(c_dn - c_up) = 2

  δ_CKM = Δw × θ_CS × tanh(π) = 2 × θ_CS × tanh(π) = 68.63°
       (observed: 69° ± 3°, 0.12σ match)

The BF-crossing mode (gen 3, m=3, μ₇=0) contributes 92.6% of the
total Plancherel weight difference; tanh saturates rapidly so all
other modes are negligible.

Predictions (no adjustable parameters):
  |V_us| = 0.237 (obs: 0.224, 6% off)
  θ_C = 13.7° (obs: 13.0°, 5% off)
  δ = 68.63° (obs: 69°, 0.37° off)  ← from 2·θ_CS·tanh(π)
  J = 3.09 × 10⁻⁵ (obs: 3.0 × 10⁻⁵, 3% off)  ← consistency check
  |V_us| >> |V_cb| >> |V_ub| ✓ (Wolfenstein hierarchy)
"""

import numpy as np
from math import sqrt, exp, sinh, pi, log


def b_exact(N):
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


def eta_invariant_phase(N=7, mu4_up=0.5, mu4_down=1.5):
    """CKM phase from the H² Dirac Plancherel density (exact).

    The Selberg trace formula gives the Plancherel density of the
    Dirac operator on H² as (1/(4pi))*tanh(pi*s), where s is the
    Plancherel spectral parameter (Bolte-Stiepan 2006; Bar 2000).
    The tanh(pi*s) factor measures spectral asymmetry.

    For the BF-crossing mode, s sweeps from s_up = 0 (BF saturated)
    to s_dn = 1 (BF-crossing endpoint), accumulating weight tanh(pi).
    The SL(2,R) weight factor is Delta_w = 2(c_dn - c_up) = 2, and
    each unit of weight contributes theta_CS:

      delta = Delta_w * theta_CS * tanh(pi) = 2 * theta_CS * tanh(pi)

    where theta_CS = 2*pi*frac(k_phys) = 0.601 rad from N=7.
    Numerically: delta = 2 * 0.601 * 0.9963 = 1.198 rad = 68.63 deg
    (observed 69 +/- 3 deg, 0.12 sigma match).

    The digamma identity Im psi(1/2 + is) = (pi/2)*tanh(pi*s) underlies
    both the Plancherel density and the Havelock eigenvalue kernel.

    Returns dict with delta, mode breakdown, and consistency checks.
    """
    from math import tanh, sin, cosh
    c_N = 12 * b_exact(N)
    k_phys = c_N / 6 - N / 2
    k_frac = k_phys - int(k_phys)
    theta_CS = 2 * pi * k_frac

    # The BF crossing range (spectral parameter sweep)
    delta_m = mu4_down - mu4_up  # = 1 for the T3 split

    # SL(2,R) weight factor: Delta_w = 2(c_dn - c_up) = 2 * delta_m
    delta_w = 2 * delta_m

    # Plancherel weight at the BF-crossing endpoint: tanh(pi * s_dn)
    plancherel_weight = tanh(pi * delta_m)  # tanh(pi) = 0.9963

    # The prediction: delta = Delta_w * theta_CS * tanh(pi)
    delta_rad = delta_w * theta_CS * plancherel_weight
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


def bf_barrier_transmission(N=7, rho_star=1.734, c=1.5):
    """Orbifold image barrier transmission T_2 from the Legendre Q function.

    On H²/Z_N, the nearest orbifold image at radius rho* is at geodesic
    distance d = acosh(cosh²(rho*) - sinh²(rho*) cos(2π/N)).
    The Dirac Green's function at this distance gives the transmission:
        T_2 = Q_{c-1/2}(cosh d)
    For the BF-crossing mode (c = 3/2), this is Q_1(cosh d).

    Returns dict with d, cosh_d, T_2, V_cb, and all image contributions.
    """
    from math import cos, acosh, cosh as _cosh, sinh as _sinh, tanh as _tanh

    # Geodesic distance to nearest Z_N image at radius rho*
    angle = 2 * pi / N
    cosh_d = _cosh(rho_star)**2 - _sinh(rho_star)**2 * cos(angle)
    d = acosh(cosh_d)

    # Legendre Q functions: Q_0(x) = (1/2)ln((x+1)/(x-1)), Q_1(x) = x*Q_0(x) - 1
    nu = c - 0.5  # Legendre order
    x = cosh_d
    Q0 = 0.5 * log((x + 1) / (x - 1))

    if abs(nu) < 1e-10:
        T_2 = Q0
    elif abs(nu - 1.0) < 1e-10:
        T_2 = x * Q0 - 1
    else:
        raise NotImplementedError(f"Q_{{nu}}(x) for nu={nu} not implemented; use c=1/2 or c=3/2")

    # All image contributions
    images = []
    for k in range(1, N):
        angle_k = 2 * pi * k / N
        cosh_dk = _cosh(rho_star)**2 - _sinh(rho_star)**2 * cos(angle_k)
        dk = acosh(cosh_dk)
        xk = cosh_dk
        Q0k = 0.5 * log((xk + 1) / (xk - 1))
        Q1k = xk * Q0k - 1
        images.append({'k': k, 'd': dk, 'cosh_d': cosh_dk, 'Q1': Q1k})

    # V_cb from geometric mean: |V_cb| = sqrt(V_cb_pert * T_2)
    V_cb_pert = 0.092
    V_cb_uncorrected = sqrt(V_cb_pert * T_2)

    # Self-consistent orbifold correction to rho*:
    # The two nearest Z_N images (k=1, k=N-1) each contribute Q_1(cosh d)
    # to the BO potential. Images are stabilising (same-sign vortex repulsion
    # pushes the ring inward), so V_orb = V - 2*Q_1 < V at the threshold.
    # The zero of V_orb shifts RIGHT: rho*_new > rho*_0.
    # Linearised: V'(rho*)(rho_new - rho*_0) = 2*Q_1, i.e.
    #   rho*_new = rho*_0 + 2*Q_1 / coth(rho*_0)
    #            = rho*_0 + 2*Q_1 * tanh(rho*_0)
    rho_sc = rho_star
    for _ in range(10):
        cosh_d_sc = _cosh(rho_sc)**2 - _sinh(rho_sc)**2 * cos(angle)
        x_sc = cosh_d_sc
        Q0_sc = 0.5 * log((x_sc + 1) / (x_sc - 1))
        Q1_sc = x_sc * Q0_sc - 1
        rho_sc = rho_star + 2 * Q1_sc * _tanh(rho_star)

    T_2_sc = Q1_sc
    V_cb_sc = sqrt(V_cb_pert * T_2_sc)

    return {
        'N': N,
        'rho_star': rho_star,
        'rho_star_sc': rho_sc,
        'c': c,
        'nu': nu,
        'angle': angle,
        'd': d,
        'cosh_d': cosh_d,
        'T_2': T_2,
        'T_2_sc': T_2_sc,
        'V_cb_pert': V_cb_pert,
        'V_cb_uncorrected': V_cb_uncorrected,
        'V_cb': V_cb_sc,
        'images': images,
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
