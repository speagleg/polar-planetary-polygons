"""
K₀ stability with central vortex: the missing Jupiter computation.

For the finite-Rossby-radius interaction h(d) = K₀(d/R_d), compute the
constrained Hessian eigenvalue for the N-ring + central vortex.

Key result:
    (R/R_d)_crit(N=8, κ₀/κ=0.7) ≈ 0.79

This means N=8 is stable under K₀ only for R/R_d < 0.79 (nearly barotropic).
Jupiter's tropospheric regime (R/R_d ∈ [1, 4]) lies entirely in the
unstable region. The Jupiter N=8 prediction requires the barotropic limit
(R_d >> R, i.e., a deep weather layer with H_eff >> R²f²/g).

K₀ and K₁ are implemented via Abramowitz & Stegun polynomial approximations
(9.8.1-9.8.8), accuracy ~10⁻⁷. No scipy dependency.
"""
import numpy as np
import math


# ---------------------------------------------------------------
# Modified Bessel functions K₀, K₁ (A&S 9.8.1-9.8.8)
# ---------------------------------------------------------------

def _i0(x):
    """Modified Bessel I₀(x), A&S 9.8.1-9.8.2, |eps| < 1.6e-7."""
    ax = abs(x)
    if ax <= 3.75:
        t = (ax / 3.75) ** 2
        return 1.0 + t * (3.5156229 + t * (3.0899424 + t * (1.2067492
                    + t * (0.2659732 + t * (0.0360768 + t * 0.0045813)))))
    else:
        t = 3.75 / ax
        return (np.exp(ax) / np.sqrt(ax)) * (
            0.39894228 + t * (0.01328592 + t * (0.00225319
            + t * (-0.00157565 + t * (0.00916281 + t * (-0.02057706
            + t * (0.02635537 + t * (-0.01647633 + t * 0.00392377))))))))


def k0(x):
    """Modified Bessel K₀(x), A&S 9.8.5-9.8.6, |eps| < 1e-8."""
    if x <= 0:
        return float('inf')
    if x <= 2.0:
        t = (x / 2.0) ** 2
        return -np.log(x / 2) * _i0(x) + (
            -0.57721566 + t * (0.42278420 + t * (0.23069756
            + t * (0.03488590 + t * (0.00262698
            + t * (0.00010750 + t * 0.00000740))))))
    else:
        t = 2.0 / x
        return (np.exp(-x) / np.sqrt(x)) * (
            1.25331414 + t * (-0.07832358 + t * (0.02189568
            + t * (-0.01062446 + t * (0.00587872
            + t * (-0.00251540 + t * 0.00053208))))))


def k1(x):
    """Modified Bessel K₁(x) = -dK₀/dx, via central difference of K₀."""
    h = max(x * 1e-5, 1e-8)
    return -(k0(x + h) - k0(x - h)) / (2 * h)


# ---------------------------------------------------------------
# Constrained Hessian for K₀ + central vortex
# ---------------------------------------------------------------

def K0_constrained_eigenvalue(N, R_over_Rd, kappa_ratio=0.0, R=1.0):
    """
    Minimum physical constrained eigenvalue for N-ring + central vortex
    under the K₀(d/R_d) interaction.

    Parameters
    ----------
    N : int
        Number of ring vortices.
    R_over_Rd : float
        Ratio R/R_d. Small values → barotropic (≈ point vortex).
    kappa_ratio : float
        Central vortex strength κ₀/κ. 0 = no central vortex.
    R : float
        Ring radius (default 1.0).

    Returns
    -------
    float
        Minimum physical constrained eigenvalue. Positive → stable.
    """
    Rd = R / R_over_Rd if R_over_Rd > 0 else 1e10 * R
    z = R * np.exp(2j * np.pi * np.arange(N) / N)
    pos = np.concatenate([z.real, z.imag])
    dim = 2 * N

    H = np.zeros((dim, dim))
    grad_H = np.zeros(dim)

    # Ring-ring interaction
    for j in range(N):
        for k in range(N):
            if j == k:
                continue
            dz = z[j] - z[k]
            dx, dy = dz.real, dz.imag
            d = abs(dz)
            if d < 1e-12:
                continue
            xi = d / Rd
            K0v = k0(xi)
            K1v = k1(xi)

            dh_dr = -K1v / Rd
            d2h_dr2 = (K0v + K1v / xi) / Rd**2

            d2 = d**2
            d3 = d**3
            h_xx = dh_dr * (1 / d - dx**2 / d3) + d2h_dr2 * dx**2 / d2
            h_yy = dh_dr * (1 / d - dy**2 / d3) + d2h_dr2 * dy**2 / d2
            h_xy = -dh_dr * dx * dy / d3 + d2h_dr2 * dx * dy / d2

            grad_H[j] += dh_dr * dx / d
            grad_H[j + N] += dh_dr * dy / d

            H[j, j] += h_xx;           H[j + N, j + N] += h_yy
            H[j, j + N] += h_xy;       H[j + N, j] += h_xy
            H[j, k] -= h_xx;           H[j + N, k + N] -= h_yy
            H[j, k + N] -= h_xy;       H[j + N, k] -= h_xy

    # Ring-center interaction
    if kappa_ratio != 0:
        xi_R = R / Rd
        K0_R = k0(xi_R)
        K1_R = k1(xi_R)
        K0pp_R = (K0_R + K1_R / xi_R) / Rd**2
        dh_dr_R = -K1_R / Rd

        for j in range(N):
            dx, dy = z[j].real, z[j].imag
            r = abs(z[j])
            r2 = r**2
            r3 = r**3

            grad_H[j] += kappa_ratio * dh_dr_R * dx / r
            grad_H[j + N] += kappa_ratio * dh_dr_R * dy / r

            h_xx = dh_dr_R * (1 / r - dx**2 / r3) + K0pp_R * dx**2 / r2
            h_yy = dh_dr_R * (1 / r - dy**2 / r3) + K0pp_R * dy**2 / r2
            h_xy = -dh_dr_R * dx * dy / r3 + K0pp_R * dx * dy / r2

            H[j, j] += kappa_ratio * h_xx
            H[j + N, j + N] += kappa_ratio * h_yy
            H[j, j + N] += kappa_ratio * h_xy
            H[j + N, j] += kappa_ratio * h_xy

    # Constraint projection
    grad_L = 2 * pos
    grad_Px = np.concatenate([np.ones(N), np.zeros(N)])
    grad_Py = np.concatenate([np.zeros(N), np.ones(N)])
    G = np.column_stack([grad_L, grad_Px, grad_Py])

    mu, _, _, _ = np.linalg.lstsq(G, grad_H, rcond=None)
    mu_L = mu[0]

    H_lagr = H - 2 * mu_L * np.eye(dim)
    U, S, Vt = np.linalg.svd(G.T)
    rank = int(np.sum(S > 1e-10))
    null_basis = Vt[rank:].T

    H_restricted = null_basis.T @ H_lagr @ null_basis
    evals = np.sort(np.linalg.eigvalsh(H_restricted))

    physical = [e for e in evals if abs(e) > 1e-5]
    return float(min(physical)) if physical else 0.0


def critical_R_over_Rd(N, kappa_ratio, tol=0.005):
    """
    Find the critical R/R_d at which the N-ring + central vortex transitions
    from stable to unstable under the K₀ interaction.

    Returns float: the critical R/R_d. Below this → stable; above → unstable.
    Returns None if unstable for all R/R_d (no central vortex, N >= 8).
    """
    # Check barotropic limit
    lam_baro = K0_constrained_eigenvalue(N, 0.01, kappa_ratio)
    if lam_baro < -1e-6:
        return None  # unstable even in barotropic limit

    # Check high R/R_d
    lam_high = K0_constrained_eigenvalue(N, 10.0, kappa_ratio)
    if lam_high > 1e-6:
        return float('inf')  # stable everywhere

    # Bisect
    lo, hi = 0.01, 10.0
    for _ in range(60):
        mid = (lo + hi) / 2
        lam = K0_constrained_eigenvalue(N, mid, kappa_ratio)
        if lam > 0:
            lo = mid
        else:
            hi = mid

    return (lo + hi) / 2


def jupiter_K0_table():
    """
    K₀ stability table for Jupiter parameters.

    Reports (R/R_d)_crit for N = 6..9 at κ₀/κ = 0.7.
    The key number is (R/R_d)_crit(N=8) ≈ 0.79.
    """
    kappa_ratio = 0.7
    rows = []
    for N in range(6, 10):
        R_Rd_crit = critical_R_over_Rd(N, kappa_ratio)
        rows.append({
            'N': N,
            'kappa_ratio': kappa_ratio,
            'R_Rd_crit': R_Rd_crit,
            'tropospheric_stable': R_Rd_crit is not None and R_Rd_crit > 4.0,
        })
    return rows


if __name__ == '__main__':
    print('K₀ + central vortex stability: (R/R_d)_crit')
    print(f"{'N':>3}  {'κ₀/κ':>6}  {'(R/Rd)_crit':>12}  {'tropo stable':>14}")
    print('-' * 42)
    for row in jupiter_K0_table():
        crit = f"{row['R_Rd_crit']:.2f}" if row['R_Rd_crit'] is not None else 'never'
        ts = 'YES' if row['tropospheric_stable'] else 'no'
        print(f"{row['N']:>3}  {row['kappa_ratio']:>6.1f}  {crit:>12}  {ts:>14}")
