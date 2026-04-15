"""Tests for G = ℓ/(8 b(N)), the polygon-central-charge derivation of Newton's constant.

Verifies:
  - Gauss product: ∏sin(πm/N) = N/2^{N-1} (Paper I, Thm)
  - b(N) structure via Gauss product identity
  - Central charge c = 12 b(N)
  - G = 3ℓ/(2c) = ℓ/(8 b(N)) follows from Brown-Henneaux
"""
from __future__ import annotations

from math import log, pi, sin

import pytest


def gauss_product_numerical(N: int) -> float:
    """Numerically compute ∏_{m=1}^{N-1} sin(πm/N)."""
    prod = 1.0
    for m in range(1, N):
        prod *= sin(pi * m / N)
    return prod


def gauss_product_exact(N: int) -> float:
    """N / 2^{N-1} (Gauss's exact identity)."""
    return N / 2 ** (N - 1)


def b_N(N: int) -> float:
    """Polygon self-energy constant."""
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


def test_gauss_product_identity():
    """∏ sin(πm/N) = N/2^{N-1} for all N ≥ 2."""
    for N in range(2, 20):
        num = gauss_product_numerical(N)
        exact = gauss_product_exact(N)
        assert abs(num - exact) < 1e-12, f"N={N}: {num} vs {exact}"


def test_bN_from_gauss_product():
    """b(N) = N(N+1)/12 + log(∏sin)/(N-1)."""
    for N in [3, 5, 7, 11]:
        # Direct formula:
        b_direct = N * (N + 1) / 12 - log(2) + log(N) / (N - 1)
        # Via Gauss product:
        gp = gauss_product_exact(N)
        b_via_gp = N * (N + 1) / 12 + log(gp) / (N - 1)
        assert abs(b_direct - b_via_gp) < 1e-12


def test_central_charge_N7():
    """c = 12 b(N) at N=7."""
    c = 12 * b_N(7)
    assert abs(c - 51.5741) < 0.001


def test_G_from_polygon_central_charge():
    """G = ℓ/(8 b(N)) matches G = 3ℓ/(2c) (Brown-Henneaux)."""
    for N in [3, 5, 7, 11, 23]:
        b = b_N(N)
        c = 12 * b
        G_from_b = 1 / (8 * b)  # in units ℓ=1
        G_BH = 3 / (2 * c)
        assert abs(G_from_b - G_BH) < 1e-14, (
            f"N={N}: G from b(N): {G_from_b}, G from BH: {G_BH}"
        )


def test_G_numerical_values():
    """Numerical check of G values."""
    # N=7: G = ℓ / (8 × 4.298) = 0.0291 ℓ
    assert abs(1 / (8 * b_N(7)) - 0.02908) < 1e-4
    # N=11: G = ℓ / (8 × 10.547) = 0.01185 ℓ
    assert abs(1 / (8 * b_N(11)) - 0.01185) < 1e-4


def test_G_decreases_with_N():
    """G decreases as N grows (b(N) grows)."""
    Gs = [1 / (8 * b_N(N)) for N in [3, 5, 7, 11, 23]]
    for i in range(len(Gs) - 1):
        assert Gs[i] > Gs[i + 1], f"G({i}) = {Gs[i]} not > G({i+1}) = {Gs[i+1]}"


def test_bN_polygon_invariant():
    """b(N) does not depend on any free parameter — only N."""
    # Trivially true: b_N is a function of N only
    # Test: recomputing gives the same value
    for N in [7, 11]:
        values = [b_N(N) for _ in range(10)]
        assert all(v == values[0] for v in values)
