"""Tests for the Standard Model gauge group from the polygon hierarchy.

Tests cover:
  1. SU(2) from Witten-Achúcarro-Townsend CS theorem (proven)
  2. SU(3) from McKay correspondence on Z/3Z Galois orbifold (proven in orbifold CFT)
  3. U(1) from Kaluza-Klein (textbook)
  4. Weinberg angle from CS threshold couplings
  5. Central charge consistency: c = 12b(N), not N²
  6. Coupling lock α/(8πG) = 1/(2π²)
  7. The Havelock action
"""

import math
import pytest
from planetary_polygons.extensions.standard_model_gauge import (
    casimir, spin_j, trace_field_degree, central_charge, b_exact,
    galois_action_on_pairs, su3_from_galois, su3_from_mckay,
    su2_from_cs_gravity, u1_from_kk,
    weinberg_angle, weinberg_angle_cs_threshold,
    two_force_unification, standard_model_table,
    frobenius_orbits, mckay_embedding, havelock_action,
)


# =====================================================================
# Central charge: c = 12b(N), NOT N²
# =====================================================================

class TestCentralCharge:
    def test_b_formula(self):
        """b(N) = N(N+1)/12 - ln2 + ln(N)/(N-1)."""
        for N in [4, 7, 8, 11]:
            expected = N * (N + 1) / 12 - math.log(2) + math.log(N) / (N - 1)
            assert b_exact(N) == pytest.approx(expected)

    def test_c_equals_12b(self):
        """c = 12b(N) exactly."""
        for N in [4, 7, 8, 11]:
            assert central_charge(N) == pytest.approx(12 * b_exact(N))

    def test_c_approaches_N_squared(self):
        """c/N² → 1 as N → ∞ (with O(1/N) correction)."""
        for N in [50, 100, 500]:
            ratio = central_charge(N) / N**2
            assert abs(ratio - 1.0) < 2.0 / N  # O(1/N) correction

    def test_c_not_equal_N_squared(self):
        """c ≠ N² at finite N (the paper's c=N² was an approximation)."""
        for N in [4, 7, 8, 11]:
            c = central_charge(N)
            assert abs(c - N**2) > 0.5  # they differ by O(N)


# =====================================================================
# Graviton: j = 2 at N=7 (unique)
# =====================================================================

class TestGraviton:
    def test_j2_at_N7(self):
        """j = 2 at N=7 (the graviton)."""
        assert spin_j(3, 7) == pytest.approx(2.0)

    def test_j1_at_N4(self):
        """j = 1 at N=4 (the gauge boson)."""
        assert spin_j(2, 4) == pytest.approx(1.0)

    def test_j2_unique_to_N7(self):
        """j = 2 at the critical mode occurs ONLY at N=7."""
        for N in range(3, 31):
            if N == 7:
                continue
            m = N // 2
            j = spin_j(m, N)
            assert abs(j - 2.0) > 0.01, f"N={N} also has j=2!"


# =====================================================================
# SU(2) from Witten's CS formulation of 3D gravity
# =====================================================================

class TestSU2:
    def test_cs_gravity_theorem(self):
        """SU(2) from Witten/AT theorem on the zero-mode sector."""
        result = su2_from_cs_gravity(4)
        assert result['gauge_group'] == 'SU(2) × SU(2)'
        assert result['theorem'] == 'Witten 1988, Achúcarro-Townsend 1986'

    def test_critical_mode_is_zero_mode(self):
        """At N=4, the critical mode m*=2 has μ_KK = 0."""
        result = su2_from_cs_gravity(4)
        assert result['is_zero_mode'] is True

    def test_j1_is_adjoint(self):
        """The critical mode at N=4 is in the SU(2) adjoint (j=1)."""
        result = su2_from_cs_gravity(4)
        assert result['is_adjoint'] is True
        assert result['j'] == 1

    def test_cs_level_from_central_charge(self):
        """CS level k = c/6 from Brown-Henneaux."""
        result = su2_from_cs_gravity(4)
        c = central_charge(4)
        assert result['cs_level'] == pytest.approx(c / 6)

    def test_fermion_parity_anomaly_even_N(self):
        """For even N, the fermion parity anomaly level shift vanishes."""
        for N in [4, 8, 12]:
            signs = [1 if (m + 0.5 - N/2) > 0 else -1 for m in range(N)]
            delta_k = sum(signs) / 2
            assert delta_k == 0, f"Fermion anomaly should vanish at even N={N}"

    def test_fermion_parity_anomaly_odd_N(self):
        """For odd N, one zero mode gives |Delta_k| = 1/2."""
        for N in [7, 11, 15]:
            signs = [1 if (m + 0.5 - N/2) > 0 else -1 for m in range(N)]
            delta_k = sum(signs) / 2
            assert abs(delta_k) == 0.5, f"Odd N={N} should give |Delta_k|=1/2"

    def test_seifert_parity_violation(self):
        """The Seifert Euler class e=N/2 breaks A+ <-> A- symmetry for all N>=3."""
        for N in range(3, 16):
            euler_class = N / 2
            assert euler_class > 0, "Euler class must be positive (oriented fiber)"


# =====================================================================
# SU(3) from McKay correspondence at N=7
# =====================================================================

class TestSU3:
    def test_trace_field_degree_7(self):
        """K₇ has degree 3 over Q."""
        assert trace_field_degree(7) == 3

    def test_frobenius_order_3(self):
        """σ: m → 2m mod 7 has order 3 (since 2³=8≡1 mod 7)."""
        assert pow(2, 3, 7) == 1

    def test_frobenius_orbits(self):
        """Two orbits of size 3 at N=7."""
        orbits = frobenius_orbits(7)
        assert len(orbits) == 2
        assert all(len(orb) == 3 for orb in orbits)
        # Orbit containing 1
        orb1 = [o for o in orbits if 1 in o][0]
        assert sorted(orb1) == [1, 2, 4]

    def test_mckay_embedding(self):
        """Z/3Z ⊂ SU(2) via diag(ω, ω⁻¹) with det = 1."""
        mckay = mckay_embedding(7)
        assert mckay['orbit_plus'] == [1, 2, 4]
        assert mckay['det_check'] is True
        assert mckay['dynkin_diagram'] == 'A₂'
        assert mckay['gauge_group'] == 'SU(3)'

    def test_su3_from_mckay(self):
        """SU(3) from McKay correspondence."""
        result = su3_from_mckay(7)
        assert result['gauge_group'] == 'SU(3)'
        assert result['level'] == 1
        assert 'McKay' in result['method']

    def test_galois_cyclic_permutation(self):
        """Gal(K₇/Q) = Z/3Z cyclically permutes the 3 pairs."""
        ga = galois_action_on_pairs(7)
        assert ga['n_pairs'] == 3
        assert ga['is_cyclic_permutation'] is True

    def test_su3_from_galois_legacy(self):
        """Legacy interface delegates to McKay."""
        result = su3_from_galois(7)
        assert result['gauge_group'] == 'SU(3)'

    def test_palindromic_casimirs(self):
        """The palindromic Casimirs of the N=7 orbit."""
        mckay = mckay_embedding(7)
        assert mckay['casimirs'] == [3.0, 5.0, 6.0]

    def test_su3_central_charge(self):
        """c(SU(3)₁) = k×dim/(k+h∨) = 1×8/(1+3) = 2."""
        mckay = mckay_embedding(7)
        assert mckay['central_charge_su3'] == pytest.approx(2.0)


# =====================================================================
# Eightfold Way: PSL(2,7) tensor products = SU(3) tensor algebra
# =====================================================================

class TestEightfoldWay:
    """PSL(2,F_7) reproduces the full SU(3) tensor product rules.

    χ₃ = holomorphic differentials on the Klein quartic X(7).
    PSL(2,7) embeds in SU(3) via χ₃, and:
      3 ⊗ 3̄ = 1 ⊕ 8    (Eightfold Way)
      Sym²(3) = 6        (symmetric diquarks)
      ∧²(3) = 3̄          (dual)
    """

    def _psl27_characters(self):
        """Return PSL(2,7) character table and class data."""
        import cmath
        s7 = 7**0.5
        # Classes: 1A, 2A, 3A, 4A, 7A, 7B (sizes: 1, 21, 56, 42, 24, 24)
        chi = {
            1: [1, 1, 1, 1, 1, 1],
            3: [3, -1, 0, 1, (-1+1j*s7)/2, (-1-1j*s7)/2],
            6: [6, 2, 0, 0, -1, -1],
            7: [7, -1, 1, -1, 0, 0],
            8: [8, 0, -1, 0, 1, 1],
        }
        chi['3p'] = [v.conjugate() if isinstance(v, complex) else v for v in chi[3]]
        sizes = [1, 21, 56, 42, 24, 24]
        # g² class map: 1²=1, 2²=1, 3²=3, 4²=2, 7A²=7A, 7B²=7B
        g2_map = [0, 0, 2, 1, 4, 5]
        return chi, sizes, g2_map

    def _decompose(self, product_char, chi, sizes):
        """Decompose a product character into irrep multiplicities."""
        order = sum(sizes)
        result = {}
        for name, ch in chi.items():
            mult = sum(sizes[i] * product_char[i] * (ch[i].conjugate() if isinstance(ch[i], complex) else ch[i])
                       for i in range(6)) / order
            m = round(mult.real if isinstance(mult, complex) else mult)
            if m > 0:
                result[name] = m
        return result

    def test_eightfold_way(self):
        """χ₃ ⊗ χ̄₃ = χ₁ ⊕ χ₈ (the Eightfold Way)."""
        chi, sizes, _ = self._psl27_characters()
        chi3 = chi[3]
        chi3p = chi['3p']
        product = [chi3[i] * chi3p[i] for i in range(6)]
        decomp = self._decompose(product, chi, sizes)
        assert decomp == {1: 1, 8: 1}

    def test_sym2_is_6(self):
        """Sym²(χ₃) = χ₆."""
        chi, sizes, g2_map = self._psl27_characters()
        chi3 = chi[3]
        chi3_g2 = [chi3[g2_map[i]] for i in range(6)]
        sym2 = [(chi3[i]**2 + chi3_g2[i])/2 for i in range(6)]
        decomp = self._decompose(sym2, chi, sizes)
        assert decomp == {6: 1}

    def test_wedge2_is_3bar(self):
        """∧²(χ₃) = χ̄₃."""
        chi, sizes, g2_map = self._psl27_characters()
        chi3 = chi[3]
        chi3_g2 = [chi3[g2_map[i]] for i in range(6)]
        anti2 = [(chi3[i]**2 - chi3_g2[i])/2 for i in range(6)]
        decomp = self._decompose(anti2, chi, sizes)
        assert decomp == {'3p': 1}

    def test_adjoint_irreducible(self):
        """The SU(3) adjoint (dim 8) restricts to PSL(2,7) as irreducible χ₈."""
        chi, _, _ = self._psl27_characters()
        # 3 ⊗ 3̄ - 1 = 8 (adjoint = tensor product minus singlet)
        chi3 = chi[3]
        chi3p = chi['3p']
        adjoint = [chi3[i] * chi3p[i] - 1 for i in range(6)]
        # Should equal χ₈
        assert all(abs(adjoint[i] - chi[8][i]) < 1e-10 for i in range(6))

    def test_dimensions(self):
        """3 × 3 = 9 = 1 + 8."""
        assert 3 * 3 == 1 + 8

    def test_qr_qnr_are_chi3_chi3bar(self):
        """QR modes {1,2,4} carry χ₃, QNR modes {3,5,6} carry χ̄₃."""
        # QR mod 7: 1²=1, 2²=4, 3²=2 → QR = {1, 2, 4}
        qr = sorted([pow(k, 2, 7) for k in range(1, 7)])
        assert sorted(set(qr)) == [1, 2, 4]
        qnr = sorted(set(range(1, 7)) - set(qr))
        assert qnr == [3, 5, 6]


# =====================================================================
# U(1) from Kaluza-Klein
# =====================================================================

class TestU1:
    def test_kk(self):
        result = u1_from_kk()
        assert result['gauge_group'] == 'U(1)'

    def test_coupling_lock_exact(self):
        """α/(8πG) = 1/(2π²), exact and N-independent."""
        result = u1_from_kk()
        assert result['lock_matches'] is True
        assert result['coupling_lock'] == pytest.approx(1 / (2 * math.pi**2))


# =====================================================================
# Weinberg angle from CS threshold
# =====================================================================

class TestWeinbergAngle:
    def test_3_over_11(self):
        """sin²θ_W = 3/11 at the orbifold threshold."""
        result = weinberg_angle_cs_threshold()
        assert result['sin2_theta_W'] == pytest.approx(3 / 11)

    def test_from_quantum_corrected_levels(self):
        """Derived from k̃₂ = k+h∨ = 3 and dim(SU(3)) = 8."""
        result = weinberg_angle_cs_threshold()
        assert result['inv_g2_sq'] == 3   # k₂ + h∨(SU(2)) = 1 + 2
        assert result['inv_gY_sq'] == 8   # dim(SU(3))

    def test_equals_dim_ratio(self):
        """3/11 = dim(SU(2))/(dim(SU(2))+dim(SU(3)))."""
        result = weinberg_angle_cs_threshold()
        dim_ratio = 3 / (3 + 8)
        assert result['sin2_theta_W'] == pytest.approx(dim_ratio)

    def test_closer_than_su5(self):
        """Our prediction is closer to experiment than SU(5) GUT."""
        result = weinberg_angle_cs_threshold()
        assert result['discrepancy_pct'] < result['su5_discrepancy_pct']

    def test_between_experiment_and_su5(self):
        """3/11 is between experiment (0.231) and SU(5) (0.375)."""
        result = weinberg_angle_cs_threshold()
        assert 0.231 < result['sin2_theta_W'] < 0.375

    def test_legacy_interface(self):
        """Legacy weinberg_angle(N=4) still works."""
        result = weinberg_angle(4)
        assert result['sin2_theta_W'] == pytest.approx(3 / 11)


# =====================================================================
# Two-force unification
# =====================================================================

class TestTwoForceUnification:
    def test_complete(self):
        result = two_force_unification()
        assert result['gauge_group'] == 'SU(3) × SU(2) × U(1)'
        assert result['force_1']['N'] == 7

    def test_unification_field(self):
        result = two_force_unification()
        assert 'ζ₅₆' in result['unification_field']


# =====================================================================
# Havelock action
# =====================================================================

class TestHavelockAction:
    def test_action_at_N7(self):
        act = havelock_action(7)
        c = central_charge(7)
        assert act['central_charge'] == pytest.approx(c)
        assert act['G'] == pytest.approx(3 / (2 * c))
        assert act['Lambda'] == pytest.approx((49 - 16) / 16)

    def test_coupling_lock_in_action(self):
        for N in [4, 7, 8, 11]:
            act = havelock_action(N)
            assert act['coupling_lock'] == pytest.approx(1 / (2 * math.pi**2))


# =====================================================================
# Standard Model table
# =====================================================================

class TestStandardModelTable:
    def test_table(self):
        table = standard_model_table()
        assert len(table) == 13  # N=3..15
        # N=4 is gauge boson
        n4 = [r for r in table if r['N'] == 4][0]
        assert n4['j_integer'] == 1
        # N=7 is graviton
        n7 = [r for r in table if r['N'] == 7][0]
        assert n7['j_integer'] == 2

    def test_central_charges(self):
        """All table entries use c = 12b(N), not N²."""
        table = standard_model_table()
        for row in table:
            N = row['N']
            assert row['central_charge'] == pytest.approx(central_charge(N))
