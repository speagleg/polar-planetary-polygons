"""Tests for Weyl anomaly Δ-independence on the torus."""

import math
import pytest
import sys
sys.path.insert(0, 'src')

from planetary_polygons.extensions.weyl_anomaly_delta import (
    torus_interaction, torus_angular_eigenvalue, flat_casimir,
    extract_weyl_anomaly, check_delta_independence,
)


class TestTorusInteraction:
    """Test the torus lattice interaction."""

    def test_power_law_positive(self):
        """Power-law interaction is positive for Δ > 0."""
        z1 = complex(0.1, 0.2)
        z2 = complex(0.4, 0.3)
        for Delta in [0.5, 1.0, 2.0]:
            V = torus_interaction(z1, z2, Delta, L=1.0, n_images=3)
            assert V > 0, f"V should be positive for Δ={Delta}"

    def test_log_diverges_at_coincidence(self):
        """Log interaction diverges when z1 = z2."""
        z1 = complex(0.1, 0.2)
        V = torus_interaction(z1, z1, 0, L=1.0, n_images=3)
        assert V == float('inf'), "Should diverge at coincidence"


class TestFlatCasimir:
    """Test the flat-plane generalized Casimir."""

    def test_delta_zero(self):
        """At Δ=0, flat Casimir = 2m(N-m)."""
        for N in [5, 6, 7]:
            for m in range(1, N):
                h = flat_casimir(m, N, 0)
                expected = 2 * m * (N - m)
                assert abs(h - expected) < 1e-8

    def test_palindromic(self):
        """h(m) = h(N-m) for all Δ."""
        for Delta in [0, 0.5, 1.0]:
            for N in [5, 6]:
                for m in range(1, N):
                    h_m = flat_casimir(m, N, Delta)
                    h_Nm = flat_casimir(N - m, N, Delta)
                    assert abs(h_m - h_Nm) < 1e-8


class TestWeylAnomaly:
    """Test the Weyl anomaly extraction and Δ-independence."""

    @pytest.fixture
    def anomaly_n5(self):
        """Extract anomalies for N=5 at several Δ."""
        return check_delta_independence(
            5, R=0.15, L=1.0, n_images=3,
            Delta_values=[0.0, 0.5, 1.0]
        )

    @pytest.fixture
    def anomaly_n6(self):
        """Extract anomalies for N=6 at several Δ."""
        return check_delta_independence(
            6, R=0.15, L=1.0, n_images=3,
            Delta_values=[0.0, 0.5, 1.0]
        )

    def test_anomaly_extracted(self, anomaly_n5):
        """Anomaly extraction succeeds for all Δ."""
        for a in anomaly_n5['anomalies']:
            assert a is not None

    def test_anomaly_palindromic(self, anomaly_n5):
        """Anomaly respects palindromic symmetry: δ_m = δ_{N-m}."""
        N = 5
        for a in anomaly_n5['anomalies']:
            if a is None:
                continue
            na = a['normalized_anomaly']
            for m in range(1, N):
                assert abs(na[m] - na[N - m]) < 0.05, \
                    f"Δ={a['Delta']}: δ_{m} ≠ δ_{N-m}"

    def test_inner_product_high_n5(self, anomaly_n5):
        """N=5 anomaly shape is ~98% Δ-independent."""
        ip = anomaly_n5['inner_products']
        # Compare Δ=0.5 vs Δ=1.0 (both power-law)
        assert abs(ip[1, 2]) > 0.99, \
            f"N=5 inner product Δ=0.5 vs Δ=1.0 = {ip[1,2]:.4f}, expected >0.99"

    def test_inner_product_high_n6(self, anomaly_n6):
        """N=6 anomaly shape is ~98% Δ-independent."""
        ip = anomaly_n6['inner_products']
        assert abs(ip[1, 2]) > 0.99, \
            f"N=6 inner product Δ=0.5 vs Δ=1.0 = {ip[1,2]:.4f}, expected >0.99"

    def test_anomaly_norm_positive(self, anomaly_n5):
        """Anomaly norm is positive (torus corrections exist)."""
        for a in anomaly_n5['anomalies']:
            if a is None:
                continue
            assert a['anomaly_norm'] > 1e-10, \
                f"Δ={a['Delta']}: anomaly norm = {a['anomaly_norm']}"

    def test_n7_shape_change(self):
        """N=7 anomaly shape changes qualitatively at Δ=0→Δ>0."""
        result = check_delta_independence(
            7, R=0.15, L=1.0, n_images=3,
            Delta_values=[0.0, 0.5]
        )
        ip = result['inner_products']
        # The Δ=0 and Δ=0.5 anomalies should be very different for N=7
        assert abs(ip[0, 1]) < 0.5, \
            f"N=7 Δ=0 vs Δ=0.5 inner product = {ip[0,1]:.4f}, expected < 0.5"
