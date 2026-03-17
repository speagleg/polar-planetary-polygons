"""Tests for the analytic sign rule proof."""

import numpy as np
import pytest
from sign_rule_proof import (
    H_double_prime_analytic,
    H_double_prime_numerical,
    check_sign_rule_conditions,
    verify_sign_rule,
)


# Standard interactions for testing
LOG = {
    'name': '-ln(r)',
    'h': lambda r: -np.log(r),
    'hp': lambda r: -1/r,
    'hpp': lambda r: 1/r**2,
}
POWER_HALF = {
    'name': '-r^0.5',
    'h': lambda r: -r**0.5,
    'hp': lambda r: -0.5*r**(-0.5),
    'hpp': lambda r: 0.25*r**(-1.5),
}
POWER_TWO = {
    'name': '-r^2',
    'h': lambda r: -r**2,
    'hp': lambda r: -2*r,
    'hpp': lambda r: -2.0 + 0*r,
}
SMALL_EPSILON = {
    'name': '-r^0.01',
    'h': lambda r: -r**0.01,
    'hp': lambda r: -0.01*r**(-0.99),
    'hpp': lambda r: 0.01*0.99*r**(-1.99),
}


class TestAnalyticFormula:
    """Verify analytic formula matches numerical computation."""

    @pytest.mark.parametrize("N", [3, 4, 5, 6, 7, 8])
    def test_log_interaction(self, N):
        H_a = H_double_prime_analytic(N, LOG['hp'], LOG['hpp'])
        H_n = H_double_prime_numerical(N, LOG['h'])
        assert abs(H_a - H_n) < 0.01 * abs(H_n)

    @pytest.mark.parametrize("N", [3, 5, 6, 8])
    def test_power_half(self, N):
        H_a = H_double_prime_analytic(N, POWER_HALF['hp'], POWER_HALF['hpp'])
        H_n = H_double_prime_numerical(N, POWER_HALF['h'])
        assert abs(H_a - H_n) < 0.01 * abs(H_n)

    @pytest.mark.parametrize("N", [3, 5, 6, 8])
    def test_power_two(self, N):
        H_a = H_double_prime_analytic(N, POWER_TWO['hp'], POWER_TWO['hpp'])
        H_n = H_double_prime_numerical(N, POWER_TWO['h'])
        assert abs(H_a - H_n) < 0.01 * abs(H_n)


class TestSignRule:
    """Test that h'<0 and (rh')'<=0 implies H''(0)<0."""

    @pytest.mark.parametrize("interaction", [LOG, POWER_HALF, POWER_TWO, SMALL_EPSILON])
    @pytest.mark.parametrize("N", [3, 4, 5, 6, 7, 8, 9])
    def test_negative_H_pp(self, interaction, N):
        H_pp = H_double_prime_analytic(N, interaction['hp'], interaction['hpp'])
        assert H_pp < 0, (
            f"{interaction['name']}, N={N}: H''(0)={H_pp:.6f} should be < 0"
        )

    @pytest.mark.parametrize("interaction", [LOG, POWER_HALF, POWER_TWO, SMALL_EPSILON])
    def test_conditions_satisfied(self, interaction):
        result = check_sign_rule_conditions(interaction['hp'], interaction['hpp'])
        assert result['condition_i'], f"{interaction['name']}: h'(r) not < 0"
        assert result['condition_ii'], f"{interaction['name']}: (rh')' not <= 0"


class TestLogSpecialCase:
    """For h=-ln(r), the first term vanishes: d^2*h'' + d*h' = 0."""

    @pytest.mark.parametrize("N", [3, 5, 6, 8])
    def test_first_term_vanishes(self, N):
        """A_m = d_m^2/d_m^2 + d_m*(-1/d_m) = 1 - 1 = 0 for all m."""
        for m in range(1, N):
            d_m = 2 * np.sin(np.pi * m / N)
            A_m = d_m**2 * (1/d_m**2) + d_m * (-1/d_m)
            assert abs(A_m) < 1e-14

    @pytest.mark.parametrize("N", [3, 5, 6, 8])
    def test_recovers_paper_formula(self, N):
        """Should give H''(0) = -(1/4N^2) Sum (N-m)m^2/sin^2(pi m/N)."""
        H_anal = H_double_prime_analytic(N, lambda r: -1/r, lambda r: 1/r**2)
        H_paper = 0.0
        for m in range(1, N):
            H_paper -= (N - m) * m**2 / (4 * N**2 * np.sin(np.pi * m / N)**2)
        assert abs(H_anal - H_paper) < 1e-10 * abs(H_paper)


class TestReviewerCounterexample:
    """Referee A suggested h(r) = -r^eps might fail. It doesn't."""

    @pytest.mark.parametrize("eps", [0.001, 0.01, 0.1, 0.5, 1.0, 2.0])
    def test_power_law_always_negative(self, eps):
        hp = lambda r: -eps * r**(eps - 1)
        hpp = lambda r: -eps * (eps - 1) * r**(eps - 2)
        for N in [3, 6, 8]:
            H_pp = H_double_prime_analytic(N, hp, hpp)
            assert H_pp < 0, f"eps={eps}, N={N}: H''={H_pp}"

    @pytest.mark.parametrize("eps", [0.001, 0.01, 0.1, 0.5, 1.0, 2.0])
    def test_conditions_hold(self, eps):
        hp = lambda r: -eps * r**(eps - 1)
        hpp = lambda r: -eps * (eps - 1) * r**(eps - 2)
        result = check_sign_rule_conditions(hp, hpp)
        assert result['sign_rule_applies']


class TestVerifyFunction:

    def test_full_verification_passes(self):
        assert verify_sign_rule(verbose=False)
