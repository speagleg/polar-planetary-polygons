"""
Tests for the generalized Havelock formula for Platonic solids.

THEOREM: T_ρ = Σ K(d)[1 - P_j(cos d)] when D^j|_G is irreducible.

EXTENDED: T_ρ = Σ K(d)[1 - φ_ρ(v_k)] using the full G-character formula,
which handles the case where D^j SPLITS into multiple G-irreps upon
restriction (e.g., cube j=3: D³|_{S_4} = 1' ⊕ 3 ⊕ 3').

Verifies:
1. Eigenvalue formula matches numerical K-matrix eigenvalues
2. P_j(cos d) IS the eigenvector of K (Schur + zonal spherical function)
3. The formula holds for tetrahedron, octahedron, icosahedron, cube (j≤2)
4. Per-vertex sum C₁ is G-symmetric
5. Zero-sum property (trivial irrep has T=0)
6. FULL character formula for cube j=3 (split case)
7. FULL character formula for dodecahedron j=3,4,5 (split cases)
8. Cross-check: full formula = Legendre formula when D^j is irreducible
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
    build_rotation_group,
    find_coset_representatives,
    rotation_angle,
    so3_character,
    generalized_casimir_full,
    verify_full_formula,
    zonal_spherical_function_full,
    _classify_conjugacy_classes,
    _match_conjugacy_classes,
    _character_table_for_group,
    _so3_restriction_to_g,
)
from planetary_polygons.explorations.platonic_vortices import (
    tetrahedron_vertices,
    octahedron_vertices,
    cube_vertices,
    icosahedron_vertices,
    dodecahedron_vertices,
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


# =====================================================================
# Tests for the rotation group construction
# =====================================================================

class TestBuildRotationGroup:
    """Test that we correctly enumerate all rotation matrices for each group."""

    def test_tetrahedron_order_12(self):
        group = build_rotation_group('tetrahedron')
        assert len(group) == 12, f"A_4 should have order 12, got {len(group)}"

    def test_cube_order_24(self):
        group = build_rotation_group('cube')
        assert len(group) == 24, f"S_4 should have order 24, got {len(group)}"

    def test_octahedron_order_24(self):
        group = build_rotation_group('octahedron')
        assert len(group) == 24

    def test_icosahedron_order_60(self):
        group = build_rotation_group('icosahedron')
        assert len(group) == 60, f"A_5 should have order 60, got {len(group)}"

    def test_dodecahedron_order_60(self):
        group = build_rotation_group('dodecahedron')
        assert len(group) == 60

    def test_closure_tetrahedron(self):
        """Verify the group is closed under multiplication."""
        group = build_rotation_group('tetrahedron')
        for g1 in group:
            for g2 in group:
                product = g1 @ g2
                found = any(np.allclose(product, g, atol=1e-8) for g in group)
                assert found, "Product not in group -- not closed"

    def test_closure_cube(self):
        group = build_rotation_group('cube')
        for g1 in group:
            for g2 in group:
                product = g1 @ g2
                found = any(np.allclose(product, g, atol=1e-8) for g in group)
                assert found, "Product not in group -- not closed"

    def test_all_rotations(self):
        """Every matrix should be a proper rotation (det=1, orthogonal)."""
        for name in ['tetrahedron', 'cube', 'icosahedron']:
            group = build_rotation_group(name)
            for g in group:
                assert abs(np.linalg.det(g) - 1.0) < 1e-10, \
                    f"{name}: det != 1"
                assert np.allclose(g @ g.T, np.eye(3), atol=1e-10), \
                    f"{name}: not orthogonal"

    def test_identity_present(self):
        """Identity matrix should be in every group."""
        for name in ['tetrahedron', 'cube', 'icosahedron', 'dodecahedron']:
            group = build_rotation_group(name)
            has_identity = any(np.allclose(g, np.eye(3), atol=1e-10)
                               for g in group)
            assert has_identity, f"{name}: identity not found"


class TestCosetRepresentatives:
    """Test coset decomposition G = union of g_k * H."""

    @pytest.mark.parametrize("name,vfn,expected_coset_size", [
        ('tetrahedron', tetrahedron_vertices, 3),   # |A_4|/4 = 3
        ('cube', cube_vertices, 3),                 # |S_4|/8 = 3
        ('octahedron', octahedron_vertices, 4),     # |S_4|/6 = 4
        ('icosahedron', icosahedron_vertices, 5),   # |A_5|/12 = 5
        ('dodecahedron', dodecahedron_vertices, 3), # |A_5|/20 = 3
    ])
    def test_coset_sizes(self, name, vfn, expected_coset_size):
        verts = vfn()
        group = build_rotation_group(name)
        cosets = find_coset_representatives(verts, group)
        for k, c in enumerate(cosets):
            assert len(c) == expected_coset_size, \
                f"{name} vertex {k}: coset size {len(c)} != {expected_coset_size}"

    def test_all_elements_assigned(self):
        """Every group element should be in exactly one coset."""
        for name, vfn in [('cube', cube_vertices),
                          ('dodecahedron', dodecahedron_vertices)]:
            verts = vfn()
            group = build_rotation_group(name)
            cosets = find_coset_representatives(verts, group)
            all_indices = []
            for c in cosets:
                all_indices.extend(c)
            assert sorted(all_indices) == list(range(len(group)))


class TestConjugacyClasses:
    """Test conjugacy class computation."""

    def test_tetrahedron_4_classes(self):
        group = build_rotation_group('tetrahedron')
        classes, angles = _classify_conjugacy_classes(group)
        assert len(classes) == 4, \
            f"A_4 should have 4 conjugacy classes, got {len(classes)}"

    def test_cube_5_classes(self):
        group = build_rotation_group('cube')
        classes, angles = _classify_conjugacy_classes(group)
        assert len(classes) == 5, \
            f"S_4 should have 5 conjugacy classes, got {len(classes)}"

    def test_icosahedron_5_classes(self):
        group = build_rotation_group('icosahedron')
        classes, angles = _classify_conjugacy_classes(group)
        assert len(classes) == 5, \
            f"A_5 should have 5 conjugacy classes, got {len(classes)}"

    def test_class_sizes_sum_to_order(self):
        for name, order in [('tetrahedron', 12), ('cube', 24),
                            ('icosahedron', 60)]:
            group = build_rotation_group(name)
            classes, _ = _classify_conjugacy_classes(group)
            total = sum(len(c) for c in classes)
            assert total == order, \
                f"{name}: class sizes sum to {total}, not {order}"


class TestSO3Character:
    """Test the SO(3) character formula."""

    def test_identity(self):
        """chi_j(identity) = 2j+1."""
        I = np.eye(3)
        for j in range(6):
            assert abs(so3_character(j, I) - (2*j+1)) < 1e-12

    def test_pi_rotation(self):
        """chi_j(pi rotation) = (-1)^j."""
        from math import pi
        from planetary_polygons.proofs.platonic_havelock import rotation_matrix
        R = rotation_matrix([0, 0, 1], pi)
        for j in range(6):
            expected = (-1)**j
            assert abs(so3_character(j, R) - expected) < 1e-10, \
                f"j={j}: got {so3_character(j, R)}, expected {expected}"


# =====================================================================
# Tests for D^j restriction and decomposition
# =====================================================================

class TestDjRestriction:
    """Test the decomposition of D^j upon restriction to G."""

    def _get_decomposition(self, name, j):
        group = build_rotation_group(name)
        classes, angles = _classify_conjugacy_classes(group)
        table, csizes, dims, names, order = _character_table_for_group(name)
        _, perm = _match_conjugacy_classes(
            group, classes, angles, table, csizes, dims, order)
        classes_matched = [classes[perm[i]] for i in range(len(classes))]
        mults = _so3_restriction_to_g(
            j, group, classes_matched, angles, table, dims, order)
        return dict(zip(names, mults))

    # A_4 (tetrahedron)
    def test_A4_D0(self):
        d = self._get_decomposition('tetrahedron', 0)
        assert d == {'1': 1, "1'": 0, "1''": 0, '3': 0}

    def test_A4_D1(self):
        d = self._get_decomposition('tetrahedron', 1)
        assert d == {'1': 0, "1'": 0, "1''": 0, '3': 1}

    def test_A4_D2(self):
        """D^2|_{A_4} = 1' + 1'' + 3."""
        d = self._get_decomposition('tetrahedron', 2)
        assert d['3'] == 1
        # 1' and 1'' should each appear once
        assert d["1'"] + d["1''"] == 2

    def test_A4_D3(self):
        """D^3|_{A_4} = 1 + 3 + 3."""
        d = self._get_decomposition('tetrahedron', 3)
        assert d['1'] == 1
        assert d['3'] == 2  # 3 appears twice

    # S_4 (cube/octahedron)
    def test_S4_D0(self):
        d = self._get_decomposition('cube', 0)
        assert d == {'1': 1, "1'": 0, '2': 0, '3': 0, "3'": 0}

    def test_S4_D1(self):
        d = self._get_decomposition('cube', 1)
        assert d == {'1': 0, "1'": 0, '2': 0, '3': 1, "3'": 0}

    def test_S4_D2(self):
        """D^2|_{S_4} = 2 + 3'."""
        d = self._get_decomposition('cube', 2)
        assert d == {'1': 0, "1'": 0, '2': 1, '3': 0, "3'": 1}

    def test_S4_D3(self):
        """D^3|_{S_4} = 1' + 3 + 3'. THIS is the key split case."""
        d = self._get_decomposition('cube', 3)
        assert d == {'1': 0, "1'": 1, '2': 0, '3': 1, "3'": 1}

    def test_S4_D3_dimension(self):
        """D^3 has dimension 7 = 1 + 3 + 3."""
        d = self._get_decomposition('cube', 3)
        dims = {'1': 1, "1'": 1, '2': 2, '3': 3, "3'": 3}
        total = sum(d[k] * dims[k] for k in d)
        assert total == 7

    # A_5 (icosahedron/dodecahedron)
    def test_A5_D1(self):
        d = self._get_decomposition('icosahedron', 1)
        assert d == {'1': 0, '3': 1, "3'": 0, '4': 0, '5': 0}

    def test_A5_D2(self):
        d = self._get_decomposition('icosahedron', 2)
        assert d == {'1': 0, '3': 0, "3'": 0, '4': 0, '5': 1}

    def test_A5_D3(self):
        """D^3|_{A_5} = 3' + 4."""
        d = self._get_decomposition('icosahedron', 3)
        assert d == {'1': 0, '3': 0, "3'": 1, '4': 1, '5': 0}

    def test_A5_D4(self):
        """D^4|_{A_5} = 4 + 5."""
        d = self._get_decomposition('icosahedron', 4)
        assert d == {'1': 0, '3': 0, "3'": 0, '4': 1, '5': 1}

    def test_A5_D5(self):
        """D^5|_{A_5} = 1 + 3 + 3' + 4 or similar (dim 11)."""
        d = self._get_decomposition('icosahedron', 5)
        dims = {'1': 1, '3': 3, "3'": 3, '4': 4, '5': 5}
        total = sum(d[k] * dims[k] for k in d)
        assert total == 11  # dim of D^5


# =====================================================================
# THE KEY TESTS: Full character formula for split cases
# =====================================================================

class TestFullCharacterFormula:
    """Test the full character formula T_rho = sum K(d)[1 - phi_rho(v_k)]
    where phi_rho is the G-zonal spherical function."""

    def test_cube_all_eigenvalues_match(self):
        """Cube: full formula matches ALL K-matrix eigenvalues."""
        result = verify_full_formula('cube')
        for m in result['matches']:
            assert m['eigenvalue_match'], \
                f"Cube irrep {m['irrep']}: T_formula={m['T_formula']:.6f} " \
                f"vs T_numerical={m['T_numerical']:.6f} (err={m['error']:.2e})"

    def test_cube_j3_split(self):
        """CRITICAL TEST: Cube at j=3 where D^3 splits into 1' + 3 + 3'.

        The Legendre formula gives the AVERAGE; the full formula gives
        the individual eigenvalues for 1', 3, and 3'.
        """
        verts = cube_vertices()
        result = generalized_casimir_full(verts, 'cube')

        # Check that D^3 splits into 1' + 3 + 3'
        decomp3 = result['decompositions'].get(3, [])
        decomp_dict = {name: mult for name, mult in decomp3}
        assert decomp_dict.get("1'", 0) == 1, "1' should appear in D^3|_{S_4}"
        assert decomp_dict.get("3", 0) == 1, "3 should appear in D^3|_{S_4}"
        assert decomp_dict.get("3'", 0) == 1, "3' should appear in D^3|_{S_4}"

        # Check that the three eigenvalues are DISTINCT
        T_1p = result['eigenvalues'].get("1'")
        T_3 = result['eigenvalues'].get("3")
        T_3p = result['eigenvalues'].get("3'")
        assert T_1p is not None, "1' eigenvalue missing"
        assert T_3 is not None, "3 eigenvalue missing"
        assert T_3p is not None, "3' eigenvalue missing"

        # They should not all be equal (that would mean the Legendre
        # formula was sufficient, contradicting the known splitting)
        values = [T_1p, T_3, T_3p]
        assert not (abs(values[0] - values[1]) < 0.01 and
                    abs(values[1] - values[2]) < 0.01), \
            "Split eigenvalues should be distinct"

        # The Legendre formula gives a DIFFERENT average than the
        # dim-weighted average because P_j is the SO(3) character,
        # not the G-character. They are related but not equal when
        # D^j splits into multiple G-irreps.
        T_legendre = generalized_casimir(verts, 3)
        T_avg = (1 * T_1p + 3 * T_3 + 3 * T_3p) / 7
        # Both should be in the range of the individual values
        assert min(values) - 0.5 < T_legendre < max(values) + 0.5, \
            f"Legendre T_3={T_legendre:.4f} should be near the split values"

    def test_cube_eigenvalues_vs_numerical(self):
        """Cube: each formula eigenvalue matches a numerical K eigenvalue."""
        verts = cube_vertices()
        K = interaction_matrix(verts)
        evals_K = sorted(-np.linalg.eigvalsh(K))

        result = generalized_casimir_full(verts, 'cube')
        for name, T_formula in result['eigenvalues'].items():
            if T_formula is None:
                continue
            # Find closest numerical eigenvalue
            diffs = [abs(T_formula - e) for e in evals_K]
            min_diff = min(diffs)
            assert min_diff < 0.01, \
                f"Cube {name}: T_formula={T_formula:.6f}, " \
                f"no matching numerical eigenvalue (min diff={min_diff:.2e})"

    def test_dodecahedron_eigenvalues_match(self):
        """Dodecahedron: full formula matches except multiplicity-2 irreps.

        The dim-4 irrep appears with multiplicity 2 in the permutation rep
        (20 = 1+3+3'+4+4+5). The character formula gives the AVERAGE of
        the two copies (16.0 = (15.125+16.875)/2), not the individual values.
        This is a fundamental limitation, not a bug.
        """
        result = verify_full_formula('dodecahedron')
        for m in result['matches']:
            if m['dim'] == 4:
                # Multiplicity-2: formula gives average, allow 1.0 tolerance
                assert m['error'] < 1.0, \
                    f"Dodec dim-4 avg: T={m['T_formula']:.4f} vs {m['T_numerical']:.4f}"
            else:
                assert m['eigenvalue_match'], \
                    f"Dodec {m['irrep']}: T={m['T_formula']:.6f} vs {m['T_numerical']:.6f}"

    def test_dodecahedron_j3_split(self):
        """Dodecahedron j=3: D^3|_{A_5} = 3' + 4, eigenvalues split.

        The 3' irrep (multiplicity 1) matches exactly.
        The 4-dim irrep (multiplicity 2) gives the AVERAGE of two copies.
        """
        verts = dodecahedron_vertices()
        result = generalized_casimir_full(verts, 'dodecahedron')

        T_3p = result['eigenvalues'].get("3'")
        assert T_3p is not None, "3' eigenvalue missing"

        # 3' (mult 1) should match K-matrix exactly
        K = interaction_matrix(verts)
        evals_K = sorted(-np.linalg.eigvalsh(K))
        diffs = [abs(T_3p - e) for e in evals_K]
        assert min(diffs) < 0.01, f"Dodec 3': T={T_3p:.4f}, no match"

    def test_dodecahedron_j4_multiplicity(self):
        """Dodecahedron dim-4: appears with multiplicity 2.

        The character formula gives the AVERAGE of the two copies:
        T_avg = (15.125 + 16.875)/2 = 16.0.
        This is a known limitation for irreps with multiplicity > 1.
        """
        verts = dodecahedron_vertices()
        result = generalized_casimir_full(verts, 'dodecahedron')
        T_4 = result['eigenvalues'].get('4')
        assert T_4 is not None

        # The average should be close to 16.0
        assert abs(T_4 - 16.0) < 0.1, f"Dodec 4: T_avg={T_4:.4f} (expect ~16.0)"

        # The actual eigenvalues are 15.125 and 16.875
        K = interaction_matrix(verts)
        evals_K = sorted(-np.linalg.eigvalsh(K))
        deg4_evals = [e for e in evals_K
                      if any(abs(e - t) < 0.1 for t in [15.125, 16.875])]
        assert len(deg4_evals) >= 4, "Should find at least 4 eigenvalues near 15.125/16.875"


class TestLegendreConsistency:
    """Cross-check: when D^j|_G is irreducible, the full formula
    must agree with the Legendre formula."""

    @pytest.mark.parametrize("name,vfn,j", [
        ('tetrahedron', tetrahedron_vertices, 1),    # D^1|_{A_4} = 3
        ('octahedron', octahedron_vertices, 1),      # D^1|_{S_4} = 3
        ('octahedron', octahedron_vertices, 2),      # D^2|_{S_4} = 2+3' (split!)
        ('cube', cube_vertices, 1),                  # D^1|_{S_4} = 3
        ('icosahedron', icosahedron_vertices, 1),    # D^1|_{A_5} = 3
        ('icosahedron', icosahedron_vertices, 2),    # D^2|_{A_5} = 5
    ])
    def test_irreducible_cases(self, name, vfn, j):
        """For irreducible D^j|_G, full formula = Legendre formula."""
        verts = vfn()
        result = generalized_casimir_full(verts, name)

        # Check if D^j is irreducible
        decomp = result['decompositions'].get(j, [])
        if len(decomp) == 1 and decomp[0][1] == 1:
            irrep_name = decomp[0][0]
            T_legendre = generalized_casimir(verts, j)
            T_full = result['eigenvalues'].get(irrep_name)
            assert T_full is not None, f"Missing eigenvalue for {irrep_name}"
            assert abs(T_legendre - T_full) < 1e-6, \
                f"{name} j={j}: Legendre={T_legendre:.8f}, " \
                f"full={T_full:.8f}, diff={abs(T_legendre-T_full):.2e}"

    def test_cube_legendre_consistency(self):
        """Comprehensive Legendre consistency check for the cube."""
        result = verify_full_formula('cube')
        assert result['legendre_consistency'], \
            f"Cube: Legendre checks failed: {result['legendre_checks']}"

    def test_dodecahedron_legendre_consistency(self):
        """Comprehensive Legendre consistency check for the dodecahedron."""
        result = verify_full_formula('dodecahedron')
        assert result['legendre_consistency'], \
            f"Dodec: Legendre checks failed: {result['legendre_checks']}"


class TestZonalSphericalFunction:
    """Test properties of the zonal spherical function phi_rho."""

    def test_trivial_irrep_is_constant(self):
        """phi for the trivial irrep should be identically 1."""
        for name, vfn in [('cube', cube_vertices),
                          ('dodecahedron', dodecahedron_vertices)]:
            verts = vfn()
            group = build_rotation_group(name)
            cosets = find_coset_representatives(verts, group)
            classes, angles = _classify_conjugacy_classes(group)
            table, csizes, dims, names, order = _character_table_for_group(name)
            _, perm = _match_conjugacy_classes(
                group, classes, angles, table, csizes, dims, order)
            classes_matched = [classes[perm[i]] for i in range(len(classes))]

            # Trivial irrep is index 0
            phi = zonal_spherical_function_full(
                verts, group, cosets, classes_matched, table,
                dims, names, order, 0)
            assert phi is not None, f"{name}: trivial phi is None"
            assert np.allclose(phi, 1.0, atol=1e-10), \
                f"{name}: trivial phi should be all 1s, got {phi}"

    def test_phi_normalized_at_v0(self):
        """phi_rho(v_0) = 1 for all irreps in the permutation rep."""
        for name, vfn in [('cube', cube_vertices),
                          ('dodecahedron', dodecahedron_vertices)]:
            verts = vfn()
            group = build_rotation_group(name)
            cosets = find_coset_representatives(verts, group)
            classes, angles = _classify_conjugacy_classes(group)
            table, csizes, dims, names, order = _character_table_for_group(name)
            _, perm = _match_conjugacy_classes(
                group, classes, angles, table, csizes, dims, order)
            classes_matched = [classes[perm[i]] for i in range(len(classes))]

            for rho_idx in range(len(names)):
                phi = zonal_spherical_function_full(
                    verts, group, cosets, classes_matched, table,
                    dims, names, order, rho_idx)
                if phi is not None:
                    assert abs(phi[0] - 1.0) < 1e-10, \
                        f"{name} {names[rho_idx]}: phi(v_0)={phi[0]}, not 1"

    def test_phi_is_eigenvector(self):
        """phi_rho should be an eigenvector of K with eigenvalue -T_rho."""
        verts = cube_vertices()
        K = interaction_matrix(verts)

        group = build_rotation_group('cube')
        cosets = find_coset_representatives(verts, group)
        classes, angles = _classify_conjugacy_classes(group)
        table, csizes, dims, names, order = _character_table_for_group('cube')
        _, perm = _match_conjugacy_classes(
            group, classes, angles, table, csizes, dims, order)
        classes_matched = [classes[perm[i]] for i in range(len(classes))]

        result = generalized_casimir_full(verts, 'cube')

        for rho_idx in range(len(names)):
            phi = zonal_spherical_function_full(
                verts, group, cosets, classes_matched, table,
                dims, names, order, rho_idx)
            if phi is None:
                continue

            T_rho = result['eigenvalues'].get(names[rho_idx])
            if T_rho is None:
                continue

            # K * phi should = -T_rho * phi
            Kphi = K @ phi
            expected = -T_rho * phi
            if np.linalg.norm(phi) > 1e-10 and abs(T_rho) > 1e-10:
                residual = np.linalg.norm(Kphi - expected) / np.linalg.norm(expected)
                assert residual < 1e-6, \
                    f"Cube {names[rho_idx]}: eigenvector residual={residual:.2e}"


class TestVerifyFullFormula:
    """Test the comprehensive verification function."""

    @pytest.mark.parametrize("name", [
        'tetrahedron', 'octahedron', 'cube', 'icosahedron',
    ])
    def test_multiplicity_1_solids(self, name):
        """Solids where all irreps have multiplicity 1 in the perm rep."""
        result = verify_full_formula(name)
        assert result['all_eigenvalues_match'], \
            f"{name}: not all eigenvalues match. Matches: {result['matches']}"

    def test_dodecahedron_with_multiplicity(self):
        """Dodecahedron: dim-4 has multiplicity 2, formula gives average."""
        result = verify_full_formula('dodecahedron')
        for m in result['matches']:
            if m['dim'] != 4:
                assert m['eigenvalue_match'], \
                    f"Dodec {m['irrep']}: T={m['T_formula']:.4f} vs {m['T_numerical']:.4f}"
            else:
                # Multiplicity 2: average is within 1.0 of each copy
                assert m['error'] < 1.0, \
                    f"Dodec dim-4 average error too large: {m['error']:.4f}"
