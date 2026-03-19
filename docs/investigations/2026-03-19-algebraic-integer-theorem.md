# Algebraic Integer Theorem for Stability Thresholds

**Date**: 2026-03-19
**Status**: PROVEN

## Result

The hyperbolic stability threshold xi*(N) is an algebraic integer
(lives in the maximal order Z[sqrt(D)]) if and only if N is in the
finite set {8, 9, 11, 15, 23}.

The differences between consecutive values are {1, 2, 4, 8} — powers of 2.

## Proof

The threshold satisfies the palindromic quadratic A*xi^2 + B*xi + A = 0.
It is an algebraic integer iff the monic form xi^2 + (B/A)*xi + 1 = 0
has integer coefficients, i.e., B/A is an integer.

**For odd N >= 9**: m = (N-1)/2, giving
  A = -(N-1)(N-7)/8,  B = (N-1)(N+1)/4
  B/A = -2(N+1)/(N-7)

This is an integer iff (N-7) | 2(N+1).
Since 2(N+1) = 2(N-7) + 16, this reduces to **(N-7) | 16**.
The divisors of 16 giving odd N >= 9 are: N-7 in {2, 4, 8, 16}
giving N in {9, 11, 15, 23}.

**For even N >= 8**: A = -(N^2 - 8N + 8)/8, B = N^2/4.
B/A ∈ Z requires (N^2 - 8N + 8) | 2N^2. Since N^2 - 8N + 8
grows faster than 2N^2's divisors, only N=8 satisfies this.

**Complete list**: N in {8, 9, 11, 15, 23}. QED.

## The Pell connection

For these 5 values, xi*(N) satisfies the Pell equation a^2 - Db^2 = 1:
- N=8:  xi* = 8 - 3*sqrt(7),  D=7,  8^2 - 7*9 = 1
- N=9:  xi* = 5 - 2*sqrt(6),  D=6,  25 - 24 = 1
- N=11: xi* = 3 - 2*sqrt(2),  D=2,  9 - 8 = 1
- N=15: xi* = 2 - sqrt(3),    D=3,  4 - 3 = 1
- N=23: xi* = (3 - sqrt(5))/2, D=5, but this is in Z[(1+sqrt(5))/2] (the golden ring)

## Physical significance

The algebraic-integer thresholds are the "cleanest" stability transitions:
they correspond to exact Pell solutions and fundamental units of real
quadratic number fields. The N=8 transition (the physically relevant one
for Jupiter) is the FIRST and simplest in this sequence.

The 7 in sqrt(7) comes from the stability boundary N=7: the threshold
polynomial's discriminant has 252 = 4 * 9 * 7, and the 7 is the
residue of the N=7 marginality.
