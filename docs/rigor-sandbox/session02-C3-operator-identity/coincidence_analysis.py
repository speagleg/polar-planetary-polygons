"""
C3 Phase 3: when does f(m, N) = j(j+1) for integer j?

The paper's Weinberg derivation uses the coincidence at (m, N) = (2, 4)
where f(2, 4) = 2 = j(j+1)|_{j=1} = C_2(j=1). Rigor plan asks:
is this a GENERAL pattern or a j=1-specific coincidence?

Analysis: enumerate (m, N) pairs with f(m, N) = j(j+1) for integer j ≥ 0.
"""

from __future__ import annotations

from fractions import Fraction


def f(m: int, N: int) -> Fraction:
    """Havelock Casimir eigenvalue: f(m, N) = m(N-m)/2."""
    return Fraction(m * (N - m), 2)


def jjp1(j: int) -> int:
    """j(j+1) for integer j ≥ 0."""
    return j * (j + 1)


def find_coincidences(N_max: int = 15, j_max: int = 8):
    """Find all (m, N) pairs where f(m, N) = j(j+1) for some integer j ≥ 0."""
    coincidences = []
    for N in range(3, N_max + 1):
        for m in range(0, N + 1):
            f_val = f(m, N)
            if f_val.denominator != 1:
                continue  # non-integer f
            f_int = f_val.numerator
            for j in range(0, j_max + 1):
                if f_int == jjp1(j):
                    coincidences.append((m, N, f_int, j))
                    break
    return coincidences


def main():
    print("=" * 78)
    print("C3 Phase 3: f(m, N) = j(j+1) coincidence analysis")
    print("=" * 78)
    print()
    print("Paper's claim: f(2, 4) = 2 = j(j+1)|_{j=1} = C_2 of SU(2) adjoint.")
    print("Rigor plan question: is this j=1 specific or a general pattern?")
    print()

    coincidences = find_coincidences(N_max=15, j_max=8)
    print(f"  {'m':>4} {'N':>4}  {'m(N-m)':>8}  {'f=m(N-m)/2':>12}  "
          f"{'j':>4}  {'j(j+1)':>8}  {'match':>6}")
    print("  " + "-" * 58)

    for (m, N, f_val, j) in coincidences:
        prod = m * (N - m)
        match = "✓" if f_val == jjp1(j) else "✗"
        # Flag polygon-theory special cases
        flag = ""
        if (m, N) == (2, 4):
            flag = "  [SU(2) adjoint — paper's case]"
        elif N == 7 and m in (3, 4):
            flag = "  [N=7 critical pair]"
        elif N == 7 and m in (1, 6):
            flag = "  [N=7 pair 1 — trivial]"
        elif N == 7 and m in (2, 5):
            flag = "  [N=7 pair 2]"
        print(f"  {m:>4} {N:>4}  {prod:>8}  {str(f_val):>12}  "
              f"{j:>4}  {jjp1(j):>8}  {match:>6}{flag}")

    print()
    print("=" * 78)
    print("Observations")
    print("=" * 78)
    print(f"\nTotal coincidences (m, N) pairs with f(m, N) = j(j+1) integer j, "
          f"N ≤ 15, j ≤ 8: {len(coincidences)}")
    print()
    print("Pattern: f(m, N) = j(j+1) happens iff m(N-m) = 2j(j+1), which")
    print("requires m(N-m) to be a 'twice-triangular' number 2T_j = j(j+1)·2.")
    print()
    print("For specific polygon values:")
    print("  N = 4, m = 2: f = 2, j = 1 ✓ (SU(2) ADJOINT — paper uses this)")
    print("  N = 5, m = 1,4: f = 2, j = 1")
    print("  N = 7, m = 3,4: f = 6, j = 2 (N=7 CRITICAL pair)")
    print("  N = 7, m = 2,5: f = 5, no integer j (j² + j = 10 has no integer sol)")
    print("  N = 7, m = 1,6: f = 3, no integer j (j² + j = 6 → j = 2 but 2·3=6 ≠ 3·2=6)")
    print()

    # Verify specific polygon cases
    print("Polygon-specific verification:")
    for (m, N) in [(2, 4), (3, 7), (4, 7), (1, 7), (2, 7)]:
        f_val = f(m, N)
        if f_val.denominator == 1:
            f_int = f_val.numerator
            # Find j such that j(j+1) = f_int
            j_matches = [j for j in range(0, 10) if j * (j + 1) == f_int]
            j_str = f"{j_matches[0]}" if j_matches else "NONE"
            print(f"  N={N}, m={m}: f = {f_val}, integer j with j(j+1) = {f_int}: {j_str}")
        else:
            print(f"  N={N}, m={m}: f = {f_val} (non-integer, no j match)")

    print()
    print("=" * 78)
    print("Conclusion")
    print("=" * 78)
    print("""
The coincidence f(m, N) = j(j+1) at integer j is NOT generic. It happens
at SPECIFIC (m, N) pairs where m(N-m) = 2j(j+1).

For the polygon theory:
  N = 4 (isospin): m* = 2 gives f = 2 = j(j+1)|_{j=1}
      → corresponds to SU(2)_L adjoint (spin-1, dim 3)
      → this is the identification used in Paper IV §11 Weinberg derivation

  N = 7 (color): m* = 3, 4 give f = 6 = j(j+1)|_{j=2}
      → corresponds to some sl(2, R) spin-2 rep (dim 5)
      → NOT directly used for SU(3) color derivation
      (SU(3) comes from McKay Z/3 → A_2, not from sl(2,R) j=2)

  Other pairs (1, 7), (2, 7) do NOT give integer j.

So the identification "f(m*, N) = C_2(j=1) = 2" at (m*, N) = (2, 4) is
SPECIFIC to this particular polygon + mode. It is NOT a general pattern
for all KK modes on all polygons — only for "resonant" pairs where
m(N-m)/2 happens to be a triangular number j(j+1)/2.

This is a POSITIVE finding: the identification isn't arbitrary. It uses
a genuine COINCIDENCE between:
  1. The polygon's Havelock eigenvalue at critical mode
  2. A standard Casimir eigenvalue j(j+1) for integer j

The paper's derivation is correct at (2, 4) but the identification is
MODE-SPECIFIC, not a general operator-theoretic equality.
""")


if __name__ == "__main__":
    main()
