r"""
EXPLORATION: Irreducible representation decomposition of the Havelock
Hessian for Platonic solid vortex configurations.

For the regular N-gon (Z_N symmetry), the Havelock decomposition is:
    H = ⊕_m λ_m P_m,  λ_m = C₁ - m(N-m)/2

where P_m is the Z_N Fourier projector onto mode m, and m(N-m)/2 is
the Z_N Casimir.

QUESTION: Does this generalize to non-abelian groups?
For a Platonic solid with symmetry group G, the tangent space
decomposes into irreps ρ of G:
    T = ⊕_ρ n_ρ · V_ρ

and the Hessian should decompose as:
    H = ⊕_ρ λ_ρ · Id_{n_ρ dim(ρ)}

with λ_ρ = C₁ - C₂(ρ) for some "generalized Casimir" C₂(ρ).

If this works, it would mean:
- The Casimir determines stability (same structure as polygon case)
- The McKay correspondence maps irreps to gauge representations
- The stability threshold is C₁ = max_ρ C₂(ρ)

PLATONIC GROUP IRREPS:
    A_4 (tetrahedral):  1, 1', 1'', 3
    S_4 (octahedral):   1, 1', 2, 3, 3'
    A_5 (icosahedral):  1, 3, 3', 4, 5
"""

import numpy as np
from math import pi, sqrt, cos, sin, acos


# =====================================================================
# Character tables of Platonic groups
# =====================================================================

def A4_character_table():
    """Character table of A_4 (tetrahedral rotation group, order 12).

    Conjugacy classes: {e}, {(123),(132),(124),(142),(134),(143),(234),(243)},
    {(12)(34),(13)(24),(14)(23)}, ... Actually:
    A_4 has 4 conjugacy classes:
      C_1: {e} (size 1)
      C_2: {(12)(34),(13)(24),(14)(23)} (size 3)
      C_3: {(123),(134),(142),(243)} (size 4, order 3)
      C_4: {(132),(143),(124),(234)} (size 4, order 3)

    Irreps: 1, 1', 1'', 3
    """
    omega = np.exp(2j * pi / 3)
    # Rows = irreps, Columns = conjugacy classes
    # Class sizes: [1, 3, 4, 4]
    table = np.array([
        [1, 1, 1, 1],           # trivial
        [1, 1, omega, omega**2],     # 1'
        [1, 1, omega**2, omega],     # 1''
        [3, -1, 0, 0],          # standard 3-dim rep
    ], dtype=complex)
    class_sizes = [1, 3, 4, 4]
    irrep_dims = [1, 1, 1, 3]
    irrep_names = ['1', "1'", "1''", '3']
    return table, class_sizes, irrep_dims, irrep_names


def S4_character_table():
    """Character table of S_4 (octahedral rotation group, order 24).

    Conjugacy classes: {e}, {transpositions}, {3-cycles}, {4-cycles}, {double transpositions}
    Sizes: [1, 6, 8, 6, 3]

    Irreps: 1, 1' (sign), 2, 3, 3' (= 3 ⊗ 1')
    """
    table = np.array([
        [1, 1, 1, 1, 1],       # trivial
        [1, -1, 1, -1, 1],     # sign
        [2, 0, -1, 0, 2],      # standard 2-dim
        [3, 1, 0, -1, -1],     # standard 3-dim
        [3, -1, 0, 1, -1],     # 3 ⊗ sign
    ], dtype=complex)
    class_sizes = [1, 6, 8, 6, 3]
    irrep_dims = [1, 1, 2, 3, 3]
    irrep_names = ['1', "1'", '2', '3', "3'"]
    return table, class_sizes, irrep_dims, irrep_names


def A5_character_table():
    """Character table of A_5 (icosahedral rotation group, order 60).

    Conjugacy classes:
      C_1: {e} (size 1)
      C_2: (12)(34)-type (size 15, order 2)
      C_3: (123)-type (size 20, order 3)
      C_4: (12345)-type (size 12, order 5)
      C_5: (13524)-type (size 12, order 5)

    Irreps: 1, 3, 3', 4, 5
    """
    phi = (1 + sqrt(5)) / 2  # golden ratio
    psi = (1 - sqrt(5)) / 2  # conjugate
    table = np.array([
        [1, 1, 1, 1, 1],             # trivial
        [3, -1, 0, phi, psi],        # 3 (icosahedral)
        [3, -1, 0, psi, phi],        # 3' (conjugate)
        [4, 0, 1, -1, -1],           # 4-dim
        [5, 1, -1, 0, 0],            # 5-dim (standard)
    ], dtype=complex)
    class_sizes = [1, 15, 20, 12, 12]
    irrep_dims = [1, 3, 3, 4, 5]
    irrep_names = ['1', '3', "3'", '4', '5']
    return table, class_sizes, irrep_dims, irrep_names


# =====================================================================
# Group Casimirs
# =====================================================================

def group_casimir(table, class_sizes, irrep_dims, group_order):
    """Compute the quadratic Casimir for each irrep.

    The Casimir of irrep ρ is related to the character inner product
    with the "generating" conjugacy class. For finite groups, the
    natural Casimir is:

        C₂(ρ) = (dim(ρ)/|G|) Σ_g |χ_ρ(g)|²  ... no, that's just dim(ρ).

    The actual analogue of the Lie algebra Casimir for a finite group
    is defined through the group algebra. For a finite subgroup of SO(3),
    the Casimir is inherited from the SO(3) embedding:

        C₂(ρ) = j(j+1)

    where j is the SO(3) spin label of ρ. The irreps of G ⊂ SO(3) are
    restrictions of SO(3) representations to G.

    For A_4 ⊂ SO(3): 1 → j=0, 3 → j=1 (but 1', 1'' are non-trivial)
    For S_4 ⊂ SO(3): 1 → j=0, 2 → j=2 restriction, 3 → j=1, 3' → j=1 ⊗ sign
    For A_5 ⊂ SO(3): 1 → j=0, 3 → j=1, 3' → j=1, 4 → j=3 restriction, 5 → j=2
    """
    pass  # Will compute from SO(3) embedding below


def so3_casimirs_platonic():
    """Quadratic Casimirs from the SO(3) embedding of Platonic irreps.

    Each irrep ρ of G ⊂ SO(3) restricts from an SO(3) representation
    D^j. The Casimir is j(j+1).

    A_4 (order 12):
      D^0 → 1 (trivial), C₂ = 0
      D^1 → 3 (standard), C₂ = 2
      The 1' and 1'' are one-dimensional and come from the
      A_4/V_4 = Z_3 quotient. They have C₂ = 0 (trivial SO(3)).
      Actually they're NOT SO(3) reps — they only exist as A_4 reps.

    S_4 (order 24):
      D^0 → 1, C₂ = 0
      D^1 → 3, C₂ = 2
      D^2 → 5 = 2 ⊕ 3', so 2 has C₂ from j=2 (C₂=6) restricted,
        and 3' has C₂ from j=2 restricted.
      Sign rep: not an SO(3) rep.

    A_5 (order 60):
      D^0 → 1, C₂ = 0
      D^1 → 3, C₂ = 2
      D^2 → 5, C₂ = 6
      D^3 → 3' ⊕ 4: need to check
    """
    casimirs = {
        'A_4': {
            '1': 0,     # j=0
            "1'": 0,    # non-SO(3), trivial Casimir
            "1''": 0,   # non-SO(3), trivial Casimir
            '3': 2,     # j=1, C₂ = 1×2 = 2
        },
        'S_4': {
            '1': 0,     # j=0
            "1'": 0,    # sign rep, not SO(3)
            '2': 6,     # from j=2 restriction (D^2 = 2 ⊕ 3')
            '3': 2,     # j=1
            "3'": 6,    # from j=2 restriction
        },
        'A_5': {
            '1': 0,     # j=0
            '3': 2,     # j=1
            "3'": 12,   # from j=3 restriction (D^3 → 3' ⊕ 4... actually need to check)
            '4': 12,    # from j=3 restriction
            '5': 6,     # j=2
        },
    }
    return casimirs


# =====================================================================
# Tangent space decomposition into irreps
# =====================================================================

def tangent_space_decomposition(group_name, N):
    """Decompose the tangent space at a Platonic configuration into irreps.

    The tangent space T has dimension 2N (two tangential directions per vertex).
    The physical space (after removing SO(3) zero modes) has dimension 2N-3.

    For a configuration with symmetry G ⊂ SO(3), the tangent space
    decomposes as a representation of G. We compute this using the
    character formula.

    The tangent representation = (natural permutation rep on N vertices) ⊗ R²
    minus the SO(3) adjoint (3-dim, the zero modes).
    """
    if group_name == 'A_4':
        # A_4 acts on 4 vertices. The permutation rep decomposes as:
        # R^4 = 1 ⊕ 3 (trivial + standard)
        # Tangent space: R^4 ⊗ R^2 (each vertex has 2 tangent DOF on S²)
        # But R^2 at each vertex is the tangent plane, which transforms
        # differently under G depending on the vertex stabilizer.
        #
        # For the tetrahedron, the vertex stabilizer is Z_3 (rotations
        # fixing one vertex). The tangent plane at a vertex transforms
        # as the standard 2-dim rep of Z_3.
        #
        # The induced representation: Ind_{Z_3}^{A_4}(R²)
        # = Ind_{Z_3}^{A_4}(1 ⊕ ω ⊕ ω²) ... actually R² = 1+ω where ω = e^{2πi/3}
        #
        # This gets complicated. Let me just use the numerical approach.
        return {'method': 'numerical', 'N': N, 'group': group_name}

    return {'method': 'numerical', 'N': N, 'group': group_name}


def numerical_irrep_decomposition(vertices, group_name):
    """Numerically decompose the Hessian eigenspaces into group irreps.

    Method: compute the Hessian, diagonalize, then check which eigenspaces
    are invariant under the group action. The dimension of each eigenspace
    tells us which irrep it belongs to.
    """
    from planetary_polygons.explorations.platonic_vortices import (
        hessian_log_sin_s2, tangent_basis_at_point
    )

    N = len(vertices)
    H = hessian_log_sin_s2(vertices)
    evals, evecs = np.linalg.eigh(H)

    # Group eigenvalues by degeneracy (within tolerance)
    tol = 1e-4
    groups = []
    used = set()
    sorted_idx = np.argsort(evals)

    for i in sorted_idx:
        if i in used:
            continue
        val = evals[i]
        cluster = [i]
        for j in sorted_idx:
            if j != i and j not in used and abs(evals[j] - val) < tol:
                cluster.append(j)
        for j in cluster:
            used.add(j)
        groups.append({
            'eigenvalue': np.mean(evals[list(cluster)]),
            'degeneracy': len(cluster),
            'indices': cluster,
        })

    # Sort by eigenvalue
    groups.sort(key=lambda g: g['eigenvalue'])

    return {
        'group_name': group_name,
        'N': N,
        'eigenvalue_groups': groups,
        'total_dim': 2 * N,
    }


# =====================================================================
# The generalized Havelock conjecture
# =====================================================================

def test_generalized_havelock(group_name, vertices):
    """Test: do the eigenvalue degeneracies match irrep dimensions?

    If the Havelock decomposition generalizes, then:
    1. Each eigenspace should have dimension = dim(ρ) for some irrep ρ
    2. The eigenvalue should be C₁ - C₂(ρ) for the SO(3) Casimir C₂

    This is the KEY TEST of the generalization.
    """
    decomp = numerical_irrep_decomposition(vertices, group_name)

    # Get the character table
    if group_name == 'A_4':
        _, _, irrep_dims, irrep_names = A4_character_table()
    elif group_name == 'S_4':
        _, _, irrep_dims, irrep_names = S4_character_table()
    elif group_name == 'A_5':
        _, _, irrep_dims, irrep_names = A5_character_table()
    else:
        return {'error': f'Unknown group {group_name}'}

    casimirs = so3_casimirs_platonic()[group_name]

    # Check if each eigenspace dimension matches an irrep dimension
    matches = []
    for g in decomp['eigenvalue_groups']:
        deg = g['degeneracy']
        matching_irreps = [name for name, dim in zip(irrep_names, irrep_dims)
                           if dim == deg]
        g['matching_irreps'] = matching_irreps
        g['matches_irrep'] = len(matching_irreps) > 0
        matches.append(g)

    # Try to identify C₁: the "offset" that makes λ_ρ = C₁ - C₂(ρ)
    # For the trivial irrep (dim 1), λ_trivial = C₁ - 0 = C₁
    # So C₁ = eigenvalue of the trivial (1-dim) eigenspace
    trivial_eigenspaces = [g for g in matches if g['degeneracy'] == 1]

    # Check the C₁ - C₂(ρ) formula
    formula_check = []
    if trivial_eigenspaces:
        C1_candidates = [g['eigenvalue'] for g in trivial_eigenspaces]
        for C1 in C1_candidates:
            checks = []
            for g in matches:
                if g['degeneracy'] == 1:
                    continue  # skip trivial
                for irrep_name in g['matching_irreps']:
                    if irrep_name in casimirs:
                        C2 = casimirs[irrep_name]
                        predicted = C1 - C2
                        actual = g['eigenvalue']
                        err = abs(predicted - actual)
                        checks.append({
                            'irrep': irrep_name,
                            'C2': C2,
                            'predicted': predicted,
                            'actual': actual,
                            'error': err,
                            'matches': err < 0.5,  # generous tolerance
                        })
            if checks:
                formula_check.append({
                    'C1': C1,
                    'checks': checks,
                    'all_match': all(c['matches'] for c in checks),
                })

    return {
        'group_name': group_name,
        'eigenspace_decomposition': matches,
        'all_degeneracies_match_irreps': all(g['matches_irrep'] for g in matches),
        'C1_formula_checks': formula_check,
        'generalized_havelock_works': any(fc['all_match'] for fc in formula_check) if formula_check else False,
    }


# =====================================================================
# Main exploration
# =====================================================================

if __name__ == '__main__':
    from planetary_polygons.explorations.platonic_vortices import (
        tetrahedron_vertices, octahedron_vertices, cube_vertices,
        icosahedron_vertices, dodecahedron_vertices,
    )

    print("=" * 75)
    print("IRREP DECOMPOSITION OF PLATONIC VORTEX HESSIANS")
    print("=" * 75)
    print()

    # Character tables
    for name, table_fn in [('A_4', A4_character_table),
                            ('S_4', S4_character_table),
                            ('A_5', A5_character_table)]:
        table, sizes, dims, names = table_fn()
        order = sum(sizes)
        print(f"{name} (order {order}): irreps = {dict(zip(names, dims))}")
    print()

    # SO(3) Casimirs
    casimirs = so3_casimirs_platonic()
    print("SO(3) Casimirs (j(j+1) from embedding):")
    for group, cas in casimirs.items():
        print(f"  {group}: {cas}")
    print()

    # Eigenvalue decomposition for each Platonic solid
    configs = [
        ('A_4', 'tetrahedron', tetrahedron_vertices()),
        ('S_4', 'octahedron', octahedron_vertices()),
        ('S_4', 'cube', cube_vertices()),
        ('A_5', 'icosahedron', icosahedron_vertices()),
    ]

    for group_name, solid_name, verts in configs:
        print(f"--- {solid_name} (N={len(verts)}, group={group_name}) ---")

        decomp = numerical_irrep_decomposition(verts, group_name)
        print(f"  Eigenvalue groups (degeneracy):")
        for g in decomp['eigenvalue_groups']:
            print(f"    λ = {g['eigenvalue']:+8.4f}, deg = {g['degeneracy']}")

        result = test_generalized_havelock(group_name, verts)
        print(f"  All degeneracies match irreps: {result['all_degeneracies_match_irreps']}")

        if result['C1_formula_checks']:
            for fc in result['C1_formula_checks']:
                print(f"  C₁ = {fc['C1']:.4f}:")
                for c in fc['checks']:
                    status = "✓" if c['matches'] else "✗"
                    print(f"    {c['irrep']}: C₂={c['C2']}, predicted={c['predicted']:.4f}, "
                          f"actual={c['actual']:.4f}, err={c['error']:.4f} {status}")
                print(f"  Generalized Havelock: {fc['all_match']}")
        else:
            print(f"  No C₁ formula check possible (no trivial eigenspace found)")
        print()

    print("=" * 75)
    print("SUMMARY: Does λ_ρ = C₁ - C₂(ρ) hold for Platonic solids?")
    print("=" * 75)
