# The Stability Counting Function on S²

**Date:** 2026-03-22
**Status:** PROVED (exact rational, from S² threshold table)

## The Result

On the 2-sphere, the total "stable volume" — the sum over polygon types
N = 3, ..., 7 of the fraction of the hemisphere where the N-gon is stable —
is an exact rational number:

$$\mathcal{N}(\Lambda) = \frac{1}{2} + \frac{1}{3} + \frac{1}{4} + \frac{1}{10} + 0 = \frac{71}{60}$$

where each term is $1 - \cos\varphi_{\text{crit}}(N) = 1 - m(N-m)/(2(N-1))$.

## The Stability Staircase

| Colatitude range | # stable types | Which N |
|---|---|---|
| φ₀ = 0° (pole) | 5 | 3,4,5,6,7 |
| 0° < φ₀ < 25.8° | 4 | 3,4,5,6 |
| 25.8° < φ₀ < 41.4° | 3 | 3,4,5 |
| 41.4° < φ₀ < 48.2° | 2 | 3,4 |
| 48.2° < φ₀ < 60° | 1 | 3 only |
| 60° < φ₀ < 90° | 0 | none |

## The Structure of 71/60

The sum of cosines is a **perfect square over 60**:

$$\sum_{N=3}^{6} \cos\varphi_{\text{crit}}(N) = \frac{1}{2}+\frac{2}{3}+\frac{3}{4}+\frac{9}{10} = \frac{169}{60} = \frac{13^2}{60}$$

Therefore: $\mathcal{N} = 4 - 13^2/60 = 71/60$.

The individual fractions have closed forms:

| N | Type | $1 - \cos\varphi_{\text{crit}}$ | Formula |
|---|---|---|---|
| 3 (odd, k=1) | 1/2 | $(3-k)/4$ |
| 4 (even, k=2) | 1/3 | $(4k-2-k^2)/(2(2k-1))$ |
| 5 (odd, k=2) | 1/4 | $(3-k)/4$ |
| 6 (even, k=3) | 1/10 | $(4k-2-k^2)/(2(2k-1))$ |
| 7 (odd, k=3) | 0 | $(3-k)/4 = 0$ (boundary) |

## The S²–H² Asymmetry

| | S² (Λ > 0) | Flat (Λ = 0) | H² (Λ < 0) |
|---|---|---|---|
| Curvature effect | destabilizes | neutral | stabilizes |
| N_crit | drops 7→2 | constant 7 | rises 7→∞ |
| Threshold fields | Q (rational) | — | Q(√D) (algebraic) |
| Stable volume N | 71/60 (finite) | 5 | ∞ |

The rationality of N(Λ>0) = 71/60 follows from the **linear** marginal
equation on S² (C₁ is linear fractional in ξ → rational roots).

The irrationality of H² thresholds follows from the **quadratic**
palindromic equation (→ algebraic-irrational roots in Q(√D)).

The flat plane is the transition point: all thresholds collapse to ξ = 0
(a degenerate rational), and N_crit = 7 is uniform.

## Significance

The number 71/60 is the **stability partition function** for polygon
configurations on the round sphere. It measures the total "phase space
volume" of stable configurations, analogous to a thermodynamic partition
function but counting geometric rather than statistical states.

The arithmetic of the palindromic hierarchy is the interference between
conformal invariance and geometric curvature — the residue that the
renormalization group cannot wash away.
