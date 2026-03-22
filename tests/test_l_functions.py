"""Tests for L-function computations on the Bolza form."""

import mpmath
import pytest

from planetary_polygons.extensions.number_theory.l_functions import (
    dirichlet_chars_mod5,
    l_value,
    l_derivative,
    l_log_derivative,
)

mpmath.mp.dps = 50

# Use moderate num_terms for tests to keep runtime reasonable
_TEST_TERMS = 50000


class TestDirichletCharsMod5:
    """Test the four Dirichlet characters mod 5."""

    def setup_method(self):
        self.chars = dirichlet_chars_mod5()

    def test_trivial_character_values(self):
        """chi_0 is 1 on all coprime residues, 0 on multiples of 5."""
        chi0 = self.chars[0]
        assert chi0(1) == 1
        assert chi0(2) == 1
        assert chi0(3) == 1
        assert chi0(4) == 1
        assert chi0(5) == 0
        assert chi0(10) == 0

    def test_real_character_legendre(self):
        """chi_1 = (./5) Legendre symbol values."""
        chi1 = self.chars[1]
        assert chi1(1) == 1
        assert chi1(2) == -1
        assert chi1(3) == -1
        assert chi1(4) == 1
        assert chi1(5) == 0

    def test_order4_character_values(self):
        """chi_2 has order 4: chi_2(2)=i, chi_2(3)=-i, chi_2(4)=-1."""
        chi2 = self.chars[2]
        assert chi2(1) == 1
        assert chi2(2) == mpmath.mpc(0, 1)
        assert chi2(3) == mpmath.mpc(0, -1)
        assert chi2(4) == -1
        assert chi2(5) == 0

    def test_order4_conj_character_values(self):
        """chi_3 = conjugate of chi_2."""
        chi3 = self.chars[3]
        assert chi3(1) == 1
        assert chi3(2) == mpmath.mpc(0, -1)
        assert chi3(3) == mpmath.mpc(0, 1)
        assert chi3(4) == -1
        assert chi3(5) == 0

    def test_periodicity(self):
        """All characters are periodic mod 5."""
        for chi in self.chars:
            for n in range(1, 20):
                assert chi(n) == chi(n + 5), f"Failed periodicity at n={n}"

    def test_character_orthogonality(self):
        """sum_{n=1}^{4} |chi(n)|^2 = 4 for each character."""
        for i, chi in enumerate(self.chars):
            total = sum(abs(chi(n)) ** 2 for n in range(1, 5))
            assert abs(total - 4) < 1e-10, (
                f"Orthogonality failed for chi_{i}: got {total}"
            )


class TestLValues:
    """Test L(1, f tensor chi) values."""

    def test_L1_trivial_approximate(self):
        """L(1, f) should be approximately 0.815."""
        val = l_value(1, 0, num_terms=_TEST_TERMS)
        assert abs(val - 0.815) < 0.005, f"L(1, f) = {val}, expected ~0.815"

    def test_L1_real_approximate(self):
        """L(1, f tensor (./5)) should be approximately 1.053."""
        val = l_value(1, 1, num_terms=_TEST_TERMS)
        assert abs(val - 1.053) < 0.005, f"L(1, f x (./5)) = {val}, expected ~1.053"

    def test_all_L_values_nonzero(self):
        """All four L(1, f tensor chi) should be nonzero."""
        for i in range(4):
            val = l_value(1, i, num_terms=_TEST_TERMS)
            assert abs(val) > 0.1, (
                f"L(1, f x chi_{i}) = {val}, too close to zero"
            )

    def test_self_consistency_convergence(self):
        """L(1, f) at 50k terms vs 200k terms should agree to 6+ digits."""
        val_50k = l_value(1, 0, num_terms=50000)
        val_200k = l_value(1, 0, num_terms=200000)
        rel_diff = abs(val_50k - val_200k) / abs(val_200k)
        matching = -float(mpmath.log10(rel_diff)) if rel_diff > 0 else 50
        assert matching >= 6, (
            f"Only {matching:.1f} matching digits between 50k and 200k terms"
        )

    def test_conjugate_symmetry(self):
        """L(1, f x chi_2) and L(1, f x chi_3) should be complex conjugates."""
        v2 = l_value(1, 2, num_terms=_TEST_TERMS)
        v3 = l_value(1, 3, num_terms=_TEST_TERMS)
        assert abs(v2 - mpmath.conj(v3)) < 1e-8, (
            f"chi_2 and chi_3 L-values not conjugate: {v2}, {v3}"
        )
