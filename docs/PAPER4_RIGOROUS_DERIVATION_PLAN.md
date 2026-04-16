# Paper IV Rigorous Derivation Plan

**Date**: 2026-04-16
**Directive**: No fitting, no hand-waving, no numerical coincidences, no retreating. Every claim rigorously derived.
**Scope**: Paper IV is the flagship physics paper. Every structural issue from both reviewers (math + physics) addressed via rigorous derivation, NOT by acknowledgement/retreat.

## Baseline State

- Math-reviewer: 6.8/10, 8 structural issues (some overlap with physics)
- Physics-reviewer: 4.8/10, 10 structural physics issues
- Convergent issues (both reviewers flag): 4
- Total unique structural issues: 11

## The 11 Structural Issues

### Convergent (both reviewers flag)

**C1. Warp factor σ unification** (math S1 / physics PS2)
- Problem: σ_geo = N, σ_CKM = N-2, σ_mass = (N-2)√N introduced via different arguments. RS factor-of-2 invoked but Seifert ≠ RS. The identity f((N-1)/2,N) + 1 = N at N=7 is a Diophantine coincidence used to relabel a fit.
- Required derivation: ONE coherent KK-reduction-on-Seifert-fiber calculation that produces the mass hierarchy. Every power of σ emerges from this calculation.
- If no single σ works: this reveals that σ-tower is phenomenological and must be demoted.

**C2. Topological mass vs physical W mass** (math S7 / physics PS1)
- Problem: Claimed topological masses m_L ~ 490 TeV, m_R ~ 107 TeV at Seifert scale. These are NOT the physical W/Z masses (~80-90 GeV from Higgs mechanism). Paper conflates them.
- Required derivation:
  - Compute topological mass rigorously from η-invariant
  - Separately, derive Higgs VEV and W mass via Higgs mechanism
  - Show relationship between the two scales (if any)
  - Justify why SU(2)_L identification with one chirality sector is derived, not chosen

**C3. D²_CS = Δ operator identity domain** (math S6 / physics PS5)
- Problem: Claimed universal, but only holds on Z_N-equivariant scalars. For matter in non-trivial representations, there are curvature/commutator terms.
- Required derivation:
  - State the identity precisely with domain restriction
  - For matter in representation R, work out [F, φ] and R-dependent corrections
  - Justify the f(m*,N) = C_2(j=1) = 2 coincidence from operator theory
  - Show whether this is a general pattern or specific to j=1

**C4. Quark mass K^n exponent selection** (math S5 / physics PS3)
- Problem: m_c gets K², m_u doesn't. Different exponents {n_q} = {2,4,6,2} for {b,s,u,c} introduced ad hoc.
- Required derivation:
  - Derive a SELECTION RULE that predicts which quark gets which K^n
  - Show this selection rule follows from gauge-invariance, symmetry, or topology
  - Verify the rule independently gives the observed mass hierarchy (not a fit)

### Physics-specific

**P1. KK-mode → Weyl-fermion dictionary** (PS7)
- Problem: The paper talks about "fermion pairs (m_7, m_4)" but doesn't explicitly write 15 Weyl fermions per generation with their SU(3)×SU(2)×U(1) quantum numbers.
- Required derivation:
  - Full table: (m_7, m_4) → (color rep × isospin × hypercharge)
  - Verify the 15 Weyl fermions of one SM generation are reproduced
  - Compute anomalies Tr(Y), Tr(Y³), Tr(T₃²Y), Tr(T₃YY) from the derived charges
  - Verify all vanish per generation

**P2. PMNS conjecture handling** (PS9)
- Problem: Z_7 fractions (6/7, 4/7, 1/48) for mixing angles reported with σ-level precision alongside proven θ₂₃=45° theorem. δ_CP = arctan√7 is in ~3σ tension with T2K/NOvA.
- Required derivation:
  - Option A: DERIVE Z_7 fractions from Klein quartic modular forms at CM point τ_0 = (1+i√7)/2 (currently labeled "open")
  - Option B: Demote to conjecture, remove from main claims
- δ_CP tension: acknowledge honestly

**P3. CKM selective correction** (PS10)
- Problem: Tree-level |V_cb| = 0.092 (100% off), "NLO instanton" corrects |V_ub| by factor 24 but not |V_cb|. Applies only where needed.
- Required derivation:
  - Selection rule: which CKM elements receive K^n corrections
  - Derive n for each element from winding number / topology
  - Show this SAME rule gives correct values for V_us, V_cb, V_ub without fitting

**P4. Graviton emergence rigor** (PS6)
- Problem: "Boundary T(z) has helicity +2" is a CFT statement, not a 4D Lorentz helicity statement. Weinberg-Witten theorem dismissed without proof.
- Required derivation:
  - Compute 4D graviton 2-point function from boundary ⟨TT⟩ + KK lift
  - Demonstrate pole at k²=0 with tensor polarizations
  - Resolve Weinberg-Witten issue explicitly

### Math-specific

**M1. γ⁵ Clifford decomposition** (S3)
- Required: explicit computation showing γ⁵ = γ⁰γ¹γ²γ³ action on KK modes on H² × S¹. Verify the claimed e^{iπm} factor.

**M2. Fiber = S¹ uniqueness proof** (S4)
- Required: tighten the proof. The current spectral argument doesn't rule out non-round S¹ metrics, orbifold circle quotients, or accidentally-matching homogeneous spaces. Need either a precise uniqueness theorem or honest demotion to "motivating argument."

**M3. N = 11 = 4 + 7 additivity** (S2)
- Required: either pull the Paper VI argument into Paper IV or strengthen the local claim. Currently deferred.

## Execution Plan

### Phase 1: Foundation (Sessions 1-5)

**Session 1**: P1 — KK-mode → fermion dictionary
- Full table of 15 Weyl fermions per generation
- Derive SU(3)×SU(2)×U(1) quantum numbers from polygon data
- Verify anomaly cancellation from derived charges
- Deliverable: new section or subsection with the explicit dictionary

**Session 2**: M1 — γ⁵ Clifford decomposition
- Explicit computation of γ⁵ on H² × S¹
- Verify the claimed e^{iπm} factor
- Connect to 4D chirality projection

**Session 3**: C3 — D² operator identity domain
- Precise statement with domain
- Work out [F, φ] for matter in non-trivial rep
- Derive j=1 coincidence from first principles

**Session 4-5**: C1 — Warp factor σ unification
- Single KK-reduction on Seifert fiber
- Derive mass hierarchy from one σ
- Verify m_c, m_b, m_s, m_u, m_d via the derived structure
- If no single σ works: admit phenomenology, revise claims

### Phase 2: Selection rules (Sessions 6-8)

**Session 6**: C4 — Quark mass K^n exponents
- Derive selection rule from gauge invariance
- Verify all 4 quarks (u, d, s, c, b, t) from the rule
- If selection rule doesn't work: revise mass formulas, admit where derivation stops

**Session 7**: P3 — CKM correction selection rule
- Derive n_ij for each CKM element
- Verify V_us, V_cb, V_ub, V_cd, V_td from the rule
- Connect to winding number / topological interpretation

**Session 8**: C2 — Topological mass vs physical W mass
- Separate computations: topological (η-invariant) and physical (Higgs)
- Derive the relationship (if any)
- Justify SU(2)_L assignment via explicit chirality matching
- Or remove the topological mass identification if it doesn't match SM

### Phase 3: Harder derivations (Sessions 9-14)

**Session 9-10**: P4 — Graviton emergence
- Compute boundary ⟨TT⟩ 2-point function
- KK lift to 4D
- Verify pole structure k²=0 with correct polarizations
- Resolve Weinberg-Witten

**Session 11-12**: P2 — PMNS fractions
- Attempt: derive 6/7, 4/7, 1/48 from Klein quartic modular forms at τ_0
- If successful: new theorem replacing Conjecture 16.6
- If unsuccessful: demote to conjecture, remove from main claims
- Address δ_CP vs T2K/NOvA tension honestly

**Session 13**: M2 — Fiber = S¹ uniqueness proof
- Tighten the proof using spectral geometry theorems
- Rule out non-round metrics, orbifold quotients, accidental matches
- Or demote to motivating argument

**Session 14**: M3 — N = 11 = 4 + 7 additivity
- Pull Paper VI argument into Paper IV
- Or strengthen the local Paper IV claim

### Phase 4: Integration and review (Sessions 15-17)

**Session 15**: Dispatch math-reviewer, physics-reviewer after all fixes
**Session 16**: Address any new issues from triangulation review
**Session 17**: Final polish and minor fixes

## Expected Outcomes by Phase

- **After Phase 1**: Paper IV 4.8 → 6.5 (foundation solid)
- **After Phase 2**: 6.5 → 7.5 (selection rules derived)
- **After Phase 3**: 7.5 → 8.5 (harder items resolved)
- **After Phase 4**: 8.5 → 9.0+ (fully rigorous)

## Early Termination Conditions

**Commit to honest framing only if**:
- A specific derivation (e.g., PMNS fractions) is genuinely open research
- Multiple independent frameworks fail the same way (exhaustion argument like Paper III c = 12b(N))

**Do NOT retreat if**:
- The derivation requires more math we haven't tried
- The first attempt fails but alternative approaches exist
- Physical intuition suggests the result should hold

## Total Estimate

**17 sessions** for complete rigorous derivation of Paper IV.

Per session: 2-3 hours of focused work on one technical problem.

Assumption: some of these will take LONGER (PMNS fractions, graviton emergence are deep). If a session runs long, it runs long — no cutting corners.

## First Step

Commit to Session 1: P1 KK-mode → fermion dictionary. This is the foundation — without it, no later derivation is airtight.

**Request Gordon's approval before beginning.**
