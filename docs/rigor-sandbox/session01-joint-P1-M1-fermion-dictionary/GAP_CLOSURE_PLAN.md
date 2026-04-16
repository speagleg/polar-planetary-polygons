# Gap closure plan: systematic resolution of each open/fitted/partial item

**Date**: 2026-04-16
**Goal**: close every identified gap for a fully coherent unified framework.

## Gaps to address (from FRAMEWORK_AUDIT.md)

### Corrections (Session 1's own missteps)

**G0. Retract Pati-Salam UV framing**
- Issue: we framed Pati-Salam as the UV gauge group; paper explicitly rejects GUT (Paper VI §683).
- Fix: retain PS only as REP-LEVEL notational decomposition of matter content; remove "UV framework" language from revision draft.
- Effort: document update + revision draft edit.
- Status: in progress below.

### Partially derived — need rigorous derivation

**G1. SU(2)_L vs SU(2)_R assignment to m_4 pairs**
- Issue: our dictionary assigns {m_4 = 1, 2} to SU(2)_L doublet, {m_4 = 0, 3} to SU(2)_R doublet. Motivated by critical-mode proximity (m_4 = 2 is SU(2) adjoint), but not derived.
- Need: spectral/symmetry argument identifying which CP pair is L vs R.
- Difficulty: MEDIUM — requires understanding chirality projection on N=4 KK modes.

**G2. Y = T_3R + (B-L)/2 formula**
- Issue: we use this as an ansatz that reproduces SM Y values. Need to derive from polygon structure.
- Fix: derive Y from the Cartan structure of SU(3)_c × SU(2)_L × SU(2)_R × U(1)_Y (polygon's UV gauge group) with specific matter embedding.
- Difficulty: MEDIUM.

**G3. Pair 3 = Higgs doublet identification**
- Issue: paper says "pair 3 (modes 3, 4) is Higgs" via "BF-crossing structure" — not fully derived.
- Fix: explicit derivation from BF instanton dynamics on H².
- Difficulty: HIGH.

### Genuinely fitted (rigor plan items)

**G4. Quark mass K^n exponents {n_b=2, n_s=4, n_u=6, n_c=2}** — rigor plan C4
- Issue: ad hoc selection per quark.
- Fix: derive selection rule from gauge-invariance / symmetry / topology.
- Difficulty: HIGH (explicit open problem in rigor plan).

**G5. σ warp-factor coherence (σ_geo, σ_CKM, σ_mass)** — rigor plan C1
- Issue: three σ values via distinct arguments.
- Fix: single KK-reduction calculation producing all three.
- Difficulty: HIGH (explicit open problem in rigor plan).

### Conjectured (explicitly open)

**G6. PMNS fractions 6/7, 4/7, 1/48** — Conjecture 16.6
- Issue: conjectured, not derived.
- Fix: derive via Klein quartic modular forms at CM point τ_0 = (1+i√7)/2.
- Difficulty: HIGH (technical automorphic forms).

**G7. δ_CP tension with T2K/NOvA**
- Issue: prediction 69.3° in ~3σ tension with experiment preference ~-90°.
- Resolution: acknowledge; DUNE/HyperK will decide.
- Not a derivation gap; an experimental open question.

### Technical / quantitative

**G8. Quantitative Yukawa overlap integrals**
- Issue: structure derived (Z/7 at cusps), values not computed.
- Fix: explicit Eisenstein series overlap on Klein quartic.
- Difficulty: MEDIUM-HIGH.

**G9. Numerological b = g = 3 at N=7**
- Issue: match is unique to N=7 but may be coincidental.
- Fix: derive via Dedekind zeta / Eichler-Selberg.
- Difficulty: HIGH, and may not yield structural result.

## Prioritized attack order

1. **G0** — simplest correction, do now
2. **G1** — accessible, medium effort, structurally important
3. **G2** — follows from G1 + structural reasoning
4. **G5 (C1)** — important rigor plan item, structural
5. **G4 (C4)** — hard rigor plan item, may need novel insight
6. **G3** — BF-crossing derivation, deep
7. **G6 (Conjecture 16.6)** — specialized modular forms work
8. **G8** — technical, follows from previous
9. **G9** — exploratory, low priority

## This session: address G0, G1, G2

**G0**: retract PS-UV framing in revision draft
**G1**: derive SU(2)_L/R m_4 assignment from polygon structure
**G2**: derive Y formula from polygon Cartan structure

Each subsequent gap addressed in subsequent sessions or within this session if time.
