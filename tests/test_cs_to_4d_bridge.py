"""Tests for the CS₃ → 4D gauge theory bridge."""
import pytest
from math import pi
from planetary_polygons.proofs.cs_to_4d_bridge import (
    cs_ym_coupling, effective_coupling, conformal_weight,
    verify_matching, verify_dhvw_kk_commute,
)


def test_su2_coupling():
    """SU(2)_1: g² = 2π/3."""
    g2 = cs_ym_coupling(k=1, h_dual=2)
    assert abs(g2 - 2 * pi / 3) < 1e-12


def test_u1_coupling():
    """U(1)_1: g² = 2π."""
    g2 = cs_ym_coupling(k=1, h_dual=0)
    assert abs(g2 - 2 * pi) < 1e-12


def test_effective_equals_2pi_h():
    """α_eff(R) = 2π h_R for both SU(2) and U(1)."""
    # SU(2)
    g2_W = cs_ym_coupling(1, 2)
    alpha_W = effective_coupling(g2_W, 2.0)
    h_W = conformal_weight(2.0, 1, 2)
    assert abs(alpha_W - 2 * pi * h_W) < 1e-12

    # U(1)
    g2_Y = cs_ym_coupling(1, 0)
    alpha_Y = effective_coupling(g2_Y, 0.25)
    h_Y = conformal_weight(0.25, 1, 0)
    assert abs(alpha_Y - 2 * pi * h_Y) < 1e-12


def test_2pi_cancels_in_ratio():
    """The 2π factor cancels: sin²θ from couplings = sin²θ from weights."""
    r = verify_matching()
    assert r['match']
    assert abs(r['sin2_gauge'] - r['sin2_weight']) < 1e-12


def test_weinberg_angle_3_over_11():
    """sin²θ_W = 3/11 from both gauge couplings and conformal weights."""
    r = verify_matching()
    assert abs(r['value'] - 3 / 11) < 1e-12


def test_dhvw_kk_commute():
    """The Frobenius Z/3Z and KK reduction commute."""
    assert verify_dhvw_kk_commute()


def test_fiber_radius_independence():
    """The mixing angle is independent of the fiber radius R."""
    for R in [0.5, 1.0, 2.0, 5.0]:
        r = verify_matching(R=R)
        assert abs(r['value'] - 3 / 11) < 1e-12


def test_coupling_ratio_not_3_over_4():
    """The BARE coupling ratio g'²/(g²+g'²) = 3/4, NOT 3/11.
    The EFFECTIVE ratio α_Y/(α_Y+α_W) = 3/11.
    The difference: effective couplings include C₂(R)."""
    g2_W = cs_ym_coupling(1, 2)
    g2_Y = cs_ym_coupling(1, 0)
    bare_ratio = g2_Y / (g2_Y + g2_W)
    assert abs(bare_ratio - 3 / 4) < 1e-12  # bare: 3/4 (wrong)

    r = verify_matching()
    assert abs(r['value'] - 3 / 11) < 1e-12  # effective: 3/11 (correct)
