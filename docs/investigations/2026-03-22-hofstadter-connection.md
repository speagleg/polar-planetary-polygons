# The Hofstadter Connection: Vortex Thresholds and Band Edges

**Date:** 2026-03-22
**Status:** ESTABLISHED (partial — Q(√5) confirmed, Q(√3) fails)

## The Result

The algebraic number φ⁻² = (3−√5)/2 ≈ 0.3820 appears as:

1. **Vortex:** the stability threshold ξ*(23) for the 23-gon on H²
2. **Hofstadter:** a band edge of the Harper equation at flux α = 1/5

Both are roots of x² − 3x + 1 = 0 (the minimal polynomial of φ⁻²
in Q(√5)). The Galois conjugate φ² = (3+√5)/2 also appears in both:
ξ*(23)⁻¹ in the vortex (palindromic dual) and a band edge at α = 2/5
in Hofstadter.

## The Norm +1 Selection Rule

Among algebraic integers of Z[φ] with |x| < 4:
- **7 out of 103** hit Harper band edges (6.8% observed vs 1.5% random = 4.7× excess)
- **All exact matches have norm +1** (product of Galois conjugates = +1)
- Specifically: only {0, ±φ⁻², ±φ²} match — the units of Z[φ] with norm +1

Among the 23 units ±φⁿ with |x| < 5:
- **0 out of 12** odd-power units (norm −1) are Harper edges
- **4 out of 11** even-power units (norm +1) are Harper edges
- The selection is sharp: no odd-power unit comes within 0.41 of an edge

**The norm +1 condition is structural:** it follows from det(T_q) = 1
for the Harper transfer matrix AND from the palindromic condition
(constant term = 1) for the vortex threshold polynomial. Both are
consequences of the SL(2,Z) structure underlying both problems.

## The Q(√3) Failure

2 − √3 (the vortex threshold ξ*(15)) does NOT appear as a Harper
band edge at α = 1/12. Tr(2−√3) = −5.61 at α = 1/12 — far from ±2.
The closest Harper edge is 0.089 away.

The sharing of algebraic numbers is **specific to Q(√5)**, not general.
It works because φ⁻² = 2cos(2π/5) − 1 is simultaneously a Chebyshev
value (from the Harper trigonometry) and a palindromic root (from the
vortex stability). This double role is special to the golden ratio.

## The Selberg Connection

Every closed geodesic on SL(2,Z)\H² is parameterised by a norm +1 unit
of Q(√D) where D = t² − 4 and t is the matrix trace. This is AUTOMATIC
from det(γ) = 1.

The vortex threshold ξ*(23) corresponds to the trace-3 geodesic
(the shortest geodesic in Q(√5), length ≈ 1.925).

## Code

- Harper equation computation: inline in this session (not a standalone module)
- Band edge finder: `find_harper_edges(p, q)` using transfer matrix product
- Algebraic integer enumeration: Z[φ] = {a + bφ : a, b ∈ Z}
- Norm selection test: verified for all units ±φⁿ with |x| < 5

## For the Paper

The φ⁻² coincidence and the norm +1 selection rule are clean results.
The Q(√3) failure is equally important — it shows the connection is
specific to the golden ratio's unique properties, not a universal
KK-theoretic phenomenon. Both the positive and negative results
should be reported.
