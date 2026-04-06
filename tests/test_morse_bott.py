"""
Tests for the Morse-Bott structure theorem.

Verifies:
1. Dimension counting (normal space = 2(N-2) = quotient dim)
2. Eigenvalue classification (exact rational arithmetic)
3. N=7 is the unique non-Morse-Bott case
4. Complex Morse index = max(0, N-5) for N != 7
5. Numerical verification against constrained Hessian
"""

import pytest
from fractions import Fraction

from planetary_polygons.proofs.morse_bott import (
    havelock_eigenvalue,
    normal_eigenvalues,
    morse_bott_analysis,
    verify_mode_counting,
    zero_eigenvalue_classification,
    morse_index_formula_value,
    verify_morse_index_formula,
    full_morse_bott_table,
)


class TestHavelockEigenvalue:
    """Test the exact Havelock eigenvalue formula."""

    def test_known_values(self):
        # N=6, m=3: lambda = 5 - 9/2 = 1/2
        assert havelock_eigenvalue(3, 6) == Fraction(1, 2)

    def test_n7_m3_zero(self):
        # N=7, m=3: lambda = 6 - 6 = 0 (the critical case)
        assert havelock_eigenvalue(3, 7) == 0

    def test_n7_m4_zero(self):
        # N=7, m=4: lambda = 6 - 6 = 0 (palindromic partner)
        assert havelock_eigenvalue(4, 7) == 0

    def test_palindromic_symmetry(self):
        """lambda_m = lambda_{N-m} for all N, m."""
        for N in range(3, 20):
            for m in range(1, N):
                assert havelock_eigenvalue(m, N) == havelock_eigenvalue(N - m, N)

    def test_n8_negative_modes(self):
        # N=8: m=3 -> 7 - 15/2 = -1/2, m=4 -> 7 - 8 = -1
        assert havelock_eigenvalue(3, 8) == Fraction(-1, 2)
        assert havelock_eigenvalue(4, 8) == Fraction(-1)


class TestDimensionCounting:
    """Test that the Fourier mode counting matches the quotient dimension."""

    @pytest.mark.parametrize("N", range(3, 20))
    def test_dimensions_match(self, N):
        result = verify_mode_counting(N)
        assert result['dimensions_match'], (
            f"N={N}: normal dim {result['normal_mode_dim']} != "
            f"quotient dim {result['quotient_dim']}"
        )

    def test_specific_dimensions(self):
        r = verify_mode_counting(7)
        assert r['config_dim'] == 14
        assert r['constraint_surface_dim'] == 11
        assert r['quotient_dim'] == 10
        assert r['normal_mode_dim'] == 10


class TestMorseBott:
    """Test the Morse-Bott classification."""

    @pytest.mark.parametrize("N", [3, 4, 5, 6])
    def test_small_N_is_minimum(self, N):
        mb = morse_bott_analysis(N)
        assert mb.is_morse_bott
        assert mb.complex_morse_index == 0
        assert mb.kernel_dimension == 0

    def test_n7_not_morse_bott(self):
        mb = morse_bott_analysis(7)
        assert not mb.is_morse_bott
        assert mb.kernel_dimension == 4  # modes m=3,4, each 2-real-dim

    @pytest.mark.parametrize("N", [8, 9, 10, 11, 12])
    def test_large_N_is_morse_bott_saddle(self, N):
        mb = morse_bott_analysis(N)
        assert mb.is_morse_bott
        assert mb.complex_morse_index > 0
        assert mb.kernel_dimension == 0

    @pytest.mark.parametrize("N", range(3, 25))
    def test_morse_index_formula(self, N):
        """Complex Morse index = 0 for N<=6, N-5 for N>=8."""
        mb = morse_bott_analysis(N)
        expected = morse_index_formula_value(N)
        assert mb.complex_morse_index == expected, (
            f"N={N}: got index {mb.complex_morse_index}, expected {expected}"
        )

    @pytest.mark.parametrize("N", range(3, 25))
    def test_real_index_is_double(self, N):
        """Real Morse index = 2 * complex Morse index."""
        mb = morse_bott_analysis(N)
        assert mb.real_morse_index == 2 * mb.complex_morse_index


class TestUniquenessOfN7:
    """Test that N=7 is the unique non-Morse-Bott case."""

    def test_analytical_uniqueness(self):
        result = zero_eigenvalue_classification()
        assert result['unique_N'] == 7
        assert result['numerical_zeros'] == {7: [3, 4]}
        assert result['analytical_zeros'] == {7: [3, 4]}

    @pytest.mark.parametrize("N", range(3, 100))
    def test_no_other_zeros(self, N):
        """For N != 7, no normal eigenvalue is zero."""
        if N == 7:
            return
        evals = normal_eigenvalues(N)
        assert all(lam != 0 for lam in evals), (
            f"N={N} has zero eigenvalue(s)"
        )


class TestMorseIndexFormula:
    """Verify the index formula across a range."""

    def test_formula_table(self):
        results = verify_morse_index_formula()
        for N, data in results.items():
            assert data['matches'], (
                f"N={N}: computed {data['computed_index']} != "
                f"formula {data['formula_index']}"
            )


class TestFullTable:
    """Test the complete classification table."""

    def test_table_generation(self):
        rows = full_morse_bott_table(15)
        assert len(rows) == 13  # N=3,...,15
        for row in rows:
            assert row['dim_check']

    def test_transition_at_7(self):
        rows = full_morse_bott_table(10)
        for row in rows:
            if row['N'] <= 6:
                assert row['is_morse_bott']
                assert row['complex_index'] == 0
            elif row['N'] == 7:
                assert not row['is_morse_bott']
            else:
                assert row['is_morse_bott']
                assert row['complex_index'] > 0
