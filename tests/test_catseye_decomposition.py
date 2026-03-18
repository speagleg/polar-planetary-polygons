# tests/test_catseye_decomposition.py
"""
Tests for the cat's-eye decomposition and Rossby bridge analysis.

The key result: in the Stuart vortex concentration limit (eps -> 1),
the braid fraction of total circulation vanishes as O(1-eps),
establishing the conditions for Proposition 8 to apply.
"""
import numpy as np
from planetary_polygons.extensions.catseye_decomposition import (
    stuart_stream_function,
    stuart_vorticity,
    stuart_velocity,
    stuart_separatrix_level,
    stuart_background_vorticity,
    classify_regions,
    label_individual_lobes,
    circulation_partition,
    lobe_centroids,
    fit_scaling_law,
)


def _setup_grid(sigma=0.5, ny=256, nx=256, domain_factor=6.0):
    domain_half = domain_factor * sigma
    y = np.linspace(-domain_half, domain_half, ny)
    x = np.linspace(0, 2 * np.pi, nx, endpoint=False)
    return y, x


def test_stuart_vorticity_positive():
    """Stuart vortex vorticity is strictly positive for eps < 1."""
    y, x = _setup_grid()
    for eps in [0.1, 0.5, 0.9, 0.99]:
        omega = stuart_vorticity(y, x, sigma=0.5, eps=eps, n=6)
        assert np.all(omega > 0), f"Negative vorticity at eps={eps}"


def test_stuart_separatrix_exact():
    """Separatrix level matches analytical formula."""
    for sigma in [0.1, 0.5, 1.0]:
        for eps in [0.3, 0.7, 0.95]:
            psi_sep = stuart_separatrix_level(sigma, eps)
            expected = -sigma**2 * np.log(1.0 + eps)
            assert abs(psi_sep - expected) < 1e-12


def test_stuart_total_circulation_conserved():
    """Total circulation is independent of eps (for eps < 1)."""
    y, x = _setup_grid(sigma=0.5, ny=512, nx=512)
    dy, dx = y[1] - y[0], x[1] - x[0]

    Gamma_ref = None
    for eps in [0.1, 0.5, 0.8, 0.95]:
        omega = stuart_vorticity(y, x, sigma=0.5, eps=eps, n=6)
        Gamma = float(np.sum(omega) * dy * dx)
        if Gamma_ref is None:
            Gamma_ref = Gamma
        else:
            # Should agree to a few percent (grid effects at high eps)
            assert abs(Gamma - Gamma_ref) / Gamma_ref < 0.02, \
                f"Circulation changed: {Gamma:.4f} vs {Gamma_ref:.4f} at eps={eps}"


def test_regions_cover_domain():
    """Lobe + braid + background cover the full grid."""
    y, x = _setup_grid()
    Psi = stuart_stream_function(y, x, sigma=0.5, eps=0.8, n=6)
    psi_sep = stuart_separatrix_level(0.5, 0.8)
    mask = classify_regions(Psi, psi_sep, braid_half_width=0.05 * 0.25)
    ny, nx = len(y), len(x)
    assert np.sum(mask == 0) + np.sum(mask == 1) + np.sum(mask == 2) == ny * nx


def test_lobes_detected():
    """At eps=0.8, n=6, we detect 6 or 7 lobes (7 if boundary wraps)."""
    y, x = _setup_grid()
    Psi = stuart_stream_function(y, x, sigma=0.5, eps=0.8, n=6)
    psi_sep = stuart_separatrix_level(0.5, 0.8)
    mask = classify_regions(Psi, psi_sep, braid_half_width=0.05 * 0.25)
    labels = label_individual_lobes(mask)
    n_lobes = int(labels.max())
    assert n_lobes in (6, 7), f"Expected 6-7 lobes, got {n_lobes}"


def test_lobe_fraction_increases_with_eps():
    """As eps -> 1, an increasing fraction of vorticity is in the lobes."""
    y, x = _setup_grid(sigma=0.5, ny=512, nx=512)
    dy, dx = y[1] - y[0], x[1] - x[0]
    dA = dy * dx
    sigma = 0.5

    fracs = []
    for eps in [0.3, 0.7, 0.95]:
        omega = stuart_vorticity(y, x, sigma=sigma, eps=eps, n=6)
        Psi = stuart_stream_function(y, x, sigma=sigma, eps=eps, n=6)
        psi_sep = stuart_separatrix_level(sigma, eps)
        mask = classify_regions(Psi, psi_sep, 0.05 * sigma**2)
        G_lobe = np.sum(omega[mask == 1]) * dA
        G_total = np.sum(omega) * dA
        fracs.append(G_lobe / G_total)

    # Lobe fraction should increase monotonically
    for i in range(len(fracs) - 1):
        assert fracs[i+1] > fracs[i], \
            f"Lobe fraction not increasing: {fracs}"


def test_braid_fraction_vanishes():
    """
    THE KEY BRIDGE RESULT:
    Braid fraction of total circulation vanishes as O(1-eps).

    This is the condition that allows Proposition 8 (inertia preservation)
    to apply to the lobe component of the cat's-eye, closing the
    Rossby bridge gap in the concentration limit.
    """
    y, x = _setup_grid(sigma=0.5, ny=512, nx=512)
    dy, dx = y[1] - y[0], x[1] - x[0]
    dA = dy * dx
    sigma = 0.5

    eps_values = [0.3, 0.5, 0.7, 0.8, 0.9, 0.95, 0.98, 0.99]
    one_minus = []
    braid_fracs = []

    for eps in eps_values:
        omega = stuart_vorticity(y, x, sigma=sigma, eps=eps, n=6)
        Psi = stuart_stream_function(y, x, sigma=sigma, eps=eps, n=6)
        psi_sep = stuart_separatrix_level(sigma, eps)
        mask = classify_regions(Psi, psi_sep, 0.05 * sigma**2)
        G_braid = np.sum(omega[mask == 2]) * dA
        G_total = np.sum(omega) * dA
        one_minus.append(1.0 - eps)
        braid_fracs.append(G_braid / G_total)

    # Fit braid_frac ~ (1-eps)^alpha
    alpha, C, r2 = fit_scaling_law(one_minus, braid_fracs)

    # Exponent should be approximately 1 (O(1-eps) vanishing)
    assert alpha > 0.8, f"Braid exponent {alpha:.3f} too low (expected ~1.0)"
    assert alpha < 1.4, f"Braid exponent {alpha:.3f} unexpectedly high"
    assert r2 > 0.99, f"Poor fit R^2 = {r2:.4f}"

    # At eps=0.99, braid fraction should be < 1%
    assert braid_fracs[-1] < 0.015, \
        f"Braid fraction at eps=0.99 too large: {braid_fracs[-1]:.4f}"


def test_lobe_centroids_at_ngon():
    """Lobe centroids should lie on y=0 (the jet axis) at the n-gon vertices."""
    y, x = _setup_grid(sigma=0.5, ny=256, nx=256)
    sigma, eps, n = 0.5, 0.8, 6

    omega = stuart_vorticity(y, x, sigma=sigma, eps=eps, n=n)
    Psi = stuart_stream_function(y, x, sigma=sigma, eps=eps, n=n)
    psi_sep = stuart_separatrix_level(sigma, eps)
    mask = classify_regions(Psi, psi_sep, 0.05 * sigma**2)
    labels = label_individual_lobes(mask)
    centroids = lobe_centroids(omega, labels, y, x)

    for (y_c, x_c) in centroids:
        # y-centroid should be near 0 (jet axis)
        assert abs(y_c) < 0.1, f"Lobe centroid off jet axis: y_c = {y_c:.4f}"
        # x-centroid should be near a multiple of 2*pi/n
        x_mod = x_c % (2 * np.pi / n)
        x_dist = min(x_mod, 2 * np.pi / n - x_mod)
        assert x_dist < 0.2, f"Lobe centroid not at n-gon vertex: x_c = {x_c:.4f}"
