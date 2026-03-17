"""
Constrained Hessian analysis of the Thomson energy at the regular N-gon.

RESULT (2026-03-16):
The regular N-gon is an energy MINIMUM (not maximum) on the conserved-quantity
surface {L = const, P = 0}, where L = Sigma |z_k|^2 is angular impulse and
P = Sigma z_k is linear impulse.

This overturns the paper's Onsager argument:
    OLD: H''(0) < 0 along spiral -> energy maximum -> Onsager selects polygon
    NEW: N-gon minimises H at constant L,P -> dynamically stable (Arnold/Thomson)

The H''(0) < 0 result along the spiral deformation is TRUE but MISLEADING:
the spiral direction has components that change L and P (conserved quantities),
so it includes dynamically inaccessible directions. On the physical constraint
surface, the Lagrange multiplier correction (-2*mu_L*I, with mu_L < 0)
overwhelms the negative H'', giving a positive-definite Lagrangian Hessian.

Key findings:
    N=3,...,7: all constrained Lagrangian eigenvalues >= 0 -> STABLE (minimum)
    N=8: 3 negative Lagrangian eigenvalues appear -> UNSTABLE (saddle)
    Crossover at N~7 recovers Thomson's classical stability boundary.

Physical picture (two-scale):
    Macro: Onsager negative temperature + inverse cascade -> N clusters form
    Meso:  Thomson/Arnold dynamical stability -> clusters arrange as polygon

The arrangement is deterministic (stability), not statistical (Onsager).
"""

import numpy as np
from numpy.linalg import norm, svd, eigvalsh
from dataclasses import dataclass
from typing import Optional


@dataclass
class ConstrainedHessianResult:
    """Results of constrained Hessian analysis for N-gon."""
    N: int
    mu_L: float                    # Lagrange multiplier for angular impulse
    mu_Px: float                   # Lagrange multiplier for x-impulse
    mu_Py: float                   # Lagrange multiplier for y-impulse
    grad_H_norm: float             # |nabla H| at N-gon (should be nonzero)
    lagrange_residual: float       # |nabla H - mu . nabla C| (should be ~0)
    unconstrained_evals: np.ndarray
    lagrangian_evals: np.ndarray   # eigenvalues of nabla^2 H - 2*mu_L*I
    constrained_evals: np.ndarray  # Lagrangian restricted to tangent space
    n_neg: int
    n_zero: int
    n_pos: int
    is_stable: bool                # True if constrained minimum (all evals >= 0)
    spiral_H_pp: float             # H'' along spiral (unconstrained)
    spiral_lagr: float             # Lagrangian curvature along spiral tangent


def thomson_energy(pos: np.ndarray) -> float:
    """H = -sum_{j<k} ln|z_j - z_k| for point vortices at positions pos."""
    N = len(pos) // 2
    x, y = pos[:N], pos[N:]
    H = 0.0
    for j in range(N):
        for k in range(j + 1, N):
            dx = x[j] - x[k]
            dy = y[j] - y[k]
            r2 = dx**2 + dy**2
            if r2 > 1e-30:
                H -= 0.5 * np.log(r2)
    return H


def ngon_positions(N: int, R: float = 1.0) -> np.ndarray:
    """Regular N-gon on circle of radius R, as flat [x0,...,xN-1,y0,...,yN-1]."""
    theta = 2 * np.pi * np.arange(N) / N
    return np.concatenate([R * np.cos(theta), R * np.sin(theta)])


def numerical_gradient(f, pos: np.ndarray, eps: float = 1e-7) -> np.ndarray:
    """Central-difference gradient."""
    n = len(pos)
    grad = np.zeros(n)
    for i in range(n):
        p_plus = pos.copy(); p_plus[i] += eps
        p_minus = pos.copy(); p_minus[i] -= eps
        grad[i] = (f(p_plus) - f(p_minus)) / (2 * eps)
    return grad


def numerical_hessian(f, pos: np.ndarray, eps: float = 1e-5) -> np.ndarray:
    """Central-difference Hessian via 4-point stencil."""
    n = len(pos)
    H = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            p_pp = pos.copy(); p_pp[i] += eps; p_pp[j] += eps
            p_pm = pos.copy(); p_pm[i] += eps; p_pm[j] -= eps
            p_mp = pos.copy(); p_mp[i] -= eps; p_mp[j] += eps
            p_mm = pos.copy(); p_mm[i] -= eps; p_mm[j] -= eps
            val = (f(p_pp) - f(p_pm) - f(p_mp) + f(p_mm)) / (4 * eps**2)
            H[i, j] = val
            H[j, i] = val
    return H


def constrained_hessian_analysis(N: int, R: float = 1.0) -> ConstrainedHessianResult:
    """
    Full constrained Hessian analysis for the regular N-gon.

    Conserved quantities of point vortex dynamics:
        L  = sum |z_k|^2   (angular impulse)
        Px = sum x_k        (x-component of linear impulse)
        Py = sum y_k        (y-component of linear impulse)

    The N-gon is a critical point of H on the surface {L=NR^2, Px=0, Py=0}
    by the equivariant critical point theorem (Z_N symmetry).

    The constrained second derivative test uses the Lagrangian:
        L_lagr = H - mu_L * L - mu_Px * Px - mu_Py * Py

    Since nabla^2(L) = 2I, nabla^2(Px) = nabla^2(Py) = 0:
        nabla^2(L_lagr) = nabla^2(H) - 2*mu_L * I

    Restrict this to the tangent space of the constraint surface and
    check definiteness.
    """
    pos = ngon_positions(N, R)
    dim = 2 * N

    # Gradient of H
    grad_H = numerical_gradient(thomson_energy, pos)

    # Constraint gradients at the N-gon
    grad_L = 2 * pos
    grad_Px = np.concatenate([np.ones(N), np.zeros(N)])
    grad_Py = np.concatenate([np.zeros(N), np.ones(N)])
    G = np.column_stack([grad_L, grad_Px, grad_Py])

    # Lagrange multipliers: nabla H = mu_L * nabla L + mu_Px * nabla Px + mu_Py * nabla Py
    mu, _, _, _ = np.linalg.lstsq(G, grad_H, rcond=None)
    mu_L, mu_Px, mu_Py = mu
    lagrange_residual = norm(grad_H - G @ mu)

    # Full Hessian of H
    H_full = numerical_hessian(thomson_energy, pos)

    # Lagrangian Hessian: nabla^2(H) - 2*mu_L*I
    H_lagr = H_full - 2 * mu_L * np.eye(dim)

    # Orthonormal basis for constraint tangent space via SVD
    U, S, Vt = svd(G.T)
    rank = np.sum(S > 1e-10)
    null_basis = Vt[rank:].T  # columns span null space of G^T

    # Restricted Lagrangian Hessian
    H_restricted = null_basis.T @ H_lagr @ null_basis
    constrained_evals = eigvalsh(H_restricted)

    tol = 1e-4
    n_neg = int(np.sum(constrained_evals < -tol))
    n_zero = int(np.sum(np.abs(constrained_evals) <= tol))
    n_pos = int(np.sum(constrained_evals > tol))

    # Spiral direction analysis (centered deformation)
    k = np.arange(N)
    factor = (k - (N - 1) / 2) / N
    x0, y0 = pos[:N], pos[N:]
    v_spiral = np.concatenate([factor * x0, factor * y0])

    # Project spiral onto tangent space
    GtG_inv = np.linalg.inv(G.T @ G)
    P_proj = np.eye(dim) - G @ GtG_inv @ G.T
    v_tangent = P_proj @ v_spiral

    spiral_H_pp = (v_spiral @ H_full @ v_spiral / norm(v_spiral)**2
                   if norm(v_spiral) > 1e-10 else 0.0)

    if norm(v_tangent) > 1e-10:
        v_hat = v_tangent / norm(v_tangent)
        spiral_lagr = float(v_hat @ H_lagr @ v_hat)
    else:
        spiral_lagr = 0.0

    return ConstrainedHessianResult(
        N=N,
        mu_L=mu_L,
        mu_Px=mu_Px,
        mu_Py=mu_Py,
        grad_H_norm=float(norm(grad_H)),
        lagrange_residual=float(lagrange_residual),
        unconstrained_evals=eigvalsh(H_full),
        lagrangian_evals=eigvalsh(H_lagr),
        constrained_evals=constrained_evals,
        n_neg=n_neg,
        n_zero=n_zero,
        n_pos=n_pos,
        is_stable=(n_neg == 0),
        spiral_H_pp=float(spiral_H_pp),
        spiral_lagr=float(spiral_lagr),
    )


def constrained_hessian_with_central_vortex(
    N: int, kappa_ratio: float, R: float = 1.0
) -> ConstrainedHessianResult:
    """
    Constrained Hessian for N ring vortices + central vortex of strength
    kappa_center = kappa_ratio * kappa_ring.

    The central vortex is fixed at the origin (not a degree of freedom).
    Its effect enters only through the interaction energy:
        H = -sum_{j<k} ln|z_j - z_k| - kappa_ratio * sum_k ln|z_k|

    For Jupiter's N=8 ring, a central vortex with sufficient strength
    should restore stability (make the constrained Hessian positive definite).
    """
    def energy_with_center(pos):
        N_ring = len(pos) // 2
        x, y = pos[:N_ring], pos[N_ring:]
        # Ring-ring interaction
        H = 0.0
        for j in range(N_ring):
            for k in range(j + 1, N_ring):
                dx = x[j] - x[k]
                dy = y[j] - y[k]
                r2 = dx**2 + dy**2
                if r2 > 1e-30:
                    H -= 0.5 * np.log(r2)
        # Ring-center interaction
        for k in range(N_ring):
            r2 = x[k]**2 + y[k]**2
            if r2 > 1e-30:
                H -= kappa_ratio * 0.5 * np.log(r2)
        return H

    pos = ngon_positions(N, R)
    dim = 2 * N

    grad_H = numerical_gradient(energy_with_center, pos)

    # Constraint gradients (same as before — central vortex doesn't move)
    grad_L = 2 * pos
    grad_Px = np.concatenate([np.ones(N), np.zeros(N)])
    grad_Py = np.concatenate([np.zeros(N), np.ones(N)])
    G = np.column_stack([grad_L, grad_Px, grad_Py])

    mu, _, _, _ = np.linalg.lstsq(G, grad_H, rcond=None)
    mu_L, mu_Px, mu_Py = mu
    lagrange_residual = norm(grad_H - G @ mu)

    H_full = numerical_hessian(energy_with_center, pos)
    H_lagr = H_full - 2 * mu_L * np.eye(dim)

    U, S, Vt = svd(G.T)
    rank = np.sum(S > 1e-10)
    null_basis = Vt[rank:].T

    H_restricted = null_basis.T @ H_lagr @ null_basis
    constrained_evals = eigvalsh(H_restricted)

    tol = 1e-4
    n_neg = int(np.sum(constrained_evals < -tol))
    n_zero = int(np.sum(np.abs(constrained_evals) <= tol))
    n_pos = int(np.sum(constrained_evals > tol))

    # Spiral analysis
    k_idx = np.arange(N)
    factor = (k_idx - (N - 1) / 2) / N
    x0, y0 = pos[:N], pos[N:]
    v_spiral = np.concatenate([factor * x0, factor * y0])
    GtG_inv = np.linalg.inv(G.T @ G)
    P_proj = np.eye(dim) - G @ GtG_inv @ G.T
    v_tangent = P_proj @ v_spiral

    spiral_H_pp = (v_spiral @ H_full @ v_spiral / norm(v_spiral)**2
                   if norm(v_spiral) > 1e-10 else 0.0)
    if norm(v_tangent) > 1e-10:
        v_hat = v_tangent / norm(v_tangent)
        spiral_lagr = float(v_hat @ H_lagr @ v_hat)
    else:
        spiral_lagr = 0.0

    return ConstrainedHessianResult(
        N=N,
        mu_L=mu_L,
        mu_Px=mu_Px,
        mu_Py=mu_Py,
        grad_H_norm=float(norm(grad_H)),
        lagrange_residual=float(lagrange_residual),
        unconstrained_evals=eigvalsh(H_full),
        lagrangian_evals=eigvalsh(H_lagr),
        constrained_evals=constrained_evals,
        n_neg=n_neg,
        n_zero=n_zero,
        n_pos=n_pos,
        is_stable=(n_neg == 0),
        spiral_H_pp=float(spiral_H_pp),
        spiral_lagr=float(spiral_lagr),
    )


def instability_directions(N: int, R: float = 1.0) -> dict:
    """
    For N >= 8 (unstable), identify the unstable deformation directions.

    Returns the eigenvectors corresponding to negative constrained Lagrangian
    eigenvalues, decomposed into Fourier modes of the ring.
    """
    pos = ngon_positions(N, R)
    dim = 2 * N

    H_full = numerical_hessian(thomson_energy, pos)

    grad_L = 2 * pos
    grad_Px = np.concatenate([np.ones(N), np.zeros(N)])
    grad_Py = np.concatenate([np.zeros(N), np.ones(N)])
    G = np.column_stack([grad_L, grad_Px, grad_Py])

    mu, _, _, _ = np.linalg.lstsq(G, numerical_gradient(thomson_energy, pos), rcond=None)
    mu_L = mu[0]

    H_lagr = H_full - 2 * mu_L * np.eye(dim)

    U, S, Vt = svd(G.T)
    rank = np.sum(S > 1e-10)
    null_basis = Vt[rank:].T

    H_restricted = null_basis.T @ H_lagr @ null_basis
    evals, evecs_restricted = np.linalg.eigh(H_restricted)

    # Map back to full space
    evecs_full = null_basis @ evecs_restricted

    tol = 1e-4
    unstable_mask = evals < -tol
    unstable_evals = evals[unstable_mask]
    unstable_evecs = evecs_full[:, unstable_mask]

    # Fourier decompose each unstable direction
    # A deformation (dx_k, dy_k) can be written as dz_k = dx_k + i*dy_k
    # Fourier mode m: dz_k ~ exp(2*pi*i*m*k/N)
    fourier_modes = []
    for col in range(unstable_evecs.shape[1]):
        dx = unstable_evecs[:N, col]
        dy = unstable_evecs[N:, col]
        dz = dx + 1j * dy
        # DFT
        coeffs = np.fft.fft(dz) / N
        fourier_modes.append(np.abs(coeffs))

    return {
        'N': N,
        'mu_L': mu_L,
        'unstable_evals': unstable_evals,
        'unstable_evecs': unstable_evecs,
        'fourier_decomposition': fourier_modes,
        'n_unstable': len(unstable_evals),
    }


def critical_central_vortex_strength(N: int, R: float = 1.0,
                                      tol: float = 0.01) -> float:
    """
    Find the minimum central vortex strength kappa_ratio that stabilises
    the N-gon ring (makes constrained Hessian positive semi-definite).

    Uses bisection on kappa_ratio in [0, N].
    """
    def is_stable(kr):
        result = constrained_hessian_with_central_vortex(N, kr, R)
        return result.is_stable

    if is_stable(0.0):
        return 0.0

    # Find upper bound
    kr_high = 1.0
    while not is_stable(kr_high) and kr_high < 100:
        kr_high *= 2

    if not is_stable(kr_high):
        return float('inf')

    # Bisect
    kr_low = 0.0
    while kr_high - kr_low > tol:
        kr_mid = (kr_low + kr_high) / 2
        if is_stable(kr_mid):
            kr_high = kr_mid
        else:
            kr_low = kr_mid

    return (kr_low + kr_high) / 2


def kappa_crit_sympy(N: int):
    """
    Exact kappa_crit for N-gon + central vortex using sympy.
    For N=6 returns sympy.Rational(-1, 4).

    Method: build the constrained Lagrangian Hessian at the N-gon equilibrium
    (kappa_0 = 0). Find the smallest positive eigenvalue lambda_crit of the
    ring-only constrained Hessian (the mode first destabilised by the central
    vortex). Compute the derivative of that eigenvalue with respect to kappa_0
    via first-order perturbation theory, accounting for the change in Lagrange
    multiplier. Solve lambda_crit + kappa_0 * rate = 0 for kappa_0.

    For N=6 the critical mode is m=2 (Fourier mode 2 of the ring), its
    eigenvalue at kappa_0=0 is 0.5, and the rate is 2, giving kappa_crit = -1/4.
    """
    import sympy as sp

    N_val = int(N)
    z = np.exp(2j * np.pi * np.arange(N_val) / N_val)
    pos = np.concatenate([z.real, z.imag])

    # ------------------------------------------------------------------
    # Build ring-ring Hessian H_ring (2N x 2N) analytically
    # H = -sum_{j<k} ln|z_j - z_k|
    # d²H/dx_j dx_k = (dy²-dx²)/d⁴  [off-diagonal, same xy-block]
    # ------------------------------------------------------------------
    H_ring = np.zeros((2*N_val, 2*N_val))
    for j in range(N_val):
        for k in range(N_val):
            if j == k:
                continue
            dz = z[j] - z[k]
            dx, dy = dz.real, dz.imag
            d2 = dx**2 + dy**2
            d4 = d2**2
            h_xx = (dy**2 - dx**2) / d4
            h_yy = (dx**2 - dy**2) / d4
            h_xy = -2.0 * dx * dy / d4
            H_ring[j, j] -= h_xx;         H_ring[j+N_val, j+N_val] -= h_yy
            H_ring[j, j+N_val] -= h_xy;   H_ring[j+N_val, j] -= h_xy
            H_ring[j, k] += h_xx;         H_ring[j+N_val, k+N_val] += h_yy
            H_ring[j, k+N_val] += h_xy;   H_ring[j+N_val, k] += h_xy

    # ------------------------------------------------------------------
    # Build ring-central Hessian H_central (2N x 2N)
    # Contribution from H_central = -kappa_0 * sum_j ln|z_j|
    # For unit ring |z_j| = 1, d²/dx_j² ln|z_j| = (y_j²-x_j²)/|z_j|⁴ etc.
    # ------------------------------------------------------------------
    H_central = np.zeros((2*N_val, 2*N_val))
    for j in range(N_val):
        dx, dy = z[j].real, z[j].imag
        d2 = dx**2 + dy**2  # = 1 for unit ring
        d4 = d2**2
        h_xx = (dy**2 - dx**2) / d4
        h_yy = (dx**2 - dy**2) / d4
        h_xy = -2.0 * dx * dy / d4
        H_central[j, j] -= h_xx
        H_central[j+N_val, j+N_val] -= h_yy
        H_central[j, j+N_val] -= h_xy
        H_central[j+N_val, j] -= h_xy

    # ------------------------------------------------------------------
    # Constraint gradients and null-space basis
    # Constraints: L = sum|z_k|² (angular impulse),
    #              Px = sum x_k, Py = sum y_k (linear impulse)
    # ------------------------------------------------------------------
    grad_L  = 2 * pos
    grad_Px = np.concatenate([np.ones(N_val),  np.zeros(N_val)])
    grad_Py = np.concatenate([np.zeros(N_val), np.ones(N_val)])
    G = np.column_stack([grad_L, grad_Px, grad_Py])

    U_svd, S_svd, Vt_svd = np.linalg.svd(G.T)
    rank = int(np.sum(S_svd > 1e-10))
    null_basis = Vt_svd[rank:].T   # columns span tangent space of constraint surface

    # ------------------------------------------------------------------
    # Lagrange multiplier for ring-only energy (kappa_0 = 0)
    # nabla H_ring = mu_L * nabla L + mu_Px * nabla Px + mu_Py * nabla Py
    # ------------------------------------------------------------------
    grad_H_ring = numerical_gradient(
        lambda p: sum(
            -0.5 * np.log((p[j] - p[k])**2 + (p[j + N_val] - p[k + N_val])**2)
            for j in range(N_val) for k in range(j + 1, N_val)
        ),
        pos
    )
    mu_ring, _, _, _ = np.linalg.lstsq(G, grad_H_ring, rcond=None)
    mu_L_ring = float(mu_ring[0])

    # Lagrange multiplier for central-vortex energy (per unit kappa_0)
    # grad of -sum_j ln|z_j| at the unit ring
    grad_H_central = np.zeros(2 * N_val)
    for j in range(N_val):
        r2 = z[j].real**2 + z[j].imag**2
        grad_H_central[j]         = -z[j].real / r2
        grad_H_central[j + N_val] = -z[j].imag / r2
    mu_central, _, _, _ = np.linalg.lstsq(G, grad_H_central, rcond=None)
    mu_L_central = float(mu_central[0])   # d(mu_L)/d(kappa_0)

    # ------------------------------------------------------------------
    # Constrained Lagrangian Hessian at kappa_0 = 0
    # nabla² L_lagr = H_ring - 2*mu_L_ring*I  (since nabla²L = 2I)
    # Restricted to tangent space of constraint surface
    # ------------------------------------------------------------------
    H_lagr_ring = H_ring - 2.0 * mu_L_ring * np.eye(2 * N_val)
    H_ring_restricted = null_basis.T @ H_lagr_ring @ null_basis
    evals_ring, evecs_ring = np.linalg.eigh(H_ring_restricted)

    # Find the critical eigenvalue: smallest strictly positive eval
    # (the zero eval belongs to the rotational Goldstone mode for N<=6,
    # and the critical mode is the next one that kappa_0 drives negative)
    tol_zero = 1e-4
    pos_mask = evals_ring > tol_zero
    if not np.any(pos_mask):
        raise RuntimeError(f"No positive constrained eigenvalue found for N={N_val}")

    idx_crit = int(np.argmax(pos_mask))   # first index with eval > tol
    lambda_crit = float(evals_ring[idx_crit])
    v_crit_restricted = evecs_ring[:, idx_crit]
    v_crit = null_basis @ v_crit_restricted   # lift back to full space

    # ------------------------------------------------------------------
    # First-order perturbation theory: rate = d(lambda_crit)/d(kappa_0)
    # d(H_lagr)/d(kappa_0) = H_central - 2*mu_L_central*I
    # rate = v_crit^T [H_central - 2*mu_L_central*I] v_crit
    # ------------------------------------------------------------------
    d_H_lagr = H_central - 2.0 * mu_L_central * np.eye(2 * N_val)
    rate = float(v_crit @ d_H_lagr @ v_crit)

    if abs(rate) < 1e-12:
        raise RuntimeError(f"Rate is zero for N={N_val}; central vortex does not couple to critical mode")

    # kappa_crit: lambda_crit + kappa_crit * rate = 0
    kappa_crit_float = -lambda_crit / rate

    # Convert to exact sympy Rational
    result = sp.nsimplify(kappa_crit_float, rational=True, tolerance=1e-6)
    return result


def full_analysis_report(N_range: range = range(3, 11),
                         verbose: bool = True) -> dict:
    """Run constrained Hessian analysis for all N and print report."""
    results = {}
    for N in N_range:
        results[N] = constrained_hessian_analysis(N)

    if verbose:
        print("=" * 70)
        print("CONSTRAINED HESSIAN ANALYSIS: Regular N-gon energy landscape")
        print("Constraints: L = sum|z_k|^2 (angular impulse), P = sum z_k = 0")
        print("Lagrangian: L_lagr = H - mu_L*L,  Hessian = nabla^2 H - 2*mu_L*I")
        print("=" * 70)

        for N, r in results.items():
            status = "STABLE (min)" if r.is_stable else "UNSTABLE (saddle)"
            print(f"\n  N={N}: mu_L={r.mu_L:.4f}, shift={-2*r.mu_L:.4f}")
            print(f"    Constrained evals: {r.n_neg} neg, {r.n_zero} zero, {r.n_pos} pos")
            print(f"    H'' spiral (unconstrained): {r.spiral_H_pp:+.4f}")
            print(f"    Lagrangian along spiral:    {r.spiral_lagr:+.4f}")
            print(f"    -> {status}")

        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        for N, r in results.items():
            marker = "OK" if r.is_stable else "UNSTABLE"
            print(f"  N={N}: [{marker:>8s}]  "
                  f"{r.n_neg} neg, {r.n_zero} zero, {r.n_pos} pos  "
                  f"mu_L={r.mu_L:.3f}")

    return results
