# Rigor Rewrite Workflow Template

Proven through Items #1 and #6. Apply to each structural rewrite across the series.

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

### Phase 5: Integration
1. Identify ALL downstream references (use Explore agent, very thorough)
2. Build replacement text for the canonical paper (`paper-1-mathematics/` for Paper I)
3. Present diff to user for approval
4. Apply to canonical paper + ALL series papers that reference the result
5. Update CLAUDE.md if formula is referenced there
6. Run full test suite (4447+ pass, zero regression)
7. Commit

## Key Principles (learned from Items #1 and #6)

- **Oracle first:** Build numerical verification BEFORE attempting algebra. The oracle catches errors in real time.
- **No frame assumptions:** Verify which coordinate frame the formula applies in (Item #6: stereographic vs geodesic vs canonical).
- **Check the cited result:** Don't assume cited formulas are correct. Verify against oracle. (Item #6: BC2003 citation was wrong.)
- **Series-wide sweep:** After fixing one paper, sweep ALL series papers for the same formula/values. Use Explore agent with "very thorough" setting.
- **No meta-commentary:** State what IS, not what was wrong in earlier versions (Gordon's feedback).
- **Canonical file:** `paper-1-mathematics/main.tex` is Paper I. `paper/main.tex` is a standalone copy — keep in sync but work on the series version.
- **American English:** All paper text (feedback_american_english memory).
- **Language protocol:** Present language options to Gordon, never edit prose autonomously (feedback_language_protocol memory).

## Gate Criteria

- **Numerical:** `numerical_check.py` exits 0
- **math-reviewer:** ≥ 9.0, zero structural deductions
- **User approval:** Diff shown and approved before any paper edit
- **Test suite:** Full suite passes after integration
- **Sweep:** Zero remaining references to old formula/values in any file
