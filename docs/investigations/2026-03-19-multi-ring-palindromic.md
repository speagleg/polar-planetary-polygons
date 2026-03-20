# Multi-Ring Palindromic Conjecture

**Date:** 2026-03-19
**Status:** CONJECTURE (k=1 proven, k=2 structure identified)

## The Deep Reason for Palindromic Structure

C₁(ξ) = (N-1)(1+ξ²)/(1-ξ)² satisfies **C₁(1/ξ) = C₁(ξ)**.

This invariance under conformal inversion ξ ↔ 1/ξ is the geometric
reason the threshold equation C₁(ξ) = c has roots ξ₁ξ₂ = 1, making
the threshold polynomial palindromic.

## Single Ring (k=1) — PROVEN

- Parameter: ξ ∈ (0,1)
- Inversion: ξ → 1/ξ
- Threshold: palindromic QUADRATIC ξ² - Bξ + 1 = 0
- Roots: units in quadratic fields Q(√D)
- Algebraic-integer cases: N ∈ {8, 9, 11, 15, 23}

## Two Rings (k=2) — STRUCTURE IDENTIFIED

- Parameters: (ξ, ρ) where ξ is curvature and ρ = R₂/R₁ is radius ratio
- Joint inversion: (ξ, ρ) → (1/ξ, 1/ρ) [isometry of H²]
- C₁(1/ξ) = C₁(ξ) and K₁₂(1/ξ, 1/ρ) = K₁₂(ξ, ρ)
- The stability determinant is invariant under the joint inversion
- Threshold at fixed ρ: NOT palindromic (ρ breaks individual inversion)
- Threshold on joint-invariant slices: palindromic
- The joint threshold (eliminating ρ) involves a QUARTIC polynomial

## Multi-Ring Conjecture

For k concentric rings on H², the conformal inversion acts on
all k parameters simultaneously. The threshold polynomial (after
eliminating the radius ratios) is palindromic of degree 2k:

| k | Polynomial degree | Number field | Unit equation |
|---|-------------------|--------------|---------------|
| 1 | 2 (quadratic) | Q(√D) | Pell equation |
| 2 | 4 (quartic) | Totally real quartic | Quartic unit eq. |
| 3 | 6 (sextic) | Totally real sextic | Sextic unit eq. |

If confirmed, this would connect multi-ring vortex stability to the
arithmetic of totally real number fields of arbitrary degree, with
the Pell equation as the k=1 case.

## Dihedral vs Cyclic Symmetry

For the regular N-gon, D_N symmetry adds nothing beyond Z_N:
the palindromic pairing λ_m = λ_{N-m} already groups modes into
D_N irreps. The Z_N Casimir m(N-m)/2 is the D_N Casimir restricted
to the cyclic subgroup.

D_N symmetry becomes genuinely new for:
- Two-ring configurations (D_N symmetry with inter-ring coupling)
- Staggered polygons (alternating radii, D_{N/2} symmetry)
- Any configuration where the FULL dihedral group, not just rotations,
  constrains the stability matrix

## Computation Results (2026-03-19)

### Strong conjecture: FAILS

The two-ring threshold at fixed radius ratio ρ = const is **NOT palindromic**
in ξ. The roots do not satisfy ξ₁ξ₂ = 1. The multi-ring thresholds at
fixed ρ do NOT produce Pell units.

### Corrected statement: PROVEN (structural argument)

In logarithmic variables u = ln(ξ), v = ln(ρ), the joint inversion acts as
(u,v) → (−u,−v). The threshold surface F(u,v) = 0 satisfies F(u,v) = F(−u,−v).

On any **power-law curve** ρ = ξ^α (i.e., v = αu), the restriction
g(u) = F(u, αu) is an EVEN function: g(u) = g(−u). In the ξ variable,
this means g(ln ξ) = g(ln(1/ξ)) — the equation IS palindromic along
power-law paths.

**Corrected theorem**: Multi-ring thresholds on H² are palindromic
along power-law scaling paths ρ = ξ^α, but NOT along constant-ρ paths.
The single-ring case (k=1) is always palindromic because there is only
one parameter (ξ), and every 1D path through the origin is a power law.

### Physical interpretation

- **Single ring**: the curvature parameter ξ is the ONLY variable.
  The threshold is always palindromic → Pell units.
- **Two rings**: the radius ratio ρ is an ADDITIONAL parameter.
  If both rings scale together with curvature (ρ = ξ^α for some α),
  the palindromic structure survives. If the ratio is fixed while
  curvature changes, the palindromic structure breaks.
- **Physical vortex systems**: on a planet, the radius ratio ρ is
  determined by the dynamics (equilibrium condition), not by the
  curvature. The ratio generically does NOT scale as a power law
  in ξ. So the palindromic/Pell structure is specific to single-ring
  configurations.

### What this means for the paper

The Pell equation structure is a **single-ring phenomenon**. It does
not generalize to multi-ring systems in the way conjectured. The
palindromic property of the threshold comes from the conformal inversion
symmetry C₁(1/ξ) = C₁(ξ), which is a single-variable identity. When
additional parameters enter (inter-ring coupling), the palindromic
structure breaks along generic paths.

This STRENGTHENS the paper's single-ring result: the Pell equation
structure is not a generic feature of stability on H² but a specific
consequence of the Z_N-symmetric single-ring geometry. The single-ring
case is algebraically special.
