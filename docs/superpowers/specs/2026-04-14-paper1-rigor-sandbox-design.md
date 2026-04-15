# Paper I Rigor Rewrites — Sandbox Workflow Design

**Date:** 2026-04-14
**Input:** `docs/PAPER1_RIGOR_REWRITE_SPEC.md` (6 structural rewrites + 7 minor cleanups)
**Problem:** In-place edits to `latex/paper/main.tex` have repeatedly introduced new errors while fixing old ones. Paper I has oscillated at 8.0 ± 0.6 across 8 review rounds.
**Goal:** A per-item surgical rewrite workflow that forbids any edit to `latex/paper/main.tex` until the replacement proof has passed numerical, reviewer, and human diff gates.

## Pilot Scope

This design is piloted on **Structural Rewrite #1** (Theorem `thm:constrained-min` — full Lagrangian eigenvalue derivation of `λ_m^± = (N-1) − m(N-m)/2`). Items #2–#6 and all minor cleanups are **out of scope** for this session and will follow the same workflow in later sessions.

## Non-Goals

- No edits to `latex/paper/main.tex` until the diff gate is cleared.
- No prose polishing or "while I'm here" cleanups in the §6.2 vicinity — surgical means only the flagged proof changes.
- No attempt to improve the paper's overall score by touching unrelated sections.
- No physics-reviewer pass on isolated proofs (pure-math scope; physics-reviewer is reserved for whole-paper rounds).

## Workflow (applied per structural item)

### Step 1 — Context read (required before drafting)

Before writing any derivation, read:

- Current `§6.2` of `latex/paper/main.tex` (the section being replaced)
- `src/planetary_polygons/core/` Havelock implementation (source of truth for λ values)
- Existing `tests/test_angular_hessian.py` if present, else whichever test asserts current Havelock values
- Last fresh-eyes review note flagging this theorem (pinpoint exactly what reviewers said was missing)

### Step 2 — Sandbox draft

Create the sandbox directory for this item:

```
docs/rigor-sandbox/
└── item1-constrained-min/
    ├── derivation.tex       # standalone LaTeX, compiles independently
    ├── numerical_check.py   # symbolic+numerical validation of every step
    ├── review-notes.md      # math-reviewer feedback + resolution log
    └── final-diff.patch     # exact surgical diff for main.tex (produced in Step 5)
```

`derivation.tex` follows the spec's 6-step plan:

1. Set up 2×2 block at mode m in (radial, tangential) basis with explicit Fourier amplitudes
2. Compute `d²H/dr_j dr_k` explicitly using `z_k = e^{iθ_k}`, perturbation `z_k → (1 + a cos(2πmk/N)) e^{iθ_k}`
3. Sum over pairs using Z_N Fourier orthogonality; reduce to the Havelock identity `T_m = m(N-m)/2`
4. Apply the Lagrange shift `−2μ_L = (N-1)/2`
5. Convert from amplitude to unit-eigenvector normalization
6. Derive — not assert — the trace identity `λ^+ + λ^- = N-1`

### Step 3 — Numerical gate

`numerical_check.py` must:

- Symbolically reproduce each algebraic step using `sympy` (or `mpmath` where necessary)
- Numerically verify the spec's three canonical test cases:
  - `(N=5, m=2)` → `(λ^+, λ^-) = (1, 3)`
  - `(N=7, m=3)` → `(λ^+, λ^-) = (0, 6)`
  - `(N=11, m=5)` → `(λ^+, λ^-) = (-5, 15)`
- Verify the trace identity falls out of the derivation (not imposed)
- Exit `0` on success; any mismatch means the derivation is wrong (not the tests)

**Gate:** Script exits `0`. No exceptions.

### Step 4 — math-reviewer gate

Dispatch the `math-reviewer` subagent on `derivation.tex` **alone** (not the whole paper). Prompt must explicitly forbid "what was fixed" context per the existing `feedback_fresh_eyes_reviews` memory rule.

**Gate (soft):** Score ≥ 9.0 AND zero structural deductions. Structural deductions include:

- "Key step omitted"
- "Unverified claim"
- "Hand-wave" / "by symmetry" without explicit symmetry
- "Standard result" without precise citation

Prose nitpicks and stylistic deductions do not block the gate. Iterate the sandbox until the structural-deduction count is zero, logging each round in `review-notes.md`.

### Step 5 — Diff proposal

Produce `final-diff.patch` containing the exact surgical change to `latex/paper/main.tex` §6.2. Present the diff to the user. User approves or requests changes.

**Gate:** User approval of the diff. No approval = no edit.

### Step 6 — Apply & verify

Apply the approved diff. Rebuild the paper (`pdflatex` in `latex/paper/`). Run `pytest tests/ -q`. Confirm no test regression and no LaTeX build regression.

**Gate:** Build succeeds, all previously-passing tests still pass.

## Rollback policy

If at any point after Step 6 a regression is discovered (test failure, reviewer flag on a different section caused by the edit, or reader-level confusion introduced in surrounding prose), `git revert` the commit immediately rather than patching forward. Debugging a regression counts as new evidence that the sandbox gate was insufficient — update the gate criteria before re-attempting.

## Deliverables for the pilot session (Item #1)

- `docs/rigor-sandbox/item1-constrained-min/derivation.tex` (compiles standalone, ~3 pages)
- `docs/rigor-sandbox/item1-constrained-min/numerical_check.py` (exits 0)
- `docs/rigor-sandbox/item1-constrained-min/review-notes.md` (math-reviewer rounds logged)
- `docs/rigor-sandbox/item1-constrained-min/final-diff.patch` (approved diff)
- Commit applying the diff to `latex/paper/main.tex`

## Success criteria

- `numerical_check.py` exits 0 with all three canonical cases matching
- `math-reviewer` on the sandbox: score ≥ 9.0, zero structural deductions
- Diff approved by user
- Paper builds cleanly and `pytest tests/ -q` shows no regression from baseline
- `tests/test_angular_hessian.py` exists and asserts paper formulas against numerical diagonalization (add if missing)

## Future items (out of scope this session, follow same workflow)

In the suggested order from the input spec: #6 (C₁(S²) appendix), #4 (computer-assisted cor:inertia-N7), #5 (prop:inertia clean formulation), #2 (Riemannian λ_m^- universality), #3 (uniform two-ring) — plus the 7 minor cleanups addressed opportunistically when their section is being touched by a structural rewrite.

## References

- Input spec: `docs/PAPER1_RIGOR_REWRITE_SPEC.md`
- Memory: `feedback_fresh_eyes_reviews.md` (review prompts must not include "what was fixed")
- Memory: `feedback_first_principles_proofs.md` (never silently downgrade theorems)
- Memory: `feedback_language_protocol.md` (present options, never autonomously edit paper language)
