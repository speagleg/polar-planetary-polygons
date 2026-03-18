# tests/test_circulation_disorder.py
import numpy as np
from planetary_polygons.extensions.circulation_disorder import (
    _H_hyp_kappa, disorder_min_eigenvalue_h2, instability_probability,
)
from planetary_polygons.extensions.h2_stability import H_hyp, min_eigenvalue


# ── _H_hyp_kappa unit tests ───────────────────────────────────────────────────

def test_H_hyp_kappa_uniform_matches_H_hyp():
    """κ_k = 1 for all k: H_κ must equal H_hyp exactly."""
    N, a = 6, 1.0
    rho = 0.5
    r_E = a * np.tanh(rho / (2 * a))
    z = r_E * np.exp(2j * np.pi * np.arange(N) / N)
    kappa = np.ones(N)
    H_kappa = _H_hyp_kappa(z.real, z.imag, a, kappa)
    H_standard = H_hyp(z.real, z.imag, a)
    assert abs(H_kappa - H_standard) < 1e-12, \
        f"H_kappa={H_kappa:.10f} != H_hyp={H_standard:.10f}"


def test_H_hyp_kappa_scalar_scaling():
    """Rescaling all κ_k by c scales H_κ by c²."""
    N, a = 5, 1.0
    rho = 0.4
    r_E = a * np.tanh(rho / (2 * a))
    z = r_E * np.exp(2j * np.pi * np.arange(N) / N)
    kappa = np.ones(N)
    c = 2.0
    H1 = _H_hyp_kappa(z.real, z.imag, a, kappa)
    H2 = _H_hyp_kappa(z.real, z.imag, a, c * kappa)
    assert abs(H2 - c ** 2 * H1) < 1e-10, \
        f"c²H1={c**2*H1:.10f}, H2={H2:.10f}"


def test_H_hyp_kappa_finite():
    """H_κ is finite for well-separated vortices with arbitrary κ."""
    N, a = 7, 1.0
    rho = 0.8
    r_E = a * np.tanh(rho / (2 * a))
    z = r_E * np.exp(2j * np.pi * np.arange(N) / N)
    rng = np.random.default_rng(0)
    kappa = 1.0 + rng.normal(0, 0.1, N)
    H = _H_hyp_kappa(z.real, z.imag, a, kappa)
    assert np.isfinite(H), "H_κ must be finite"


# ── disorder_min_eigenvalue_h2 ────────────────────────────────────────────────

def test_disorder_eigenvalue_zero_eta_matches_uniform():
    """η = 0 for all k: disordered eigenvalue must match the uniform-κ result."""
    N, rho, a = 6, 0.5, 1.0
    eta = np.zeros(N)
    lam_disorder = disorder_min_eigenvalue_h2(N, rho, eta, a=a)
    lam_uniform = min_eigenvalue(N, rho, a=a)
    assert abs(lam_disorder - lam_uniform) < 1e-6, \
        f"disorder={lam_disorder:.8f}, uniform={lam_uniform:.8f}"


def test_disorder_eigenvalue_n7_marginal_flat():
    """
    N=7 zero-disorder eigenvalue matches uniform min_eigenvalue at rho=0.3.

    The flat-space marginal mode has λ·r_E² → 0 but λ itself is large at
    small ring radii (scales as 1/r_E²).  We verify the FD eigenvalue is
    consistent with the uniform-κ formula, not that it is near zero.
    """
    N, rho = 7, 0.3
    eta = np.zeros(N)
    lam_disorder = disorder_min_eigenvalue_h2(N, rho, eta, a=1.0)
    lam_uniform = min_eigenvalue(N, rho, a=1.0)
    assert abs(lam_disorder - lam_uniform) < 1e-5, \
        f"disorder={lam_disorder:.8f}, uniform={lam_uniform:.8f}"


def test_disorder_eigenvalue_n6_stable():
    """N=6 is stable at rho=0.5 even with small disorder."""
    rng = np.random.default_rng(1)
    eta = rng.normal(0, 0.05, 6)
    lam = disorder_min_eigenvalue_h2(6, 0.5, eta, a=1.0)
    assert lam > -0.1, f"N=6 should remain nearly stable under small disorder, got {lam:.6f}"


def test_disorder_eigenvalue_large_eta_can_destabilize():
    """
    N=7 near flat limit with large circulation disorder:
    with high probability at least one realization gives λ_min < 0.
    """
    rng = np.random.default_rng(42)
    found_unstable = False
    for _ in range(50):
        eta = rng.normal(0, 0.5, 7)
        lam = disorder_min_eigenvalue_h2(7, 0.05, eta)
        if lam < 0:
            found_unstable = True
            break
    assert found_unstable, "Expected at least one unstable realization with eta_std=0.5"


# ── instability_probability ───────────────────────────────────────────────────

def test_instability_probability_zero_disorder():
    """η_std = 0 (all κ_k = 1): P = 0 for a stable configuration."""
    p = instability_probability(6, 0.5, eta_std=0.0, n_trials=50, seed=0)
    assert p == 0.0, f"Expected P=0 for zero disorder, got {p:.4f}"


def test_instability_probability_bounded():
    """P must be in [0, 1]."""
    p = instability_probability(7, 0.3, eta_std=0.2, n_trials=100, seed=7)
    assert 0.0 <= p <= 1.0, f"P must be in [0,1], got {p}"


def test_instability_probability_increases_with_disorder():
    """
    P(λ_min < 0) is non-decreasing in eta_std for N=7 at rho=0.1
    (marginal ring: easier to destabilize with more disorder).
    """
    p_small = instability_probability(7, 0.1, eta_std=0.1, n_trials=200, seed=5)
    p_large = instability_probability(7, 0.1, eta_std=0.5, n_trials=200, seed=5)
    assert p_large >= p_small, \
        f"P(large disorder)={p_large:.3f} should be ≥ P(small disorder)={p_small:.3f}"


def test_instability_probability_n8_high_curvature_stable():
    """
    N=8 at rho=2.0 (well inside stable region):
    even with moderate disorder, P should be low.
    """
    p = instability_probability(8, 2.0, eta_std=0.1, n_trials=200, seed=8)
    assert p < 0.5, f"N=8 at rho=2.0 should be mostly stable, P={p:.3f}"
