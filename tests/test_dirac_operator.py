"""
Tests for the Clifford module and Koszul complex (Dirac operator).

Verifies three levels of structure:

Level 1 (Mode-level):
    - Havelock eigenvalue signs
    - Index = number of negative modes = N-5 for N >= 8
    - Index = 0 for N <= 6
    - N=7 degenerate case

Level 2 (Clifford/Spinor):
    - Clifford relations: {gamma^a, gamma^b} = 2 delta_{ab}
    - Chirality: Gamma^2 = I, {Gamma, gamma^a} = 0
    - Number operators: J_k^2 = 1/4, [J_j, J_k] = 0, eigenvalues +/-1/2
    - Higgs field spectrum matches binary-string eigenvalues
    - Z_N equivariance: [R, Phi] = 0

Level 3 (Koszul complex):
    - Dimensions C(n_neg, k) for k = 0, ..., n_neg
    - Euler characteristic = 0 for n_neg >= 1
    - Acyclicity for N != 7

Cross-checks:
    - Index = Morse index
    - Index = Euler class degree
    - Consistency across all N = 3, ..., 14
"""

import pytest
import math
import itertools
from fractions import Fraction

from planetary_polygons.proofs.dirac_operator import (
    havelock_eigenvalue,
    normal_eigenvalues,
    negative_modes,
    zero_modes,
    positive_modes,
    mode_index,
    build_gamma_matrices,
    verify_clifford_relations,
    build_chirality,
    verify_chirality,
    build_number_operators,
    verify_number_operators,
    build_higgs_field,
    higgs_field_spectrum,
    binary_string_eigenvalue,
    binary_string_chirality,
    spinor_spectrum,
    koszul_dimensions,
    koszul_euler_characteristic,
    koszul_acyclicity,
    compute_index,
    expected_index,
    build_zn_generator,
    verify_zn_equivariance,
    verify_higgs_spectrum,
    n7_degenerate_analysis,
    cross_check_all,
    index_table,
    HAS_NUMPY,
)

requires_numpy = pytest.mark.skipif(
    not HAS_NUMPY, reason="numpy not available"
)


# ============================================================
# Level 1: Mode-level index = N - 5
# ============================================================

class TestModeIndex:
    """The core claim: index = number of negative Havelock modes = N-5."""

    @pytest.mark.parametrize("N", [3, 4, 5, 6])
    def test_no_negative_modes_stable(self, N):
        """N <= 6: all eigenvalues positive, index = 0."""
        assert mode_index(N) == 0
        assert negative_modes(N) == []

    def test_n7_no_negative_modes(self):
        """N=7: zero modes m=3,4 but no negative modes, index = 0."""
        assert mode_index(7) == 0
        assert negative_modes(7) == []
        assert zero_modes(7) == [3, 4]

    @pytest.mark.parametrize("N", range(8, 26))
    def test_index_equals_N_minus_5(self, N):
        """For N >= 8: index = N - 5."""
        assert mode_index(N) == N - 5

    def test_n8_explicit(self):
        """N=8: negative modes {3,4,5}, index = 3."""
        assert negative_modes(8) == [3, 4, 5]
        assert mode_index(8) == 3

    def test_n10_explicit(self):
        """N=10: negative modes {3,4,5,6,7}, index = 5."""
        assert negative_modes(10) == [3, 4, 5, 6, 7]
        assert mode_index(10) == 5

    @pytest.mark.parametrize("N", range(3, 26))
    def test_index_matches_expected_formula(self, N):
        """mode_index(N) agrees with the closed-form expected_index(N)."""
        assert mode_index(N) == expected_index(N)

    @pytest.mark.parametrize("N", range(8, 26))
    def test_negative_modes_contiguous(self, N):
        """For N >= 8, S^- = {3, 4, ..., N-3} (contiguous block)."""
        expected = list(range(3, N - 2))
        assert negative_modes(N) == expected

    @pytest.mark.parametrize("N", range(3, 26))
    def test_mode_count_consistent(self, N):
        """n_pos + n_neg + n_zero = N - 2 (total number of modes)."""
        assert (len(positive_modes(N)) + len(negative_modes(N))
                + len(zero_modes(N))) == N - 2


class TestExpectedIndex:
    """Verify the expected index formula."""

    @pytest.mark.parametrize("N", [3, 4, 5, 6, 7])
    def test_small_N_zero(self, N):
        assert expected_index(N) == 0

    @pytest.mark.parametrize("N", range(8, 20))
    def test_large_N(self, N):
        assert expected_index(N) == N - 5


# ============================================================
# Level 2: Clifford algebra {gamma^a, gamma^b} = 2 delta_{ab}
# ============================================================

class TestCliffordAlgebra:
    """Verify the Clifford algebra construction."""

    @requires_numpy
    @pytest.mark.parametrize("d", [1, 2, 3, 4, 5, 6])
    def test_anticommutation_relations(self, d):
        """gamma^a gamma^b + gamma^b gamma^a = 2 delta_{ab} I."""
        gammas = build_gamma_matrices(d)
        result = verify_clifford_relations(gammas)
        assert result['passed'], (
            f"d={d}: max dev = {result['max_deviation']:.2e}"
        )

    @requires_numpy
    @pytest.mark.parametrize("d", [1, 2, 3, 4, 5, 6])
    def test_correct_count_and_size(self, d):
        """2d gamma matrices of size 2^d x 2^d."""
        gammas = build_gamma_matrices(d)
        assert len(gammas) == 2 * d
        expected_size = 2 ** d
        for g in gammas:
            assert g.shape == (expected_size, expected_size)

    @requires_numpy
    @pytest.mark.parametrize("d", [1, 2, 3, 4, 5, 6])
    def test_hermiticity(self, d):
        """Each gamma matrix is Hermitian."""
        import numpy as np
        gammas = build_gamma_matrices(d)
        for i, g in enumerate(gammas):
            dev = np.max(np.abs(g - g.conj().T))
            assert dev < 1e-14, (
                f"d={d}, gamma[{i}] not Hermitian, dev = {dev:.2e}"
            )

    @requires_numpy
    def test_N4_clifford(self):
        """N=4 (d=2): 4 gammas of size 4x4."""
        gammas = build_gamma_matrices(2)
        assert len(gammas) == 4
        assert gammas[0].shape == (4, 4)
        assert verify_clifford_relations(gammas)['passed']

    @requires_numpy
    def test_N5_clifford(self):
        """N=5 (d=3): 6 gammas of size 8x8."""
        gammas = build_gamma_matrices(3)
        assert len(gammas) == 6
        assert gammas[0].shape == (8, 8)
        assert verify_clifford_relations(gammas)['passed']

    @requires_numpy
    def test_N8_clifford(self):
        """N=8 (d=6): 12 gammas of size 64x64."""
        gammas = build_gamma_matrices(6)
        assert len(gammas) == 12
        assert gammas[0].shape == (64, 64)
        assert verify_clifford_relations(gammas)['passed']


# ============================================================
# Chirality operator
# ============================================================

class TestChirality:
    """Verify the chirality operator Gamma."""

    @requires_numpy
    @pytest.mark.parametrize("d", [1, 2, 3, 4, 5, 6])
    def test_gamma_squared_is_identity(self, d):
        """Gamma^2 = I."""
        gammas = build_gamma_matrices(d)
        chirality = build_chirality(gammas, d)
        result = verify_chirality(chirality, gammas)
        assert result['sq_deviation'] < 1e-12

    @requires_numpy
    @pytest.mark.parametrize("d", [1, 2, 3, 4, 5, 6])
    def test_anticommutes_with_gammas(self, d):
        """{Gamma, gamma^a} = 0 for all a."""
        gammas = build_gamma_matrices(d)
        chirality = build_chirality(gammas, d)
        result = verify_chirality(chirality, gammas)
        assert result['max_anticomm_deviation'] < 1e-12

    @requires_numpy
    @pytest.mark.parametrize("d", [1, 2, 3, 4, 5, 6])
    def test_hermitian(self, d):
        """Gamma is Hermitian."""
        gammas = build_gamma_matrices(d)
        chirality = build_chirality(gammas, d)
        result = verify_chirality(chirality, gammas)
        assert result['hermiticity_deviation'] < 1e-12

    @requires_numpy
    @pytest.mark.parametrize("d", [1, 2, 3, 4, 5, 6])
    def test_equal_chirality_split(self, d):
        """dim(S+) = dim(S-) = 2^{d-1}."""
        gammas = build_gamma_matrices(d)
        chirality = build_chirality(gammas, d)
        result = verify_chirality(chirality, gammas)
        assert result['equal_split']
        assert result['n_plus'] == 2 ** (d - 1)
        assert result['n_minus'] == 2 ** (d - 1)


# ============================================================
# Number operators J_m
# ============================================================

class TestNumberOperators:
    """Verify the complex structure / number operators J_m."""

    @requires_numpy
    @pytest.mark.parametrize("d", [1, 2, 3, 4, 5, 6])
    def test_J_squared(self, d):
        """J_k^2 = (1/4) I for all k."""
        gammas = build_gamma_matrices(d)
        J_ops = build_number_operators(gammas, d)
        result = verify_number_operators(J_ops)
        assert result['max_sq_deviation'] < 1e-12

    @requires_numpy
    @pytest.mark.parametrize("d", [1, 2, 3, 4, 5, 6])
    def test_J_commute(self, d):
        """[J_j, J_k] = 0 for j != k."""
        gammas = build_gamma_matrices(d)
        J_ops = build_number_operators(gammas, d)
        result = verify_number_operators(J_ops)
        assert result['max_commutativity_deviation'] < 1e-12

    @requires_numpy
    @pytest.mark.parametrize("d", [1, 2, 3, 4, 5, 6])
    def test_J_hermitian(self, d):
        """Each J_k is Hermitian."""
        gammas = build_gamma_matrices(d)
        J_ops = build_number_operators(gammas, d)
        result = verify_number_operators(J_ops)
        assert result['max_hermiticity_deviation'] < 1e-12

    @requires_numpy
    @pytest.mark.parametrize("d", [1, 2, 3, 4, 5, 6])
    def test_J_eigenvalues_pm_half(self, d):
        """Each J_k has eigenvalues +/- 1/2 only."""
        gammas = build_gamma_matrices(d)
        J_ops = build_number_operators(gammas, d)
        result = verify_number_operators(J_ops)
        assert result['eigenvalue_check']

    @requires_numpy
    def test_correct_number_of_operators(self):
        """d number operators for d complex dimensions."""
        for d in [1, 2, 3, 4, 5, 6]:
            gammas = build_gamma_matrices(d)
            J_ops = build_number_operators(gammas, d)
            assert len(J_ops) == d


# ============================================================
# Higgs field: spectrum matches binary strings
# ============================================================

class TestHiggsField:
    """Verify the Havelock Higgs field Phi = sum lambda_m J_m."""

    @requires_numpy
    @pytest.mark.parametrize("N", [4, 5, 6, 7, 8])
    def test_higgs_hermitian(self, N):
        """Phi is Hermitian."""
        import numpy as np
        d = N - 2
        gammas = build_gamma_matrices(d)
        J_ops = build_number_operators(gammas, d)
        Phi = build_higgs_field(N, J_ops)
        dev = np.max(np.abs(Phi - Phi.conj().T))
        assert dev < 1e-12

    @requires_numpy
    @pytest.mark.parametrize("N", [4, 5, 6, 8])
    def test_spectrum_matches_binary_strings(self, N):
        """Matrix eigenvalues of Phi match binary-string eigenvalues."""
        result = verify_higgs_spectrum(N)
        assert result['matches'], (
            f"N={N}: max dev = {result['max_deviation']:.2e}"
        )

    @requires_numpy
    @pytest.mark.parametrize("N", [4, 5, 6, 8])
    def test_higgs_commutes_with_J(self, N):
        """[Phi, J_k] = 0 for all k (simultaneous diagonalisation)."""
        import numpy as np
        d = N - 2
        gammas = build_gamma_matrices(d)
        J_ops = build_number_operators(gammas, d)
        Phi = build_higgs_field(N, J_ops)

        for k, J in enumerate(J_ops):
            comm = Phi @ J - J @ Phi
            dev = np.max(np.abs(comm))
            assert dev < 1e-12, f"N={N}: [Phi, J_{k}] != 0"


# ============================================================
# Spinor spectrum
# ============================================================

class TestSpinorSpectrum:
    """Spectral decomposition of Phi on the spinor space."""

    @pytest.mark.parametrize("N", [3, 4, 5, 6, 8])
    def test_total_count(self, N):
        """Total eigenvalue count = 2^d."""
        sp = spinor_spectrum(N)
        total = (sp.pos_in_S_plus + sp.neg_in_S_plus + sp.zero_in_S_plus
                 + sp.pos_in_S_minus + sp.neg_in_S_minus + sp.zero_in_S_minus)
        assert total == sp.spinor_dim

    @pytest.mark.parametrize("N", [3, 4, 5, 6, 8])
    def test_chirality_split(self, N):
        """S+ and S- each have dimension 2^{d-1}."""
        sp = spinor_spectrum(N)
        assert sp.dim_S_plus == 2 ** (sp.d - 1)
        assert sp.dim_S_minus == 2 ** (sp.d - 1)

    @pytest.mark.parametrize("N", [3, 4, 5, 6, 8, 10])
    def test_dimensions_correct(self, N):
        """dim(S+) + dim(S-) = 2^d."""
        sp = spinor_spectrum(N)
        assert sp.dim_S_plus + sp.dim_S_minus == sp.spinor_dim


# ============================================================
# Binary-string eigenvalue and chirality
# ============================================================

class TestBinaryStringBasis:
    """Test the binary-string basis functions directly."""

    def test_eigenvalue_N3(self):
        """N=3, d=1: one mode m=2 with lambda=1."""
        assert binary_string_eigenvalue((1,), 3) == Fraction(1, 2)
        assert binary_string_eigenvalue((-1,), 3) == Fraction(-1, 2)

    def test_eigenvalue_N4(self):
        """N=4, d=2: modes m=2 (lambda=1), m=3 (lambda=3/2)."""
        # ev = lambda_2*s_2/2 + lambda_3*s_3/2 = 1*s_2/2 + (3/2)*s_3/2
        assert binary_string_eigenvalue((1, 1), 4) == Fraction(5, 4)
        assert binary_string_eigenvalue((1, -1), 4) == Fraction(-1, 4)
        assert binary_string_eigenvalue((-1, 1), 4) == Fraction(1, 4)
        assert binary_string_eigenvalue((-1, -1), 4) == Fraction(-5, 4)

    def test_eigenvalue_all_plus(self):
        """All-plus string: ev = sum(lambda_m) / 2."""
        for N in [3, 4, 5, 8]:
            d = N - 2
            all_plus = (1,) * d
            ev = binary_string_eigenvalue(all_plus, N)
            expected = sum(havelock_eigenvalue(m, N) for m in range(2, N)) / 2
            assert ev == expected

    def test_chirality_all_plus(self):
        """All-plus has chirality +1."""
        assert binary_string_chirality((1, 1, 1)) == 1

    def test_chirality_one_minus(self):
        """Single flip gives chirality -1."""
        assert binary_string_chirality((-1, 1, 1)) == -1

    def test_chirality_two_minus(self):
        """Two flips restore chirality +1."""
        assert binary_string_chirality((-1, -1, 1)) == 1

    def test_chirality_parity(self):
        """Chirality = (-1)^{number of -1 entries}."""
        for d in range(1, 6):
            for bits in itertools.product((1, -1), repeat=d):
                n_minus = sum(1 for s in bits if s == -1)
                expected = (-1) ** n_minus
                assert binary_string_chirality(bits) == expected


# ============================================================
# Level 3: Koszul complex
# ============================================================

class TestKoszulComplex:
    """Verify the Koszul complex of the negative mode subspace."""

    @pytest.mark.parametrize("N", [3, 4, 5, 6])
    def test_trivial_for_stable(self, N):
        """N <= 6: no negative modes, trivial complex [1]."""
        assert koszul_dimensions(N) == [1]

    @pytest.mark.parametrize("N", range(8, 15))
    def test_dimensions_are_binomial(self, N):
        """Lambda^k(V^-) has dimension C(n_neg, k)."""
        n_neg = mode_index(N)
        dims = koszul_dimensions(N)
        assert len(dims) == n_neg + 1
        for k in range(n_neg + 1):
            assert dims[k] == math.comb(n_neg, k)

    def test_N8_koszul_dims(self):
        """N=8: n_neg=3, dims = [1, 3, 3, 1]."""
        assert koszul_dimensions(8) == [1, 3, 3, 1]

    def test_N10_koszul_dims(self):
        """N=10: n_neg=5, dims = [1, 5, 10, 10, 5, 1]."""
        assert koszul_dimensions(10) == [1, 5, 10, 10, 5, 1]

    @pytest.mark.parametrize("N", [3, 4, 5, 6])
    def test_euler_char_trivial(self, N):
        """N <= 6: Euler characteristic = 1 (trivial complex)."""
        assert koszul_euler_characteristic(N) == 1

    @pytest.mark.parametrize("N", range(8, 15))
    def test_euler_char_zero(self, N):
        """For N >= 8: Euler characteristic = 0."""
        assert koszul_euler_characteristic(N) == 0

    @pytest.mark.parametrize("N", range(3, 15))
    def test_acyclicity(self, N):
        """Koszul complex is acyclic for N != 7."""
        if N == 7:
            return  # N=7 is special, tested separately
        result = koszul_acyclicity(N)
        assert result['is_acyclic']

    def test_koszul_total_dim(self):
        """Total dimension of Koszul complex = 2^{n_neg}."""
        for N in range(8, 15):
            n_neg = mode_index(N)
            dims = koszul_dimensions(N)
            assert sum(dims) == 2 ** n_neg


# ============================================================
# N=7 degenerate case
# ============================================================

class TestN7Degenerate:
    """N=7 has zero modes m=3,4; index = 0."""

    def test_index_zero(self):
        """Mode-level index is 0 for N=7."""
        assert mode_index(7) == 0

    def test_zero_modes_present(self):
        """N=7 has zero modes at m=3 and m=4."""
        assert zero_modes(7) == [3, 4]

    def test_no_negative_modes(self):
        """N=7 has no negative modes."""
        assert negative_modes(7) == []

    def test_detailed_analysis_index(self):
        """Detailed analysis confirms index = 0."""
        analysis = n7_degenerate_analysis()
        assert analysis['index'] == 0
        assert analysis['n_negative_modes'] == 0
        assert analysis['n_zero_modes'] == 2

    def test_mode_level_degenerate(self):
        """N=7 is degenerate at the mode level (zero Havelock eigenvalues)."""
        analysis = n7_degenerate_analysis()
        assert not analysis['mode_level_fredholm']

    def test_higgs_kernel_empty(self):
        """
        The Higgs field Phi has EMPTY kernel on the spinor space.

        Although lambda_3 = lambda_4 = 0 (Havelock zero modes), the
        remaining modes (lambda_2 = lambda_5 = 1, lambda_6 = 3) prevent
        any binary string from summing to zero:
            s_2 + s_5 + 3*s_6 = 0 has no solution with s_i in {+1,-1}.
        """
        analysis = n7_degenerate_analysis()
        assert analysis['kernel_size'] == 0
        assert analysis['spinor_kernel_empty']

    def test_higgs_kernel_balanced(self):
        """Kernel is equally distributed between S+ and S- (both 0)."""
        analysis = n7_degenerate_analysis()
        assert analysis['kernel_S_plus'] == analysis['kernel_S_minus']  # both 0


# ============================================================
# Z_N equivariance
# ============================================================

class TestZNEquivariance:
    """Verify [Z_N generator, Phi] = 0."""

    @requires_numpy
    @pytest.mark.parametrize("N", [5, 7, 8])
    def test_commutes_with_higgs(self, N):
        """[R, Phi] = 0."""
        result = verify_zn_equivariance(N)
        assert result['commutes'], (
            f"N={N}: ||[R, Phi]|| = {result['commutator_norm']:.2e}"
        )

    @requires_numpy
    @pytest.mark.parametrize("N", [5, 7, 8])
    def test_R_N_is_scalar_times_identity(self, N):
        """R^N is proportional to the identity."""
        result = verify_zn_equivariance(N)
        assert result['RN_is_identity'], (
            f"N={N}: R^N ~ I deviation = {result['RN_identity_deviation']:.2e}"
        )

    @requires_numpy
    @pytest.mark.parametrize("N", [4, 5, 6, 8, 10])
    def test_extended_equivariance(self, N):
        """Equivariance for extended range of N."""
        result = verify_zn_equivariance(N)
        assert result['passed']


# ============================================================
# Cross-checks: index vs Morse vs Euler class
# ============================================================

class TestCrossChecks:
    """Cross-check index against Morse index and Euler class degree."""

    @pytest.mark.parametrize("N", range(3, 15))
    def test_index_matches_expected(self, N):
        """Index matches the closed-form formula."""
        cc = cross_check_all(N)
        assert cc['index_matches_expected']

    @pytest.mark.parametrize("N", range(8, 15))
    def test_index_equals_morse(self, N):
        """For N >= 8: index = Morse index = N-5."""
        cc = cross_check_all(N)
        assert cc['mode_index'] == cc['morse_index'] == N - 5

    @pytest.mark.parametrize("N", range(8, 15))
    def test_index_equals_euler_degree(self, N):
        """For N >= 8: index = Euler class degree = N-5."""
        cc = cross_check_all(N)
        assert cc['mode_index'] == cc['euler_class_degree']

    @pytest.mark.parametrize("N", range(3, 15))
    def test_all_consistent(self, N):
        """All cross-checks pass simultaneously."""
        cc = cross_check_all(N)
        assert cc['all_consistent']


# ============================================================
# Matrix vs binary-string spectrum agreement
# ============================================================

class TestMethodAgreement:
    """Matrix Clifford construction matches binary-string computation."""

    @requires_numpy
    @pytest.mark.parametrize("N", [8, 10, 12])
    def test_spectrum_agreement(self, N):
        """Phi eigenvalues match binary-string predictions."""
        result = verify_higgs_spectrum(N)
        assert result['matches'], (
            f"N={N}: spectrum max dev = {result['max_deviation']:.2e}"
        )

    @requires_numpy
    @pytest.mark.parametrize("N", range(3, 11))
    def test_spectrum_agreement_extended(self, N):
        """Agreement across full range N=3,...,10."""
        result = verify_higgs_spectrum(N)
        assert result['matches']


# ============================================================
# compute_index integration
# ============================================================

class TestComputeIndex:
    """Integration test for the compute_index function."""

    @pytest.mark.parametrize("N", range(3, 15))
    def test_compute_index_result(self, N):
        """compute_index returns correct IndexResult."""
        result = compute_index(N)
        assert result.N == N
        assert result.d == N - 2
        assert result.index == expected_index(N)
        assert result.n_positive + result.n_negative + result.n_zero == N - 2

    @pytest.mark.parametrize("N", range(8, 15))
    def test_fredholm_for_N_ge_8(self, N):
        """N >= 8 is Fredholm (no zero modes)."""
        result = compute_index(N)
        assert result.is_fredholm

    def test_not_fredholm_N7(self):
        """N=7 is not Fredholm."""
        result = compute_index(7)
        assert not result.is_fredholm

    @pytest.mark.parametrize("N", [3, 4, 5, 6])
    def test_fredholm_stable(self, N):
        """N <= 6 is Fredholm (no zero modes)."""
        result = compute_index(N)
        assert result.is_fredholm

    def test_invalid_N(self):
        """N < 3 raises ValueError."""
        with pytest.raises(ValueError, match="N must be >= 3"):
            compute_index(2)


# ============================================================
# Explicit small-N cases
# ============================================================

class TestExplicitSmallN:
    """Detailed verification of small-N cases."""

    def test_N3(self):
        """N=3: d=1, one mode m=2, lambda=1, index=0."""
        result = compute_index(3)
        assert result.d == 1
        assert result.n_positive == 1
        assert result.n_negative == 0
        assert result.index == 0

    def test_N4(self):
        """N=4: d=2, modes m=2,3, both lambda=1, index=0."""
        result = compute_index(4)
        assert result.d == 2
        assert result.positive_modes == [2, 3]
        assert result.index == 0

    def test_N5(self):
        """N=5: d=3, all modes positive, index=0."""
        result = compute_index(5)
        assert result.d == 3
        assert result.index == 0
        assert all(havelock_eigenvalue(m, 5) > 0 for m in range(2, 5))

    def test_N8(self):
        """N=8: d=6, negative modes {3,4,5}, index=3."""
        result = compute_index(8)
        assert result.d == 6
        assert result.negative_modes == [3, 4, 5]
        assert result.positive_modes == [2, 6, 7]
        assert result.index == 3
        assert result.koszul_dims == [1, 3, 3, 1]


# ============================================================
# Dimension consistency
# ============================================================

class TestDimensions:
    """Verify dimension formulas."""

    @pytest.mark.parametrize("N", range(3, 15))
    def test_spinor_dim(self, N):
        """Spinor dimension = 2^{N-2}."""
        sp = spinor_spectrum(N)
        assert sp.spinor_dim == 2 ** (N - 2)

    @pytest.mark.parametrize("N", range(3, 13))
    def test_chirality_split_sum(self, N):
        """dim(S+) + dim(S-) = 2^d."""
        sp = spinor_spectrum(N)
        assert sp.dim_S_plus + sp.dim_S_minus == 2 ** sp.d

    @pytest.mark.parametrize("N", range(3, 13))
    def test_chirality_equal(self, N):
        """dim(S+) = dim(S-) = 2^{d-1}."""
        sp = spinor_spectrum(N)
        assert sp.dim_S_plus == sp.dim_S_minus == 2 ** (sp.d - 1)


# ============================================================
# Summary table
# ============================================================

class TestIndexTable:
    """Test the summary table generation."""

    def test_table_range(self):
        """Table covers N=3,...,14."""
        rows = index_table(14)
        assert len(rows) == 12
        assert rows[0]['N'] == 3
        assert rows[-1]['N'] == 14

    def test_table_all_match(self):
        """All entries match expected values."""
        for row in index_table(14):
            assert row['matches'], (
                f"N={row['N']}: index {row['index']} != "
                f"expected {row['expected']}"
            )

    def test_table_fredholm(self):
        """Fredholm status correct in table."""
        for row in index_table(14):
            N = row['N']
            if N == 7:
                assert not row['fredholm']
            else:
                assert row['fredholm']
