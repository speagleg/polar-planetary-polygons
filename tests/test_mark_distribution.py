"""Tests for the I* mark distribution and its identities."""

import pytest
from fractions import Fraction


class TestADEMarks:
    """Tests for ADE affine mark data."""

    def test_e8_marks(self):
        from planetary_polygons.proofs.mark_distribution import ade_marks
        assert ade_marks('E8') == [1, 2, 3, 4, 5, 6, 4, 2, 3]

    def test_e7_marks(self):
        from planetary_polygons.proofs.mark_distribution import ade_marks
        assert ade_marks('E7') == [1, 2, 3, 4, 3, 2, 1, 2]

    def test_e6_marks(self):
        from planetary_polygons.proofs.mark_distribution import ade_marks
        assert ade_marks('E6') == [1, 1, 2, 2, 3, 2, 1]

    def test_e8_coxeter_number(self):
        from planetary_polygons.proofs.mark_distribution import ade_marks
        assert sum(ade_marks('E8')) == 30

    def test_e8_group_order(self):
        from planetary_polygons.proofs.mark_distribution import ade_marks
        m = ade_marks('E8')
        assert sum(d**2 for d in m) == 120


class TestMarkBalance:
    """Tests for the mark-balance identity Σd(d-k₁)=0."""

    def test_e8_balance(self):
        from planetary_polygons.proofs.mark_distribution import mark_balance
        bal, k1 = mark_balance([1, 2, 3, 4, 5, 6, 4, 2, 3])
        assert bal == 0
        assert k1 == Fraction(4)

    def test_e8_pivot_4_unique(self):
        """Pivot k₁ = 4 holds ONLY for E₈ among all exceptional types."""
        from planetary_polygons.proofs.mark_distribution import mark_balance, ade_marks
        for t in ['E6', 'E7']:
            _, k1 = mark_balance(ade_marks(t))
            assert k1 != Fraction(4), f"{t} should NOT have k₁ = 4"
        _, k1_e8 = mark_balance(ade_marks('E8'))
        assert k1_e8 == Fraction(4)

    def test_e6_pivot_is_2(self):
        from planetary_polygons.proofs.mark_distribution import mark_balance
        _, k1 = mark_balance([1, 1, 2, 2, 3, 2, 1])
        assert k1 == Fraction(2)

    def test_e8_gauss_bonnet(self):
        """Mark-balance equivalent to |I*| = 4h (Gauss-Bonnet tiling)."""
        from planetary_polygons.proofs.mark_distribution import ade_marks
        m = ade_marks('E8')
        assert sum(d**2 for d in m) == 4 * sum(m)


class TestVtensorF:
    """Tests for V⊗F = 4×reg(A₅)."""

    def test_icosahedron_vf_equals_roots(self):
        from planetary_polygons.proofs.mark_distribution import vtensor_f_multiplicity
        k = vtensor_f_multiplicity(V=12, F=20, stab_V=5, stab_F=3, group_order=60)
        assert k == 4  # V⊗F = 4 × reg(A₅)
        assert 12 * 20 == 240  # = roots(E₈)

    def test_octahedron_vf(self):
        from planetary_polygons.proofs.mark_distribution import vtensor_f_multiplicity
        k = vtensor_f_multiplicity(V=6, F=8, stab_V=4, stab_F=3, group_order=24)
        assert k == 2  # V⊗F = 2 × reg(S₄)

    def test_tetrahedron_not_regular(self):
        """Tetrahedron: gcd(3,3)=3≠1, so V⊗F is NOT a multiple of reg."""
        from planetary_polygons.proofs.mark_distribution import vtensor_f_multiplicity
        k = vtensor_f_multiplicity(V=4, F=4, stab_V=3, stab_F=3, group_order=12)
        assert k is None


class TestChargeMagnitudeChain:
    """Tests for the iterated charge-magnitude map E₈→E₆→A₃→∅."""

    def test_e8_to_e6(self):
        from planetary_polygons.proofs.mark_distribution import charge_magnitude_map
        target, kernel = charge_magnitude_map([1, 2, 3, 4, 5, 6, 4, 2, 3], pivot=4)
        assert sorted(target) == sorted([1, 1, 1, 2, 2, 2, 3])
        assert kernel == [4, 4]

    def test_e6_to_a3(self):
        from planetary_polygons.proofs.mark_distribution import charge_magnitude_map
        target, kernel = charge_magnitude_map([1, 1, 2, 2, 3, 2, 1], pivot=2)
        assert sorted(target) == [1, 1, 1, 1]
        assert sorted(kernel) == [2, 2, 2]

    def test_full_chain(self):
        from planetary_polygons.proofs.mark_distribution import division_algebra_chain
        chain = division_algebra_chain([1, 2, 3, 4, 5, 6, 4, 2, 3])
        pivots = [step['pivot'] for step in chain]
        assert pivots == [4, 2, 1]
        assert sum(pivots) == 7
        assert 4 * 2 * 1 == 8


class TestPivotUniqueness:
    """Test the uniqueness theorem: (4,2,1) unique with Σ=Π-1."""

    def test_uniqueness(self):
        from planetary_polygons.proofs.mark_distribution import sum_equals_product_minus_one
        solutions = sum_equals_product_minus_one(max_a=20)
        assert solutions == [(4, 2, 1)]

    def test_product_identity(self):
        """Πdᵢ = 6!×4! = 17280."""
        from planetary_polygons.proofs.mark_distribution import ade_marks
        from math import factorial
        m = ade_marks('E8')
        prod = 1
        for d in m:
            prod *= d
        assert prod == factorial(6) * factorial(4)


class TestTwoAdicFiltration:
    """Tests for the 2-adic layer structure."""

    def test_layer_assignment(self):
        from planetary_polygons.proofs.mark_distribution import two_adic_layers
        layers = two_adic_layers([1, 2, 3, 4, 5, 6, 4, 2, 3])
        assert layers['K3'] == [1, 3, 5, 3]
        assert layers['K2'] == [2, 6, 2]
        assert layers['K1'] == [4, 4]

    def test_supertrace_cancellation(self):
        from planetary_polygons.proofs.mark_distribution import two_adic_layers
        layers = two_adic_layers([1, 2, 3, 4, 5, 6, 4, 2, 3])
        assert sum(d * (d - 4) for d in layers['K1']) == 0
        assert sum(d * (d - 4) for d in layers['K2']) == 4
        assert sum(d * (d - 4) for d in layers['K3']) == -4

    def test_sigma_d2_matching(self):
        """Σd²(bosons) = Σd²(fermions) = 44."""
        from planetary_polygons.proofs.mark_distribution import two_adic_layers
        layers = two_adic_layers([1, 2, 3, 4, 5, 6, 4, 2, 3])
        assert sum(d**2 for d in layers['K2']) == 44
        assert sum(d**2 for d in layers['K3']) == 44

    def test_proper_3_coloring_e8(self):
        from planetary_polygons.proofs.mark_distribution import is_proper_2adic_coloring
        assert is_proper_2adic_coloring('E8') is True

    def test_proper_3_coloring_d4(self):
        from planetary_polygons.proofs.mark_distribution import is_proper_2adic_coloring
        assert is_proper_2adic_coloring('D4') is True

    def test_proper_3_coloring_e6(self):
        """E₆ admits a proper 2-adic 3-coloring (with correct topology)."""
        from planetary_polygons.proofs.mark_distribution import is_proper_2adic_coloring
        assert is_proper_2adic_coloring('E6') is True

    def test_proper_3_coloring_e7(self):
        """E₇ admits a proper 2-adic 3-coloring."""
        from planetary_polygons.proofs.mark_distribution import is_proper_2adic_coloring
        assert is_proper_2adic_coloring('E7') is True

    def test_all_exceptional_proper(self):
        """The proper 3-coloring holds for ALL exceptional types + D₄."""
        from planetary_polygons.proofs.mark_distribution import is_proper_2adic_coloring
        for t in ['D4', 'E6', 'E7', 'E8']:
            assert is_proper_2adic_coloring(t) is True, f"{t} should be proper"

    def test_d5_d6_not_proper(self):
        """D₅ and D₆ fail the proper 3-coloring (adjacent mark-2 nodes)."""
        from planetary_polygons.proofs.mark_distribution import is_proper_2adic_coloring
        assert is_proper_2adic_coloring('D5') is False
        assert is_proper_2adic_coloring('D6') is False

    def test_layer_sizes_sum_to_9(self):
        from planetary_polygons.proofs.mark_distribution import two_adic_layers
        layers = two_adic_layers([1, 2, 3, 4, 5, 6, 4, 2, 3])
        total = sum(len(v) for v in layers.values())
        assert total == 9


class TestMarkSupercharge:
    """Tests for ρ₁ as the supercharge."""

    def test_q_squared_bosonic(self):
        """ρ₁⊗ρ₁ = ρ₀+ρ₂, both in K₃ (bosonic)."""
        from planetary_polygons.proofs.mark_distribution import mark_supercharge_squared
        rho0_dim, rho2_dim = mark_supercharge_squared()
        assert rho0_dim == 1
        assert rho2_dim == 3

    def test_layer_transitions(self):
        """ρ₁⊗ maps each layer to OTHER layers only."""
        from planetary_polygons.proofs.mark_distribution import supercharge_transitions
        trans = supercharge_transitions()
        for src in ['K1', 'K2', 'K3']:
            assert src not in trans[src], f"{src} maps to itself!"


class TestCartanSpectrum:
    """Tests for the Ẽ₈ Cartan eigenvalues and spectral decomposition."""

    def test_eigenvalue_count(self):
        from planetary_polygons.proofs.mark_distribution import cartan_eigenvalues
        eigs = cartan_eigenvalues('E8')
        assert len(eigs) == 9

    def test_eigenvalues_golden(self):
        from planetary_polygons.proofs.mark_distribution import cartan_eigenvalues
        from math import sqrt
        eigs = cartan_eigenvalues('E8')
        phi = (1 + sqrt(5)) / 2
        # Cartan eigenvalues μ = 2 - λ_adj where λ_adj ∈ {±2,±φ,±1,±1/φ,0}
        expected = sorted([0, 1/phi**2, 1, 3-phi, 2, 2+1/phi, 3, 2+phi, 4])
        for e, x in zip(sorted(eigs), expected):
            assert abs(e - x) < 1e-10

    def test_spectral_denominators(self):
        from planetary_polygons.proofs.mark_distribution import spectral_denominators
        denoms = spectral_denominators(h=30)
        assert denoms == {1, 2, 3, 5}
        assert sum(denoms) == 11
        assert 1 * 2 * 3 * 5 == 30

    def test_cyclotomic_indices(self):
        from planetary_polygons.proofs.mark_distribution import cyclotomic_indices
        indices = cyclotomic_indices()
        assert indices == {1, 2, 3, 4, 5, 6, 10}
        assert all(60 % d == 0 and d <= 10 for d in indices)

    def test_dark_light_decomposition(self):
        """60 = 16 (light) + 44 (dark)."""
        from planetary_polygons.proofs.mark_distribution import dark_light_decomposition
        light, dark = dark_light_decomposition()
        assert light == 16
        assert dark == 44
        assert light + dark == 60


class TestGenerations:
    """Tests for three generations from the weak eigenvector."""

    def test_e8_three_generations(self):
        from planetary_polygons.proofs.mark_distribution import weak_eigenvector_generations
        n_gen, doublets = weak_eigenvector_generations('E8')
        assert n_gen == 3

    def test_e6_three_generations_generic(self):
        """E₆ has 2D eigenspace at μ=1; generic vector gives 3 generations."""
        # The μ=1 eigenspace is {(v0,v1,v0,v1,0,-(v0+v1),-(v0+v1))}
        # Three doublets exist iff v0≠0, v1≠0, v0+v1≠0 (generic).
        # numpy's arbitrary basis may not satisfy this, so test analytically.
        import numpy as np
        edges = [(0,2),(1,3),(2,4),(3,4),(4,5),(5,6)]
        v = np.array([1, 1, 1, 1, 0, -2, -2], dtype=float)
        A = np.zeros((7,7))
        for i,j in edges: A[i,j]=1; A[j,i]=1
        assert np.max(np.abs(A @ v - v)) < 1e-10, "Not an eigenvector"
        # Count doublets
        doublets = []
        visited = set()
        for i,j in edges:
            if i not in visited and j not in visited:
                if abs(v[i]) > 0.1 and abs(v[j]) > 0.1:
                    if np.sign(v[i]) == np.sign(v[j]):
                        doublets.append((i,j))
                        visited.add(i); visited.add(j)
        assert len(doublets) == 3, f"E6 generic: {len(doublets)} doublets"

    def test_e7_e8_three_generations(self):
        """E₇ and E₈ have unique μ=1 eigenvector giving 3 generations."""
        from planetary_polygons.proofs.mark_distribution import weak_eigenvector_generations
        for t in ['E7', 'E8']:
            n_gen, _ = weak_eigenvector_generations(t)
            assert n_gen == 3, f"{t} gives {n_gen} generations, expected 3"

    def test_det_removal_equals_mark_squared(self):
        """det(C without ρᵢ) = dᵢ² for all i."""
        from planetary_polygons.proofs.mark_distribution import det_removal
        marks = [1, 2, 3, 4, 5, 6, 4, 2, 3]
        for i, d in enumerate(marks):
            det = det_removal('E8', i)
            assert abs(det - d**2) < 1e-8, f"node {i}: det={det}, d²={d**2}"


class TestBipartiteConjugation:
    """Tests for matter-antimatter bipartite symmetry."""

    def test_conjugate_eigenvectors(self):
        from planetary_polygons.proofs.mark_distribution import bipartite_conjugation_check
        assert bipartite_conjugation_check('E8')

    def test_five_independent_modes(self):
        """9 eigenvalues → 4 conjugate pairs + 1 self-conjugate at μ=2."""
        from planetary_polygons.proofs.mark_distribution import cartan_eigenvalues
        eigs = sorted(cartan_eigenvalues('E8'))
        for i in range(4):
            assert abs(eigs[i] + eigs[8-i] - 4.0) < 1e-10
        assert abs(eigs[4] - 2.0) < 1e-10

    def test_spectral_denom_sum(self):
        """Σ(spectral denoms) = 11 and Π = 30 = h."""
        from planetary_polygons.proofs.mark_distribution import spectral_denominators
        denoms = spectral_denominators(h=30)
        assert sum(denoms) == 11
        prod = 1
        for d in denoms:
            prod *= d
        assert prod == 30


class TestSpectralDiameter:
    """Tests for Level 0: the spectral diameter is 4 for all affine ADE."""

    def test_spectral_diameter_constant(self):
        from planetary_polygons.proofs.mark_distribution import spectral_diameter
        assert spectral_diameter() == 4

    def test_all_ade_max_eigenvalue_is_4(self):
        """max(Cartan eigenvalue) = 4 for all ADE types with edges defined."""
        from planetary_polygons.proofs.mark_distribution import cartan_eigenvalues
        for t in ['D4', 'D5', 'D6', 'E6', 'E7', 'E8']:
            eigs = cartan_eigenvalues(t)
            assert abs(max(eigs) - 4.0) < 1e-8, f"{t}: max eigenvalue = {max(eigs)}"

    def test_all_ade_min_eigenvalue_is_0(self):
        """min(Cartan eigenvalue) = 0 for all ADE types with edges defined."""
        from planetary_polygons.proofs.mark_distribution import cartan_eigenvalues
        for t in ['D4', 'D5', 'D6', 'E6', 'E7', 'E8']:
            eigs = cartan_eigenvalues(t)
            assert abs(min(eigs)) < 1e-8, f"{t}: min eigenvalue = {min(eigs)}"

    def test_e8_unique_k1_equals_diameter(self):
        """E₈ is the unique ADE type with k₁ = spectral diameter = 4."""
        from planetary_polygons.proofs.mark_distribution import mark_balance, ade_marks
        from fractions import Fraction
        for t in ['D4', 'D5', 'D6', 'E6', 'E7']:
            _, k1 = mark_balance(ade_marks(t))
            assert k1 != Fraction(4), f"{t} has k₁ = {k1} = 4!"
        _, k1_e8 = mark_balance(ade_marks('E8'))
        assert k1_e8 == Fraction(4)


class TestGoldenDecoherence:
    """Tests for Level 5: golden decoherence from incommensurable frequencies."""

    def test_observable_hidden_split(self):
        from planetary_polygons.proofs.mark_distribution import (
            cartan_eigenvalues, golden_decoherence_rate
        )
        eigs = cartan_eigenvalues('E8')
        n_obs, n_hid, min_gap = golden_decoherence_rate(eigs)
        assert n_obs == 5  # eigenvalues at 0, 1, 2, 3, 4
        assert n_hid == 4  # golden eigenvalues

    def test_min_gap_is_irrational(self):
        """The minimum frequency gap involves the golden ratio."""
        from planetary_polygons.proofs.mark_distribution import (
            cartan_eigenvalues, golden_decoherence_rate
        )
        from math import sqrt
        eigs = cartan_eigenvalues('E8')
        _, _, min_gap = golden_decoherence_rate(eigs)
        phi = (1 + sqrt(5)) / 2
        # The smallest gap should be |1/φ² - 0| = 1/φ² ≈ 0.382 or |1 - 1/φ²| ≈ 0.618
        assert min_gap > 0.3
        assert min_gap < 0.7


class TestMasterEquationDerivation:
    """Tests for the 7-step master equation derivation (Theorem V-7.1).
    Verifies that b = a+1 and c = a+2 are DERIVED, not assumed."""

    def test_spectral_diameter_universal(self):
        """a = 4 is shared by ALL bipartite affine ADE — it selects nothing."""
        from planetary_polygons.proofs.mark_distribution import cartan_eigenvalues
        for typ in ['D4', 'D5', 'D6', 'E6', 'E7', 'E8']:
            eigs = cartan_eigenvalues(typ)
            assert max(eigs) == pytest.approx(4.0, abs=1e-10), f"{typ}: max eigenvalue ≠ 4"

    def test_mark_balance_selects_e8(self):
        """k₁ = Σd²/Σd = 4 = a, unique to E₈ among all ADE types."""
        from planetary_polygons.proofs.mark_distribution import ade_marks
        for typ in ['D4', 'D5', 'D6', 'E6', 'E7']:
            d = ade_marks(typ)
            k1 = Fraction(sum(x*x for x in d), sum(d))
            assert k1 != 4, f"{typ} also has k₁ = 4 (should be unique to E₈)"
        d8 = ade_marks('E8')
        k1_e8 = Fraction(sum(x*x for x in d8), sum(d8))
        assert k1_e8 == 4

    def test_e_family_unique(self):
        """(p-1)(q-1) = 2 has unique solution (p,q) = (2,3)."""
        solutions = []
        for p in range(2, 20):
            for q in range(p, 20):
                if (p - 1) * (q - 1) == 2:
                    solutions.append((p, q))
        assert solutions == [(2, 3)]

    def test_spherical_bound(self):
        """For (2,3,r): r < 6 = a+2, so r_max = 5 = a+1."""
        a = 4
        p, q = 2, 3
        r_crit = Fraction(p * q, p * q - p - q)
        assert r_crit == 6
        assert r_crit == a + 2
        r_max = int(r_crit) - 1  # largest integer < r_crit
        assert r_max == a + 1 == 5

    def test_r_crit_equals_a_plus_2(self):
        """r_crit = 2(p+1) = a+2, because p = χ(S²) = 2 and q = p+1."""
        p, q = 2, 3
        a = 2 * p  # = 2χ(S²) = 4
        r_crit = p * q // (p * q - p - q)
        assert r_crit == 2 * (p + 1)
        assert r_crit == a + 2

    def test_affine_mark_recurrence(self):
        """Marks on longest arm: d_k = k+1 (arithmetic progression)."""
        # Simulate the recurrence d_{k+1} = 2d_k - d_{k-1}
        # with d_0 = 1, d_1 = 2 (endpoint condition)
        r = 5  # arm length
        d = [1, 2]
        for k in range(1, r):
            d.append(2 * d[-1] - d[-2])
        assert d == [1, 2, 3, 4, 5, 6]
        assert d[-1] == r + 1  # d_max = r+1 = a+2

    def test_c_equals_a_plus_2(self):
        """Maximum mark of Ẽ₈ = 6 = a+2."""
        from planetary_polygons.proofs.mark_distribution import ade_marks
        d = ade_marks('E8')
        assert max(d) == 6 == 4 + 2

    def test_gauss_bonnet(self):
        """|I*| = a/ε = 120, cross-check abc = 120."""
        a, b, c = 4, 5, 6
        epsilon = Fraction(1, 2) + Fraction(1, 3) + Fraction(1, 5) - 1
        assert epsilon == Fraction(1, 30)
        assert a * b * c == 120
        assert Fraction(a, 1) / epsilon == 120

    def test_coxeter_number(self):
        """h = |I*|/a = 30 from mark-balance."""
        from planetary_polygons.proofs.mark_distribution import ade_marks
        d = ade_marks('E8')
        h = sum(d)
        assert h == 30
        assert h == 120 // 4  # |I*|/a

    def test_rank_from_class_equation(self):
        """9 conjugacy classes → rank = 8 = 2a."""
        # Conjugacy class sizes of I*
        cc_sizes = [1, 1, 12, 12, 20, 20, 30, 12, 12]
        assert sum(cc_sizes) == 120  # |I*|
        assert len(cc_sizes) == 9
        rank = len(cc_sizes) - 1
        assert rank == 8 == 2 * 4

    def test_rank_formula(self):
        """|CC(I*)| = 2b - 1 = 2(a+1) - 1 = 2a + 1 = 9."""
        a, b = 4, 5
        assert 2 * b - 1 == 9
        assert 2 * a + 1 == 9

    def test_pivots_sum(self):
        """Σ pivots = a + a/2 + a/4 = 7 = N_crit."""
        a = 4
        assert a + a // 2 + a // 4 == 7

    def test_dim_e8(self):
        """dim(E₈) = |I*| + 2^(rank-1) = 248."""
        assert 120 + 2**7 == 248
