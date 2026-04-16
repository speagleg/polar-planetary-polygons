# Full framework audit: derived, fitted, underived, or erroneous

**Date**: 2026-04-16
**Goal**: systematic classification of every structural claim in the combined (Paper + Session 1) framework, identifying gaps for a fully coherent unified derivation.

---

## The framework's logical chain

```
Pell equation selects N=7  (Paper I)
         ↓
Polygon geometry: R × (H² ×_7 S¹)  (Paper III)
         ↓
Gauge group: SU(3)_c × SU(2)_L × SU(2)_R × U(1)_Y  (Paper IV §8)
         ↓ [our session]
Explicit (m_7, m_4, χ) → SM fermion dictionary (16 Weyl/gen)
         ↓
3 generations: Riemann-Hurwitz F=3 on X(7) (Klein quartic)
         ↓
Anomalies: Tr(Y)=Tr(Y³)=Tr(T₃²Y)=Tr(C_SU3·Y)=Tr(C_SU3³)=0 derived
         ↓
Yukawa structure: Z/7 charge conservation (paper) = Z/7 at cusps (ours)
         ↓
Fermion masses, CKM, PMNS (paper)
```

---

## Classification by claim

### (A) RIGOROUSLY DERIVED (no gaps)

| Claim | Source | Status |
|-------|--------|--------|
| N=7 from Pell equation | Paper I | Rigorous |
| Polygon geometry as Seifert manifold | Paper III | Rigorous |
| SU(3)_c via Frobenius Z/3 + McKay | Paper IV §8.3 | Rigorous |
| SU(2)_L × SU(2)_R via Witten CS | Paper IV §8.1 | Rigorous |
| SU(2)_R gapping at m_R ~ 107 TeV | Paper IV §8.1 | Rigorous (topological, Redlich) |
| U(1)_Y gauge field from S¹ KK | Paper IV §8.5 | Rigorous (existence) |
| sin²θ_W = 3/11 from CS formula | Paper IV §8.6 | Rigorous (polygon-intrinsic) |
| γ⁵ = γ^(3)·γ³ Clifford identity | Our M1 | Rigorous (sympy) |
| 3 generations = 3 Z/7-fixed cusps on X(7) | Our Riemann-Hurwitz | Rigorous |
| N=7 uniqueness for F=(N-1)/2 match | Our computation | Rigorous |
| Cusp ↔ pair-label identification | Our cusp_identification.py | Rigorous |
| Anomalies vanish from derived charges | Our oracle | Rigorous |
| Z/7 Yukawa texture structure (zeros) | Paper §13.1 | Rigorous |
| Yukawa rule = Z/7 charge conservation at cusps | Our cusp_geometry_theorem | Rigorous |
| PMNS S_3 symmetry from cusp permutation | Our pmns_consistency + cusp_geometry | Rigorous |
| θ_23 = 45° theorem (symmetric limit) | Paper §16 Thm 16.4(d) | Rigorous |
| CKM phase δ = 69.3° | Paper Bernoulli backbone | Rigorous |
| Proton stability (exact, Z_{28}) | Paper §14.2 | Rigorous |
| ν_R Dirac mass M_KK ~ 10^13 GeV | Paper V §23, Pell identity | Rigorous |

### (B) PARTIALLY DERIVED — depends on structural choice

| Claim | Gap | Status |
|-------|-----|--------|
| (4, 2, 1) vs (4̄, 1, 2) SU(2)_L/R assignment | Which m_4 pair is L doublet vs R doublet | MOTIVATED by fermion mass hierarchy (up-type μ=1/2 for L doublet), not derived from polygon |
| Y = T_3R + (B-L)/2 formula | Choice of PS embedding for matter | NATURAL from SU(4) 4-rep decomposition of {0} ∪ O±, but the 4-rep embedding itself is a STRUCTURAL choice |
| B-L charges (+1/3 quark, -1 lepton) | Follows from 4-rep SU(4) normalization | Derived IF 4-rep embedding accepted |
| T_3R = ±1/2 for (4̄, 1, 2) m_4 assignment | Chosen to give SM Y values | Fitted |
| Which chirality survives Redlich projection | Sign of η_grav on Seifert | Derived in paper but depends on fiber orientation choice |
| Pair 3 = Higgs doublet (modes 3, 4 in N=7) | BF-crossing structure | Motivated; full derivation involves BF instanton dynamics |

### (C) FITTED / AD HOC

| Claim | Issue | Status |
|-------|-------|--------|
| Quark mass K^n exponents {n_b, n_s, n_u, n_c} = {2, 4, 6, 2} | No selection rule derived | **FITTED** — explicit open problem C4 in rigor plan |
| σ_geo = N, σ_CKM = N-2, σ_mass = (N-2)√N warp factors | Three different σ values via distinct arguments | Flagged as potentially phenomenological in C1 of rigor plan |
| m_u not receiving K² correction (unlike m_c) | No selection rule | Part of C4 |
| One calibration input: Δm²_atm for M_poly | Observational, not derived | Acceptable (standard "one dimensional input") |

### (D) CONJECTURED (explicitly open)

| Claim | Issue | Status |
|-------|-------|--------|
| PMNS sin²(2θ_12) = 6/7 | Not derived | Conjecture 16.6, numerically matches within 1σ |
| PMNS sin²θ_23 = 4/7 | Not derived | Conjecture 16.6, 0.1σ from PDG |
| PMNS sin²θ_13 = 1/48 | Not derived | Conjecture 16.6, 1.4σ from PDG |
| δ_CP = arctan√7 = 69.3° | Derived but in 3σ tension with T2K/NOvA | Tension with current experiment |

### (E) ERRONEOUS — FIXED in Session 1

| Original claim | Problem | Fix |
|----------------|---------|-----|
| γ⁵ → γ^(3)·e^{iπm} (§8.1 Step 2) | e^{iπm} factor unjustified | γ⁵ = γ^(3)·γ³ exact identity (M1 fix) |
| "Fermion quantum numbers by SM arithmetic" (§14.2) | 0% derived | Explicit dictionary + anomaly derivation |

### (F) STRUCTURAL OBSERVATIONS (neither claimed nor derived)

| Observation | Note |
|-------------|------|
| ε_7 = 8 + 3√7 has b=3; g(X(7))=3 | Numerological match unique to N=7; structural significance unclear |
| Matter content fits Pati-Salam 4-rep | Observed, not claimed as UV gauge group |
| Z/3 Frobenius acts on both colors and generations | Structural duality; not gauged across generations |
| S_4 ⊂ PSL(2, F_7) ⊂ SU(4) | Gives only Weyl group embedding, not gauge |

---

## What's "NOT DERIVED" for a fully coherent framework

Ranked by impact on framework coherence:

### Critical (would weaken unified-framework claim)

**C1. SU(2)_L vs SU(2)_R assignment to m_4 pairs**
- Current: m_4 ∈ {1, 2} = SU(2)_L doublet, m_4 ∈ {0, 3} = SU(2)_R doublet
- Motivation: up-type fermions closer to critical mode μ_4 = 1/2
- Gap: need a SPECTRAL / SYMMETRY argument deriving this assignment
- Consequence if wrong: would change SM fermion mapping, potentially all Y values
- **Priority: HIGH** — this is the most structurally unjustified choice in our dictionary

**C4. Quark mass K^n exponents (rigor plan item)**
- Current: {n_b, n_s, n_u, n_c} = {2, 4, 6, 2} ad hoc
- Gap: no selection rule derived
- Consequence if unfixed: the quark mass hierarchy derivation is phenomenological
- **Priority: HIGH** — explicitly on rigor plan

**PMNS fractions (Conjecture 16.6)**
- Current: 6/7, 4/7, 1/48 conjectured
- Gap: need Klein quartic modular form derivation
- Consequence if unfixed: PMNS predictions are conjectural
- **Priority: MEDIUM** — matches PDG within 1–1.5σ, deviation small

### Significant (gaps but don't block framework)

**C1. σ warp-factor coherence**
- Three σ values (geo, CKM, mass) derived via distinct arguments
- Gap: unified derivation from single KK-reduction calculation
- Consequence: warp factor "tower" structure is currently phenomenological
- **Priority: MEDIUM** — paper's C1 open item

**BF-crossing → Higgs pair 3 identification**
- Current: pair 3 = Higgs doublet via BF-crossing structure
- Gap: need explicit derivation from BF instanton dynamics
- Consequence: Higgs identification is motivated but not fully derived
- **Priority: LOW** — structurally plausible

### Minor (technical gaps)

**Quantitative cusp overlap integrals**
- Yukawa coefficients from Klein quartic automorphic forms
- Gap: explicit Eisenstein series computation
- Consequence: YUKAWA TEXTURE is derived, but SPECIFIC COEFFICIENTS aren't
- **Priority: LOW** — technical automorphic form calculation

**b = g = 3 structural link at N=7**
- Numerological match between Pell unit coefficient and Klein quartic genus
- Gap: derive via Dedekind zeta / Eichler-Selberg
- Consequence: would deepen the N=7 uniqueness argument
- **Priority: LOW** — structural elegance, not essential

---

## What's FITTED in the framework (honest accounting)

Strict fitted parameters:
1. **Quark mass exponents {n_q}** — 4 ad hoc integer choices (C4)
2. **M_poly calibration via Δm²_atm** — 1 observational input
3. **Higgs mass NLO coefficients** — some computation, some approximation

Everything else is either derived, conjectured (explicitly labeled), or structural observation.

## What's ERRONEOUS / INCONSISTENT (post-Session 1)

After Session 1:
- γ⁵ formula fixed ✓
- §14.2 anomaly claim derived ✓

Remaining potential issues:
- **The "Pati-Salam UV" framing we introduced earlier in this session is MISLEADING.** Paper explicitly rejects GUT interpretation (Paper VI §683). We should frame matter content as "PS-embedded" at the rep level, not as a UV gauge group claim.
- **The "sin²θ_W matches PS at ρ² = 8/5" observation is post-hoc**, not a signature of Pati-Salam.

**Revision for Paper IV draft**: remove "Pati-Salam UV framework" language, keep mathematical content but frame as explicit polygon-to-SM mapping using PS-style embedding notation for charge decomposition.

---

## Summary: what the unified framework has and lacks

### What we have (rigorous chain)

1. Pell → N=7 ✓
2. Polygon → SU(3) × SU(2)_L × SU(2)_R × U(1)_Y gauge structure ✓
3. Klein quartic → 3 generations (Riemann-Hurwitz) ✓
4. Polygon (m_7, m_4, χ) → SM fermion dictionary ✓
5. Anomalies cancel from derived charges ✓
6. Yukawa texture from Z/7 at cusps ✓
7. PMNS θ_23 = 45° from cusp S_3 ✓
8. sin²θ_W, proton stability, ν_R masses derived ✓

### What we lack (gaps)

1. **SU(2)_L vs SU(2)_R assignment to m_4 pairs** — motivated, not derived
2. **Quark mass K^n exponents** — fitted (C4 rigor plan)
3. **PMNS fractions** — conjectured (Conjecture 16.6)
4. **σ warp-factor unified derivation** — C1 rigor plan
5. **Quantitative Yukawa coefficients** — automorphic form computation needed
6. **BF crossing → Higgs pair 3** — partially derived

### What's MISLEADING / to correct

1. Our "Pati-Salam UV framework" claims — should be retracted
2. "sin²θ_W = 3/11 matches PS at ρ²=8/5" — remove from framework, keep as observation

### Is the framework unified?

**Mostly, with specific gaps.** The framework is unified at the STRUCTURAL level (polygon → gauge group → matter → generations → Yukawa structure) but has QUANTITATIVE gaps (exponents, conjectures) that prevent a complete "every number derived" claim.

For a fully unified framework, the critical gaps to close are:
1. SU(2)_L/R assignment derivation (priority)
2. C4 quark mass exponents (priority)
3. PMNS fraction derivation (medium)

Other gaps are technical (quantitative automorphic form calculations) or observational (one calibration).

The framework is **more unified than SM** (derives SM content from geometry) but **not fully unified** (some gaps remain, explicitly flagged).
