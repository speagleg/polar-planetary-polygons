# Paper III — Structural Rigor Rewrites (Spec)

## Status

Paper III scores **6.5/10** on fresh-eyes mathematical review. Five structural deductions and seven minor issues identified. Core results (uniqueness of logarithmic kernel, Pell graviton identification, Jensen-based Einstein derivation, Onsager contraction) are computationally correct but several proofs have gaps or errors in intermediate steps.

## Canonical file

`latex/paper-3-gravity/main.tex` (5576 lines)

See `docs/rigor-sandbox/WORKFLOW_TEMPLATE.md` for the per-item workflow.

## Working files

- `latex/paper-3-gravity/main.tex` — canonical Paper III
- `latex/paper-A-appendices/main.tex` — shared appendices
- `src/planetary_polygons/extensions/` — computational backing
- `tests/` — all numerical claims have backing tests

---

## Structural Rewrite #1: Proposition `prop:non-crossing` (line 4453) — odd-N extremum formula

**Current state**: The proof claims `R_max = (N²-2)/(4N²)` by evaluating at `m = N/2 - 1`. For even N this is correct. For odd N = 2k+1, the maximum of `g(m) = 2m(N-m-1)+(N-1)` on `1 ≤ m < N/2` occurs at `m = k = floor(N/2)`, giving `g = (N²-1)/2 > (N²-2)/2`. The displayed bound `1/4 - 1/(2N²)` is wrong for odd N.

**Conclusion still holds**: `(N²-1)/(4N²) < 1/4` for all N. Just the displayed formula is wrong.

**Fix**: Replace `1/4 - 1/(2N²)` with `1/4 - 1/(4N²)` (valid for all N), or distinguish even/odd cases.

**Downstream impact**: Proof-only fix. The proposition statement bound `< 1/4` is unchanged, so Remark `rmk:field-preservation` (line 4483) and all citations of non-crossing are unaffected. No value changes propagate.

**Difficulty**: Low. Formula fix + verify.

**Estimated effort**: 30 minutes. **STATUS: DONE** (commit ab6c9a1).

---

## Structural Rewrite #2: Lemma `lem:regge-bridge` (line 2313) — sign error in chain rule

**Current state**: The proof claims `d²S/dR² = (dS/dC₁)(d²C₁/dR²) + (d²S/dC₁²)(dC₁/dR)²` and asserts the first term has sign `(-)(+) = (-)`. But `dS/dC₁ = (1/2) Σ 1/λ_m > 0` (entropy increases with confinement), so the first term is `(+)(+) = (+)`, not negative.

**Conclusion still holds**: The second (strictly negative) term dominates numerically, confirmed by the oracle. But the claim "strict concavity holds exactly, not just at leading order" is not established.

**Fix**: Correct the sign, provide a quantitative bound showing dominance of the second term for all ε in the relevant range, or restrict the claim to sufficiently small ε.

**Downstream impact**: The conclusion `d²S/dR² < 0` feeds into the Jensen argument (lines 2374-2376) which gives the unique entropy maximum at constant curvature. If d²S/dR² < 0 is weakened to "holds for ε small enough," then the Einstein derivation becomes conditional on ε being in the concavity domain. Check: does the subsequent Jensen argument use the "exact" claim, or just concavity in a neighborhood? The Einstein result (Prop `prop:einstein-from-onsager`) at line ~1685 uses S concave in R — if we restrict ε, the proposition hypotheses need updating.

**Difficulty**: Medium. Need to bound the ratio of the two terms.

**Estimated effort**: 1 day.

---

## Structural Rewrite #3: Derivation `thm:partition-equality` (line 910) — SL(2,R) one-loop exactness gap

**Current state**: Step 5b claims CS is one-loop exact at the SL(2,R) flat connection by complexification from SU(2). The cited references (Axelrod-Singer, Witten 1989) address the compact case. The SL(2,R) path integral requires a contour prescription (Plancherel measure) and the analytic continuation of higher-loop coefficients requires more than real-form equivalence at the Lie algebra level.

**What's missing**: Either a rigorous justification of the complexification, or a citation to a result that directly establishes one-loop exactness for SL(2,R) CS theory at a flat connection.

**Difficulty**: Hard. This is a genuine gap in the mathematical physics.

**Plan**: Check if Gukov-Witten (2010) or Dimofte-Gukov-Lenells-Zagier handle the non-compact case. If not, state the result as conditional on one-loop exactness (with the cited evidence) rather than as proved.

**Downstream impact**: The partition function correspondence is the bridge between vortex statistical mechanics and CS/gravity. If Step 5b becomes conditional, then Derivation `thm:partition-equality` becomes a conditional result ("under one-loop exactness for SL(2,R) CS"). Trace what cites `thm:partition-equality` — this likely affects the Regge bridge, the BTZ entropy matching, and the WDW ground state. Map the full chain before editing.

**Estimated effort**: 1-2 days.

---

## Structural Rewrite #4: Proposition `prop:central-charge` (line 637) — conditional c = 12b(N)

**Current state**: The normalization `G = ℓ/(8b(N))` is presented as a conditional hypothesis (disclosed in Remark `rmk:central-charge-open`, line 660). But downstream quantitative results (WDW kinetic coefficient, BTZ matching, Cardy asymptotics) use `c = 12b(N)` as established fact without repeating the caveat.

**Fix**: Systematically mark all results conditional on the Brown-Henneaux normalization. Add a remark at first downstream use reminding the reader of the conditional status.

**Downstream impact**: c = 12b(N) appears 40+ times. The fix is a framing change (notation convention paragraph), not a mathematical change — no statements or values change. Downstream results remain valid conditional on the normalization. The key is that the reader can never encounter c = 12b(N) without knowing it's conditional.

**STATUS: DONE** (commit ab6c9a1). Added "Notation" paragraph after rmk:central-charge-open.

**Difficulty**: Low-medium. Tracking exercise across the paper.

**Estimated effort**: Half day.

---

## Structural Rewrite #5: Corollary `cor:onsager-contraction` (line 1950) — general surface extension

**Current state**: The contraction is proved on the Bolza surface with specific constants (λ₁ = 3.839). The extension to "any compact hyperbolic surface with λ₁ > 1/4" (lines 2211-2229) is asserted but the basin invariance (requiring surface-specific Sobolev and elliptic constants) is not verified for general surfaces.

**Fix**: Either prove the extension rigorously (deriving surface-independent bounds on the Sobolev constant) or restrict the corollary to the Bolza surface and state the extension as a conjecture.

**Downstream impact**: The Onsager contraction is used in the entropy bridge (linking vortex entropy to Bekenstein-Hawking). If restricted to Bolza, the BTZ/BH entropy match (Section ~5) remains valid only on Bolza. Check: does the BTZ argument use the general-surface claim, or does it only need the Bolza case? The gravity side is AdS₃ / BTZ, which corresponds to a specific surface — if that surface IS Bolza (or admits the same λ₁ bound), the restriction is harmless.

**Difficulty**: Medium. The Sobolev constant bound from Aubin/Hebey may suffice but needs to be spelled out.

**Estimated effort**: 1 day.

---

## Minor Issues

1. **M1: R̄₀ factor of 2** (line 1689): ~~Proposition states `R̄₀ = 2πχ/A`, proof derives `R̄₀ = 4πχ/A`.~~ **DONE** (commit ab6c9a1).
2. **M2: Antisymmetry tautology** (line 476): ~~Claims `[e∧e] = -[e∧e]`.~~ **DONE** (commit ab6c9a1). Replaced with sign-flip mechanism.
3. **M3: λ₀ notation overload** (line 1329): ~~`λ₀` collision.~~ **DONE** (commit ab6c9a1). Renamed to Λ_N.
4. **M4: λ₀ undefined** (line 1333): `λ₀ = (4/3)j(j+1)` with `j=(N-1)/2` appears before definition. Define first.
5. **M5: Pell sign convention** (prop:graviton, line 1343): Even-N uses positive Pell, odd-N uses negative Pell. Make the switch explicit in the proof.
6. **M6: O-notation hides relevant coefficient** (line 4454): `c = N² + N - 12ln2 + O(ln N/N)` hides the coefficient 12 of the `ln(N)/(N-1)` term. Consider making it explicit.
7. **M7: Sobolev constant bound** (lines 2187-2191): Claims `C_Sob ≤ 1.5` from Aubin/Hebey without derivation. Spell out or cite the specific theorem.

---

## Suggested Order of Attack

1. **M1 first** (R̄₀ factor): 5-minute fix
2. **S1 next** (non-crossing odd-N formula): 30-minute fix
3. **S4 next** (conditional c = 12b(N)): tracking exercise, half day
4. **S2 next** (Regge bridge sign): needs quantitative bound, 1 day
5. **S5 next** (Onsager contraction extension): needs Sobolev analysis, 1 day
6. **S3 last** (SL(2,R) one-loop exactness): hardest, may require conditional statement
7. **Remaining minor fixes** addressed as sections are touched

After each structural rewrite: dispatch math-reviewer on just that section.

## Expected Score Trajectory

- Current: 6.5
- After M1, S1: ~7.0
- After S4: ~7.5
- After S2, S5: ~8.5
- After S3: ~9.0+

## Reproducibility

```bash
cd /mnt/c/Users/gspea/source/repos/planetary-polygons-unified
python3 -m pytest tests/ -q --tb=no
# 4447 passed
```
