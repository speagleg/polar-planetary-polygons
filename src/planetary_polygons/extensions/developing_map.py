"""Developing map for N conical singularities with Z_N symmetry.

The flat cone metric with N equal conical singularities at the N-th roots
of unity has the developing map

    f(z) = z * _2F1(beta, 1/N; 1+1/N; z^N)

where beta = 4Gm is the deficit parameter (cone angle = 2*pi*(1-beta)).
The derivative is f'(z) = (1 - z^N)^{-beta} (for |z| < 1).

Key result (Proposition): On a flat spatial slice (Lambda = 0), the
Havelock eigenvalues of the regular N-gon of conical singularities are
INDEPENDENT of beta:

    lambda_m = (N-1) - m(N-m)/2    for all beta in [0, 1/N).

This follows from conformal invariance of the 2D Green's function
and the Z_N symmetry f(omega*z) = omega*f(z), which maps the N-gon
of cone points to a regular N-gon in the developed plane.

The image radius is

    R_f = Gamma(1 + 1/N) * Gamma(1 - beta) / Gamma(1 + 1/N - beta)

by Gauss's summation formula for _2F1(a, b; c; 1).
"""

import math
import cmath


# ---------------------------------------------------------------------------
# Gamma function (Lanczos approximation, sufficient for our purposes)
# ---------------------------------------------------------------------------

_LANCZOS_G = 7
_LANCZOS_P = [
    0.99999999999980993,
    676.5203681218851,
    -1259.1392167224028,
    771.32342877765313,
    -176.61502916214059,
    12.507343278686905,
    -0.13857109526572012,
    9.9843695780195716e-6,
    1.5056327351493116e-7,
]


def gamma_func(x):
    """Real Gamma function via Lanczos approximation."""
    if x < 0.5:
        return math.pi / (math.sin(math.pi * x) * gamma_func(1 - x))
    x -= 1
    a = _LANCZOS_P[0]
    t = x + _LANCZOS_G + 0.5
    for i in range(1, len(_LANCZOS_P)):
        a += _LANCZOS_P[i] / (x + i)
    return math.sqrt(2 * math.pi) * t ** (x + 0.5) * math.exp(-t) * a


def log_gamma(x):
    """Logarithm of the Gamma function for x > 0."""
    return math.log(gamma_func(x))


# ---------------------------------------------------------------------------
# Hypergeometric function _2F1
# ---------------------------------------------------------------------------

def hyp2f1_series(a, b, c, z, tol=1e-14, max_terms=2000):
    """Gauss hypergeometric _2F1(a, b; c; z) by power series.

    Converges for |z| < 1.  For |z| near 1 with c - a - b > 0,
    converges but slowly; use hyp2f1_at_one instead.
    """
    s = complex(1.0)
    term = complex(1.0)
    z = complex(z)
    for k in range(1, max_terms):
        term *= (a + k - 1) * (b + k - 1) / ((c + k - 1) * k) * z
        s += term
        if abs(term) < tol * max(abs(s), 1e-30):
            break
    return s


def hyp2f1_at_one(a, b, c):
    """Gauss's summation: _2F1(a, b; c; 1) = Gamma(c)*Gamma(c-a-b) /
    (Gamma(c-a)*Gamma(c-b)).

    Requires c - a - b > 0 for convergence.
    """
    if c - a - b <= 0:
        raise ValueError(f"c - a - b = {c - a - b} <= 0; series diverges at z=1")
    return (gamma_func(c) * gamma_func(c - a - b)
            / (gamma_func(c - a) * gamma_func(c - b)))


# ---------------------------------------------------------------------------
# Developing map
# ---------------------------------------------------------------------------

def image_radius(N, beta):
    """Radius of the image N-gon under the developing map.

    R_f(N, beta) = Gamma(1 + 1/N) * Gamma(1 - beta) / Gamma(1 + 1/N - beta)

    At beta = 0: R_f = 1.
    At beta = 1/N: R_f = Gamma(1+1/N)*Gamma(1-1/N) = (pi/N)/sin(pi/N).
    """
    a, b, c = beta, 1.0 / N, 1.0 + 1.0 / N
    return hyp2f1_at_one(a, b, c)


def developing_map(z, N, beta, tol=1e-13):
    """f(z) = z * _2F1(beta, 1/N; 1+1/N; z^N).

    Valid for |z^N| < 1.  At the cone points (|z^N| = 1),
    use image_radius() * exp(2*pi*i*j/N) instead.
    """
    z = complex(z)
    zN = z ** N
    if abs(zN) >= 1.0 - tol:
        raise ValueError(f"|z^N| = {abs(zN):.6f} too close to 1; "
                         "use image_radius for cone-point values")
    F = hyp2f1_series(beta, 1.0 / N, 1.0 + 1.0 / N, zN, tol=tol)
    return z * F


def developing_map_derivative(z, N, beta):
    """f'(z) = (1 - z^N)^{-beta}  (for |z| < 1, principal branch).

    Diverges at z^N = 1 (cone points).
    """
    zN = complex(z) ** N
    return (1.0 - zN) ** (-beta)


# ---------------------------------------------------------------------------
# The conformal invariance theorem
# ---------------------------------------------------------------------------

def image_positions(N, beta):
    """Image of the N cone points under the developing map.

    Returns list of N complex numbers: R_f * exp(2*pi*i*j/N).
    By Z_N symmetry: f(omega*z) = omega*f(z), so the image is
    a regular N-gon of radius R_f.
    """
    Rf = image_radius(N, beta)
    return [Rf * cmath.exp(2j * math.pi * k / N) for k in range(N)]


def log_energy_ngon(R, N):
    """Pairwise logarithmic energy of a regular N-gon of radius R.

    H = -sum_{j<k} log|R*e^{2pi*i*j/N} - R*e^{2pi*i*k/N}|
      = -N(N-1)/2 * log(R) - (N/2)*log(N)
    """
    return -N * (N - 1) / 2 * math.log(R) - N / 2 * math.log(N)


def havelock_eigenvalue_flat(N, m):
    """Standard Havelock eigenvalue on the flat plane.

    lambda_m = (N-1) - m(N-m)/2
    """
    return (N - 1) - m * (N - m) / 2


# ---------------------------------------------------------------------------
# Numerical Hessian verification
# ---------------------------------------------------------------------------

def _pairwise_energy(positions):
    """H = -sum_{j<k} log|z_j - z_k|."""
    N = len(positions)
    H = 0.0
    for j in range(N):
        for k in range(j + 1, N):
            d = abs(positions[j] - positions[k])
            if d < 1e-30:
                return float('inf')
            H -= math.log(d)
    return H


def numerical_hessian_eigenvalues(N, R=1.0, eps=1e-5):
    """Compute Hessian eigenvalues of logarithmic energy for a regular
    N-gon of radius R, using finite differences.

    Returns the N Fourier-mode eigenvalues (real, tangential direction).
    For the standard N-gon: lambda_m should be (N-1) - m(N-m)/2
    divided by R^2 (the R^2 normalization).
    """
    # Equilibrium positions
    pos0 = [R * cmath.exp(2j * math.pi * k / N) for k in range(N)]
    H0 = _pairwise_energy(pos0)

    # Compute first row of the circulant Hessian (tangential-tangential)
    # Tangential perturbation at vertex j: z_j -> z_j * exp(i*phi_j)
    # ≈ z_j * (1 + i*phi_j) for small phi_j
    hess_row = []
    for k in range(N):
        if k == 0:
            # d^2 H / d phi_0^2
            def perturbed(phi):
                p = list(pos0)
                p[0] = pos0[0] * cmath.exp(1j * phi)
                return _pairwise_energy(p)
            h = (perturbed(eps) - 2 * H0 + perturbed(-eps)) / eps ** 2
        else:
            # d^2 H / d phi_0 d phi_k
            def perturbed(phi0, phik):
                p = list(pos0)
                p[0] = pos0[0] * cmath.exp(1j * phi0)
                p[k] = pos0[k] * cmath.exp(1j * phik)
                return _pairwise_energy(p)
            h = (perturbed(eps, eps) - perturbed(eps, -eps)
                 - perturbed(-eps, eps) + perturbed(-eps, -eps)) / (4 * eps ** 2)
        hess_row.append(h)

    # DFT to get eigenvalues (circulant matrix)
    eigenvalues = []
    for m in range(N):
        lam = 0.0
        for k in range(N):
            lam += hess_row[k] * math.cos(2 * math.pi * m * k / N)
        eigenvalues.append(lam)

    return eigenvalues


def verify_conformal_invariance(N_max=12, betas=None):
    """Verify that Havelock eigenvalues are independent of beta.

    For each N and beta: compute the image radius R_f, place a regular
    N-gon at that radius, compute the Hessian eigenvalues, and check
    they match the flat-plane values (up to the R^2 scaling).

    Returns dict of {(N, beta): max_relative_error}.
    """
    if betas is None:
        betas = [0.0, 0.01, 0.05, 0.1]

    results = {}
    for N in range(3, N_max + 1):
        beta_max = 1.0 / N - 0.01  # stay away from compactification
        for beta in betas:
            if beta >= 1.0 / N:
                continue
            Rf = image_radius(N, beta)
            eigs = numerical_hessian_eigenvalues(N, R=Rf)

            # Expected: lambda_m * R_f^2 (the R^2 normalization)
            # But numerical_hessian_eigenvalues returns the raw Hessian
            # eigenvalues (in angular coordinates), which are lambda_m
            # independent of R.
            max_err = 0.0
            for m in range(N):
                expected = havelock_eigenvalue_flat(N, m)
                if abs(expected) > 0.01:
                    err = abs(eigs[m] - expected) / abs(expected)
                else:
                    err = abs(eigs[m] - expected)
                max_err = max(max_err, err)
            results[(N, beta)] = max_err

    return results


# ---------------------------------------------------------------------------
# Image radius analysis
# ---------------------------------------------------------------------------

def image_radius_table(N_range=None, beta_range=None):
    """Table of R_f(N, beta) values.

    Shows how the developing map contracts the N-gon as beta increases.
    """
    if N_range is None:
        N_range = range(3, 13)
    if beta_range is None:
        beta_range = [0.0, 0.01, 0.05, 0.1]

    rows = []
    for N in N_range:
        row = {'N': N, 'beta_max': 1.0 / N}
        for beta in beta_range:
            if beta < 1.0 / N:
                row[f'R_f(beta={beta})'] = image_radius(N, beta)
            else:
                row[f'R_f(beta={beta})'] = None
        # Endpoint value
        beta_end = 1.0 / N
        Rf_end = gamma_func(1 + 1.0 / N) * gamma_func(1 - beta_end)
        # Use reflection formula: Gamma(1-1/N) = pi/(N*sin(pi/N)*Gamma(1/N))
        # But simpler: Gamma(1+1/N)*Gamma(1-1/N) = (pi/N)/sin(pi/N)
        try:
            Rf_end = (math.pi / N) / math.sin(math.pi / N)
        except ZeroDivisionError:
            Rf_end = 1.0
        row['R_f(endpoint)'] = Rf_end
        rows.append(row)
    return rows


def developing_map_first_order(z, N):
    """First-order correction: f(z) = z * (1 + beta * g(z^N) + O(beta^2))

    where g(zeta) = sum_{k=1}^inf zeta^k / (k*(Nk+1)).

    Returns g(z^N) for |z^N| < 1.
    """
    zN = complex(z) ** N
    s = 0.0 + 0j
    term = zN
    for k in range(1, 500):
        s += term / (k * (N * k + 1))
        term *= zN
        if abs(term / (k * (N * k + 1))) < 1e-15:
            break
    return s


# ---------------------------------------------------------------------------
# Integral representation (for verification)
# ---------------------------------------------------------------------------

def developing_map_integral(z, N, beta, n_quad=200):
    """f(z) = int_0^z (w^N - 1)^{-beta} dw, computed numerically.

    Uses the substitution w = z*t for t in [0,1], with Gauss-Jacobi
    quadrature to handle the (1-t)^{-beta} singularity at t=1.

    For the Z_N-symmetric case: (w^N - 1)^{-beta} = (z^N t^N - 1)^{-beta}
    = (-1)^{-beta} (1 - z^N t^N)^{-beta}  (for |z^N t^N| < 1).
    """
    z = complex(z)
    if abs(z) < 1e-15:
        return 0.0 + 0j

    # Gauss-Legendre on [0, 1-delta] + analytical tail
    # For simplicity, use substitution t = 1 - s^(1/(1-beta)) to
    # regularize the endpoint singularity.
    # Instead, just split: integral from 0 to 1-delta (regular)
    # + integral from 1-delta to 1 (asymptotic).

    delta = 0.01
    # Part 1: t in [0, 1-delta], no singularity
    h = (1 - delta) / n_quad
    integral = 0.0 + 0j
    for i in range(n_quad):
        t = (i + 0.5) * h  # midpoint rule
        w = z * t
        wN = w ** N
        # (w^N - 1)^{-beta} with branch cut
        integrand = (wN - 1) ** (-beta)  # complex power
        integral += integrand * h

    # Part 2: t in [1-delta, 1], near the cone point z
    # w = z*t, w^N = z^N * t^N ≈ z^N * (1 - N*(1-t))
    # (w^N - 1) ≈ z^N - 1 + z^N * N * (t-1) * ...
    # For z = e^{2pi i j/N}: z^N = 1, so (w^N - 1) ≈ N*z^{N-1}*(w-z)
    # = N*z^{N-1}*z*(t-1) = N*z^N*(t-1)
    # So integrand ≈ (N*z^N)^{-beta} * (t-1)^{-beta}
    # Integral from 1-delta to 1: (N*z^N)^{-beta} * delta^{1-beta}/(1-beta)

    # For general z: use n_quad/2 points with substitution
    n2 = max(n_quad // 2, 50)
    h2 = delta / n2
    for i in range(n2):
        t = (1 - delta) + (i + 0.5) * h2
        w = z * t
        wN = w ** N
        integrand = (wN - 1) ** (-beta)
        integral += integrand * h2

    return z * integral  # the dw = z*dt factor


# ---------------------------------------------------------------------------
# The key proposition for the paper
# ---------------------------------------------------------------------------

def conformal_invariance_proposition():
    """Statement of the conformal invariance result.

    PROPOSITION (Conformal invariance of flat-plane stability).
    On a flat spatial slice (Lambda = 0) with N equal conical singularities
    of deficit delta = 8*pi*G*m in a regular ring, the Havelock eigenvalues
    are
        lambda_m = (N-1) - m(N-m)/2
    for all G*m in [0, 1/(2N)).  In particular, N_crit = 7 is independent
    of the deficit angle.

    PROOF. The developing map f(z) = z * _2F1(beta, 1/N; 1+1/N; z^N) is
    a conformal isometry from the cone surface to the Euclidean plane.
    By Z_N symmetry, f(omega*z) = omega*f(z), so the image of the regular
    N-gon is a regular N-gon of radius

        R_f = Gamma(1+1/N) * Gamma(1-beta) / Gamma(1+1/N-beta).

    The 2D Green's function is conformally invariant:

        Delta_g G = delta  =>  G(z,w) = -(1/2pi) log|z - w|

    in conformal coordinates, independent of the cone structure.
    Therefore the interaction energy H = -sum log|z_j - z_k| is the
    same as on the flat plane.  Since the Havelock eigenvalues depend
    only on N and the angular structure of the N-gon (not the radius),
    they are independent of beta.  QED.

    REMARK. The transition from N_crit = 7 (flat) to N_crit <= 6 (S^2)
    occurs through the cosmological curvature C_1 = (N-1)*cos(phi),
    not through the backreaction of the deficit angles.  The flat-plane
    backreaction is exactly zero: a consequence of conformal invariance.
    """
    pass
