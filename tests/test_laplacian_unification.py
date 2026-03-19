"""tests/test_laplacian_unification.py — Laplacian unification tests."""
import math
from planetary_polygons.core.laplacian_unification import (
    domain_admissible,
    max_admissible_N,
    blob_constrained_eigenvalue,
    blob_stable_window,
    beta_effective_epsilon,
    unified_N_crit,
    laplacian_selection,
    laplacian_unification_table,
)


class TestDomainAdmissibility:
    def test_point_vortex_always_admissible(self):
        """eps=0: domain is always admissible."""
        for N in range(3, 20):
            assert domain_admissible(N, 0.0)

    def test_packing_equivalence(self):
        """Domain admissibility reproduces the packing bound."""
        assert domain_admissible(6, 0.49)
        assert not domain_admissible(7, 0.45)  # sin(pi/7) = 0.434 < 0.45

    def test_max_admissible(self):
        """max_admissible_N matches packing_bound from universal_selection."""
        from planetary_polygons.core.universal_selection import packing_bound
        for eps_R in [0.1, 0.3, 0.5, 0.7]:
            N_adm = max_admissible_N(eps_R)
            N_pack = packing_bound(1.0, eps_R)
            assert N_adm == N_pack, f"eps/R={eps_R}: admissible={N_adm}, packing={N_pack}"


class TestBlobEigenvalue:
    def test_point_vortex_limit(self):
        """At eps~0, blob eigenvalue matches Havelock spectral gap sign."""
        for N in range(3, 8):
            lam = blob_constrained_eigenvalue(N, 0.001)
            assert lam >= -0.01, f"N={N} should be stable at eps~0"
        lam8 = blob_constrained_eigenvalue(8, 0.001)
        assert lam8 < 0, "N=8 should be unstable at eps~0"

    def test_N8_remains_unstable_at_finite_eps(self):
        """N=8 remains unstable throughout the admissible domain (no blob window)."""
        # With the corrected Hessian, N=8 never becomes blob-stable
        lam = blob_constrained_eigenvalue(8, 0.35)
        assert lam < 0, f"N=8 at eps/R=0.35 should remain unstable, got {lam}"


class TestBlobStableWindow:
    def test_N7_stable_from_zero(self):
        """N=7 is stable starting from eps=0."""
        window = blob_stable_window(7)
        assert window is not None
        assert window[0] == 0.0

    def test_N8_no_window(self):
        """N=8 has NO blob-stable window (corrected Hessian)."""
        window = blob_stable_window(8)
        assert window is None, \
            f"N=8 should have no blob-stable window, got {window}"

    def test_N9_no_window(self):
        """N=9 has no blob-stable window."""
        window = blob_stable_window(9)
        assert window is None


class TestUnifiedSelection:
    def test_point_vortex_thomson(self):
        """At eps=0, unified bound = Thomson bound."""
        assert unified_N_crit(0.0, kappa_ratio=0) == 7
        assert unified_N_crit(0.0, kappa_ratio=0.5) == 8

    def test_admissibility_binds(self):
        """At large eps, admissibility binds over Thomson."""
        assert unified_N_crit(0.569, kappa_ratio=0.7) == 5


class TestLaplacianSelection:
    def test_saturn(self):
        """Saturn: Rossby stationarity from modified Laplacian."""
        r = laplacian_selection('saturn')
        assert r['N_selected'] == 6
        assert r['binding'] == 'rossby'

    def test_jupiter_north(self):
        """Jupiter north: spectral (Thomson + central vortex)."""
        r = laplacian_selection('jupiter_north')
        assert r['N_selected'] == 8
        assert r['binding'] == 'spectral'

    def test_jupiter_south(self):
        """Jupiter south: domain admissibility from Laplacian BVP."""
        r = laplacian_selection('jupiter_south')
        assert r['N_selected'] == 5
        assert r['binding'] == 'admissibility'

    def test_all_match(self):
        """All three systems match observations."""
        for row in laplacian_unification_table():
            assert row['match'], \
                f"{row['system']}: expected {row['N_observed']}, got {row['N_selected']}"

    def test_three_different_facets(self):
        """Each system is governed by a different Laplacian facet."""
        table = laplacian_unification_table()
        facets = {row['laplacian_facet'] for row in table}
        assert len(facets) == 3
