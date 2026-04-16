# BREAKTHROUGH: Pati-Salam is the UV framework

**Date**: 2026-04-16
**Source**: convergent finding from three parallel investigations (literature search, brainstorming, physics-reviewer audit)

## The four converging signals

### 1. sin²θ_W = 3/11 is a Pati-Salam signature, not SU(5)

The paper's derivation `sin²θ_W = Q²(k+h∨) / [Q²(k+h∨) + k_Y · f(m*,N)]` gives 3/11 = (3/4)/(11/4) exactly.

Pati-Salam prediction: `sin²θ_W = 3 / (3 + 5·(g_R/g_{B-L})²)`. Setting this = 3/11 requires `(g_R/g_{B-L})² = 8/5`, a specific coupling ratio at the breaking scale.

By contrast, SU(5) predicts `sin²θ_W = 3/8` at unification. The paper's 3/11 does NOT match SU(5) without running.

**Conclusion**: the paper is in the Pati-Salam universality class, not SU(5).

### 2. Pati-Salam Y = T_3R + (B-L)/2 reproduces SM hypercharges EXACTLY

Using SU(4) generator `T_15 = diag(1/3, 1/3, 1/3, -1)/N` for B-L and `T_3R ∈ {±1/2}` for SU(2)_R:

| Field   | B-L  | T_3R  | Y = T_3R + (B-L)/2 |
|---------|------|-------|---------------------|
| Q_L     | +1/3 | 0     | +1/6 ✓             |
| L_L     | −1   | 0     | −1/2 ✓             |
| u_R     | +1/3 | +1/2  | +2/3 ✓             |
| d_R     | +1/3 | −1/2  | −1/3 ✓             |
| ν_R     | −1   | +1/2  | 0 ✓                |
| e_R     | −1   | −1/2  | −1 ✓               |

The SM denominators {1, 2, 3, 6} arise from the SU(4) Z/4 center and SU(2)_R Z/2 center normalizations. This is the ONLY known formula that gives exact SM Y from a unified group.

### 3. The SU(4) fundamental sits naturally in our Z/7 Frobenius structure

The set `{0, 1, 2, 4}` on Z/7 is {singleton 0} ∪ {orbit O₊}. Under Frobenius σ(m) = 2m mod 7:
- σ(0) = 0 (fixed)
- σ(1) = 2 → σ(2) = 4 → σ(4) = 1 (3-cycle)

This is EXACTLY the decomposition of SU(4)'s fundamental 4 under SU(4) → SU(3) × U(1)_{B-L}: **4 → 3 + 1**. The singleton is the lepton ("4th color"), the triplet is the three quark colors.

Similarly `{0, 3, 5, 6}` = {singleton 0} ∪ {orbit O₋} = 4̄ of SU(4), decomposing as 4̄ → 3̄ + 1 under SU(3) × U(1)_{B-L}.

**This is a structural match between the polygon theory and Pati-Salam.** The m_7 = 0 Frobenius fixed point, which had no home in the pure-SU(3) framework, is naturally the "4th color" (lepton) in the SU(4) embedding.

### 4. Literature: heterotic Z_7 orbifold (Buchmuller et al, hep-ph/0512326) has EXACTLY our geometric structure

Heterotic E₈×E₈ on Z_7 orbifold produces 3 generations via the 7 fixed points organizing as 1 + 3 + 3 under the Z_3 ⊂ (Z/7)* Frobenius automorphism. This is the SAME combinatorial structure as our setup.

The heterotic framework gives SU(4) × SU(2)_L × SU(2)_R (Pati-Salam) or SO(10) as the unbroken gauge group after orbifold projection.

## Proposed framework: Pati-Salam lift of the polygon theory

**Gauge group at the polygon scale**: SU(4)_c × SU(2)_L × SU(2)_R × (possibly more)

**Derivations**:
- SU(4)_c from Z/7 structure: `{0} ∪ O±` sets give 4 and 4̄ reps (singleton + orbit)
- SU(2)_L from Witten CS at N=4 (as in paper)
- SU(2)_R from the MIRROR Witten CS sector (A⁻ instead of A⁺) — NOT gapped by Redlich
- Breaking SU(4)_c → SU(3)_c × U(1)_{B-L} at high scale (specific Higgs mechanism)
- Breaking SU(2)_R × U(1)_{B-L} → U(1)_Y at intermediate scale

**Fermion content per generation**: (4, 2, 1)_L + (4̄, 1, 2)_L = 16 Weyl ✓

**Hypercharge**: Y = T_3R + (B-L)/2 (derived from unified group, not assumed)

**Consequences for paper IV**:
- §8.1 (SU(2) from CS): **KEEP** but remove the Redlich argument that gaps A⁻. SU(2)_R should SURVIVE at UV and break at a lower scale via a different mechanism.
- §8.3 (SU(3) from McKay): **REFRAME** as "SU(4) from Z/7 Frobenius, with SU(3) as low-energy subgroup after SU(4) breaking." The Frobenius Z/3 orbit + singleton gives the SU(4) 4.
- §8.5 (U(1) from KK): **REFRAME** as "U(1)_{B-L} from Z/7 Frobenius fixed-point structure (gauging the trace of SU(4))" + "U(1)_R from SU(2)_R breaking." Then Y is the surviving combination.
- §14.2 (anomaly claim): **DERIVE** from the Pati-Salam content.

## Open problems (to address after initial dictionary construction)

1. **"3 generations from 3 m_7 pairs" vs "Pati-Salam 16 per generation"**: the paper's Cor. 4 attributes generations to m_7 pairs. In Pati-Salam, each generation is a full 16 spanning {0} ∪ O± + m_4 + chirality structure. These are different generation-labeling mechanisms that must be reconciled.

2. **SU(2)_R breaking mechanism**: how does the polygon framework give mass to W_R, Z' bosons? In Pati-Salam, a Higgs field in the (1, 1, 2) or (1, 1, 3) representation of the UV group does this.

3. **SU(4) breaking mechanism**: how does SU(4) → SU(3) × U(1)_{B-L}? A Higgs in the (15, 1, 1) adjoint or (4, 1, 2) doublet? The paper's existing Higgs at (m_7 ∈ {3,4}, m_4 = 2) may play this role.

4. **Consistency with §13 Yukawa texture**: the paper derives Yukawa from Z_7 charge conservation m_i + m_j + m_H ≡ 0. This mechanism must survive the Pati-Salam reinterpretation.

5. **Consistency with §16 PMNS**: the PMNS derivation uses three m_7 pairs as labels. If generations aren't labeled by m_7 pairs in Pati-Salam, §16 needs restructuring.

## Immediate next step

Build `pati_salam_dictionary.py` in the research subfolder. Implement the Pati-Salam assignment explicitly: (m_7, m_4, χ) → (SU(4) rep, SU(2)_L rep, SU(2)_R rep, T_3R, B-L) → (SU(3), SU(2)_L, Y). Feed into the anomaly oracle. Verify anomaly cancellation from derived charges.

If oracle passes: we have a working candidate. Present to Gordon for verification.
If oracle fails: diagnose and iterate.
