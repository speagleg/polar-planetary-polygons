"""
Tests for the generalized Havelock formula for Platonic solids.

THEOREM: T_ρ = Σ K(d)[1 - P_j(cos d)] when D^j|_G is irreducible.

Verifies:
1. Eigenvalue formula matches numerical K-matrix eigenvalues
2. P_j(cos d) IS the eigenvector of K (Schur + zonal spherical function)
3. The formula holds for tetrahedron, octahedron, icosahedron, cube (j≤2)
4. Per-vertex sum C₁ is G-symmetric
5. Zero-sum property (trivial irrep has T=0)
"""

import pytest
import numpy as np

from planetary_polygons.proofs.platonic_havelock import (
    interaction_matrix,
    per_vertex_sum,
    legendre_p,
    generalized_casimir,
    verify_formula,
    verify_eigenvector,
    full_proof,
)
from planetary_polygons.explorations.platonic_vortices import (
    tetrahedron_vertices,
    octahedron_vertices,
    cube_vertices,
    icosahedron_vertices,
)


class TestLegendre:
    def test_p0(self):
        assert abs(legendre_p(0, 0.5) - 1.0) < 1e-15

    def test_p1(self):
        assert abs(legendre_p(1, 0.5) - 0.5) < 1e-15

    def test_p2(self):
        # P_2(x) = (3x²-1)/2
        x = 0.5
        assert abs(legendre_p(2, x) - (3 * x ** 2 - 1) / 2) < 1e-15

    def test_p_at_1(self):
        """P_j(1) = 1 for all j (crucial for the proof)."""
        for j in range(10):
            assert abs(legendre_p(j, 1.0) - 1.0) < 1e-12


class TestInteractionMatrix:
    @pytest.mark.parametrize("vfn", [tetrahedron_vertices, octahedron_vertices,
                                      cube_vertices, icosahedron_vertices])
    def test_zero_sum(self, vfn):
        """Each row sums to zero."""
        K = interaction_matrix(vfn())
        row_sums = np.sum(K, axis=1)
        assert np.allclose(row_sums, 0, atol=1e-12)

    @pytest.mark.parametrize("vfn", [tetrahedron_vertices, octahedron_vertices,
                                      cube_vertices, icosahedron_vertices])
    def test_symmetric(self, vfn):
        """K is symmetric (K_{jk} = K_{kj})."""
        K = interaction_matrix(vfn())
        assert np.allclose(K, K.T, atol=1e-12)

    @pytest.mark.parametrize("vfn", [tetrahedron_vertices, octahedron_vertices,
                                      cube_vertices, icosahedron_vertices])
    def test_per_vertex_sum_constant(self, vfn):
        """C₁ is the same at every vertex (G-symmetry)."""
        verts = vfn()
        N = len(verts)
        K = interaction_matrix(verts)
        sums = [-K[j, j] for j in range(N)]  # -K_{jj} = Σ_{k≠j} K_{jk}
        assert np.allclose(sums, sums[0], atol=1e-10)


class TestGeneralizedCasimir:
    def test_j0_is_zero(self):
        """T_0 = 0 (trivial irrep, from P_0=1)."""
        for vfn in [tetrahedron_vertices, octahedron_vertices, icosahedron_vertices]:
            assert abs(generalized_casimir(vfn(), 0)) < 1e-12

    def test_tetra_j1(self):
        T = generalized_casimir(tetrahedron_vertices(), 1)
        assert abs(T - 1.5) < 1e-10

    def test_octa_j1(self):
        T = generalized_casimir(octahedron_vertices(), 1)
        assert abs(T - 2.5) < 1e-10

    def test_octa_j2(self):
        T = generalized_casimir(octahedron_vertices(), 2)
        assert abs(T - 3.0) < 1e-10

    def test_icosa_j1(self):
        T = generalized_casimir(icosahedron_vertices(), 1)
        assert abs(T - 5.5) < 1e-10

    def test_icosa_j3(self):
        T = generalized_casimir(icosahedron_vertices(), 3)
        assert abs(T - 8.0) < 1e-10


class TestEigenvalueFormula:
    """Verify T_j matches K-matrix eigenvalues."""

    @pytest.mark.parametrize("name,vfn,j_max", [
        ('tetra', tetrahedron_vertices, 1),
        ('octa', octahedron_vertices, 2),
        ('icosa', icosahedron_vertices, 3),
        ('cube', cube_vertices, 2),
    ])
    def test_all_match(self, name, vfn, j_max):
        result = verify_formula(vfn(), name, j_max)
        assert result['all_match'], f"{name}: eigenvalue mismatch"


class TestEigenvector:
    """Verify P_j(cos d) IS the eigenvector of K."""

    @pytest.mark.parametrize("name,vfn,j_list", [
        ('tetra', tetrahedron_vertices, [1]),
        ('octa', octahedron_vertices, [1, 2]),
        ('icosa', icosahedron_vertices, [1, 2, 3]),
        ('cube', cube_vertices, [1, 2]),
    ])
    def test_eigenvector(self, name, vfn, j_list):
        verts = vfn()
        for j in j_list:
            result = verify_eigenvector(verts, j)
            assert result['is_eigenvector'], (
                f"{name}, j={j}: residual={result['residual']:.2e}"
            )


class TestFullProof:
    def test_all_solids(self):
        results = full_proof()
        for name, data in results.items():
            assert data['all_eigenvalues_match'], f"{name}: eigenvalue mismatch"
            assert data['all_eigenvectors_match'], f"{name}: eigenvector mismatch"
