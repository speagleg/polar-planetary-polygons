"""Tests for the Bolza form eta(8z)*eta(16z) q-expansion."""

import pytest

from planetary_polygons.extensions.number_theory.arithmetic import hecke_eigenvalue_ap
from planetary_polygons.extensions.number_theory.bolza_form import (
    _kronecker_minus2,
    bolza_coefficients,
    eta_product_coefficients,
)


class TestEtaProductCoefficients:
    def test_a1_is_one(self):
        coeffs = eta_product_coefficients(20)
        assert coeffs[1] == 1

    def test_a2_through_a8_are_zero(self):
        coeffs = eta_product_coefficients(20)
        for n in range(2, 9):
            assert coeffs[n] == 0, f"a_{n} = {coeffs[n]}, expected 0"

    def test_a9_is_minus_one(self):
        coeffs = eta_product_coefficients(20)
        assert coeffs[9] == -1


class TestCrossCheck:
    """Cross-check eta product against Hecke eigenvalues at primes."""

    @pytest.mark.parametrize("p", [17, 41, 73, 89, 97])
    def test_eta_vs_hecke_at_prime(self, p):
        coeffs = eta_product_coefficients(p + 1)
        eta_ap = coeffs[p]
        hecke_ap = hecke_eigenvalue_ap(p)
        assert eta_ap == hecke_ap, (
            f"Mismatch at p={p}: eta gives {eta_ap}, Hecke gives {hecke_ap}"
        )


class TestHeckePrimePower:
    def test_a289(self):
        """a_{289} = a_{17^2} = a_17^2 - chi(17) = (-2)^2 - 1 = 3.

        chi(17) = Kronecker(-2/17). 17 ≡ 1 (mod 8) so (2/17)=1,
        and 17 ≡ 1 (mod 4) so (-1/17)=1, hence chi(17) = 1.
        """
        coeffs = bolza_coefficients(290)
        assert coeffs[289] == 3


class TestMultiplicativity:
    def test_a153(self):
        """a_{153} = a_9 * a_17 since gcd(9, 17) = 1.

        a_9 = -1 (from eta product), a_17 = -2, so a_153 = 2.
        """
        coeffs = bolza_coefficients(154)
        assert coeffs[153] == 2

    def test_a153_matches_eta(self):
        """Cross-check: bolza_coefficients vs eta_product at n=153."""
        eta = eta_product_coefficients(154)
        bolza = bolza_coefficients(154)
        assert eta[153] == bolza[153]


class TestBolzaVsEtaProduct:
    """Broad cross-check of both methods up to moderate bound."""

    def test_agreement_up_to_100(self):
        N = 100
        eta = eta_product_coefficients(N)
        bolza = bolza_coefficients(N)
        for n in range(1, N):
            assert eta[n] == bolza[n], (
                f"Mismatch at n={n}: eta={eta[n]}, bolza={bolza[n]}"
            )
