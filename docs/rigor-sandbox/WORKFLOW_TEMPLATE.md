# Rigor Rewrite Workflow Template

Proven through Paper I (Items #1, #2, #6 + minor fixes). Apply to every structural rewrite across the entire series.

## Canonical Paper Files

**Always edit the canonical file. Never edit standalone copies.**

| Paper | Canonical file |
|-------|---------------|
| Paper I — Mathematics | `latex/paper-1-mathematics/main.tex` |
| Paper II — Physics | `latex/paper-2-physics/main.tex` |
| Paper III — Gravity | `latex/paper-3-gravity/main.tex` |
| Paper IV — Field Theory | `latex/paper-4-field-theory/main.tex` |
| Paper V — Cosmology | `latex/paper-5-cosmology/main.tex` |
| Paper V — S³ Framework | `latex/paper-5-s3-framework/main.tex` |
| Paper VI — Discussion | `latex/paper-6-discussion/main.tex` |
| Overview | `latex/paper-0-overview/main.tex` |
| Appendices | `latex/paper-A-appendices/main.tex` |
| Supplement (Proofs) | `latex/supplement-proofs/main.tex` |
| Companion | `latex/companion/main.tex` |
| Readers Guide | `latex/readers-guide/main.tex` |
| Shared preamble | `latex/shared/preamble.tex` |
| Shared bibliography | `latex/shared/refs.bib` |

**NOT canonical (do not edit):**
- `latex/paper/main.tex` — standalone copy of Paper I. Historical artifact. All work goes in `paper-1-mathematics/` instead.

## Per-Item Workflow

### Phase 1: Sandbox Setup
1. Create `docs/rigor-sandbox/itemN-<name>/`
2. Scaffold: `numerical_check.py`, `derivation.tex`, `review-notes.md`
3. Commit

### Phase 2: Numerical Oracle
1. Build a trusted oracle that computes the claimed result from first principles (finite-difference Hessian, direct diagonalization, etc.)
2. Verify the paper's formula against the oracle
3. **If discrepancy found:** investigate before proceeding (Item #6 lesson — the formula may be wrong)
4. Commit

### Phase 3: Algebraic Derivation
1. Derive each intermediate step, verify against oracle at each step (sympy 30-digit or mpmath)
2. Write derivation.tex (standalone, compiles independently)
3. No placeholders — every algebraic claim must have a numerical check
4. Commit after each major section

### Phase 4: Consolidate + Review Gate
1. Add main theorem statement at top of derivation.tex
2. Add verification section at end
3. Scan for placeholders (grep TODO/TBD)
4. Two-pass pdflatex, zero warnings
5. Dispatch math-reviewer (subagent): score ≥ 9.0 AND zero structural deductions
6. Iterate until gate passes
7. Commit each round

### Phase 4b: Downstream Impact Assessment
**Before integrating any proof change, assess what breaks downstream.**
1. List every proposition, corollary, remark, and equation in the SAME paper that cites or depends on the changed result
2. For each: does the fix change the statement, the hypotheses, or only the proof internals?
3. If statement or hypotheses change: trace further downstream (what cites THAT result?)
4. If a numerical value changes (threshold, eigenvalue, constant): grep the entire `latex/` tree for the old value
5. If the proof technique changes (e.g., new scaling law): check whether any later proof reuses the old technique or bound
6. Document the impact chain in the sandbox review-notes.md BEFORE writing replacement text
7. Present the impact chain to user alongside the diff

### Phase 5: Integration
1. Identify ALL downstream references across ALL canonical files (use Explore agent, very thorough)
2. Build replacement text for the canonical paper where the result lives
3. Present diff to user for approval (include downstream impact assessment from Phase 4b)
4. Apply to canonical paper + every other series paper that references the result
5. Propagate any changed statements/values to all downstream results identified in Phase 4b
6. Update CLAUDE.md if formula is referenced there
7. Run full test suite (4447+ pass, zero regression)
8. Final sweep: grep all canonical files for old formula/values, confirm zero remaining
9. Commit

## Key Principles (learned from Paper I)

- **Oracle first:** Build numerical verification BEFORE attempting algebra. The oracle catches errors in real time.
- **No frame assumptions:** Verify which coordinate frame the formula applies in (Item #6: stereographic vs geodesic vs canonical).
- **Check the cited result:** Don't assume cited formulas are correct. Verify against oracle. (Item #6: BC2003 citation was wrong.)
- **Compare existing proofs:** Before writing a new proof, check if the canonical paper already has one (Item #2: paper-1-mathematics already had the full proof that paper/main.tex lacked).
- **Downstream impact first:** Before integrating a fix, trace what depends on the changed result within the same paper AND across the series. A proof-only fix (internals change, statement unchanged) has no downstream impact. A statement/hypothesis/value change propagates — map the chain before editing.
- **Series-wide sweep:** After fixing one paper, sweep ALL canonical files for the same formula/values. Use Explore agent with "very thorough" setting. A fix is not done until grep returns zero matches for old values across the entire `latex/` directory.
- **No meta-commentary:** State what IS, not what was wrong in earlier versions.
- **American English:** All paper text.
- **Language protocol:** Present language options to Gordon, never edit prose autonomously.

## Gate Criteria

- **Numerical:** `numerical_check.py` exits 0
- **math-reviewer:** ≥ 9.0, zero structural deductions
- **User approval:** Diff shown and approved before any paper edit
- **Test suite:** Full suite passes after integration
- **Sweep:** Zero remaining references to old formula/values in any canonical file
