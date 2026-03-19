"""tests/test_first_principles.py — First-principles prediction tests.

Tests the first_principles module that predicts polygon wavenumber N
from atmospheric parameters (Coriolis, deformation radius, constraints).
No scipy dependency.
"""
import math

from planetary_polygons.core.first_principles import (
    coriolis_params,
    deformation_radius,
    predict_jupiter_north,
    predict_jupiter_south,
    predict_saturn,
    first_principles_table,
)


# ===================================================================
# Coriolis parameters
# ===================================================================

class TestCoriolisParams:
    def test_jupiter_f(self):
        """f at Jupiter 83 deg latitude should be ~3.49e-4 rad/s (within 1%)."""
        # Jupiter: Omega = 1.7585e-4 rad/s, R_polar = 6.6854e7 m
        result = coriolis_params(
            Omega=1.7585e-4, R_polar=6.6854e7, lat_deg=83.0
        )
        f = result['f']
        expected = 3.49e-4
        assert abs(f - expected) / expected < 0.01, (
            f"f = {f:.4e}, expected ~{expected:.4e} (within 1%)"
        )

    def test_jupiter_beta(self):
        """beta at Jupiter 83 deg should be ~6.0e-13 m^-1 s^-1 (within 10%)."""
        result = coriolis_params(
            Omega=1.7585e-4, R_polar=6.6854e7, lat_deg=83.0
        )
        beta = result['beta']
        expected = 6.0e-13
        assert abs(beta - expected) / expected < 0.10, (
            f"beta = {beta:.4e}, expected ~{expected:.4e} (within 10%)"
        )

    def test_saturn_beta(self):
        """beta at Saturn 76 deg should be ~1.46e-12 m^-1 s^-1 (within 5%)."""
        # Saturn: Omega = 1.638e-4 rad/s, R_polar = 5.4364e7 m
        result = coriolis_params(
            Omega=1.638e-4, R_polar=5.4364e7, lat_deg=76.0
        )
        beta = result['beta']
        expected = 1.46e-12
        assert abs(beta - expected) / expected < 0.05, (
            f"beta = {beta:.4e}, expected ~{expected:.4e} (within 5%)"
        )


# ===================================================================
# Deformation radius
# ===================================================================

class TestDeformationRadius:
    def test_basic(self):
        """R_d = sqrt(g'*H)/f, check with simple values.

        g'=1, H=1e5, f=1e-4 -> R_d = sqrt(1e5)/1e-4 = 3.16e6 m.
        """
        R_d = deformation_radius(g_prime=1.0, H_eff=1e5, f=1e-4)
        expected = math.sqrt(1e5) / 1e-4  # ~3.162e6
        assert abs(R_d - expected) / expected < 1e-10, (
            f"R_d = {R_d:.4e}, expected {expected:.4e}"
        )

    def test_jupiter_north_scale(self):
        """With H=3000 km, g'=0.3, f~3.49e-4, R_d should be ~2500-3000 km."""
        f_jupiter = 3.49e-4  # rad/s at 83 deg
        R_d = deformation_radius(g_prime=0.3, H_eff=3000e3, f=f_jupiter)
        R_d_km = R_d / 1e3
        assert 2500 <= R_d_km <= 3000, (
            f"R_d = {R_d_km:.0f} km, expected 2500-3000 km"
        )


# ===================================================================
# Predictions
# ===================================================================

class TestPredictions:
    def test_saturn_selects_6(self):
        """Saturn Rossby prediction gives N=6."""
        result = predict_saturn(120.0)
        assert result['N_rossby'] == 6, (
            f"Expected N_rossby=6, got {result['N_rossby']}"
        )

    def test_jupiter_north_selects_8(self):
        """Jupiter north prediction gives N=8."""
        result = predict_jupiter_north(3000e3, 0.3)
        assert result['N_selected'] == 8, (
            f"Expected N_selected=8, got {result['N_selected']}"
        )

    def test_jupiter_south_selects_5(self):
        """Jupiter south with chi=1.34 asymmetry gives N=5."""
        result = predict_jupiter_south(3000e3, 0.3, chi=1.34)
        assert result['N_selected'] == 5, (
            f"Expected N_selected=5, got {result['N_selected']}"
        )

    def test_jupiter_north_thomson_binds(self):
        """At Jupiter north, Thomson bound should be tighter than packing.

        N_pack > N_thomson because cyclones fit easily on the ring.
        """
        result = predict_jupiter_north(3000e3, 0.3)
        N_pack = result.get('N_pack')
        N_thomson = result.get('N_thomson')
        assert N_pack is not None and N_thomson is not None
        assert N_pack > N_thomson, (
            f"Expected N_pack ({N_pack}) > N_thomson ({N_thomson}) at north"
        )

    def test_jupiter_south_packing_binds(self):
        """At Jupiter south, packing bound should be tighter than Thomson.

        N_pack < N_thomson because large cyclones + beta-drift crowd the ring.
        """
        result = predict_jupiter_south(3000e3, 0.3, chi=1.34)
        N_pack = result.get('N_pack')
        N_thomson = result.get('N_thomson')
        assert N_pack is not None and N_thomson is not None
        assert N_pack < N_thomson, (
            f"Expected N_pack ({N_pack}) < N_thomson ({N_thomson}) at south"
        )


# ===================================================================
# First-principles table
# ===================================================================

class TestFirstPrinciplesTable:
    def test_all_match(self):
        """All entries in the table should have match==True."""
        table = first_principles_table()
        # Table may be dict (keyed by system) or list of dicts
        entries = table.values() if isinstance(table, dict) else table
        for entry in entries:
            assert entry['match'], (
                f"predicted N={entry.get('N_selected', entry.get('N_rossby'))} "
                f"!= observed N={entry.get('N_observed')}"
            )

    def test_three_systems(self):
        """Table should have 3 entries covering Saturn, Jupiter N, Jupiter S."""
        table = first_principles_table()
        if isinstance(table, dict):
            assert len(table) == 3, f"Expected 3 entries, got {len(table)}"
            assert 'saturn' in table
            assert 'jupiter_north' in table
            assert 'jupiter_south' in table
        else:
            assert len(table) == 3


# ===================================================================
# Sensitivity / robustness
# ===================================================================

class TestSensitivity:
    def test_north_robust(self):
        """N=8 should hold for H_eff in [1000 km, 3500 km] at g'=0.3.

        Above ~3500 km, R_d exceeds 3100 km and packing limits to N=7.
        """
        for H_eff in [1000e3, 2000e3, 3000e3, 3500e3]:
            result = predict_jupiter_north(H_eff, 0.3)
            assert result['N_selected'] == 8, (
                f"N_selected={result['N_selected']} at H_eff={H_eff/1e3:.0f} km, "
                f"expected 8"
            )

    def test_south_sensitive_to_chi(self):
        """N=5 at chi=1.34 but N>5 at chi=1.0 (relaxed packing).

        Without south-pole size asymmetry (chi=1.0), the packing
        constraint relaxes and allows more vortices.
        """
        result_asym = predict_jupiter_south(3000e3, 0.3, chi=1.34)
        assert result_asym['N_selected'] == 5, (
            f"Expected N=5 at chi=1.34, got {result_asym['N_selected']}"
        )

        result_sym = predict_jupiter_south(3000e3, 0.3, chi=1.0)
        assert result_sym['N_selected'] > 5, (
            f"Expected N>5 at chi=1.0 (no asymmetry), got {result_sym['N_selected']}"
        )
