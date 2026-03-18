"""
Effect of finite deformation radius on N-vortex ring stability. (§6.2)

With baroclinic effects: h(d) = K₀(d/R_d), modified Bessel function.
Paper number: suppression transition at R/R_d ≈ 1.29 for N=6.

Sign convention note
--------------------
The Thomson energy is H = sum_{j<k} K₀(d_{jk}/R_d).
Because K₀ > 0 and is repulsive, the Hessian d²H/dx_j² is computed directly:

    d²H/dx_j² = Σ_{k≠j} h_xx(dx_{jk}, dy_{jk}, d_{jk})

where h_xx = (dh/dr)(1/d − dx²/d³) + (d²h/dr²)(dx²/d²)
and dh/dr = −K₁(ξ)/Rd, d²h/dr² = (K₀(ξ) + K₁(ξ)/ξ)/Rd².

This gives H[j,j] += h_xx (positive accumulation), opposite to the
Thomson log-energy convention where the flat formula (dy²-dx²)/d⁴ is
already negated before the −= assembly.
"""
import numpy as np
from scipy.special import k0, k1
from scipy.linalg import eigvalsh
from scipy.optimize import brentq


def _ring_positions(N, R=1.0):
    return R * np.exp(2j*np.pi*np.arange(N)/N)


def _K0_pair_derivs(dx, dy, d, Rd):
    """
    Direct second derivatives of K₀(d/Rd) w.r.t. x_j.

    Returns (h_xx, h_yy, h_xy) = d²K₀/dx² etc.
    These are the DIRECT Hessian contributions (positive for diagonal).
    """
    xi = d / Rd
    if xi < 1e-10:
        return 0.0, 0.0, 0.0
    K0v = float(k0(xi))
    K1v = float(k1(xi))
    # d²K₀(r/Rd)/dr² = (K₀(xi) + K₁(xi)/xi) / Rd²
    K0pp = K0v + K1v / xi

    dh_dr = -K1v / Rd
    d2h_dr2 = K0pp / Rd**2

    d2 = d**2; d3 = d**3
    h_xx = dh_dr * (1/d - dx**2/d3) + d2h_dr2 * dx**2/d2
    h_yy = dh_dr * (1/d - dy**2/d3) + d2h_dr2 * dy**2/d2
    h_xy = -dh_dr * dx*dy/d3 + d2h_dr2 * dx*dy/d2
    return h_xx, h_yy, h_xy


def _K0_hessian(N, R, Rd):
    """
    Build the 2N×2N Hessian for K₀ interaction with correct sign convention.

    H[j,j] accumulates +h_xx (direct second derivative of K₀ energy).
    H[j,k] accumulates -h_xx (cross term).
    """
    z = _ring_positions(N, R)
    H = np.zeros((2*N, 2*N))
    for j in range(N):
        for k in range(N):
            if j == k:
                continue
            dz = z[j] - z[k]
            dx, dy = dz.real, dz.imag
            d = abs(dz)
            if d < 1e-12:
                continue
            h_xx, h_yy, h_xy = _K0_pair_derivs(dx, dy, d, Rd)
            # Direct assembly: d²H/dx_j² = Σ h_xx → H[j,j] += h_xx
            H[j, j] += h_xx;         H[j+N, j+N] += h_yy
            H[j, j+N] += h_xy;       H[j+N, j] += h_xy
            H[j, k] -= h_xx;         H[j+N, k+N] -= h_yy
            H[j, k+N] -= h_xy;       H[j+N, k] -= h_xy
    return H, z


def _K0_gradient(N, R, Rd):
    """Gradient of K₀ energy at the N-gon equilibrium."""
    z = _ring_positions(N, R)
    grad_H = np.zeros(2*N)
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
            if xi < 1e-10:
                continue
            K1v = float(k1(xi))
            dh_dr = -K1v / Rd
            grad_H[j] += dh_dr * dx / d
            grad_H[j+N] += dh_dr * dy / d
    return grad_H, z


def _constrained_min_eval(N, R, Rd):
    """
    Minimum physical (non-Goldstone) constrained eigenvalue for K₀ interaction.

    Uses the 3-constraint approach (L, Px, Py). The Goldstone rotation mode
    has eigenvalue ≈ 0 and is excluded by filtering |eval| < 1e-3.
    Returns the minimum eigenvalue of the remaining physical modes.

    Positive → ring is stable; negative → ring is unstable.
    """
    H, z = _K0_hessian(N, R, Rd)
    pos = np.concatenate([z.real, z.imag])
    grad_H, _ = _K0_gradient(N, R, Rd)

    grad_L = 2 * pos
    grad_Px = np.concatenate([np.ones(N), np.zeros(N)])
    grad_Py = np.concatenate([np.zeros(N), np.ones(N)])
    G_mat = np.column_stack([grad_L, grad_Px, grad_Py])

    U_svd, S_svd, Vt_svd = np.linalg.svd(G_mat.T)
    null_basis = Vt_svd[3:].T

    mu_vec, _, _, _ = np.linalg.lstsq(G_mat, grad_H, rcond=None)
    mu_L = float(mu_vec[0])

    H_lagr = H - 2 * mu_L * np.eye(2*N)
    H_restricted = null_basis.T @ H_lagr @ null_basis
    evals = np.sort(eigvalsh(H_restricted))

    # Filter Goldstone rotation mode (|eval| < 1e-5) and return minimum physical mode.
    # The Goldstone is at machine precision (~1e-8 to 1e-10); the instability mode
    # approaches zero at the transition (so threshold must be < transition eigenvalue).
    physical = [e for e in evals if abs(e) > 1e-5]
    if not physical:
        return 0.0
    return float(min(physical))


def _constrained_mode_eval(N, R, Rd, mode_index=1):
    """
    Return the mode_index-th physical constrained eigenvalue (skipping Goldstone).

    mode_index=1 → smallest physical eigenvalue (stability indicator).
    mode_index=2 → second smallest, etc.
    """
    H, z = _K0_hessian(N, R, Rd)
    pos = np.concatenate([z.real, z.imag])
    grad_H, _ = _K0_gradient(N, R, Rd)

    grad_L = 2 * pos
    grad_Px = np.concatenate([np.ones(N), np.zeros(N)])
    grad_Py = np.concatenate([np.zeros(N), np.ones(N)])
    G_mat = np.column_stack([grad_L, grad_Px, grad_Py])

    U_svd, S_svd, Vt_svd = np.linalg.svd(G_mat.T)
    null_basis = Vt_svd[3:].T

    mu_vec, _, _, _ = np.linalg.lstsq(G_mat, grad_H, rcond=None)
    mu_L = float(mu_vec[0])

    H_lagr = H - 2 * mu_L * np.eye(2*N)
    H_restricted = null_basis.T @ H_lagr @ null_basis
    evals = np.sort(eigvalsh(H_restricted))

    # Sort physical modes (skip Goldstone with |eval| < 1e-5), return mode_index-th.
    physical = sorted([e for e in evals if abs(e) > 1e-5])
    if mode_index - 1 < len(physical):
        return float(physical[mode_index - 1])
    return float(evals[mode_index - 1])


def K0_eigenvalue(N, m, R_over_Rd, R=1.0):
    """
    Constrained eigenvalue for mode m with K₀ interaction at R/Rd.

    Parameters
    ----------
    N : int
        Number of ring vortices.
    m : int
        Mode index (1 = smallest physical mode, i.e., stability indicator).
    R_over_Rd : float
        Ratio R/R_d. Large R/Rd → strong baroclinic suppression.
    R : float
        Ring radius (default 1.0).

    Returns
    -------
    float
        The m-th physical constrained eigenvalue. Positive → stable.
    """
    Rd = R / R_over_Rd
    return _constrained_mode_eval(N, R, Rd, mode_index=m)


def suppression_transition(N=6, R=1.0):
    """
    R/Rd at which the first physical mode eigenvalue crosses zero.

    For N=6: paper gives ≈ 1.29. Uses the minimum physical eigenvalue
    (excluding Goldstone rotation mode).

    Returns
    -------
    float
        R/Rd at the stability → instability transition.
    """
    def f(R_over_Rd):
        return _constrained_min_eval(N, R, R / R_over_Rd)

    try:
        return float(brentq(f, 0.5, 10.0))
    except ValueError:
        return float('nan')


def K0_correction_table():
    """Eigenvalue vs R/Rd for N=6,7,8."""
    result = {}
    for N in [6, 7, 8]:
        evals = {}
        for R_Rd in [0.1, 0.5, 1.0, 2.0]:
            evals[R_Rd] = _constrained_min_eval(N, 1.0, 1.0/R_Rd)
        result[N] = evals
    return result


if __name__ == "__main__":
    print(f"N=6 suppression transition: R/Rd = {suppression_transition(6):.4f}")
    print("Expected: ≈1.29")
