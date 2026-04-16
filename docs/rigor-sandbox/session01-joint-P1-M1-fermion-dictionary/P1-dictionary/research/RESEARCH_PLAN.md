# P1 research sub-session: lepton embedding

**Date opened**: 2026-04-16
**Status**: active
**Scope**: find the correct derivation of the full SM fermion content (including leptons) from the polygon framework on R × (H² ×_7 S¹) ∪ (N=4 sector).

## The problem

Paper series (especially Paper IV §8/§13/§16, Paper V §23) establishes:
- **Quark content**: three generations, one per m₇ pair (1,6), (2,5), (3,4); each pair has 1 O₊ (color **3**) + 1 O₋ (color **3̄**).
- **Neutrino content**: indexed by the same m₇ pairs as quarks (Paper V §23).
- **SU(2)/U(1)**: doublet/singlet structure from m₄ modes and KK momentum charge.

But nowhere in the series is it derived how the COLORLESS lepton Weyl fermions (L_L, e_R^c, ν_R^c — 4 per generation) fit inside the KK tower. The naive count of m₇ pairs gives only colored content.

## Candidate frameworks to test

### F1. "m_4-decoloration" — different m_4 modes carry different SU(3) assignments

*Hypothesis*: For the SAME m_7 ∈ O₊, the SU(3) representation depends on m_4. Specifically, m_4 modes in the "up-type" class {1, 2} carry the standard 3 of SU(3); m_4 modes in the "down-type" class {0, 3} carry the SU(3) singlet.

*Consistency with paper*: §13.3 says "up-type μ_4 = 1/2 vs down-type μ_4 = 3/2" for fermions. The MASS differs; this framework would extend the distinction to the SU(3) rep.

*Test*:
- Count per generation: 2 m_7 (pair) × 2 m_4_up × 2 χ × color_dim(3) = 24 colored Weyl per pair. TOO MANY.
- Count per generation: 2 m_7 × 2 m_4_down × 2 χ × color_dim(1) = 8 colorless Weyl per pair. TOO MANY.
- Ratio wrong (24 colored : 8 colorless ≈ 3:1, SM is 12:4 = 3:1 ✓ actually).
- Multiply by generations = 3: 72 colored, 24 colorless. SM: 36 colored, 12 colorless. Factor of 2 off.

Result: RATIOS match (3:1), but magnitudes are 2× too many. Requires a projection (chirality-lock?) to halve. Plausible.

### F2. "Klein-quartic multiplet" — PSL(2, F₇) representation theory

*Hypothesis*: Fermion content decomposes under Aut(X(7)) = PSL(2, F₇). Its irreps: {1, 3, 3̄, 6, 7, 8}. SU(3) embeds via χ_3 ⊗ χ̄_3 = χ_1 ⊕ χ_8 (Paper IV §8.3). Leptons and quarks live in DIFFERENT PSL(2, F₇) irreps.

*Candidates for lepton sector*: χ_1 (singlet, 1 Weyl per copy), χ_6 (6 Weyl per copy), χ_7 (7 Weyl per copy).

*Test*: need 4 colorless Weyl per generation × 3 generations = 12 colorless Weyl total. Options:
- 3 × χ_1 = 3 Weyl total. Too few (need 12).
- 2 × χ_6 = 12 ✓ in total count; but unclear decomposition into 3 generations × 4 Weyl.
- 12 × χ_1 = 12 — needs 12 copies.

### F3. "Pati–Salam SU(4)" — lepton as fourth color

*Hypothesis*: The theory is effectively SU(4) color × SU(2)_L × SU(2)_R at a higher scale, breaking to SM. Leptons = "4th color" in the SU(4) fundamental.

*Consistency with paper*: The paper derives SU(3), not SU(4). But maybe SU(4) is the UV structure and SU(3) the IR after breaking.

*Test*: SU(4) × SU(2) × SU(2) per generation content is (4, 2, 1) + (4̄, 1, 2) = 16 Weyl ✓. Decomposes to SM+ν_R under SU(4) → SU(3) × U(1)_{B-L} exactly.

Need to derive SU(4) from polygon. Obstruction: (Z/7)* doesn't have a Z/4 subgroup (only Z/2, Z/3, Z/6). So Frobenius-based SU(4) is not automatic.

### F4. "Genus-based generation counting" — chiral index on higher-genus base

*Hypothesis*: Compactify on a genus-g Riemann surface base. Chiral index `index(D) = N/2 + (1−g)` (from `src/extensions/fermions_uv.py`). For 3 generations, need index = 3.

*Test*: N/2 + (1−g) = 3 gives N + 2(1−g) = 6, so (N, g) ∈ {(4, 0), (6, 1), (8, 2), (10, 3), ...}.
- N=4, g=0 sphere: isospin sector base.
- N=8, g=2 Bolza surface: unusual; Bolza is paper III's g=2 surface.

*Consistency with paper*: N=7 is the main polygon, but chiral index at N=7 is non-integer for integer g. Either the framework requires g NOT integer, or uses a DIFFERENT N for fermion index.

### F5. "Orbifold twisted sectors" — leptons from twisted modes

*Hypothesis*: The Z_7 orbifold has N−1 = 6 twisted sectors (DHVW twist fields). Quarks live in the untwisted sector; leptons live in twisted sectors.

*Test*: Each twisted sector has localized states at orbifold fixed points. The number of twisted-sector Weyl fermions per sector is determined by the orbifold action.

*Obstruction*: The DHVW twist fields in Paper IV are bosonic (scalar OPE coefficients). Whether they carry fermionic content requires additional structure.

### F6. "Extended chiral algebra" — boundary CFT hosts fermion content

*Hypothesis*: The boundary 2D CFT at c = 12 b(N) on the Seifert hosts the fermion content via some chiral algebra decomposition. Gauge-invariant fermion bilinears or spin-structure content of the boundary provides the leptons.

*Obstruction*: The boundary CFT is c ≈ 51.6 at N=7 — that's a LOT of central charge, plenty of room for SM matter. But identifying specific SM fermions with specific boundary states is non-trivial.

### F7. "Three copies of m_7 = 0" — lepton tower at the Frobenius fixed point

*Hypothesis*: The m_7 = 0 mode has 3-fold multiplicity from some structural reason (e.g., 3 SPHERICAL MODES on the H² base at fixed m_7).

*Test*: Chiral index of Dirac on H² (or its quotient) at m_7 = 0 — if this gives 3 zero modes, it matches. For H² ITSELF (non-compact, not Γ-quotiented), zero modes are infinite in number (continuous spectrum). For H²/Γ with Γ = Γ(7) acting on Klein quartic, the Dirac zero modes are FINITE and determined by the genus g = 3 of X(7). Genus-3 surface has Dirac zero modes counted by Riemann-Roch: index = deg(L) − g + 1 for a line bundle L. For spin-bundle on g=3: index = 3 − 3 + 1 = 1... not 3.

### F8. "Auxiliary fiber bundle" — leptons from a SEPARATE S¹ or Seifert

*Hypothesis*: In addition to the main H² ×_7 S¹ Seifert, the theory has a second fiber bundle (e.g., a g=2 base or another orbifold) that hosts the lepton sector.

*Obstruction*: Significant additional structure; not clearly motivated by the paper.

---

## Plan of attack

1. **Phase A**: Build a unified oracle that, for each framework, generates the implied fermion content as a list of Weyl fermions with (SU(3), SU(2), Y) charges, and checks:
   - Total Weyl count per generation = 16
   - All 5 SM anomaly traces vanish
   - Consistency with paper's Higgs/Yukawa/PMNS structure

2. **Phase B**: Systematically test frameworks F1–F8. Eliminate those failing counting or anomaly.

3. **Phase C**: If one framework survives: build a full derivation proof in `derivation.md`. Present to Gordon.

4. **Phase D**: If multiple frameworks survive: present ranked alternatives to Gordon with trade-offs. Choose based on consistency with paper's other derivations.

5. **Phase E**: If NONE survive: document the exhaustion honestly and consult on whether this is a genuine open problem.

## First concrete task

Build `frameworks_oracle.py` that encodes each framework F1–F8 as a function `(N, g, orbit_data) → List[WeylFermion]` and uses the existing anomaly checker from `../oracle.py` to test each. Report pass/fail.

## Open structural questions to resolve along the way

- Does the paper's derivation of `sin²θ_W = 3/11` depend on specific lepton hypercharges? (Yes — implicit in Tr(Y²) or similar.)
- Does the proton-stability argument in §14.2 (line 3757) assume 3 colored generations and implicitly constrain the lepton content?
- What's the relationship between the Higgs modes (m_7 = 3, 4 pair 3) and the top generation in the same pair? If they're co-located, does this constrain the lepton assignment?

These questions must be answered incrementally as we work through the frameworks.
