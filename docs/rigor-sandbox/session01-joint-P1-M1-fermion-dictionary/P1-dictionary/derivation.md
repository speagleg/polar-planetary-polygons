# Session 1 (P1): KK-mode → Weyl-fermion dictionary — exploration report

**Date**: 2026-04-16
**Status**: EXPLORATION (pre-derivation) — presenting structural findings to Gordon before committing to a framework.

---

## 1. The SM target (with right-handed neutrino)

One fermion generation of the SM + ν_R contains **16 left-handed Weyl fermions**:

| Field     | SU(3) | SU(2) | Y     | # Weyl |
|-----------|-------|-------|-------|--------|
| Q_L       | 3     | 2     | +1/6  | 6      |
| u_R^c     | 3̄     | 1     | −2/3  | 3      |
| d_R^c     | 3̄     | 1     | +1/3  | 3      |
| L_L       | 1     | 2     | −1/2  | 2      |
| e_R^c     | 1     | 1     | +1    | 1      |
| ν_R^c     | 1     | 1     | 0     | 1      |
| **total** |       |       |       | **16** |

The oracle (`oracle.py`) verifies this generation satisfies all five anomaly traces
(Tr Y, Tr Y³, Tr T₃²Y, Tr C_SU(3)·Y, Tr C_SU(3)³) exactly. Three generations = 48 Weyl.

(The SM without ν_R has 15 Weyl per generation; the paper's introduction of a ν_R per generation, via the right-handed KK zero mode on the Seifert fiber, is natural here since the sole known evidence against ν_R is the neutrino mass mechanism, which Paper IV treats via Dirac KK modes rather than a Majorana mass.)

## 2. The KK mode content available on R × (H² ×_7 S¹) × (polygon N=4 sector)

**SU(3) sector (N = 7, Frobenius orbits)** — already derived in §8.3 of Paper IV:

| m₇                | Frobenius orbit | SU(3) rep |
|-------------------|-----------------|-----------|
| 0                 | {0} (fixed)     | **1**     |
| 1, 2, 4           | O₊              | **3**     |
| 3, 5, 6           | O₋              | **3̄**     |

Seven modes total, organised as 1 ⊕ 3 ⊕ 3̄.

**SU(2) sector (N = 4, Z/4 structure)** — fermion KK masses μ₄ᶠ = |m₄ − 3/2|:

| m₄ | μ₄ᶠ  | "type" (§13.3) |
|----|------|-----------------|
| 0  | 3/2  | down-type       |
| 1  | 1/2  | up-type         |
| 2  | 1/2  | up-type         |
| 3  | 3/2  | down-type       |

Note: CP for fermions on N=4 must preserve fermion mass (μ₄ᶠ), so the correct CP action is m₄ → 3 − m₄ mod 4 (which pairs {0, 3} and {1, 2} — both μ-preserving). The scalar CP m₄ → 4 − m₄ mod 4 would pair {1, 3} (different masses), which is incorrect for the fermion sector.

**Full KK mode pair space** (N₇ × N₄) = 7 × 4 = **28 mode pairs** (m₇, m₄).

## 3. The counting problem

**Naive count**: each mode pair (m₇, m₄) gives one 4D Dirac fermion after KK reduction = 2 Weyl fermions (L + R chirality). Total: 28 × 2 = **56 Weyl fermions**.

**SM target**: 3 generations × 16 = **48 Weyl fermions**.

**Discrepancy**: **8 extra Weyl dof** (56 − 48).

This is a structural issue that the Session 1 derivation must resolve. Possible resolutions:

### Resolution A: Project out the m₄ = 2 adjoint mode
§8.1 identifies m₄ = 2 at N = 4 with the SU(2) adjoint (j = 1, dimension 3), which is a GAUGE field, not matter. Projecting out this mode removes 7 (m₇ values) × 2 (chirality) = **14 Weyl dof**, leaving 42 — too few.

### Resolution B: The m₇ = 0 singleton is absorbed into gauge structure
The m₇ = 0 scalar mode is critical for N = 7 and may be absorbed as the massless gauge mode of some sector. Removing m₇ = 0: 6 × 4 × 2 = **48 Weyl dof** — matches exactly!

### Resolution C: Chirality is locked to (m₇, m₄) by the Seifert geometry
KK reduction of a 4D Dirac fermion on a compact manifold with boundary (the Seifert CS setup) may project out one chirality per mode, not both. If each (m₇, m₄) mode gives only ONE Weyl fermion (not a Dirac pair), the count is 28 Weyl — **too few**.

**Hybrid resolution (provisional)**: Apply Resolution B. The m₇ = 0 mode is the SCALAR singlet (Higgs-like or gauge-like), NOT matter. Then matter fermion modes live on m₇ ∈ {1, ..., 6} × m₄ ∈ {0, 1, 2, 3}, giving 6 × 4 × 2 = 48 Weyl ✓.

## 4. Proposed structural dictionary (to verify)

Under Resolution B:

### 4a. Generation index = m₇ pair

| Generation | m₇ pair      | SU(3) content        |
|------------|--------------|----------------------|
| gen 1      | {1, 6}       | 3 (from 1) + 3̄ (from 6) |
| gen 2      | {2, 5}       | 3 (from 2) + 3̄ (from 5) |
| gen 3      | {3, 4}       | 3̄ (from 3) + 3 (from 4) |

(Pair 3 is the Higgs scalar pair in §13.1; here we identify it as the TOP generation fermions, co-located with the Higgs. Scalar and fermion coexist on the same KK tower because they sit at different KK-mass tiers: scalars at integer m − N/2, fermions at half-integer.)

Each generation therefore has 2 × 4 × 2 = **16 Weyl fermions** (2 m₇ modes × 4 m₄ modes × 2 chiralities). ✓ matches SM+ν_R per generation.

### 4b. SU(2) assignment per generation

Within one generation, we have 2 (m₇) × 4 (m₄) × 2 (χ) = 16 Weyl fermions. SM+ν_R decomposition:
- 6 Weyl in Q_L (3, 2): colored doublets
- 3 + 3 Weyl in u_R^c, d_R^c (3̄, 1): colored singlets
- 2 Weyl in L_L (1, 2): colorless doublet
- 1 + 1 Weyl in e_R^c, ν_R^c (1, 1): colorless singlets

But our 16 Weyl are all COLORED (both m₇ modes in a pair carry color). There are **no colorless states in one m₇ pair** — yet SM has L_L + e_R^c + ν_R^c = 4 colorless Weyl per generation.

**This reveals Resolution B is INCOMPLETE**: the color-neutral leptonic sector has no home.

### 4c. Revised framework: leptons from m₇ = 0

The m₇ = 0 mode is the COLOR-SINGLET KK sector of N = 7. Its KK tower in m₄ gives 4 × 2 = 8 Weyl fermions per m₇=0 copy. Per generation, we need 4 colorless Weyl (L_L + e_R^c + ν_R^c). With 3 generations, we need 12 colorless Weyl.

If m₇ = 0 provides only 8 Weyl total (one copy), we are short by 4. If it provides 3 copies (one per generation), we have 24 Weyl — 12 too many.

### 4d. A more promising framework: the GUT-style unification

A cleaner resolution: each SM generation is a chunk of 16 KK modes spanning BOTH the colored and the uncolored sectors of the Seifert product. Specifically:

- **Colored part**: 2 (m₇ pair) × 2 (m₄ up-type) × χ=L  → 4 Weyl  = ¿?
- **Colored part**: 2 (m₇ pair) × 2 (m₄ down-type) × χ=L, χ=R → ...
- **Colorless part**: (m₇ = 0) × 4 m₄ × ...

None of these naive assignments reproduces the exact SM count.

**Conclusion of the exploration**: a straightforward KK mode counting does not uniquely reproduce the SM fermion content. A refined framework is needed — most likely involving the specific embedding of the 4D chirality projector γ⁵ (Session 2, M1), which can project out half the naive Weyl dof and correlate isospin with color.

## 5. What we have definitively established

1. **SU(3) assignment is derived**: m₇ → Frobenius orbit → (1, 3, 3̄). This is rigorous (Paper IV §8.3).
2. **SU(2) doublet structure is a candidate**: the up-type {m₄ = 1, 2} and down-type {m₄ = 0, 3} CP orbits are natural doublet candidates, but the assignment of which orbit becomes a doublet vs two singlets is not yet derived.
3. **Hypercharge is NOT yet derived**: the formula Y = m/N works for the Higgs (Y_H = 1/2 at m₄ = 2) but does not obviously generalize to fermions with both m₇ and m₄ labels. A linear formula Y = α·m₇ + β·m₄ + γ may exist but is not yet constructed.
4. **The counting has an 8-Weyl discrepancy** that requires a structural resolution not yet given in Paper IV.

## 6. What requires further work (and what may need Session 2 input)

- **Chirality projection (Session 2, M1)**: before P1 can be completed, the γ⁵ action on KK modes must be made explicit. This determines which (m₇, m₄) modes give L vs R Weyl fermions — and likely projects out half, fixing the 56 → ~28 count.
- **Hypercharge formula**: may require a two-U(1) structure (one from each S¹ fiber) with a linear combination identified as Y.
- **Lepton embedding**: where does the colorless sector come from? Candidates: m₇ = 0 with 3 copies (one per generation), or a separate N-sector, or embedding via the SU(2) singlet content of a single m₇ pair combined with some projection.

## 7. Recommendation

Before completing Session 1, suggest:

(a) **Sequence Session 2 (M1, chirality) BEFORE finishing Session 1 (P1, fermion dictionary)**. The chirality projector γ⁵ determines fundamental mode counting, which is prerequisite to the dictionary.

(b) **OR** Gordon provides the intended framework for the lepton/colorless sector, so Session 1 can close without waiting for Session 2.

(c) **OR** Accept that P1 and M1 must be done together in an expanded "Session 1+2" scope, producing a joint chirality + dictionary derivation.

---

## Appendix: oracle verification

The oracle (`oracle.py`) verifies:
- SM reference generation satisfies all five anomaly traces (Tr Y, Tr Y³, Tr T₃²Y, Tr C_SU(3)·Y, Tr C_SU(3)³) exactly in `Fraction` arithmetic.
- Enumerates the 28 KK mode pairs (m₇, m₄) with SU(3) assignment from Frobenius orbits.

Once a candidate dictionary is locked, the oracle can be extended to verify anomaly cancellation over the proposed (m₇, m₄, χ) → (SU(3), SU(2), Y) map and assert whether the full 3-generation content of the theory is anomaly-free.
