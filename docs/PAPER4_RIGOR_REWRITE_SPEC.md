# Paper IV — Structural Rigor Rewrites (Spec)

## Status

Paper IV scores **5.2/10** on fresh-eyes mathematical review. Ten structural issues and fourteen minor issues identified. Core results (CKM phase via Gauss sums, graviton identification via Pell, PMNS θ₂₃ = π/4, mass hierarchy predictions) are arithmetically clean. The issues are concentrated in the **gauge-group derivation** (SU(2), SU(3), U(1)) and the **spacetime uniqueness** proof. No circular dependency on c = 12b(N).

## Canonical file

`latex/paper-4-field-theory/main.tex` (3823 lines)

See `docs/rigor-sandbox/WORKFLOW_TEMPLATE.md` for the per-item workflow.

## Working files

- `latex/paper-4-field-theory/main.tex` — canonical Paper IV
- `latex/paper-A-appendices/main.tex` — shared appendices
- `src/planetary_polygons/extensions/` — computational backing
- `tests/` — all numerical claims have backing tests

---

## Structural Rewrite #1: N assignment inconsistency for SU(2) (lines 2680–2690, 2957–2963, 3689–3697)

**Current state**: The Weinberg-angle derivation puts SU(2) at N=4 (m*=2, f(2,4)=2, k+h∨=3). The proton-stability/sector-decoupling proof (§sec:decoupling, cor:proton-stability) requires SU(2) at N=8 (since lcm(7,8)=56 and solves 8(m₁+m₂) ≡ 28 mod 56). These are inconsistent: if SU(2) is at N=4, the relevant overfield is ℚ(ζ₂₈) and the congruence 4(m₁+m₂) ≡ 14 mod 28 has no integer solutions.

**Fix**: Pick one N for SU(2) (either N=4 or N=8) and rederive both sections consistently.

**Difficulty**: Medium-hard. Requires tracing through both derivations to see which N is physically correct, then rewriting the other.

**Estimated effort**: 2-3 sessions.

---

## Structural Rewrite #2: Category error in spacetime uniqueness proof (Proposition 3.1, lines 248–272)

**Current state**: Step (ii) conflates polygon deformation modes (N-1 modes of N vortex positions on the base) with fiber Fourier modes (N-1 modes of S¹/Z_N). These are a priori different Hilbert spaces. The claim "on any d-dimensional fiber, mode count grows as O(N^d)" is incoherent — the polygon always has N-1 deformation modes regardless of fiber.

**Fix**: Either (a) derive the fiber dimension from a separate physical requirement (zero-mode counting in KK reduction), or (b) explicitly identify polygon modes with fiber Fourier modes via a theorem.

**Difficulty**: Hard. Requires rethinking the uniqueness argument.

**Estimated effort**: 2-3 sessions.

---

## Structural Rewrite #3: SU(2)_L internal contradiction (lines 1027–1054)

**Current state**: Line 1027: "the physical weak force is identified with the sector having the SMALLER effective k." Lines 1049–1054: SU(2)_L assigned to sector with k_L^eff = 23/14 (the LARGER effective level). Direct contradiction.

**Fix**: Decide whether physical weak force has smaller or larger k_eff and rewrite consistently. The η sign choice for "left" must be principled, not post hoc.

**Difficulty**: Low-medium. Statement-level fix.

**Estimated effort**: Half day.

---

## Structural Rewrite #4: CKM "up-type sums QR" asserted, not derived (lines 3058–3099)

**Current state**: α_2 = 1 + G(QR) = (1+i√7)/2 gives arg α_2 = arctan√7. But the assignment "up-type amplitude = Y₀ + Σ_{m∈QR} Y_m" is a CHOICE. Why should up-type not include QNR contributions?

**Fix**: Show that only QR sectors contribute to up-type three-point function via a selection rule from SU(2) isospin quantum number.

**Difficulty**: Medium. Requires deriving a selection rule.

**Estimated effort**: 1-2 sessions.

---

## Structural Rewrite #5: Gauss-Bonnet "free-energy minimization" circular (lines 641–681)

**Current state**: Step (ii-b) of Proposition `prop:couplings` claims F(g) = 4πℓ²(g-1) - Tg ln 3 is minimized at g=2. But F is LINEAR in g, so the minimum is at the smallest allowed g. The "g ≥ 2" constraint is what forces g=2, not the minimization.

**Fix**: State honestly that g=2 is the smallest non-degenerate genus, not selected by thermodynamic minimization. Or find a non-circular minimization.

**Difficulty**: Low. Statement-level fix.

**Estimated effort**: Half day.

---

## Structural Rewrite #6: ALE/K-matrix conflates abelian and non-abelian CS (lines 1461–1476)

**Current state**: Wen K-matrix at K=A₂ gives U(1)×U(1) CS with 3 sectors. Paper asserts this has "same topological order as SU(3)_1". While conformal weights match, these ARE different theories: U(1)×U(1) is abelian; SU(3)_1 is non-abelian with non-trivial fusion. K-matrix does NOT give non-abelian gauge bosons with [J^a, J^b] = if^{abc}J^c.

**Fix**: Either (a) weaken to "abelian subsector matches", or (b) use McKay correspondence + heterotic CFT directly without K-matrix.

**Difficulty**: Medium. Conceptual fix.

**Estimated effort**: 1 session.

---

## Structural Rewrite #7: η_grav formula needs explicit derivation or citation (lines 981–1018)

**Current state**: Formula η_grav(N) = −4s(1,N) + (N-1)/(6N) stated to arise from Bismut-Cheeger adiabatic limit. Base contribution η(Σ)=0 justified by "2D Dirac has symmetric spectrum" (correct). But (N-1)/(6N) term asserted without explicit citation for its lens-space defect origin.

**Fix**: Cite specific computation (Komuro, Nishi, Nishikawa) or derive from first principles via APS index on L(N,1).

**Difficulty**: Medium. Literature search + citation.

**Estimated effort**: 1 session.

---

## Structural Rewrite #8: thm:maximal-atm part (d) assumes σ₂₃-preserving breaking (lines 3261–3319)

**Current state**: Theorem derives m_ν with doubly-degenerate eigenvalue 7w/4. Part (d) selects basis {ν₂, ν₃} by diagonalizing σ₂₃ simultaneously with m_ν — this is additional input, not derived. The remark acknowledges this but the theorem statement does not include the hypothesis.

**Fix**: State in theorem that θ₂₃ = π/4 follows given σ₂₃-preserving breaking (equivalently, μ-τ exchange symmetry).

**Difficulty**: Low. Statement-level fix.

**Estimated effort**: Half day.

---

## Structural Rewrite #9: c_EW identity is approximate, not exact (lines 3737–3740)

**Current state**: Paper claims c_EW = c_7/3 = c_4 = 12b(4) as exact structural identity. Numerically: 12b(7)/3 = 17.19 vs 12b(4) = 17.23. Differ by 0.035 (0.2%).

**Fix**: Acknowledge as approximate (numerical coincidence) OR find the exact identity.

**Difficulty**: Low. Either acknowledgement or find hidden identity.

**Estimated effort**: Half day.

---

## Structural Rewrite #10: "Integer spin at Havelock threshold" Pell selection is infinite family (line 156, prop:spacetime)

**Current state**: Pell j(j+1) = f(m*,N) = (N²-1)/8 (odd N) has solutions (N,j) = (1,0), (7,2), (41,11), (239,...). For even N: only N=4. Paper says "Pell selects N=4 and N=7" but next solution is N=41.

**Fix**: Explicitly state the bound that excludes N=41 (e.g., stability on H² at small ξ, or N ≤ N_crit+4 from Paper I).

**Difficulty**: Low-medium. Needs citation or short argument.

**Estimated effort**: Half day.

---

## Minor Issues (14 total)

1. **M1** (line 217): c₁ = N/2 (Chern convention) vs c₁ = N (Seifert "twice-Euler") used inconsistently
2. **M2** (line 582): 4/51.57 = 7.76% rounds to 8% but treated as exact
3. **M3** (line 263): f(m,N) injective on {1,...,⌊N/2⌋} — benign but worth noting for odd N
4. **M4** (line 267): "palindromic pairing exactly 2-fold" — needs exception for self-paired m=N/2
5. **M5** (lines 1080-1093): Level quantization conflates one-loop dual-Coxeter shift with eta-invariant boundary contribution
6. **M6** (line 1840): Weinberg derivation — cleaner as "ratio depends only on Q²/k_Y and C₂/(k+h∨)"
7. **M7** (conj:pmns): PMNS fractions labeled "Conjecture"; framing should not read as proof
8. **M8** (line 2279): k₁(E₈) = 4 notation undefined
9. **M9** (line 2095): f(m*,N) = j(j+1) match is specific to N=4 and N=7, not universal
10. **M10** (thm:instanton-vub): K = 0.548 not dilute; higher-order corrections not demonstrably subdominant
11. **M11** (line 1679): Δk = 3 ∈ ℤ assumes all 6 quark flavors have same sign mass
12. **M12** (line 2910): m_c/m_b = K² = 0.30 prediction (observed 0.304) should be stated
13. **M13** (line 2869): Two-loop RK4 M_poly shift should be stated or cited
14. **M14** (der:string-tension): Z(S³) factorization — "two S³ caps bounding Σ_g × S¹" geometrically unclear

---

## Suggested Order of Attack

1. **S3 first** (SU(2)_L contradiction): 30-min fix, statement-level
2. **S5 next** (Gauss-Bonnet circular): 30-min fix
3. **S8 next** (thm:maximal-atm hypothesis): 30-min fix
4. **S9 next** (c_EW approximate): 1 hour
5. **S10 next** (Pell exclusion of N=41): needs citation, 1 hour
6. **S7 next** (η_grav citation): 1 session
7. **S4 next** (CKM QR selection): 1-2 sessions
8. **S6 next** (K-matrix weakening): 1 session
9. **S1 last** (SU(2) N=4 vs N=8): 2-3 sessions, requires tracing
10. **S2 last** (spacetime uniqueness category error): 2-3 sessions, conceptual

After each structural rewrite: dispatch math-reviewer on just that section.

## Expected Score Trajectory

- Current: 5.2
- After S3, S5, S8, S9, S10: ~6.5
- After S4, S6, S7: ~7.5
- After S1, S2: ~8.5+

## Reproducibility

```bash
cd /mnt/c/Users/gspea/source/repos/planetary-polygons-unified
python3 -m pytest tests/ -q --tb=no
# 4447 passed
```
