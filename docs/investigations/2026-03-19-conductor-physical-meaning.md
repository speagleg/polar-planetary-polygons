# The Conductor as a Physical Observable

**Date:** 2026-03-19
**Status:** PROVEN (the identities), INTERPRETIVE (the physical meaning)

## The Conductor f

For each algebraic-integer threshold ξ* with discriminant Δ = B²−4:
  Δ = f²·D where D = sq-free(Δ), f = conductor

| N | f | D | Δ | csch²(ℓ/2) = 4/Δ | Physical role |
|---|---|---|---|---|---|
| 23 | 1 | 5 | 5 | 0.80 | Most sensitive to topology |
| 15 | 2 | 3 | 12 | 0.33 | |
| 11 | 4 | 2 | 32 | 0.125 | |
| 9 | 4 | 6 | 96 | 0.042 | |
| 8 | 6 | 7 | 252 | 0.016 | Most insensitive to topology |

## Two Physical Meanings

### 1. Topological Sensitivity

On a quotient surface Γ\H², each geodesic γ contributes an
automorphic correction δC₁ ∝ 4/Δ = 4/(f²D) to the stability
eigenvalue.

- **f = 1 (N=23)**: correction = 4/5 = 0.80 → STRONG coupling
  to surface topology. The golden ratio threshold shifts
  significantly when the surface is compactified.

- **f = 6 (N=8)**: correction = 4/252 = 0.016 → WEAK coupling.
  The N=8 threshold barely changes from H² to any quotient.
  It is effectively "universal" (insensitive to global topology).

**The conductor measures how strongly the vortex threshold couples
to the global topology of the underlying surface.**

### 2. Experimental Precision Required

The sensitivity dλ/dξ at the threshold determines how precisely
the curvature parameter must be controlled to resolve the transition:

| N | f | δξ for δλ=0.1 | Relative precision |
|---|---|--------------|-------------------|
| 23 | 1 | 0.0004 | 0.1% |
| 15 | 2 | 0.0011 | 0.4% |
| 11 | 4 | 0.0024 | 1.4% |
| 9 | 4 | 0.0041 | 4.1% |
| 8 | 6 | 0.0055 | 8.8% |

**Paradox**: The f=1 (golden ratio) threshold is the most SENSITIVE
to topology but requires the most PRECISION to resolve experimentally.
The f=6 (N=8) threshold is INSENSITIVE to topology but is the easiest
to measure (8.8% precision suffices).

This is because f controls BOTH the topological coupling (4/Δ) and
the threshold's position (ξ* is further from 0 for small f, making
dλ/dξ larger at the threshold).

## What the Conductor Does NOT Control

- **Bifurcation codimension**: always 1 (one mode crossing zero),
  independent of f. The palindromic symmetry λ_m = λ_{N-m} gives
  codimension 2 (paired modes), but this is universal.

- **Number of near-zero modes**: this depends on N directly,
  not on f. The conductor and N are correlated but not equivalent.

## The Conductor as an Invariant

The conductor f is determined by the Z_N Casimir through the
discriminant Δ = B²−4, which factors as f²·D. It depends on N
but not on the surface or the curvature parameter. It is an
INTRINSIC property of the N→(N+1) transition, not of the
particular surface on which the vortices live.

On any arithmetic surface with a geodesic of trace B, the
correction strength is 4/(f²D). Different surfaces have different
geodesic spectra, but the WEIGHT of each geodesic's contribution
is fixed by f and D — these are properties of the THRESHOLD,
not of the SURFACE.
