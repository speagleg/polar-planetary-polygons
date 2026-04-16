# Session 2: C3 — D²_CS = Δ operator identity domain

**Date opened**: 2026-04-16
**Plan reference**: `docs/PAPER4_RIGOROUS_DERIVATION_PLAN.md`, Session 3 item (C3 — Session 2 in execution order since M1 was done in Session 1 joint scope).
**Workflow**: `docs/rigor-sandbox/WORKFLOW_TEMPLATE.md`

## The claim (Paper IV §11 lines 2085–2135)

The polygon theory's Weinberg-angle derivation uses the operator identity:
```
D²_CS = Δ_H² = Ω_{sl(2,R)}
```
- D²_CS: covariant Laplacian built from the Chern-Simons connection A = ω + e/ℓ
- Δ_H²: Laplace-Beltrami operator on H²
- Ω_{sl(2,R)}: Casimir of sl(2,R) via the identification H² = SL(2,R)/SO(2) (Helgason)

**Key numerical consequence**: at the critical mode m* = 2 on N = 4, the eigenvalue
`D² φ_m* = f(m*, N) φ_m* = 2 φ_m*`, matching `C_2(j = 1) = j(j+1)|_{j=1} = 2`.

## Problem (rigor plan C3)

> "Claimed universal, but only holds on Z/N-equivariant scalars. For matter in non-trivial representations, there are curvature/commutator terms."

Required:
1. **State the identity precisely with domain restriction**
2. **Work out [F, φ] for matter in representation R** (R-dependent corrections)
3. **Justify the f(m*, N) = C_2(j=1) = 2 coincidence from operator theory**
4. **Show whether this is a general pattern or specific to j=1**

## Why this matters

The sin²θ_W = 3/11 derivation relies on this identity holding on the relevant matter (the critical KK mode). If the identity needs corrections for non-trivial representations, the Weinberg angle derivation may shift.

Paper currently invokes the identity on Z/N-equivariant scalars. We need to:
- Rigorously state the SCALAR-Laplacian case (paper's argument)
- Generalize to other representations (curvature + [F, φ] terms)
- Show whether the critical mode m*, with f(m*, N) = j(j+1), has special structure

## Approach

### Phase 1: Scalar identity on Z/N-equivariant H² (paper's argument)
- State the Helgason theorem precisely
- Verify D²_CS = Δ_H² on Z/N-equivariant SCALAR functions
- Derive eigenvalue formula

### Phase 2: Generalization to non-trivial representations
- Lichnerowicz-style formula: D² = Δ − R · (spin factor) + [F, ·]
- For spinors (Dirac): D² = Δ + R/4 + (1/2) γ^μ γ^ν F_μν
- For tensor rep R: D² = Δ + curvature_R(F) + commutator terms

### Phase 3: The f(m*,N) = C_2(j=1) coincidence
- f(m, N) = m(N-m)/2 = j(j+1) requires m(N-m) = 2j(j+1) for integer j
- For (m, N) = (2, 4): j(j+1) = 2 → j = 1 ✓
- For (m, N) = (3, 7): j(j+1) = 6 → j = 2 ✓
- Show: this coincidence appears at PARTICULAR (m, N) pairs (specifically palindromic critical modes with integer j)

### Phase 4: Verification and write-up
- Numerical / symbolic verification
- Clean theorem statement with domain
- Integration-ready derivation

## Layout

```
session02-C3-operator-identity/
├── README.md                       # this file
├── derivation.md                   # formal derivation
├── oracle.py                       # symbolic verification of D² = Δ on scalars
├── representation_corrections.py   # [F, φ] for non-trivial reps
├── coincidence_analysis.py         # when does f(m, N) = j(j+1)?
└── review-notes.md                 # reviewer feedback (post-dispatch)
```

## Current status

- Plan drafted, sandbox initialized.
- Next step: Phase 1 (scalar identity derivation + oracle).
