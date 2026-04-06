"""
Tests for the Atiyah-Singer index theorem: ind(D_N) = N - 5.

Verifies:
1. Negative mode count = N - 5 for N >= 8 (contiguous block {3,...,N-3})
2. Chern character is correct sum of roots of unity
3. Todd class computation
4. Index = Morse index cross-check
5. xi-independence (topological invariant)
6. Palindromic structure of S^-
7. K-theory splitting principle
8. The complete proof chain
"""

import pytest
import math
from fractions import Fraction

from planetary_polygons.proofs.index_theorem import (
    havelock_eigenvalue,
    negative_modes,
    negative_mode_count,
    verify_contiguous_block,
    chern_character_exact,
    chern_character_trace,
    chern_character_rank,
    todd_class_factor,
    todd_class_product,
    todd_class_at_identity,
    a_hat_contribution,
    xi_critical,
    xi_independence_proof,
    cross_check_morse_index,
    index_theorem_proof,
    index_theorem_table,
    verify_palindromic_structure,
    splitting_principle_decomposition,
)


# ============================================================
# Negative mode count = N - 5
# ============================================================

class TestNegativeModeCount:
    """The core claim: |S^-| = N - 5 for N >= 8."""

    @pytest.mark.parametrize("N", [3, 4, 5, 6])
    def test_no_negative_modes_stable(self, N):
        """N <= 6: all eigenvalues positive, no negative modes."""
        assert negative_mode_count(N) == 0
        assert negative_modes(N) == []

    def test_n7_no_negative_modes(self):
        """N = 7: zero modes m=3,4 but no negative modes."""
        assert negative_mode_count(7) == 0
        assert negative_modes(7) == []

    @pytest.mark.parametrize("N", range(8, 26))
    def test_count_equals_N_minus_5(self, N):
        """For N >= 8: |S^-| = N - 5."""
        assert negative_mode_count(N) == N - 5

    def test_n8_explicit(self):
        """N=8: S^- = {3, 4, 5}, count = 3."""
        assert negative_modes(8) == [3, 4, 5]
        assert negative_mode_count(8) == 3

    def test_n9_explicit(self):
        """N=9: S^- = {3, 4, 5, 6}, count = 4."""
        assert negative_modes(9) == [3, 4, 5, 6]
        assert negative_mode_count(9) == 4

    def test_n10_explicit(self):
        """N=10: S^- = {3, 4, 5, 6, 7}, count = 5."""
        assert negative_modes(10) == [3, 4, 5, 6, 7]
        assert negative_mode_count(10) == 5


class TestContiguousBlock:
    """Negative modes form the block {3, ..., N-3} for N >= 8."""

    @pytest.mark.parametrize("N", range(8, 26))
    def test_contiguous_block(self, N):
        """S^- = {3, 4, ..., N-3} for N >= 8."""
        result = verify_contiguous_block(N)
        assert result['is_contiguous'], (
            f"N={N}: got {result['negative_modes']}, "
            f"expected {result['expected_block']}"
        )

    @pytest.mark.parametrize("N", range(8, 26))
    def test_boundary_modes_positive(self, N):
        """Modes m=2 and m=N-2 are NON-negative (boundary of the block)."""
        assert havelock_eigenvalue(2, N) > 0
        assert havelock_eigenvalue(N - 2, N) > 0

    @pytest.mark.parametrize("N", range(8, 26))
    def test_interior_modes_negative(self, N):
        """All modes m in {3, ..., N-3} are strictly negative."""
        for m in range(3, N - 2):
            lam = havelock_eigenvalue(m, N)
            assert lam < 0, f"N={N}, m={m}: lambda = {lam} >= 0"

    @pytest.mark.parametrize("N", [3, 4, 5, 6, 7])
    def test_small_N_vacuous(self, N):
        """For N < 8, contiguous block check is vacuously true."""
        result = verify_contiguous_block(N)
        assert result['is_contiguous']


# ============================================================
# Chern character
# ============================================================

class TestChernCharacter:
    """Chern character ch(nu^-) in the representation ring R(Z_N)."""

    @pytest.mark.parametrize("N", range(8, 20))
    def test_chern_coefficients_are_indicator(self, N):
        """Chern character coefficients are 0 or 1 (distinct line bundles)."""
        coeffs = chern_character_exact(N)
        assert len(coeffs) == N
        for c in coeffs:
            assert c in (0, 1)

    @pytest.mark.parametrize("N", range(8, 20))
    def test_chern_support_equals_negative_modes(self, N):
        """Non-zero coefficients are exactly at the negative mode indices."""
        coeffs = chern_character_exact(N)
        support = [k for k, c in enumerate(coeffs) if c == 1]
        assert support == negative_modes(N)

    @pytest.mark.parametrize("N", range(8, 20))
    def test_chern_rank_equals_count(self, N):
        """ch(nu^-)(1) = sum of coefficients = |S^-| = N - 5."""
        assert chern_character_rank(N) == N - 5

    @pytest.mark.parametrize("N", [3, 4, 5, 6])
    def test_chern_trivial_for_stable(self, N):
        """ch(nu^-) = 0 for N <= 6 (no negative modes)."""
        coeffs = chern_character_exact(N)
        assert all(c == 0 for c in coeffs)
        assert chern_character_rank(N) == 0

    @pytest.mark.parametrize("N", range(8, 16))
    def test_chern_trace_is_sum_of_roots(self, N):
        """ch(nu^-)(omega) = sum_{m in S^-} omega^m, computed independently."""
        omega = complex(
            math.cos(2 * math.pi / N),
            math.sin(2 * math.pi / N)
        )
        expected = sum(omega ** m for m in negative_modes(N))
        actual = chern_character_trace(N)
        assert abs(actual - expected) < 1e-12, (
            f"N={N}: trace mismatch {actual} vs {expected}"
        )

    def test_n8_chern_trace(self):
        """N=8: ch(omega) = omega^3 + omega^4 + omega^5."""
        omega = complex(
            math.cos(2 * math.pi / 8),
            math.sin(2 * math.pi / 8)
        )
        expected = omega**3 + omega**4 + omega**5
        actual = chern_character_trace(8)
        assert abs(actual - expected) < 1e-12


# ============================================================
# Todd class
# ============================================================

class TestToddClass:
    """Equivariant Todd class Td(nu^-)."""

    @pytest.mark.parametrize("N", range(8, 16))
    def test_todd_factors_well_defined(self, N):
        """Each Todd factor (omega - omega^m)/(1 - omega^m) is finite."""
        for m in negative_modes(N):
            factor = todd_class_factor(m, N)
            assert math.isfinite(factor.real)
            assert math.isfinite(factor.imag)

    @pytest.mark.parametrize("N", range(8, 16))
    def test_todd_product_finite(self, N):
        """The full Todd class product is finite and non-zero."""
        td = todd_class_product(N)
        assert abs(td) > 1e-15, f"N={N}: Todd class vanishes"
        assert math.isfinite(td.real)
        assert math.isfinite(td.imag)

    @pytest.mark.parametrize("N", [3, 4, 5, 6])
    def test_todd_trivial_for_stable(self, N):
        """Td(nu^-) = 1 when S^- is empty."""
        td = todd_class_product(N)
        assert abs(td - 1.0) < 1e-12

    def test_todd_at_identity(self):
        """Td(nu^-)(1) = 1 for all N (formal evaluation)."""
        for N in range(3, 20):
            assert todd_class_at_identity(N) == 1

    @pytest.mark.parametrize("N", range(8, 16))
    def test_todd_product_consistency(self, N):
        """Todd product equals product of individual factors."""
        neg = negative_modes(N)
        product = complex(1.0, 0.0)
        for m in neg:
            product *= todd_class_factor(m, N)
        td = todd_class_product(N)
        assert abs(product - td) < 1e-10, (
            f"N={N}: product {product} != todd_class_product {td}"
        )


# ============================================================
# A-hat genus
# ============================================================

class TestAHatGenus:
    """A-hat genus contribution (trivial on 0-dim base)."""

    @pytest.mark.parametrize("N", range(3, 20))
    def test_a_hat_is_one(self, N):
        """A-hat(pt) = 1 for the point base."""
        result = a_hat_contribution(N)
        assert result['a_hat_base'] == 1

    @pytest.mark.parametrize("N", range(8, 20))
    def test_a_hat_index_equals_rank(self, N):
        """ind = A-hat(base) * rank(nu^-) = 1 * (N-5) = N-5."""
        result = a_hat_contribution(N)
        assert result['index'] == N - 5


# ============================================================
# xi-independence (topological invariant)
# ============================================================

class TestXiCritical:
    """xi_crit(N) marks the boundary of the Fredholm regime."""

    @pytest.mark.parametrize("N", [3, 4, 5, 6])
    def test_no_critical_for_stable(self, N):
        """N <= 6: no instability transition exists."""
        assert xi_critical(N) is None

    def test_n7_critical_is_zero(self):
        """N = 7: degenerate at xi = 0 (lambda_3 = 0)."""
        assert xi_critical(7) == 0.0

    @pytest.mark.parametrize("N", range(8, 26))
    def test_critical_positive_for_unstable(self, N):
        """N >= 8: xi_crit > 0 (Fredholm regime has positive width)."""
        xc = xi_critical(N)
        assert xc is not None
        assert xc > 0, f"N={N}: xi_crit = {xc} <= 0"

    @pytest.mark.parametrize("N", range(8, 26))
    def test_critical_less_than_one(self, N):
        """xi_crit < 1 (transition occurs before the Poincare disk boundary)."""
        xc = xi_critical(N)
        assert xc < 1.0


class TestXiIndependence:
    """The index is constant in the Fredholm regime [0, xi_crit)."""

    @pytest.mark.parametrize("N", range(8, 20))
    def test_index_constant_in_fredholm_regime(self, N):
        """Index does not change for xi in [0, 0.9 * xi_crit)."""
        result = xi_independence_proof(N)
        assert result['is_constant'], (
            f"N={N}: index varies with xi: {result['index_at_each_xi']}"
        )

    @pytest.mark.parametrize("N", range(8, 20))
    def test_index_value_at_xi_zero(self, N):
        """At xi = 0, index = N - 5."""
        result = xi_independence_proof(N, [0.0])
        assert result['index_at_each_xi'] == [N - 5]

    @pytest.mark.parametrize("N", [3, 4, 5, 6])
    def test_stable_N_constant_zero(self, N):
        """For N <= 6, index = 0 at xi = 0."""
        result = xi_independence_proof(N)
        assert all(c == 0 for c in result['index_at_each_xi'])

    @pytest.mark.parametrize("N", range(8, 20))
    def test_dense_sampling_in_fredholm_regime(self, N):
        """Index constant over dense sampling within [0, 0.9*xi_crit)."""
        xc = xi_critical(N)
        safe_max = xc * 0.9
        xi_dense = [safe_max * i / 50 for i in range(51)]
        result = xi_independence_proof(N, xi_dense)
        assert result['is_constant']
        assert result['index_value'] == N - 5

    @pytest.mark.parametrize("N", range(8, 16))
    def test_mode_lost_beyond_critical(self, N):
        """Beyond xi_crit, at least one mode leaves S^- (physical effect)."""
        xc = xi_critical(N)
        xi_beyond = xc * 1.1
        c1 = (N - 1) * (1 + xi_beyond**2) / (1 - xi_beyond)**2
        neg_beyond = [m for m in range(2, N) if c1 - m * (N - m) / 2 < -1e-15]
        # Should have strictly fewer negative modes than at xi=0
        assert len(neg_beyond) < N - 5, (
            f"N={N}: expected fewer negative modes beyond xi_crit, "
            f"got {len(neg_beyond)} (flat: {N-5})"
        )


# ============================================================
# Cross-check with Morse-Bott
# ============================================================

class TestMorseCrossCheck:
    """Index theorem agrees with direct Morse index computation."""

    @pytest.mark.parametrize("N", range(3, 26))
    def test_index_matches_morse(self, N):
        """ind(D_N) = complex Morse index for all N."""
        result = cross_check_morse_index(N)
        assert result['all_agree'], (
            f"N={N}: index_thm={result['index_theorem']}, "
            f"morse={result['morse_formula']}, "
            f"eig_count={result['eigenvalue_count']}"
        )

    @pytest.mark.parametrize("N", range(8, 26))
    def test_three_computations_agree(self, N):
        """All three methods give N - 5."""
        result = cross_check_morse_index(N)
        assert result['index_theorem'] == N - 5
        assert result['morse_formula'] == N - 5
        assert result['eigenvalue_count'] == N - 5


# ============================================================
# Palindromic structure
# ============================================================

class TestPalindromicStructure:
    """Negative modes come in palindromic pairs {m, N-m}."""

    @pytest.mark.parametrize("N", range(8, 20))
    def test_palindromic_pairing(self, N):
        """Every m in S^- has its partner N-m also in S^-."""
        neg = negative_modes(N)
        for m in neg:
            assert (N - m) in neg, (
                f"N={N}: m={m} in S^- but N-m={N-m} not"
            )

    @pytest.mark.parametrize("N", range(8, 20))
    def test_pair_count_consistent(self, N):
        """2 * #pairs + #self_palindromic = |S^-|."""
        result = verify_palindromic_structure(N)
        assert result['count_matches']

    @pytest.mark.parametrize("N", range(8, 20, 2))
    def test_even_N_self_palindromic(self, N):
        """For even N >= 8, m = N/2 is self-palindromic and in S^-."""
        half = N // 2
        neg = negative_modes(N)
        # N/2 is always >= 4 for N >= 8, and lambda_{N/2} < 0 for N >= 8
        assert half in neg, f"N={N}: N/2={half} not in S^-"
        result = verify_palindromic_structure(N)
        assert half in result['self_palindromic']

    @pytest.mark.parametrize("N", range(9, 20, 2))
    def test_odd_N_no_self_palindromic(self, N):
        """For odd N, no mode is self-palindromic."""
        result = verify_palindromic_structure(N)
        assert result['self_palindromic'] == []

    def test_real_euler_class(self):
        """Palindromic structure guarantees real Euler class for all N."""
        for N in range(8, 20):
            result = verify_palindromic_structure(N)
            assert result['real_euler_class']


# ============================================================
# K-theory splitting principle
# ============================================================

class TestSplittingPrinciple:
    """Splitting nu^- = direct_sum L_m in equivariant K-theory."""

    @pytest.mark.parametrize("N", range(8, 20))
    def test_bundle_rank(self, N):
        """rank(nu^-) = |S^-| = N - 5."""
        sp = splitting_principle_decomposition(N)
        assert sp['bundle_rank'] == N - 5

    @pytest.mark.parametrize("N", range(8, 20))
    def test_total_index_from_splitting(self, N):
        """Total index = sum of individual line bundle indices = N - 5."""
        sp = splitting_principle_decomposition(N)
        assert sp['total_index'] == N - 5

    @pytest.mark.parametrize("N", range(8, 20))
    def test_each_line_bundle_contributes_one(self, N):
        """Each L_m contributes index 1."""
        sp = splitting_principle_decomposition(N)
        for m, data in sp['line_bundles'].items():
            assert data['individual_index'] == 1

    @pytest.mark.parametrize("N", range(8, 20))
    def test_line_bundle_eigenvalues_negative(self, N):
        """Each L_m in the splitting has lambda_m < 0."""
        sp = splitting_principle_decomposition(N)
        for m, data in sp['line_bundles'].items():
            assert data['eigenvalue'] < 0, (
                f"N={N}: L_{m} has lambda = {data['eigenvalue']} >= 0"
            )

    @pytest.mark.parametrize("N", [3, 4, 5, 6])
    def test_trivial_splitting_stable(self, N):
        """For N <= 6, nu^- = 0 (empty decomposition)."""
        sp = splitting_principle_decomposition(N)
        assert sp['bundle_rank'] == 0
        assert sp['total_index'] == 0
        assert sp['line_bundles'] == {}


# ============================================================
# Full proof chain
# ============================================================

class TestProofChain:
    """Integration test: the complete proof chain."""

    @pytest.mark.parametrize("N", range(8, 26))
    def test_proof_chain_passes(self, N):
        """All proof steps pass for N >= 8."""
        result = index_theorem_proof(N)
        assert result.index == N - 5
        assert result.is_contiguous_block
        assert result.chern_rank == N - 5
        assert result.a_hat_base == 1
        assert result.xi_independent
        assert result.morse_cross_check

    @pytest.mark.parametrize("N", [3, 4, 5, 6])
    def test_proof_chain_stable(self, N):
        """Proof chain for stable N <= 6: index = 0."""
        result = index_theorem_proof(N)
        assert result.index == 0
        assert result.chern_rank == 0
        assert result.a_hat_base == 1
        assert result.xi_independent
        assert result.morse_cross_check

    def test_proof_chain_n7(self):
        """N = 7: degenerate case, index = 0 (kernel, not negative)."""
        result = index_theorem_proof(7)
        assert result.index == 0
        assert result.morse_cross_check

    def test_proof_generates_steps(self):
        """Proof chain produces non-trivial step descriptions."""
        result = index_theorem_proof(10)
        assert len(result.proof_steps) >= 7
        # Check that conclusion step exists
        conclusion = result.proof_steps[-1]
        assert "CONCLUSION" in conclusion
        assert "ind(D_10)" in conclusion

    def test_proof_chain_raises_for_invalid_N(self):
        """N < 3 raises ValueError."""
        with pytest.raises(ValueError, match="N must be >= 3"):
            index_theorem_proof(2)


# ============================================================
# Index theorem table
# ============================================================

class TestTable:
    """Test the summary table generation."""

    def test_table_range(self):
        """Table covers requested range."""
        table = index_theorem_table(3, 15)
        assert len(table) == 13  # N = 3, ..., 15
        assert table[0]['N'] == 3
        assert table[-1]['N'] == 15

    def test_table_all_checks_pass(self):
        """All entries in the table pass internal checks."""
        for row in index_theorem_table(3, 25):
            N = row['N']
            assert row['morse_check'], f"N={N}: Morse cross-check failed"
            assert row['xi_independent'], f"N={N}: xi-independence failed"
            if N >= 8:
                assert row['contiguous'], f"N={N}: contiguous block failed"
                assert row['index'] == N - 5
                assert row['chern_rank'] == N - 5

    def test_table_transition_at_7(self):
        """The index transitions from 0 to positive at N = 7 -> 8."""
        table = index_theorem_table(5, 10)
        idx_by_N = {row['N']: row['index'] for row in table}
        assert idx_by_N[6] == 0
        assert idx_by_N[7] == 0
        assert idx_by_N[8] == 3  # = 8 - 5
        assert idx_by_N[9] == 4  # = 9 - 5


# ============================================================
# Exact arithmetic consistency
# ============================================================

class TestExactArithmetic:
    """Verify that Fraction-based computation is exact (no float error)."""

    @pytest.mark.parametrize("N", range(3, 30))
    def test_eigenvalues_are_exact_fractions(self, N):
        """All Havelock eigenvalues are exact Fraction objects."""
        for m in range(2, N):
            lam = havelock_eigenvalue(m, N)
            assert isinstance(lam, Fraction)

    def test_n8_m4_eigenvalue_exact(self):
        """lambda_4(N=8) = 7 - 16/2 = 7 - 8 = -1 exactly."""
        assert havelock_eigenvalue(4, 8) == Fraction(-1)

    def test_n8_m3_eigenvalue_exact(self):
        """lambda_3(N=8) = 7 - 15/2 = -1/2 exactly."""
        assert havelock_eigenvalue(3, 8) == Fraction(-1, 2)

    def test_n6_m3_marginal(self):
        """lambda_3(N=6) = 5 - 9/2 = 1/2 > 0 (marginal but positive)."""
        assert havelock_eigenvalue(3, 6) == Fraction(1, 2)
        assert havelock_eigenvalue(3, 6) > 0

    def test_n7_m3_exact_zero(self):
        """lambda_3(N=7) = 6 - 12/2 = 0 exactly."""
        assert havelock_eigenvalue(3, 7) == Fraction(0)
