"""
Tests for E₈ Casimir = Platonic Havelock bridge identity.

THEOREM: For each irrep ρ of I* (binary icosahedral group, order 120),
the Platonic Havelock Casimir T_ρ equals j_ρ(j_ρ+1) × C₁_norm,
where j_ρ is the SU(2) spin and C₁_norm is a universal geometric
constant of the icosahedron.
"""

import pytest
import numpy as np
from math import pi, sqrt


class TestIStarCharacterTable:
    """Tests for the binary icosahedral group I* character table."""

    def test_group_order(self):
        """I* has order 120."""
        from planetary_polygons.proofs.e8_casimir_bridge import i_star_character_table
        table, class_sizes, irrep_dims, irrep_names, class_angles = (
            i_star_character_table()
        )
        assert sum(class_sizes) == 120

    def test_num_irreps(self):
        """I* has 9 irreducible representations."""
        from planetary_polygons.proofs.e8_casimir_bridge import i_star_character_table
        table, class_sizes, irrep_dims, irrep_names, class_angles = (
            i_star_character_table()
        )
        assert len(irrep_dims) == 9
        assert table.shape == (9, 9)

    def test_sum_of_squares(self):
        """Σ dᵢ² = |G| = 120."""
        from planetary_polygons.proofs.e8_casimir_bridge import i_star_character_table
        table, class_sizes, irrep_dims, irrep_names, class_angles = (
            i_star_character_table()
        )
        assert sum(d**2 for d in irrep_dims) == 120

    def test_irrep_dims_mckay_order(self):
        """Dims in McKay (affine E₈) order: {1,2,3,4,5,6,4,2,3}."""
        from planetary_polygons.proofs.e8_casimir_bridge import i_star_character_table
        table, class_sizes, irrep_dims, irrep_names, class_angles = (
            i_star_character_table()
        )
        assert irrep_dims == [1, 2, 3, 4, 5, 6, 4, 2, 3]

    def test_row_orthogonality(self):
        """(1/|G|) Σ_C |C| χᵢ(C)* χⱼ(C) = δᵢⱼ."""
        from planetary_polygons.proofs.e8_casimir_bridge import i_star_character_table
        table, class_sizes, irrep_dims, irrep_names, class_angles = (
            i_star_character_table()
        )
        sizes = np.array(class_sizes, dtype=complex)
        for i in range(9):
            for j in range(9):
                inner = np.sum(sizes * np.conj(table[i]) * table[j]) / 120.0
                expected = 1.0 if i == j else 0.0
                assert abs(inner - expected) < 1e-10, (
                    f"Row orthogonality fail: <χ_{i}, χ_{j}> = {inner}"
                )

    def test_column_orthogonality(self):
        """Σ_ρ χ_ρ(C_a)* χ_ρ(C_b) = (|G|/|C_a|) δ_{ab}."""
        from planetary_polygons.proofs.e8_casimir_bridge import i_star_character_table
        table, class_sizes, irrep_dims, irrep_names, class_angles = (
            i_star_character_table()
        )
        for a in range(9):
            for b in range(9):
                inner = sum(
                    np.conj(table[rho, a]) * table[rho, b]
                    for rho in range(9)
                )
                expected = 120.0 / class_sizes[a] if a == b else 0.0
                assert abs(inner - expected) < 1e-10, (
                    f"Column orthogonality fail at ({a},{b}): {inner} != {expected}"
                )

    def test_identity_character(self):
        """χ_ρ(e) = dim(ρ) for all irreps."""
        from planetary_polygons.proofs.e8_casimir_bridge import i_star_character_table
        table, class_sizes, irrep_dims, irrep_names, class_angles = (
            i_star_character_table()
        )
        for i, d in enumerate(irrep_dims):
            assert abs(table[i, 0] - d) < 1e-10

    def test_center_character(self):
        """χ_ρ(-I) = +dim for integer spin, -dim for half-integer."""
        from planetary_polygons.proofs.e8_casimir_bridge import i_star_character_table
        table, class_sizes, irrep_dims, irrep_names, class_angles = (
            i_star_character_table()
        )
        # Integer spin: ρ₀,ρ₂,ρ₄,ρ₆,ρ₈ → χ(-I)=+dim
        # Half-integer: ρ₁,ρ₃,ρ₅,ρ₇ → χ(-I)=-dim
        integer_spin = [0, 2, 4, 6, 8]
        half_integer_spin = [1, 3, 5, 7]
        for i in integer_spin:
            assert abs(table[i, 1] - irrep_dims[i]) < 1e-10, (
                f"ρ_{i}: χ(-I)={table[i,1].real:.4f}, expected +{irrep_dims[i]}"
            )
        for i in half_integer_spin:
            assert abs(table[i, 1] + irrep_dims[i]) < 1e-10, (
                f"ρ_{i}: χ(-I)={table[i,1].real:.4f}, expected -{irrep_dims[i]}"
            )

    def test_mckay_tensor_product(self):
        """McKay graph: ρ₁ ⊗ ρᵢ encodes extended E₈ Dynkin diagram.

        Adjacency: 0-1-2-3-4-5-6-7 with branch 5-8.
        """
        from planetary_polygons.proofs.e8_casimir_bridge import i_star_character_table
        table, class_sizes, irrep_dims, irrep_names, class_angles = (
            i_star_character_table()
        )
        sizes = np.array(class_sizes, dtype=complex)
        expected_adj = {
            0: {1: 1},
            1: {0: 1, 2: 1},
            2: {1: 1, 3: 1},
            3: {2: 1, 4: 1},
            4: {3: 1, 5: 1},
            5: {4: 1, 6: 1, 8: 1},
            6: {5: 1, 7: 1},
            7: {6: 1},
            8: {5: 1},
        }
        for i in range(9):
            mults = []
            for j in range(9):
                inner = np.sum(
                    sizes * table[1] * table[i] * np.conj(table[j])
                ) / 120.0
                mults.append(int(round(inner.real)))
            expected = expected_adj[i]
            for j in range(9):
                exp = expected.get(j, 0)
                assert mults[j] == exp, (
                    f"McKay fail: ρ₁⊗ρ_{i} has mult(ρ_{j})={mults[j]}, "
                    f"expected {exp}"
                )


class TestIntegerSpinCasimirs:
    """Platonic Havelock T_j for icosahedron A₅ irreps (integer spin)."""

    def test_T0_is_zero(self):
        """Trivial irrep (j=0) has T=0."""
        from planetary_polygons.proofs.e8_casimir_bridge import (
            icosahedron_havelock_casimirs_integer_spin,
        )
        casimirs = icosahedron_havelock_casimirs_integer_spin()
        assert abs(casimirs[0]) < 1e-10

    def test_T1_positive(self):
        """j=1 irrep has T>0."""
        from planetary_polygons.proofs.e8_casimir_bridge import (
            icosahedron_havelock_casimirs_integer_spin,
        )
        casimirs = icosahedron_havelock_casimirs_integer_spin()
        assert casimirs[1] > 0

    def test_exact_T_values(self):
        """T values are exact half-integers determined by icosahedral geometry.

        T₀ = 0, T₁ = 11/2, T₂ = 15/2, T₃ = 8.
        These are NOT proportional to j(j+1).
        C₁ = 13/2.
        """
        from planetary_polygons.proofs.e8_casimir_bridge import (
            icosahedron_havelock_casimirs_integer_spin,
        )
        from planetary_polygons.proofs.platonic_havelock import per_vertex_sum
        from planetary_polygons.explorations.platonic_vortices import (
            icosahedron_vertices,
        )
        casimirs = icosahedron_havelock_casimirs_integer_spin()
        verts = icosahedron_vertices()
        C1 = per_vertex_sum(verts)
        assert abs(C1 - 6.5) < 1e-10, f"C₁ = {C1}, expected 13/2"
        assert abs(casimirs[0] - 0.0) < 1e-10
        assert abs(casimirs[1] - 5.5) < 1e-10, f"T₁ = {casimirs[1]}"
        assert abs(casimirs[2] - 7.5) < 1e-10, f"T₂ = {casimirs[2]}"
        assert abs(casimirs[3] - 8.0) < 1e-10, f"T₃ = {casimirs[3]}"

    def test_T1_equals_N_minus_1_over_2(self):
        """Universal Casimir: T₁ = (N-1)/2 for any Platonic solid."""
        from planetary_polygons.proofs.e8_casimir_bridge import (
            icosahedron_havelock_casimirs_integer_spin,
        )
        casimirs = icosahedron_havelock_casimirs_integer_spin()
        N = 12  # icosahedron vertices
        assert abs(casimirs[1] - (N - 1) / 2) < 1e-10


class TestE8AdjointDecomposition:
    """E₈ adjoint (248-dim) decomposition under I*."""

    def test_principal_su2_identity_char(self):
        """Character at identity = 248."""
        from planetary_polygons.proofs.e8_casimir_bridge import (
            e8_adjoint_character_principal_su2,
        )
        char = e8_adjoint_character_principal_su2()
        assert abs(char[0] - 248) < 1e-10

    def test_principal_su2_dim_sum(self):
        """Decomposition sums to 248."""
        from planetary_polygons.proofs.e8_casimir_bridge import (
            e8_adjoint_character_principal_su2, decompose_under_i_star,
            i_star_character_table,
        )
        char = e8_adjoint_character_principal_su2()
        mults = decompose_under_i_star(char)
        _, _, dims, _, _ = i_star_character_table()
        assert sum(m * d for m, d in zip(mults, dims)) == 248

    def test_principal_su2_integer_spin_only(self):
        """Principal SU(2) uses only integer-spin irreps (all E₈ exponents are integer)."""
        from planetary_polygons.proofs.e8_casimir_bridge import (
            e8_adjoint_character_principal_su2, decompose_under_i_star,
        )
        char = e8_adjoint_character_principal_su2()
        mults = decompose_under_i_star(char)
        # Half-integer indices: 1(ρ₁), 3(ρ₃), 5(ρ₅), 7(ρ₇)
        for i in [1, 3, 5, 7]:
            assert mults[i] == 0, f"ρ_{i} has mult {mults[i]}, expected 0"

    def test_principal_su2_known_mults(self):
        """Principal SU(2) gives mults [0,0,14,0,20,0,16,0,14]."""
        from planetary_polygons.proofs.e8_casimir_bridge import (
            e8_adjoint_character_principal_su2, decompose_under_i_star,
        )
        char = e8_adjoint_character_principal_su2()
        mults = decompose_under_i_star(char)
        assert mults == [0, 0, 14, 0, 20, 0, 16, 0, 14]

    def test_su2_e7_dim_sum(self):
        """SU(2)×E₇ decomposition sums to 248."""
        from planetary_polygons.proofs.e8_casimir_bridge import (
            e8_adjoint_character_su2_e7, decompose_under_i_star,
            i_star_character_table,
        )
        char = e8_adjoint_character_su2_e7()
        mults = decompose_under_i_star(char)
        _, _, dims, _, _ = i_star_character_table()
        assert sum(m * d for m, d in zip(mults, dims)) == 248

    def test_su2_e7_known_mults(self):
        """SU(2)×E₇ gives mults [133, 56, 1, 0, 0, 0, 0, 0, 0]."""
        from planetary_polygons.proofs.e8_casimir_bridge import (
            e8_adjoint_character_su2_e7, decompose_under_i_star,
        )
        char = e8_adjoint_character_su2_e7()
        mults = decompose_under_i_star(char)
        assert mults == [133, 56, 1, 0, 0, 0, 0, 0, 0]


class TestTangentHessianPairing:
    """Tangent-space Hessian eigenvalue pairing theorem."""

    def test_icosahedron_trace(self):
        """Tr(H) = N(N-1)/2 = 66 for icosahedron."""
        from planetary_polygons.proofs.e8_casimir_bridge import (
            tangent_hessian_eigenvalues,
        )
        from planetary_polygons.explorations.platonic_vortices import (
            icosahedron_vertices,
        )
        evals = tangent_hessian_eigenvalues(icosahedron_vertices())
        N = 12
        assert abs(sum(evals) - N * (N - 1) / 2) < 0.01

    def test_icosahedron_eigenvalue_pairs_sum(self):
        """All eigenvalue pairs sum to (N-1)/2 = 11/2 for icosahedron.

        THEOREM: The tangent Hessian eigenvalues come in pairs
        (lambda_-, lambda_+) with lambda_- + lambda_+ = (N-1)/2.

        Icosahedron pairs:
          3-dim: (0, 11/2)
          4-dim: (5/4, 17/4)
          5-dim: (1/2, 5)
        """
        from planetary_polygons.proofs.e8_casimir_bridge import (
            tangent_hessian_eigenvalues, cluster_eigenvalues,
        )
        from planetary_polygons.explorations.platonic_vortices import (
            icosahedron_vertices,
        )
        evals = tangent_hessian_eigenvalues(icosahedron_vertices())
        clusters = cluster_eigenvalues(evals)
        N = 12
        target = (N - 1) / 2.0

        # Match pairs by degeneracy
        by_deg = {}
        for val, deg in clusters:
            by_deg.setdefault(deg, []).append(val)

        for deg, vals in by_deg.items():
            if len(vals) == 2:
                pair_sum = vals[0] + vals[1]
                assert abs(pair_sum - target) < 0.01, (
                    f"deg-{deg} pair ({vals[0]:.4f}, {vals[1]:.4f}) "
                    f"sums to {pair_sum:.4f}, expected {target}"
                )

    def test_icosahedron_exact_eigenvalues(self):
        """Exact eigenvalues: 0(x3), 1/2(x5), 5/4(x4), 17/4(x4), 5(x5), 11/2(x3)."""
        from planetary_polygons.proofs.e8_casimir_bridge import (
            tangent_hessian_eigenvalues, cluster_eigenvalues,
        )
        from planetary_polygons.explorations.platonic_vortices import (
            icosahedron_vertices,
        )
        evals = tangent_hessian_eigenvalues(icosahedron_vertices())
        clusters = cluster_eigenvalues(evals)
        expected = [(0, 3), (0.5, 5), (1.25, 4), (4.25, 4), (5.0, 5), (5.5, 3)]
        assert len(clusters) == len(expected)
        for (val, deg), (exp_val, exp_deg) in zip(clusters, expected):
            assert deg == exp_deg, f"deg {deg} != {exp_deg}"
            assert abs(val - exp_val) < 0.01, f"{val} != {exp_val}"

    def test_tetrahedron_pairing(self):
        """Tetrahedron: pairs (0, 3/2) and (3/4, 3/4) sum to 3/2."""
        from planetary_polygons.proofs.e8_casimir_bridge import (
            tangent_hessian_eigenvalues, cluster_eigenvalues,
        )
        from planetary_polygons.explorations.platonic_vortices import (
            tetrahedron_vertices,
        )
        evals = tangent_hessian_eigenvalues(tetrahedron_vertices())
        N = 4
        assert abs(sum(evals) - N * (N - 1) / 2) < 0.01
        clusters = cluster_eigenvalues(evals)
        # (0, 3), (0.75, 2), (1.5, 3) — pairs: (0,1.5) and (0.75,0.75)
        target = (N - 1) / 2.0  # 1.5
        vals = [v for v, d in clusters]
        assert abs(vals[0] + vals[2] - target) < 0.01  # 0 + 1.5
        assert abs(2 * vals[1] - target) < 0.01  # 0.75 + 0.75

    def test_octahedron_pairing(self):
        """Octahedron: pairs (0, 5/2) and (1/2, 2) sum to 5/2."""
        from planetary_polygons.proofs.e8_casimir_bridge import (
            tangent_hessian_eigenvalues, cluster_eigenvalues,
        )
        from planetary_polygons.explorations.platonic_vortices import (
            octahedron_vertices,
        )
        evals = tangent_hessian_eigenvalues(octahedron_vertices())
        N = 6
        assert abs(sum(evals) - N * (N - 1) / 2) < 0.01
        clusters = cluster_eigenvalues(evals)
        target = (N - 1) / 2.0  # 2.5
        vals = [v for v, d in clusters]
        assert abs(vals[0] + vals[3] - target) < 0.01  # 0 + 2.5
        assert abs(vals[1] + vals[2] - target) < 0.01  # 0.5 + 2
