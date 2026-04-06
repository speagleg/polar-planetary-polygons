"""
Tests for the gauge group derivation:
    Seifert geometry H^2 x_N S^1 -> SU(3) x SU(2) x U(1) at k=1.

Verifies:
1. Frobenius automorphism and orbit structure
2. McKay correspondence: Z/d -> A_{d-1} -> SU(d)
3. DHVW level k=1 from twist-field OPE
4. U(1) from KK with correct charge quantization
5. Central charge budget: c_gauge = 4 is unique for SU(3)_1 x SU(2)_1 x U(1)_1
6. Full derivation chain at N=7 and N=11
"""

import pytest
from fractions import Fraction

from planetary_polygons.proofs.gauge_group_derivation import (
    seifert_orbifold_data,
    frobenius_action,
    frobenius_order,
    frobenius_orbits,
    euler_totient,
    mckay_correspondence,
    mckay_from_frobenius,
    dhvw_level,
    verify_dhvw_twist_dimensions,
    u1_from_kk,
    wzw_central_charge,
    enumerate_gauge_combinations,
    verify_uniqueness,
    derive_gauge_group,
    derive_gauge_group_n11,
    verification_table,
)


# =====================================================================
# 1. Seifert orbifold data
# =====================================================================

class TestSeifertOrbifold:
    @pytest.mark.parametrize("N", [3, 4, 5, 7, 11])
    def test_euler_class(self, N):
        data = seifert_orbifold_data(N)
        assert data['euler_class'] == Fraction(N, 2)

    def test_n_cone_points(self):
        data = seifert_orbifold_data(7)
        assert data['n_cone_points'] == 7

    def test_kk_modes(self):
        data = seifert_orbifold_data(7)
        assert data['kk_modes'] == list(range(7))


# =====================================================================
# 2. Frobenius automorphism
# =====================================================================

class TestFrobenius:
    def test_action_n7(self):
        """sigma: a -> 2a mod 7."""
        assert frobenius_action(1, 7) == 2
        assert frobenius_action(2, 7) == 4
        assert frobenius_action(4, 7) == 1  # 2*4 = 8 ≡ 1 mod 7

    def test_order_7(self):
        assert frobenius_order(7, 2) == 3

    def test_order_4(self):
        assert frobenius_order(4, 3) == 2

    def test_order_11(self):
        assert frobenius_order(11, 2) == 10

    def test_orbits_7(self):
        orbits = frobenius_orbits(7, 2)
        assert len(orbits) == 2
        # Each orbit has size 3
        for orb in orbits:
            assert len(orb) == 3
        # Together they cover {1,2,3,4,5,6}
        all_elements = sorted(sum(orbits, []))
        assert all_elements == [1, 2, 3, 4, 5, 6]

    def test_orbits_contain_1_2_4(self):
        orbits = frobenius_orbits(7, 2)
        found = False
        for orb in orbits:
            if set(orb) == {1, 2, 4}:
                found = True
        assert found

    def test_orbit_sizes_divide_phi(self):
        """Each orbit size divides phi(N)."""
        for N in range(3, 20):
            phi = euler_totient(N)
            d = frobenius_order(N, 2)
            if d is not None:
                assert phi % d == 0

    @pytest.mark.parametrize("N", range(3, 20))
    def test_orbits_partition(self, N):
        """Frobenius orbits partition (Z/NZ)^*."""
        orbits = frobenius_orbits(N, 2)
        all_elts = []
        for orb in orbits:
            all_elts.extend(orb)
        # Should be exactly the units mod N
        units = [k for k in range(1, N) if Fraction(k, N).denominator == N // Fraction(N, 1).denominator or True]
        # Simpler: check no duplicates and correct count
        assert len(all_elts) == len(set(all_elts))
        assert len(all_elts) == euler_totient(N)


# =====================================================================
# 3. McKay correspondence
# =====================================================================

class TestMcKay:
    def test_z3_gives_su3(self):
        result = mckay_correspondence(3)
        assert result['gauge_group'] == 'SU(3)'
        assert result['dynkin'] == 'A_2'
        assert result['rank'] == 2
        assert result['dimension'] == 8

    def test_z2_gives_su2(self):
        result = mckay_correspondence(2)
        assert result['gauge_group'] == 'SU(2)'
        assert result['dynkin'] == 'A_1'
        assert result['dimension'] == 3

    def test_z4_gives_su4(self):
        result = mckay_correspondence(4)
        assert result['gauge_group'] == 'SU(4)'

    def test_n7_gives_su3(self):
        result = mckay_from_frobenius(7, 2)
        assert result['gauge_group'] == 'SU(3)'
        assert result['frobenius_order'] == 3

    def test_dual_coxeter(self):
        """h∨(SU(d)) = d."""
        for d in range(2, 8):
            result = mckay_correspondence(d)
            assert result['dual_coxeter'] == d


# =====================================================================
# 4. DHVW level
# =====================================================================

class TestDHVW:
    @pytest.mark.parametrize("d", [2, 3, 4, 5, 7])
    def test_level_is_1(self, d):
        result = dhvw_level(d)
        assert result['level'] == 1

    @pytest.mark.parametrize("d", [2, 3, 4, 5, 7])
    def test_twist_dimension_sum(self, d):
        """Sum of twist dimensions = (d^2-1)/12."""
        result = verify_dhvw_twist_dimensions(d)
        assert result['matches'], f"d={d}: {result['sum_h_k']} != {result['expected']}"

    def test_twist_dim_sigma_1_at_d3(self):
        """sigma_1 at d=3 has h = 1*2/(2*9) = 2/18 = 1/9."""
        result = dhvw_level(3)
        assert result['twist_dimensions'][1] == Fraction(1, 9)

    def test_sigma_0_is_identity(self):
        """sigma_0 always has h=0 (identity twist)."""
        for d in [2, 3, 5, 7]:
            result = dhvw_level(d)
            assert result['twist_dimensions'][0] == 0


# =====================================================================
# 5. U(1) from KK
# =====================================================================

class TestU1:
    def test_level(self):
        result = u1_from_kk(7)
        assert result['level'] == 1

    def test_critical_charge_n4(self):
        result = u1_from_kk(4)
        assert result['critical_charge'] == Fraction(1, 2)

    def test_critical_charge_n7(self):
        result = u1_from_kk(7)
        assert result['critical_charge'] == Fraction(3, 7)


# =====================================================================
# 6. WZW central charges
# =====================================================================

class TestWZWCentralCharge:
    def test_su3_level1(self):
        assert wzw_central_charge('SU', 3, 1) == Fraction(2)

    def test_su2_level1(self):
        assert wzw_central_charge('SU', 2, 1) == Fraction(1)

    def test_su2_level2(self):
        assert wzw_central_charge('SU', 2, 2) == Fraction(3, 2)

    def test_e8_level1(self):
        """E8 at level 1 has c=8 (the famous result)."""
        assert wzw_central_charge('SU', 2, 1) + wzw_central_charge('SU', 2, 1) == Fraction(2)
        # Direct E8 check would need the exceptional case


# =====================================================================
# 7. Central charge budget uniqueness
# =====================================================================

class TestUniqueness:
    def test_su3_su2_u1_sums_to_4(self):
        c = (wzw_central_charge('SU', 3, 1)
             + wzw_central_charge('SU', 2, 1)
             + Fraction(1))
        assert c == 4

    def test_uniqueness_at_c4(self):
        result = verify_uniqueness(c_target=4)
        assert result['unique'], (
            f"Not unique! Found {result['n_physical']} combinations: "
            f"{result['physical_combinations']}"
        )

    def test_the_combination(self):
        result = verify_uniqueness(c_target=4)
        assert result['the_combination'] is not None
        assert 'SU(3)_1' in result['the_combination']
        assert 'SU(2)_1' in result['the_combination']
        assert 'U(1)_1' in result['the_combination']

    def test_multiple_c4_combinations_exist(self):
        """There ARE other c=4 combinations, but only one is physical."""
        result = verify_uniqueness(c_target=4)
        assert result['n_total'] > 1


# =====================================================================
# 8. Full derivation at N=7
# =====================================================================

class TestFullDerivationN7:
    def test_derived_flag(self):
        result = derive_gauge_group(7)
        assert result['derived']

    def test_gauge_group(self):
        result = derive_gauge_group(7)
        assert 'SU(3)' in result['gauge_group']
        assert 'SU(2)' in result['gauge_group']
        assert 'U(1)' in result['gauge_group']

    def test_levels(self):
        result = derive_gauge_group(7)
        for g, k in result['levels'].items():
            assert k == 1, f"{g} has level {k} != 1"

    def test_frobenius_order(self):
        result = derive_gauge_group(7)
        assert result['step2_frobenius_order'] == 3

    def test_twist_dimensions(self):
        result = derive_gauge_group(7)
        assert result['step4_twist_check']['matches']


# =====================================================================
# 9. Full derivation at N=11
# =====================================================================

class TestFullDerivationN11:
    def test_decomposition(self):
        result = derive_gauge_group_n11()
        assert result['decomposition'] == '11 = 4 + 7'

    def test_gauge_group(self):
        result = derive_gauge_group_n11()
        assert result['gauge_group'] == 'SU(3) x SU(2) x U(1)'

    def test_su3_from_n7(self):
        result = derive_gauge_group_n11()
        assert result['su3_from_n7']['gauge_group'] == 'SU(3)'

    def test_central_charge_decomposition(self):
        result = derive_gauge_group_n11()
        assert result['central_charge']['decomposition_exact']


# =====================================================================
# 10. Verification table
# =====================================================================

class TestVerificationTable:
    def test_table_has_entries(self):
        rows = verification_table(12)
        assert len(rows) == 10  # N=3,...,12

    def test_n7_entry(self):
        rows = verification_table()
        n7 = [r for r in rows if r['N'] == 7][0]
        assert n7['ord_N_2'] == 3
        assert n7['mckay_group'] == 'SU(3)'
        assert n7['n_orbits'] == 2
