"""Tests for the 4D graviton from KK decomposition."""

import pytest
from planetary_polygons.extensions.graviton_4d import (
    dof_counting, kk_decomposition, graviton_mass_spectrum,
    graviton_propagator_structure, spin2_dof_check, graviton_theorem,
)


class TestDOFCounting:
    def test_4d_graviton_has_2_dof(self):
        """The 4D graviton has exactly 2 physical DOF."""
        assert dof_counting(4)['physical_dof'] == 2

    def test_3d_gravity_topological(self):
        """3D gravity has 0 physical DOF (topological)."""
        assert dof_counting(3)['physical_dof'] == 0

    def test_general_formula(self):
        """d(d-3)/2 formula for graviton DOF."""
        for d in [3, 4, 5, 6, 10, 11]:
            expected = d * (d - 3) // 2
            assert dof_counting(d)['physical_dof'] == expected


class TestKKDecomposition:
    def test_total_is_2(self):
        """KK decomposition gives 2 total DOF."""
        kk = kk_decomposition()
        assert kk['total_dof'] == 2

    def test_matches_4d(self):
        """KK DOF matches 4D graviton DOF."""
        assert kk_decomposition()['matches_4d_graviton'] is True

    def test_3d_metric_topological(self):
        """3D metric sector has 0 DOF."""
        kk = kk_decomposition()
        metric = [s for s in kk['sectors'] if '3D metric' in s['field']][0]
        assert metric['dof'] == 0

    def test_graviphoton_propagates(self):
        """Graviphoton has 1 propagating DOF."""
        kk = kk_decomposition()
        gp = [s for s in kk['sectors'] if 'graviphoton' in s['field']][0]
        assert gp['dof'] == 1
        assert gp['nature'] == 'propagating'

    def test_radion_propagates(self):
        """Radion has 1 propagating DOF."""
        kk = kk_decomposition()
        rad = [s for s in kk['sectors'] if 'radion' in s['field']][0]
        assert rad['dof'] == 1
        assert rad['nature'] == 'propagating'


class TestGravitonMassSpectrum:
    def test_even_N_has_massless(self):
        """Even N has a massless graviton zero mode."""
        for N in [4, 6, 8, 10, 12]:
            spec = graviton_mass_spectrum(N)
            assert spec['has_massless_graviton'] is True

    def test_odd_N_no_massless(self):
        """Odd N has no massless graviton (lightest mass = 1/2)."""
        for N in [5, 7, 9, 11]:
            spec = graviton_mass_spectrum(N)
            assert spec['has_massless_graviton'] is False
            assert spec['lightest_massive'] == pytest.approx(0.5)

    def test_n_modes(self):
        """N KK modes at polygon number N."""
        for N in [4, 7, 11]:
            assert graviton_mass_spectrum(N)['n_modes'] == N

    def test_mass_formula(self):
        """μ_m = |m - N/2| for each mode."""
        for N in [7, 8]:
            spec = graviton_mass_spectrum(N)
            for s in spec['spectrum']:
                expected = abs(s['m'] - N / 2.0)
                assert s['mass'] == pytest.approx(expected)

    def test_n7_critical_mode(self):
        """At N=7, critical modes m=3,4 have mass 1/2 and Casimir 6."""
        spec = graviton_mass_spectrum(7)
        for s in spec['spectrum']:
            if s['m'] in [3, 4]:
                assert s['mass'] == pytest.approx(0.5)
                assert s['casimir'] == pytest.approx(6.0)
                assert s['is_critical'] is True


class TestSpin2Check:
    def test_graviton_is_j2(self):
        """Spin-2 gives 2 physical DOF."""
        check = spin2_dof_check(2)
        assert check['physical_dof'] == 2
        assert check['is_graviton'] is True

    def test_gauge_boson_is_j1(self):
        """Spin-1 gives 1 physical DOF (after transversality)."""
        check = spin2_dof_check(1)
        assert check['physical_dof'] == 1


class TestGravitonTheorem:
    def test_theorem_consistent(self):
        """The full graviton theorem is internally consistent."""
        thm = graviton_theorem()
        assert thm['4D_dof']['physical_dof'] == 2
        assert thm['3D_dof']['physical_dof'] == 0
        assert thm['kk_decomposition']['matches_4d_graviton'] is True
        assert thm['spin2_check']['is_graviton'] is True
