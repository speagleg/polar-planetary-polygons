# Reviewer feedback — Sessions 1-6 framework

**Date**: 2026-04-16
**Reviewers**: math-reviewer + physics-reviewer (parallel dispatch)

---

## Math review: grade **C+** (overclaims) → fixable to B+

### What's SOLID
- **M1 γ⁵ fix** (grade A): matrix identity γ⁵ = γ^(3)·γ³ is correct, sympy-verified.
- **G5 σ identity** (grade A−): (N²+7)/8 = N → (N-1)(N-7) = 0 is genuine algebra.
- **Riemann-Hurwitz 3-gen** (grade B−): arithmetic correct; uniqueness claim needs "g(X(N)) ≥ 1" hypothesis (N=5 also gives F=2 trivially).

### What's OVERCLAIMED
1. **"Five independent N=7 uniqueness arguments" is too strong**:
   - Pell, Riemann-Hurwitz, Legendre are all "special mod-7 arithmetic" → NOT truly independent
   - G5 Dirac-σ identity is genuinely independent (good)
   - PMNS 1/(N²-1) is marginal fit (sin²θ_13 is -2.2σ off PDG) → NOT a uniqueness theorem

2. **"Legendre selection rule is DERIVED"**:
   - Pattern-fit to 16 target modes, not derived from first principles
   - CP-consistency argument ADMITS CP flips the sign, then rescues via Redlich gap
   - Reviewer recommends: demote from **Lemma** to **Proposition/Conjecture**

3. **"n_q = 2(λ + δ_iso) is a derivation"**:
   - Pattern match with down-quark going through Gatto (formula doesn't close on 6th quark)
   - Label as "proposed pattern matching observed exponents"

4. **"Y = T_3R + (B-L)/2 uniquely derived"**:
   - With 2 constraints and 2 unknowns, it's algebra not derivation
   - Say "consistent with SM" rather than "uniquely derived"

### What's IMPRECISE
- **C3 Lichnerowicz corrections**: formula sketch conflates Riemannian and gauge curvature
- **M1 derivation.md**: has scratch-work confusion at lines 75-87 (block algebra admitted as off) — clean up

### Recommendation
Rewrite uniqueness claims honestly: "three algebraic/geometric N=7 signals (Pell, RH, Dirac-σ), plus Legendre residue and empirical PMNS match." Demote Legendre rule to Proposition. Add "g(X(N)) ≥ 1" to RH theorem.

---

## Physics review: grade **B−** (structurally solid, derivations uneven) → fixable

### What's CORRECT
- **Matter content = SM + ν_R exactly** (verified numerically): 16 Weyl/gen, anomalies cancel, hypercharges match.
- **m_L = 493 TeV vs m_W = 80 GeV scale separation**: clean.
- **sin²θ_W = 3/11** is polygon-intrinsic prediction (not PS signature post-Task 7).
- **Pati-Salam framing retraction** aligns with Paper VI §683 "no GUT".

### GAPS
1. **m_4 → SU(2)_L/R assignment not derived**: `polygon_to_PS_mapping.py` asserts m_4 ∈ {1,2} → L doublet, m_4 ∈ {0,3} → R doublet, but the ASSIGNMENT comes from fiat, not polygon structure. Needs explicit N=4 isospin sector derivation.

2. **Higgs real-dof count missing**: BF gives 2 complex scalar modes at (3,2),(4,2); SM Higgs doublet has 4 real components (3 eaten). Explicit reconciliation missing.

3. **Higgs VEV scale not addressed**: BF instability naturally gives VEV at polygon scale (300 TeV); SM Higgs v = 246 GeV. The ε_7^{-7} electroweak hierarchy bridges this but must be invoked explicitly.

4. **4D graviton KK lift**: "boundary SO(2) = 4D transverse SO(2)" is asserted, not constructed. Standard AdS_3/CFT_2 gives 3D graviton; 4D uplift via S¹ fiber is non-standard and under-developed.

5. **sin²θ_W at M_Z is 3.9% off** (0.240 predicted vs 0.231 observed) — not a "confirmed prediction" as might be claimed.

### CROSS-ARTIFACT INCONSISTENCY
- `polygon_to_PS_mapping.py` still claims "matches PS at ρ² = 8/5"
- `z3_extensions_analysis.md` correctly retracts this
- Need to fix the script or explicitly note retraction

### Recommendation
One more rigor pass addressing:
1. Demote Legendre rule to Proposition (math reviewer also)
2. Derive m_4 → SU(2)_L/R assignment
3. Count Higgs real dof explicitly
4. Address Higgs VEV vs M_poly scale
5. Construct 4D graviton KK lift (or honest flag)
6. Honest sin²θ_W language
7. Fix cross-artifact PS framing

---

## Combined verdict

**Both reviewers agree**:
- Framework has REAL content (M1, G5, anomaly cancellation, 3-gen geometric count).
- Matter content IS SM+ν_R (verified).
- Main issue: **overclaiming in revision draft** — several "theorems"/"derivations" are structural fits.
- **Fixable with one more pass**.

**Current framework status**:
- Math: C+ → with honest relabeling → B+
- Physics: B− → with structural gaps filled → B+/A−

**Recommended action**: one more rigor pass before publication review, focusing on:
1. Honest language ("proposition" for structural fits, not "lemma")
2. Fill specific gaps (m_4 assignment, Higgs dof, 4D graviton lift)
3. Tighten uniqueness statements (add "g ≥ 1" hypothesis, acknowledge empirical PMNS tension)
4. Clean up scratch work in M1 derivation.md
5. Fix cross-artifact PS framing inconsistency

Framework has a SOLID core; main work is expository honesty.

---

## Priorities for addressing

**HIGH (reviewer-flagged errors)**:
- Fix RH theorem uniqueness with "g(X(N)) ≥ 1" hypothesis
- Demote Legendre "Lemma" to "Proposition"
- Strip "five independent uniqueness" to "three genuine + PMNS empirical"
- Clean up cross-artifact PS framing inconsistency

**MEDIUM (structural gaps)**:
- Derive m_4 → SU(2)_L/R assignment
- Higgs real-dof count
- 4D graviton KK lift construction

**LOW (exposition)**:
- Clean up M1 derivation.md scratch work
- Honest sin²θ_W language
- Explicit Lichnerowicz formulas in C3

**Should address before actual paper application.** Gordon decides priority.
