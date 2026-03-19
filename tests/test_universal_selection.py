"""tests/test_universal_selection.py — Universal framework tests."""
import math
from fractions import Fraction

from planetary_polygons.core.universal_selection import (
    havelock_eigenvalue,
    spectral_gap,
    spectral_gap_table,
    packing_bound,
    packing_bound_exact,
    kappa_crit,
    thomson_bound,
    universal_selection,
    saturn_selection,
    jupiter_north_selection,
    jupiter_south_selection,
    cross_planetary_table,
)


# ===================================================================
# Spectral gap (Havelock eigenvalues)
# ===================================================================

class TestHavelockEigenvalue:
    def test_known_values(self):
        """lambda_m = (N-1) - m(N-m)/2 for known cases."""
        # N=3, m=1: 2 - 1 = 1
        assert havelock_eigenvalue(3, 1) == Fraction(1)
        # N=6, m=1: 5 - 5/2 = 5/2
        assert havelock_eigenvalue(6, 1) == Fraction(5, 2)
        # N=6, m=3: 5 - 9/2 = 1/2
        assert havelock_eigenvalue(6, 3) == Fraction(1, 2)
        # N=7, m=3: 6 - 6 = 0
        assert havelock_eigenvalue(7, 3) == Fraction(0)
        # N=8, m=4: 7 - 8 = -1
        assert havelock_eigenvalue(8, 4) == Fraction(-1)

    def test_symmetry(self):
        """lambda_m = lambda_{N-m} (palindromic symmetry)."""
        for N in range(3, 12):
            for m in range(1, N):
                assert havelock_eigenvalue(N, m) == havelock_eigenvalue(N, N - m)


class TestSpectralGap:
    def test_stable_range(self):
        """N=3..6: spectral gap > 0 (stable)."""
        for N in range(3, 7):
            assert spectral_gap(N) > 0, f"N={N} should be stable"

    def test_marginal_N7(self):
        """N=7: spectral gap = 0 (marginal)."""
        assert spectral_gap(7) == 0

    def test_unstable_N8_plus(self):
        """N=8..12: spectral gap < 0 (unstable)."""
        for N in range(8, 13):
            assert spectral_gap(N) < 0, f"N={N} should be unstable"

    def test_exact_values(self):
        """Check specific exact spectral gap values."""
        assert spectral_gap(3) == Fraction(1)
        assert spectral_gap(4) == Fraction(1)
        # N=5: m=2, lambda = 4 - 2*3/2 = 1
        assert spectral_gap(5) == Fraction(1)
        assert spectral_gap(6) == Fraction(1, 2)
        assert spectral_gap(7) == Fraction(0)
        assert spectral_gap(8) == Fraction(-1)

    def test_table_length(self):
        """Table covers requested range."""
        t = spectral_gap_table(3, 12)
        assert len(t) == 10
        assert t[0]['N'] == 3
        assert t[-1]['N'] == 12


# ===================================================================
# Packing bound
# ===================================================================

class TestPackingBound:
    def test_basic_geometry(self):
        """sin(pi/N) >= r/R determines the packing limit."""
        # r/R = 0.5 => sin(pi/N) >= 0.5 => pi/N >= pi/6 => N <= 6
        assert packing_bound(1.0, 0.5) == 6

    def test_small_exclusion(self):
        """Very small r_excl allows large N."""
        assert packing_bound(1.0, 0.01) >= 50

    def test_large_exclusion(self):
        """r_excl close to R_ring gives N=3."""
        assert packing_bound(1.0, 0.85) == 3

    def test_impossible(self):
        """r_excl > R_ring returns None."""
        assert packing_bound(1.0, 1.5) is None

    def test_sin_pi_over_N_inequality(self):
        """Verify that the bound satisfies sin(pi/N) >= r/R for all returned N."""
        for R in [1.0, 5.0, 10.0]:
            for r in [0.1, 0.3, 0.5, 0.8]:
                N = packing_bound(R, r)
                if N is not None:
                    assert math.sin(math.pi / N) >= r / R - 1e-10
                    # And N+1 violates
                    if N + 1 >= 3:
                        assert math.sin(math.pi / (N + 1)) < r / R + 1e-10

    def test_exact_details(self):
        """packing_bound_exact returns margin information."""
        result = packing_bound_exact(1.0, 0.5)
        assert result['N_max'] == 6
        assert result['margin_at_N'] >= -1e-12  # floating-point tolerance
        assert result['deficit_at_N_plus_1'] < 1e-12


# ===================================================================
# Thomson bound
# ===================================================================

class TestThomsonBound:
    def test_no_central_vortex(self):
        """kappa_ratio=0 gives N_thomson=7."""
        assert thomson_bound(0) == 7

    def test_half(self):
        """kappa_ratio=0.5 gives N_thomson=8."""
        assert thomson_bound(0.5) == 8

    def test_one(self):
        """kappa_ratio=1.0 gives N_thomson=9."""
        assert thomson_bound(1.0) == 9

    def test_kappa_crit_known(self):
        """Known kappa_crit values."""
        for N in range(3, 8):
            assert kappa_crit(N) == 0
        assert kappa_crit(8) == Fraction(1, 2)
        assert kappa_crit(9) == Fraction(1)


# ===================================================================
# Universal selection
# ===================================================================

class TestUniversalSelection:
    def test_min_constraint(self):
        """Selection picks the minimum of all bounds."""
        result = universal_selection(8, 5, 6)
        assert result['N_selected'] == 5
        assert 'packing' in result['binding_constraint']

    def test_rossby_binding(self):
        """When Rossby is tightest."""
        result = universal_selection(7, None, 6)
        assert result['N_selected'] == 6
        assert 'rossby' in result['binding_constraint']

    def test_thomson_binding(self):
        """When Thomson is tightest."""
        result = universal_selection(8, 20, None)
        assert result['N_selected'] == 8
        assert 'thomson' in result['binding_constraint']


# ===================================================================
# KEY TESTS: Planet-specific selections
# ===================================================================

class TestSaturnSelection:
    def test_saturn_selects_6(self):
        """Saturn hexagon: N=6 via Rossby stationarity."""
        result = saturn_selection()
        assert result['N_selected'] == 6
        assert 'rossby' in result['binding_constraint']

    def test_saturn_rossby_near_6(self):
        """Continuous n* should be near 6 (within ~1)."""
        result = saturn_selection()
        assert 5.0 <= result['n_star_continuous'] <= 7.0


class TestJupiterNorthSelection:
    def test_jupiter_north_selects_8(self):
        """Jupiter north octagon: N=8 via Thomson bound."""
        result = jupiter_north_selection()
        assert result['N_selected'] == 8
        assert 'thomson' in result['binding_constraint']

    def test_packing_not_binding_north(self):
        """Packing allows many more than 8 at Jupiter north."""
        result = jupiter_north_selection()
        N_pack = result['constraints'].get('packing')
        assert N_pack is None or N_pack > 8


class TestJupiterSouthSelection:
    def test_jupiter_south_selects_5(self):
        """Jupiter south pentagon: N=5 via packing constraint."""
        result = jupiter_south_selection()
        assert result['N_selected'] == 5
        assert 'packing' in result['binding_constraint']

    def test_thomson_allows_more(self):
        """Thomson alone would allow N=8, but packing limits to 5."""
        result = jupiter_south_selection()
        assert result['constraints']['thomson'] == 8

    def test_exclusion_radius_physical(self):
        """r_excl should be about 1.3x cyclone radius."""
        result = jupiter_south_selection()
        assert abs(result['r_excl_over_r_cyclone'] - 1.3) < 0.1


# ===================================================================
# Cross-planetary table
# ===================================================================

class TestCrossPlanetaryTable:
    def test_all_match(self):
        """All three systems reproduce observed N."""
        table = cross_planetary_table()
        for row in table:
            assert row['match'], \
                f"{row['system']}: expected N={row['N_observed']}, got N={row['N_selected']}"

    def test_table_completeness(self):
        """Table has entries for all three systems."""
        table = cross_planetary_table()
        assert len(table) == 3
        systems = {row['system'] for row in table}
        assert any('Saturn' in s for s in systems)
        assert any('north' in s for s in systems)
        assert any('south' in s for s in systems)

    def test_different_binding_constraints(self):
        """Each system has a different binding constraint."""
        table = cross_planetary_table()
        bindings = [row['binding'] for row in table]
        # All three should be different
        assert len(set(bindings)) == 3, \
            f"Expected 3 different binding constraints, got {bindings}"
