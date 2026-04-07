r"""
EXPLORATION: Bring surface (genus 4) tau computation.

The Bring surface is the unique genus-4 surface with maximal
automorphism group |Aut| = 120 = |S_5|. It is the Fermat quintic
curve x^5 + y^5 + z^5 = 0 in CP^2.

The ADE prediction: if the pattern Bolza (|Aut|=48, O*→E_7) extends,
then the Bring surface (|Aut|=120, I*→E_8) should give tau related
to E_8 data (h=30, exponents 1,7,11,13,17,19,23,29).

The Bring surface is uniformized by a Fuchsian group Gamma with
fundamental domain a regular 16-gon in H^2 (genus 4 → 2g = 8 generators
→ 4g-gon = 16-gon). The interior angles are π/4 each (so 8 pentagons
meet at each vertex: 8 × π/4 = 2π).

The systole (shortest closed geodesic) has length:
  ℓ_sys = 2 arccosh(φ) where φ = (1+√5)/2 (golden ratio)
  ℓ_sys ≈ 1.9248

APPROACH: Build the Fuchsian group from the 16-gon side pairings,
enumerate group elements by BFS, build the convolution matrix,
and compute tau(P_-).
"""

import numpy as np
from math import pi, sqrt, sin, cos, cosh, acosh, sinh, atanh, tanh, log


# =====================================================================
# Hyperbolic geometry in the Poincaré disk
# =====================================================================

def disk_distance(z1, z2):
    """Hyperbolic distance between two points in the Poincaré disk."""
    num = abs(z1 - z2)
    den = abs(1 - z1 * np.conj(z2))
    if den < 1e-15:
        return 0.0
    ratio = min(num / den, 0.99999)
    return 2 * atanh(ratio)


def mobius(z, a, b, c, d):
    """Möbius transformation (az+b)/(cz+d) in the Poincaré disk."""
    num = a * z + b
    den = c * z + d
    if abs(den) < 1e-15:
        return complex(1e10, 0)
    return num / den


# =====================================================================
# Regular 16-gon fundamental domain
# =====================================================================

def regular_polygon_vertices(n, R):
    """Vertices of a regular n-gon of hyperbolic radius R centered at origin."""
    return [R * np.exp(2j * pi * k / n) for k in range(n)]


def genus4_polygon_radius():
    """Hyperbolic radius of the regular 16-gon with angle π/8.

    For a regular n-gon with interior angle α:
    cosh(R) = cos(π/n) / sin(α/2)

    For genus-4 surface: n=16, all 16 vertices identified,
    angle sum = 2π, so α = 2π/16 = π/8.
    cosh(R) = cos(π/16) / sin(π/16) = cot(π/16) ≈ 5.027.
    Area = (16-2)π - 2π = 12π = 4π(g-1) ✓
    """
    n = 16
    alpha = pi / 8  # interior angle: 16 angles sum to 2π
    cosh_R = cos(pi / n) / sin(alpha / 2)
    R_hyp = acosh(cosh_R)
    R_disk = tanh(R_hyp / 2)
    return R_disk, R_hyp


def genus4_side_pairing_generators():
    """Build the 8 side-pairing Möbius transformations for the genus-4 surface.

    The regular 16-gon has sides labeled a₁,b₁,a₁⁻¹,b₁⁻¹,...,a₄,b₄,a₄⁻¹,b₄⁻¹.
    Side k is paired with side k+8 (opposite side).

    Each side-pairing is a hyperbolic translation that maps one side
    to its partner. For a regular polygon centered at the origin,
    the side-pairing maps the midpoint of side k to the midpoint of
    side k+8, and is a translation along the perpendicular bisector.
    """
    R_disk, R_hyp = genus4_polygon_radius()
    n = 16

    generators = []
    inverses = []

    # Vertices of the 16-gon
    verts = regular_polygon_vertices(n, R_disk)

    for k in range(8):  # 8 generators (4 a's and 4 b's)
        # Side k goes from vertex k to vertex k+1
        # Its partner is side k+8 (from vertex k+8 to vertex k+9)
        # The pairing maps midpoint of side k to midpoint of side k+8

        # Midpoints (in the Poincaré disk)
        mid_k = (verts[k] + verts[(k + 1) % n]) / 2
        mid_partner = (verts[(k + 8) % n] + verts[(k + 9) % n]) / 2

        # The side-pairing is a hyperbolic isometry mapping mid_k to mid_partner.
        # For a centered regular polygon, this is a rotation by π (= 8 steps of 2π/16)
        # composed with a translation.

        # Simpler approach: the side-pairing for a regular 2g-gon is a
        # rotation by (2k+1)π/g followed by hyperbolic scaling.
        # For g=4 (16-gon): rotation by (2k+1)π/4.

        # Actually, the standard genus-g surface from a 4g-gon uses:
        # Side pairings that map side j to side j+2g (with rotation).
        # The Möbius transformation: T_k(z) = e^{iθ_k} × (z - a_k)/(1 - ā_k z)
        # where a_k is the translation vector and θ_k is the rotation.

        # For a symmetric polygon: the translation distance is
        # d = 2R_hyp sin(π/n) = 2R_hyp sin(π/16)
        # and the rotation angle is π + 2πk/n = π + πk/8

        # Build the Möbius transformation that maps:
        #   center of side k → center of side k+8
        #   preserves the hyperbolic metric

        # The center of side k in the disk:
        angle_k = 2 * pi * (k + 0.5) / n
        angle_partner = 2 * pi * ((k + 8) + 0.5) / n

        # The translation: from center along angle_k to center along angle_partner
        # This is a rotation by angle_partner - angle_k = 8 × 2π/16 = π
        # plus a hyperbolic boost.

        # For a regular polygon, the side-pairing generator is:
        # T_k(z) = e^{i(π + 2πk/8)} × z  (rotation by π plus k/8 turns)
        # This is approximate — let me use a more careful construction.

        # Use the fact that for a regular 4g-gon, the generators are
        # rotations by angle π(2k+1)/(2g) composed with the translation
        # that maps the origin to the midpoint of side k+g.

        # For practical purposes, let me use the rotation-only approximation:
        theta_rot = pi + 2 * pi * k / 8  # rotation by π + k×45°
        # This maps side k to side k+8 by rotation about the center.

        # As a Möbius transformation on the disk:
        # T(z) = e^{iθ} z (pure rotation, no translation)
        # This preserves the center but doesn't translate.
        # For the actual side pairing, we need a TRANSLATION too.

        # Let me use a different approach: build generators from the
        # known geodesic structure.

        # The translation distance for side-pairing:
        # For a regular 4g-gon with angle π/(2g):
        # translation length = 2 arccosh(cosh(R) sin(π/(4g)))
        # For g=4: 2 arccosh(cosh(R) sin(π/16))

        # Side length: cosh(s/2) = cos(α/2)/sin(π/n) = cot(π/16)
        alpha = pi / 8
        cosh_s2 = cos(alpha / 2) / sin(pi / n)
        trans_length = 2 * acosh(cosh_s2)

        # Direction: along the perpendicular bisector of side k
        # which points from the midpoint of side k toward the center
        direction = angle_k + pi  # inward from midpoint of side k

        # Möbius translation by distance d along direction θ:
        # T(z) = (z cosh(d/2) + e^{iθ} sinh(d/2)) /
        #        (z̄ e^{-iθ} sinh(d/2) + cosh(d/2))
        # Wait, that's not right for general direction.

        # A hyperbolic translation by distance d along the real axis:
        # T(z) = (z + tanh(d/2)) / (1 + z tanh(d/2))
        # Rotated to direction θ:
        # T(z) = e^{iθ} × (e^{-iθ}z + tanh(d/2)) / (1 + e^{-iθ}z × tanh(d/2))

        t = tanh(trans_length / 2)
        phase = np.exp(1j * direction)
        phase_inv = np.exp(-1j * direction)

        # Store as (a, b, c, d) for Möbius (az+b)/(cz+d)
        a = phase
        b = t
        c = t * phase_inv * phase  # = t
        d_coeff = phase_inv

        # Actually let me use the standard form:
        # Translation by distance d along angle θ:
        # [cosh(d/2)  e^{iθ}sinh(d/2)]
        # [e^{-iθ}sinh(d/2)  cosh(d/2)]

        ch = cosh(trans_length / 2)
        sh = sinh(trans_length / 2)
        gen = np.array([
            [ch, np.exp(1j * direction) * sh],
            [np.exp(-1j * direction) * sh, ch],
        ])

        # Inverse: negate the translation direction
        gen_inv = np.array([
            [ch, np.exp(1j * (direction + pi)) * sh],
            [np.exp(-1j * (direction + pi)) * sh, ch],
        ])

        generators.append(gen)
        inverses.append(gen_inv)

    return generators, inverses


def apply_sl2(M, z):
    """Apply SL(2,C) matrix M to point z in the Poincaré disk."""
    num = M[0, 0] * z + M[0, 1]
    den = M[1, 0] * z + M[1, 1]
    if abs(den) < 1e-15:
        return complex(1e10, 0)
    return num / den


# =====================================================================
# Group enumeration (BFS)
# =====================================================================

def enumerate_group_bfs(generators, inverses, max_length=3, dedup_tol=1e-4):
    """Enumerate Fuchsian group elements by BFS word length."""
    n_gen = len(generators)
    all_gens = generators + inverses

    # Start with identity
    identity = np.eye(2, dtype=complex)
    elements = [identity]
    z_images = [complex(0, 0)]  # image of origin

    seen = {(0.0, 0.0)}  # dedup by image of origin

    current_level = [identity]
    counts = [1]  # level 0 = identity

    for L in range(1, max_length + 1):
        next_level = []
        for M in current_level:
            for g in all_gens:
                Mg = M @ g
                # Image of origin
                z = apply_sl2(Mg, 0.0)
                if abs(z) > 0.999:
                    continue  # too close to boundary
                key = (round(z.real / dedup_tol) * dedup_tol,
                       round(z.imag / dedup_tol) * dedup_tol)
                if key not in seen:
                    seen.add(key)
                    elements.append(Mg)
                    z_images.append(z)
                    next_level.append(Mg)

        counts.append(len(next_level))
        current_level = next_level

    return elements, z_images, counts


# =====================================================================
# Convolution matrix and tau computation
# =====================================================================

def green_function_h2(d):
    """H² Green's function G(d) = -ln(2 sinh(d/2))."""
    if d < 1e-12:
        return 0.0
    return -log(2 * sinh(d / 2))


def build_convolution_matrix(z_images):
    """Build the convolution matrix H_{ij} = G(d(z_i, z_j))."""
    n = len(z_images)
    H = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                d = disk_distance(z_images[i], z_images[j])
                H[i, j] = green_function_h2(d)
    return H


def compute_tau_bring(max_word_length=2, verbose=True):
    """Compute tau(P_-) on the Bring surface."""
    if verbose:
        print(f"Building Bring surface Fuchsian group (L={max_word_length})...")

    gens, invs = genus4_side_pairing_generators()

    if verbose:
        print(f"  {len(gens)} generators")
        R_disk, R_hyp = genus4_polygon_radius()
        print(f"  16-gon radius: R_disk={R_disk:.4f}, R_hyp={R_hyp:.4f}")

    elements, z_images, counts = enumerate_group_bfs(
        gens, invs, max_word_length, dedup_tol=0.0001
    )
    n = len(elements)

    if verbose:
        print(f"  Elements: {n} (by level: {counts})")
        if n > 1:
            dists = [disk_distance(z_images[0], z_images[k])
                     for k in range(1, min(n, 50))]
            print(f"  Distance range: [{min(dists):.4f}, {max(dists):.4f}]")

    if n < 3:
        return {'n_elements': n, 'tau_counting': 0, 'message': 'Too few elements'}

    if verbose:
        print(f"Building {n}×{n} convolution matrix...")

    H = build_convolution_matrix(z_images)
    evals = np.sort(np.linalg.eigvalsh(H))

    n_neg = sum(1 for e in evals if e < -1e-12)
    tau = n_neg / n if n > 0 else 0

    if verbose:
        print(f"  Spectral radius: {max(abs(evals)):.6f}")
        print(f"  Negative eigenvalues: {n_neg}/{n}")
        print(f"  tau(P_-) [counting]: {tau:.6f}")

    return {
        'n_elements': n,
        'eigenvalues': evals,
        'tau_counting': tau,
        'n_negative': n_neg,
        'n_by_level': counts,
    }


# =====================================================================
# Bring surface data
# =====================================================================

def bring_surface_data():
    """Known data about the Bring surface."""
    phi = (1 + sqrt(5)) / 2
    return {
        'genus': 4,
        'area': 4 * pi * 3,  # 4π(g-1) = 12π
        'aut_order': 120,
        'aut_group': 'S_5',
        'binary_group': 'I* (order 120)',
        'mckay': 'E_8',
        'coxeter_number': 30,
        'exponents': [1, 7, 11, 13, 17, 19, 23, 29],
        'systole': 2 * acosh(phi),  # ≈ 1.925
        'e8_prediction': 91 / 120,  # tau = (120-29)/120
    }


if __name__ == '__main__':
    print("=" * 65)
    print("BRING SURFACE (genus 4, Aut = S_5, McKay → E_8)")
    print("=" * 65)
    print()

    data = bring_surface_data()
    print(f"Genus: {data['genus']}")
    print(f"|Aut| = {data['aut_order']} ({data['aut_group']})")
    print(f"McKay: {data['mckay']}")
    print(f"Coxeter number h = {data['coxeter_number']}")
    print(f"Systole: {data['systole']:.4f}")
    print(f"E_8 prediction for tau: {data['e8_prediction']:.6f} = 91/120")
    print()

    # Compute tau
    for L in [1, 2, 3]:
        result = compute_tau_bring(max_word_length=L)
        print(f"\n  L={L}: n={result['n_elements']}, "
              f"tau={result['tau_counting']:.6f}")
