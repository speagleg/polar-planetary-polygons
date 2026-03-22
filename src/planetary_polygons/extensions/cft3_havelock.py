r"""Havelock decomposition in CFT_3 (the boundary of AdS_4).

The 2D palindromic hierarchy on the Poincaré disk:
  λ_m = C₁(ξ) - m(N-m)/2
  C₁(ξ) = C₁(1/ξ)  (conformal inversion invariance → palindromic)

The 3D generalisation on S²:
  N heavy operators at equally-spaced points on a ring at colatitude θ₀
  on S² (the boundary of AdS₄).

  Interaction: V(x,y) = |x-y|^{-2Δ}  (the CFT two-point function)
  where Δ is the conformal dimension.

  For Δ → 0: V → -log|x-y| (the 2D case, recovered).
  For Δ > 0: the interaction is STILL Möbius-invariant on S².

  The Havelock decomposition:
    λ_m^{(3)} = C₁^{(3)}(θ₀, Δ) - f^{(3)}(m, N, Δ)

  where f^{(3)} is the angular Casimir (from the Z_N Fourier decomposition
  of V on the ring) and C₁^{(3)} is the confining potential (from the
  radial/polar second variation).

KEY QUESTION: does C₁^{(3)}(θ₀) = C₁^{(3)}(π - θ₀)?
  (the conformal inversion of S² maps θ₀ ↦ π - θ₀)

If yes: the threshold equation is palindromic, and the palindromic
hierarchy extends to 3+1D via AdS₄/CFT₃.
"""

import math
import numpy as np


# ============================================================
# Geometry: ring of N points on S²
# ============================================================

def ring_positions_s2(N, theta0):
    """N equally-spaced points on a ring at colatitude θ₀ on S².

    Returns array of shape (N, 3) in Cartesian coordinates on the unit sphere.
    """
    positions = np.zeros((N, 3))
    for k in range(N):
        phi = 2 * math.pi * k / N
        positions[k, 0] = math.sin(theta0) * math.cos(phi)
        positions[k, 1] = math.sin(theta0) * math.sin(phi)
        positions[k, 2] = math.cos(theta0)
    return positions


def chord_distance_s2(pos_j, pos_k):
    """Euclidean (chord) distance between two points on the unit sphere."""
    diff = pos_j - pos_k
    return np.sqrt(np.sum(diff**2))


def chord_distance_ring(N, theta0, j, k):
    """Chord distance between vertices j and k of the N-ring at colatitude θ₀.

    |x_j - x_k|² = 2sin²θ₀(1 - cos(2π(j-k)/N)) + 0
                  = 4sin²θ₀ sin²(π(j-k)/N)

    So |x_j - x_k| = 2sinθ₀ |sin(π(j-k)/N)|.
    """
    return 2 * math.sin(theta0) * abs(math.sin(math.pi * (j - k) / N))


# ============================================================
# The interaction energy for general Δ
# ============================================================

def pairwise_energy(N, theta0, Delta):
    r"""Energy of N-ring on S² with interaction V = |x-y|^{-2Δ}.

    E = Σ_{j<k} |x_j - x_k|^{-2Δ}

    For Δ → 0: E → -Σ log|x_j - x_k| (the 2D case, up to a constant).
    """
    E = 0.0
    for j in range(N):
        for k in range(j + 1, N):
            d = chord_distance_ring(N, theta0, j, k)
            if d < 1e-30:
                return float('inf')
            if abs(Delta) < 1e-10:
                E -= math.log(d)
            else:
                E += d ** (-2 * Delta)
    return E


def log_pairwise_energy(N, theta0, Delta):
    r"""Logarithmic energy: E = -Σ_{j<k} log|x_j - x_k|.

    This is the Δ→0 limit, and also the derivative dE/dΔ|_{Δ=0}.
    """
    return pairwise_energy(N, theta0, 0)


# ============================================================
# Angular Hessian (Z_N Fourier decomposition)
# ============================================================

def angular_hessian_eigenvalue_s2(N, m, theta0, Delta, eps=1e-6):
    r"""The m-th Z_N eigenvalue of the angular Hessian of E on S².

    Computed by finite differences: perturb the azimuthal angles
    φ_k → φ_k + a·cos(2πmk/N) and take d²E/da².

    For Δ = 0: should give m(N-m)/2 (the 2D Havelock Casimir).
    For Δ > 0: gives f^{(3)}(m, N, Δ, θ₀).
    """
    def energy_perturbed(a):
        E = 0.0
        for j in range(N):
            for k in range(j + 1, N):
                phi_j = 2 * math.pi * j / N + a * math.cos(2 * math.pi * m * j / N)
                phi_k = 2 * math.pi * k / N + a * math.cos(2 * math.pi * m * k / N)
                # Chord distance with perturbed azimuths
                xj = np.array([math.sin(theta0) * math.cos(phi_j),
                               math.sin(theta0) * math.sin(phi_j),
                               math.cos(theta0)])
                xk = np.array([math.sin(theta0) * math.cos(phi_k),
                               math.sin(theta0) * math.sin(phi_k),
                               math.cos(theta0)])
                d = np.sqrt(np.sum((xj - xk)**2))
                if d < 1e-30:
                    return float('inf')
                if abs(Delta) < 1e-10:
                    E -= math.log(d)
                else:
                    E += d ** (-2 * Delta)
        return E

    E_p = energy_perturbed(eps)
    E_0 = energy_perturbed(0)
    E_m = energy_perturbed(-eps)
    return (E_p - 2 * E_0 + E_m) / eps**2


# ============================================================
# Radial (polar) second variation → C₁
# ============================================================

def radial_second_variation(N, theta0, Delta, eps=1e-5):
    r"""Second variation of E with respect to colatitude θ₀.

    d²E/dθ₀² at the N-ring configuration.
    This gives the "confining potential" C₁^{(3)}.
    """
    E_p = pairwise_energy(N, theta0 + eps, Delta)
    E_0 = pairwise_energy(N, theta0, Delta)
    E_m = pairwise_energy(N, theta0 - eps, Delta)
    return (E_p - 2 * E_0 + E_m) / eps**2


def C1_from_radial(N, theta0, Delta, eps=1e-5):
    r"""Extract C₁^{(3)} from the radial second variation.

    For the Havelock decomposition: the radial eigenvalue of the
    unconstrained Hessian for the breathing mode is related to C₁
    by a normalization that depends on the number of pairs.

    Convention: match the 2D result C₁ = (N-1)(1+ξ²)/(1-ξ)²
    in the Δ → 0, θ₀ → 0 limit.
    """
    d2E = radial_second_variation(N, theta0, Delta, eps)
    # In the 2D case: d²E/du² = N·C₁ where u = log R.
    # Here: u = θ₀, so the normalization may differ.
    return d2E


# ============================================================
# THE KEY TEST: conformal inversion invariance on S²
# ============================================================

def test_conformal_inversion(N, Delta, theta_values=None):
    r"""Test whether C₁^{(3)}(θ₀) = C₁^{(3)}(π - θ₀).

    Conformal inversion of S² maps the north pole to the south pole:
    θ₀ ↦ π - θ₀.  If the interaction |x-y|^{-2Δ} is Möbius-invariant
    on S², then the energy at colatitude θ₀ should equal the energy
    at colatitude π - θ₀.

    Returns dict with comparison data.
    """
    if theta_values is None:
        theta_values = [0.1, 0.3, 0.5, 0.7, 1.0, 1.2, math.pi/4, math.pi/3]

    results = []
    for theta in theta_values:
        theta_inv = math.pi - theta
        if theta_inv < 0.01 or theta_inv > math.pi - 0.01:
            continue

        E = pairwise_energy(N, theta, Delta)
        E_inv = pairwise_energy(N, theta_inv, Delta)

        d2E = radial_second_variation(N, theta, Delta)
        d2E_inv = radial_second_variation(N, theta_inv, Delta)

        results.append({
            'theta': theta,
            'theta_inv': theta_inv,
            'E': E,
            'E_inv': E_inv,
            'E_match': abs(E - E_inv) < 1e-6 * max(abs(E), 1),
            'E_diff': E - E_inv,
            'd2E': d2E,
            'd2E_inv': d2E_inv,
            'd2E_diff': d2E - d2E_inv,
        })

    return results


def test_angular_casimir_metric_independence(N, Delta, theta_values=None):
    r"""Test whether the angular Casimir f^{(3)}(m,N) is independent of θ₀.

    In 2D: f(m,N) = m(N-m)/2 is metric-independent (Theorem 3.2).
    In 3D with Δ > 0: does f^{(3)} depend on θ₀?

    If yes: the Havelock decomposition FAILS in 3D (modes couple).
    If no: the decomposition extends, and palindromic is possible.
    """
    if theta_values is None:
        theta_values = [0.2, 0.5, 0.8, 1.0, 1.3]

    results = {}
    for m in range(1, N):
        eigenvalues = []
        for theta in theta_values:
            mu = angular_hessian_eigenvalue_s2(N, m, theta, Delta)
            eigenvalues.append((theta, mu))
        results[m] = eigenvalues

    return results


# ============================================================
# The stereographic palindromic parameter
# ============================================================

def stereographic_xi(theta0):
    r"""The stereographic parameter ξ = tan²(θ₀/2).

    This maps θ₀ ∈ (0, π) to ξ ∈ (0, ∞).
    Conformal inversion θ₀ → π - θ₀ maps ξ → 1/ξ:
      tan²((π-θ₀)/2) = cot²(θ₀/2) = 1/tan²(θ₀/2) = 1/ξ.

    So the palindromic parameter for S² is ξ = tan²(θ₀/2),
    and conformal inversion IS the palindromic involution ξ → 1/ξ.
    """
    return math.tan(theta0 / 2) ** 2


def theta_from_xi(xi):
    """Colatitude from stereographic parameter: θ₀ = 2 arctan(√ξ)."""
    return 2 * math.atan(math.sqrt(xi))


# ============================================================
# Full Havelock computation on S²
# ============================================================

def havelock_s2(N, theta0, Delta=0, n_modes=None):
    r"""Full Havelock decomposition on S² for N-ring at colatitude θ₀.

    Returns dict with:
      - angular eigenvalues f^{(3)}(m, N) for each mode m
      - radial stiffness (related to C₁^{(3)})
      - conformal inversion test (E(θ) vs E(π-θ))
      - palindromic parameter ξ = tan²(θ₀/2)
    """
    if n_modes is None:
        n_modes = N

    xi = stereographic_xi(theta0)

    # Angular eigenvalues
    angular = {}
    for m in range(n_modes):
        mu = angular_hessian_eigenvalue_s2(N, m, theta0, Delta)
        angular[m] = mu

    # Radial stiffness
    d2E = radial_second_variation(N, theta0, Delta)

    # Conformal inversion
    theta_inv = math.pi - theta0
    E_here = pairwise_energy(N, theta0, Delta)
    E_inv = pairwise_energy(N, theta_inv, Delta)

    return {
        'N': N,
        'theta0': theta0,
        'theta0_deg': math.degrees(theta0),
        'Delta': Delta,
        'xi': xi,
        'angular_eigenvalues': angular,
        'radial_stiffness': d2E,
        'E': E_here,
        'E_inverted': E_inv,
        'E_palindromic': abs(E_here - E_inv) < 1e-6 * max(abs(E_here), 1),
        'E_diff': E_here - E_inv,
    }
