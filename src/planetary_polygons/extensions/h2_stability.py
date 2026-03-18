"""
Point vortex ring stability on the hyperbolic plane H². (§5.x)

Exact computation using the Poincaré disk model:
  H_hyp = -Σ_{j<k} ln|z_j - z_k| + (N-1)/2 · Σ_k ln(a² - |z_k|²)
  J_hyp = Σ_k (a² + |z_k|²)/(a² - |z_k|²)   [SO(2,1) moment map]

Equilibrium: N-vortex ring at Euclidean radius r_E = a·tanh(ρ/(2a))
  Ω = [−(N−1)/(2r_E) − (N−1)r_E/(a²−r_E²)] / [4a²r_E/(a²−r_E²)²]

Riemannian Havelock identity (EXACT):
  λ_m · r_E² = C₁(H², ξ) − m(N−m)/2
  C₁(H², ξ) = (N−1)(1+ξ²)/(1−ξ)²,   ξ = r_E²/a²

7→8 transition threshold (EXACT):
  ξ* = 8 − 3√7 ≈ 0.0627
  γ = 1/ξ*² = 127 + 48√7 ≈ 254
"""
import numpy as np

XI_STAR_78 = 8 - 3 * np.sqrt(7)   # exact 7→8 stability threshold, ξ = r_E²/a²
GAMMA_78 = 127 + 48 * np.sqrt(7)  # = 1/ξ*², exact: (8-3√7)²(127+48√7) = 1


def H_hyp(z_re, z_im, a):
    z = z_re + 1j * z_im
    N = len(z)
    H = 0.0
    for j in range(N):
        for k in range(j + 1, N):
            H -= np.log(abs(z[j] - z[k]))
        H += (N - 1) / 2 * np.log(a**2 - abs(z[j])**2)
    return H


def J_hyp(z_re, z_im, a):
    r2 = z_re**2 + z_im**2
    return np.sum((a**2 + r2) / (a**2 - r2))


def get_Omega(N, r_E, a):
    # CORRECT sign (negative for both terms)
    dH_dx0 = -(N - 1) / (2 * r_E) - (N - 1) * r_E / (a**2 - r_E**2)
    dJ_dx0 = 4 * a**2 * r_E / (a**2 - r_E**2)**2
    return dH_dx0 / dJ_dx0


def fourier_eigenvalue(m, N, rho, a=1.0, h_fd=1e-5):
    r_E = a * np.tanh(rho / (2 * a))
    k = np.arange(N)
    z = r_E * np.exp(2j * np.pi * k / N)
    q0 = np.zeros(2 * N)
    q0[0::2] = z.real
    q0[1::2] = z.imag
    Omega = get_Omega(N, r_E, a)

    theta_k = 2 * np.pi * k / N
    amp = np.cos(2 * np.pi * m * k / N)
    u = np.zeros(2 * N)
    u[0::2] = amp * np.cos(theta_k)
    u[1::2] = amp * np.sin(theta_k)
    norm_sq = np.dot(u, u)
    if norm_sq < 1e-10:
        return np.nan
    u_hat = u / np.sqrt(norm_sq)

    def F(q):
        return H_hyp(q[0::2], q[1::2], a) - Omega * J_hyp(q[0::2], q[1::2], a)

    F0 = F(q0)
    return (F(q0 + h_fd * u_hat) - 2 * F0 + F(q0 - h_fd * u_hat)) / h_fd**2


def min_eigenvalue(N, rho, a=1.0):
    lams = [fourier_eigenvalue(m, N, rho, a) for m in range(1, N // 2 + 1)]
    return min(l for l in lams if not np.isnan(l))


def ncrit_h2(rho, a=1.0, N_max=24):
    """Find N_crit numerically using FD Hessian. Returns largest stable N."""
    ncrit = 2
    for N in range(3, N_max + 1):
        r_E = a * np.tanh(rho / (2 * a))
        if r_E >= a - 1e-6:
            break
        lam_min = min_eigenvalue(N, rho, a)
        if lam_min >= -1e-6:
            ncrit = N
        else:
            break
    return ncrit


def C1_h2_exact(N, xi):
    """
    Exact C₁ coefficient for N-vortex ring on H².
    C₁(H², ξ) = (N-1)(1+ξ²)/(1-ξ)²
    ξ = r_E²/a², where r_E is Euclidean ring radius, a is curvature radius.
    """
    return (N - 1) * (1 + xi**2) / (1 - xi)**2


def ncrit_h2_exact(rho, a=1.0, N_max=24):
    """
    Find N_crit from exact C₁ formula (fast, no FD).
    Ring of N vortices is stable iff min over m of [C1 - m(N-m)/2] >= 0.
    """
    r_E = a * np.tanh(rho / (2 * a))
    xi = (r_E / a) ** 2
    ncrit = 2
    for N in range(3, N_max + 1):
        if xi >= 1 - 1e-10:
            break
        C1 = C1_h2_exact(N, xi)
        lam_min = min(C1 - m * (N - m) / 2 for m in range(1, N // 2 + 1))
        if lam_min >= 0:
            ncrit = N
        else:
            break
    return ncrit


def threshold_78_exact():
    """
    Return (xi_star, gamma) for the exact 7→8 stability threshold.
    Setting C₁(H², ξ*) = 8 gives ξ² - 16ξ + 1 = 0 → ξ* = 8 - 3√7.
    γ = 1/ξ*² = 127 + 48√7 (algebraically exact).
    """
    return XI_STAR_78, GAMMA_78


def h2_geodesic_distance(z_j, z_k, a):
    """
    Geodesic distance between z_j and z_k on the Poincaré disk of radius a.

    Formula (Beardon 1983; Kimura 1999):
        cosh(d/a) = 1 + 2a²|z_j-z_k|² / ((a²-|z_j|²)(a²-|z_k|²))

    Parameters
    ----------
    z_j, z_k : complex
        Points inside the disk |z| < a.
    a : float
        Curvature radius.

    Returns
    -------
    float
        Geodesic distance d(z_j, z_k).
    """
    dz2 = abs(z_j - z_k) ** 2
    rj2 = abs(z_j) ** 2
    rk2 = abs(z_k) ** 2
    cosh_arg = 1.0 + 2.0 * a ** 2 * dz2 / ((a ** 2 - rj2) * (a ** 2 - rk2))
    return a * np.arccosh(cosh_arg)


def h2_green_identity_residual(N, rho, a=1.0):
    """
    Verify the algebraic identity linking the two forms of the H² Hamiltonian.

    The Poincaré-disk form and the geodesic-distance form are related by
    (derived in §4.3 via the identity sinh(d/(2a)) = a|z_j-z_k|/√((a²-|z_j|²)(a²-|z_k|²))):

        H_hyp(z, a) = Σ_{j<k} −ln sinh(d_{H²}(j,k)/(2a)) + N(N-1)/2 · ln a

    Returns the residual of this identity, which should be ≈ 0 to machine
    precision for any ring configuration.

    Parameters
    ----------
    N : int
        Number of vortices.
    rho : float
        Geodesic ring radius (ρ/a ratio when a=1).
    a : float
        Curvature radius.

    Returns
    -------
    float
        |H_hyp − (H_sinh + const)|.  Zero to floating-point precision.
    """
    r_E = a * np.tanh(rho / (2.0 * a))
    z = r_E * np.exp(2j * np.pi * np.arange(N) / N)

    H_disk = H_hyp(z.real, z.imag, a)

    H_sinh = 0.0
    for j in range(N):
        for k in range(j + 1, N):
            d_jk = h2_geodesic_distance(z[j], z[k], a)
            H_sinh -= np.log(np.sinh(d_jk / (2.0 * a)))

    const = N * (N - 1) / 2.0 * np.log(a)
    return float(H_disk - (H_sinh + const))


def ncrit_h2_table(rho_vals, a=1.0):
    """
    Return dict mapping ρ/a → N_crit (exact formula).
    """
    return {rho: ncrit_h2_exact(rho, a) for rho in rho_vals}
