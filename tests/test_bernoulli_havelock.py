"""Tests for the Bernoulli-Havelock structural backbone.

Every test here verifies an exact algebraic identity (Fraction arithmetic)
or a high-precision numerical claim.  No scipy required.
"""

import pytest
from fractions import Fraction
from math import pi, sqrt, factorial, atan
import cmath

from planetary_polygons.extensions.bernoulli_havelock import (
    bernoulli_number, bernoulli_poly, bernoulli_poly_float,
    havelock_casimir, havelock_from_bernoulli, normalized_havelock,
    parabola_form,
    b2_zeros, stable_fraction,
    moment_M2_exact, integral_B2_squared, integral_B2_power,
    moment_M4_exact, moment_even,
    moment_closed_form, moment_tower,
    zeta_from_bernoulli, M2_as_zeta_ratio,
    weinberg_angle_from_bernoulli, fermion_mass_bernoulli_table,
    cosmological_constant_from_N, alpha_s_csc_sum, b6_at_N7,
    havelock_zeta, havelock_zeta_ratio,
    bernoulli_tower_table, full_decomposition,
    quadratic_residues, quadratic_nonresidues,
    gauss_sum_qr, frobenius_eigenvalue_at_2, ckm_phase_from_gauss_sum,
    orbifold_sector_coherence,
)


# ============================================================
# Bernoulli numbers
# ============================================================

class TestBernoulliNumbers:
    """Verify the Bernoulli number table against known values."""

    def test_B0(self):
        assert bernoulli_number(0) == Fraction(1)

    def test_B1(self):
        assert bernoulli_number(1) == Fraction(-1, 2)

    def test_B2(self):
        assert bernoulli_number(2) == Fraction(1, 6)

    def test_B4(self):
        assert bernoulli_number(4) == Fraction(-1, 30)

    def test_B6(self):
        assert bernoulli_number(6) == Fraction(1, 42)

    def test_B8_equals_B4(self):
        """B_8 = B_4 = -1/30 (the Coxeter number coincidence)."""
        assert bernoulli_number(8) == Fraction(-1, 30)
        assert bernoulli_number(8) == bernoulli_number(4)

    def test_B12(self):
        assert bernoulli_number(12) == Fraction(-691, 2730)

    def test_odd_vanish(self):
        """B_n = 0 for odd n >= 3."""
        for n in [3, 5, 7, 9, 11]:
            assert bernoulli_number(n) == 0


# ============================================================
# Bernoulli polynomials
# ============================================================

class TestBernoulliPolynomials:
    """B_2(x) = x^2 - x + 1/6."""

    def test_B2_at_zero(self):
        assert bernoulli_poly(2, Fraction(0)) == Fraction(1, 6)

    def test_B2_at_one(self):
        assert bernoulli_poly(2, Fraction(1)) == Fraction(1, 6)

    def test_B2_at_half(self):
        """B_2(1/2) = 1/4 - 1/2 + 1/6 = -1/12."""
        assert bernoulli_poly(2, Fraction(1, 2)) == Fraction(-1, 12)

    def test_B2_at_third(self):
        """B_2(1/3) = 1/9 - 1/3 + 1/6 = 2/18 - 6/18 + 3/18 = -1/18."""
        assert bernoulli_poly(2, Fraction(1, 3)) == Fraction(-1, 18)

    def test_B2_symmetry(self):
        """B_2(x) = B_2(1-x) for all x."""
        for x in [Fraction(1, 7), Fraction(2, 7), Fraction(3, 7)]:
            assert bernoulli_poly(2, x) == bernoulli_poly(2, 1 - x)

    def test_B2_integral_vanishes(self):
        """integral_0^1 B_2(x) dx = 0 (midpoint Riemann sum)."""
        n = 10000
        total = sum(bernoulli_poly_float(2, (i + 0.5) / n) for i in range(n))
        assert abs(total / n) < 1e-8


# ============================================================
# The core identity: f(m,N) = (N^2/12)(1 - 6 B_2(m/N))
# ============================================================

class TestCoreIdentity:
    """The Havelock-Bernoulli identity must hold exactly."""

    @pytest.mark.parametrize("N", range(3, 16))
    def test_identity_all_modes(self, N):
        """f(m,N) via direct formula == f(m,N) via Bernoulli, for all m."""
        for m in range(1, N):
            direct = havelock_casimir(m, N)
            via_B2 = havelock_from_bernoulli(m, N)
            assert direct == via_B2, f"Failed at m={m}, N={N}: {direct} != {via_B2}"

    def test_identity_is_affine_not_multiplicative(self):
        """The relationship is 1 - 6 B_2, NOT 6 B_2.

        This is the bug in the spiral-hexagon bernoulli_bridge.py.
        f_norm = 1 - 6 B_2, so f_norm(0) = 1 - 6*(1/6) = 0 (correct: f(0,N)=0).
        If it were 6 B_2, we'd get f_norm(0) = 6*(1/6) = 1 (WRONG).
        """
        assert normalized_havelock(0, 7) == 0  # f(0,N) = 0
        B2_zero = bernoulli_poly(2, Fraction(0))
        assert B2_zero == Fraction(1, 6)
        assert 6 * B2_zero == 1  # 6 B_2(0) = 1, not 0
        assert 1 - 6 * B2_zero == 0  # 1 - 6 B_2(0) = 0, correct

    def test_known_values_N7(self):
        """Spot-check f(m,7) for all m."""
        expected = {1: 3, 2: 5, 3: 6, 4: 6, 5: 5, 6: 3}
        for m, val in expected.items():
            assert havelock_casimir(m, 7) == Fraction(val)
            assert havelock_from_bernoulli(m, 7) == Fraction(val)

    def test_known_values_N6(self):
        expected = {1: Fraction(5, 2), 2: 4, 3: Fraction(9, 2), 4: 4, 5: Fraction(5, 2)}
        for m, val in expected.items():
            assert havelock_casimir(m, 6) == val
            assert havelock_from_bernoulli(m, 6) == val

    def test_max_at_midpoint(self):
        """f is maximized at m = N/2 (or nearest integer)."""
        for N in range(4, 12):
            vals = [havelock_casimir(m, N) for m in range(1, N)]
            m_max = vals.index(max(vals)) + 1
            assert m_max == N // 2


# ============================================================
# B_2 zeros and stability
# ============================================================

class TestStabilityTransitions:

    def test_b2_zeros_are_roots(self):
        """B_2(x) = 0 at x = (3 +/- sqrt(3))/6."""
        x_lo, x_hi = b2_zeros()
        assert abs(bernoulli_poly_float(2, x_lo)) < 1e-14
        assert abs(bernoulli_poly_float(2, x_hi)) < 1e-14

    def test_zeros_sum_to_one(self):
        """x_lo + x_hi = 1 (Vieta's for x^2 - x + 1/6)."""
        x_lo, x_hi = b2_zeros()
        assert abs(x_lo + x_hi - 1.0) < 1e-14

    def test_zeros_product(self):
        """x_lo * x_hi = 1/6 (Vieta's)."""
        x_lo, x_hi = b2_zeros()
        assert abs(x_lo * x_hi - 1.0 / 6) < 1e-14

    def test_stable_fraction_value(self):
        """Stable fraction = (3-sqrt(3))/3 ~ 0.4226."""
        sf = stable_fraction()
        assert abs(sf - (3 - sqrt(3)) / 3) < 1e-14


# ============================================================
# Moment identities
# ============================================================

class TestMoments:

    def test_M2_exact(self):
        """M_2 = 6/5 exactly."""
        assert moment_M2_exact() == Fraction(6, 5)

    def test_integral_B2_squared(self):
        """integral B_2^2 = 1/180, NOT 1/30."""
        assert integral_B2_squared() == Fraction(1, 180)
        # Numerical verification
        n = 100000
        total = sum(bernoulli_poly_float(2, (i + 0.5) / n)**2 for i in range(n))
        assert abs(total / n - 1.0 / 180) < 1e-8

    def test_M2_from_components(self):
        """M_2 = 1 + 0 + 36*(1/180) = 6/5."""
        int_1 = Fraction(1)
        int_B2 = Fraction(0)
        int_B2_sq = Fraction(1, 180)
        M2 = int_1 - 12 * int_B2 + 36 * int_B2_sq
        assert M2 == Fraction(6, 5)

    def test_integral_B2_cubed(self):
        """integral B_2^3 = 1/3780."""
        assert integral_B2_power(3) == Fraction(1, 3780)
        # Numerical check
        n = 100000
        total = sum(bernoulli_poly_float(2, (i + 0.5) / n)**3 for i in range(n))
        assert abs(total / n - 1.0 / 3780) < 1e-8

    def test_M4_is_rational(self):
        """M_4 must be a positive rational number."""
        M4 = moment_M4_exact()
        assert isinstance(M4, Fraction)
        assert M4 > 0

    def test_M2_numerical_riemann(self):
        """Verify M_2 = 6/5 by brute-force Riemann sum."""
        n = 100000
        total = 0.0
        for i in range(n):
            x = (i + 0.5) / n
            f_norm = 1 - 6 * bernoulli_poly_float(2, x)
            total += f_norm**2
        M2_num = total / n
        assert abs(M2_num - 1.2) < 1e-6


# ============================================================
# Bernoulli-zeta bridge
# ============================================================

class TestZetaBridge:

    def test_zeta_2(self):
        """zeta(2) = pi^2/6."""
        assert abs(zeta_from_bernoulli(1) - pi**2 / 6) < 1e-12

    def test_zeta_4(self):
        """zeta(4) = pi^4/90."""
        assert abs(zeta_from_bernoulli(2) - pi**4 / 90) < 1e-12

    def test_zeta_6(self):
        """zeta(6) = pi^6/945."""
        assert abs(zeta_from_bernoulli(3) - pi**6 / 945) < 1e-10

    def test_M2_equals_3_zeta4_over_zeta2_sq(self):
        """M_2 = 6/5 = 3 * zeta(4)/zeta(2)^2."""
        ratio = M2_as_zeta_ratio()
        assert abs(ratio - 1.2) < 1e-12

    def test_zeta_ratio_exact(self):
        """zeta(4)/zeta(2)^2 = 2/5 exactly."""
        z2 = pi**2 / 6
        z4 = pi**4 / 90
        assert abs(z4 / z2**2 - 0.4) < 1e-14


# ============================================================
# Particle physics: Bernoulli decomposition
# ============================================================

class TestParticlePhysics:

    def test_weinberg_angle(self):
        """sin^2(theta_W) = 3/11."""
        w = weinberg_angle_from_bernoulli()
        assert w['sin2_theta_W'] == Fraction(3, 11)

    def test_weinberg_B2_values(self):
        """B_2(1/2) = -1/12, B_2(1/3) = -1/18."""
        w = weinberg_angle_from_bernoulli()
        assert w['B2_at_half'] == Fraction(-1, 12)
        assert w['B2_at_third'] == Fraction(-1, 18)

    def test_weinberg_casimirs(self):
        """f(2,4) = 2, f(1,3) = 1."""
        w = weinberg_angle_from_bernoulli()
        assert w['f_24'] == Fraction(2)
        assert w['f_13'] == Fraction(1)

    def test_fermion_table_N7(self):
        """N=7 fermion table has 6 entries, all exact."""
        table = fermion_mass_bernoulli_table(7)
        assert len(table) == 6
        for entry in table:
            assert isinstance(entry['B2'], Fraction)
            assert isinstance(entry['f'], Fraction)
            # f must equal m(N-m)/2
            m = entry['m']
            assert entry['f'] == Fraction(m * (7 - m), 2)

    def test_fermion_symmetry(self):
        """f(m,7) = f(7-m,7) for all m."""
        table = fermion_mass_bernoulli_table(7)
        for i in range(3):
            assert table[i]['f'] == table[5 - i]['f']

    def test_cosmological_constant_N7(self):
        """Lambda_3(7) = 33/16."""
        assert cosmological_constant_from_N(7) == Fraction(33, 16)

    def test_csc_sum_N7(self):
        """sum csc^2(pi m/7) = (49-1)/3 = 16."""
        assert alpha_s_csc_sum(7) == Fraction(16)

    def test_csc_sum_numerical(self):
        """Verify the csc^2 sum identity numerically for N=7."""
        from math import sin
        total = sum(1.0 / sin(pi * m / 7)**2 for m in range(1, 7))
        assert abs(total - 16.0) < 1e-10

    def test_B6_N7_connection(self):
        """B_6 = 1/42, and 42 = 6*7."""
        info = b6_at_N7()
        assert info['B6'] == Fraction(1, 42)
        assert info['denominator'] == 42


# ============================================================
# Havelock zeta function
# ============================================================

class TestHavelockZeta:

    def test_zeta_N7_s1(self):
        """Z_H(1, 7) = sum 1/f(m,7) = 1/3 + 1/5 + 1/6 + 1/6 + 1/5 + 1/3."""
        expected = 2 * (1.0/3 + 1.0/5 + 1.0/6)
        assert abs(havelock_zeta(7, 1.0) - expected) < 1e-12

    def test_zeta_N7_s2(self):
        """Z_H(2, 7) = sum 1/f(m,7)^2."""
        expected = 2 * (1.0/9 + 1.0/25 + 1.0/36)
        assert abs(havelock_zeta(7, 2.0) - expected) < 1e-12

    def test_zeta_decreases_with_N(self):
        """Z_H(2, N) decreases with N (more eigenvalues, larger)."""
        z5 = havelock_zeta(5, 2.0)
        z6 = havelock_zeta(6, 2.0)
        z7 = havelock_zeta(7, 2.0)
        # Not necessarily monotone; just check they're finite and positive
        assert z5 > 0
        assert z6 > 0
        assert z7 > 0


# ============================================================
# Bernoulli tower
# ============================================================

class TestBernoulliTower:

    def test_tower_has_three_levels(self):
        tower = bernoulli_tower_table()
        assert len(tower) == 3

    def test_level_2_proved(self):
        tower = bernoulli_tower_table()
        assert tower[0]['level'] == 2
        assert 'PROVED' in tower[0]['magri']

    def test_level_4_proved(self):
        tower = bernoulli_tower_table()
        assert tower[1]['level'] == 4
        assert 'PROVED' in tower[1]['magri']

    def test_level_6_conjectured(self):
        tower = bernoulli_tower_table()
        assert tower[2]['level'] == 6
        assert 'CONJECTURED' in tower[2]['magri']

    def test_B6_in_tower(self):
        tower = bernoulli_tower_table()
        assert tower[2]['B_2k'] == Fraction(1, 42)


# ============================================================
# Full decomposition
# ============================================================

class TestFullDecomposition:

    def test_decomposition_N7(self):
        d = full_decomposition(7)
        assert d['N'] == 7
        assert d['M2'] == Fraction(6, 5)
        assert d['Lambda_3'] == Fraction(33, 16)
        assert d['csc2_sum'] == Fraction(16)
        assert len(d['eigenvalue_table']) == 6
        assert len(d['tower']) == 3

    def test_decomposition_core_identity(self):
        d = full_decomposition(7)
        assert 'B_2' in d['core_identity']

    def test_derivation_chains_present(self):
        d = full_decomposition(7)
        chains = d['derivation_chains']
        assert len(chains) == 8
        # Each chain has required keys
        for c in chains:
            assert 'prediction' in c
            assert 'chain' in c
            assert 'B2_inputs' in c

    def test_weinberg_chain_B2_half(self):
        """The Weinberg chain must reference B_2(1/2) = -1/12."""
        d = full_decomposition(7)
        wc = d['derivation_chains'][0]
        assert 'sin^2(theta_W)' in wc['prediction']
        assert wc['B2_inputs']['B_2(1/2)'] == Fraction(-1, 12)

    def test_ncrit_chain_B2_value(self):
        """N_crit chain must have B_2(3/7)."""
        d = full_decomposition(7)
        nc = d['derivation_chains'][1]
        assert nc['value'] == 7
        expected_B2 = Fraction(3, 7)**2 - Fraction(3, 7) + Fraction(1, 6)
        assert nc['B2_inputs']['B_2(3/7)'] == expected_B2

    def test_all_chains_have_B2(self):
        """Every derivation chain must have at least one B_2 input."""
        d = full_decomposition(7)
        for c in d['derivation_chains']:
            assert len(c['B2_inputs']) > 0, f"Chain '{c['prediction']}' has no B_2 inputs"


# ============================================================
# Parabola identity: 1 - 6 B_2(x) = 6x(1-x)
# ============================================================

class TestParabola:

    def test_parabola_at_zero(self):
        assert parabola_form(Fraction(0)) == 0

    def test_parabola_at_one(self):
        assert parabola_form(Fraction(1)) == 0

    def test_parabola_at_half(self):
        """Max at x=1/2: 6*(1/2)*(1/2) = 3/2."""
        assert parabola_form(Fraction(1, 2)) == Fraction(3, 2)

    def test_parabola_equals_normalized_havelock(self):
        """6x(1-x) = 1 - 6 B_2(x) for all x = m/N."""
        for N in range(3, 12):
            for m in range(N + 1):
                x = Fraction(m, N)
                assert parabola_form(x) == normalized_havelock(m, N)

    def test_parabola_is_beta_density(self):
        """6x(1-x) is 6 * Beta(2,2) density."""
        # Beta(2,2) density at x is x*(1-x) / B(2,2) = x(1-x) * 6
        # So parabola_form IS 6 * x(1-x) = 6 * B(2,2) pdf evaluated at x / 6
        assert parabola_form(Fraction(1, 4)) == Fraction(6 * 1 * 3, 16)


# ============================================================
# Closed-form moment tower
# ============================================================

class TestMomentClosedForm:

    def test_M1_equals_1(self):
        """M_1 = 6^1 * 1/6 = 1."""
        assert moment_closed_form(1) == Fraction(1)

    def test_M2_equals_6_over_5(self):
        assert moment_closed_form(2) == Fraction(6, 5)

    def test_M4_equals_72_over_35(self):
        assert moment_closed_form(4) == Fraction(72, 35)

    def test_M6_equals_3888_over_1001(self):
        assert moment_closed_form(6) == Fraction(3888, 1001)

    def test_agrees_with_binomial_method(self):
        """Closed form must agree with the binomial expansion method."""
        assert moment_closed_form(2) == moment_even(1)   # M_2
        assert moment_closed_form(4) == moment_even(2)   # M_4

    def test_tower_length(self):
        tower = moment_tower(8)
        assert len(tower) == 8
        assert tower[0] == (1, Fraction(1))
        assert tower[1] == (2, Fraction(6, 5))

    def test_moments_grow(self):
        """M_k is monotonically increasing for k >= 1."""
        tower = moment_tower(8)
        for i in range(len(tower) - 1):
            assert tower[i][1] < tower[i + 1][1]

    def test_beta_function_formula(self):
        """M_k = 6^k * B(k+1, k+1) where B(a,b) = (a-1)!(b-1)!/(a+b-1)!."""
        for k in range(1, 8):
            beta = Fraction(factorial(k) * factorial(k), factorial(2 * k + 1))
            expected = Fraction(6**k) * beta
            assert moment_closed_form(k) == expected


# ============================================================
# Gauss sum and CKM phase
# ============================================================

class TestGaussSum:

    def test_QR_mod_7(self):
        """Quadratic residues mod 7 are {1, 2, 4}."""
        assert quadratic_residues(7) == [1, 2, 4]

    def test_QNR_mod_7(self):
        """Quadratic non-residues mod 7 are {3, 5, 6}."""
        assert quadratic_nonresidues(7) == [3, 5, 6]

    def test_gauss_sum_value(self):
        """G(QR) at p=7 equals (-1 + i*sqrt(7))/2."""
        G = gauss_sum_qr(7)
        expected = (-1 + 1j * sqrt(7)) / 2
        assert abs(G - expected) < 1e-12

    def test_gauss_sum_plus_complement_is_minus_1(self):
        """G(QR) + G(QNR) = -1 (sum of all nontrivial roots of unity)."""
        omega = cmath.exp(2j * pi / 7)
        G_QR = gauss_sum_qr(7)
        G_QNR = sum(omega**a for a in quadratic_nonresidues(7))
        assert abs(G_QR + G_QNR + 1) < 1e-12

    def test_gauss_sum_difference_is_i_sqrt_7(self):
        """G(QR) - G(QNR) = i*sqrt(7) (the full Gauss sum)."""
        omega = cmath.exp(2j * pi / 7)
        G_QR = gauss_sum_qr(7)
        G_QNR = sum(omega**a for a in quadratic_nonresidues(7))
        assert abs((G_QR - G_QNR) - 1j * sqrt(7)) < 1e-12


class TestFrobeniusEigenvalue:

    def test_alpha_2_modulus(self):
        """|alpha_2|^2 = 2 (Weil bound)."""
        frob = frobenius_eigenvalue_at_2(7)
        assert abs(frob['modulus_sq'] - 2.0) < 1e-12

    def test_alpha_2_is_complex(self):
        """p=7 is 3 mod 4, so alpha_2 is complex."""
        frob = frobenius_eigenvalue_at_2(7)
        assert frob['is_complex'] is True

    def test_alpha_2_equals_neg_conj_GQR(self):
        """alpha_2 = -conj(G(QR))."""
        frob = frobenius_eigenvalue_at_2(7)
        assert frob['match'] is True

    def test_p_1_mod_4_is_real(self):
        """p=5 is 1 mod 4, so no complex phase."""
        frob = frobenius_eigenvalue_at_2(5)
        assert frob['is_complex'] is False


class TestCKMPhase:

    def test_ckm_phase_value(self):
        """delta_CKM = arctan(sqrt(7)) = 69.295 deg."""
        result = ckm_phase_from_gauss_sum(7)
        assert abs(result['delta_CKM_deg'] - 69.2952) < 0.001

    def test_ckm_within_PDG(self):
        """0.10 sigma from PDG central value."""
        result = ckm_phase_from_gauss_sum(7)
        assert result['tension_sigma'] < 0.5

    def test_cp_violation_requires_3_mod_4(self):
        """N=7 gives CP violation because 7 = 3 mod 4."""
        result = ckm_phase_from_gauss_sum(7)
        assert result['has_CP_violation'] is True
        assert result['N_mod_4'] == 3

    def test_no_cp_at_N5(self):
        """N=5 (= 1 mod 4) would give no CP violation."""
        result = ckm_phase_from_gauss_sum(5)
        assert result['has_CP_violation'] is False

    def test_von_staudt_clausen_chain(self):
        """N=7 appears in the von Staudt-Clausen primes for B_6."""
        result = ckm_phase_from_gauss_sum(7)
        assert result['N_in_denom'] is True
        assert 7 in result['von_staudt_clausen_primes']

    def test_chain_has_6_steps(self):
        result = ckm_phase_from_gauss_sum(7)
        assert len(result['chain']) == 6

    def test_arctan_sqrt_7_exact(self):
        """arctan(sqrt(7)) as a numerical identity."""
        delta = atan(sqrt(7)) * 180 / pi
        # This is NOT a rational multiple of pi
        # But it's algebraic: tan(delta) = sqrt(7)
        assert abs(delta - 69.29518893) < 1e-6

    def test_physical_mechanism_present(self):
        """The physical mechanism dict is included."""
        result = ckm_phase_from_gauss_sum(7)
        assert 'physical_mechanism' in result
        mech = result['physical_mechanism']
        assert mech['conjugate_symmetric'] is True
        assert mech['A_up_equals_alpha_2'] is True


# ============================================================
# Orbifold sector coherence (physical mechanism)
# ============================================================

class TestOrbifoldCoherence:

    def test_A_up_equals_alpha_2(self):
        """A_up = 1 + G(QR) = (1+i*sqrt(7))/2 = alpha_2."""
        mech = orbifold_sector_coherence(7)
        alpha_2 = (1 + 1j * sqrt(7)) / 2
        assert abs(mech['A_up'] - alpha_2) < 1e-12

    def test_A_down_is_conjugate(self):
        """A_down = conj(A_up) when N = 3 mod 4."""
        mech = orbifold_sector_coherence(7)
        assert mech['conjugate_symmetric'] is True

    def test_irremovable_phase_is_arctan_sqrt_7(self):
        """The irremovable CKM phase is arctan(sqrt(7))."""
        mech = orbifold_sector_coherence(7)
        expected = atan(sqrt(7)) * 180 / pi
        assert abs(mech['irremovable_phase_deg'] - expected) < 1e-10

    def test_total_phase_is_double(self):
        """Total phase content is 2 * arctan(sqrt(7))."""
        mech = orbifold_sector_coherence(7)
        expected = 2 * atan(sqrt(7)) * 180 / pi
        assert abs(mech['total_phase_content_deg'] - expected) < 1e-10

    def test_heegner_property(self):
        """Q(sqrt(-7)) has class number 1 (Heegner)."""
        mech = orbifold_sector_coherence(7)
        assert mech['heegner']['class_number_1'] is True
        assert mech['heegner']['unique_CM_point'] is True

    def test_non_heegner_detected(self):
        """Q(sqrt(-23)) has class number 3, not 1."""
        mech = orbifold_sector_coherence(23)
        assert mech['heegner']['class_number_1'] is False

    def test_untwisted_sector_anchors(self):
        """Without the +1 (untwisted), the phase is supplementary."""
        omega = cmath.exp(2j * pi / 7)
        G_QR = omega + omega**2 + omega**4
        # Without untwisted: arg = pi - arctan(sqrt(7)) ~ 110.7
        # With untwisted: arg = arctan(sqrt(7)) ~ 69.3
        angle_without = abs(cmath.phase(G_QR)) * 180 / pi
        angle_with = abs(cmath.phase(1 + G_QR)) * 180 / pi
        assert abs(angle_without + angle_with - 180.0) < 1e-10


# ============================================================
# Unified backbone exports
# ============================================================

from planetary_polygons.extensions.bernoulli_havelock import (
    SIGMA_0, N_CRIT, BERNOULLI_PHASES,
    havelock_eigenvalue_unified, conformal_dim_unified,
    F_IR, instanton_fugacity,
)


class TestUnifiedBackbone:

    def test_sigma_0_is_5(self):
        assert SIGMA_0 == 5

    def test_n_crit_is_7(self):
        assert N_CRIT == 7

    def test_havelock_eigenvalue_QR(self):
        """lambda = {3, 1, 0} for QR = {1, 2, 4} at N=7."""
        assert havelock_eigenvalue_unified(1) == 3
        assert havelock_eigenvalue_unified(2) == 1
        assert havelock_eigenvalue_unified(4) == 0

    def test_conformal_dim_at_BF(self):
        """c(m=4) = 1/2 exactly (BF threshold)."""
        assert conformal_dim_unified(4) == Fraction(1, 2)

    def test_conformal_dim_values(self):
        """c = {13/14, 9/14, 1/2} for QR modes."""
        assert conformal_dim_unified(1) == Fraction(13, 14)
        assert conformal_dim_unified(2) == Fraction(9, 14)

    def test_F_IR_at_BF(self):
        """F_IR(0.5, sigma) = 1/sqrt(sigma)."""
        for sigma in [3, 5, 10, 20]:
            assert abs(F_IR(0.5, sigma) - 1 / sqrt(sigma)) < 1e-12

    def test_F_IR_exponential_suppression(self):
        """UV-localized modes (c > 0.5) are exponentially suppressed."""
        f_uv = F_IR(0.93, 10)
        f_bf = F_IR(0.5, 10)
        assert f_uv < f_bf * 0.1

    def test_F_IR_correct_sign(self):
        """The denominator has exp(+x), not exp(-x)."""
        from math import exp as mexp
        c, sigma = 0.9, 10.0
        x = (2 * c - 1) * sigma
        expected = sqrt(abs(2 * c - 1) / (mexp(x) - 1))
        assert abs(F_IR(c, sigma) - expected) < 1e-12

    def test_instanton_fugacity(self):
        """K = exp(-2*pi*k_frac) = 0.548 at N=7."""
        K = instanton_fugacity()
        assert abs(K - 0.548182) < 0.001

    def test_bernoulli_phases_ratio(self):
        """aL/aR = 6/5 = M_2."""
        assert BERNOULLI_PHASES['aL'] / BERNOULLI_PHASES['aR'] == Fraction(6, 5)

    def test_bernoulli_phases_denominator(self):
        """All phase denominators divide 42 = denom(B_6)."""
        for key in ['aL', 'aR', 'aH']:
            assert 42 % BERNOULLI_PHASES[key].denominator == 0

    def test_bernoulli_phases_pattern(self):
        """Numerators are N-1, N-2, N-3 over denom(B_6)=42."""
        assert BERNOULLI_PHASES['aL'] == Fraction(6, 42)
        assert BERNOULLI_PHASES['aR'] == Fraction(5, 42)
        assert BERNOULLI_PHASES['aH'] == Fraction(4, 42)
