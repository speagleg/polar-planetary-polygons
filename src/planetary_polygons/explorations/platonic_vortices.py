r"""
EXPLORATION: Vortex configurations with Platonic solid symmetry on S².

The current framework uses regular N-gons (Z_N symmetry, 2D).
This exploration extends to the 3D Platonic solids on S²:

  Tetrahedron:   4 vertices,  A_4 symmetry (order 12)
  Octahedron:    6 vertices,  S_4 symmetry (order 24)
  Cube:          8 vertices,  S_4 symmetry (order 24)
  Icosahedron:  12 vertices,  A_5 symmetry (order 60)
  Dodecahedron: 20 vertices,  A_5 symmetry (order 60)

The McKay correspondence for binary Platonic groups Γ* ⊂ SU(2):
  Binary tetrahedral  T* (order 24)  → E_6
  Binary octahedral   O* (order 48)  → E_7
  Binary icosahedral  I* (order 120) → E_8

QUESTIONS:
  Q1: What are the Havelock-like eigenvalues for Platonic vortex configs on S²?
  Q2: Is there a stability threshold analogous to N=7?
  Q3: Does the McKay correspondence give gauge groups from the eigenvalue spectrum?
  Q4: Does the CS-Havelock identity extend to non-abelian groups?
  Q5: What is the "central charge" c for each Platonic configuration?
"""

import numpy as np
from math import pi, sqrt, acos, sin, cos, log
from fractions import Fraction
from itertools import combinations


# =====================================================================
# Platonic solid vertex coordinates on the unit sphere
# =====================================================================

def tetrahedron_vertices():
    """4 vertices of a regular tetrahedron inscribed in the unit sphere.

    Orientation: one vertex at the north pole.
    """
    # Vertex at north pole, three others equally spaced below
    theta_top = 0.0
    theta_bottom = acos(-1/3)  # ≈ 109.47°
    verts = [
        (0, 0, 1),  # north pole
    ]
    for k in range(3):
        phi = 2 * pi * k / 3
        verts.append((
            sin(theta_bottom) * cos(phi),
            sin(theta_bottom) * sin(phi),
            cos(theta_bottom),
        ))
    return np.array(verts)


def octahedron_vertices():
    """6 vertices of a regular octahedron inscribed in the unit sphere."""
    return np.array([
        (1, 0, 0), (-1, 0, 0),
        (0, 1, 0), (0, -1, 0),
        (0, 0, 1), (0, 0, -1),
    ], dtype=float)


def cube_vertices():
    """8 vertices of a cube inscribed in the unit sphere."""
    s = 1 / sqrt(3)
    verts = []
    for sx in [-1, 1]:
        for sy in [-1, 1]:
            for sz in [-1, 1]:
                verts.append((sx * s, sy * s, sz * s))
    return np.array(verts)


def icosahedron_vertices():
    """12 vertices of a regular icosahedron inscribed in the unit sphere."""
    phi = (1 + sqrt(5)) / 2  # golden ratio
    r = sqrt(1 + phi**2)
    verts = []
    for s1 in [-1, 1]:
        for s2 in [-1, 1]:
            verts.append((0, s1 / r, s2 * phi / r))
            verts.append((s1 / r, s2 * phi / r, 0))
            verts.append((s2 * phi / r, 0, s1 / r))
    return np.array(verts)


def dodecahedron_vertices():
    """20 vertices of a regular dodecahedron inscribed in the unit sphere."""
    phi = (1 + sqrt(5)) / 2
    r1 = sqrt(3)
    r2 = sqrt(3)
    verts = []
    # Cube vertices: (±1, ±1, ±1)/√3
    s = 1 / r1
    for sx in [-1, 1]:
        for sy in [-1, 1]:
            for sz in [-1, 1]:
                verts.append((sx * s, sy * s, sz * s))
    # Rectangle vertices: (0, ±φ, ±1/φ)/√3 and cyclic permutations
    for s1 in [-1, 1]:
        for s2 in [-1, 1]:
            verts.append((0, s1 * phi / r2, s2 / (phi * r2)))
            verts.append((s1 / (phi * r2), 0, s2 * phi / r2))
            verts.append((s1 * phi / r2, s2 / (phi * r2), 0))
    verts = np.array(verts)
    # Normalize to unit sphere
    norms = np.linalg.norm(verts, axis=1, keepdims=True)
    return verts / norms


PLATONIC_SOLIDS = {
    'tetrahedron': (tetrahedron_vertices, 4, 'A_4', 12, 'T*', 24, 'E_6'),
    'octahedron': (octahedron_vertices, 6, 'S_4', 24, 'O*', 48, 'E_7'),
    'cube': (cube_vertices, 8, 'S_4', 24, 'O*', 48, 'E_7'),
    'icosahedron': (icosahedron_vertices, 12, 'A_5', 60, 'I*', 120, 'E_8'),
    'dodecahedron': (dodecahedron_vertices, 20, 'A_5', 60, 'I*', 120, 'E_8'),
}


# =====================================================================
# Spherical distance and energy
# =====================================================================

def spherical_distance(p1, p2):
    """Great-circle distance between two points on S²."""
    dot = np.clip(np.dot(p1, p2), -1.0, 1.0)
    return acos(dot)


def chord_distance(p1, p2):
    """Euclidean chord distance between two points on S²."""
    return np.linalg.norm(p1 - p2)


def thomson_energy_s2(vertices):
    """Thomson energy H = -Σ_{j<k} ln|p_j - p_k| on S².

    Uses the chord distance (stereographic Green's function).
    """
    N = len(vertices)
    H = 0.0
    for j in range(N):
        for k in range(j + 1, N):
            d = chord_distance(vertices[j], vertices[k])
            if d > 1e-15:
                H -= log(d)
    return H


def log_sin_energy_s2(vertices):
    """Spherical energy H = -Σ_{j<k} ln sin(d_{jk}/2) on S².

    This is the natural S² Green's function (eq. H_sph in Appendix).
    """
    N = len(vertices)
    H = 0.0
    for j in range(N):
        for k in range(j + 1, N):
            d = spherical_distance(vertices[j], vertices[k])
            s = sin(d / 2)
            if s > 1e-15:
                H -= log(s)
    return H


# =====================================================================
# Hessian computation on S² (the key new calculation)
# =====================================================================

def tangent_basis_at_point(p):
    """Orthonormal basis for the tangent plane at p ∈ S²."""
    p = np.array(p, dtype=float)
    # Find a vector not parallel to p
    if abs(p[0]) < 0.9:
        v = np.array([1, 0, 0], dtype=float)
    else:
        v = np.array([0, 1, 0], dtype=float)
    # Gram-Schmidt
    e1 = v - np.dot(v, p) * p
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(p, e1)
    e2 /= np.linalg.norm(e2)
    return e1, e2


def hessian_log_sin_s2(vertices):
    """Full Hessian of H = -Σ ln sin(d_{jk}/2) on S².

    Returns a 2N × 2N matrix (two tangent directions per vertex).

    The second derivative of -ln sin(d/2) with respect to
    tangential displacements uses the S² csc² kernel
    (analogous to the flat-plane csc² circulant).
    """
    N = len(vertices)
    # Build tangent bases for each vertex
    bases = [tangent_basis_at_point(vertices[k]) for k in range(N)]

    H = np.zeros((2 * N, 2 * N))

    for j in range(N):
        e1j, e2j = bases[j]
        for k in range(N):
            if j == k:
                continue
            e1k, e2k = bases[k]

            pj = vertices[j]
            pk = vertices[k]
            d = spherical_distance(pj, pk)
            if d < 1e-12:
                continue

            # The S² Green's function second derivatives
            # G = -ln sin(d/2)
            # Using chord distance r = 2 sin(d/2):
            # G = -ln(r/2) = -ln r + ln 2
            # The Hessian of -ln r in ambient R³ restricted to S²
            # involves the projected Hessian of the chord distance.

            r = chord_distance(pj, pk)
            if r < 1e-12:
                continue

            # Direction vector (on the sphere, via tangent projection)
            diff = pk - pj  # ambient
            # Project onto tangent planes
            diff_j = np.array([np.dot(diff, e1j), np.dot(diff, e2j)])
            diff_k = np.array([np.dot(diff, e1k), np.dot(diff, e2k)])

            # Second derivative of -ln r:
            # ∂²(-ln r)/∂x_j^a ∂x_k^b = (δ_{ab} r² - 2 Δx_a Δx_b) / r⁴
            # with appropriate tangent-plane projections
            for a in range(2):
                for b in range(2):
                    # Tangent vectors
                    eja = [e1j, e2j][a]
                    ekb = [e1k, e2k][b]

                    # ∂²(-ln r)/∂(δj_a)(δk_b)
                    # = [eja · ekb / r² - 2(eja · diff)(ekb · diff) / r⁴]
                    # But with sign: moving j and k in opposite directions
                    # for the off-diagonal block

                    ej_dot_ek = np.dot(eja, ekb)
                    ej_dot_diff = np.dot(eja, diff)
                    ek_dot_diff = np.dot(ekb, diff)

                    val = -(ej_dot_ek / r**2 - 2 * ej_dot_diff * ek_dot_diff / r**4)

                    H[2 * j + a, 2 * k + b] += val
                    # Diagonal accumulation
                    H[2 * j + a, 2 * j + a] -= val

    return H


# =====================================================================
# Eigenvalue analysis
# =====================================================================

def hessian_eigenvalues(vertices):
    """Compute eigenvalues of the constrained Hessian on S².

    Removes the 3 rigid-rotation zero modes (SO(3) symmetry).
    Returns sorted eigenvalues.
    """
    H = hessian_log_sin_s2(vertices)
    evals = np.linalg.eigvalsh(H)
    # Sort and remove the 3 smallest (should be ~0, from SO(3))
    evals = np.sort(evals)
    # Count near-zero eigenvalues
    n_zero = np.sum(np.abs(evals) < 1e-6)
    return evals, n_zero


def stability_analysis(name, vertices):
    """Full stability analysis for a Platonic vortex configuration.

    Returns:
        dict with eigenvalues, stability status, and McKay data
    """
    N = len(vertices)
    evals, n_zero = hessian_eigenvalues(vertices)

    # Energy
    E_chord = thomson_energy_s2(vertices)
    E_sphere = log_sin_energy_s2(vertices)

    # Stability: all non-zero eigenvalues positive?
    nonzero_evals = evals[np.abs(evals) > 1e-6]
    n_positive = np.sum(nonzero_evals > 1e-6)
    n_negative = np.sum(nonzero_evals < -1e-6)
    is_stable = n_negative == 0

    # McKay data
    _, n_verts, rot_group, rot_order, binary_group, binary_order, mckay_type = \
        PLATONIC_SOLIDS.get(name, (None, N, '?', 0, '?', 0, '?'))

    return {
        'name': name,
        'N': N,
        'rotation_group': rot_group,
        'rotation_order': rot_order,
        'binary_group': binary_group,
        'binary_order': binary_order,
        'mckay_type': mckay_type,
        'energy_chord': E_chord,
        'energy_sphere': E_sphere,
        'eigenvalues': evals,
        'n_zero_modes': n_zero,
        'n_positive': n_positive,
        'n_negative': n_negative,
        'is_stable': is_stable,
        'morse_index': n_negative,
    }


# =====================================================================
# McKay correspondence for binary Platonic groups
# =====================================================================

def mckay_data():
    """The McKay correspondence for binary Platonic groups Γ* ⊂ SU(2).

    Each finite subgroup Γ ⊂ SO(3) has a binary lift Γ* ⊂ SU(2).
    The McKay graph of Γ* is an extended ADE Dynkin diagram.
    The corresponding Lie algebra determines the "gauge group" in the
    polygon framework.
    """
    return {
        'cyclic': {
            'description': 'Z_n → A_{n-1} → SU(n)',
            'examples': {
                3: {'group': 'SU(3)', 'dynkin': 'A_2', 'rank': 2, 'dim': 8},
                7: {'group': 'SU(7)', 'dynkin': 'A_6', 'rank': 6, 'dim': 48},
            },
        },
        'binary_dihedral': {
            'description': 'D*_n (order 4n) → D_{n+2} → SO(2n+4)',
            'examples': {
                2: {'group': 'SO(8)', 'dynkin': 'D_4', 'rank': 4, 'dim': 28},
                3: {'group': 'SO(10)', 'dynkin': 'D_5', 'rank': 5, 'dim': 45},
            },
        },
        'binary_tetrahedral': {
            'description': 'T* (order 24) → E_6',
            'group': 'E_6', 'dynkin': 'E_6',
            'rank': 6, 'dim': 78, 'dual_coxeter': 12,
            'n_vertices': 4,  # tetrahedron
            'n_irreps': 7,  # T* has 7 irreducible representations
        },
        'binary_octahedral': {
            'description': 'O* (order 48) → E_7',
            'group': 'E_7', 'dynkin': 'E_7',
            'rank': 7, 'dim': 133, 'dual_coxeter': 18,
            'n_vertices': 6,  # octahedron (or 8 for cube)
            'n_irreps': 8,  # O* has 8 irreducible representations
        },
        'binary_icosahedral': {
            'description': 'I* (order 120) → E_8',
            'group': 'E_8', 'dynkin': 'E_8',
            'rank': 8, 'dim': 248, 'dual_coxeter': 30,
            'n_vertices': 12,  # icosahedron (or 20 for dodecahedron)
            'n_irreps': 9,  # I* has 9 irreducible representations
        },
    }


def wzw_central_charge(group, rank, k=1):
    """WZW central charge c = k·dim(G)/(k + h∨)."""
    data = {
        'E_6': (78, 12), 'E_7': (133, 18), 'E_8': (248, 30),
    }
    if group in data:
        dim_G, h_dual = data[group]
    elif group.startswith('SU'):
        n = rank + 1
        dim_G = n * n - 1
        h_dual = n
    elif group.startswith('SO'):
        n = 2 * rank  # approximate
        dim_G = n * (n - 1) // 2
        h_dual = n - 2
    else:
        return None
    return k * dim_G / (k + h_dual)


# =====================================================================
# Comparison table
# =====================================================================

def full_exploration():
    """Run stability analysis for all Platonic solids and compare."""
    results = {}
    for name, (vertex_fn, n_verts, rot, rot_ord, binary, bin_ord, mckay) in PLATONIC_SOLIDS.items():
        verts = vertex_fn()
        result = stability_analysis(name, verts)
        results[name] = result

    return results


if __name__ == '__main__':
    print("=" * 75)
    print("PLATONIC SOLID VORTEX CONFIGURATIONS ON S²")
    print("=" * 75)
    print()

    # McKay table
    print("McKay correspondence for binary Platonic groups:")
    print(f"{'Group':<25s} {'Order':>6s} {'McKay':>6s} {'Lie':>6s} {'dim':>5s} {'c(k=1)':>8s}")
    print("-" * 65)
    for name, data in [
        ('Z_3 (triangle)', {'dim': 8, 'group': 'SU(3)', 'dynkin': 'A_2', 'rank': 2}),
        ('Z_7 (heptagon)', {'dim': 48, 'group': 'SU(7)', 'dynkin': 'A_6', 'rank': 6}),
        ('T* (tetrahedral)', {'dim': 78, 'group': 'E_6', 'dynkin': 'E_6', 'rank': 6}),
        ('O* (octahedral)', {'dim': 133, 'group': 'E_7', 'dynkin': 'E_7', 'rank': 7}),
        ('I* (icosahedral)', {'dim': 248, 'group': 'E_8', 'dynkin': 'E_8', 'rank': 8}),
    ]:
        c = wzw_central_charge(data['group'], data['rank'])
        c_str = f"{c:.2f}" if c else "?"
        print(f"{name:<25s} {'':>6s} {data['dynkin']:>6s} {data['group']:>6s} "
              f"{data['dim']:5d} {c_str:>8s}")
    print()

    # Stability analysis
    print("Stability analysis on S²:")
    print(f"{'Solid':<14s} {'N':>3s} {'Group':>5s} {'McKay':>5s} "
          f"{'E_sphere':>10s} {'#zero':>5s} {'#neg':>5s} {'Stable':>7s}")
    print("-" * 65)

    results = full_exploration()
    for name in ['tetrahedron', 'octahedron', 'cube', 'icosahedron', 'dodecahedron']:
        r = results[name]
        print(f"{name:<14s} {r['N']:3d} {r['rotation_group']:>5s} "
              f"{r['mckay_type']:>5s} {r['energy_sphere']:10.4f} "
              f"{r['n_zero_modes']:5d} {r['n_negative']:5d} "
              f"{'YES' if r['is_stable'] else 'NO':>7s}")
    print()

    # Detailed eigenvalue spectra
    for name in ['tetrahedron', 'octahedron', 'icosahedron']:
        r = results[name]
        print(f"--- {name} (N={r['N']}, McKay → {r['mckay_type']}) ---")
        evals = r['eigenvalues']
        nonzero = evals[np.abs(evals) > 1e-6]
        print(f"  Eigenvalues (nonzero): {np.sort(nonzero)[:10]}")
        if len(nonzero) > 10:
            print(f"  ... ({len(nonzero)} total)")
        print(f"  Zero modes: {r['n_zero_modes']}")
        print(f"  Negative: {r['n_negative']}, Positive: {r['n_positive']}")
        print()

    # The key question: analogy with N=7
    print("=" * 75)
    print("KEY QUESTION: Is there a 'N=7' transition for Platonic solids?")
    print("=" * 75)
    print()
    print("For the polygon framework:")
    print("  N ≤ 6: stable (index 0)")
    print("  N = 7: marginal (kernel)")
    print("  N ≥ 8: unstable (index N-5)")
    print()
    print("For Platonic solids on S²:")
    for name in ['tetrahedron', 'octahedron', 'cube', 'icosahedron', 'dodecahedron']:
        r = results[name]
        status = "STABLE" if r['is_stable'] else f"UNSTABLE (index {r['morse_index']})"
        print(f"  {name:<14s} (N={r['N']:2d}): {status}")
