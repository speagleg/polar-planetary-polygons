"""Regularized Euclidean action for N-polygon vs BTZ in 2+1D AdS gravity.

Computes the on-shell Euclidean action I_E = beta*F for:
  (a) N equal-mass conical singularities in a regular ring on AdS_3
  (b) A BTZ black hole with the same total mass

The action difference Delta I = I_polygon - I_BTZ determines the phase
diagram: Delta I > 0 means BTZ is preferred; Delta I < 0 means the
polygon is preferred.

Key results:
  1. The polygon-BTZ transition temperature is
       T_c = (1/(2*pi*ell)) * sqrt(1 - 8*G*E_polygon)
     which is the Hawking-Page temperature shifted by the polygon mass.

  2. The polygon is always locally stable for N <= N_crit(xi)
     (Havelock eigenvalue criterion), independent of temperature.

  3. For N > N_crit: the negative Havelock mode m = floor(N/2)
     is a negative mode of the gravitational action, signaling
     decay toward a non-symmetric polygon and eventually BTZ.

Conventions:
  - Masses are parameterized by Gm (dimensionless, 0 < Gm < 1/(4N))
  - alpha = 1 - 4*Gm is the cone angle parameter
  - M = (1 - alpha^2)/(8G) is the mass above vacuum (Brown-York)
  - The vacuum has M_vac = -1/(8G), so M_abs = -alpha^2/(8G)
  - BTZ: M = r_+^2/(8*G*ell^2), T = r_+/(2*pi*ell^2), S = pi*r_+/(2*G)
"""

import math
import cmath


# ============================================================
# BTZ thermodynamics
# ============================================================

def btz_mass_from_rplus(r_plus, G, ell):
    """BTZ mass: M = r_+^2 / (8*G*ell^2)."""
    return r_plus**2 / (8 * G * ell**2)


def btz_temperature(r_plus, ell):
    """BTZ Hawking temperature: T = r_+ / (2*pi*ell^2)."""
    return r_plus / (2 * math.pi * ell**2)


def btz_entropy(r_plus, G):
    """BTZ Bekenstein-Hawking entropy: S = pi*r_+ / (2*G)."""
    return math.pi * r_plus / (2 * G)


def btz_rplus_from_mass(M, G, ell):
    """Horizon radius from mass: r_+ = ell*sqrt(8*G*M)."""
    return ell * math.sqrt(8 * G * M)


def btz_free_energy(beta, G, ell):
    """BTZ free energy at inverse temperature beta.

    F = M - T*S = -pi^2*ell^2 / (2*G*beta^2).
    """
    return -math.pi**2 * ell**2 / (2 * G * beta**2)


def btz_action(beta, G, ell):
    """Euclidean action of BTZ at inverse temperature beta.

    I_BTZ = beta*F = -pi^2*ell^2 / (2*G*beta).
    """
    return -math.pi**2 * ell**2 / (2 * G * beta)


def btz_action_at_hawking_temp(M, G, ell):
    """Euclidean action of BTZ evaluated at its own Hawking temperature.

    I = beta*M - S = -pi*r_+/(4*G) = -pi*ell*sqrt(8*G*M)/(4*G).
    """
    r_plus = btz_rplus_from_mass(M, G, ell)
    return -math.pi * r_plus / (4 * G)


# ============================================================
# Single conical singularity
# ============================================================

def cone_mass(Gm):
    """Mass of a single conical singularity above vacuum.

    Delta M = (1 - alpha^2)/(8G) where alpha = 1 - 4*Gm.
    In units where we track Gm: Delta M = Gm*(1 - 2*Gm) / G.
    But since we work with dimensionless Gm: Delta M * G = Gm*(1 - 2*Gm).
    """
    alpha = 1 - 4 * Gm
    return (1 - alpha**2) / 8  # this is G*Delta_M


def cone_action(beta, Gm, G, ell):
    """Euclidean action of a single conical singularity at the center.

    I = -alpha^2 * beta / (8*G), where alpha = 1 - 4*Gm.
    This is beta * M_abs = beta * (-alpha^2/(8G)).
    """
    alpha = 1 - 4 * Gm
    return -alpha**2 * beta / (8 * G)


# ============================================================
# Polygon: chordal interaction on the Poincaré disk
# ============================================================

def chordal_distance(xi, j, k, N):
    """Chordal distance sigma(z_j, z_k) on the Poincaré disk.

    z_j = sqrt(xi) * exp(2*pi*i*j/N), z_k = sqrt(xi) * exp(2*pi*i*k/N).
    sigma = |z_j - z_k| / |1 - bar(z_j)*z_k|.
    """
    R = math.sqrt(xi)
    angle = 2 * math.pi * (j - k) / N
    numerator = 2 * R * abs(math.sin(math.pi * (j - k) / N))
    denominator = abs(1 - xi * cmath.exp(1j * angle))
    return numerator / denominator


def havelock_energy_h2(N, xi):
    """Havelock energy of the regular N-gon on H^2:
    H = -sum_{j<k} log sigma(z_j, z_k).

    Returns a positive number (sigma < 1 on the disk so log < 0, H > 0).
    Requires xi > 0 (the ring has nonzero radius).
    """
    if xi <= 0:
        raise ValueError("xi must be > 0 for the energy computation "
                         "(xi=0 gives a degenerate ring at the origin)")
    H = 0.0
    for j in range(N):
        for k in range(j + 1, N):
            sigma = chordal_distance(xi, j, k, N)
            if sigma <= 0:
                raise ValueError(f"sigma({j},{k}) = {sigma} <= 0")
            H -= math.log(sigma)
    return H


def polygon_binding_energy(N, Gm, xi):
    """Gravitational binding energy of the N-polygon.

    V_int = -(Gm)^2 * (1/pi) * sum_{j!=k} log sigma_{jk}
           = (Gm)^2 * (2/pi) * H(N, xi)

    where H = -sum_{j<k} log sigma > 0 (positive).
    So V_int > 0 in this convention (repulsive for "anti-gravitational"
    sign, or we interpret it as the pairwise energy).

    Actually: the gravitational interaction energy between two masses
    m_j, m_k on H^2 is V_{jk} = -G*m_j*m_k * G_H2(z_j, z_k)
    where G_H2 = -(1/(2*pi))*log(sigma). So:
    V_{jk} = -(G*m^2/(2*pi)) * (-log sigma) = (G*m^2/(2*pi)) * log sigma

    Total: V_int = (G*m^2/(2*pi)) * sum_{j<k} log sigma = -(G*m^2/(2*pi)) * H

    So V_int < 0 (attractive). In units of G: V_int * G = -(Gm)^2/(2*pi) * H.
    """
    H = havelock_energy_h2(N, xi)
    return -(Gm)**2 / (2 * math.pi) * H  # negative (attractive)


def polygon_total_energy_G(N, Gm, xi):
    """Total energy of the N-polygon in units of 1/G.

    E * G = N * Gm * (1 - 2*Gm) + V_int * G
    where V_int * G = -(Gm)^2/(2*pi) * H(N, xi).
    """
    E_kinematic = N * Gm * (1 - 2 * Gm)
    V_int = polygon_binding_energy(N, Gm, xi)
    return E_kinematic + V_int


def polygon_action(beta, N, Gm, G, ell, xi):
    """Euclidean action of the N-polygon at inverse temperature beta.

    I = I_vacuum + beta * E_polygon
      = -beta/(8*G) + beta * E_polygon
    """
    E_G = polygon_total_energy_G(N, Gm, xi)  # E * G
    return -beta / (8 * G) + beta * E_G / G


# ============================================================
# Phase diagram: polygon vs BTZ
# ============================================================

def polygon_btz_action_difference(beta, N, Gm, G, ell, xi):
    """Delta I = I_polygon - I_BTZ at the same temperature.

    If Delta I < 0: polygon is globally preferred.
    If Delta I > 0: BTZ is globally preferred.
    """
    I_poly = polygon_action(beta, N, Gm, G, ell, xi)
    I_btz = btz_action(beta, G, ell)
    return I_poly - I_btz


def transition_temperature(N, Gm, G, ell, xi):
    """Temperature at which the polygon and BTZ free energies cross.

    Solving I_polygon = I_BTZ:
      -beta/(8G) + beta*E/G = -pi^2*ell^2/(2*G*beta)

    => beta^2 * (E*G - 1/8) = -pi^2*ell^2/2
    => beta^2 = pi^2*ell^2 / (2*(1/8 - E*G))
    => beta^2 = 4*pi^2*ell^2 / (1 - 8*G*E)

    T_c = 1/(2*pi*ell) * sqrt(1 - 8*G*E_polygon)

    Exists iff 8*G*E < 1 (polygon mass below BTZ threshold).
    """
    E_G = polygon_total_energy_G(N, Gm, xi)  # E * G
    discriminant = 1 - 8 * E_G

    if discriminant <= 0:
        return None  # no transition; BTZ always preferred

    T_c = math.sqrt(discriminant) / (2 * math.pi * ell)
    return T_c


def hawking_page_temperature(ell):
    """Standard Hawking-Page temperature: T_HP = 1/(2*pi*ell)."""
    return 1.0 / (2 * math.pi * ell)


# ============================================================
# Negative mode analysis
# ============================================================

def C1_h2(N, xi):
    """C1 on the Poincaré disk: C1 = (N-1)*(1+xi^2)/(1-xi)^2."""
    return (N - 1) * (1 + xi**2) / (1 - xi)**2


def havelock_eigenvalue_h2(N, m, xi):
    """Havelock eigenvalue on H^2: lambda_m = C1(xi) - m(N-m)/2."""
    return C1_h2(N, xi) - m * (N - m) / 2


def critical_mode(N):
    """The first mode to go unstable: m_crit = floor(N/2)."""
    return N // 2


def min_eigenvalue(N, xi):
    """Minimum Havelock eigenvalue: lambda_{N/2} at mode m_crit."""
    m = critical_mode(N)
    return havelock_eigenvalue_h2(N, m, xi)


def negative_mode_eigenvalue(N, xi):
    """The negative mode eigenvalue (the gravitational negative mode).

    Returns (m_crit, lambda_crit).
    lambda_crit < 0 means the polygon is unstable and has a negative
    mode in the Euclidean gravitational action.
    """
    m = critical_mode(N)
    lam = havelock_eigenvalue_h2(N, m, xi)
    return m, lam


def polygon_onset_xi(N):
    """The curvature xi at which the polygon becomes unstable.

    This is the palindromic threshold xi*(N): the value of xi where
    lambda_{m_crit} = 0, i.e., C1(xi) = f_max(N).

    For N <= 7: the polygon is stable on the flat plane (xi=0),
    so xi* is not defined (or equivalently xi* = 0).

    For N >= 8: xi* > 0, given by solving
    (N-1)*(1+xi^2)/(1-xi)^2 = m_crit*(N-m_crit)/2.
    """
    m = critical_mode(N)
    f_max = m * (N - m) / 2

    if N <= 7:
        return 0.0  # stable on flat plane

    # Solve (N-1)(1+x^2)/(1-x)^2 = f_max
    # Let F = f_max/(N-1). Then (1+x^2)/(1-x)^2 = F
    # => 1 + x^2 = F*(1 - 2x + x^2)
    # => x^2(1-F) + 2Fx + (1-F) = 0
    # => (F-1)*x^2 - 2Fx + (F-1) = 0  [multiply by -1]
    # => x = (2F ± sqrt(4F^2 - 4(F-1)^2)) / (2(F-1))
    # => x = (2F ± 2*sqrt(F^2 - (F-1)^2)) / (2(F-1))
    # => x = (F ± sqrt(2F - 1)) / (F - 1)

    F = f_max / (N - 1)
    if F <= 0.5:
        return None  # no threshold (always stable on H^2)

    disc = 2 * F - 1
    sqrt_disc = math.sqrt(disc)
    # Two solutions; take the smaller positive one
    x1 = (F - sqrt_disc) / (F - 1)
    x2 = (F + sqrt_disc) / (F - 1)
    # We want xi in (0, 1)
    candidates = [x for x in [x1, x2] if 0 < x < 1]
    if not candidates:
        return None
    return min(candidates)


# ============================================================
# Phase diagram computation
# ============================================================

def phase_diagram_row(N, Gm, ell, xi):
    """Compute all thermodynamic quantities for one (N, xi) point.

    Returns dict with:
      - E_polygon: total polygon energy (*G)
      - T_c: transition temperature (polygon-BTZ)
      - T_HP: standard Hawking-Page temperature
      - m_crit, lambda_crit: negative mode data
      - phase: 'stable_preferred', 'stable_metastable',
               'unstable_preferred', 'unstable_decay'
    """
    G = 1.0  # work in units where G = 1

    E_G = polygon_total_energy_G(N, Gm, xi)
    T_HP = hawking_page_temperature(ell)
    T_c = transition_temperature(N, Gm, G, ell, xi)
    m_crit, lam_crit = negative_mode_eigenvalue(N, xi)

    locally_stable = lam_crit >= 0

    # Determine phase
    if locally_stable:
        if T_c is not None:
            phase = 'stable_metastable'  # locally stable, BTZ preferred at high T
        else:
            phase = 'stable_preferred'
    else:
        if T_c is not None:
            phase = 'unstable_decay'  # unstable AND BTZ preferred at high T
        else:
            phase = 'unstable_preferred'  # unstable but lower action than BTZ

    return {
        'N': N,
        'xi': xi,
        'Gm': Gm,
        'E_polygon_G': E_G,
        'T_c': T_c,
        'T_HP': T_HP,
        'm_crit': m_crit,
        'lambda_crit': lam_crit,
        'locally_stable': locally_stable,
        'phase': phase,
    }


def full_phase_diagram(Gm=0.01, ell=1.0, N_range=None, xi_range=None):
    """Compute the full phase diagram in (N, xi) space.

    Returns list of phase_diagram_row dicts.
    """
    if N_range is None:
        N_range = range(3, 16)
    if xi_range is None:
        xi_range = [0.0, 0.01, 0.05, 0.1, 0.2, 0.5]

    rows = []
    for N in N_range:
        if Gm >= 1.0 / (4 * N):
            continue
        for xi in xi_range:
            if xi >= 1.0:
                continue
            rows.append(phase_diagram_row(N, Gm, ell, xi))
    return rows


# ============================================================
# The polygon-BTZ entropy gap
# ============================================================

def polygon_btz_entropy_gap(N, Gm, xi, G=1.0, ell=1.0):
    """The entropy gap between BTZ and polygon at the same total energy.

    Delta S = S_BTZ(E_polygon) - S_polygon = S_BTZ(E_polygon) - 0
            = pi * ell * sqrt(8*G*E) / (2*G)

    where E = E_polygon is the total energy.
    This is always positive: the BTZ has higher entropy at any energy.
    The polygon is therefore always metastable (never the global minimum
    of the free energy in the microcanonical ensemble).

    The TUNNELING RATE from polygon to BTZ goes as exp(-Delta S).
    """
    E_G = polygon_total_energy_G(N, Gm, xi)
    if E_G <= 0:
        return 0.0  # below BTZ threshold
    E = E_G / G
    r_plus = ell * math.sqrt(8 * G * E)
    S_btz = math.pi * r_plus / (2 * G)
    return S_btz


# ============================================================
# The negative mode: detailed analysis
# ============================================================

def negative_mode_profile(N, xi):
    """The spatial profile of the first negative mode.

    At N > N_crit(xi): mode m = floor(N/2) has lambda_m < 0.
    This mode represents alternating inward-outward displacement:
      delta_theta_k = A * cos(2*pi*m*k/N)

    For even N: this is exact alternation (every other vertex in, out).
    For odd N: approximate alternation with a slowly-varying envelope.

    Returns dict with mode profile data.
    """
    m = critical_mode(N)
    lam = havelock_eigenvalue_h2(N, m, xi)

    profile = []
    for k in range(N):
        displacement = math.cos(2 * math.pi * m * k / N)
        profile.append({
            'vertex': k,
            'angle': 2 * math.pi * k / N,
            'displacement': displacement,
            'direction': 'inward' if displacement < 0 else 'outward',
        })

    return {
        'N': N,
        'xi': xi,
        'm_crit': m,
        'lambda': lam,
        'unstable': lam < 0,
        'profile': profile,
    }


def decay_channel_analysis(N, xi, Gm, G=1.0, ell=1.0):
    """Analysis of the decay channel for unstable polygons.

    For N > N_crit:
    1. The negative mode m = floor(N/2) grows exponentially
    2. Adjacent masses approach each other (alternating pattern)
    3. When masses coalesce: total mass Nm exceeds BTZ threshold
       if 8*G*Nm > 1, forming a BTZ black hole

    Returns dict with decay analysis.
    """
    m, lam = negative_mode_eigenvalue(N, xi)
    E_G = polygon_total_energy_G(N, Gm, xi)

    # Check if total mass exceeds BTZ threshold
    btz_threshold = 1.0 / (8 * G)  # M = 1/(8G) is the massless BTZ
    total_mass = E_G / G

    # BTZ at the total mass
    if total_mass > 0:
        r_plus = ell * math.sqrt(8 * G * total_mass)
        T_btz = btz_temperature(r_plus, ell)
        S_btz = btz_entropy(r_plus, G)
    else:
        r_plus = 0
        T_btz = 0
        S_btz = 0

    # Growth rate of the negative mode (in the linearized approximation)
    # For gravitational dynamics (second-order): omega^2 = -|lambda| * (restoring force scale)
    # The instability timescale is ~ 1/sqrt(|lambda|)
    growth_rate = math.sqrt(abs(lam)) if lam < 0 else 0

    return {
        'N': N,
        'xi': xi,
        'Gm': Gm,
        'm_crit': m,
        'lambda_crit': lam,
        'unstable': lam < 0,
        'total_mass_G': E_G,
        'exceeds_btz_threshold': total_mass > 0,
        'btz_horizon': r_plus,
        'btz_temperature': T_btz,
        'btz_entropy': S_btz,
        'growth_rate': growth_rate,
        'entropy_gap': S_btz,  # tunneling suppression
        'decay_endpoint': 'BTZ' if total_mass > 0 else 'thermal_AdS',
    }


# ============================================================
# One-loop determinant (spectral bound)
# ============================================================

def one_loop_bound(lambda1_spatial):
    """Bound on the one-loop correction from the spectral gap.

    |delta C1| <= 2 / (4*pi*lambda_1)

    where lambda_1 is the first nonzero eigenvalue of the Laplacian
    on the spatial slice.

    For the Bolza surface: lambda_1 ≈ 3.839 (Strohmaier-Uski 2013).
    Bound: |delta C1| <= 0.052.

    For the modular surface: lambda_1 ≈ 91.1 (Hejhal).
    Bound: |delta C1| <= 0.0017.
    """
    return 2.0 / (4 * math.pi * lambda1_spatial)


def one_loop_shift_critical_N(lambda1_spatial, N=7):
    """Check if the one-loop correction can shift N_crit from 7.

    At N=7, lambda_3 = 0 exactly (flat plane).
    The one-loop correction shifts: lambda_3 -> 0 + delta C1.
    If |delta C1| < f_max(7) - (N-1) = 0 (marginal), even a tiny
    positive delta C1 stabilizes the heptagon.

    But delta C1 can be positive or negative depending on the
    spatial geometry.
    """
    bound = one_loop_bound(lambda1_spatial)
    m = N // 2
    f_max = m * (N - m) / 2
    C1_flat = N - 1
    gap = C1_flat - f_max  # = 0 for N=7

    return {
        'N': N,
        'lambda_flat': gap,
        'one_loop_bound': bound,
        'can_shift': bound > abs(gap),
        'diagnosis': ('marginal: one-loop correction determines stability'
                      if gap == 0 else
                      f'gap = {gap}, bound = {bound:.4f}'),
    }
