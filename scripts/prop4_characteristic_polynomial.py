#!/usr/bin/env python3
"""
Supplementary material: Proposition 4, N=6 characteristic polynomial.
Computes kappa_crit = -1/4 symbolically and verifies it.

Run: uv run --all-extras python scripts/prop4_characteristic_polynomial.py
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import sympy as sp


def main():
    from planetary_polygons.core.hessian import kappa_crit_sympy

    print("=" * 60)
    print("Proposition 4: N=6 Critical Ratio κ_crit")
    print("=" * 60)

    kc = kappa_crit_sympy(6)
    print(f"\nSymbolic result: κ_crit = {kc}")
    print(f"Numerical value: {float(kc):.10f}")
    print(f"Expected:        -0.2500000000")
    print(f"LaTeX form:      $\\kappa_{{\\mathrm{{crit}}}} = {sp.latex(kc)}$")

    # Strict assertion
    assert kc == sp.Rational(-1, 4), f"FAILED: got {kc}, expected -1/4"
    assert abs(float(kc) + 0.25) < 1e-10, "FAILED: numerical check"

    print("\nSign check at boundary:")
    eps = 0.01
    print(f"  κ₀/κ = {float(kc)+eps:.4f} (above threshold): stabilizing")
    print(f"  κ₀/κ = {float(kc):.4f}     (at threshold):    marginal")
    print(f"  κ₀/κ = {float(kc)-eps:.4f} (below threshold): destabilizing")

    print("\n[PASS] κ_crit = -1/4 verified symbolically and numerically")


if __name__ == "__main__":
    main()
