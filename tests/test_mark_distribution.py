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

    def test_proper_3_coloring_e7(self):
        """E₇ also admits a proper 2-adic 3-coloring."""
        from planetary_polygons.proofs.mark_distribution import is_proper_2adic_coloring
        assert is_proper_2adic_coloring('E7') is True

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

    def test_e6_two_generations(self):
        from planetary_polygons.proofs.mark_distribution import weak_eigenvector_generations
        n_gen, _ = weak_eigenvector_generations('E6')
        assert n_gen == 2

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

    def test_n_crit_from_spectral(self):
        """N_crit = Σ(spectral denoms) - dim(spacetime) = 11 - 4 = 7."""
        from planetary_polygons.proofs.mark_distribution import spectral_denominators
        assert sum(spectral_denominators(h=30)) - 4 == 7
