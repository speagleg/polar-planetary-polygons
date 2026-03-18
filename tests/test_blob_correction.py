# tests/test_blob_correction.py
import numpy as np
from fractions import Fraction
from planetary_polygons.extensions.blob_correction import (
    compute_Pm, blob_correction_table, stabilization_threshold
)

# Expected P_m values from paper §6.4
EXPECTED_PM = {3: -1/3, 4: 1/4, 5: 1.0, 6: 4.0, 7: 8.0, 8: 65/4}
EXPECTED_CM_SIGN = {3: -1, 4: -1, 5: -1, 6: 1, 7: 1, 8: 1}  # -1=negative, 1=positive


def test_Pm_table_values():
    """P_m values must match paper to within 5%."""
    for N, expected in EXPECTED_PM.items():
        pm = compute_Pm(N)
        rel_err = abs(pm - expected) / (abs(expected) + 1e-10)
        assert rel_err < 0.05, f"N={N}: P_m={pm:.4f}, expected={expected:.4f}, rel_err={rel_err:.3f}"


def test_cm_signs():
    """c_m < 0 for N<=5 (destabilizing), c_m > 0 for N>=6 (stabilizing)."""
    table = blob_correction_table()
    for N, expected_sign in EXPECTED_CM_SIGN.items():
        cm = table[N]['cm']
        if expected_sign == -1:
            assert cm < 0, f"N={N}: expected c_m < 0, got {cm:.4f}"
        else:
            assert cm > 0, f"N={N}: expected c_m > 0, got {cm:.4f}"


def test_stabilization_threshold_n6():
    eps = stabilization_threshold(6)
    assert 0 < eps < 1.0, f"N=6: expected 0 < eps < 1, got {eps:.4f}"


def test_stabilization_threshold_n3_infinite():
    eps = stabilization_threshold(3)
    assert eps == float('inf'), "N=3: c_m < 0, cannot be stabilized"


# ── Multipole far-field expansion tests ──────────────────────────────────────

from planetary_polygons.extensions.blob_correction import multipole_far_field_residual


def test_multipole_far_field_d_scaling():
    """Residual scales as d⁻² for fixed ε (doubling d reduces residual by ≈4)."""
    K, eps = 1.0, 0.1
    r1 = multipole_far_field_residual(K, eps, d=10.0)
    r2 = multipole_far_field_residual(K, eps, d=20.0)
    ratio = r1 / r2
    assert 3.5 < ratio < 4.5, (
        f"Expected d⁻² scaling (ratio≈4), got {ratio:.3f}. "
        f"residuals: d=10 → {r1:.6f}, d=20 → {r2:.6f}"
    )


def test_multipole_far_field_eps_scaling():
    """Residual scales as ε² for fixed d (doubling ε increases residual by ≈4)."""
    K, d = 1.0, 30.0
    r1 = multipole_far_field_residual(K, eps=0.1, d=d)
    r2 = multipole_far_field_residual(K, eps=0.2, d=d)
    ratio = r2 / r1
    assert 3.5 < ratio < 4.5, (
        f"Expected ε² scaling (ratio≈4), got {ratio:.3f}. "
        f"residuals: ε=0.1 → {r1:.6f}, ε=0.2 → {r2:.6f}"
    )


def test_multipole_residual_small_for_large_separation():
    """Residual is negligible compared to monopole when d >> ε."""
    K, eps, d = 1.0, 0.05, 50.0
    residual = multipole_far_field_residual(K, eps, d)
    monopole = K ** 2 * abs(np.log(d))
    assert abs(residual) / monopole < 1e-4, (
        f"Residual {residual:.2e} not small vs monopole {monopole:.2f}"
    )
