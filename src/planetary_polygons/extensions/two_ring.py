"""
Two-ring vortex stability analysis.

Computes the constrained Hessian for M inner vortices at radius R1
plus N outer vortices at radius R2, all with unit circulation.

Key result (Proposition): For M >= 2 inner vortices, the two-ring
configuration generically has more negative Lagrangian eigenvalues
than the single-ring N-gon.  The center-plus-ring geometry (M=0,
single central vortex) is the UNIQUE configuration that preserves
the Z_N symmetry of the outer ring, which is why Proposition 4
(central vortex stabilization) works but two-ring stabilization
generically does not.

The mechanism: a central vortex at the Z_N fixed point contributes
a UNIFORM shift to all Fourier-mode eigenvalues (proportional to
kappa_0/R^2).  Inner ring vortices at M equally-spaced positions
break Z_N symmetry unless M divides N, and even when M|N the
coupling introduces M-fold modulations of the eigenvalues that
generically create new negative modes.
"""
import numpy as np
from fractions import Fraction


def two_ring_positions(N, M, R1, R2):
    """
    Positions of M inner + N outer vortices.

    Inner: M vortices at radius R1, equally spaced.
    Outer: N vortices at radius R2, equally spaced.

    Returns complex array of length M+N.
    """
    z_inner = R1 * np.exp(2j * np.pi * np.arange(M) / M)
    z_outer = R2 * np.exp(2j * np.pi * np.arange(N) / N)
    return np.concatenate([z_inner, z_outer])


def two_ring_hessian(N, M, R1, R2):
    """
    Full (2(M+N)) x (2(M+N)) Hessian of H = -sum_{j<k} ln|z_j - z_k|
    at the two-ring configuration.
    """
    z = two_ring_positions(N, M, R1, R2)
    Ntot = M + N
    H = np.zeros((2 * Ntot, 2 * Ntot))

    for j in range(Ntot):
        for k in range(Ntot):
            if j == k:
                continue
            dz = z[j] - z[k]
            dx, dy = dz.real, dz.imag
            d2 = dx**2 + dy**2
            if d2 < 1e-30:
                continue
            d4 = d2**2
            h_xx = (dy**2 - dx**2) / d4
            h_yy = (dx**2 - dy**2) / d4
            h_xy = -2 * dx * dy / d4
            # Diagonal
            H[j, j] -= h_xx
            H[j + Ntot, j + Ntot] -= h_yy
            H[j, j + Ntot] -= h_xy
            H[j + Ntot, j] -= h_xy
            # Off-diagonal
            H[j, k] += h_xx
            H[j + Ntot, k + Ntot] += h_yy
            H[j, k + Ntot] += h_xy
            H[j + Ntot, k] += h_xy

    return H


def two_ring_constrained_eigenvalues(N, M, R1, R2):
    """
    Constrained Lagrangian Hessian eigenvalues for the two-ring system.

    Constraints: L = sum |z_k|^2 (angular impulse), Px = sum x_k,
    Py = sum y_k (linear impulse).

    Returns sorted eigenvalues on the constraint tangent space.
    """
    z = two_ring_positions(N, M, R1, R2)
    Ntot = M + N
    pos = np.concatenate([z.real, z.imag])

    H = two_ring_hessian(N, M, R1, R2)

    # Constraint gradients
    grad_L = 2 * pos
    grad_Px = np.concatenate([np.ones(Ntot), np.zeros(Ntot)])
    grad_Py = np.concatenate([np.zeros(Ntot), np.ones(Ntot)])
    G = np.column_stack([grad_L, grad_Px, grad_Py])

    # Energy gradient (numerical)
    def energy(p):
        nn = len(p) // 2
        x, y = p[:nn], p[nn:]
        e = 0.0
        for j in range(nn):
            for k in range(j + 1, nn):
                r2 = (x[j] - x[k])**2 + (y[j] - y[k])**2
                if r2 > 1e-30:
                    e -= 0.5 * np.log(r2)
        return e

    eps = 1e-7
    grad_H = np.zeros(2 * Ntot)
    for i in range(2 * Ntot):
        p_plus = pos.copy()
        p_minus = pos.copy()
        p_plus[i] += eps
        p_minus[i] -= eps
        grad_H[i] = (energy(p_plus) - energy(p_minus)) / (2 * eps)

    # Lagrange multipliers
    mu_vec, _, _, _ = np.linalg.lstsq(G, grad_H, rcond=None)
    mu_L = float(mu_vec[0])

    # Lagrangian Hessian
    H_lagr = H - 2 * mu_L * np.eye(2 * Ntot)

    # Project onto constraint tangent space
    U, S, Vt = np.linalg.svd(G.T)
    rank = np.sum(S > 1e-10)
    null_basis = Vt[rank:].T

    H_restricted = null_basis.T @ H_lagr @ null_basis
    evals = np.sort(np.linalg.eigvalsh(H_restricted))
    return evals


def two_ring_stability_survey(N_values=(5, 6, 8), M_range=range(1, 9),
                               R_ratios=(1.5, 2.0, 3.0)):
    """
    Survey two-ring stability across parameter space.

    Returns list of dicts with N, M, R2/R1, n_neg, min_eval.
    """
    results = []
    for N in N_values:
        for M in M_range:
            for ratio in R_ratios:
                R1 = 0.5
                R2 = R1 * ratio
                evals = two_ring_constrained_eigenvalues(N, M, R1, R2)
                tol = 1e-6
                n_neg = int(np.sum(evals < -tol))
                n_zero = int(np.sum(np.abs(evals) <= tol))
                n_pos = int(np.sum(evals > tol))
                results.append({
                    'N': N, 'M': M, 'R2_over_R1': ratio,
                    'n_neg': n_neg, 'n_zero': n_zero, 'n_pos': n_pos,
                    'min_eval': float(evals[0]),
                    'stable': n_neg == 0,
                })
    return results


def center_vs_ring_comparison(N=8):
    """
    Compare: center vortex (M=0, kappa_0) vs inner ring (M>=1).

    The center vortex preserves Z_N symmetry → uniform eigenvalue shift.
    The inner ring breaks Z_N (unless M|N) → non-uniform coupling.

    Returns comparison dict.
    """
    from planetary_polygons.core.hessian import (
        constrained_hessian_with_central_vortex,
        constrained_hessian_analysis,
    )

    # Single ring (no center, no inner ring)
    base = constrained_hessian_analysis(N)

    # Center vortex at kappa_ratio = 0.5
    center = constrained_hessian_with_central_vortex(N, 0.5)

    # Inner ring: M=1 at various radii (M=1 is actually a center vortex
    # but at nonzero radius, breaking Z_N)
    inner_results = {}
    for M in [2, 3, 4]:
        for ratio in [1.5, 2.0, 3.0]:
            R1 = 0.5
            R2 = R1 * ratio
            evals = two_ring_constrained_eigenvalues(N, M, R1, R2)
            tol = 1e-6
            n_neg = int(np.sum(evals < -tol))
            inner_results[(M, ratio)] = {
                'n_neg': n_neg,
                'min_eval': float(evals[0]),
                'stable': n_neg == 0,
            }

    return {
        'N': N,
        'base_n_neg': base.n_neg,
        'center_n_neg': center.n_neg,
        'center_stable': center.is_stable,
        'inner_ring_results': inner_results,
    }


def symmetry_breaking_theorem_check(N_values=(5, 6, 7, 8, 9, 10),
                                      M_values=(2, 3, 4, 5, 6)):
    """
    Verify the symmetry-breaking theorem:

    For M >= 2 inner vortices at any radius R1 < R2, the two-ring
    configuration (M inner, N outer) has AT LEAST as many negative
    eigenvalues as the single outer ring alone, and generically more.

    The center (M=0) is the unique stabilizing configuration because
    it preserves Z_N.
    """
    from planetary_polygons.core.hessian import constrained_hessian_analysis

    results = []
    for N in N_values:
        base = constrained_hessian_analysis(N)
        base_n_neg = base.n_neg

        for M in M_values:
            if M >= N:
                continue
            for ratio in [1.5, 2.0, 3.0, 5.0]:
                R1 = 0.4
                R2 = R1 * ratio
                evals = two_ring_constrained_eigenvalues(N, M, R1, R2)
                tol = 1e-6
                n_neg = int(np.sum(evals < -tol))

                results.append({
                    'N': N, 'M': M, 'R2_over_R1': ratio,
                    'base_n_neg': base_n_neg,
                    'two_ring_n_neg': n_neg,
                    'additional_unstable': n_neg - base_n_neg,
                    'weakly_more_unstable': n_neg >= base_n_neg,
                })

    return results


if __name__ == "__main__":
    print("Two-ring stability survey")
    print("=" * 70)

    results = symmetry_breaking_theorem_check()

    print(f"\n{'N':>3} {'M':>3} {'R2/R1':>6} {'base_neg':>8} {'2ring_neg':>9} {'extra':>6} {'>=base':>6}")
    print("-" * 50)
    all_weakly = True
    for r in results:
        flag = "YES" if r['weakly_more_unstable'] else "NO"
        if not r['weakly_more_unstable']:
            all_weakly = False
        print(f"{r['N']:>3} {r['M']:>3} {r['R2_over_R1']:>6.1f} "
              f"{r['base_n_neg']:>8} {r['two_ring_n_neg']:>9} "
              f"{r['additional_unstable']:>6} {flag:>6}")

    print(f"\nTheorem check: two-ring always >= base unstable modes: "
          f"{'PASSED' if all_weakly else 'FAILED'}")
