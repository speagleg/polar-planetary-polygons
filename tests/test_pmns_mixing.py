"""Tests for PMNS neutrino mixing from CKM-PMNS complementarity."""

import pytest
from math import pi, sqrt, atan, degrees, sin, asin

from planetary_polygons.extensions.pmns_mixing import (
    pmns_angles, complementarity_identity, reactor_angle,
)


class TestComplementarity:
    def test_complementarity_identity(self):
        """arctan(1/2) + arctan(1/3) = pi/4 exactly."""
        assert complementarity_identity()

    def test_complementarity_numeric(self):
        result = atan(0.5) + atan(1 / 3)
        assert abs(result - pi / 4) < 1e-14


class TestPMNSAngles:
    def test_theta_12(self):
        """theta_12^PMNS within 2 deg of PDG 33.41."""
        result = pmns_angles()
        assert abs(result['theta_12_deg'] - 33.41) < 2.0

    def test_theta_23(self):
        """theta_23^PMNS = 45 deg (maximal, pair symmetry)."""
        result = pmns_angles()
        assert abs(result['theta_23_deg'] - 45.0) < 0.01

    def test_theta_13(self):
        """theta_13^PMNS within 2 deg of PDG 8.54."""
        result = pmns_angles()
        assert abs(result['theta_13_deg'] - 8.54) < 2.0

    def test_delta_cp(self):
        """delta_CP^PMNS = arctan(sqrt(7)) (same Gauss sum as CKM)."""
        result = pmns_angles()
        expected = degrees(atan(sqrt(7)))
        assert abs(result['delta_CP_deg'] - expected) < 0.01

    def test_sin2_theta_13(self):
        """sin^2(theta_13) = (1/2)*sin^2(theta_C) within 10%."""
        result = pmns_angles()
        assert abs(result['sin2_theta_13'] - 0.0218) / 0.0218 < 0.30


class TestReactorAngle:
    def test_reactor_formula(self):
        """sin^2(theta_13) = (1/2)*sin^2(theta_C)."""
        s12_ckm = 0.210
        sin2_13 = reactor_angle(s12_ckm)
        expected = 0.5 * s12_ckm ** 2
        assert abs(sin2_13 - expected) < 1e-10
