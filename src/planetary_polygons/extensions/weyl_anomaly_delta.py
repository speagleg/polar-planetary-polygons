r"""Test whether the Weyl anomaly δ_m is Δ-independent.

The three-layer decomposition:
    λ_m = C₁(ξ) − f(m,N) + δ_m(N)

where:
    C₁ = Ricci scalar (runs with ξ, mode-independent)
    f(m,N) = m(N−m)/2 = Casimir (universal, surface-independent)
    δ_m = Weyl anomaly (topological, traceless, ξ-independent)

For Δ = 0 (logarithmic interaction), δ_m is known exactly on surfaces
where we can compute the eigenvalue. On the flat plane, δ_m = 0 by
definition (the Havelock identity is exact). On a torus, δ_m ≠ 0.

KEY CONJECTURE: δ_m is Δ-independent.

If true, the number-theoretic content (Pythagorean sign rule, Hecke
eigenvalues, Langlands cases) survives the transition from 2D to 3+1D.

TEST: Compute eigenvalues on a square torus with |x-y|^{-2Δ} interaction,
extract δ_m = λ_m − C₁ + f_Δ(m,N), and check independence in Δ.

On the torus, the Green's function has lattice corrections, so δ_m ≠ 0.
The torus provides the simplest ARITHMETIC surface to test on.
"""

import math
import numpy as np


# ============================================================
# Square torus: Z²-lattice Green's function images
# ============================================================

def torus_interaction(z1, z2, Delta, L=1.0, n_images=5):
    """Interaction V(z1, z2) on a square torus of side L.

    For Δ = 0: V = -log|z1 - z2| + lattice corrections (Eisenstein sum)
    For Δ > 0: V = Σ' |z1 - z2 + nL|^{-2Δ}  (Epstein zeta function)

    n_images: number of lattice images in each direction.
    Uses the image sum directly (converges for Δ > 0, needs regularization for Δ = 0).
    """
    dz = z1 - z2
    dx, dy = dz.real, dz.imag

    if abs(Delta) < 1e-10:
        # Logarithmic case: use Weierstrass sigma / theta function
        # For simplicity, use image sum of -log|z + nL| with cutoff
        # This needs careful regularization; use the standard result instead.
        return _torus_log_green(dx, dy, L, n_images)

    # Power-law case: image sum converges for Δ > 0
    total = 0.0
    for nx in range(-n_images, n_images + 1):
        for ny in range(-n_images, n_images + 1):
            x = dx + nx * L
            y = dy + ny * L
            r2 = x * x + y * y
            if r2 < 1e-30:
                continue  # Skip self-image
            total += r2 ** (-Delta)
    return total


def _torus_log_green(dx, dy, L, n_images):
    """Regularized logarithmic Green's function on the square torus.

    G(z) = -log|θ₁(πz/L, q)| + const

    where θ₁ is the Jacobi theta function and q = e^{-πτ} with τ = 1
    for the square torus.

    For simplicity, use the image sum with careful regularization.
    """
    # Direct image sum with renormalization
    # -Σ' log|z + nL| = -log|z| - Σ_{n≠0} [log|z+nL| - log|nL|] - Σ_{n≠0} log|nL|
    # The last sum is a constant that cancels in eigenvalue differences.

    r0 = math.sqrt(dx * dx + dy * dy)
    if r0 < 1e-30:
        return float('inf')

    total = -math.log(r0)
    for nx in range(-n_images, n_images + 1):
        for ny in range(-n_images, n_images + 1):
            if nx == 0 and ny == 0:
                continue
            x = dx + nx * L
            y = dy + ny * L
            r = math.sqrt(x * x + y * y)
            r_lattice = math.sqrt((nx * L) ** 2 + (ny * L) ** 2)
            # Regularized: subtract the lattice-only part
            total += -math.log(r) + math.log(r_lattice)
    return total


# ============================================================
# N-ring on the torus
# ============================================================

def torus_ring_positions(N, R, L=1.0):
    """N equally-spaced points on a ring of radius R on the torus.

    The ring is centered at the origin (mod L).
    Returns list of complex numbers.
    """
    return [R * np.exp(2j * math.pi * k / N) for k in range(N)]


def torus_ring_energy(N, R, Delta, L=1.0, n_images=5):
    """Total energy of the N-ring on the torus."""
    positions = torus_ring_positions(N, R, L)
    E = 0.0
    for j in range(N):
        for k in range(j + 1, N):
            E += torus_interaction(positions[j], positions[k], Delta, L, n_images)
    return E


def torus_angular_eigenvalue(N, m, R, Delta, L=1.0, n_images=5, eps=1e-6):
    """Angular Hessian eigenvalue for mode m on the torus.

    Finite-difference computation: perturb φ_k → φ_k + a·cos(2πmk/N)
    and compute d²E/da².
    """
    def energy_perturbed(a):
        E = 0.0
        positions = []
        for k in range(N):
            phi = 2 * math.pi * k / N + a * math.cos(2 * math.pi * m * k / N)
            positions.append(R * complex(math.cos(phi), math.sin(phi)))

        for j in range(N):
            for k in range(j + 1, N):
                E += torus_interaction(positions[j], positions[k], Delta, L, n_images)
        return E

    E_p = energy_perturbed(eps)
    E_0 = energy_perturbed(0)
    E_m = energy_perturbed(-eps)
    return (E_p - 2 * E_0 + E_m) / eps ** 2


def torus_radial_stiffness(N, R, Delta, L=1.0, n_images=5, eps=1e-6):
    """Radial second variation d²E/dR² on the torus."""
    E_p = torus_ring_energy(N, R + eps, Delta, L, n_images)
    E_0 = torus_ring_energy(N, R, Delta, L, n_images)
    E_m = torus_ring_energy(N, R - eps, Delta, L, n_images)
    return (E_p - 2 * E_0 + E_m) / eps ** 2


# ============================================================
# The generalized Casimir on the flat plane (for reference)
# ============================================================

def flat_casimir(m, N, Delta):
    """The flat-plane Casimir h(m, N, Δ).

    h(m, N, Δ) = Σ_{p=1}^{N-1} w̃(p, Δ) (1 - cos(2πmp/N))

    For Δ = 0: h = m(N-m) (before the /2 normalization).
    """
    total = 0.0
    for p in range(1, N):
        u = math.pi * p / N
        sin_u = math.sin(u)
        cos_u = math.cos(u)
        if abs(sin_u) < 1e-30:
            continue
        w = sin_u ** (-2 * Delta - 2) * (1 + 2 * Delta * cos_u ** 2)
        total += w * (1 - math.cos(2 * math.pi * m * p / N))
    return total


# ============================================================
# Weyl anomaly extraction
# ============================================================

def extract_weyl_anomaly(N, R, Delta, L=1.0, n_images=5):
    """Extract δ_m for each mode m = 1, ..., N-1.

    δ_m = (angular_eigenvalue_m − C₁) + flat_casimir(m)

    where C₁ is extracted from the average:
        C₁ = (1/(N-1)) Σ_m [angular_eigenvalue_m + flat_casimir(m)]

    Wait — the decomposition is:
        angular_eigenvalue_m = C₁ − flat_casimir(m) + δ_m

    So: C₁ = angular_eigenvalue_m + flat_casimir(m) − δ_m

    Since Σ δ_m = 0 (traceless), summing over m:
        (N-1)·C₁ = Σ_m angular_eigenvalue_m + Σ_m flat_casimir(m)

    Then: δ_m = angular_eigenvalue_m − C₁ + flat_casimir(m)

    BUT: the "flat_casimir" for Δ > 0 is NOT m(N-m)/2 — it's h(m,N,Δ)/2.
    We need the normalization right.

    Actually, let's be more careful. On the torus vs flat plane:

    The angular eigenvalue ON THE TORUS includes:
    (a) The flat-plane part (from the primary image)
    (b) The lattice correction (from image sums)

    For Δ = 0:
        angular_torus_m = flat_angular_m + correction_m
        flat_angular_m = (R^{-2}) · m(N-m)/2  (with R-dependent prefactor)
        correction_m = δ_m (the Weyl anomaly)

    For Δ > 0:
        angular_torus_m = flat_angular_m(Δ) + correction_m(Δ)
        flat_angular_m(Δ) = (some R,Δ-dependent prefactor) · h(m,N,Δ)/2

    The test: does correction_m(Δ) = correction_m(0)?

    Approach: compute eigenvalues at two or more Δ values, subtract the
    flat-plane part (which we know analytically), and compare the remainders.
    """
    eigenvalues = {}
    for m in range(1, N):
        mu = torus_angular_eigenvalue(N, m, R, Delta, L, n_images)
        eigenvalues[m] = mu

    # The flat-plane angular eigenvalue scales as:
    # For Δ = 0: (1/R²) · m(N-m)/2
    # For Δ > 0: the angular Hessian on the flat plane (just the primary vertex pair)
    #            scales with R^{-2Δ-2} · h(m,N,Δ)/something.
    #
    # Rather than figure out the exact normalization, let's extract δ_m
    # using the traceless condition. Define:
    #
    # δ_m_raw = eigenvalue_m - <eigenvalue> (zero-mean)
    #
    # The flat-plane part also has zero mean if we subtract its average.
    # So δ_m = (eigenvalue_m - <eigenvalue>) - (flat_m - <flat>)
    #
    # But the flat part has the same SHAPE as h(m,N,Δ) and its average
    # is (1/(N-1)) Σ h(m,N,Δ). So:
    #
    # Actually, let's use ratios. On the flat plane, the ratio
    # eigenvalue_m / eigenvalue_1 = h(m,N,Δ) / h(1,N,Δ).
    #
    # On the torus: eigenvalue_m / eigenvalue_1 = h(m,N,Δ)/h(1,N,Δ) + δ_m_correction.
    #
    # The δ_m_correction in the ratio is what we want to test for Δ-independence.

    # Method: compute ratio anomaly
    # ratio_m = (torus_eigenvalue_m / torus_eigenvalue_1) - (flat_h_m / flat_h_1)
    flat_h = {m: flat_casimir(m, N, Delta) for m in range(1, N)}

    if abs(eigenvalues[1]) < 1e-30 or abs(flat_h[1]) < 1e-30:
        return None

    ratio_anomaly = {}
    for m in range(1, N):
        torus_ratio = eigenvalues[m] / eigenvalues[1]
        flat_ratio = flat_h[m] / flat_h[1]
        ratio_anomaly[m] = torus_ratio - flat_ratio

    # Also extract absolute anomaly using traceless decomposition
    # C₁ = (1/(N-1)) Σ (eigenvalue_m + flat_m_normalized)
    # But we need the normalization...

    # Simpler: the anomaly δ_m (up to a common scale) can be extracted as:
    # eigenvalue_m = A · h(m,N,Δ) + B · δ_m
    # where A depends on R,Δ and B depends on R,Δ.
    # The RATIO δ_m / h(m_crit,N,Δ) tells us the relative importance.
    #
    # For the Δ-independence test, we just need the SHAPE of the anomaly
    # (normalized to sum to 0 and norm 1).

    # Extract shape: anomaly_m = eigenvalue_m - best_fit(A * flat_h_m)
    # Best fit A = Σ(eigenvalue_m * flat_h_m) / Σ(flat_h_m²)
    ev_list = [eigenvalues[m] for m in range(1, N)]
    fh_list = [flat_h[m] for m in range(1, N)]

    A_fit = sum(e * f for e, f in zip(ev_list, fh_list)) / sum(f * f for f in fh_list)

    absolute_anomaly = {}
    for m in range(1, N):
        absolute_anomaly[m] = eigenvalues[m] - A_fit * flat_h[m]

    # Normalize to unit norm
    norm = math.sqrt(sum(v ** 2 for v in absolute_anomaly.values()))
    if norm < 1e-30:
        normalized_anomaly = {m: 0.0 for m in range(1, N)}
    else:
        normalized_anomaly = {m: v / norm for m, v in absolute_anomaly.items()}

    return {
        'N': N,
        'R': R,
        'Delta': Delta,
        'L': L,
        'eigenvalues': eigenvalues,
        'flat_casimir': flat_h,
        'A_fit': A_fit,
        'ratio_anomaly': ratio_anomaly,
        'absolute_anomaly': absolute_anomaly,
        'normalized_anomaly': normalized_anomaly,
        'anomaly_norm': norm,
    }


def check_delta_independence(N, R=0.2, L=1.0, n_images=3,
                            Delta_values=None):
    """Test whether the Weyl anomaly shape is Δ-independent.

    Computes the normalized anomaly at several Δ values and measures
    the inner product between each pair. If δ_m is Δ-independent,
    all inner products should be ≈ 1.

    Returns dict with results and inner product matrix.
    """
    if Delta_values is None:
        Delta_values = [0.0, 0.25, 0.5, 1.0, 2.0]

    anomalies = []
    for Delta in Delta_values:
        result = extract_weyl_anomaly(N, R, Delta, L, n_images)
        if result is None:
            anomalies.append(None)
        else:
            anomalies.append(result)

    # Inner product matrix
    n = len(Delta_values)
    inner_products = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if anomalies[i] is None or anomalies[j] is None:
                inner_products[i, j] = float('nan')
                continue
            a_i = anomalies[i]['normalized_anomaly']
            a_j = anomalies[j]['normalized_anomaly']
            inner_products[i, j] = sum(
                a_i[m] * a_j[m] for m in range(1, N)
            )

    return {
        'N': N,
        'R': R,
        'L': L,
        'Delta_values': Delta_values,
        'anomalies': anomalies,
        'inner_products': inner_products,
    }


if __name__ == '__main__':
    print("=" * 60)
    print("Weyl anomaly Δ-independence test")
    print("=" * 60)

    for N in [5, 6, 7, 8]:
        print(f"\n--- N = {N} ---")
        result = test_delta_independence(N, R=0.15, L=1.0, n_images=3)

        print(f"Inner product matrix (should be ≈1 if Δ-independent):")
        print(f"  Δ values: {result['Delta_values']}")
        for i, Di in enumerate(result['Delta_values']):
            row = [f"{result['inner_products'][i,j]:.6f}"
                   for j in range(len(result['Delta_values']))]
            print(f"  Δ={Di:4.2f}: [{', '.join(row)}]")

        # Show anomaly norms
        print(f"  Anomaly norms:")
        for a in result['anomalies']:
            if a is not None:
                print(f"    Δ={a['Delta']:4.2f}: ||δ|| = {a['anomaly_norm']:.6e}")
