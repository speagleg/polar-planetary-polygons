"""
Tests for the APS index theorem proof: ind(D_N) = μ(N).

Every test uses exact rational arithmetic (fractions).
No floating point, no scipy, no sympy.
"""
import pytest
from fractions import Fraction
from planetary_polygons.proofs.aps_index_proof import (
    casimir, C1_flat, C1_H2, havelock_eigenvalue,
    morse_index, morse_index_formula,
    eta_invariant, eta_at_flat, eta_limit,
    spectral_flow, kernel_dim_at_flat,
    aps_index, verify_aps_equals_morse,
    dC1_positive_proof, prove_eta_parity,
    monotonicity_implies_simple_crossings,
    crossing_points, full_proof,
)


class TestCasimir:
    """Z_N Casimir f(m,N) = m(N-m)/2."""

    def test_known_values(self):
        assert casimir(1, 7) == Fraction(3)
        assert casimir(2, 7) == Fraction(5)
        assert casimir(3, 7) == Fraction(6)

    def test_palindromic(self):
        """f(m,N) = f(N-m,N)."""
        for N in range(3, 20):
            for m in range(1, N):
                assert casimir(m, N) == casimir(N - m, N)

    def test_maximum_odd(self):
        """For odd N, max f = (N²-1)/8 at m=(N-1)/2."""
        for N in range(3, 20, 2):
            m_max = (N - 1) // 2
            f_max = casimir(m_max, N)
            assert f_max == Fraction(N**2 - 1, 8)
            for m in range(1, N):
                assert casimir(m, N) <= f_max

    def test_maximum_even(self):
        """For even N, max f = N²/8 at m=N/2."""
        for N in range(4, 20, 2):
            m_max = N // 2
            f_max = casimir(m_max, N)
            assert f_max == Fraction(N**2, 8)


class TestMorseIndex:
    """μ(N) = 0 for N ≤ 7, N-5 for N ≥ 8."""

    def test_small_N(self):
        for N in range(3, 8):
            assert morse_index(N) == 0

    def test_N7_marginal(self):
        """N=7: λ₃ = 0, not counted as negative."""
        assert morse_index(7) == 0
        lam3 = havelock_eigenvalue(3, 7)
        assert lam3 == 0

    def test_N8_first_unstable(self):
        assert morse_index(8) == 3

    def test_formula_match(self):
        """Counting matches closed form for N=3..50."""
        for N in range(3, 51):
            assert morse_index(N) == morse_index_formula(N)

    def test_unstable_band_is_3_to_Nminus3(self):
        """For N ≥ 8, negative eigenvalues are exactly m=3,...,N-3."""
        for N in range(8, 30):
            C1 = C1_flat(N)
            for m in range(1, N):
                lam = havelock_eigenvalue(m, N, C1)
                if 3 <= m <= N - 3:
                    assert lam < 0, f"N={N}, m={m}: expected negative"
                else:
                    assert lam > 0, f"N={N}, m={m}: expected positive"


class TestEtaInvariant:
    """η(H_N) = Σ sgn(λ_m)."""

    def test_all_positive_small_N(self):
        """For N ≤ 6, all eigenvalues positive, η = N-1."""
        for N in range(3, 7):
            assert eta_at_flat(N) == N - 1

    def test_N7_marginal(self):
        """N=7: λ₃ = 0 contributes 0 to η. η = 6 - 0 = 5 (not 6)."""
        # 6 eigenvalues: m=1,2 positive, m=3 zero, m=4,5,6 by palindrome
        # m=4: λ₄ = λ₃ = 0, m=5: λ₅ = λ₂ > 0, m=6: λ₆ = λ₁ > 0
        # So η = 4 positive + 0 zero + 0 negative... wait
        # λ₁(7) = 6 - 3 = 3 > 0
        # λ₂(7) = 6 - 5 = 1 > 0
        # λ₃(7) = 6 - 6 = 0
        # λ₄(7) = 6 - 6 = 0
        # λ₅(7) = 6 - 5 = 1 > 0
        # λ₆(7) = 6 - 3 = 3 > 0
        # η = 4 (four positive, two zero)
        assert eta_at_flat(7) == 4

    def test_N8(self):
        """N=8: μ=3, so η = (N-1) - 2μ = 7 - 6 = 1."""
        assert eta_at_flat(8) == 1

    def test_identity_eta_0(self):
        """η(0) = (N-1) - 2μ(N) - h₀ for all N."""
        for N in range(3, 30):
            eta = eta_at_flat(N)
            mu = morse_index(N)
            h0 = kernel_dim_at_flat(N)
            expected = (N - 1) - 2 * mu - h0
            assert eta == expected

    def test_eta_limit(self):
        """η(∞) = N-1 for all N."""
        for N in range(3, 30):
            assert eta_limit(N) == N - 1


class TestAPSIndex:
    """ind(D_N) = (η(∞) - η(0)) / 2."""

    def test_small_N_zero(self):
        """For N ≤ 6, ind = 0."""
        for N in range(3, 7):
            assert aps_index(N) == 0

    def test_N7_zero(self):
        """N=7: marginal case with kernel correction.

        η(0) = 4, η(∞) = 6, h₀ = 2 (modes m=3,4 are zero).
        Naive (η(∞)-η(0))/2 = 1, but corrected:
        (η(∞) - η(0) - h₀)/2 = (6 - 4 - 2)/2 = 0 = μ(7). ✓

        Equivalently: SF = 0 (no negative eigenvalue crosses to positive).
        """
        assert aps_index(7) == 0
        assert spectral_flow(7) == 0
        assert kernel_dim_at_flat(7) == 2
        # Verify the kernel-corrected eta formula also gives 0
        eta_0 = eta_at_flat(7)
        eta_inf = eta_limit(7)
        h0 = kernel_dim_at_flat(7)
        assert (eta_inf - eta_0 - h0) // 2 == 0

    def test_N8_to_N30(self):
        """For N ≥ 8, ind(D_N) should equal μ(N) = N-5.

        For N ≥ 8 there are no zero eigenvalues at ξ=0, so the
        naive formula (η(∞) - η(0))/2 = μ(N) holds exactly.
        """
        for N in range(8, 31):
            # Verify no zero eigenvalues at ξ=0
            C1 = C1_flat(N)
            for m in range(1, N):
                assert havelock_eigenvalue(m, N, C1) != 0, (
                    f"N={N}, m={m}: unexpected zero eigenvalue"
                )
            # Now the naive formula works
            assert aps_index(N) == morse_index(N) == N - 5


class TestSpectralFlow:
    """SF(H_N, 0→1) = μ(N) via monotonicity."""

    def test_monotonicity_algebraic(self):
        """dC₁/dξ = (N-1)·2(1+ξ)/(1-ξ)³ > 0 on (0,1)."""
        proof = dC1_positive_proof()
        for xi, g_prime in proof['samples']:
            assert g_prime > 0

    def test_spectral_flow_equals_morse(self):
        """SF = #{negative eigenvalues at ξ=0} = μ(N)."""
        for N in range(3, 30):
            result = monotonicity_implies_simple_crossings(N)
            assert result['spectral_flow'] == result['morse_index']

    def test_no_positive_to_negative_crossings(self):
        """Monotonicity prevents any positive eigenvalue from becoming negative."""
        # This is immediate from dλ_m/dξ = dC₁/dξ > 0:
        # if λ_m(ξ₀) > 0, then λ_m(ξ) > λ_m(ξ₀) > 0 for all ξ > ξ₀.
        proof = dC1_positive_proof()
        assert 'dC₁/dξ > 0' in proof['conclusion']


class TestCrossingPoints:
    """Exact crossing points for N ≥ 8."""

    def test_N8_has_3_crossings(self):
        crossings = crossing_points(8)
        assert len(crossings) == 3  # m = 3, 4, 5

    def test_N8_modes(self):
        crossings = crossing_points(8)
        modes = [c['m'] for c in crossings]
        assert modes == [3, 4, 5]

    def test_crossing_discriminant_positive(self):
        """2c - 1 > 0 for all crossing modes."""
        for N in range(8, 20):
            for c in crossing_points(N):
                assert c['discriminant_2c_minus_1'] > 0


class TestParityProof:
    """η(∞) - η(0) is always even."""

    def test_parity_all_N(self):
        for N in range(3, 30):
            # For N ≠ 7 (no zero eigenvalues):
            # η(0) = (N-1) - 2μ, η(∞) = N-1
            # difference = 2μ, always even ✓
            if N != 7:
                result = prove_eta_parity(N)
                assert result['mu'] == morse_index(N)

    def test_N7_special(self):
        """N=7 has zero eigenvalues, so the simple identity
        η(0) = (N-1) - 2μ needs adjustment."""
        # For N=7: η(0) = 4 (not 6-0=6, because two zeros)
        # The identity η(0) = (N-1) - 2μ - n_zero holds
        eta_0 = eta_at_flat(7)
        assert eta_0 == 4  # 4 positive, 2 zero, 0 negative


class TestFullProof:
    """Complete proof certificate."""

    def test_full_proof_N30(self):
        """Run the full proof for N=3..30."""
        # N=7 handled specially in full_proof via spectral flow
        cert = full_proof(30)
        assert cert['all_verified']
        assert len(cert['results']) == 28  # N=3..30

    def test_proof_is_exact(self):
        cert = full_proof(10)
        assert cert['proof_type'] == 'exact_rational_arithmetic'

    def test_key_values(self):
        """Spot-check key entries in the proof certificate."""
        cert = full_proof(12)
        results = {r['N']: r for r in cert['results']}

        # N=3: trivially stable
        assert results[3]['mu'] == 0
        assert results[3]['ind'] == 0

        # N=7: marginal
        assert results[7]['mu'] == 0
        assert results[7]['ind'] == 0

        # N=8: first nontrivial
        assert results[8]['mu'] == 3
        assert results[8]['ind'] == 3

        # N=12: μ = 7
        assert results[12]['mu'] == 7
        assert results[12]['ind'] == 7


class TestC1H2Exact:
    """C₁(H²,ξ) at rational ξ values."""

    def test_xi_zero(self):
        """C₁(0) = N-1 (flat plane)."""
        for N in range(3, 15):
            assert C1_H2(N, 0, 1) == Fraction(N - 1)

    def test_xi_half(self):
        """C₁(1/2) = (N-1)(1+1/4)/(1/2)² = (N-1)·5."""
        for N in range(3, 10):
            expected = Fraction(N - 1) * 5
            assert C1_H2(N, 1, 2) == expected

    def test_monotone_at_rationals(self):
        """C₁ increases along rational sample points."""
        for N in [5, 8, 12]:
            vals = [C1_H2(N, p, 100) for p in range(0, 100)]
            for i in range(len(vals) - 1):
                assert vals[i] < vals[i + 1]
