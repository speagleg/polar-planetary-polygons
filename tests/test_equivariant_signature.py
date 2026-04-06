"""
Tests for the Z_N equivariant signature as a topological invariant.

Verifies:
1. sigma_N values at specific N (closed form vs eigenvalue count)
2. eta_Hav(0) = sigma_N (the eta invariant IS the signature)
3. Palindromic structure lambda_m = lambda_{N-m}
4. xi-independence on H^2 (signs preserved under curvature scaling)
5. APS spectral flow theorem at N=7 transition
6. Dedekind sum / rho-invariant integrality
7. Mode counting consistency
"""

import pytest
from fractions import Fraction

from planetary_polygons.proofs.equivariant_signature import (
    havelock_eigenvalue,
    normal_eigenvalues,
    positive_modes,
    negative_modes,
    zero_modes,
    sign_counts,
    signature_from_eigenvalues,
    signature_closed_form,
    eta_havelock,
    reduced_eta,
    spectral_flow,
    spectral_flow_table,
    dedekind_sum_s1N,
    eta_signature_lens,
    rho_invariant,
    rho_integrality,
    c1_h2,
    verify_xi_independence,
    verify_palindromic,
    full_analysis,
    verify_all_identities,
    signature_table,
)


# ---------------------------------------------------------------------------
# Test: known eigenvalue values
# ---------------------------------------------------------------------------

class TestHavelockEigenvalues:
    """Sanity-check the eigenvalue formula at key points."""

    def test_m2_always_positive(self):
        """lambda_2 = (N-1) - (N-2) = 1 for all N >= 3."""
        for N in range(3, 30):
            assert havelock_eigenvalue(2, N) == Fraction(1)

    def test_m_Nminus2_always_positive(self):
        """lambda_{N-2} = 1 for all N >= 4 (palindromic with m=2)."""
        for N in range(4, 30):
            assert havelock_eigenvalue(N - 2, N) == Fraction(1)

    def test_n6_m3(self):
        """N=6, m=3: lambda = 5 - 9/2 = 1/2 > 0."""
        assert havelock_eigenvalue(3, 6) == Fraction(1, 2)

    def test_n7_m3_zero(self):
        """N=7, m=3: lambda = 6 - 12/2 = 0 (the critical zero mode)."""
        assert havelock_eigenvalue(3, 7) == Fraction(0)

    def test_n7_m4_zero(self):
        """N=7, m=4: lambda = 6 - 12/2 = 0 (palindromic partner)."""
        assert havelock_eigenvalue(4, 7) == Fraction(0)

    def test_n8_m3_negative(self):
        """N=8, m=3: lambda = 7 - 15/2 = -1/2 < 0 (first instability)."""
        assert havelock_eigenvalue(3, 8) == Fraction(-1, 2)

    def test_n8_m4_negative(self):
        """N=8, m=4: lambda = 7 - 8 = -1 < 0."""
        assert havelock_eigenvalue(4, 8) == Fraction(-1)

    def test_invalid_N(self):
        with pytest.raises(ValueError):
            normal_eigenvalues(2)


# ---------------------------------------------------------------------------
# Test: signature values at specific N
# ---------------------------------------------------------------------------

class TestSignatureValues:
    """Test sigma_N at specific values of N."""

    @pytest.mark.parametrize("N, expected", [
        (3, 1),
        (4, 2),
        (5, 3),
        (6, 4),
    ])
    def test_small_N_all_positive(self, N, expected):
        """For N <= 6: all eigenvalues positive, sigma = N-2."""
        assert signature_from_eigenvalues(N) == expected

    def test_n7_with_zero_modes(self):
        """N=7: 3 positive, 0 negative, 2 zero -> sigma = 3."""
        assert signature_from_eigenvalues(7) == 3

    @pytest.mark.parametrize("N, expected", [
        (8, 0),
        (9, -1),
        (10, -2),
        (11, -3),
        (12, -4),
    ])
    def test_large_N(self, N, expected):
        """For N >= 8: sigma = 8 - N."""
        assert signature_from_eigenvalues(N) == expected

    @pytest.mark.parametrize("N", range(3, 50))
    def test_closed_form_matches_eigenvalue_count(self, N):
        """The closed-form formula agrees with direct eigenvalue counting."""
        assert signature_from_eigenvalues(N) == signature_closed_form(N)


# ---------------------------------------------------------------------------
# Test: eta invariant equals signature
# ---------------------------------------------------------------------------

class TestEtaInvariant:
    """Test that eta_Hav(N, 0) = sigma_N."""

    @pytest.mark.parametrize("N", range(3, 25))
    def test_eta_at_s0_equals_sigma(self, N):
        """eta_Hav(N, 0) = sigma_N for all N."""
        eta_0 = eta_havelock(N, 0.0)
        sigma = signature_from_eigenvalues(N)
        assert eta_0 == Fraction(sigma)

    @pytest.mark.parametrize("N", [4, 8, 12])
    def test_eta_continuity_in_s(self, N):
        """eta_Hav(N, s) -> sigma_N as s -> 0 (entire function, finite sum)."""
        sigma = signature_from_eigenvalues(N)
        # Evaluate at small s values approaching 0
        for s in [0.5, 0.1, 0.01, 0.001]:
            eta_s = float(eta_havelock(N, s))
            # As s -> 0, eta(s) -> sigma (integer)
            if s <= 0.01:
                assert abs(eta_s - sigma) < 0.1, (
                    f"N={N}, s={s}: eta={eta_s}, sigma={sigma}"
                )

    def test_eta_is_exact_fraction_at_s0(self):
        """At s=0, the result is an exact integer (as Fraction)."""
        for N in range(3, 20):
            eta = eta_havelock(N, 0.0)
            assert eta.denominator == 1


# ---------------------------------------------------------------------------
# Test: reduced eta invariant
# ---------------------------------------------------------------------------

class TestReducedEta:
    """Test the reduced eta invariant eta-bar = (sigma + dim_ker)/2."""

    @pytest.mark.parametrize("N, expected", [
        (3, Fraction(1, 2)),
        (4, Fraction(1)),
        (5, Fraction(3, 2)),
        (6, Fraction(2)),
        (7, Fraction(5, 2)),
        (8, Fraction(0)),
        (9, Fraction(-1, 2)),
        (10, Fraction(-1)),
    ])
    def test_known_values(self, N, expected):
        assert reduced_eta(N) == expected

    def test_n7_includes_kernel(self):
        """At N=7, the 2 zero modes contribute to eta-bar."""
        sigma = signature_from_eigenvalues(7)
        assert sigma == 3
        n_zero = len(zero_modes(7))
        assert n_zero == 2
        assert reduced_eta(7) == Fraction(3 + 2, 2)


# ---------------------------------------------------------------------------
# Test: mode counting
# ---------------------------------------------------------------------------

class TestModeCounting:
    """Test that mode counts are consistent."""

    @pytest.mark.parametrize("N", range(3, 30))
    def test_total_mode_count(self, N):
        """n_pos + n_neg + n_zero = N - 2 (total normal modes)."""
        n_pos, n_neg, n_zero = sign_counts(N)
        assert n_pos + n_neg + n_zero == N - 2

    @pytest.mark.parametrize("N", [3, 4, 5, 6])
    def test_no_negative_modes_small_N(self, N):
        assert negative_modes(N) == []
        assert zero_modes(N) == []

    def test_n7_zero_modes(self):
        assert zero_modes(7) == [3, 4]
        assert negative_modes(7) == []

    @pytest.mark.parametrize("N", range(8, 20))
    def test_negative_count_is_N_minus_5(self, N):
        """For N >= 8: exactly N-5 negative modes."""
        assert len(negative_modes(N)) == N - 5

    @pytest.mark.parametrize("N", range(8, 20))
    def test_positive_count_is_3(self, N):
        """For N >= 8: exactly 3 positive modes {2, N-2, N-1}."""
        pos = positive_modes(N)
        assert len(pos) == 3
        assert set(pos) == {2, N - 2, N - 1}

    @pytest.mark.parametrize("N", range(8, 20))
    def test_negative_modes_are_interior(self, N):
        """For N >= 8: negative modes are {3, ..., N-3}."""
        neg = negative_modes(N)
        assert neg == list(range(3, N - 2))


# ---------------------------------------------------------------------------
# Test: palindromic structure
# ---------------------------------------------------------------------------

class TestPalindromic:
    """Test lambda_m = lambda_{N-m} (palindromic symmetry)."""

    @pytest.mark.parametrize("N", range(3, 25))
    def test_eigenvalue_palindrome(self, N):
        """lambda_m = lambda_{N-m} for all m in {2, ..., N-1}."""
        result = verify_palindromic(N)
        assert result['all_palindromic']

    @pytest.mark.parametrize("N", range(3, 25))
    def test_sign_palindrome(self, N):
        """Signs are palindromic: sgn(lambda_m) = sgn(lambda_{N-m})."""
        for m in range(2, N):
            lam_m = havelock_eigenvalue(m, N)
            lam_partner = havelock_eigenvalue(N - m, N)
            if lam_m > 0:
                assert lam_partner > 0
            elif lam_m < 0:
                assert lam_partner < 0
            else:
                assert lam_partner == 0

    @pytest.mark.parametrize("N", range(8, 16))
    def test_negative_modes_palindromic(self, N):
        """Every negative mode m has palindromic partner N-m also negative."""
        neg = negative_modes(N)
        for m in neg:
            assert (N - m) in neg

    @pytest.mark.parametrize("N", [8, 10, 12, 14])
    def test_self_palindromic_even_N(self, N):
        """For even N >= 8, mode m=N/2 is self-palindromic and negative."""
        m_half = N // 2
        assert m_half in negative_modes(N)
        result = verify_palindromic(N)
        assert result['self_palindromic'] is not None
        assert result['self_palindromic']['m'] == m_half


# ---------------------------------------------------------------------------
# Test: xi-independence on H^2
# ---------------------------------------------------------------------------

class TestXiIndependence:
    """Test that sigma_N is independent of the H^2 parameter xi."""

    @pytest.mark.parametrize("N", range(3, 16))
    def test_xi_independence(self, N):
        """sigma_N(xi) = sigma_N for all xi in (0, 1)."""
        result = verify_xi_independence(N, [0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99])
        assert result['all_match']

    @pytest.mark.parametrize("xi", [0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99])
    def test_c1_positive(self, xi):
        """C_1(N, xi) > 0 for all N >= 3 and xi in (0, 1)."""
        for N in range(3, 20):
            assert c1_h2(N, xi) > 0

    def test_c1_boundary_raises(self):
        """C_1 is undefined at xi = 0 and xi = 1."""
        with pytest.raises(ValueError):
            c1_h2(5, 0.0)
        with pytest.raises(ValueError):
            c1_h2(5, 1.0)

    def test_n8_critical_case(self):
        """N=8 has sigma=0 everywhere on H^2, verifying xi-independence."""
        for xi in [0.01, 0.5, 0.99]:
            c1 = c1_h2(8, xi)
            # All eigenvalues scaled by same positive factor
            sigma = 0
            for m in range(2, 8):
                lam = float(havelock_eigenvalue(m, 8)) * c1
                if lam > 0:
                    sigma += 1
                elif lam < 0:
                    sigma -= 1
            assert sigma == 0


# ---------------------------------------------------------------------------
# Test: spectral flow
# ---------------------------------------------------------------------------

class TestSpectralFlow:
    """Test the APS spectral flow at the N=7 transition."""

    def test_total_flow_6_to_8(self):
        """SF(6 -> 8) = -4 = -2 * dim_ker(N=7)."""
        sf = spectral_flow(6, 8)
        assert sf == -4
        assert sf == -2 * len(zero_modes(7))

    def test_flow_stable_regime(self):
        """SF = +1 for each step N -> N+1 in the stable regime N <= 5."""
        for N in range(3, 6):
            assert spectral_flow(N, N + 1) == 1

    def test_flow_6_to_7(self):
        """SF(6 -> 7) = -1 (two modes go from positive to zero,
        one new mode is positive)."""
        assert spectral_flow(6, 7) == -1

    def test_flow_7_to_8(self):
        """SF(7 -> 8) = -3 (two zero modes become negative,
        one positive becomes negative, one new positive)."""
        assert spectral_flow(7, 8) == -3

    def test_flow_unstable_regime(self):
        """SF = -1 for each step N -> N+1 in the unstable regime N >= 8."""
        for N in range(8, 20):
            assert spectral_flow(N, N + 1) == -1

    def test_spectral_flow_table(self):
        """Verify the spectral flow table is consistent."""
        table = spectral_flow_table(15)
        for row in table:
            assert row['spectral_flow'] == row['sigma_next'] - row['sigma_prev']


# ---------------------------------------------------------------------------
# Test: Dedekind sum and rho-invariant
# ---------------------------------------------------------------------------

class TestDedekindAndRho:
    """Test the Dedekind sum formula and rho-invariant integrality."""

    @pytest.mark.parametrize("N", range(3, 20))
    def test_dedekind_s1N_formula(self, N):
        """s(1, N) = (N-1)(N-2)/(12N) (exact Fraction)."""
        s = dedekind_sum_s1N(N)
        assert s == Fraction((N - 1) * (N - 2), 12 * N)

    @pytest.mark.parametrize("N", range(3, 20))
    def test_eta_signature_lens(self, N):
        """eta_sig(L(N,1)) = 4 * s(1,N) = (N-1)(N-2)/(3N)."""
        eta = eta_signature_lens(N)
        assert eta == Fraction((N - 1) * (N - 2), 3 * N)

    @pytest.mark.parametrize("N", range(3, 30))
    def test_rho_3N_is_integer(self, N):
        """3*N*rho(N) is always an integer."""
        val = rho_integrality(N)
        assert val.denominator == 1, f"N={N}: 3N*rho = {val} is not integer"

    @pytest.mark.parametrize("N, expected", [
        (3, 7),
        (4, 18),
        (5, 33),
        (6, 52),
    ])
    def test_rho_3N_stable_formula(self, N, expected):
        """For N <= 6: 3*N*rho = (N-2)(2N+1)."""
        val = rho_integrality(N)
        assert int(val) == expected
        assert int(val) == (N - 2) * (2 * N + 1)

    @pytest.mark.parametrize("N", range(8, 20))
    def test_rho_3N_unstable_formula(self, N):
        """For N >= 8: 3*N*rho = -4N^2 + 27N - 2."""
        val = int(rho_integrality(N))
        expected = -4 * N * N + 27 * N - 2
        assert val == expected


# ---------------------------------------------------------------------------
# Test: comprehensive identity verification
# ---------------------------------------------------------------------------

class TestComprehensiveVerification:
    """Run the full identity verification for a range of N."""

    @pytest.mark.parametrize("N", range(3, 25))
    def test_all_identities(self, N):
        """All claimed identities hold simultaneously."""
        checks = verify_all_identities(N)
        assert checks['all_pass'], f"N={N}: failed checks = {checks}"

    @pytest.mark.parametrize("N", range(3, 25))
    def test_full_analysis_consistent(self, N):
        """The full_analysis result is internally consistent."""
        r = full_analysis(N)
        assert r.sigma == r.n_positive - r.n_negative
        assert r.n_positive + r.n_negative + r.n_zero == N - 2
        assert r.eta_hav_0 == Fraction(r.sigma)
        assert r.reduced_eta == Fraction(r.sigma + r.n_zero, 2)

    def test_signature_table(self):
        """The signature table generates without errors."""
        table = signature_table(20)
        assert len(table) == 18  # N = 3, ..., 20


# ---------------------------------------------------------------------------
# Test: topological properties
# ---------------------------------------------------------------------------

class TestTopologicalProperties:
    """Test the topological invariant properties of sigma_N."""

    def test_sigma_is_integer(self):
        """sigma_N is always an integer (spectral asymmetry)."""
        for N in range(3, 50):
            sigma = signature_from_eigenvalues(N)
            assert isinstance(sigma, int)

    def test_sigma_parity(self):
        """sigma_N mod 2 = N mod 2 for all N."""
        for N in range(3, 50):
            sigma = signature_from_eigenvalues(N)
            assert sigma % 2 == N % 2, f"N={N}: sigma={sigma}, parity mismatch"

    def test_sigma_monotone_stable(self):
        """sigma_N is strictly increasing for 3 <= N <= 6."""
        for N in range(3, 6):
            assert signature_from_eigenvalues(N + 1) > signature_from_eigenvalues(N)

    def test_sigma_monotone_unstable(self):
        """sigma_N is strictly decreasing for N >= 8."""
        for N in range(8, 30):
            assert signature_from_eigenvalues(N + 1) < signature_from_eigenvalues(N)

    def test_sigma_max_at_n6(self):
        """sigma_N achieves its maximum at N=6 (sigma_6 = 4)."""
        sigma_max = max(signature_from_eigenvalues(N) for N in range(3, 50))
        assert sigma_max == 4
        assert signature_from_eigenvalues(6) == sigma_max

    def test_sigma_zero_at_n8(self):
        """sigma_N = 0 at N=8 (balanced positive/negative modes)."""
        assert signature_from_eigenvalues(8) == 0

    def test_unique_zero_crossing(self):
        """sigma_N passes through zero exactly once, between N=7 and N=9."""
        # sigma_7 = 3 > 0, sigma_8 = 0, sigma_9 = -1 < 0
        assert signature_from_eigenvalues(7) > 0
        assert signature_from_eigenvalues(8) == 0
        assert signature_from_eigenvalues(9) < 0
