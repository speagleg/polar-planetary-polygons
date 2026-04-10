"""Tests for PMNS neutrino mixing from Z_7 pair structure."""

import pytest
from math import pi, sqrt, atan, degrees, sin, cos, asin

from planetary_polygons.extensions.pmns_mixing import (
    pmns_angles, pmns_z7_fractions, maximal_atmospheric_mixing,
    complementarity_identity, reactor_angle,
)


N = 7


class TestComplementarity:
    def test_complementarity_identity(self):
        """arctan(1/2) + arctan(1/3) = pi/4 exactly."""
        assert complementarity_identity()


class TestMaximalAtmospheric:
    """Theorem: pair cosine DFT gives theta_23 = pi/4."""

    def test_character_orthogonality(self):
        """Sum_k cos^2(2pi k m/N) = (N-2)/4 for all m != 0."""
        result = maximal_atmospheric_mixing()
        assert result['proved']

    def test_column_norms_equal(self):
        """Pair modes m=2 and m=3 have identical column norms."""
        result = maximal_atmospheric_mixing()
        assert abs(result['sum_cos2_m2'] - result['sum_cos2_m3']) < 1e-12

    def test_expected_value(self):
        """Both sums equal (N-2)/4 = 5/4."""
        result = maximal_atmospheric_mixing()
        assert abs(result['sum_cos2_m2'] - result['expected']) < 1e-12

    def test_theta_23_maximal(self):
        """Leading-order prediction: theta_23 = 45 deg."""
        result = maximal_atmospheric_mixing()
        assert result['theta_23_deg'] == 45.0


class TestZ7Fractions:
    """Conjecture: PMNS angles from N=7 fractions."""

    def test_sin2_2theta12(self):
        """sin^2(2 theta_12) = (N-1)/N = 6/7."""
        result = pmns_z7_fractions()
        assert abs(result['sin2_2theta12'] - 6 / 7) < 1e-14

    def test_sin2_theta23(self):
        """sin^2(theta_23) = (N+1)/(2N) = 4/7."""
        result = pmns_z7_fractions()
        assert abs(result['sin2_theta23'] - 4 / 7) < 1e-14

    def test_sin2_theta13(self):
        """sin^2(theta_13) = 1/(N^2-1) = 1/48."""
        result = pmns_z7_fractions()
        assert abs(result['sin2_theta13'] - 1 / 48) < 1e-14

    def test_cos_2theta23(self):
        """cos(2 theta_23) = -1/N."""
        result = pmns_z7_fractions()
        assert abs(result['cos_2theta23'] - (-1 / N)) < 1e-14

    def test_theta_12_near_pdg(self):
        """theta_12 = 33.9 deg (PDG: 33.41 +/- 0.79, 0.6 sigma)."""
        result = pmns_z7_fractions()
        assert abs(result['theta_12_deg'] - 33.41) < 1.5

    def test_theta_23_near_pdg(self):
        """theta_23 = 49.1 deg (PDG: 49.0 +/- 1.3, 0.1 sigma)."""
        result = pmns_z7_fractions()
        assert abs(result['theta_23_deg'] - 49.0) < 1.5

    def test_theta_13_near_pdg(self):
        """theta_13 = 8.3 deg (PDG: 8.54 +/- 0.15, 1.6 sigma)."""
        result = pmns_z7_fractions()
        assert abs(result['theta_13_deg'] - 8.54) < 1.0

    def test_delta_cp(self):
        """delta_CP = arctan(sqrt(7)) (same Gauss sum as CKM)."""
        result = pmns_z7_fractions()
        expected = degrees(atan(sqrt(N)))
        assert abs(result['delta_CP_deg'] - expected) < 0.01


class TestReactorAngle:
    def test_reactor_formula(self):
        """sin^2(theta_13) = 1/(N^2-1) = 1/48."""
        sin2_13 = reactor_angle(0.210)  # s12_ckm ignored
        assert abs(sin2_13 - 1 / 48) < 1e-14


class TestBackwardCompatibility:
    def test_pmns_angles_returns_dict(self):
        """pmns_angles() still returns a dict with expected keys."""
        result = pmns_angles()
        assert 'theta_12_deg' in result
        assert 'theta_23_deg' in result
        assert 'theta_13_deg' in result
        assert 'delta_CP_deg' in result
