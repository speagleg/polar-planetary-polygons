# Design: First-Principles Derivation of c = 12b(N) via Quillen/Takhtajan-Zograf Anomaly (Route C3a-extended)

**Date:** 2026-04-16 (v2, pivoted after Phase 0 literature audit)
**Status:** approved by Gordon, pivoted from bare WP to Quillen/TZ anomaly
**Target gap:** The central charge c = 12b(N) in Paper III is currently a matching condition (via Brown-Henneaux), not a derivation from polygon data alone. This spec attempts to derive it rigorously via the Chern form of the determinant line bundle on M_{0,N} with conical singularities.

## 0. Pivot from v1

**v1 was dead:** The Mirzakhani-Do-Norbury theorem proves ∫_{M̄_{0,N}} ω_WP at cone angles α_k is a rational multiple of π^(2(N-3)). This cannot equal 2b(N) because b(N) contains transcendental terms (ln 2, ln N) that don't arise from ψ-class / κ-class intersection theory.

**v2 pivot:** The determinant line bundle λ_det on the universal curve over M_{0,N} has a Chern form that decomposes into WP and Takhtajan-Zograf (TZ) pieces:
```
c_1(λ_det) = (1/12π²) ω_WP − (1/9) ω_TZ + (Quillen anomaly terms)
```
The TZ metric and the Quillen metric anomaly produce LOG-TYPE terms via analytic torsion — exactly the transcendence type of b(N).

**Reference:** Park-Takhtajan 2015 (arXiv:1508.02102) — "Potentials and Chern forms for Weil-Petersson and Takhtajan-Zograf metrics on moduli spaces of punctured Riemann surfaces."

## 1. The Mathematical Framework

### 1.1 The Moduli Space

Let M_{0,N} denote the moduli space of N ordered points on CP¹ modulo SL(2,R):
```
M_{0,N} = {(z_1, ..., z_N) ∈ (CP¹)^N : z_i ≠ z_j} / SL(2,R)
```
Complex dimension: N-3 (after the SL(2,R) quotient).

At the Z_N-symmetric configuration z_k = e^(2πik/N), we have a distinguished point (up to SL(2,R) rotation).

### 1.2 The Weil-Petersson Kähler Form

The Weil-Petersson metric on M_{0,N} arises from the classical Liouville action at the hyperbolic saddle. For N conical singularities of angle 2π/N (our case):

**Zograf-Takhtajan theorem (1987, 1988):**
```
ω_WP = (i/π) ∂∂̄ S_cl
```
where S_cl is the classical Liouville action evaluated on the saddle-point conformal factor φ_* solving:
```
Δφ = e^(2φ) − (π/N) Σ_k δ(z − z_k)
```

### 1.3 The Witten-Hitchin Identification

For SL(2,R) Chern-Simons theory at level k on Σ × S¹:

**Witten-Hitchin (1991, 1992):**
```
[ω_WP] / (2π) = k · [c_1]
```
where [c_1] is the first Chern class of a specific line bundle on M_{0,N}.

**Derivation plan:**
```
[ω_WP] / (2π) at Z_N-symmetric point = 2b(N)
```
Combined with c = 6k:
```
c = 12 b(N)
```

## 2. Why This Would Be a Genuine Derivation

**Unlike the current matching-condition framing:**
- Zograf-Takhtajan is a THEOREM (explicit formula for ω_WP)
- Witten-Hitchin is a THEOREM (Kähler class = CS level)
- Both are derived from first principles in the cited papers
- The composition gives c from polygon data (N, cone angles, symmetric configuration)
- No appeal to Brown-Henneaux or holographic dictionary

**What this would prove:**
- c = 12b(N) is uniquely determined by polygon geometry
- The factor 12 is not a convention but a consequence of (i) Zograf-Takhtajan and (ii) Witten-Hitchin and (iii) the Virasoro-CS relation c = 6k
- The Brown-Henneaux formula c = 3ℓ/(2G) becomes a CONSEQUENCE, not an assumption

## 3. The Technical Challenge

The computation requires evaluating [ω_WP] at the Z_N-symmetric point. This involves:
- The classical Liouville action S_cl at the N-gon saddle
- Differentiation with respect to puncture positions
- Integration over a chosen 2-cycle to extract the Kähler class

**For explicit cases:**
- N=3: trivial (no moduli, M_{0,3} is a point)
- N=4: complex dim 1. S_cl satisfies Painlevé VI. Computable via hypergeometric functions.
- N=5: complex dim 2. S_cl solvable via Heun-type equations.
- N=6: complex dim 3. More complex, but tractable with Painlevé-family machinery.
- N≥7: generally requires numerical PDE for the Liouville equation.

## 4. Phased Implementation Plan

### Phase 0: Literature Audit (1 session)
- Survey Zograf-Takhtajan papers for explicit WP formulas on M_{0,N}
- Survey Witten-Hitchin theorems for the Kähler class identification
- Check recent work (Takhtajan-Teo, Mondello, Krichever) for computational machinery
- Identify: is there already an explicit formula for [ω_WP] at the Z_N-symmetric point?

**Deliverable:** `docs/investigations/2026-04-16-goldman-hitchin-literature.md` summarizing what's known.

### Phase 1: N=4 — The Painlevé VI Test Case (2-3 sessions)
**Mathematical setup:**
- M_{0,4} ≅ CP¹ \ {0, 1, ∞} parametrized by cross-ratio λ
- At Z_4-symmetric: λ = -1 (puncture at each of 4th roots of unity, mapped via SL(2,R))
- Classical Liouville saddle satisfies Painlevé VI with specific parameters

**Computation:**
- Compute S_cl(λ) as a function of cross-ratio
- Compute ∂²S_cl / ∂λ ∂λ̄ at λ = -1
- Integrate ω_WP over CP¹ (the moduli space of M_{0,4})
- Check: does the result equal 2π · 2b(4) = 2π · 2.871?

**Success criterion:** The integral gives 2π · 2b(4) to within numerical precision.

**Deliverable:** `src/planetary_polygons/extensions/goldman_hitchin_n4.py` with tests.

### Phase 2: N=5 — The Heun Case (3-5 sessions)
**Mathematical setup:**
- M_{0,5} has complex dim 2
- At Z_5-symmetric: unique (up to SL(2,R) quotient)
- Liouville saddle solvable via Heun-type equations

**Computation:**
- Compute S_cl and its Hessian at the Z_5-symmetric point
- Compute [ω_WP] by integrating over a distinguished 4-cycle
- Check: 2π · 2b(5) = 2π · 4.418?

**Success criterion:** Agreement with 2π · 2b(5) to numerical precision.

**Deliverable:** `src/planetary_polygons/extensions/goldman_hitchin_n5.py` with tests.

### Phase 3: N=6, 7 — Numerical PDE Methods (5-10 sessions)
**Mathematical setup:**
- For N≥6, solve the Liouville PDE numerically on the punctured sphere
- Conformal factor φ_* sourced by N delta functions with cone angle 2π/N
- Use finite element or spectral methods

**Computation:**
- Discretize the sphere with N punctures
- Solve the Liouville PDE for φ_*
- Evaluate S_cl and its Hessian
- Compute [ω_WP]
- Check agreement with 2π · 2b(N)

**Success criterion:** Numerical agreement at N=6, 7 within controlled accuracy.

**Deliverable:** `src/planetary_polygons/extensions/goldman_hitchin_numerical.py` with PDE solver and tests.

### Phase 4: Analytical Proof (potentially many sessions, possibly indefinite)
**Mathematical setup:**
- If Phases 1-3 all confirm [ω_WP]/(2π) = 2b(N), derive the general formula
- Identify the specific coefficient function that gives 2b(N)
- Possible structures:
  - Formula involving the Gauss product Π sin(πm/N) (known to give transcendental part)
  - Formula involving the mean Casimir N(N+1)/12 (rational part)
  - Combination yielding b(N) = N(N+1)/12 − ln2 + lnN/(N-1)

**Success criterion:** A proof (analogous to Zograf-Takhtajan's original) that:
```
[ω_WP](z_k = e^(2πik/N)) / (2π) = 2b(N)
```

**Deliverable:** A theorem statement and proof in a new paper section or standalone note.

### Phase 5: Integration into Paper III (1-2 sessions, after Phase 4)
- Rewrite Proposition `prop:central-charge` as a derivation (not conditional)
- Update Remark `rmk:central-charge-open` to reference the new theorem
- Update all downstream references
- Run full test suite, verify no regressions

## 5. Risk Assessment

**High risks:**
- **Phase 1 may fail immediately**: If the explicit Painlevé VI computation at N=4 does NOT give 2b(4), the entire route is invalidated. Time invested: 2-3 sessions.
- **Phases 1-3 give DIFFERENT results**: The Kähler class might equal 2b(N) at N=4 by coincidence but not generalize. This would be evidence against the route without being definitive.
- **Analytical proof is infeasible**: Even if Phases 1-3 succeed, deriving a closed-form proof (Phase 4) may require techniques beyond current machinery.

**Medium risks:**
- **Numerical PDE accuracy**: At N=6, 7 the Liouville PDE solver may have insufficient precision to distinguish between 2b(N) and a nearby value.
- **Conical singularities in PDE**: The cone-angle boundary conditions introduce numerical challenges.

**Low risks:**
- **Code infrastructure**: We already have `cft_liouville_action.py` and `symplectic_comparison.py` as starting points.
- **Paper integration**: Phase 5 is straightforward once the derivation is done.

## 6. Early Termination Conditions

**Stop and reconsider if:**
- Phase 1 (N=4) does NOT give 2b(4) within numerical precision
- Phase 2 (N=5) does NOT give 2b(5) when N=4 did
- Phase 4 attempts show the identification requires additional inputs beyond Zograf-Takhtajan + Witten-Hitchin (in which case it's not a clean derivation)

If any termination condition triggers, we have evidence that C3a is not the right route and should switch to C3b (W_N orbit), C3c (Kirillov character), or return to the "matching condition" framing (Gordon's option B).

## 7. Success Outcome

If Phases 1-4 succeed:
- c = 12b(N) becomes a DERIVED result, not a matching condition
- The paper's final remaining gap is closed
- The factor 12 is explained as a composition of (Zograf-Takhtajan theorem) × (Witten-Hitchin identification) × (c = 6k from CS-WZW)
- Brown-Henneaux c = 3ℓ/(2G) becomes a consequence, not an assumption

This would constitute a genuine first-principles derivation of Newton's constant from polygon data.

## 8. Commitment

This project is expected to span 10-20 sessions (Phases 0-5 combined) with significant uncertainty. The outcome is binary: either we derive c = 12b(N) rigorously, or we have strong evidence that this route doesn't work and must accept the matching-condition framing.

Gordon has confirmed willingness to invest the time required, with the explicit instruction to "exhaust all routes before honest framing."

## 9. Files to Create

**New modules:**
- `src/planetary_polygons/extensions/goldman_hitchin_n4.py`
- `src/planetary_polygons/extensions/goldman_hitchin_n5.py`
- `src/planetary_polygons/extensions/goldman_hitchin_numerical.py` (Phase 3)
- `src/planetary_polygons/proofs/weil_petersson_kahler_class.py` (Phase 4)

**New tests:**
- `tests/test_goldman_hitchin_n4.py`
- `tests/test_goldman_hitchin_n5.py`
- `tests/test_goldman_hitchin_numerical.py`

**New docs:**
- `docs/investigations/2026-04-16-goldman-hitchin-literature.md` (Phase 0)
- `docs/investigations/2026-04-16-painleve-vi-wp-n4.md` (Phase 1)
- `docs/investigations/2026-04-16-heun-wp-n5.md` (Phase 2)

## 10. Phase 0 Result (COMPLETED 2026-04-16)

Literature audit by physics-reviewer produced decisive findings:
- Bare WP route is dead (Mirzakhani-Do-Norbury theorem: integral is rational · π^(2(N-3)), cannot equal 2b(N))
- Quillen/TZ anomaly route is viable (log terms from analytic torsion match b(N) transcendence type)
- Park-Takhtajan 2015 has explicit Chern form formula for c_1(λ_det)

## 11. Immediate Next Step (Phase 0b)

Deep-dive into Park-Takhtajan 2015 (arXiv:1508.02102) and Takhtajan-Zograf 2014 local index theorem for orbifolds. Extract:

1. **Exact formula for c_1(λ_det)** in terms of ω_WP, ω_TZ, and Quillen metric log terms
2. **Explicit computation** of the TZ Kähler form at the Z_N-symmetric point of M_{0,N}
3. **Quillen metric anomaly** contributions: the log(det Δ) terms at conical cusps
4. **Numerical check at N=4**: does c_1(λ_det) [with correct normalization] equal 2b(4)?

If the N=4 numerical check matches 2b(4) = 2.871 to the expected precision, proceed to Phase 1 in full.
If the numerical check fails, we have decisive negative evidence for C3a-extended as well.

## 12. Revised Phase Plan (post-pivot)

- **Phase 0** (done): Bare WP route eliminated; pivot to Quillen/TZ.
- **Phase 0b** (current, 1-2 sessions): Extract Park-Takhtajan formula, numerical N=4 test.
- **Phase 1** (2-3 sessions if 0b passes): Full N=4 c_1(λ_det) computation with test suite.
- **Phase 2** (3-5 sessions): N=5, 6 via same machinery.
- **Phase 3** (5+ sessions): General analytical derivation that c_1(λ_det)(Z_N-symmetric) = 2b(N).
- **Phase 4** (2 sessions): Paper integration.
