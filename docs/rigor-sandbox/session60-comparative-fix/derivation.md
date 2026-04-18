# Session 60 — Replace §15.6 competitor-comparison table with derivation-content statement

## Context

PAPER4_REVISION_DRAFT.md CHANGE 15 §15.6 currently closes the uplift no-go discussion with a 5-row table ranking the polygon framework against Standard Model, LQG, string landscape, and asymptotic safety on "Ω_Λ prediction from first principles." The unified-framework reviewer flagged this as rhetorical overreach: the bracketing is unfair (each row represents a program with different goals and different notions of "first principles"), and the load-bearing content — what the polygon framework actually derives, from what inputs — is obscured by the comparative framing.

This session replaces that table with a proposition that states the derivation content directly: inputs, outputs, rigor level, residual. No comparative claim is made.

## 1. What §15.6 should say

The content §15.6 is trying to communicate is:

- Given a specific input set, the polygon framework derives a specific Ω_Λ.
- The derivation has a specific rigor level (tree + 1-loop CW + FR + tree-level BO instanton).
- The residual Planck-tension is structurally bounded by the Session 49 no-go theorem.

None of these statements require naming competitor frameworks. The table-form claim "the ONLY one among [SM, LQG, string landscape, asymptotic safety] that derives Ω_Λ from first principles" is true-but-rhetorical and will draw reviewer fire.

The replacement is a proposition of the form: **Given inputs X, the framework derives Y, with rigor level Z, residual R bounded by theorem T.**

## 2. Proposition (replacement §15.6)

**Proposition 15.6 (Ω_Λ derivation content).** Under the following inputs and rigor level, the polygon framework derives Ω_Λ to the stated precision with a theorem-bounded residual:

- **Inputs (three):**
  1. **M_Planck** (observational; fixes the overall energy scale v = 246 GeV ≤ M_P in the standard reduction chain);
  2. **Polygon vertex count N = 11** (derived from Havelock stability: the smallest N ≥ 8 compatible with the Paper VI cosmology section selection rule, not a free parameter);
  3. **Standard cosmological fluid content** (baryons, cold dark matter, radiation, neutrinos — their mass-energy densities are framework outputs from Papers III-V, not inputs to this proposition).

- **Derivation chain (4 steps, all from prior sessions):**
  1. Havelock stability + Paper VI's §n-selection ⇒ N = 11;
  2. H² curvature radius ℓ satisfies ln(ℓ v) = S_BO(11) − γ_E/2 = 102.435 (Session 33 WKB, Session 51 dimensional restoration);
  3. Topological CC of the 3D base after S¹ reduction is Λ_3 = (N² − 16)/16 = 105/16 (Paper V Prop. prop:lambda);
  4. Observed 4D CC is Λ_4^obs = Λ_3/ℓ² (Session 51 eq. 51.12).

- **Output (one number, two digits):** Ω_Λ = 0.695.

- **Rigor level:** tree-level + 1-loop Coleman-Weinberg + Freund-Rubin + tree-level BO instanton (explicit, Paper VI §radion-potential).

- **Residual:** 1.4σ Planck tension on Ω_Λ (Planck 2018 central value 0.685 ± 0.007).

- **Residual bound:** The Session 49 no-go theorem (CHANGE 15 §15.2) shows that no combination of 14 derivable correction classes within the stated rigor level closes this 1.4σ residual. The residual is therefore structural-at-this-rigor, not a numerical artifact.

Verification: the numerical check in Session 51 §6 gives Λ_4^theory / Λ_4^obs = 0.992 (0.8% agreement with Planck 2018), using only numpy-level arithmetic from the four derivation-chain steps above. ∎

## 3. What §15.6 should NOT say

- No claim that the polygon framework is "the only" framework to do anything.
- No comparison to Standard Model, LQG, string landscape, asymptotic safety.
- No use of the word "competitor" or any substitute (alternative, rival, peer).
- No ranking table.

These belong in informal exposition (talks, blog posts), not a revision draft of a mathematical-physics paper.

## 4. Proposed Paper VI edit (replacement for §15.6 lines 3046-3064)

Replace the entire subsection §15.6 with:

```markdown
### 15.6 Derivation content

**Proposition (Ω_Λ derivation content).** Given the inputs (M_Planck;
polygon vertex count N=11, derived from Havelock stability and the
Paper VI §n-selection rule; and standard cosmological fluid content),
the polygon framework derives

    Ω_Λ = 0.695

at rigor level (tree + 1-loop Coleman-Weinberg + Freund-Rubin +
tree-level BO instanton), via the four-step chain:

  (i)   Havelock stability + Paper VI n-selection  ⇒  N = 11;
  (ii)  H² curvature radius  ln(ℓ·v) = S_BO(11) − γ_E/2 = 102.435
        (Session 33 WKB; Session 51 dimensional restoration);
  (iii) Topological 3D base CC  Λ_3 = (N² − 16)/16 = 105/16
        (Paper V Prop. prop:lambda);
  (iv)  Observed 4D CC  Λ_4^obs = Λ_3/ℓ²  (Session 51 eq. 51.12).

The 1.4σ Planck-2018 tension on Ω_Λ is bounded by the Session 49 no-go
theorem (§15.2): no combination of the fourteen derivable correction
classes within the stated rigor level closes this residual. The
tension is structural at this rigor level, not a numerical artifact.

The rigor-extension direction (e.g., 2-loop CW, higher-genus BO, or
an explicit companion sector) is well-defined but outside the scope
of this paper.
```

This is ~18 lines vs. the current ~19 lines — no net length change.

## 5. Why this is a net rhetorical improvement

- **What the reviewer attacks reduces.** The current §15.6 offers a four-framework bracket that a motivated reviewer will contest on the merits of each framework. The replacement offers only first-party derivation content, which cannot be attacked on bracketing grounds.

- **What the reader learns increases.** The current §15.6 communicates "we are best." The replacement communicates the three inputs, four derivation steps, rigor level, numerical output, and residual bound — all of which are load-bearing for a reader deciding whether the framework's Ω_Λ prediction is worth engaging with.

- **Consistency with Session 47/48 framing.** CHANGE 14 established the pattern of converting claim-level statements into precise scope statements (e.g., reheat ceiling T_rh ≤ 3 GeV, σ_start algebraic-coincidence footnote). §15.6's replacement follows the same template.

## 6. Numerical consistency with Session 51

All numbers in the proposition are lifted directly from Session 51 §6 without modification:

- S_BO(11) = 102.724 (Session 33)
- ln(ℓ·v) = 102.435 (Session 51 eq. 51.13)
- ℓ = 1.248 × 10⁴² GeV⁻¹ (Session 51 eq. ℓ-from-v)
- Λ_3 = 105/16 = 6.5625 (Paper V)
- Λ_4^theory = 4.21 × 10⁻⁸⁴ GeV² (Session 51 eq. 51.14)
- Λ_4^obs = 4.25 × 10⁻⁸⁴ GeV² (Planck 2018)
- Ratio 0.992 (0.8% agreement)
- Ω_Λ = 0.695 (CHANGE 9, Paper V Prop. cosmology)

No re-computation is needed; this session is rhetorical/structural.

## 7. Summary

- Session 60 is a structural fix to PAPER4_REVISION_DRAFT.md CHANGE 15 §15.6.
- Content of the replacement is derivation-first: inputs, chain, output, rigor, residual, residual-bound.
- No mention of competitor frameworks.
- No numerical changes; all values inherited from Session 51.
- Paper VI edit is a single-subsection swap (§15.6 lines 3046-3064).
