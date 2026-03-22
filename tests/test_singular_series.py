"""Tests for singular series constants (twin prime constant, S_{40,17})."""

import mpmath
import pytest

from planetary_polygons.extensions.number_theory.singular_series import (
    twin_prime_constant_c2,
    compute_s40_17,
)

mpmath.mp.dps = 50


class TestTwinPrimeConstant:
    """Test the Hardy-Littlewood twin prime constant C_2."""

    def test_c2_value(self):
        """C_2 (wide convention, including p=2 factor) ~ 1.3203."""
        c2 = twin_prime_constant_c2(prime_bound=1_000_000)
        assert abs(c2 - 1.3203) < 0.001, f"C_2 = {c2}, expected ~1.3203"

    def test_c2_known_digits(self):
        """C_2 should match 1.3203236... to 6 digits."""
        c2 = twin_prime_constant_c2(prime_bound=1_000_000)
        # Wide convention: 2 * 0.6601618... = 1.3203236...
        expected = mpmath.mpf('1.3203236')
        assert abs(c2 - expected) < 1e-6, f"C_2 = {c2}, expected ~{expected}"

    def test_c2_convergence(self):
        """C_2 at 100k vs 1M primes should agree to 4+ digits."""
        c2_100k = twin_prime_constant_c2(prime_bound=100_000)
        c2_1m = twin_prime_constant_c2(prime_bound=1_000_000)
        rel_diff = abs(c2_100k - c2_1m) / abs(c2_1m)
        matching = -float(mpmath.log10(rel_diff)) if rel_diff > 0 else 50
        assert matching >= 4, f"Only {matching:.1f} matching digits"


class TestS40_17:
    """Test the Bateman-Horn constant S_{40,17}."""

    def test_s40_17_value(self):
        """S_{40,17} = (10/3)*C_2 ~ 4.401."""
        s = compute_s40_17(prime_bound=1_000_000)
        assert abs(s - 4.401) < 0.01, f"S_{{40,17}} = {s}, expected ~4.401"

    def test_s40_17_relation_to_c2(self):
        """S_{40,17} should be exactly (10/3)*C_2."""
        c2 = twin_prime_constant_c2(prime_bound=100_000)
        s = compute_s40_17(prime_bound=100_000)
        expected = (mpmath.mpf(10) / 3) * c2
        assert abs(s - expected) < 1e-30, "S_{40,17} != (10/3)*C_2"
