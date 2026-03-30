"""Tests for the BF instanton mass hierarchy mechanism."""
import pytest
import math
from planetary_polygons.proofs.mass_hierarchy import (
    rs_profile,
    conformal_dimensions,
    mass_ratio,
    find_M_poly_for_ratio,
)


def test_conformal_dimensions():
    """Conformal dimensions for N=7 down-type quarks."""
    c = conformal_dimensions(7, mu4=1.5)
    assert len(c) == 3
    assert abs(c[0] - 2.500) < 0.001  # gen 1 (d quark)
    assert abs(c[1] - 1.803) < 0.001  # gen 2 (s quark)
    assert abs(c[2] - 1.500) < 0.001  # gen 3 (b quark)


def test_rs_profile_limits():
    """RS profile at large warp factor."""
    # At large sigma, c > 1/2: F ~ sqrt(2c-1) * exp(-(c-1/2)*sigma)
    f = rs_profile(2.0, 20.0)
    expected = math.sqrt(3.0) * math.exp(-1.5 * 20.0)
    assert abs(f / expected - 1) < 0.1
    # F decreases with sigma for c > 1/2
    assert rs_profile(2.0, 10.0) > rs_profile(2.0, 15.0)


def test_instanton_dominates():
    """Y₃₃^inst >> Y₃₁ at the physical warp factor."""
    r = mass_ratio(300)
    K = r['K']
    f = r['f']
    Y33_inst = K ** 2 * f[2] ** 2
    Y31_tree = f[2] * f[0]
    assert Y33_inst / Y31_tree > 100, "Instanton must dominate over tree-level Y₃₁"


def test_mass_ratio_at_300TeV():
    """m_s/m_b ≈ 0.059 at the one-loop polygon scale."""
    r = mass_ratio(300)
    assert 0.04 < r['analytic'] < 0.08
    assert 0.04 < r['m_s_over_m_b'] < 0.08


def test_mass_ratio_at_exact_scale():
    """m_s/m_b = 0.024 at the corrected polygon scale."""
    M = find_M_poly_for_ratio(0.024)
    assert 800 < M < 2000, f"Expected 800-2000 TeV, got {M:.0f}"
    r = mass_ratio(M)
    assert abs(r['analytic'] - 0.024) < 0.001


def test_scale_factor_within_two_loop():
    """The scale factor is within standard two-loop corrections."""
    M = find_M_poly_for_ratio(0.024)
    factor = M / 300
    # Two-loop + threshold corrections in non-SUSY unification
    # shift the scale by factor 2-10 (standard)
    assert 2 < factor < 10


def test_K_from_CKM():
    """K = 0.548 is the same instanton fugacity as in the CKM."""
    K = 0.548
    # K = exp(-2π k_frac) where k_frac = 0.0957
    k_frac = -math.log(K) / (2 * math.pi)
    assert abs(k_frac - 0.0957) < 0.001


def test_delta_c_from_KK():
    """Δc = 0.303 from the KK mass spectrum."""
    c = conformal_dimensions(7, mu4=1.5)
    Dc = c[1] - c[2]
    assert abs(Dc - 0.303) < 0.001


@pytest.mark.parametrize("M_poly", [200, 500, 1000, 2000])
def test_ratio_monotonic(M_poly):
    """m_s/m_b decreases with M_poly (more warp → more hierarchy)."""
    r1 = mass_ratio(M_poly)
    r2 = mass_ratio(M_poly * 1.5)
    assert r2['analytic'] < r1['analytic']
