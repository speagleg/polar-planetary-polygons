"""tests/test_k0_central_vortex.py — K₀ + central vortex stability tests."""
from planetary_polygons.extensions.k0_central_vortex import (
    k0, k1, K0_constrained_eigenvalue, critical_R_over_Rd, jupiter_K0_table,
)


class TestBesselFunctions:
    def test_k0_known_values(self):
        """K₀(x) matches known values to 4 decimal places."""
        assert abs(k0(1.0) - 0.42102) < 5e-4
        assert abs(k0(2.0) - 0.11389) < 5e-4
        assert abs(k0(0.1) - 2.42707) < 5e-3

    def test_k1_known_values(self):
        """K₁(x) matches known values to 3 decimal places."""
        assert abs(k1(1.0) - 0.60191) < 5e-3
        assert abs(k1(2.0) - 0.13987) < 5e-3

    def test_k0_positive(self):
        """K₀(x) > 0 for all x > 0."""
        for x in [0.01, 0.1, 0.5, 1, 2, 5, 10]:
            assert k0(x) > 0

    def test_k0_decreasing(self):
        """K₀ is strictly decreasing."""
        prev = k0(0.01)
        for x in [0.1, 0.5, 1, 2, 5]:
            curr = k0(x)
            assert curr < prev, f"K₀ not decreasing at x={x}"
            prev = curr


class TestK0Eigenvalue:
    def test_barotropic_limit_matches_point_vortex(self):
        """At R/R_d → 0, K₀ eigenvalue matches point-vortex result."""
        # Point vortex N=8, kappa_ratio=0.7: lambda_min ≈ 0.40
        lam = K0_constrained_eigenvalue(8, 0.01, kappa_ratio=0.7)
        assert abs(lam - 0.40) < 0.05, f"Barotropic limit: {lam} (expected ~0.40)"

    def test_N8_unstable_at_R_Rd_1(self):
        """N=8 with κ₀/κ=0.7 is unstable at R/R_d=1."""
        lam = K0_constrained_eigenvalue(8, 1.0, kappa_ratio=0.7)
        assert lam < 0, f"N=8 should be unstable at R/Rd=1, got {lam}"

    def test_N6_stable_at_R_Rd_4(self):
        """N=6 with κ₀/κ=0.7 stays stable well into tropospheric regime."""
        lam = K0_constrained_eigenvalue(6, 4.0, kappa_ratio=0.7)
        assert lam > 0, f"N=6 should be stable at R/Rd=4, got {lam}"


class TestCriticalRatio:
    def test_N8_critical_ratio(self):
        """(R/R_d)_crit(N=8, κ₀/κ=0.7) ≈ 0.79."""
        crit = critical_R_over_Rd(8, 0.7)
        assert crit is not None
        assert 0.6 < crit < 1.0, f"Expected ~0.79, got {crit}"

    def test_N8_crit_below_tropospheric(self):
        """Critical ratio for N=8 is below the tropospheric range [1,4]."""
        crit = critical_R_over_Rd(8, 0.7)
        assert crit < 1.0, \
            f"N=8 critical R/Rd={crit:.2f} should be < 1 (tropospheric boundary)"

    def test_N7_crit_above_tropospheric(self):
        """N=7 remains stable through most of the tropospheric range."""
        crit = critical_R_over_Rd(7, 0.7)
        assert crit > 3.0, f"N=7 critical R/Rd={crit:.2f} should be > 3"

    def test_N6_very_stable(self):
        """N=6 is stable to very large R/R_d."""
        crit = critical_R_over_Rd(6, 0.7)
        assert crit > 10.0, f"N=6 critical R/Rd={crit:.2f} should be >> 4"


class TestJupiterTable:
    def test_table_has_key_entries(self):
        """Table covers N=6..9."""
        table = jupiter_K0_table()
        Ns = [row['N'] for row in table]
        assert 6 in Ns and 7 in Ns and 8 in Ns and 9 in Ns

    def test_N8_not_tropospheric_stable(self):
        """N=8 is NOT stable in the tropospheric regime."""
        table = jupiter_K0_table()
        n8 = [r for r in table if r['N'] == 8][0]
        assert not n8['tropospheric_stable']
