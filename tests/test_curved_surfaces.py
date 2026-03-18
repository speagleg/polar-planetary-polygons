"""tests/test_curved_surfaces.py"""
import numpy as np
from planetary_polygons.extensions.curved_surfaces import (
    sphere_constrained_eigenvalues,
    ncrit_sphere,
    hyperbolic_ncrit,
)


def test_sphere_eigenvalues_shape():
    evals = sphere_constrained_eigenvalues(N=6, colatitude_deg=14.0)
    assert len(evals) > 0


def test_ncrit_sphere_n6_stable_at_76N():
    """Saturn 76°N = colatitude 14°: N=6 should be stable."""
    n = ncrit_sphere(14.0)
    assert n >= 6, f"Expected N_crit >= 6 at colatitude 14°, got {n}"


def test_hyperbolic_ncrit_n12_stable():
    """N=12 should be stable at R/a=1 on hyperbolic plane."""
    eval12 = hyperbolic_ncrit(N=12, R_over_a=1.0)
    eval13 = hyperbolic_ncrit(N=13, R_over_a=1.0)
    assert eval12 >= -1e-4, f"N=12 should be stable, eigenvalue={eval12:.6f}"
    assert eval13 < 0.5, f"N=13 should be less stable than N=12"
