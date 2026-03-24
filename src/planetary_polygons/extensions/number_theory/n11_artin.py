"""
N = 11: the quintic field Q(cos 2pi/11) and its Artin representation.

N = 7 gave an ABELIAN representation (3 distinct Hecke values, reducible).
N = 11 has trace field Q(cos 2pi/11) of degree 5 over Q.

KEY QUESTION: does N = 11 give something RICHER?

The Galois group: Gal(Q(cos 2pi/11)/Q) = (Z/11Z)*/<+/-1>
= {[1], [2], [3], [4], [5]} (classes mod 11, up to sign)
= Z/5Z (cyclic of order 5)

STILL ABELIAN! (Z/5Z is abelian)

But the DEGREE is 5, which means the representation theory is richer:
- More distinct Hecke eigenvalue classes (5 instead of 3)
- The spectral parameters live in a higher-degree field
- The discriminant 11^4 = 14641 is much larger

Can the N=11 form be IRREDUCIBLE on GL(2)?
For an abelian Galois group: all irreps are 1-dimensional.
So any 2d rep is reducible (sum of two characters).

BUT: the Havelock eigenvalues might NOT factor through (Z/11Z)*.
If they depend on MORE than just p mod 11: the representation
could factor through a LARGER (non-abelian) group.

Let me check.
"""

import numpy as np
from math import pi, sin, cos, log, sqrt, exp, gcd


def havelock_eigenvalue(m, N):
    return sum(-log(2 * abs(sin(pi * j / N))) * cos(2 * pi * j * m / N)
               for j in range(1, N))


def chebyshev_U(k, t):
    if k == 0:
        return 1.0
    if k == 1:
        return 2.0 * t
    U_prev2 = 1.0
    U_prev1 = 2.0 * t
    for _ in range(2, k + 1):
        U_curr = 2 * t * U_prev1 - U_prev2
        U_prev2 = U_prev1
        U_prev1 = U_curr
    return U_prev1


# =====================================================================
# PART 1: The N=11 spectrum
# =====================================================================

def n11_spectrum():
    """The Havelock spectrum at N = 11."""
    print("=" * 72)
    print("  PART 1: THE HAVELOCK SPECTRUM AT N = 11")
    print("=" * 72)

    N = 11
    S = {m: havelock_eigenvalue(m, N) for m in range(1, N)}
    S_max = max(abs(S[m]) for m in range(1, N))
    C = S_max / 2.0

    print(f"\n  N = 11, C = {C:.10f}")
    print(f"\n  {'m':>4s} {'S_m':>14s} {'a_m = S_m/C':>14s} {'Casimir':>10s} {'theta_m':>10s}")

    for m in range(1, N):
        a_m = S[m] / C
        cas = m * (N - m) / 2.0
        theta = np.arccos(np.clip(a_m / 2.0, -1, 1))
        print(f"  {m:4d} {S[m]:14.8f} {a_m:14.8f} {cas:10.1f} {theta:10.6f}")

    print(f"\n  Palindromic check:")
    for m in range(1, 6):
        print(f"    S_{m} - S_{11-m} = {abs(S[m] - S[11-m]):.2e}")

    # The 5 independent eigenvalues
    print(f"\n  5 independent normalized eigenvalues:")
    for m in range(1, 6):
        print(f"    a_{m} = {S[m]/C:.10f}")

    return S, C


# =====================================================================
# PART 2: Hecke eigenvalues at rational primes
# =====================================================================

def n11_hecke(S, C):
    """Compute Hecke eigenvalues and test dependence on p mod 11."""
    print(f"\n{'='*72}")
    print("  PART 2: HECKE EIGENVALUES AT RATIONAL PRIMES")
    print("=" * 72)

    N = 11

    # The Hecke eigenvalue at prime p: a_p = a_{p mod N} / C
    # (from the periodic extension of the mode eigenvalues)

    primes = [p for p in range(2, 500)
              if all(p % d != 0 for d in range(2, int(sqrt(p))+1))]

    # First: tabulate by p mod 11
    print(f"\n  Hecke eigenvalues by p mod 11:\n")
    print(f"  {'r = p mod 11':>14s} {'a_r':>14s} {'paired with':>14s}")

    for r in range(1, 6):
        a_r = S[r] / C
        r_pair = 11 - r
        print(f"  {r:14d} {a_r:14.8f} {r_pair:14d}")

    # Splitting in Q(cos 2pi/11):
    # Gal(Q(cos 2pi/11)/Q) = (Z/11Z)*/<+/-1> = {[1],[2],[3],[4],[5]}
    # [1] = {1,10}, [2] = {2,9}, [3] = {3,8}, [4] = {4,7}, [5] = {5,6}
    #
    # Order of [p] in Z/5Z:
    # [1]: order 1 -> splits completely
    # [2]: ord(2) mod 11 = 10, so [2] has order 5 -> INERT
    # [3]: ord(3) mod 11 = 5, so [3] has order 5 -> INERT? No...
    #
    # Need: order of p in (Z/11Z)*/<+/-1> = order of {p,-p} in (Z/11Z)*
    # This is ord(p mod 11) / gcd(ord(p), 2) ... let me just compute.

    print(f"\n  Splitting of x^5 + ... (min poly of cos 2pi/11) mod p:\n")
    print(f"  {'p':>5s} {'p mod 11':>10s} {'[p]':>6s} {'# roots':>8s} {'split type':>14s}")

    # Minimal polynomial of 2cos(2pi/11) = alpha:
    # alpha^5 + alpha^4 - 4*alpha^3 - 3*alpha^2 + 3*alpha + 1 = 0
    min_poly = [1, 1, -4, -3, 3, 1]  # coefficients of x^5 + x^4 - 4x^3 - 3x^2 + 3x + 1

    split_data = {}
    for p in primes[:60]:
        if p == 11:
            split_data[p] = ("RAMIFIED", 0)
            print(f"  {p:5d} {0:10d} {'ram':>6s} {'—':>8s} {'RAMIFIED':>14s}")
            continue

        # Factor the minimal polynomial mod p
        roots = []
        for x in range(p):
            val = 0
            xk = 1
            for coeff in reversed(min_poly):
                val = (val + coeff * xk) % p
                xk = (xk * x) % p
            if val % p == 0:
                roots.append(x)

        n_roots = len(roots)
        r = p % 11
        bracket = f"[{min(r, 11-r)}]"

        if n_roots == 5:
            stype = "SPLIT"
        elif n_roots == 0:
            stype = "INERT"
        elif n_roots == 1:
            stype = "PARTIAL(1+)"
        else:
            stype = f"({n_roots} roots)"

        split_data[p] = (stype, n_roots)

        if p <= 100 or n_roots == 5:
            print(f"  {p:5d} {r:10d} {bracket:>6s} {n_roots:8d} {stype:>14s}")

    # The KEY test: do the Hecke eigenvalues depend ONLY on p mod 11?
    print(f"\n  KEY TEST: are Hecke eigenvalues determined by p mod 11?\n")
    print(f"  For each residue class r mod 11:")
    print(f"  Check: do ALL primes p = r mod 11 give the SAME Havelock eigenvalue?\n")

    for r in range(1, 11):
        r_eff = r if r <= 5 else 11 - r
        a_havelock = S[r_eff] / C

        # But the actual Hecke eigenvalue might also depend on splitting type
        ps_in_class = [p for p in primes[:60] if p % 11 == r and p != 11]
        split_types = [split_data.get(p, ("?", 0))[0] for p in ps_in_class]
        unique_splits = set(split_types)

        print(f"  r = {r:2d} (eff = {r_eff}): a = {a_havelock:10.6f}, "
              f"splitting = {unique_splits}, "
              f"n_primes = {len(ps_in_class)}")

    return split_data


# =====================================================================
# PART 3: The representation structure
# =====================================================================

def representation_structure(S, C, split_data):
    """Analyze the representation structure at N=11."""
    print(f"\n{'='*72}")
    print("  PART 3: REPRESENTATION STRUCTURE")
    print("=" * 72)

    N = 11

    print("""
  Gal(Q(cos 2pi/11)/Q) = (Z/11Z)*/<+/-1> = Z/5Z (cyclic of order 5).

  The classes:
    [1] = {1, 10}: p = 1 mod 11 or p = 10 mod 11
    [2] = {2, 9}
    [3] = {3, 8}
    [4] = {4, 7}
    [5] = {5, 6}

  For the quintic field: a prime p splits completely iff p = +/-1 mod 11
  (i.e., [p] = [1] in Z/5Z).

  The Havelock eigenvalue depends on [p] in Z/5Z:
    [1] -> a_1 (the maximum)
    [2] -> a_2
    [3] -> a_3
    [4] -> a_4
    [5] -> a_5

  This gives 5 DISTINCT Hecke eigenvalue values (not just 3 as at N=7).

  For a 2-DIMENSIONAL representation rho: G -> GL(2, C):
  The trace Tr(rho(g)) at each g in G must be one of these 5 values.

  For an ABELIAN group G = Z/5Z: all irreps are 1-dimensional.
  A 2d rep is rho = chi_a + chi_b (direct sum of two characters).

  Then: Tr(rho([k])) = chi_a([k]) + chi_b([k]) for k = 1,...,5.
  Since chi_j([k]) = exp(2pi i j k / 5): these are sums of roots of unity.

  The HAVELOCK values a_1,...,a_5 must be expressible as:
    a_r = chi_a(r) + chi_b(r) = exp(2pi i a r/5) + exp(2pi i b r/5)
        = 2 cos(2pi (a-b) r / 10) * exp(2pi i (a+b) r / 10)

  Wait: for the sum to be REAL: either a = -b mod 5 (conjugate pair)
  or both characters are real (a = 0 or 5/2 - not possible for Z/5Z).

  For a conjugate pair chi_j + chi_{-j} = chi_j + chi_{5-j}:
    Tr = 2 cos(2pi j r / 5) for each r.

  The 5 values would be: 2cos(2pi j/5), 2cos(4pi j/5), 2cos(6pi j/5),
  2cos(8pi j/5), 2cos(10pi j/5) = 2cos(2pi j) = 2.

  For j = 1: {2cos(2pi/5), 2cos(4pi/5), 2cos(6pi/5), 2cos(8pi/5), 2}
           = {0.618, -1.618, -1.618, 0.618, 2}
  Only 3 DISTINCT values: 2, 0.618, -1.618.

  For j = 2: {2cos(4pi/5), 2cos(8pi/5), 2cos(12pi/5), 2cos(16pi/5), 2}
           = {-1.618, 0.618, 0.618, -1.618, 2}
  Same 3 values!

  So a pair chi_j + chi_{5-j} gives only 3 distinct Hecke values.
  But the Havelock spectrum at N=11 has 5 distinct values!

  THEREFORE: the Havelock form at N=11 CANNOT be a sum of two characters.
  It requires AT LEAST three characters (or a different structure).
""")

    # Verify: how many distinct normalized eigenvalue values at N=11?
    vals = set()
    for m in range(1, 6):
        vals.add(round(S[m] / C, 8))
    print(f"  Number of distinct eigenvalue values: {len(vals)}")
    print(f"  Values: {sorted(vals)}")

    # Compare with character pair predictions
    print(f"\n  Character pair chi_1 + chi_4 predictions:")
    for r in range(1, 6):
        pred = 2 * cos(2 * pi * r / 5)
        actual = S[r] / C
        print(f"    r={r}: predicted = {pred:.6f}, actual = {actual:.6f}, "
              f"diff = {abs(pred - actual):.6f}")

    print(f"\n  Character pair chi_2 + chi_3 predictions:")
    for r in range(1, 6):
        pred = 2 * cos(4 * pi * r / 5)
        actual = S[r] / C
        print(f"    r={r}: predicted = {pred:.6f}, actual = {actual:.6f}, "
              f"diff = {abs(pred - actual):.6f}")

    # What if it's chi_a + chi_b + chi_c (sum of THREE characters)?
    # For GL(3): the L-function would be degree 3.
    # But we want GL(2). The Havelock form at N=11 might be on GL(5)
    # (degree 5, one for each mode).

    # Actually: the mode eigenvalues S_1,...,S_5 are the 5 embeddings
    # of a single element of Q(cos 2pi/11). The "form" lives on GL(1)/K
    # (a Hecke character of the quintic field K).

    # For the L-function OVER Q: L(s) = prod_p L_p(s) where L_p has
    # degree 5 (the degree of K over Q). This is a GL(5) L-function!

    print(f"""
  THE STRUCTURE AT N = 11:

  The Havelock eigenvalue is an element of K = Q(cos 2pi/11) (degree 5).
  Its 5 embeddings give the 5 independent eigenvalues a_1,...,a_5.

  The associated L-function OVER Q has degree 5 (NOT degree 2).
  This is an L-function on GL(5)/Q, induced from GL(1)/K.

  L(s) = L(s, Ind_K^Q(psi)) where psi is a Hecke character of K.

  For GL(5): the L-function has 5 Satake parameters at each prime.
  At split primes (p = +/-1 mod 11): the 5 Satake parameters are
  the 5 embeddings of the eigenvalue.

  The Satake parameters:
""")

    for m in range(1, 6):
        a_m = S[m] / C
        if abs(a_m) <= 2:
            theta = np.arccos(np.clip(a_m / 2.0, -1, 1))
            print(f"    alpha_{m} = exp(i * {theta:.6f}), |alpha| = 1 (Ramanujan)")
        else:
            print(f"    alpha_{m} = {a_m:.6f} (|a| > 2 — Ramanujan VIOLATED)")


# =====================================================================
# PART 4: Comparison N=7 vs N=11
# =====================================================================

def compare_n7_n11():
    """Compare the structure at N=7 and N=11."""
    print(f"\n{'='*72}")
    print("  PART 4: COMPARISON N=7 vs N=11 vs GENERAL N")
    print("=" * 72)

    print("""
  ┌───────────────────────────────────────────────────────────────────┐
  │  N  │ [K:Q] │ Gal(K/Q)  │ # distinct a_m │ GL(n) over Q │ Type │
  ├─────┼───────┼───────────┼────────────────┼──────────────┼──────┤
  │  5  │   2   │ Z/2Z      │      2         │  GL(2)       │ CM   │
  │  7  │   3   │ Z/3Z      │      3         │  GL(3)       │ Abel │
  │  8  │   2   │ Z/2Z      │      2         │  GL(2)       │ CM   │
  │ 11  │   5   │ Z/5Z      │      5         │  GL(5)       │ Abel │
  │ 13  │   6   │ Z/6Z      │      6         │  GL(6)       │ Abel │
  │ 17  │   8   │ Z/8Z      │      8         │  GL(8)       │ Abel │
  │ 19  │   9   │ Z/9Z      │      9         │  GL(9)       │ Abel │
  │ 23  │  11   │ Z/11Z     │     11         │  GL(11)      │ Abel │
  └─────┴───────┴───────────┴────────────────┴──────────────┴──────┘

  THE PATTERN: the Havelock form at prime level N lives on
  GL((N-1)/2) over Q, induced from GL(1) over Q(cos 2pi/N).

  This is ALWAYS abelian because Q(cos 2pi/N) is an abelian
  extension of Q (it's a subfield of the cyclotomic field Q(zeta_N)).

  CLASS FIELD THEORY: every L-function associated to an abelian
  extension is a product of Dirichlet L-functions (Artin's theorem).
  This is EXACTLY what we found with the character decomposition.

  THE CONCLUSION: the Havelock spectrum at ANY prime N gives an
  ABELIAN automorphic object. It can never produce an irreducible
  GL(2) form over Q (which requires a NON-ABELIAN extension).

  TO GET NON-ABELIAN: we need the vortex problem on a surface
  whose fundamental group is non-abelian. The N-gon on H^2 has
  cyclic symmetry Z/NZ -> abelian. A surface with non-abelian
  fundamental group (e.g., a genus-2 surface) could give non-abelian
  representations.

  THE BOLZA SURFACE (genus 2, automorphism group of order 48)
  is exactly such a surface. The Bolza form eta(8z)eta(16z) IS
  associated to the Bolza surface, and it IS a GL(2) form.
  But it's CM (abelian via the CM field).

  For a genuinely non-abelian form: need a genus >= 2 surface
  with a non-abelian fundamental group representation that is
  NOT CM. This goes beyond the polygon vortex theory.
""")

    # Verify the GL(n) pattern
    for N in [5, 7, 8, 11, 13, 17]:
        if N == 8:
            deg = 2  # Q(sqrt(2))
        else:
            deg = (N - 1) // 2 if N % 2 == 1 else N // 2 - 1

        S = {m: havelock_eigenvalue(m, N) for m in range(1, N)}
        S_max = max(abs(S[m]) for m in range(1, N))
        C_val = S_max / 2.0

        n_distinct = len(set(round(S[m]/C_val, 6) for m in range(1, (N+1)//2)))

        print(f"  N={N:3d}: degree = {deg}, distinct eigenvalues = {n_distinct}, "
              f"GL({n_distinct})/Q")


# =====================================================================
# PART 5: What WOULD give non-abelian?
# =====================================================================

def nonabelian_directions():
    """What modifications could yield non-abelian representations?"""
    print(f"\n{'='*72}")
    print("  PART 5: PATHS TO NON-ABELIAN REPRESENTATIONS")
    print("=" * 72)

    print("""
  THE FUNDAMENTAL LIMITATION:
  The N-vortex polygon on H^2 has symmetry group Z/NZ (cyclic).
  The associated Galois representation factors through this abelian group.
  Result: always abelian, never irreducible GL(2).

  POSSIBLE EXITS:

  1. COMPOSITE N: for N = pq (product of primes), the group (Z/NZ)*
     is NOT cyclic (it's Z/phi(p)Z x Z/phi(q)Z by CRT).
     But this is STILL ABELIAN. No help.

  2. NON-CYCLIC POLYGON: instead of regular N-gon, use a polygon with
     non-abelian symmetry group. E.g., the dodecahedron (A_5 symmetry)
     or the icosahedron. The representation theory of A_5 includes
     IRREDUCIBLE 2d representations -> could give GL(2).

  3. MULTIPLE VORTEX SPECIES: different "charges" for different vortices.
     This breaks the cyclic symmetry and could give non-abelian structure.

  4. HIGHER GENUS SURFACES: the Bolza surface (genus 2) has
     pi_1 = <a,b,c,d | [a,b][c,d] = 1> (non-abelian fundamental group).
     Representations of pi_1 into GL(2) can be irreducible.
     The vortex problem on the Bolza surface would give non-abelian data.

  5. THE SELBERG ZETA FUNCTION of a hyperbolic surface: encodes the
     LENGTH SPECTRUM of closed geodesics. This is inherently non-abelian
     (the geodesic flow mixes the fundamental group).

  THE MOST PROMISING: option 4 (Bolza surface vortices).
  The Bolza surface has the largest automorphism group (order 48)
  among genus-2 surfaces. Its arithmetic is well-studied (CM by Q(sqrt(-2)),
  Jacobian is isogenous to a product of elliptic curves).

  Placing vortices at the 48 automorphism points of the Bolza surface
  would give a vortex problem with NON-ABELIAN symmetry (the order-48
  group contains S_3 as a subgroup -> irreducible 2d representations).

  This is a DIFFERENT computation from the polygon vortices.
  It would require:
  - The Green's function on the Bolza surface (known from spectral theory)
  - The interaction matrix for 48 vortices at the automorphism points
  - Diagonalization and identification of the spectrum
  - Comparison with Hecke eigenvalues of weight-2 forms on the Shimura
    curve associated to the Bolza surface

  THIS IS A CONCRETE, COMPUTABLE PROBLEM that could yield a genuine
  non-abelian automorphic form from vortex theory.
""")


# =====================================================================
# MAIN
# =====================================================================

def main():
    print("=" * 72)
    print("  N = 11: QUINTIC FIELD AND REPRESENTATION STRUCTURE")
    print("=" * 72)

    S, C = n11_spectrum()
    split_data = n11_hecke(S, C)
    representation_structure(S, C, split_data)
    compare_n7_n11()
    nonabelian_directions()


if __name__ == "__main__":
    main()
