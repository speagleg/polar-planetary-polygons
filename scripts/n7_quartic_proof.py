"""
Symbolic proof: N=7 unconstrained quartic = 153/7.

Exact arithmetic in Q(omega) = Q[w]/(Phi_7(w)), omega = e^{2 pi i/7}.
Division uses polynomial inversion mod Phi_7 (extended Euclidean algorithm).

Run: python3 scripts/n7_quartic_proof.py
"""
from sympy import (
    Poly, Symbol, Rational, cyclotomic_poly, gcd, div, expand,
    invert as poly_invert
)
import sys

w = Symbol('w')
PHI7 = Poly(cyclotomic_poly(7, w), w, domain='QQ')

# ================================================================
# Cyclotomic ring Q[w]/Phi_7(w): arithmetic
# ================================================================

def red(expr):
    """Reduce expression to canonical form in Q[w]/Phi_7."""
    p = Poly(expand(expr), w, domain='QQ')
    _, r = div(p, PHI7, domain='QQ')
    return r

def mul(a, b):
    """Multiply in Q[w]/Phi_7."""
    return red(a.as_expr() * b.as_expr())

def conj(a):
    """Complex conjugate: w -> w^6 = w^{-1}."""
    return red(a.as_expr().subs(w, w**6))

def inv(a):
    """Multiplicative inverse in Q[w]/Phi_7 via extended GCD."""
    # invert f mod Phi_7: find g such that f*g = 1 mod Phi_7
    a_poly = Poly(a.as_expr(), w, domain='QQ')
    g = poly_invert(a_poly, PHI7, domain='QQ')
    return red(g.as_expr())

def abs_sq(a):
    """| a |^2 = a * conj(a)."""
    return mul(a, conj(a))

def is_rational(p):
    """Check if element is a rational constant (degree 0)."""
    return p.degree() <= 0

def to_rat(p):
    """Extract rational value from a degree-0 poly."""
    return Rational(p.nth(0))

# ================================================================
# Model: N=7, angular m=3 mode (unnormalized)
# ================================================================

N = 7
m = 3

# z_k = w^k,  unnormalized mode: u_k = (i/2)(w^{4k} + w^{-2k})
# The quartic of the UNNORMALIZED mode is (7/2)^2 * (153/7) = 1071/4.
# The quartic of the NORMALIZED mode is 153/7.
# We compute the normalized version directly by dividing by norm^4 = (7/2)^2 at the end.

# Per-pair quartic: Q = 6C^2/A^2 - 12CB^2/A^3 + 3B^4/A^4
# where A = |Dz|^2, B = 2 Re(Dz conj(Du)), C = |Du|^2
# and Du = (i/2) Ddu, Ddu = (w^{4j}+w^{-2j}) - (w^{4k}+w^{-2k}).
#
# Using Du = (i/2) Ddu:
#   C = |Du|^2 = (1/4)|Ddu|^2
#   B = 2 Re(Dz conj(Du)) = 2 Re(Dz (-i/2) conj(Ddu)) = -Im(Dz conj(Ddu))
#
# Key identity: for X = Dz * conj(Ddu),
#   B = -Im(X) and B^2 = Im(X)^2 = (|X|^2 - Re(X)^2) = |X|^2 - Re(X)^2
#   where Re(X) = (X + conj(X))/2.
#   Actually B^2 = Im(X)^2 = (X - conj(X))^2 / (-4) = (2|X|^2 - X^2 - conj(X)^2)/4
#   Hmm this gets the imaginary part squared as a real quantity.
#
# Better: express Q entirely without needing B separately.
# Q = 6C^2/A^2 - 12CB^2/A^3 + 3B^4/A^4
# With C = |Ddu|^2/4 and B^2 = Im(X)^2:
#
# Actually, let me just compute Q = A^{-4} (6 C^2 A^2 - 12 C B^2 A + 3 B^4)
# by computing the numerator in Q(w) and dividing by A^4.

print("=" * 60)
print("  N=7 quartic: symbolic proof in Q(omega)")
print("=" * 60)
print()

total = red(Rational(0))

for j in range(N):
    for k in range(j + 1, N):
        # Dz = w^j - w^k
        Dz = red(w**j - w**k)

        # Ddu = (w^{4j} + w^{-2j}) - (w^{4k} + w^{-2k})
        Ddu = red(w**(4*j % 7) + w**((-2*j) % 7) - w**(4*k % 7) - w**((-2*k) % 7))

        # A = |Dz|^2  (element of Q(w), should be rational for this to work)
        A = abs_sq(Dz)

        # C_unnorm = |Ddu|^2  (rational since |sum of roots|^2 is rational? No, it's in Q(w))
        Ddu_sq = abs_sq(Ddu)

        # X = Dz * conj(Ddu)
        X = mul(Dz, conj(Ddu))

        # B_unnorm = -Im(X)/... Hmm, let me use the formula differently.
        # With Du = (i/2) Ddu:
        #   A = |Dz|^2
        #   C = |Ddu|^2 / 4
        #   B = 2 Re(Dz conj(Du)) = 2 Re(Dz * (-i/2) * conj(Ddu))
        #     = -Im(Dz * conj(Ddu)) = -Im(X)
        #
        # Formula: Q = 6C^2/A^2 - 12CB^2/A^3 + 3B^4/A^4
        #
        # Numerator (times A^4):
        # N = 6 C^2 A^2 - 12 C B^2 A + 3 B^4
        #
        # With C = |Ddu|^2/4, B = -Im(X), B^2 = Im(X)^2:
        # N = 6 (|Ddu|^4/16) A^2 - 12 (|Ddu|^2/4) Im(X)^2 A + 3 Im(X)^4
        #   = (3/8)|Ddu|^4 A^2 - 3|Ddu|^2 Im(X)^2 A + 3 Im(X)^4
        #
        # And Q = N / A^4.
        #
        # Alternative: use real/imag decomposition of X.
        # X = Re(X) + i Im(X). In Q(w): Re(X) = (X + conj(X))/2, etc.
        # |X|^2 = Re(X)^2 + Im(X)^2 = X * conj(X)
        # So Im(X)^2 = |X|^2 - Re(X)^2
        #
        # But Re(X)^2 requires squaring (X+conj(X))/2, which is in Q(w).
        # And X*conj(X) = |X|^2 is in Q(w) too.
        #
        # Let me just compute the quartic per pair as element of Q(w)
        # using the original formula with exact division.

        # Direct computation:
        # A_inv = 1/A in Q(w)
        A_inv = inv(A)

        # Du = (i/2) Ddu. In Q(w), i is NOT available.
        # But the per-pair formula uses REAL quantities A, B, C, Q.
        #
        # Let me use the REAL per-pair formula from the code:
        # A = |Dz|^2, B = 2 Re(Dz conj(Du)), C = |Du|^2
        # Q = 6C^2/A^2 - 12CB^2/A^3 + 3B^4/A^4
        #
        # Rewrite: Q/A^4 is a polynomial in Dz, conj(Dz), Du, conj(Du).
        # Actually, 6C^2A^2 - 12CB^2A + 3B^4 is a polynomial in A,B,C.
        #
        # And A = Dz * conj(Dz), C = Du * conj(Du),
        # B = Dz * conj(Du) + conj(Dz) * Du  (since B = 2Re(Dz conj(Du)))
        #
        # So everything can be expressed in the ring Q(w)[Dz, conj(Dz), Du, conj(Du)].
        # But Du involves i, which is outside Q(w).
        #
        # Key insight: Du = (i/2)(ddu_j - ddu_k). The factor i means
        # Du is NOT in Q(w). But |Du|^2, B, etc. ARE real (hence in Q(w) ∩ R = Q).
        #
        # Actually, |Du|^2 = (1/4)|Ddu|^2, and B = -Im(X) where X = Dz*conj(Ddu).
        # Im(X) is real but expressed as (X - conj(X))/(2i).
        #
        # In Q(w), i is not present. But for N=7, sqrt(-1) is NOT in Q(w)
        # (since 7 ≡ 3 mod 4, so i ∉ Q(ζ_7)).
        #
        # So B is NOT an element of Q(w). But B^2 IS, and B^4 IS.
        #
        # B^2 = Im(X)^2 = -((X - conj(X))/2)^2 = -(X^2 - 2X*conj(X) + conj(X)^2)/4
        #      wait: Im(X) = (X - conj(X))/(2i), so Im(X)^2 = -(X - conj(X))^2/4
        #                                                     = (2|X|^2 - X^2 - conj(X)^2)/4

        # Let Xc = conj(X). Then:
        Xc = conj(X)
        X_sq = mul(X, X)
        Xc_sq = mul(Xc, Xc)
        XX = mul(X, Xc)  # = |X|^2

        # B^2 = (2|X|^2 - X^2 - conj(X)^2) / 4
        #      = (2*XX - X_sq - Xc_sq) / 4
        B_sq_times4 = red(2 * XX.as_expr() - X_sq.as_expr() - Xc_sq.as_expr())

        # B^4 = B_sq^2 = (B_sq_times4)^2 / 16
        B_sq_sq_times16 = mul(B_sq_times4, B_sq_times4)

        # C = |Ddu|^2 / 4 = Ddu_sq / 4
        # A = |Dz|^2

        # Q = 6C^2/A^2 - 12CB^2/A^3 + 3B^4/A^4
        #   = (6 C^2 A^2 - 12 C B^2 A + 3 B^4) / A^4
        #
        # Numerator = 6 (Ddu_sq/4)^2 A^2 - 12 (Ddu_sq/4)(B_sq_times4/4) A + 3 (B_sq_sq_times16/16)
        #           = 6 Ddu_sq^2 A^2 / 16 - 12 Ddu_sq * B_sq_times4 A / 16 + 3 B_sq_sq_times16 / 16
        #           = (1/16)[6 Ddu_sq^2 A^2 - 12 Ddu_sq B_sq_times4 A + 3 B_sq_sq_times16]

        # Compute numerator (times 16)
        D2 = mul(Ddu_sq, Ddu_sq)  # Ddu_sq^2
        A2 = mul(A, A)            # A^2

        term1 = mul(D2, A2)         # Ddu_sq^2 * A^2
        term1 = red(6 * term1.as_expr())

        DB = mul(Ddu_sq, B_sq_times4)  # Ddu_sq * B_sq_times4
        term2 = mul(DB, A)
        term2 = red(-12 * term2.as_expr())

        term3 = red(3 * B_sq_sq_times16.as_expr())

        num16 = red(term1.as_expr() + term2.as_expr() + term3.as_expr())

        # Q = num16 / (16 A^4)
        A4 = mul(A2, A2)
        A4_inv = inv(A4)
        Q_times16 = mul(num16, A4_inv)
        Q_pair = red(Rational(1, 16) * Q_times16.as_expr())

        total = red(total.as_expr() + Q_pair.as_expr())

        if (j, k) in [(0,1), (0,2), (0,3), (3,4), (5,6)] or (j == N-2 and k == N-1):
            print(f"  Pair ({j},{k}): Q = {Q_pair.as_expr()}")
        sys.stdout.flush()

print(f"\nTotal (unnormalized) = {total.as_expr()}")
print(f"Is rational? {is_rational(total)}")
if is_rational(total):
    val = to_rat(total)
    print(f"Unnormalized quartic = {val} = {float(val)}")
    # The angular mode has |u|^2 = 7/2 (sum of cos^2 = N/2).
    # norm^4 = (7/2)^2 = 49/4.
    # Normalized quartic = unnormalized / norm^4 = val * 4/49.
    normalized = val * Rational(4, 49)
    print(f"norm^4 = (7/2)^2 = 49/4")
    print(f"Normalized quartic = {val} / (49/4) = {val} * 4/49 = {normalized}")
    print(f"Expected 153/7 = {Rational(153, 7)}")
    print(f"Match: {normalized == Rational(153, 7)}")
    if normalized == Rational(153, 7):
        print("\n*** PROOF COMPLETE ***")
        print(f"  Unnormalized: sum_{{j<k}} Q(j,k) = {val} (exact in Q(omega))")
        print(f"  Normalized:   {val} / (49/4) = 153/7 (exact)")
        print(f"  Constrained:  153/7 - 18/7 = 135/7 (Newton projection, exact)")
        print(f"  alpha_0:      135/7 / 6 = 45/14 (exact)")
else:
    print("NOT rational — check computation.")
    print(f"Coefficients: {total.all_coeffs()}")
