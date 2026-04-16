"""
G3: derivation that pair 3 = Higgs doublet via BF-crossing.
===========================================================

The Breitenlohner-Freedman (BF) bound on H² (equivalently AdS_2 or AdS_3 boundary):
a scalar field is stable if and only if its conformal dimension c ≥ 1.
For c < 1, the scalar is BF-unstable: its mass squared is below the BF bound
(m² > -1/(4 R²) in H² units) and the field will CONDENSE to form a VEV.

In SM physics, the HIGGS is the unique scalar with a VEV (at the
electroweak scale). In a polygon-theory language, the Higgs is therefore
the unique BF-violating scalar mode.

**Claim**: the scalar mode at (m_7 ∈ {3, 4}, m_4 = 2) is uniquely
BF-violating in the polygon theory's KK spectrum, and this UNIQUELY
identifies pair 3 × critical m_4 as the Higgs doublet.

Scalar KK masses:
  On N=7 (color sector): μ^s_{m_7} = |m_7 - N/2| = |m_7 - 7/2|
  On N=4 (isospin sector): μ^s_{m_4} = |m_4 - N/2| = |m_4 - 2|

Effective conformal dimension:
  c² = (μ^s_{m_7})² + (μ^s_{m_4})²  (total KK mass squared on product Seifert)

BF-unstable iff c < 1.

We enumerate all (m_7, m_4) scalar modes and identify which are BF-unstable.
"""

from __future__ import annotations

from math import sqrt
from fractions import Fraction


def mu_scalar_N7(m7: int) -> Fraction:
    """Scalar KK mass on N=7: μ = |m_7 - 7/2|"""
    return abs(Fraction(m7) - Fraction(7, 2))


def mu_scalar_N4(m4: int) -> Fraction:
    """Scalar KK mass on N=4: μ = |m_4 - 2|"""
    return abs(Fraction(m4) - Fraction(2))


def conformal_dim_sq(m7: int, m4: int) -> Fraction:
    """Effective conformal dimension squared: c² = μ_7² + μ_4²."""
    mu7 = mu_scalar_N7(m7)
    mu4 = mu_scalar_N4(m4)
    return mu7 * mu7 + mu4 * mu4


def is_BF_unstable(m7: int, m4: int) -> bool:
    """BF-unstable iff c² < 1."""
    return conformal_dim_sq(m7, m4) < Fraction(1)


def main():
    print("=" * 76)
    print("G3: Higgs from BF-crossing")
    print("=" * 76)

    # Enumerate all scalar (m_7, m_4) modes in the polygon theory
    print(f"\n  {'(m_7, m_4)':>10}   {'μ²_7':>8}   {'μ²_4':>8}   "
          f"{'c²':>10}   {'c':>10}  {'BF-unstable?':>14}")
    print("  " + "-" * 72)

    unstable_modes = []
    for m7 in range(7):
        for m4 in range(4):
            mu7_sq = mu_scalar_N7(m7) ** 2
            mu4_sq = mu_scalar_N4(m4) ** 2
            c_sq = mu7_sq + mu4_sq
            c_val = float(c_sq) ** 0.5
            unstable = is_BF_unstable(m7, m4)
            if unstable:
                unstable_modes.append((m7, m4))
            flag = "✓ UNSTABLE" if unstable else "stable"
            print(f"  ({m7}, {m4})    {str(mu7_sq):>8}   {str(mu4_sq):>8}   "
                  f"{str(c_sq):>10}   {c_val:>10.4f}  {flag:>14}")

    print()
    print("=" * 76)
    print(f"BF-unstable scalar modes: {len(unstable_modes)}")
    for mode in unstable_modes:
        print(f"  (m_7 = {mode[0]}, m_4 = {mode[1]}):  "
              f"c² = {conformal_dim_sq(*mode)} < 1")
    print()

    # Check the uniqueness claim
    if set(unstable_modes) == {(3, 2), (4, 2)}:
        print("✓✓✓ UNIQUENESS VERIFIED: exactly 2 BF-unstable scalar modes")
        print()
        print("These are:")
        print("  (m_7 = 3, m_4 = 2): c² = 1/4, c = 1/2 < 1")
        print("  (m_7 = 4, m_4 = 2): c² = 1/4, c = 1/2 < 1")
        print()
        print("Both are in 'pair 3' of N=7 (i.e., palindromic pair (3, 4))")
        print("with m_4 = 2 (critical N=4 scalar mode).")
        print()
        print("Interpretation:")
        print("  - These 2 scalars are uniquely BF-unstable → condense → Higgs")
        print("  - They form an SU(2)_L doublet (2 components)")
        print("  - Y = 1/2 (from Q = m_4/N_4 = 2/4 at critical mode)")
        print("  - SU(3) singlet (m_7 ≠ 0, but in PS language the Higgs is")
        print("    the (1, 2, 2) bi-doublet with T_3L = ±1/2 coming from")
        print("    pair 3's two modes)")
        print()
        print("This is the DERIVATION that pair 3 is uniquely the Higgs: the")
        print("polygon theory's scalar KK spectrum has a UNIQUE BF-unstable")
        print("scalar pair, and it's at (m_7 ∈ {3, 4}, m_4 = 2).")
    else:
        print(f"✗ UNIQUENESS CLAIM FAILED: got {set(unstable_modes)}")
        print(f"  Expected: {{(3, 2), (4, 2)}}")

    print()
    print("=" * 76)
    print("Structural interpretation")
    print("=" * 76)
    print("""
The BF bound on hyperbolic H²: scalar field stability requires
  m² ≥ m²_BF = -(d-1)²/(4 R²) = -1/(4 R²) in 2D H²

This translates to conformal dimension c ≥ 1 for a scalar on H²
(equivalently at the boundary CFT).

For the polygon theory's scalar KK modes on R × (H² ×_7 S¹) × N=4 sector:
  c² = μ²_{7} + μ²_{4}  (total effective mass-squared in H² units)

The MINIMAL c² is achieved at:
  μ²_7 minimum: pair 3 (m_7 ∈ {3, 4}), giving μ²_7 = 1/4
  μ²_4 minimum: critical mode (m_4 = 2), giving μ²_4 = 0
  Total: c² = 1/4 < 1 ✓

All other (m_7, m_4) give c² ≥ 5/4 > 1 (stable).

So pair 3 at critical m_4 is the UNIQUE BF-violating scalar.

The Higgs identification is therefore DERIVED, not chosen.
""")


if __name__ == "__main__":
    main()
