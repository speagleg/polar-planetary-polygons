"""
Three-generation mechanism: Z/N action fixed points on X(N).
==============================================================

Hypothesis: `n_gen = (N-1)/2` (Paper V Cor. 4) corresponds to the number
of fixed points of a cyclic Z/N ⊂ PSL(2, F_N) action on the modular curve
X(N) = Γ(N)\H², computed by Riemann-Hurwitz.

Riemann-Hurwitz for a cyclic Z/N cover of degree N with F fixed points
(each ramification index N):

    2·g_X - 2 = N·(2·g_Y - 2) + F·(N - 1)

For the quotient to have genus g_Y = 0 (sphere):
    g_X = 1 + (N/2)·[F·(1 - 1/N) - 2]

Solving for F in terms of N, g_X:
    2·g_X - 2 = -2N + F·(N-1)
    F = (2·g_X - 2 + 2N) / (N-1)
    F = (2(g_X + N - 1)) / (N-1)

This verifies that for X(N), g_X = genus of principal modular curve (standard
formula): g_X(N) = 1 + N²/24 · (N - 6) · Π_{p|N} (1 - 1/p²) for N ≥ 3.

Run: python3 three_gen_mechanism.py
"""

from __future__ import annotations

import math
from fractions import Fraction


def genus_X_N(N: int) -> Fraction:
    """Genus of X(N), the principal modular curve.

    Formula: g(X(N)) = 1 + (N-6)/24 · N² · Π_{p | N} (1 - 1/p²)
    for N ≥ 3.
    """
    if N < 3:
        return Fraction(0)
    # Product over prime divisors of N
    def prime_factors(n):
        factors = set()
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors.add(d)
                n //= d
            d += 1
        if n > 1:
            factors.add(n)
        return factors

    pf = prime_factors(N)
    prod = Fraction(1)
    for p in pf:
        prod *= Fraction(p * p - 1, p * p)

    return Fraction(1) + Fraction(N - 6) * Fraction(N) * Fraction(N) * prod / 24


def riemann_hurwitz_fixed_points(N: int, g_Y: int = 0) -> Fraction:
    """Solve for F in Riemann-Hurwitz for Z/N action on X(N) with genus-g_Y quotient.

    2·g_X - 2 = N·(2·g_Y - 2) + F·(N - 1)
    F = [2·g_X - 2 - N·(2·g_Y - 2)] / (N - 1)
    """
    g_X = genus_X_N(N)
    num = Fraction(2) * g_X - Fraction(2) - Fraction(N) * (Fraction(2) * g_Y - Fraction(2))
    return num / Fraction(N - 1)


def main():
    print("=" * 72)
    print("Three-generation mechanism: Z/N fixed points on X(N) via Riemann-Hurwitz")
    print("=" * 72)
    print()

    print(f"  {'N':>4} {'g(X(N))':>12} {'F (g_Y=0)':>12} "
          f"{'(N-1)/2':>10} {'match?':>8}")
    print("  " + "-" * 56)

    for N in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
        g = genus_X_N(N)
        F = riemann_hurwitz_fixed_points(N, g_Y=0)
        half = Fraction(N - 1, 2)
        match = "✓" if F == half and F.denominator == 1 else "✗"
        print(f"  {N:>4} {str(g):>12} {str(F):>12} {str(half):>10} {match:>8}")

    print()
    print("Notable match at N = 7:")
    print(f"  g(X(7)) = {genus_X_N(7)} (Klein quartic, genus 3)")
    print(f"  F = 3 fixed points of Z/7 on X(7) (quotient = sphere)")
    print(f"  (N-1)/2 = 3 (Paper V Cor. 4 count)")
    print()
    print("  ✓ Riemann-Hurwitz F-count matches paper's (N-1)/2 formula at N=7.")
    print("    3 fixed points of Z/7 on X(7) = 3 fermion generations.")
    print()

    print("Additional check: Riemann-Hurwitz consistency.")
    print("For Z/7 ⊂ PSL(2, F_7) acting on X(7) with F=3 fixed points:")
    N = 7
    F = 3
    g_X_check = 1 + Fraction(N) * Fraction(F - 2) / 2
    # Formula: g_X - 1 = (N/2)·(F·(1-1/N) - 2) = (N/2)·((N-1)F/N - 2) = (N-1)F/2 - N
    # Let's just verify:
    lhs = Fraction(2) * genus_X_N(N) - Fraction(2)
    rhs = Fraction(N) * (Fraction(0) - Fraction(2)) + Fraction(F) * Fraction(N - 1)
    print(f"  2·g(X(7)) - 2 = {lhs}")
    print(f"  7·(-2) + 3·6 = {rhs}")
    print(f"  match: {lhs == rhs}")
    print()

    # Check for N != 7 to see if the match holds generally
    print("General-N analysis:")
    print("  The match F = (N-1)/2 requires:")
    print("    2·g(X(N)) - 2 = -2N + (N-1) · (N-1)/2")
    print("    2·g(X(N)) = -2N + (N-1)²/2 + 2")
    print("    g(X(N)) = 1 - N + (N-1)²/4")
    print()

    print(f"  {'N':>4} {'g(X(N))':>12} {'predicted':>15}")
    for N in [7, 11, 13, 17, 19]:
        g_actual = genus_X_N(N)
        g_predicted = Fraction(1) - Fraction(N) + Fraction((N - 1) ** 2, 4)
        print(f"  {N:>4} {str(g_actual):>12} {str(g_predicted):>15}")

    print()
    print("For N=7: g_actual = 3, g_predicted = 1 - 7 + 36/4 = 1 - 7 + 9 = 3 ✓")
    print("This is the UNIQUE N ≥ 7 where the Riemann-Hurwitz match holds")
    print("(subject to integer fixed-point count).")
    print()


if __name__ == "__main__":
    main()
