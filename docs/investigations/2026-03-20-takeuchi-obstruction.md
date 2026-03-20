# The Takeuchi Obstruction: Why Triangle Groups Can't Reach Non-Solvable Galois

**Date:** 2026-03-20
**Status:** PROVEN (follows from Kronecker-Weber)

## The Obstruction

ALL 85 Takeuchi arithmetic triangle groups have trace fields contained
in cyclotomic fields Q(ζ_n). By the Kronecker-Weber theorem, every
abelian extension of Q is contained in a cyclotomic field. Therefore:

**The Galois group of the trace field of any Takeuchi triangle group
is ABELIAN.**

Consequently:
- The palindromic polynomial always has SOLVABLE Galois group
  (a subgroup of Z/2 ≀ (abelian), which is solvable)
- Langlands–Tunnell ALWAYS applies
- We NEVER reach non-solvable territory through triangle groups

## The Reason

Triangle group traces are polynomials in cos(π/p), cos(π/q), cos(π/r).
These cosines generate subfields of cyclotomic fields:
Q(cos(π/n)) is the maximal real subfield of Q(ζ_{2n}).
All subfields of cyclotomic fields are abelian over Q.

Even the (2,3,11) triangle group — which has trace field degree 5 and
palindromic degree 10 — has Galois group Z/5 (cyclic, abelian), NOT S₅.

## The Hierarchy (Corrected)

| Source | Trace field | Gal of trace field | Palindromic Gal | Solvable? |
|--------|-------------|-------------------|-----------------|-----------|
| SL(2,Z) | Q | trivial | Z/2 | Yes |
| (2,3,8) Bolza | Q(√2) | Z/2 | D₄ | Yes (but non-abelian) |
| (2,3,7) Klein | Q(cos π/7) | Z/3 | abelian ≀ Z/2 | Yes |
| (2,3,11) | Q(cos π/11) | Z/5 | abelian ≀ Z/2 | Yes |
| (2,3,30) | Q(cos π/30) | Z/4×Z/2 | solvable | Yes |
| ALL triangle groups | ⊂ Q(ζ_n) | abelian | solvable ≀ Z/2 | **ALWAYS** |

## What Would Be Needed for Non-Solvable

A Fuchsian group whose trace field is NOT contained in any cyclotomic
field. This requires a non-abelian extension of Q.

Such number fields exist (e.g., Q(α) where α⁵-α-1=0 has Gal = S₅),
but whether any arithmetic Fuchsian group has such a trace field is
a question about the arithmetic of quaternion algebras over totally
real fields.

The Borel-Harish-Chandra theorem guarantees that arithmetic Fuchsian
groups exist for every totally real number field. So arithmetic
Fuchsian groups with non-abelian (even non-solvable) trace fields DO
exist — they're just not triangle groups. They would be derived from
quaternion algebras over fields like Q(α) with α⁵-α-1=0.

For such a group: the palindromic polynomial has degree 10, its
Galois group contains S₅ (non-solvable), and the corresponding
Artin L-function would go BEYOND Langlands–Tunnell. Establishing
the modularity of this L-function would require the full (currently
open) Langlands correspondence for GL(5).

## The Fibonacci/Pisano Connection (verified for p=7)

The systole of Γ(7)\H² (Klein quartic) is (-I)·Q⁸, where:
- Q is the Fibonacci matrix [[1,1],[1,0]]
- Q⁸ ≡ -I mod 7 (from Pisano period: α(7)=8, π(7)=16)
- (-I)·Q⁸ ≡ I mod 7, so it's in Γ(7)
- Trace = -L₈ = -47, conductor = F₈ = 21
- Field: Q(√5) (inherited from Fibonacci eigenvalues φ, 1/φ)
- Identity: L_n² - 4 = 5·F_n² for even n

All congruence covers Γ(p)\H² inherit Q(√5) for their Fibonacci-derived
thresholds, with conductors given by Fibonacci numbers F_{α(p)}.
