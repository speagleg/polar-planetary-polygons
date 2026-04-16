# Session 1 joint P1 + M1 — findings after codebase + paper deep-dive

**Date**: 2026-04-16
**Status**: M1 complete. P1 blocked on a genuine structural gap in the paper series.

---

## 1. M1 (γ⁵ Clifford decomposition) — complete

**Result**: `γ⁵ = γ^(3) · γ³` is a fixed matrix identity (Weyl basis, signature +−−−). No KK-mode-dependent phase. Paper IV §8.1 Step 2 formula `γ⁵ → γ^(3) · e^{iπm}` is imprecise.

Artifacts:
- `M1-chirality/clifford_oracle.py` — sympy verification, exits 0
- `M1-chirality/derivation.md` — formal derivation + proposed Paper IV replacement language

This M1 result is ready for reviewer cycle independently.

---

## 2. P1 (KK → Weyl dictionary) — blocked by a genuine structural gap

### 2.1 What I found in the paper series

**Paper IV (field theory)**:
- §8 — gauge group derivation: SU(3) from Frobenius orbits on N=7, SU(2) from CS at N=4, U(1) from KK momentum.
- §13 — fermion mass structure: Yukawa texture from Z₇ charge conservation, three generations = three m₇ pairs {(1,6), (2,5), (3,4)}.
- §14.2 (line 3747–3755) — anomaly paragraph: *asserts* "each generation carries the standard SU(3)×SU(2)×U(1) quantum numbers" and "all gauge anomalies cancel per generation by the same arithmetic as in the Standard Model; the orbifold determines which modes form a generation, not what quantum numbers they carry." **This is the claim P1 was asked to derive. It is currently an assumption, not a derivation.**
- §16 — PMNS: neutrino mixing derived from pair-cosine matrix `m_ν = C^T diag(w) C` with three m₇ pairs. Theorem 16.4(d) *identifies* coordinate axes (e₁, e₂, e₃) with charged-lepton flavors (ν_e, ν_μ, ν_τ) — an *identification*, not a derivation, per the theorem statement itself.

**Paper V (cosmology), §23 "Neutrino masses from the seesaw"** (lines 1500–1585):
- ν_R is SU(2) singlet with N=4 KK mass μ_4 = 3/2.
- ν_L doublet has μ_4 = 1/2.
- Neutrinos organized by m_7 pair (1,6), (2,5), (3,4) — SAME pairs as quark generations.
- Dirac seesaw structure; ν_R Dirac mass is an *ansatz* determined by three physical inputs (eq. 1517–1529).

**Paper V, Corollary 4 ("Three generations from the Pell equation")** (lines 286–302):
> "Each pair (m, 7−m) for m = 1, 2, 3 is one generation... The Galois orbits O₊ and O₋ each contribute ONE ELEMENT PER PAIR, so n_gen = n_color = φ(7)/2 = 3."

### 2.2 The structural gap

The paper's implicit model:
- **3 generations = 3 m₇ pairs**: (1,6), (2,5), (3,4).
- Each pair contains one O₊ member (color **3**) and one O₋ member (color **3̄**).
- Neutrinos ALSO indexed by m₇ pairs (Paper V §23).

**Implication**: every m₇ mode in every generation carries non-trivial color. **Leptons live in m₇ pairs** that are supposedly non-trivially colored. This is internally inconsistent unless additional structure (not currently specified in the paper) decolors the lepton sub-sector.

**The counting problem remains**:
- 6 m₇ modes (all colored) × 4 m₄ modes × 2 chiralities = 48 Weyl (ignoring m₇ = 0).
- Per generation: 48 / 3 = 16 Weyl. ✓ matches SM+ν_R target.
- BUT per generation: all 16 would be colored (no lepton home).

**Where do leptons actually come from?** The paper does not explicitly say. Possibilities consistent with the sources I found:

| Option | Mechanism | Paper support | Obstruction |
|--------|-----------|---------------|-------------|
| **A** | Leptons at m₇ = 0 (3 copies per gen) | Structurally natural; consistent with Frobenius fixed point | Requires 3 copies of m₇ = 0 tower (no obvious geometric justification) |
| **B** | Color "decolors" for certain m₄ modes | Would give 8 colored + 8 colorless per pair (natural 16) | Paper's §8.3 derives color from m₇ orbit membership, not m₄ |
| **C** | Leptons are projections of colored modes via SU(2)-singlet combination in 3 ⊗ 3̄ | Group-theoretic natural | Not a fermion mechanism (singlet of 3⊗3̄ is a bilinear, not a linear field) |
| **D** | Leptons live on a separate polygon sector (e.g., a base Riemann surface of genus g with Dirac index 3) | `src/extensions/fermions_uv.py` mentions index = N/2 + (1−g) | Would require g=1 with N=8, or specific genus — not the main N=7 Seifert |
| **E** | The paper's implicit model is the *quarks only* and leptons are a separate, undeclared sector | — | Would mean the paper's "15 Weyl per generation" claim is unfinished |

### 2.3 What the codebase reveals

- `src/planetary_polygons/extensions/standard_model_gauge.py`: derives gauge group and sin²θ_W = 3/11. Does **not** enumerate fermion content.
- `src/planetary_polygons/extensions/fermion_masses.py`, `fermions_uv.py`: implements fermion KK spectrum, half-integer shift, chiral index of Dirac operator:
  - `index(D) = N/2 + (1 − g)` on genus-g Riemann surface base
  - For N=8, g=2: index = 3 (three generations!)
  - For N=7 (the main polygon): index = 7/2 + (1−g) — non-integer unless g fractional (impossible)
- `src/planetary_polygons/proofs/fermion_derivation.py`: derives Yukawa texture, mass hierarchy, CKM — **does not build the SU(3)×SU(2)×U(1) dictionary**.
- No file in the codebase computes the 5 SM anomaly coefficients from derived charges.

### 2.4 Honest assessment

1. **The paper series does not have an explicit, derived KK-mode → SM-fermion dictionary.** The §14.2 "standard quantum numbers" assertion is the weakest link P1 was asked to strengthen.
2. **The lepton sector embedding is UNDERSPECIFIED in the paper.** Paper V §23 writes a neutrino table indexed by m₇ pairs, but nowhere does the series derive *how* the colorless lepton content lives inside the colored m₇ pair structure.
3. **The Frobenius + pair framework gives 3 generations of QUARKS naturally.** It does NOT naturally produce the SM's 4 colorless Weyl per generation.
4. **The chiral-index formula `N/2 + (1−g)` in `fermions_uv.py` hints at a different structure** (compactification on a genus-g Riemann surface) that could give 3 generations via index theorem, but this is not obviously the main Seifert N=7 × S¹ geometry.

---

## 3. Options for Gordon

### 3.A. Accept that P1 is a genuine open problem for this paper series
Write the P1 derivation as far as possible (the colored sector is derivable) and honestly flag the lepton embedding as unresolved — following the plan's "Early Termination" clause when "multiple independent frameworks fail the same way."

### 3.B. Provide the intended lepton-sector mechanism
If you have a specific picture (one of options A–E above, or something else), state it and I'll build the derivation around it.

### 3.C. Defer P1 entirely; ship M1 alone
The M1 result (γ⁵ correction) is independently reviewable and fixes a real paper bug. Send it through physics-reviewer + math-reviewer now. Return to P1 in a later session with a clearer framework.

### 3.D. Open a separate research sub-session to construct the lepton-sector mechanism
Treat "lepton embedding in the polygon-pair framework" as a research problem in its own right. Build candidate frameworks, test each against SM anomalies, present best candidate for review. This is likely multi-session work.

---

## 4. What I recommend

**3.C** (ship M1) + **3.D** (open research sub-session for lepton embedding). Reasons:

1. M1 is a real correction to the paper and is self-contained. It should not wait for P1.
2. P1 as currently scoped is actually attempting to fill a gap that the paper series itself has not closed. It's a research problem, not an exposition problem.
3. The "17-session plan" assumed each issue had a known resolution just needing rigorous write-up. P1 / lepton embedding is different in kind — it's a missing derivation, not a rough derivation.
4. Separating M1 from P1 lets us get a clean reviewer signal on M1 while investigating P1 properly.

**Your call.**
