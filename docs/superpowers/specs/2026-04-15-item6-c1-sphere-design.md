# Item #6 (REVISED) — C₁(S²) Bugfix + Pell Unification

**Date:** 2026-04-15 (revised from initial design)
**Input:** `docs/PAPER1_RIGOR_REWRITE_SPEC.md`, Structural Rewrite #6
**Discovery:** The formula C₁(S²) = (N-1)(1-ξ)/(1+ξ) cited from BC2003 is **wrong**. The correct formula is C₁(S²) = (N-1)(1+ξ²)/(1+ξ)² — which the appendix already derives as "C₁^eucl" but then incorrectly dismisses as a "limitation of the stereographic derivation."

## Evidence

1. **Stereographic oracle** confirms C₁^eucl to 10⁻⁷ for N ∈ {4,5,6,7}, ξ ∈ {0.15, 0.3, 0.5, 0.7} using the full S² Hamiltonian H_sph with angular momentum constraint J
2. **Tangential eigenvalue** universally equals m(N-m)/(2ξ), confirming Riemannian Havelock identity
3. **LMR05** (Laurent-Polz, Montaldi, Roberts 2005, Theorem 4.2) gives the stability condition cos²θ₀ > (ℓ-1)(N-ℓ-1)/(N-1), which translates to C₁ = (N-1)(1+ξ²)/(1+ξ)²
4. **Polvani-Dritschel 1993** confirms N=4 threshold at θ = arccos(1/√3) = 54.74°, matching ξ* = 2-√3 (the C₁^eucl threshold), NOT 1/5 (the old C₁(S²) threshold)
5. At the paper's claimed threshold ξ = 1/19 for N=6, the actual eigenvalue is **+0.475** (still stable), not zero

## What was wrong

The appendix derives C₁^eucl = (N-1)(1+ξ²)/(1+ξ)² correctly (lines 262-275). Then a "Limitation" paragraph (lines 277-294) claims this is only the "Euclidean stereographic frame" result and cites BC2003 for a different "geodesic-metric" formula C₁(S²) = (N-1)(1-ξ)/(1+ξ). This citation is incorrect — LMR05 (the standard reference) gives the same formula as C₁^eucl.

## What the fix looks like

### Conceptual changes
- C₁^eucl IS the correct C₁(S²). Rename it and promote to the boxed formula.
- Remove the "Limitation" paragraph and the BC2003 citation for the wrong formula.
- S² thresholds change from rational {1/3, 1/5, 1/7, 1/19} to Pell units {1, 2-√3, 3-2√2, 9-4√5}.
- The "rational vs irrational" S²/H² asymmetry narrative becomes a **Pell unification**: both surfaces produce thresholds from fundamental units in Q(√d).

### The H²/S² duality (new, cleaner)
- H²: C₁ = (N-1)(1+ξ²)/(1-ξ)²
- S²: C₁ = (N-1)(1+ξ²)/(1+ξ)²
- Related by ξ → -ξ (curvature sign flip). Perfect duality.

### New threshold table
| N | m | Old ξ* (wrong) | New ξ* (correct) | Field |
|---|---|----------------|-------------------|-------|
| 3 | 1 | 1/3 | 1 | Q |
| 4 | 2 | 1/5 | 2-√3 | Q(√3) |
| 5 | 2 | 1/7 | 3-2√2 | Q(√2) |
| 6 | 3 | 1/19 | 9-4√5 | Q(√5) |
| ≥7 | — | None | None | — |

## Scope

### Phase 1: Sandbox verification (same workflow as Item #1)
- Verify the correct formula against the stereographic oracle (DONE — Task 2)
- Verify the new thresholds are Pell units (new check)
- Verify H²/S² duality ξ → -ξ (new check)
- math-reviewer gate on the corrected appendix section

### Phase 2: Code fixes (4 source files)
- `riemannian_havelock.py`: `C1_sphere()` → use `(1+xi**2)/(1+xi)**2`
- `algebraic_thresholds.py`: `sphere_stability_threshold()` → solve quadratic, return algebraic surd
- `oblate_spheroid.py`: `C1_sphere()` → same fix
- `spheroidal_havelock.py`: `C1_sphere_formula()` → same fix

### Phase 3: Test fixes (3+ test files)
- `test_algebraic_thresholds.py`: update threshold assertions {1/3,...} → {1, 2-√3,...}
- `test_riemannian_havelock.py`, `test_spheroidal_havelock.py`, `test_oblate_spheroid.py`: update expected values

### Phase 4: Paper fixes (8 LaTeX files)
- `paper-A-appendices/main.tex`: remove "Limitation" paragraph, promote C₁^eucl to boxed formula, update threshold list and Properties
- `paper/main.tex` (= paper-1-mathematics): update §4.2 threshold table, replace "rational" claims with Pell-unit structure, update ξ → -ξ duality discussion
- `paper-2-physics/main.tex`: update formula reference
- `paper-3-gravity/main.tex`: update table entry
- `paper-4-field-theory/main.tex`: update formula reference
- `companion/main.tex`: rewrite threshold explanation, update rationality claim
- `CLAUDE.md`: update formula

### Phase 5: Diff approval + verification (same gates as Item #1)

## Gates (same as Item #1)
1. **Numerical:** All oracle checks pass, new threshold values verified
2. **math-reviewer:** ≥9.0, zero structural deductions on corrected appendix
3. **Test suite:** All 4447+ tests pass after code+test updates
4. **Diff approval:** User approves each paper diff before application

## Non-goals
- Not changing the H² formula or thresholds (those are already correct)
- Not touching Item #2 (Riemannian Havelock universality) — the tangential eigenvalue IS universal, confirmed by oracle
- Not changing the Havelock identity proof (Item #1, already done)

## References
- LMR05: Laurent-Polz, Montaldi, Roberts 2005, Theorem 4.2
- Polvani-Dritschel 1993 (N=4 threshold confirmation)
- Oracle verification: `docs/rigor-sandbox/item6-c1-sphere/numerical_check.py`
- Item #1 workflow: `docs/superpowers/specs/2026-04-14-paper1-rigor-sandbox-design.md`
