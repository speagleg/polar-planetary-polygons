r"""Dynamical matrix for the triangular lattice with V = r^{-2Δ}.

The phonon spectrum of the triangular Bravais lattice under a power-law
repulsive interaction. The dynamical matrix at wavevector k is:

  D_{αβ}(k) = Σ_{R≠0} [V''(R) R̂_α R̂_β + V'(R)/R (δ_{αβ} - R̂_α R̂_β)]
              × (1 - cos(k·R))

For V = r^{-2Δ}: V' = -2Δ r^{-2Δ-1}, V'' = 2Δ(2Δ+1) r^{-2Δ-2}.

The lattice sum converges for 2Δ+2 > 2 (Δ > 0). At Δ = 0 (logarithmic),
Ewald summation is needed.

KEY RESULT: Δ_tri is the critical conformal dimension where the minimum
phonon frequency crosses zero — the triangular lattice melting transition.
"""

import math
import numpy as np


# ============================================================
# Triangular lattice geometry
# ============================================================

# Lattice vectors (edge length = 1)
A1 = np.array([1.0, 0.0])
A2 = np.array([0.5, math.sqrt(3) / 2])

# Reciprocal lattice vectors: b_i · a_j = 2π δ_ij
# det(A) = sqrt(3)/2
# b1 = 2π/det * (a2y, -a2x) rotated... standard formula:
_det = A1[0] * A2[1] - A1[1] * A2[0]  # sqrt(3)/2
B1 = 2 * math.pi / _det * np.array([A2[1], -A2[0]])
B2 = 2 * math.pi / _det * np.array([-A1[1], A1[0]])

# High-symmetry points in the Brillouin zone (fractional coordinates)
GAMMA = np.array([0.0, 0.0])
M_POINT = B1 / 2  # midpoint of zone edge
K_POINT = (B1 + B2) / 3  # zone corner


def lattice_vectors(n_shells):
    """Generate triangular lattice vectors up to n_shells.

    Returns array of shape (M, 2) excluding the origin.
    """
    vecs = []
    for i in range(-n_shells, n_shells + 1):
        for j in range(-n_shells, n_shells + 1):
            if i == 0 and j == 0:
                continue
            R = i * A1 + j * A2
            vecs.append(R)
    return np.array(vecs)


def lattice_norms_sorted(n_shells):
    """Distinct squared norms of the triangular lattice, sorted."""
    vecs = lattice_vectors(n_shells)
    r2 = np.sum(vecs ** 2, axis=1)
    return np.sort(np.unique(np.round(r2, 8)))


# ============================================================
# Dynamical matrix
# ============================================================

def dynamical_matrix(k, Delta, n_shells=15):
    """2×2 dynamical matrix D(k) for the triangular lattice.

    D_{αβ}(k) = Σ_{R≠0} w_{αβ}(R) (1 - cos(k·R))

    where w_{αβ} = V''(R) R̂_α R̂_β + V'(R)/R (δ_{αβ} - R̂_α R̂_β).

    For V = r^{-2Δ}:
      V'/r = -2Δ r^{-2Δ-2}
      V''  = 2Δ(2Δ+1) r^{-2Δ-2}

    So: w_{αβ} = 2Δ r^{-2Δ-2} [(2Δ+1) R̂_α R̂_β - (δ_{αβ} - R̂_α R̂_β)]
              = 2Δ r^{-2Δ-2} [(2Δ+2) R̂_α R̂_β - δ_{αβ}]

    This matches the Hessian formula: h_{αβ} = 2Δ r^{-2Δ-4} [(2Δ+2) R_α R_β - r² δ_{αβ}]
    = 2Δ r^{-2Δ-2} [(2Δ+2) R̂_α R̂_β - δ_{αβ}].
    """
    vecs = lattice_vectors(n_shells)
    D = np.zeros((2, 2))

    for R in vecs:
        r2 = R[0] ** 2 + R[1] ** 2
        r = math.sqrt(r2)
        kr = k[0] * R[0] + k[1] * R[1]
        phase = 1 - math.cos(kr)

        if abs(phase) < 1e-15:
            continue

        if abs(Delta) < 1e-10:
            # Log case: V = -log(r), V'/r = -1/r², V'' = 1/r² + 1/r² ...
            # V'(r) = -1/r → V'/r = -1/r²
            # V''(r) = 1/r²
            # w_{αβ} = (1/r²)(R̂_α R̂_β) + (-1/r²)(δ_{αβ} - R̂_α R̂_β)
            #        = (1/r²)(2 R̂_α R̂_β - δ_{αβ})
            coeff = 1.0 / r2
            for a in range(2):
                for b in range(2):
                    Rhat_a = R[a] / r
                    Rhat_b = R[b] / r
                    w = coeff * (2 * Rhat_a * Rhat_b - (1 if a == b else 0))
                    D[a, b] += w * phase
        else:
            coeff = 2 * Delta * r2 ** (-Delta - 1)  # = 2Δ r^{-2Δ-2}
            for a in range(2):
                for b in range(2):
                    Rhat_a = R[a] / r
                    Rhat_b = R[b] / r
                    w = coeff * ((2 * Delta + 2) * Rhat_a * Rhat_b
                                 - (1 if a == b else 0))
                    D[a, b] += w * phase

    return D


def phonon_eigenvalues(k, Delta, n_shells=15):
    """Eigenvalues of D(k). Returns sorted (ω₁², ω₂²)."""
    D = dynamical_matrix(k, Delta, n_shells)
    evals = np.linalg.eigvalsh(D)
    return evals


# ============================================================
# Brillouin zone scan
# ============================================================

def bz_scan(Delta, n_k=50, n_shells=15):
    """Scan the Brillouin zone and find the minimum eigenvalue.

    Samples along Γ-M-K-Γ high-symmetry path and on a grid.
    Returns (min_eval, k_min, all_data).
    """
    min_eval = float('inf')
    k_min = None
    all_data = []

    # High-symmetry path: Γ → M → K → Γ
    path_points = []
    for i in range(n_k + 1):
        t = i / n_k
        path_points.append(('GM', (1 - t) * GAMMA + t * M_POINT))
    for i in range(1, n_k + 1):
        t = i / n_k
        path_points.append(('MK', (1 - t) * M_POINT + t * K_POINT))
    for i in range(1, n_k + 1):
        t = i / n_k
        path_points.append(('KG', (1 - t) * K_POINT + t * GAMMA))

    for label, k in path_points:
        evals = phonon_eigenvalues(k, Delta, n_shells)
        e_min = evals[0]
        all_data.append((label, k, evals))
        if e_min < min_eval and np.linalg.norm(k) > 0.01:
            min_eval = e_min
            k_min = k.copy()

    # Also check a grid in the irreducible BZ
    for i in range(n_k + 1):
        for j in range(i + 1):
            s1 = i / n_k
            s2 = j / n_k
            if s1 + s2 > 1:
                continue
            k = s1 * B1 / 2 + s2 * B2 / 2
            if np.linalg.norm(k) < 0.01:
                continue
            evals = phonon_eigenvalues(k, Delta, n_shells)
            if evals[0] < min_eval:
                min_eval = evals[0]
                k_min = k.copy()

    return min_eval, k_min, all_data


def find_delta_tri(Delta_lo=0.5, Delta_hi=1.5, tol=1e-10, n_shells=20):
    """Find Δ_tri where the minimum phonon frequency crosses zero.

    Uses bisection on min_k min_eigenvalue D(k, Δ).
    """
    def min_eigenvalue(Delta):
        me, _, _ = bz_scan(Delta, n_k=30, n_shells=n_shells)
        return me

    m_lo = min_eigenvalue(Delta_lo)
    m_hi = min_eigenvalue(Delta_hi)

    if m_lo >= 0 and m_hi >= 0:
        return None  # Stable throughout
    if m_lo < 0 and m_hi < 0:
        return None  # Unstable throughout

    for _ in range(60):
        Delta_mid = (Delta_lo + Delta_hi) / 2
        m_mid = min_eigenvalue(Delta_mid)
        if abs(Delta_hi - Delta_lo) < tol:
            break
        if (m_lo >= 0) == (m_mid >= 0):
            Delta_lo = Delta_mid
            m_lo = m_mid
        else:
            Delta_hi = Delta_mid

    return (Delta_lo + Delta_hi) / 2


# ============================================================
# Complexity functionals (Computations 5.4-5.5)
# ============================================================

def stable_mode_count(Delta, N_max=20):
    """Count stable modes: #{(N,m) : λ_m(N,Δ) > 0} for N=3..N_max."""
    from planetary_polygons.extensions.ncrit_delta import constrained_hessian_delta
    count = 0
    for N in range(3, N_max + 1):
        r = constrained_hessian_delta(N, Delta)
        evals = r['constrained_evals']
        count += int(np.sum(evals > 1e-4))
    return count


def weighted_complexity(Delta, N_max=12):
    """Σ λ_m for all stable modes."""
    from planetary_polygons.extensions.ncrit_delta import constrained_hessian_delta
    total = 0.0
    for N in range(3, N_max + 1):
        r = constrained_hessian_delta(N, Delta)
        evals = r['constrained_evals']
        total += float(np.sum(evals[evals > 1e-4]))
    return total


def log_complexity(Delta, N_max=12):
    """Σ ln(λ_m) for all stable modes (one-loop effective action)."""
    from planetary_polygons.extensions.ncrit_delta import constrained_hessian_delta
    total = 0.0
    for N in range(3, N_max + 1):
        r = constrained_hessian_delta(N, Delta)
        evals = r['constrained_evals']
        pos = evals[evals > 1e-4]
        total += float(np.sum(np.log(pos))) if len(pos) > 0 else 0.0
    return total


if __name__ == '__main__':
    print("Triangular lattice dynamical matrix")
    print("Checking high-symmetry points at Δ=1.0:")
    for name, k in [('Γ', GAMMA), ('M', M_POINT), ('K', K_POINT)]:
        evals = phonon_eigenvalues(k, 1.0)
        print(f"  {name}: ω² = [{evals[0]:.4f}, {evals[1]:.4f}]")
