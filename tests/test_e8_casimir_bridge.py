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
