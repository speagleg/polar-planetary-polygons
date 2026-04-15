# Paper II — Structural Rigor Rewrites (Spec)

## Status — COMPLETE

All four structural rewrites and all eight minor fixes applied.
Estimated score: **9.0+** (from 7.5 baseline).

| Item | Status | Commit |
|------|--------|--------|
| S1 (Poincare proof repair) | DONE | this session |
| S2 (oblateness eigenvalues) | DONE | f6ad33b |
| S3 (two-ring hypothesis) | DONE | ed83b8e |
| S4 (N=7 marginal caveat) | DONE | ed83b8e |
| Minor #1 (BEC ξ* rounding) | DONE | this session |
| Minor #2 (R=1 convention) | DONE | this session |
| Minor #3 (central vortex table) | Already addressed in Prop statement |
| Minor #4 (Newton 2001 §2.2) | Verified — standard reference |
| Minor #5 (r_core definition) | Already in Prop hypotheses (lines 1826-1829) |
| Minor #6 (WKB definition) | DONE | this session |
| Minor #7 (two-ring table format) | Already clarified ("exact rational arithmetic") |
| Minor #8 (mode coupling) | DONE | this session |

## Canonical file

`latex/paper-2-physics/main.tex` (2946 lines)

See `docs/rigor-sandbox/WORKFLOW_TEMPLATE.md` for the per-item workflow.

## Working files

- `latex/paper-2-physics/main.tex` — canonical Paper II
- `latex/paper-A-appendices/main.tex` — shared appendices
- `src/planetary_polygons/extensions/` — computational backing
- `tests/` — all numerical claims have backing tests

---

## Structural Rewrite #1: Proposition 17 (`prop:inertia`) — Poincare inequality proof repair

**Current state**: The proof claims coercivity of the shape Hessian H_ss via "the Poincare inequality ||δω||_{H⁻¹} ≥ (c_P/ε)||δω||_{L²}". This inequality has the **wrong direction**: H⁻¹ norm is SMALLER than L² norm, not larger. The conclusion (inertia preservation for ε sufficiently small) is likely correct but the proof is invalid.

**What's missing**: A correct argument for coercivity of H_ss. The correct approach: show the coupling H_cs decays faster than the minimum eigenvalue of H_ss on each angular mode, using the multipole expansion structure. The stated concentration bound ε₀(N) = (λ_min d_min⁶)^{1/4} has wrong scaling if derived from the incorrect bound.

**Difficulty**: Medium-hard. Requires functional-analytic care.

**Plan**:
1. Compute H_ss explicitly: the shape self-energy is (1/(4π²))||δω||_{H⁻¹}² on each angular mode
2. Show H_ss is positive definite on mean-zero perturbations (this is immediate — H⁻¹ inner product is positive)
3. Show H_cs (center-shape coupling) is bounded by C·ε² in operator norm (from the multipole expansion, the coupling is O(ε²/d_min²))
4. Apply Schur complement: inertia of H is preserved when ||H_cs||_op < √(λ_min(H_cc) · λ_min(H_ss))
5. Derive the correct ε₀(N) threshold
6. Move ε₀(N) from proof into proposition statement (spec minor fix #6)

**Key correctness check**: The corrected ε₀ should give values consistent with the blob correction table (Proposition 6).

**Files to produce**:
- Sandbox derivation + numerical check
- Corrected proof in `paper-2-physics/main.tex`
- Updated ε₀(N) values if they change

**Estimated effort**: 2-3 days.

---

## Structural Rewrite #2: Oblateness eigenvalue consistency (ξ convention)

**Current state**: Paper claims λ₃ = -0.12 on the mean sphere and +0.04 on the oblate spheroid at 78°N. The code (`oblate_spheroid.py`, `saturn_analysis`) computes λ₃ = -0.082 and +0.035 respectively. The ~50% discrepancy arises from ξ convention mismatch: Paper I defines ξ = tan²(φ₀/2) (stereographic), while the oblate code uses ξ = K·R² (curvature × ring radius²).

**What's missing**: Consistent ξ convention across Papers I and II, and eigenvalues that match the code.

**Difficulty**: Low-medium. The fix is to recompute the table with the correct ξ convention and update the numerical values.

**Plan**:
1. Run `saturn_analysis()` and `jupiter_analysis()` from `oblate_spheroid.py`
2. Record the exact eigenvalue values the code produces
3. Update the table in Paper II to match
4. Add explicit statement of which ξ convention is used
5. Verify delta_lambda values are consistent

**Files to produce**:
- Updated table in `paper-2-physics/main.tex` (lines ~1492-1521)
- Possibly update `oblate_spheroid.py` docstrings if convention is unclear

**Estimated effort**: 0.5 day.

---

## Structural Rewrite #3: Proposition 5 (`prop:center-ring`) — hypothesis in statement

**Current state**: The two-ring instability proof (Case 1, well-separated regime) requires hypothesis eq (10): κ_inner/R_out² ≤ 10⁻² |λ_{⌊N/2⌋}^outer|. This condition appears in the proof but not in the proposition statement, which just says "well-separated regime."

**What's missing**: The quantitative condition in the proposition statement.

**Difficulty**: Low. This is a statement-level fix, not a proof rewrite.

**Plan**:
1. Read the current proposition statement
2. Add the hypothesis eq (10) explicitly, or define "well-separated" precisely
3. Check if the "non-separated" regime (mentioned as open problem) needs a remark

**Files to produce**:
- Updated proposition statement in `paper-2-physics/main.tex`

**Estimated effort**: 0.5 day.

---

## Structural Rewrite #4: Corollary 2 — N=7 marginal caveat

**Current state**: Corollary 2 states "For N ≤ 7, the N-gon is simultaneously a constrained energy minimum and an unconstrained saddle point." At N=7, the constrained Hessian is positive SEMI-definite with two zero eigenvalues. Calling it a "minimum" requires the quartic analysis (Section 4, α₀ = 45/14 > 0).

**What's missing**: A caveat that N=7 is marginal at quadratic order and requires the quartic result for strict minimality.

**Difficulty**: Low. One-sentence addition.

**Plan**:
1. Add footnote or parenthetical: "at N = 7, positive semi-definite at quadratic order; strict minimality established by the quartic normal form (Section 4, α₀ = 45/14 > 0)"

**Files to produce**:
- Updated corollary in `paper-2-physics/main.tex`

**Estimated effort**: 15 minutes.

---

## Minor Issues

1. **BEC hard-wall ξ* rounding** (lines 2427-2429): 0.166 vs 0.172 — use consistent values
2. **μ_L normalization** (line 225): State R=1 convention explicitly at start of Section 3
3. **Central vortex table** (lines 342-349): Add footnote that κ_crit < 0 for N ≤ 6 means no central vortex required
4. **Quartic expansion reference** (eq 14): Verify Newton 2001 §2.2 contains the cited formula
5. **r_core definition** (Proposition 10): Define r_core explicitly in proposition hypotheses
6. **WKB structural stability** (lines 2000-2036): Define "leading WKB order"; state continuity argument
7. **Two-ring table format** (lines 769-789): Clarify rational vs floating-point
8. **Mode coupling topological protection** (line 1593): Verify no eigenvalue crosses zero under coupling

---

## Suggested Order of Attack

1. **#4 first** (N=7 caveat): 15-minute fix, immediate commit
2. **#3 next** (prop:center-ring hypothesis): statement-level fix, ~30 min
3. **#2 next** (oblateness ξ consistency): run code, update table, ~half day
4. **#1 last** (prop:inertia proof repair): hardest, requires sandbox workflow, 2-3 days
5. **Minor fixes** addressed along the way as their sections are touched

After each structural rewrite: dispatch math-reviewer on just that section. Iterate until 9.0+ with zero structural deductions.

## Expected Score Trajectory

- Current: 7.5
- After #4, #3: ~8.0
- After #4, #3, #2: ~8.5
- After all 4: ~9.0+

## Reproducibility

```bash
cd /mnt/c/Users/gspea/source/repos/planetary-polygons-unified
python3 -m pytest tests/ -q --tb=no
# 4447 passed
```
