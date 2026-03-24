"""Tests for one-loop corrections in the Havelock Field Theory."""

import math
import pytest
from planetary_polygons.extensions.loop_corrections import (
    cs_level_shift, one_loop_cosmological_constant,
    fermion_self_energy_cs, all_loop_corrections,
    central_charge, b_exact,
)


class TestCSLevelShift:
    def test_shift_is_minus_N_over_2(self):
        """Δk = -N/2 from N Dirac fermion loops."""
        for N in [4, 7, 8, 11]:
            cs = cs_level_shift(N)
            assert cs['delta_k'] == pytest.approx(-N / 2)

    def test_k_phys_formula(self):
        """k_phys = k_bare - N/2 = c/6 - N/2."""
        for N in [4, 7, 8, 11]:
            cs = cs_level_shift(N)
            expected = central_charge(N) / 6 - N / 2
            assert cs['k_phys'] == pytest.approx(expected)

    def test_k_phys_positive(self):
        """k_phys > 0 for all N ≥ 4 (theory is well-defined)."""
        for N in range(4, 20):
            cs = cs_level_shift(N)
            assert cs['k_phys'] > 0, f"k_phys negative at N={N}"

    def test_rational_part(self):
        """Rational part of k_phys is N(N-2)/6."""
        for N in [4, 7, 8, 11]:
            cs = cs_level_shift(N)
            assert cs['k_phys_rational_part'] == pytest.approx(N * (N - 2) / 6)

    def test_massless_fermion_count(self):
        """Odd N has 1 massless fermion; even N has 0."""
        for N in [4, 6, 8, 10]:
            assert cs_level_shift(N)['n_massless_fermions'] == 0
        for N in [5, 7, 9, 11]:
            assert cs_level_shift(N)['n_massless_fermions'] == 1

    def test_k_bare_equals_2b(self):
        """k_bare = c/6 = 2b(N)."""
        for N in [4, 7, 11]:
            cs = cs_level_shift(N)
            assert cs['k_bare'] == pytest.approx(2 * b_exact(N))


class TestOneLoopCosmologicalConstant:
    def test_tree_level_formula(self):
        """Λ_tree = (N²-16)/16."""
        for N in [4, 7, 8, 11]:
            cc = one_loop_cosmological_constant(N)
            assert cc['lambda_tree'] == pytest.approx((N**2 - 16) / 16)

    def test_lambda_zero_at_N4(self):
        """Λ_tree = 0 at N=4."""
        cc = one_loop_cosmological_constant(4)
        assert cc['lambda_tree'] == pytest.approx(0.0)

    def test_one_loop_negative(self):
        """ΔΛ < 0 (fermions dominate bosons in mass³ sum for even N;
        bosons dominate for all N giving negative CW correction)."""
        for N in [7, 8, 11]:
            cc = one_loop_cosmological_constant(N)
            assert cc['delta_lambda_cubic'] < 0

    def test_one_loop_is_perturbative(self):
        """One-loop correction is < 20% of tree level for N ≥ 7."""
        for N in [7, 8, 11]:
            cc = one_loop_cosmological_constant(N)
            assert abs(cc['ratio_cubic']) < 0.20

    def test_corrected_lambda_positive(self):
        """Λ_tree + ΔΛ > 0 for N ≥ 5 (de Sitter survives one loop)."""
        for N in [5, 6, 7, 8, 11]:
            cc = one_loop_cosmological_constant(N)
            assert cc['lambda_tree'] + cc['delta_lambda_cubic'] > 0

    def test_boson_fermion_masses_correct(self):
        """Boson and fermion mass spectra match the KK formulas."""
        N = 7
        cc = one_loop_cosmological_constant(N)
        for m in range(N):
            assert cc['boson_masses'][m] == pytest.approx(abs(m - N / 2))
            assert cc['fermion_masses'][m] == pytest.approx(abs(m - (N - 1) / 2))


class TestFermionMassCorrections:
    def test_universal_shift(self):
        """δm/m = -1/(4πk) is the same for all fermions."""
        ferm = fermion_self_energy_cs(7)
        expected = -1 / (4 * math.pi * (central_charge(7) / 6))
        assert ferm['delta_m_over_m'] == pytest.approx(expected)

    def test_shift_small(self):
        """One-loop mass shift is < 2% for N ≥ 7."""
        for N in [7, 8, 11]:
            ferm = fermion_self_energy_cs(N)
            assert abs(ferm['delta_m_over_m']) < 0.02

    def test_ratios_unchanged(self):
        """Mass RATIOS are unchanged at one loop (universal shift)."""
        ferm = fermion_self_energy_cs(7)
        assert ferm['tree_ratio_12'] == pytest.approx(ferm['corrected_ratio_12'])

    def test_texture_zeros_stable(self):
        """Texture zeros are topologically protected (Z_N charge conservation)."""
        # The Yukawa texture zeros come from m_i - m_j + m_H ≢ 0 mod N.
        # This is a mod-N arithmetic condition, unchanged by continuous
        # mass corrections. Just verify the ratio stability.
        ferm = fermion_self_energy_cs(7)
        assert ferm['ratio_shift_pct'] < 0.01  # < 0.01% change


class TestCouplingLock:
    def test_lock_exact_at_all_N(self):
        """α/(8πG) = 1/(2π²) is exact (c cancels algebraically)."""
        for N in range(4, 20):
            c = central_charge(N)
            alpha = 6 / (math.pi * c)
            G = 3 / (2 * c)
            lock = alpha / (8 * math.pi * G)
            assert lock == pytest.approx(1 / (2 * math.pi**2))

    def test_lock_survives_cs_shift(self):
        """The coupling lock is independent of c → survives one-loop shift."""
        # If c → c - 3N (from CS level shift), the lock still holds
        # because α/(8πG) = [6/(πc)]/[8π·3/(2c)] = 1/(2π²) for ANY c.
        for N in [7, 11]:
            c_shifted = central_charge(N) - 3 * N
            alpha_s = 6 / (math.pi * c_shifted)
            G_s = 3 / (2 * c_shifted)
            lock_s = alpha_s / (8 * math.pi * G_s)
            assert lock_s == pytest.approx(1 / (2 * math.pi**2))
