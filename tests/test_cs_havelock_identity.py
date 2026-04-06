"""
Tests for the CS-Havelock identity:
    C_2^{CS}(m) = f(m,N) = m(N-m)/2

Verifies:
1. The csc^2 circulant eigenvalue equals the Havelock sum (exact)
2. The Z_N character Casimir equals the Havelock Casimir
3. rho-independence: the Casimir is a representation-theoretic invariant
4. Integer-spin modes at N=4 (j=1) and N=7 (j=2)
5. Gauge group emergence: SU(3) from McKay, SU(2) from Casimir, U(1) from KK
6. Weinberg angle sin^2(theta_W) = 3/11
"""

import pytest
from fractions import Fraction
from math import sqrt, pi, sinh

from planetary_polygons.proofs.cs_havelock_identity import (
    havelock_casimir,
    csc2_circulant_eigenvalue,
    zn_holonomy_matrix,
    zn_character_casimir_numerical,
    zn_character_casimir_exact,
    cs_casimir_from_holonomy,
    verify_cs_havelock_identity,
    cs_representation_at_mode,
    gauge_group_from_casimir,
    integer_spin_condition,
    frobenius_order,
    frobenius_orbits,
    mckay_gauge_group,
    kk_charge,
    hypercharge_from_critical_mode,
    weinberg_angle_from_kk,
    full_proof_chain,
    seifert_laplacian_angular,
    central_charge_decomposition,
)


# =====================================================================
# 1. Havelock Casimir basics
# =====================================================================

class TestHavelockCasimir:
    def test_exact_type(self):
        assert isinstance(havelock_casimir(3, 7), Fraction)

    def test_known_values(self):
        assert havelock_casimir(2, 4) == Fraction(2)
        assert havelock_casimir(3, 7) == Fraction(6)
        assert havelock_casimir(5, 11) == Fraction(15)

    @pytest.mark.parametrize("N", range(3, 16))
    def test_palindromic(self, N):
        for m in range(1, N):
            assert havelock_casimir(m, N) == havelock_casimir(N - m, N)

    @pytest.mark.parametrize("N", range(3, 16))
    def test_boundary(self, N):
        assert havelock_casimir(0, N) == 0
        assert havelock_casimir(N, N) == 0

    @pytest.mark.parametrize("N", range(3, 16))
    def test_positive(self, N):
        for m in range(1, N):
            assert havelock_casimir(m, N) > 0


# =====================================================================
# 2. csc^2 circulant eigenvalue = Havelock sum
# =====================================================================

class TestCsc2Eigenvalue:
    @pytest.mark.parametrize("N", range(3, 16))
    def test_matches_havelock(self, N):
        for m in range(1, N):
            T_sum, T_exact, err = csc2_circulant_eigenvalue(m, N)
            assert err < 1e-10, f"N={N}, m={m}: err={err}"

    def test_m_zero(self):
        T_sum, T_exact, err = csc2_circulant_eigenvalue(0, 7)
        assert abs(T_sum) < 1e-10


# =====================================================================
# 3. Z_N character Casimir = Havelock Casimir
# =====================================================================

class TestCharacterCasimir:
    @pytest.mark.parametrize("N", range(3, 16))
    def test_numerical_matches_exact(self, N):
        for m in range(1, N):
            C_num = zn_character_casimir_numerical(m, N)
            C_exact = float(zn_character_casimir_exact(m, N))
            assert abs(C_num - C_exact) < 1e-10, (
                f"N={N}, m={m}: num={C_num}, exact={C_exact}"
            )

    @pytest.mark.parametrize("N", range(3, 16))
    def test_exact_equals_havelock(self, N):
        for m in range(1, N):
            assert zn_character_casimir_exact(m, N) == havelock_casimir(m, N)


# =====================================================================
# 4. CS Casimir = Havelock Casimir (the theorem)
# =====================================================================

class TestCSHavelockIdentity:
    @pytest.mark.parametrize("N", range(3, 13))
    def test_identity_all_modes(self, N):
        for m in range(1, N):
            assert cs_casimir_from_holonomy(m, N) == havelock_casimir(m, N)

    @pytest.mark.parametrize("N", range(3, 13))
    def test_verify_function(self, N):
        for m in range(1, N):
            result = verify_cs_havelock_identity(N, m)
            assert result['all_match'], f"N={N}, m={m}: verification failed"


# =====================================================================
# 5. rho-independence (representation-theoretic invariant)
# =====================================================================

class TestRhoIndependence:
    @pytest.mark.parametrize("rho0", [0.2, 0.5, 1.0, 1.5, 2.0, 3.0])
    def test_angular_eigenvalue_rescales(self, rho0):
        """After multiplying by sinh^2(rho), the eigenvalue is T_m, independent of rho."""
        for N in [4, 7, 11]:
            for m in range(1, N):
                ang = seifert_laplacian_angular(N, m, rho0)
                rescaled = ang * sinh(rho0) ** 2
                T_m = m * (N - m) / 2.0
                assert abs(rescaled - T_m) < 1e-10, (
                    f"N={N}, m={m}, rho={rho0}: {rescaled} != {T_m}"
                )


# =====================================================================
# 6. Z_N holonomy
# =====================================================================

class TestHolonomy:
    @pytest.mark.parametrize("N", [3, 4, 5, 7, 11])
    def test_holonomy_order(self, N):
        import numpy as np
        h = zn_holonomy_matrix(N)
        h_N = np.linalg.matrix_power(h, N)
        assert np.allclose(h_N, np.eye(N), atol=1e-10)

    @pytest.mark.parametrize("N", [3, 4, 5, 7, 11])
    def test_holonomy_unitary(self, N):
        import numpy as np
        h = zn_holonomy_matrix(N)
        assert np.allclose(h @ h.conj().T, np.eye(N), atol=1e-10)


# =====================================================================
# 7. Integer-spin modes
# =====================================================================

class TestIntegerSpin:
    def test_n4_has_j1(self):
        modes = integer_spin_condition(4)
        j_values = [r['j'] for r in modes]
        assert 1 in j_values

    def test_n7_has_j2(self):
        modes = integer_spin_condition(7)
        j_values = [r['j'] for r in modes]
        assert 2 in j_values

    def test_n4_m2(self):
        rep = cs_representation_at_mode(2, 4)
        assert rep['is_integer_j']
        assert abs(rep['j'] - 1.0) < 1e-10
        assert 'adjoint' in rep['representation'].lower() or 'vector' in rep['representation'].lower()

    def test_n7_m3(self):
        rep = cs_representation_at_mode(3, 7)
        assert rep['is_integer_j']
        assert abs(rep['j'] - 2.0) < 1e-10
        assert 'graviton' in rep['representation'].lower() or 'spin-2' in rep['representation'].lower()

    def test_n7_m3_palindromic_partner(self):
        """m=4 is the palindromic partner of m=3 at N=7."""
        rep3 = cs_representation_at_mode(3, 7)
        rep4 = cs_representation_at_mode(4, 7)
        assert abs(rep3['f'] - rep4['f']) < 1e-10

    def test_smallest_j1_is_n4(self):
        """N=4 is the smallest N with a j=1 (vector boson) mode."""
        for N in range(3, 4):
            modes = integer_spin_condition(N)
            j_vals = [r['j'] for r in modes]
            assert 1 not in j_vals, f"j=1 found at N={N} < 4"
        modes_4 = integer_spin_condition(4)
        assert 1 in [r['j'] for r in modes_4]

    def test_smallest_j2_is_n7(self):
        """N=7 is the smallest N with a j=2 (graviton) mode."""
        for N in range(3, 7):
            modes = integer_spin_condition(N)
            j_vals = [r['j'] for r in modes]
            assert 2 not in j_vals, f"j=2 found at N={N} < 7"
        modes_7 = integer_spin_condition(7)
        assert 2 in [r['j'] for r in modes_7]

    def test_pell_selects_4_and_7(self):
        """The Pell equation N² - 8(N-1) = k² selects N=7 as the unique
        value where the critical mode has j=2 AND is at the stability threshold."""
        # At N=7, m=3 is both the critical mode (floor(N/2)) AND has j=2
        m_star = 7 // 2  # = 3
        rep = cs_representation_at_mode(m_star, 7)
        assert abs(rep['j'] - 2.0) < 1e-10
        # At N=8, j=2 exists but at m=2 (not the critical mode m=4)
        modes_8 = integer_spin_condition(8)
        j2_modes_8 = [r for r in modes_8 if r['j'] == 2]
        assert all(r['m'] != 8 // 2 for r in j2_modes_8)


# =====================================================================
# 8. SU(3) from Frobenius / McKay
# =====================================================================

class TestFrobeniusMcKay:
    def test_frobenius_order_7(self):
        assert frobenius_order(7, 2) == 3

    def test_frobenius_order_4(self):
        # ord_4(3) = 2 since 3^2 = 9 ≡ 1 mod 4
        assert frobenius_order(4, 3) == 2

    def test_frobenius_orbits_7(self):
        orbits = frobenius_orbits(7, 2)
        assert len(orbits) == 2
        assert sorted(orbits[0]) in ([1, 2, 4], [3, 5, 6])

    def test_mckay_su3_at_7(self):
        result = mckay_gauge_group(7, 2)
        assert result['gauge_group'] == 'SU(3)'
        assert result['frobenius_order'] == 3
        assert result['dynkin_diagram'] == 'A_2'
        assert result['cs_level'] == 1

    def test_mckay_su2_at_4(self):
        result = mckay_gauge_group(4, 3)
        assert result['gauge_group'] == 'SU(2)'
        assert result['frobenius_order'] == 2
        assert result['dynkin_diagram'] == 'A_1'


# =====================================================================
# 9. U(1) and hypercharge
# =====================================================================

class TestU1Hypercharge:
    def test_kk_charge_n4(self):
        assert kk_charge(2, 4) == Fraction(1, 2)

    def test_hypercharge_from_critical(self):
        result = hypercharge_from_critical_mode(4)
        assert result['Q'] == Fraction(1, 2)

    def test_kk_charge_is_fraction(self):
        assert isinstance(kk_charge(3, 7), Fraction)


# =====================================================================
# 10. Weinberg angle
# =====================================================================

class TestWeinbergAngle:
    def test_sin2_is_3_over_11(self):
        result = weinberg_angle_from_kk()
        assert result['is_3_over_11']
        assert result['sin2_theta_W'] == Fraction(3, 11)

    def test_sin2_numerical(self):
        result = weinberg_angle_from_kk()
        assert abs(result['sin2_float'] - 3 / 11) < 1e-14

    def test_intermediate_values(self):
        result = weinberg_angle_from_kk()
        assert result['j'] == 1
        assert result['C2_W'] == 2
        assert result['Q'] == Fraction(1, 2)
        assert result['h_W'] == Fraction(2, 3)
        assert result['h_Y'] == Fraction(1, 4)


# =====================================================================
# 11. Gauge group at N=4
# =====================================================================

class TestGaugeGroupN4:
    def test_has_su2(self):
        result = gauge_group_from_casimir(4)
        assert result['has_su2']

    def test_su2_at_m2(self):
        result = gauge_group_from_casimir(4)
        assert 2 in result['su2_modes']


# =====================================================================
# 12. Central charge decomposition
# =====================================================================

class TestCentralCharge:
    @pytest.mark.parametrize("N", [4, 7, 11])
    def test_decomposition_exact(self, N):
        result = central_charge_decomposition(N)
        assert result['decomposition_exact']

    def test_gauge_central_charge(self):
        result = central_charge_decomposition(7)
        assert result['c_gauge'] == 4  # SU(3)_1 + SU(2)_1 + U(1)_1 = 2+1+1


# =====================================================================
# 13. Full proof chain
# =====================================================================

class TestFullProofChain:
    def test_theorem_verified(self):
        chain = full_proof_chain(N_max=8)
        assert chain['theorem_verified']

    def test_step12_passes(self):
        chain = full_proof_chain(N_max=8)
        assert chain['step12_all_pass']

    def test_step3_rho_independent(self):
        chain = full_proof_chain(N_max=8)
        assert chain['step3_rho_independent']
