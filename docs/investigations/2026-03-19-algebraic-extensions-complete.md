# Algebraic Field Extensions: Complete Results

**Date**: 2026-03-19
**Status**: ALL PROVEN

## Theorem 1: Field Extension Pattern (proven in paper §6)

The discriminant of the palindromic threshold polynomial Aξ²+Bξ+A=0 factors as:
- Even N (m=N/2): Δ = (N-1)(N-2)², so ξ* ∈ Q(√sqfree(N-1))
- Odd N (m=(N-1)/2): Δ = (N-1)²(N-3), so ξ* ∈ Q(√sqfree(N-3))

**Proof**: Direct factorization of Δ = B² - 4A². In paper as formal proof environment.

## Theorem 2: Algebraic Integer Classification (proven)

ξ*(N) is an algebraic integer iff N ∈ {8, 9, 11, 15, 23}.

**Proof**: B/A ∈ Z iff (N-7)|16 for odd N ≥ 9 (since B/A = -2(N+1)/(N-7)
and 2(N+1) = 2(N-7)+16). For even N ≥ 8: only N=8 satisfies 8-(N-4)²|2N².
The differences {1, 2, 4, 8} are powers of 2.

## Theorem 3: Unit Power Identification (proven)

Each algebraic-integer threshold equals an explicit power of the inverse
fundamental unit:

| N  | D | Fundamental unit ε      | ξ*(N)  | Norm(ε) | k |
|----|---|------------------------|--------|---------|---|
| 8  | 7 | 8+3√7                 | ε⁻¹    | +1      | 1 |
| 9  | 6 | 5+2√6                 | ε⁻¹    | +1      | 1 |
| 11 | 2 | 1+√2 (silver ratio)   | ε⁻²    | -1      | 2 |
| 15 | 3 | 2+√3                  | ε⁻¹    | +1      | 1 |
| 23 | 5 | φ=(1+√5)/2 (golden)   | φ⁻²    | -1      | 2 |

**Proof**: Symbolic verification via sympy (ξ* - ε⁻ᵏ = 0 algebraically
for each case). The fundamental units are classical results (Hardy & Wright).

**Why k=2 for N=11, 23**: The fundamental unit has norm -1 (negative Pell
equation x²-Dy²=-1). Only even powers ε²ᵏ have norm +1, which is required
by the palindromic structure (ξ·ξ'=1). For D=2: (1+√2)²-2·1²=-1.
For D=5: φ·φ'=-1.

## Theorem 4: Continued Fraction Structure (proven)

If ξ satisfies ξ²-cξ+1=0 with integer c ≥ 3 and ξ ∈ (0,1), then:

    1/ξ = [c-1; 1, c-2, 1, c-2, ...] = [c-1; ‾1, c-2‾]

For c=3: period degenerates to [1] (golden ratio CF).

**Proof**: Four-step argument with explicit floor-function bounds:
1. a₀ = c-1 (from c-1 ≤ (c+√(c²-4))/2 < c, verified by (c-2)² ≤ c²-4 ⟺ c≥2)
2. a₁ = 1 (from 1 ≤ 1/r₀ < 2, verified by 4(2c-5)(c-2) > 0 for c≥3)
3. a₂ = c-2 (from 1/r₁ = 1/ξ - 1, so ⌊1/r₁⌋ = ⌊1/ξ⌋ - 1 = c-2)
4. r₂ = r₀ (periodicity: r₂ = 1/ξ - (c-1) = r₀)

Verified computationally for c ∈ {3, 4, 6, 10, 16} (all 5 algebraic-integer cases).

Applied to the 5 cases:
- N=8:  1/ξ* = [15; ‾1, 14‾]
- N=9:  1/ξ* = [9; ‾1, 8‾]
- N=11: 1/ξ* = [5; ‾1, 4‾]
- N=15: 1/ξ* = [3; ‾1, 2‾]
- N=23: 1/ξ* = [2; ‾1‾] = [2; 1, 1, 1, ...] (golden ratio CF)

## Theorem 5: Palindromic ↔ Pell ↔ Conformal Inversion (proven)

Three equivalent characterizations of the threshold structure:
1. **Geometric**: ξ ↔ 1/ξ conformal inversion symmetry of the Poincaré disk
2. **Algebraic**: ξ·ξ' = 1 (unit norm in the real quadratic field Q(√D))
3. **Number-theoretic**: a²-Db²=1 (Pell equation) when ξ is an algebraic integer

**Proof**: (1)↔(2): The palindromic polynomial Aξ²+Bξ+A=0 has roots multiplying
to A/A=1, which is the algebraic norm condition. (2)↔(3): For ξ=a+b√D ∈ Z[√D],
the norm ξ·ξ'=(a+b√D)(a-b√D)=a²-Db²=1 is exactly the Pell equation.
(1)↔(3): The conformal inversion z↦a²/z̄ of the Poincaré disk restricts to
ξ↦1/ξ on the real axis, which is the Galois conjugation in Q(√D).

## The Golden Ratio as Terminal Case

N=23 occupies a distinguished position:
- It is the LAST algebraic-integer threshold (the finite set {8,9,11,15,23} terminates)
- Its threshold ξ*(23) = φ⁻² = (3-√5)/2 involves the golden ratio
- Its CF has the simplest possible period [1] (all ones)
- Its monic polynomial ξ²-3ξ+1=0 has the smallest integer trace (c=3) that gives
  a palindromic with two positive roots
- The golden ratio φ is the "hardest to approximate" irrational (worst-case CF),
  making φ⁻² the algebraically simplest non-trivial unit

## Physical Significance

The algebraic structure connects:
- **Vortex dynamics** (Havelock eigenvalues on the hyperbolic plane)
- **Conformal geometry** (Möbius inversion of the Poincaré disk)
- **Algebraic number theory** (units of real quadratic fields, Pell equations)
- **Continued fractions** (periodic expansions encoding the unit group)

The N=8 threshold (physically relevant for Jupiter) involves √7 because
the discriminant contains the factor (N-1)=7, which is the residue of the
flat-plane marginality at N=7. The appearance of 7 in the number field
Q(√7) is not a coincidence — it is the algebraic shadow of the N=7
stability boundary.

## Direction 2: Class Numbers (explored, elementary result)

All 5 algebraic-integer threshold fields have class number h(D)=1 (UFD).
This is NOT a deep coincidence: (N-7)|16 forces D ∈ {2,3,5,6,7}, and
all squarefree D ≤ 7 have h=1 by classical results. Worth a brief
remark in the paper but not a theorem.

Non-UFD fields (h>1) first appear at N=13 (D=10, h=2). These always
correspond to non-algebraic-integer thresholds. No D with h≥3 appears
for N ≤ 50.

## Direction 4: Modular Forms (explored, negative result + new structure)

**No modular form connection.** The D(N) sequence is the squarefree kernel
function applied to arithmetic progressions (N-1 or N-3), not a modular
form. The connection to number theory is through Pell equations and
continued fractions, not modular or automorphic forms.

**However: Binary Subdivision Theorem (proven, new).**

The odd algebraic-integer thresholds occur at N = 7 + 2^k for k=1,2,3,4.
Their monic polynomial traces satisfy:

    c(k) = 2 + 2^(4-k)

This is a binary subdivision: each doubling of (N-7) halves the algebraic
"excess" c-2, reaching the minimum c=3 (golden ratio) at k=4 (N=23).
The sequence terminates because c=2 gives the degenerate (ξ-1)²=0.

| k | N=7+2^k | c = 2+2^(4-k) | ξ* polynomial | Field |
|---|---------|---------------|---------------|-------|
| 1 | 9       | 10            | ξ²-10ξ+1=0   | Q(√6) |
| 2 | 11      | 6             | ξ²-6ξ+1=0    | Q(√2) |
| 3 | 15      | 4             | ξ²-4ξ+1=0    | Q(√3) |
| 4 | 23      | 3             | ξ²-3ξ+1=0    | Q(√5) |

Physical interpretation: each doubling of the polygon count (above
the N=7 baseline) halves the algebraic complexity of the hyperbolic
stability threshold, converging to the golden ratio as the simplest
possible algebraic unit.

## Direction 5: Higher-Dimensional Analogues (explored, structural result)

**THEOREM (dimension uniqueness, proven):** The 2D Laplacian is the
UNIQUE dimension where the sign rule holds for the Green's function.

For all d ≥ 2: h' < 0 (condition i satisfied — interaction is attractive).
But (rh')' = 0 ONLY for d=2 (the logarithm). For d ≥ 3: (rh')' > 0
(class iii — condition ii violated). The polygon stability mechanism
is intrinsically two-dimensional.

d=2 is the borderline case: the logarithm satisfies (rh')' = 0 exactly,
making it the "least robust" polygon producer (any perturbation toward
class iii breaks the sign rule). This is already noted in the paper.

**What generalizes:**
- Conformal inversion symmetry (exists in all dimensions via Kelvin transform)
- Stability thresholds depending on curvature
- Block decomposition of the Hessian by symmetry group

**What does NOT generalize:**
- The logarithmic interaction (unique to d=2)
- The sign rule for polygon stability (requires (rh')' ≤ 0)
- The palindromic polynomial (requires 1D radial parameter)
- The Pell equation / continued fraction / unit structure
  (specific to real quadratic fields from palindromic quadratics)

**Open directions:**
- Hyperbolic tilings {p,q}: the {7,3} tiling has p=7 matching the
  flat-plane stability boundary. Conjecture: the discrete Havelock
  eigenvalue on {p,q} relates to the continuous H² threshold.
- Non-abelian symmetry: vortices at Platonic solid vertices have
  non-abelian symmetry groups (A₄, S₄, A₅). The Hessian decomposes
  into multi-dimensional irreps, giving a richer eigenvalue structure.
- Codimension-1 objects (vortex rings in R³) have a single radial
  parameter and COULD exhibit palindromic structure. Open question.

The algebraic structure discovered in this paper is intrinsically 2D —
and planetary atmospheres provide exactly this 2D constraint.

## Extension A: Torus Stability (explored, negative feasibility)

**Result: The flat torus T² does not directly support the ring stability
problem.** The analogue of the N-gon ring on the torus is a vortex ROW
(N equally-spaced vortices along one period). This row decomposes into:
- In-row (longitudinal) modes: ALWAYS stable for all N and all τ
- Out-of-row (transverse) modes: ALWAYS unstable (von Kármán instability)

There is no stability THRESHOLD analogous to N=7 on the torus, because:
1. The torus has no angular impulse (no origin → no L = Σ|z_k|²)
2. The Lagrange multiplier correction that creates the Havelock eigenvalues
   does not exist on the torus
3. The vortex row is always transversely unstable, regardless of N

The j-invariant conjecture (ξ_crit ∈ Q(j(τ))) is therefore NOT applicable
in this setting. The modular form connection, if it exists, would need a
different geometric setup — perhaps vortices on a CURVED torus (constant
negative curvature surface of genus g ≥ 2, whose moduli space IS connected
to modular forms via the Selberg zeta function).

**Open direction**: The Bolza surface (genus 2, {8,3} tiling) is the
simplest compact hyperbolic surface. Point vortices on the Bolza surface
would combine the H² algebraic structure with genus-dependent modular
corrections. This is a research program, not a quick computation.
