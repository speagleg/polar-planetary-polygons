# tests/test_riemannian_havelock.py
import numpy as np
from fractions import Fraction
from planetary_polygons.extensions.riemannian_havelock import (
    havelock_sum, havelock_exact, trace_formula_delta
)


def test_havelock_sum_exact():
    for N in range(3, 8):
        for m in range(1, N):
            num = havelock_sum(N, m)
            exact = float(havelock_exact(N, m))
            assert abs(num - exact) < 1e-8, \
                f"N={N}, m={m}: T_m={num:.10f} != exact={exact}"


def test_trace_formula_sphere():
    for N in [4, 6, 8]:
        delta = trace_formula_delta(N, surface='sphere', R=1.0)
        expected = -N / (4 * np.pi)
        assert abs(delta - expected) / abs(expected) < 1e-10
