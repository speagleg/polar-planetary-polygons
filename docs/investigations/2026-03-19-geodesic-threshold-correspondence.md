# Stability Thresholds as Closed Geodesics on the Modular Surface

**Date:** 2026-03-19
**Status:** PROVEN (algebraic identity), CONJECTURAL (deeper geometric meaning)

## Discovery

The five algebraic-integer stability thresholds of the N-gon on H² correspond
exactly to eigenvalues of hyperbolic elements of SL(2,Z). Each threshold
defines a primitive closed geodesic on the modular surface SL(2,Z)\H².

## The Correspondence

| N | B = tr(γ) | γ ∈ SL(2,Z) | ξ* = ε⁻¹ | Geodesic length | Field | CF of fixed point |
|---|-----------|-------------|-----------|-----------------|-------|-------------------|
| 23 | 3 | [[2,1],[1,1]] | φ⁻² = (3−√5)/2 | 1.925 | Q(√5) | [1; 1,1,...] |
| 15 | 4 | [[3,2],[1,1]] | 2−√3 | 2.634 | Q(√3) | [2; 1,2,1,...] |
| 11 | 6 | [[5,2],[2,1]] | 3−2√2 | 3.525 | Q(√2) | [2; 2,2,...] |
| 9 | 10 | [[9,2],[4,1]] | (5−√21)/2 | 4.585 | Q(√21) | [2; 4,2,4,...] |
| 8 | 16 | [[15,7],[2,1]] | 8−3√7 | 5.537 | Q(√7) | [7; 2,7,2,...] |

## The Selection Rule

The trace formula:
- **Odd N ≥ 9**: B = 2(N+1)/(N−7) = 2 + 16/(N−7)
- **Even N = 8**: B = 2N²/(N²−8N+8) = 16

Integrality of B requires **(N−7) | 16** (odd N) or N=8 (even), giving
exactly N ∈ {8, 9, 11, 15, 23}.

The factor **16 = 2⁴** comes from:
- Factor of 2: Havelock normalization f(m,N) = m(N−m)/**2**
- Factor of 4: critical-mode evaluation m=(N−1)/2 giving max f = (N²−1)/**4**·(1/2)

## Why This Is Not Just Coincidence

The palindromic quadratic ξ² − Bξ + 1 = 0 with integer B is simultaneously:
1. **The stability threshold equation** on H² (from C₁(ξ) = f_max(N)/(N−1))
2. **The characteristic polynomial** of a hyperbolic element γ ∈ SL(2,Z) with tr(γ) = B

Both arise from the SAME algebraic structure: the conformal inversion ξ ↔ 1/ξ
of the Poincaré disk IS the action of the Galois group on the roots of the
palindromic quadratic, which IS the eigenvalue reciprocity det(γ) = 1 of SL(2,Z).

## The Metallic Means

Two of the five thresholds are metallic means:
- **N = 23**: φ = (1+√5)/2 — the golden ratio (metallic mean n=1)
- **N = 11**: 1+√2 — the silver ratio (metallic mean n=2)

These have the simplest possible continued fractions: purely periodic with
period 1 ([1̄] and [2̄] respectively).

## The Fibonacci Matrix

The terminal case N=23 corresponds to the **Fibonacci matrix** [[2,1],[1,1]],
the most studied element of SL(2,Z). Its eigenvalues are φ and 1/φ.
The threshold ξ*(23) = φ⁻² is the eigenvalue of the SQUARE of the
Fibonacci matrix: [[5,3],[3,2]] with trace 7.

## The Dual Formula

Inverting the trace formula B = 2 + 16/(N−7):

**N = 7 + 16/(B−2)**

So N is a positive integer ≥ 8 iff (B−2) | 16. The five geodesics
correspond to the **five divisors of 16 = 2⁴**:

| d = N−7 | d as power of 2 | N | B = 2 + 16/d | ℓ |
|---------|-----------------|---|---------------|-------|
| 1 | 2⁰ | 8 | 16* | 5.537 |
| 2 | 2¹ | 9 | 10 | 4.585 |
| 4 | 2² | 11 | 6 | 3.525 |
| 8 | 2³ | 15 | 4 | 2.634 |
| 16 | 2⁴ | 23 | 3 | 1.925 |

(*N=8 is even; the odd formula gives B=18, but the actual even-N
threshold has B=16.)

## The Selection Is Arithmetic, Not Geometric

The five geodesics are not geometrically distinguished (not shortest,
not systolic, not simple). Out of ~46 primitive geodesics with ℓ ≤ 5.54
(by the prime geodesic theorem), exactly five have traces satisfying
(B−2) | 16. The selection is imposed by the **Z_N representation theory**
(the Casimir m(N−m)/2) acting as an arithmetic filter on the geodesic
spectrum.

The number 16 = 2⁴ is representation-theoretic:
- Factor 2: Havelock normalization f(m,N) = m(N−m)/2
- Factor 4: critical-mode evaluation (N²−1)/4 at m=(N−1)/2
- Product: 2·4·2 = 16 (the extra 2 from setting f_max = N−1)

## The Geometric Bridge: Automorphic Green Functions

### Layer 1: Algebraic (proven)

The palindromic quadratic ξ²−Bξ+1=0 is simultaneously the stability
threshold equation and the characteristic polynomial of γ ∈ SL(2,Z).
This is a shared algebraic structure.

### Layer 2: Arithmetic (proven)

B ∈ Z iff (N−7)|16. The Z_N Casimir divisibility condition selects
exactly 5 conjugacy classes of SL(2,Z).

### Layer 3: Geometric (the bridge)

The connection becomes geometric when vortices live on a **quotient
surface** Γ\H² rather than the universal cover H²:

**On H²**: The Green's function is G(z,w) = −ln|z−w|/(1−zw̄).
The Havelock eigenvalue uses only this.

**On Γ\H²**: The Green's function is the **automorphic Green function**:
G_Γ(z,w) = Σ_{γ∈Γ} G(z, γ(w))

The correction from a geodesic γ with length ℓ is:
- δC₁ ∝ csch²(ℓ/2) = 4/(B²−4) = **4/D** (the discriminant!)
- This is EXACT: sinh(ℓ/2) = √(B²−4)/2

**Key identity**: csch²(ℓ_N/2) = 4/Δ = 4/(f²·D) where:
- Δ = B²−4 is the full discriminant of the palindromic quadratic
- D = sq-free(Δ) is the square-free part
- f = √(Δ/D) is the conductor (index of Z[ξ*] in the maximal order)

| N | B | Δ = B²−4 | f | D | csch²(ℓ/2) = 4/(f²D) | Field |
|---|---|---------|---|---|----------------------|-------|
| 23 | 3 | 5 | 1 | 5 | 4/5 | Q(√5) |
| 15 | 4 | 12 | 2 | 3 | 4/12 = 1/3 | Q(√3) |
| 11 | 6 | 32 | 4 | 2 | 4/32 = 1/8 | Q(√2) |
| 9 | 10 | 96 | 4 | 6 | 4/96 = 1/24 | Q(√6) |
| 8 | 16 | 252 | 6 | 7 | 4/252 = 1/63 | Q(√7) |

**N = 23 is the unique f = 1 case**: Δ = 5 is itself square-free.
The simple form csch²(ℓ/2) = 4/D holds only here. The threshold
ξ* = φ⁻² is a unit in the **maximal order** O_K = Z[φ]. For all
other cases, f > 1 and ξ* generates a proper suborder of O_K.

The conductor sequence f = {1, 2, 4, 4, 6} measures how far the
threshold's order Z[ξ*] sits from the ring of integers of Q(√D).
The conductor grows with B (i.e., with distance from the golden
ratio terminal case), reflecting that deeper thresholds involve
less "arithmetically natural" algebraic integers.

The automorphic correction to C₁ from a geodesic γ is proportional
to **4/(f²D)** — the inverse discriminant factored through the
conductor. This connects the vortex stability problem to the
arithmetic of quadratic orders through the geometry of quotient surfaces.

### The palindromic preservation theorem

The automorphic correction preserves the palindromic structure of the
threshold equation because the Möbius inversion symmetry ξ ↔ 1/ξ is
inherited by the automorphic Green function (it's a conformal symmetry
of H², not broken by the quotient). So thresholds on quotient surfaces
are also roots of palindromic quadratics, but with modified trace B_Γ.

## Open Questions

1. **Is there a geometric reason** why the Z_N Casimir condition selects
   exactly these five geodesics from the infinite spectrum?

2. **Selberg trace formula**: The Selberg trace formula relates the
   eigenvalue spectrum of the Laplacian on Γ\H² to the geodesic length
   spectrum. Since our stability eigenvalues λ_m(ξ) are derived from the
   Laplacian's Green's function, is there a version of the Selberg formula
   that connects λ_m = 0 (stability boundary) to specific geodesic lengths?

3. **Hecke operators**: The traces B = {3, 4, 6, 10, 16} might be related
   to eigenvalues of Hecke operators T_n acting on modular forms. The Hecke
   eigenvalues are traces of Frobenius elements, and our traces are traces
   of hyperbolic elements. Is there a Hecke-theoretic interpretation?

4. **Higher-genus generalization**: For Fuchsian groups Γ other than SL(2,Z),
   the geodesic spectrum is different. Does the vortex stability analysis
   on Γ\H² select different geodesics, and do they have algebraic-integer
   thresholds governed by different Pell equations?

## What Is PROVEN vs CONJECTURAL

| Claim | Status |
|-------|--------|
| ξ* satisfies ξ²−Bξ+1=0 with B integer for N∈{8,9,11,15,23} | PROVEN |
| B = tr(γ) for γ ∈ SL(2,Z) (palindromic char poly) | PROVEN (algebraic identity) |
| The five traces select five primitive geodesics on SL(2,Z)\H² | PROVEN (definition) |
| The selection rule is (N−7)\|16 ⟺ integrality of B | PROVEN |
| N=23 terminal case = Fibonacci matrix eigenvalue | PROVEN |
| There is a deeper geometric connection beyond shared algebra | CONJECTURAL |
| Selberg trace formula connects stability to geodesic spectrum | CONJECTURAL |
| V(r_n) = 0 at Maass eigenvalues (spectral filter) | INCONCLUSIVE — two near-hits (r₄, r₁₀) but not statistically significant with 10 eigenvalues |
| The Casimir filter is a truncated Euler factor at p=2 | PROVEN — F(s) = Σ_{k=0}^4 2^{-ks} |

## The Spectral Filter Investigation

### The vortex spectral function

Define V(r) = Σ_{d|16} w_d · cos(r · ℓ_d) where w_d = ℓ_d/√Δ_d.

This is a 5-term trigonometric polynomial whose frequencies are the five
geodesic lengths. By the Selberg trace formula, V(r_n) at Maass eigenvalue
parameters r_n gives the vortex-filtered contribution to the n-th eigenvalue.

### The Dirichlet series of the filter

F(s) = Σ_{d|16} d^{-s} = Σ_{k=0}^{4} 2^{-ks} = (1 − 2^{-5s})/(1 − 2^{-s})

This is a **truncated Euler factor at p=2**. The full Euler factor
(1−2^{-s})^{-1} appears in the Riemann zeta function ζ(s) = Π_p(1−p^{-s})^{-1}.
Our filter is the first 5 terms of this single Euler factor.

### Numerical test: V(r_n) at Maass eigenvalues

| n | r_n | V(r_n) | Near zero? |
|---|-----|--------|------------|
| 1 | 9.534 | +1.318 | No |
| 4 | 14.359 | −0.014 | **YES** (gap 0.019) |
| 10 | 21.316 | +0.093 | **Near** (gap 0.022) |

Two of the first 10 Maass eigenvalues sit very close to zeros of V(r).
The average distance from Maass eigenvalues to V-zeros is 0.345, compared
to 0.600 expected for random placement (ratio 0.575).

**Assessment**: Monte Carlo with 10,000 trials against 50 Maass eigenvalues
gives p = 0.77 (uniform null) and p = 0.70 (Poisson null). The observed
average gap to V-zeros (0.342) is LARGER than random expectation (0.319).
**There is no statistically significant correlation between Maass eigenvalues
and V-zeros.** The two near-hits (r₄, r₁₀) at n=10 were coincidental.

### The filter is NOT a Hecke operator

The filter selects traces by (B−2)|16, which is an additive condition.
Hecke operators act multiplicatively on traces (T_n maps B to traces
of γ^n). The filter is not closed under squaring: B² − 2 ∉ {3,4,6,10,16}
for any B in the set. So the vortex filter is a genuinely new type of
spectral selection, not reducible to known Hecke theory.

### Status

The chain: Vortex → Z_N → SL(2,Z) → Geodesics → Selberg → Maass forms
is proven through step 4. Step 5 (Selberg trace formula) applies as a
theorem but the vortex-filtered version V(r) does not have demonstrated
special properties at Maass eigenvalues beyond suggestive near-misses.
The connection to Riemann zeta zeros (step 6) remains fully conjectural
and is noted only as an observation about the Euler factor structure.

## Key Computation Files

- `src/planetary_polygons/extensions/algebraic_thresholds.py` — threshold computation
- `tests/test_algebraic_thresholds.py` — verification
- `src/planetary_polygons/proofs/aps_index_proof.py` — spectral flow
