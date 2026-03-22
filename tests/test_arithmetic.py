"""Tests for number-theoretic arithmetic primitives."""

import pytest

from planetary_polygons.extensions.number_theory.arithmetic import (
    fibonacci_entry_point,
    hecke_eigenvalue_ap,
    legendre_symbol,
    sqrt2_mod_p,
    tonelli_shanks,
)
from planetary_polygons.extensions.number_theory.sieve import primes_up_to


class TestLegendreSymbol:
    def test_residue(self):
        assert legendre_symbol(1, 7) == 1

    def test_non_residue(self):
        assert legendre_symbol(3, 7) == -1

    def test_divisible(self):
        assert legendre_symbol(7, 7) == 0

    def test_2_mod_17_is_residue(self):
        # 2 is a QR mod 17 since 17 ≡ 1 (mod 8)
        assert legendre_symbol(2, 17) == 1

    def test_2_mod_3_is_non_residue(self):
        assert legendre_symbol(2, 3) == -1


class TestTonelliShanks:
    def test_sqrt_4_mod_7(self):
        r = tonelli_shanks(4, 7)
        assert r * r % 7 == 4
        assert r == min(r, 7 - r)  # smaller root

    def test_sqrt_2_mod_17(self):
        r = tonelli_shanks(2, 17)
        assert r * r % 17 == 2
        assert r == min(r, 17 - r)

    def test_sqrt_2_mod_41(self):
        r = tonelli_shanks(2, 41)
        assert r * r % 41 == 2
        assert r == min(r, 41 - r)

    def test_sqrt_2_mod_97(self):
        r = tonelli_shanks(2, 97)
        assert r * r % 97 == 2
        assert r == min(r, 97 - r)

    def test_non_residue_raises(self):
        with pytest.raises(ValueError):
            tonelli_shanks(3, 7)


class TestSqrt2ModP:
    def test_p17(self):
        r = sqrt2_mod_p(17)
        assert r * r % 17 == 2
        assert r == min(r, 17 - r)

    def test_p41(self):
        r = sqrt2_mod_p(41)
        assert r * r % 41 == 2
        assert r == min(r, 41 - r)

    def test_p3_raises(self):
        with pytest.raises(ValueError):
            sqrt2_mod_p(3)


class TestFibonacciEntryPoint:
    """Known values of the Fibonacci entry point alpha(p)."""

    @pytest.mark.parametrize("p, expected", [
        (5, 5),
        (7, 8),
        (11, 10),
        (13, 7),
        (17, 9),
    ])
    def test_known_values(self, p, expected):
        assert fibonacci_entry_point(p) == expected


class TestHeckeEigenvalue:
    def test_p2_is_zero(self):
        """p = 2 divides the level."""
        assert hecke_eigenvalue_ap(2) == 0

    def test_p3_is_zero(self):
        """3 mod 8 = 3, not 1."""
        assert hecke_eigenvalue_ap(3) == 0

    def test_p5_is_zero(self):
        """5 mod 8 = 5, not 1."""
        assert hecke_eigenvalue_ap(5) == 0

    def test_p7_is_zero(self):
        """7 mod 8 = 7, not 1."""
        assert hecke_eigenvalue_ap(7) == 0

    def test_p17(self):
        assert hecke_eigenvalue_ap(17) == -2

    def test_p41(self):
        assert hecke_eigenvalue_ap(41) == 2

    def test_all_p_1_mod_8_give_pm2(self):
        """For p ≡ 1 (mod 8), a_p ∈ {-2, 2}."""
        primes = primes_up_to(200)
        for p in primes:
            if p % 8 == 1:
                ap = hecke_eigenvalue_ap(p)
                assert ap in (-2, 2), f"a_{p} = {ap}, expected ±2"
