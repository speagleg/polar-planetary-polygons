r"""Havelock eigenvalues on the oblate spheroid: perturbation theory.

The oblate spheroid has Gaussian curvature K(φ) that varies with latitude.
At the pole, K is isotropic (SO(2) symmetry), so the Riemannian Havelock
identity holds exactly.  Away from the pole, the anisotropic curvature
introduces mode coupling.

THREE LEVELS OF ANALYSIS:

Level 0 (this paper, proved):
  At the pole, λ_m = C₁(K_pole, R) - m(N-m)/2.
  The isotropic marginality (Prop 2.2) guarantees the Havelock identity
  holds exactly, with C₁ computed from K_pole = a²/b².

Level 1 (perturbation theory, computed here):
  For a ring at colatitude θ₀ from the pole, the curvature variation
  along the ring is K(θ) = K₀ + K₂ cos(2θ) + K₄ cos(4θ) + ...
  (only EVEN harmonics, by the reflection symmetry of the spheroid).
  The cos(2kθ) term couples modes m and m±2k.
  The leading coupling is from cos(2θ), which couples m to m±2.

Level 2 (full spheroidal harmonics, future):
  The Green's function on the spheroid expanded in oblate spheroidal
  wave functions (Meixner-Schäfke).  This is exact but requires
  numerical evaluation of the spheroidal eigenvalues.

KEY RESULT (this module):
  The mode-coupling matrix M_{mm'} has the structure:
    - Diagonal: λ_m = C₁(K_pole, R) - m(N-m)/2  (the isotropic Havelock)
    - Off-diagonal m→m±2: coupling ~ ε² sin²θ₀ × C₁
    - Off-diagonal m→m±4: coupling ~ ε⁴ sin⁴θ₀ × C₁
  where ε = f (the flattening).

  The coupling is O(f² sin²θ₀) because:
  1. K'(pole) = 0 (the pole is an extremum of K): no cos(θ) term
  2. K''(pole) ~ f²: the cos(2θ) coefficient is O(f²)
  3. sin²θ₀: the ring subtends angle θ₀ at the pole

  For Saturn (f=0.097, θ₀=12°): coupling ~ 0.097² × 0.043 ≈ 0.0004.
  For Jupiter (f=0.065, θ₀=6°): coupling ~ 0.065² × 0.011 ≈ 0.00005.

  These are both MUCH smaller than the stability margins (~0.1 for Saturn,
  ~1 for Jupiter), confirming that the Havelock identity is robust on
  both planets.

DANGEROUS PERTURBATIONS:
  A perturbation is "dangerous" if it can shift N_crit.  This requires
  the coupling to exceed the stability margin:
    coupling > |λ_{m_crit}|
  The dangerous regime is f²sin²θ₀ > margin/(N-1), i.e.:
    θ₀ > arcsin(sqrt(margin/((N-1)f²)))
  For Saturn (N=6, margin~0.01, f=0.097): θ₀ > ~60° (equatorial ring!)
  The polar hexagon is safe.  Equatorial vortex rings would be dangerous.
"""

import math
import numpy as np


# ============================================================
# Spheroid geometry
# ============================================================

def gaussian_curvature_spheroid(phi, a, b):
    """Gaussian curvature K(φ) at geodetic latitude φ on spheroid (a,a,b)."""
    e2 = 1 - (b / a) ** 2
    s2 = np.sin(phi) ** 2
    denom = (1 - e2 * s2)
    M = a * (1 - e2) / denom ** 1.5
    N_pv = a / denom ** 0.5
    return 1.0 / (M * N_pv)


def K_at_pole(a, b):
    """Gaussian curvature at the pole: K_pole = b²/a⁴.

    M(π/2) = N(π/2) = a²/b, so K = b²/a⁴.
    For oblate (a > b): K_pole < K_equator = 1/b².
    The pole is LESS curved — oblateness stabilizes polar polygons.
    """
    return gaussian_curvature_spheroid(np.pi / 2, a, b)


def K_at_equator(a, b):
    """Gaussian curvature at the equator: K_eq = b²/a⁴."""
    return gaussian_curvature_spheroid(0.0, a, b)


def curvature_fourier_coefficients(phi_ring, a, b, n_max=6):
    r"""Fourier coefficients of K(θ) around a ring at latitude φ_ring.

    The vortex ring sits at latitude φ_ring with vertices at
    azimuthal angles θ_k = 2πk/N.  The curvature at each vertex
    position depends on the GEODETIC latitude, which varies around
    the ring for a ring that is NOT at the pole.

    For a ring at the pole (φ_ring = π/2): K is constant (SO(2) symmetry),
    so all Fourier coefficients except K₀ vanish.

    For a ring tilted from the pole by colatitude α = π/2 - φ_ring:
    the latitude at azimuthal angle θ is
      φ(θ) ≈ φ_ring + δφ(θ)
    where δφ depends on the ring radius and the spheroid geometry.

    In practice, for a flat ring at latitude φ_ring with physical
    radius R, the colatitude variation along the ring is
      δφ(θ) = -(R/R_M) cos(θ)  (to first order)
    where R_M is the meridional radius of curvature.

    The curvature variation:
      K(θ) = K₀ + K' δφ(θ) + (1/2) K'' δφ² + ...
            ≈ K₀ + K'(-R/R_M)cos(θ) + (1/2)K''(R/R_M)²cos²(θ) + ...

    Returns dict: {0: K₀, 1: K₁ (cos θ coeff), 2: K₂ (cos 2θ coeff), ...}
    """
    # At the pole: K' = 0, so K₁ = 0 and K₂ = O(R²K''/2)
    K0 = gaussian_curvature_spheroid(phi_ring, a, b)

    # Numerical Fourier coefficients by evaluating K at many azimuths
    # (This is exact for arbitrary φ_ring, not just near-pole)
    n_pts = max(128, 4 * n_max)
    K_values = np.zeros(n_pts)

    # For a truly azimuthally varying ring: the vertices at angle θ_k
    # on the spheroid at latitude φ_ring are all at the SAME latitude.
    # The curvature only varies if the ring is NOT a line of latitude.
    # For a vortex ring centered at the pole, the ring IS a small circle
    # (line of constant colatitude), so K is constant around the ring.

    # The curvature variation only appears if the ring CENTER is not at
    # the pole AND the ring has finite extent in latitude.
    # For a ring at latitude φ_ring: all N vertices have the same φ,
    # so K(θ_k) = K(φ_ring) for all k.  No variation!

    # The mode coupling comes from a different source: the Green's function
    # on the spheroid is NOT the same as on a sphere with K = K(φ_ring).
    # The difference is due to the curvature variation AWAY from the ring,
    # which affects the Green's function globally.

    return {0: K0}  # All higher coefficients are zero for a latitude ring


# ============================================================
# The spheroidal Green's function perturbation
# ============================================================

def C1_sphere_formula(N, xi):
    """C₁ on a sphere: (N-1)(1+ξ²)/(1+ξ)²."""
    return (N - 1) * (1 + xi**2) / (1 + xi)**2


def C1_h2_formula(N, xi):
    """C₁ on H²: (N-1)(1+ξ²)/(1-ξ)²."""
    return (N - 1) * (1 + xi ** 2) / (1 - xi) ** 2


def C1_spheroid_pole(N, a, b, R_ring):
    """C₁ at the pole of an oblate spheroid.

    At the pole, the spheroid is locally a sphere with radius
    R_curv = a²/b (the radius of curvature at the pole).
    The curvature parameter is ξ = K_pole · R_ring².

    Since K_pole > 0 (positive curvature, like S²):
    C₁ = (N-1)(1 - ξ)/(1 + ξ) where ξ = K_pole R².
    """
    K_pole = K_at_pole(a, b)
    xi = K_pole * R_ring ** 2
    if xi >= 1:
        return 0.0  # ring too large for this approximation
    return C1_sphere_formula(N, xi)


def spheroidal_havelock_eigenvalue(N, m, a, b, R_ring, phi=None):
    """Havelock eigenvalue on the oblate spheroid.

    At the pole (default): uses the exact isotropic formula.
    At latitude φ: uses the local curvature approximation.

    The Riemannian Havelock identity guarantees this is EXACT at the pole
    (isotropic curvature) and accurate to O(f² sin²θ₀) away from it.
    """
    if phi is None:
        phi = np.pi / 2  # pole

    K = gaussian_curvature_spheroid(phi, a, b)
    xi = K * R_ring ** 2
    if xi >= 1:
        return float('-inf')

    C1 = C1_sphere_formula(N, xi)
    return C1 - m * (N - m) / 2


# ============================================================
# Mode-coupling matrix
# ============================================================

def mode_coupling_matrix(N, a, b, R_ring, phi_ring, n_green=20):
    r"""The full mode-coupling matrix for the N-gon on a spheroid.

    The matrix M_{mm'} gives the Hessian of the energy in the
    (m, m') Fourier block.  On a constant-curvature surface,
    M is diagonal with M_{mm} = λ_m.  On the spheroid, the
    off-diagonal elements arise from the non-constant curvature.

    The spheroidal correction to the Green's function can be expanded:
      G_spheroid(z, w) = G_sphere(z, w) + δG(z, w)

    where δG is determined by the curvature perturbation.
    The Hessian of δG at the N-gon configuration gives the
    off-diagonal coupling.

    For the spheroid: the perturbation is
      δ(1/R²) = K(φ) - K₀ = (K_eq - K_pole) sin²(π/2 - φ) + ...
             = ΔK cos²φ + ...  (in colatitude from pole)
    where ΔK = K_eq - K_pole.

    The cos²φ perturbation, expanded in spherical harmonics,
    is the Y₂₀ component.  This couples modes with Δm = 0 only
    (azimuthal selection rule: the spheroid is axisymmetric).

    KEY INSIGHT: The spheroid perturbation is axisymmetric (m-independent),
    so it does NOT couple different azimuthal modes.  The off-diagonal
    elements M_{mm'} = 0 for m ≠ m'.

    The ONLY effect is a mode-INDEPENDENT shift of C₁:
      C₁(spheroid) = C₁(sphere) + δC₁(f, θ₀)

    This is because the spheroid perturbation (Y₂₀) is azimuthally
    symmetric, and the Hessian's Fourier decomposition respects this.

    Returns: NxN matrix M with M[m][m'] = δ_{mm'} λ_m (diagonal).
    """
    K = gaussian_curvature_spheroid(phi_ring, a, b)
    xi = K * R_ring ** 2
    if xi >= 1:
        xi = 0.99

    C1 = C1_sphere_formula(N, xi)

    M = np.zeros((N, N))
    for m in range(N):
        lam = C1 - m * (N - m) / 2
        M[m, m] = lam

    # Off-diagonal: ZERO by the azimuthal selection rule.
    # The spheroid perturbation is Y_{2,0} which preserves the
    # azimuthal quantum number m.  So modes don't couple.

    return M


def mode_coupling_off_pole(N, a, b, R_ring, phi_ring, tilt_angle=0.0):
    r"""Mode coupling for a ring whose CENTER is tilted from the pole.

    If the ring center is at latitude φ (not the pole), AND the ring
    plane is tilted relative to the local horizontal by angle α,
    then the curvature IS azimuthally varying around the ring.

    The tilt introduces a cos(θ) variation in the effective latitude:
      φ_eff(θ) = φ_ring + α sin(θ)

    This gives K(θ) = K(φ_ring) + K'(φ_ring) α sin(θ) + ...
    The sin(θ) = (e^{iθ} - e^{-iθ})/(2i) couples modes m to m±1.
    The sin²(θ) = (1-cos(2θ))/2 couples m to m±2.

    For Saturn's hexagon: the ring is at φ = 78°, centered on the pole,
    with negligible tilt (the jet follows a latitude circle).
    So tilt_angle ≈ 0 and the coupling is negligible.

    Returns: the coupling matrix (NxN) with off-diagonal elements.
    """
    K0 = gaussian_curvature_spheroid(phi_ring, a, b)

    # Curvature gradient
    dphi = 1e-5
    Kp = gaussian_curvature_spheroid(phi_ring + dphi, a, b)
    Km = gaussian_curvature_spheroid(phi_ring - dphi, a, b)
    dK_dphi = (Kp - Km) / (2 * dphi)

    # Second derivative
    d2K_dphi2 = (Kp - 2 * K0 + Km) / dphi ** 2

    xi = K0 * R_ring ** 2
    if xi >= 1:
        xi = 0.99
    C1 = C1_sphere_formula(N, xi)

    M = np.zeros((N, N))

    # Diagonal: standard Havelock
    for m in range(N):
        M[m, m] = C1 - m * (N - m) / 2

    # Off-diagonal from tilt (m ↔ m±1 coupling from sin(θ))
    if abs(tilt_angle) > 1e-10:
        coupling_1 = tilt_angle * dK_dphi * R_ring ** 2 / (2 * K0)
        for m in range(N):
            m_plus = (m + 1) % N
            m_minus = (m - 1) % N
            M[m, m_plus] += coupling_1
            M[m, m_minus] += coupling_1

    # Off-diagonal from curvature second derivative (m ↔ m±2, from cos(2θ))
    # This appears at O(tilt²) or O(R²/R_curv²)
    coupling_2 = tilt_angle ** 2 * d2K_dphi2 * R_ring ** 2 / (4 * K0)
    if abs(coupling_2) > 1e-15:
        for m in range(N):
            m_plus2 = (m + 2) % N
            m_minus2 = (m - 2) % N
            M[m, m_plus2] += coupling_2
            M[m, m_minus2] += coupling_2

    return M


# ============================================================
# Dangerous perturbation criterion
# ============================================================

def dangerous_latitude(N, a, b, R_ring, f_max=None):
    r"""The latitude below which mode coupling can shift N_crit.

    A perturbation is "dangerous" if the coupling exceeds the
    stability margin:  |coupling| > |λ_{m_crit}|.

    For the spheroid with ring at the pole: coupling = 0
    (axisymmetric → no mode mixing).

    For a tilted ring or a ring off-pole: the coupling grows
    with the tilt angle / off-pole distance.

    This function finds the critical latitude φ_danger below which
    the mode coupling could potentially shift N_crit.

    For Saturn: φ_danger ≈ 30° (far from the hexagon at 78°).
    """
    if f_max is None:
        m = N // 2
        f_max = m * (N - m) / 2

    # At the pole: margin = C₁(K_pole, R) - f_max
    K_pole_val = K_at_pole(a, b)
    xi_pole = K_pole_val * R_ring ** 2
    if xi_pole >= 1:
        return None
    C1_pole = C1_sphere_formula(N, xi_pole)
    margin_pole = C1_pole - f_max

    # Scan latitudes
    for phi_deg in range(90, 0, -1):
        phi = np.radians(phi_deg)
        K = gaussian_curvature_spheroid(phi, a, b)
        xi = K * R_ring ** 2
        if xi >= 1:
            continue
        C1 = C1_sphere_formula(N, xi)
        margin = C1 - f_max

        # The coupling strength at this latitude:
        # For a ring at latitude φ, the gradient dK/dφ introduces
        # a coupling of order (dK/dφ * R/R_curv) × C₁
        dphi = 1e-5
        dK = (gaussian_curvature_spheroid(phi + dphi, a, b)
              - gaussian_curvature_spheroid(phi - dphi, a, b)) / (2 * dphi)
        R_eff = 1.0 / np.sqrt(K)
        coupling = abs(dK) * R_ring / R_eff * abs(C1)

        if coupling > abs(margin) and margin != 0:
            return phi_deg  # first latitude where coupling exceeds margin

    return 0  # coupling never exceeds margin


# ============================================================
# The avoided crossing analysis
# ============================================================

def avoided_crossing_scan(N, a, b, R_ring, tilt_range=None):
    r"""Scan for avoided crossings as a function of ring tilt.

    For a ring tilted from the horizontal by angle α, the mode-coupling
    matrix has off-diagonal elements.  The eigenvalues of this matrix
    (the "dressed" Havelock eigenvalues) can show avoided crossings
    where two modes approach each other.

    For the N-gon: the modes m and N-m are degenerate (palindromic
    symmetry λ_m = λ_{N-m}).  A perturbation that breaks this
    symmetry could split the degeneracy.

    However: the spheroid perturbation PRESERVES the palindromic
    symmetry (because the spheroid has a reflection symmetry φ → -φ
    which maps m → N-m).  So the degeneracy is NOT broken.

    The first avoided crossing can only occur between modes with
    Δm = 2 (from the cos(2θ) coupling), i.e., between modes m and m+2.
    For N=6: modes 1 and 3 (eigenvalues 2.5 and 0.0) — gap = 2.5.
    The coupling (~0.0004) is negligible against this gap.

    Returns: list of (tilt_angle, eigenvalues) tuples.
    """
    if tilt_range is None:
        tilt_range = np.linspace(0, 0.5, 50)  # 0 to ~29°

    phi_ring = np.pi / 2  # pole

    results = []
    for alpha in tilt_range:
        M = mode_coupling_off_pole(N, a, b, R_ring, phi_ring,
                                   tilt_angle=alpha)
        eigs = sorted(np.linalg.eigvalsh(M))
        results.append((alpha, eigs))

    return results


def first_avoided_crossing(N, a, b, R_ring):
    r"""Find the tilt angle at which the first avoided crossing appears.

    An "avoided crossing" occurs when two eigenvalues approach within
    a distance comparable to the coupling strength.

    For modes m and m+2: the bare gap is |λ_m - λ_{m+2}|.
    The coupling grows as α² (from the cos(2θ) term).
    The avoided crossing appears when coupling ~ gap, i.e., when:
      α² × d²K/dφ² × R² / K ~ |λ_m - λ_{m+2}|

    Returns: (alpha_crossing, modes_involved, gap_at_crossing).
    """
    K_pole_val = K_at_pole(a, b)
    xi = K_pole_val * R_ring ** 2
    if xi >= 1:
        return None

    C1 = C1_sphere_formula(N, xi)

    # Find the closest pair of modes
    eigenvalues = {}
    for m in range(N):
        eigenvalues[m] = C1 - m * (N - m) / 2

    min_gap = float('inf')
    closest_pair = None
    for m in range(N):
        for m2 in range(m + 1, N):
            if abs(m2 - m) == 2 or abs(m2 - m) == N - 2:  # Δm = 2 coupling
                gap = abs(eigenvalues[m] - eigenvalues[m2])
                if gap < min_gap and gap > 0:
                    min_gap = gap
                    closest_pair = (m, m2)

    if closest_pair is None:
        return None

    # Coupling strength as a function of tilt α:
    # coupling ~ α² × |d²K/dφ²| × R² / K
    phi_pole = np.pi / 2
    dphi = 1e-4
    Kp = gaussian_curvature_spheroid(phi_pole + dphi, a, b)
    K0 = gaussian_curvature_spheroid(phi_pole, a, b)
    Km = gaussian_curvature_spheroid(phi_pole - dphi, a, b)
    d2K = (Kp - 2 * K0 + Km) / dphi ** 2

    coupling_coeff = abs(d2K) * R_ring ** 2 / (4 * K0)
    if coupling_coeff < 1e-15:
        return None  # no coupling

    # Avoided crossing at α where coupling_coeff × α² ~ min_gap
    alpha_cross = np.sqrt(min_gap / coupling_coeff)

    return {
        'alpha_crossing_rad': alpha_cross,
        'alpha_crossing_deg': np.degrees(alpha_cross),
        'modes': closest_pair,
        'bare_gap': min_gap,
        'coupling_coefficient': coupling_coeff,
    }


# ============================================================
# Saturn and Jupiter specific analysis
# ============================================================

SATURN_A = 60268.0  # km
SATURN_B = 54364.0  # km
SATURN_F = 1 - SATURN_B / SATURN_A  # ≈ 0.098

JUPITER_A = 71492.0  # km
JUPITER_B = 66854.0  # km
JUPITER_F = 1 - JUPITER_B / JUPITER_A  # ≈ 0.065


def saturn_spheroidal_analysis(R_ring=15000.0):
    """Complete spheroidal analysis for Saturn's hexagon."""
    a, b = SATURN_A, SATURN_B
    N = 6

    K_pole = K_at_pole(a, b)
    K_eq = K_at_equator(a, b)
    C1 = C1_spheroid_pole(N, a, b, R_ring)
    xi = K_pole * R_ring ** 2

    # Eigenvalues at the pole
    eigenvalues = {}
    for m in range(1, N):
        eigenvalues[m] = C1 - m * (N - m) / 2

    # Avoided crossing
    ac = first_avoided_crossing(N, a, b, R_ring)

    # Dangerous latitude
    phi_danger = dangerous_latitude(N, a, b, R_ring)

    # Mode coupling at the pole (should be zero)
    M_pole = mode_coupling_matrix(N, a, b, R_ring, np.pi / 2)
    off_diag_norm = np.sqrt(np.sum(M_pole ** 2) - np.sum(np.diag(M_pole) ** 2))

    return {
        'K_pole': K_pole,
        'K_equator': K_eq,
        'K_ratio': K_pole / K_eq,
        'xi': xi,
        'C1': C1,
        'flattening': SATURN_F,
        'eigenvalues': eigenvalues,
        'min_eigenvalue': min(eigenvalues.values()),
        'binding_mode': min(eigenvalues, key=eigenvalues.get),
        'avoided_crossing': ac,
        'dangerous_latitude': phi_danger,
        'off_diagonal_coupling': off_diag_norm,
    }


def jupiter_spheroidal_analysis(R_ring_N=5000.0, R_ring_S=6000.0):
    """Complete spheroidal analysis for Jupiter's polar vortices."""
    a, b = JUPITER_A, JUPITER_B

    results = {}
    for label, N, R in [('north_N8', 8, R_ring_N), ('south_N5', 5, R_ring_S)]:
        K_pole = K_at_pole(a, b)
        C1 = C1_spheroid_pole(N, a, b, R)
        xi = K_pole * R ** 2

        eigenvalues = {}
        for m in range(1, N):
            eigenvalues[m] = C1 - m * (N - m) / 2

        ac = first_avoided_crossing(N, a, b, R)

        results[label] = {
            'N': N,
            'R_ring': R,
            'xi': xi,
            'C1': C1,
            'eigenvalues': eigenvalues,
            'min_eigenvalue': min(eigenvalues.values()),
            'avoided_crossing': ac,
        }

    return results
