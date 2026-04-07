r"""
THEOREM (S³ vortex dynamics — GAP A):
    Point vortices on S³ interact via the Green's function of the
    Laplacian on S³. The 600-cell (120 I* quaternion vertices) is
    the natural I*-symmetric vortex configuration on S³.

DERIVATION (from first principles):
    Step 1: S³ Laplacian eigenvalues -Δf = l(l+2)f, degeneracy (l+1)²
    Step 2: Zonal eigenfunctions = Gegenbauer C_l^1(cos χ)
    Step 3: Green's function from eigenfunction expansion → closed form
    Step 4: Vortex Hamiltonian H = -Σ κ_j κ_k G(χ_{jk})
    Step 5: S³ Havelock decomposition via Gegenbauer polynomials

The S³ framework sits at the top of the Vortex Universe hierarchy:
    S³ (Hopf, I*→E₈) → S² (Platonic, A₅→E₈) → R² (polygon, Z₇→SM)
"""

import numpy as np
from math import pi, sin, cos, acos, sqrt, log


# =====================================================================
# Step 1: S³ Laplacian eigenvalues
# =====================================================================

def s3_laplacian_eigenvalue(l):
    """Eigenvalue of -Δ on the unit S³ for the l-th harmonic.

    -Δ Y_l = l(l+2) Y_l

    Degeneracy: (l+1)² (dimension of the l-th harmonic space on S³).

    Compare with S²: -Δ Y_l = l(l+1) Y_l, degeneracy 2l+1.
    The shift l(l+1) → l(l+2) reflects dim(S³) = 3 vs dim(S²) = 2.
    """
    return l * (l + 2)


# =====================================================================
# Step 2: Gegenbauer polynomials C_l^1(x)
# =====================================================================

def gegenbauer_C1(l, x):
    r"""Gegenbauer polynomial C_l^1(x) via recurrence.

    These are the zonal spherical functions on S³ = SO(4)/SO(3).
    Also known as Chebyshev polynomials of the second kind: C_l^1 = U_l.

    Recurrence:
        C_0^1(x) = 1
        C_1^1(x) = 2x
        C_{l+1}^1(x) = (2x C_l^1(x) - C_{l-1}^1(x))

    Key properties:
        C_l^1(1) = l + 1 (normalization at the pole)
        C_l^1(cos χ) = sin((l+1)χ) / sin(χ) (trigonometric form)

    The normalized zonal spherical function is C_l^1(cos χ) / (l+1).
    """
    if l == 0:
        return 1.0
    if l == 1:
        return 2.0 * x
    c_prev = 1.0
    c_curr = 2.0 * x
    for n in range(1, l):
        c_next = 2 * x * c_curr - c_prev
        c_prev = c_curr
        c_curr = c_next
    return c_curr


# =====================================================================
# Step 3: Green's function on S³
# =====================================================================

def s3_green_function(chi):
    r"""Green's function of the Laplacian on the unit S³.

    DERIVATION: The scalar Green's function G(χ) satisfies
        ΔG = -δ + 1/Vol(S³)
    where Vol(S³) = 2π².

    Eigenfunction expansion:
        G(χ) = -Σ_{l≥1} [1/(l(l+2))] × [(l+1)²/(2π²)] × [C_l^1(cos χ)/(l+1)]
              = -(1/(2π²)) Σ_{l≥1} (l+1)/(l(l+2)) × C_l^1(cos χ)/(l+1)
              = -(1/(2π²)) Σ_{l≥1} C_l^1(cos χ) / (l(l+2))

    Using C_l^1(cos χ) = sin((l+1)χ)/sin(χ) and partial fractions:
        1/(l(l+2)) = (1/2)[1/l - 1/(l+2)]

    The sum telescopes to give:
        G(χ) = -(1/(4π²)) × (π - χ) / sin(χ)

    CLOSED FORM (verified by direct substitution into Δf = f'' + 2cot(χ)f'):
        G(χ) = (1/(4π²)) × (π - χ) × cot(χ)

    where cot(χ) = cos(χ)/sin(χ). Satisfies ΔG = 1/(2π²) for χ ∈ (0,π).

    PROPERTIES:
        G(0⁺) → +∞ (Coulomb singularity, ≈ π/(4π²χ) as χ→0)
        G(π/2) = 0  (cot(π/2) = 0)
        G(π⁻) → -1/(4π²) (finite at antipode)
    """
    if abs(chi) < 1e-12:
        return 1.0 / (4 * pi**2) * pi / max(chi, 1e-15)
    if abs(chi - pi) < 1e-12:
        return -1.0 / (4 * pi**2)
    return 1.0 / (4 * pi**2) * (pi - chi) * cos(chi) / sin(chi)


def s3_green_eigenfunction_expansion(chi, l_max=50):
    """Partial sum of the eigenfunction expansion for G(χ).

    From the addition theorem on S³:
        G(χ) = -(1/(2π²)) Σ_{l=1}^{l_max} (l+1) C_l^1(cos χ) / (l(l+2))

    The (l+1) factor comes from the S³ addition theorem:
        Σ_{m,n} Y_{lmn}(x) Y*_{lmn}(y) = [(l+1)/(2π²)] C_l^1(cos χ)
    """
    total = 0.0
    cos_chi = cos(chi)
    for l in range(1, l_max + 1):
        Cl = gegenbauer_C1(l, cos_chi)
        total += (l + 1) * Cl / (l * (l + 2))
    return -total / (2 * pi**2)


# =====================================================================
# Step 4: Quaternion geometry on S³
# =====================================================================

def s3_geodesic_distance(q1, q2):
    """Geodesic distance on S³ between two unit quaternions.

    χ = arccos(q₁ · q₂) where the dot product is the R⁴ inner product.
    Range: χ ∈ [0, π].

    Note: on S³ (not RP³), q and -q are DIFFERENT points at distance π.
    """
    dot = sum(a * b for a, b in zip(q1, q2))
    dot = max(-1.0, min(1.0, dot))
    return acos(dot)


def build_600cell_vertices():
    """Construct the 120 vertices of the 600-cell as unit quaternions.

    These are the 120 elements of I* (binary icosahedral group) in S³.
    The 600-cell has 120 vertices, 720 edges, 1200 triangular faces,
    and 600 tetrahedral cells.

    I* = {±1, ±i, ±j, ±k} ∪ {(±1±i±j±k)/2} ∪
         {even permutations of (0, ±1, ±φ, ±1/φ)/2}
    where φ = (1+√5)/2 is the golden ratio.
    """
    phi = (1 + sqrt(5)) / 2
    elements = []

    # 8 quaternion units
    for s in [1, -1]:
        elements.append((s, 0, 0, 0))
        elements.append((0, s, 0, 0))
        elements.append((0, 0, s, 0))
        elements.append((0, 0, 0, s))

    # 16 half-integer quaternions
    for s0 in [1, -1]:
        for s1 in [1, -1]:
            for s2 in [1, -1]:
                for s3 in [1, -1]:
                    elements.append((s0/2, s1/2, s2/2, s3/2))

    # 96 golden quaternions: even permutations of (0, ±1, ±φ, ±1/φ)/2
    even_perms = [
        (0,1,2,3), (0,2,3,1), (0,3,1,2),
        (1,0,3,2), (1,2,0,3), (1,3,2,0),
        (2,0,1,3), (2,1,3,0), (2,3,0,1),
        (3,0,2,1), (3,1,0,2), (3,2,1,0),
    ]
    base = [0, 1.0, phi, 1/phi]
    for perm in even_perms:
        coords = [base[perm[i]] for i in range(4)]
        nonzero_idx = [i for i in range(4) if abs(coords[i]) > 1e-10]
        for mask in range(1 << len(nonzero_idx)):
            signed = list(coords)
            for bit, idx in enumerate(nonzero_idx):
                if mask & (1 << bit):
                    signed[idx] = -signed[idx]
            q = tuple(s / 2 for s in signed)
            norm = sqrt(sum(c**2 for c in q))
            if abs(norm - 1.0) < 1e-8:
                if not any(all(abs(q[i] - e[i]) < 1e-8 for i in range(4))
                           for e in elements):
                    elements.append(q)

    assert len(elements) == 120, f"Expected 120, got {len(elements)}"
    return elements


# =====================================================================
# Step 5: Vortex Hamiltonian on S³
# =====================================================================

def s3_vortex_energy(quats):
    r"""Vortex energy on S³: H = -Σ_{j<k} G(χ_{jk}).

    Equal circulations κ=1. The Green's function G(χ) = -(1/4π²)(π-χ)/sin(χ).
    So H = (1/4π²) Σ_{j<k} (π-χ_{jk})/sin(χ_{jk}).
    """
    N = len(quats)
    H = 0.0
    for j in range(N):
        for k in range(j + 1, N):
            chi = s3_geodesic_distance(quats[j], quats[k])
            H -= s3_green_function(chi)
    return H


def s3_interaction_matrix(quats):
    """Zero-sum interaction matrix on S³.

    K_{jk} = -G'(χ_{jk}) / sin²(χ_{jk}) ... actually for the Havelock
    decomposition we need the ANGULAR Hessian of G at the equilibrium.

    For the S³ analog, define:
        w(χ) = -G(χ) = (1/4π²)(π-χ)/sin(χ)  (the interaction weight)
        K_{jk} = w(χ_{jk}) for j ≠ k
        K_{jj} = -Σ_{k≠j} K_{jk}
    """
    N = len(quats)
    K = np.zeros((N, N))
    for j in range(N):
        for k in range(N):
            if j != k:
                chi = s3_geodesic_distance(quats[j], quats[k])
                K[j, k] = -s3_green_function(chi)
        K[j, j] = -sum(K[j, l] for l in range(N) if l != j)
    return K


# =====================================================================
# Step 6: S³ Havelock decomposition
# =====================================================================

def s3_per_vertex_sum(quats):
    """C₁ = Σ_{k≠0} w(χ_{0k}) on S³."""
    total = 0.0
    for k in range(1, len(quats)):
        chi = s3_geodesic_distance(quats[0], quats[k])
        total += -s3_green_function(chi)
    return total


def s3_havelock_casimir(quats, l):
    r"""S³ Havelock Casimir T_l for the l-th harmonic.

    T_l = Σ_{k≠0} w(χ_{0k}) [1 - C_l^1(cos χ_{0k})/(l+1)]

    The normalization C_l^1(1) = l+1 ensures the zonal spherical function
    C_l^1(cos χ)/(l+1) equals 1 at χ=0.

    This is the S³ analog of the S² Platonic Havelock formula:
        T_j = Σ K(d)[1 - P_j(cos d)]
    with Gegenbauer C_l^1/(l+1) replacing Legendre P_j.
    """
    N = len(quats)
    T = 0.0
    for k in range(1, N):
        chi = s3_geodesic_distance(quats[0], quats[k])
        w = -s3_green_function(chi)
        cos_chi = cos(chi)
        Cl = gegenbauer_C1(l, cos_chi)
        T += w * (1.0 - Cl / (l + 1))
    return T


def s3_bridge_formula(quats, l):
    r"""S³ bridge formula: λ_l via Gegenbauer projection onto the 600-cell orbit.

    λ_l = Σ_{k≠0} w(χ_{0k}) × C_l^1(cos χ_{0k}) / (l+1)

    where w = -G is the interaction weight and C_l^1/(l+1) is the
    normalized zonal spherical function on S³.

    This is the S³ analog of the GAP D bridge identity on S²:
        λ_j^{S²} = 5K₁P_j(c) + 5K₂P_j(-c) + ¼(-1)^j

    On S³, there are 8 distance classes (= I* conjugacy classes),
    so the formula has 8 terms instead of 3.

    The 600-cell (I* regular representation) gives T values for ALL 9
    I* irreps, including the 4 half-integer ones invisible on S².
    """
    N = len(quats)
    lam = 0.0
    for k in range(1, N):
        chi = s3_geodesic_distance(quats[0], quats[k])
        w = -s3_green_function(chi)
        Cl = gegenbauer_C1(l, cos(chi))
        lam += w * Cl / (l + 1)
    return lam


def build_24cell_vertices():
    """Construct the 24 vertices of the 24-cell as unit quaternions.

    The 24-cell has 24 vertices = the 24 units of the Hurwitz quaternions:
    {±1, ±i, ±j, ±k, (±1±i±j±k)/2}

    This is a regular polytope on S³ with binary tetrahedral symmetry 2T*.
    It is a SUBSET of the 600-cell (I* contains 2T* as a subgroup).
    """
    elements = []
    for s in [1, -1]:
        elements.append((s, 0, 0, 0))
        elements.append((0, s, 0, 0))
        elements.append((0, 0, s, 0))
        elements.append((0, 0, 0, s))
    for s0 in [1, -1]:
        for s1 in [1, -1]:
            for s2 in [1, -1]:
                for s3 in [1, -1]:
                    elements.append((s0/2, s1/2, s2/2, s3/2))
    assert len(elements) == 24
    return elements


def s3_stability_analysis(quats):
    """Stability analysis of a vortex configuration on S³.

    Returns dict with eigenvalue counts, energy, and I* irrep structure.

    For vortex equilibria on S³, the interaction matrix K has:
    - Positive eigenvalues: stable modes (energy increases under perturbation)
    - Zero eigenvalues: symmetry modes (SO(4) rotations)
    - Negative eigenvalues: unstable modes

    THEOREM (Schur conservation):
        For any G-equivariant perturbation (G = symmetry group),
        the K-matrix block structure (irrep degeneracies) is
        TOPOLOGICALLY PROTECTED by Schur's lemma. Eigenvalues
        vary continuously within each block, but the block sizes
        (= d² for the regular rep, d for the permutation rep)
        cannot change without breaking symmetry.

        This is the S³ analog of the Lax conservation on R²/H²:
        the Lax spectrum prevents polygon↔BTZ transitions;
        the Schur block structure prevents 600-cell↔lower symmetry transitions.
    """
    N = len(quats)
    K = s3_interaction_matrix(quats)
    evals = np.sort(np.linalg.eigvalsh(K))

    n_neg = int(sum(1 for e in evals if e < -0.001))
    n_zero = int(sum(1 for e in evals if abs(e) < 0.001))
    n_pos = int(sum(1 for e in evals if e > 0.001))

    return {
        'N': N,
        'energy': s3_vortex_energy(quats),
        'C1': s3_per_vertex_sum(quats),
        'n_negative': n_neg,
        'n_zero': n_zero,
        'n_positive': n_pos,
        'eigenvalues': evals,
        'stable': n_neg == 0,
        'morse_index': n_neg,
    }


def verify_s3_green_function(l_max=100):
    """Verify closed form matches eigenfunction expansion."""
    chi_values = [0.3, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    max_err = 0.0
    for chi in chi_values:
        G_exact = s3_green_function(chi)
        G_approx = s3_green_eigenfunction_expansion(chi, l_max)
        err = abs(G_exact - G_approx) / abs(G_exact)
        max_err = max(max_err, err)
    return max_err
