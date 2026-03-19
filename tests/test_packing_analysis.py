"""tests/test_packing_analysis.py — Packing constraint tests."""
import math

from planetary_polygons.extensions.packing_analysis import (
    exclusion_radius_sensitivity,
    beta_drift_exclusion,
    jupiter_south_packing_analysis,
    jupiter_north_packing_analysis,
)


class TestExclusionRadiusSensitivity:
    def test_inversion_consistency(self):
        """Inverted r_excl range brackets the observation."""
        result = exclusion_radius_sensitivity(R_ring=8.0e6, N_obs=5)
        # sin(pi/5) ~ 0.588, sin(pi/6) = 0.5
        assert result['r_excl_max'] > result['r_excl_min']
        # The max should give N=5, the min should give N=6
        from planetary_polygons.core.universal_selection import packing_bound
        assert packing_bound(8.0e6, result['r_excl_max']) == 5
        # Just below the min should give N >= 6
        assert packing_bound(8.0e6, result['r_excl_min'] * 0.99) >= 6

    def test_range_covers_physical_value(self):
        """The beta-drift r_excl falls within the inverted range."""
        result = exclusion_radius_sensitivity(R_ring=8.0e6, N_obs=5)
        # r_excl from beta-drift: ~4.55e6 m
        r_excl_drift = 3.5e6 * 1.3
        assert result['r_excl_min'] <= r_excl_drift <= result['r_excl_max']


class TestBetaDriftExclusion:
    def test_positive_drift(self):
        """Beta-drift always adds a positive exclusion zone."""
        result = beta_drift_exclusion(r_core=3.5e6, drift_factor=1.3)
        assert result['r_drift'] > 0
        assert result['r_excl'] > result['r_core']
        assert result['ratio'] > 1.0

    def test_ratio_matches_factor(self):
        """r_excl/r_core should match the drift_factor."""
        result = beta_drift_exclusion(r_core=3.5e6, drift_factor=1.3)
        assert abs(result['ratio'] - 1.3) < 1e-10

    def test_no_drift(self):
        """drift_factor=1.0 gives r_excl = r_core."""
        result = beta_drift_exclusion(r_core=2.5e6, drift_factor=1.0)
        assert result['r_drift'] == 0.0
        assert result['r_excl'] == result['r_core']


class TestJupiterSouthPacking:
    def test_N5_selected(self):
        """Jupiter south packing gives N=5."""
        result = jupiter_south_packing_analysis()
        assert result['N_observed'] == 5
        assert result['N_pack_with_drift'] == 5

    def test_r_excl_consistent_with_cyclone_radius(self):
        """Implied r_excl ~ 1.1-1.5 times cyclone radius (beta-drift adds ~25%)."""
        result = jupiter_south_packing_analysis()
        assert 1.0 < result['ratio_implied'] < 2.0

    def test_bare_allows_more(self):
        """Without beta-drift, bare cyclone radius allows more than 5."""
        result = jupiter_south_packing_analysis()
        assert result['N_pack_bare'] > 5

    def test_excess_is_beta_drift(self):
        """The ~25% excess over bare radius is the beta-drift zone."""
        result = jupiter_south_packing_analysis()
        assert 10 < result['excess_pct'] < 60


class TestJupiterNorthPacking:
    def test_packing_not_binding(self):
        """At Jupiter north, packing is NOT the binding constraint."""
        result = jupiter_north_packing_analysis()
        assert not result['packing_is_binding']

    def test_N_pack_exceeds_8(self):
        """Packing allows more than 8 at north pole (bare radius)."""
        result = jupiter_north_packing_analysis()
        assert result['N_pack_bare'] > 8
