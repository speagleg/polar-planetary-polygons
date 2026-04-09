# Paper IV: CKM/PMNS Rewrite — Spec 3B of 4

## Goal

Replace the Plancherel-based CKM derivation in Paper IV with the Gauss sum derivation from the Bernoulli backbone. Add PMNS section. Update the Yukawa texture to orbit-based generation assignment. Add the instanton K^(N-1) proof for V_ub.

## Scope

Paper IV Section 12 "The fermion mass structure" (lines 2325-3244) gets a structural rewrite. Specifically:

### Subsections to REWRITE

**12.1 Yukawa texture (line 2375):**
- Replace pair-based generation assignment with Frobenius orbit assignment
- Up L = QR = {1,2,4}, Down L = QNR = {3,5,6}
- Higgs = {3,4}
- Keep the Z_7 selection rule (same formula, different mode assignment)
- New texture: anti-diagonal [0,*,*; *,*,0; *,0,0] (rank 3)
- State and prove (YY†)₀₂ = 0 from the texture

**12.3 Fermion mass hierarchy (line 2418):**
- Replace c = sqrt(mu7² + mu4²) with c = 1/2 + lambda/N
- Add the two-scale sigma: sigma_CKM = 5, sigma_mass = 5*sqrt(N)
- Update mass predictions: mt, mb, mc, mu within 7%
- Note the isospin shift 1/N for down-type quarks

**12.4 CKM phase (line 2603):** FULL REPLACEMENT
- Remove the 6-step Plancherel derivation entirely
- Replace with the Gauss sum chain:
  1. B_6 = 1/42 → von Staudt-Clausen → 7 | denom(B_6) → N=7
  2. QR(7) = {1,2,4} (quadratic residues = Frobenius orbit)
  3. Gauss sum G(QR) = (-1+i√7)/2
  4. Sector amplitude alpha_2 = 1 + G(QR) = (1+i√7)/2
  5. delta_CKM = arg(alpha_2) = arctan(√7) = 69.3°
- State sin²(delta) = N/(N+1) = 7/8 as an exact identity
- Reference Paper I Theorem (von Staudt-Clausen)

**12.5 CKM mixing angles (replaces "Non-perturbative CKM" at line 2771):**
- LEFT rotation: V = U_L_up† * U_L_down from YY† (not Y†Y)
- Bernoulli instanton phases: aL=1/7, aR=5/42, aH=2/21
- State all 5 CKM predictions: delta, s12, s23, s13, J
- The instanton correction for V_ub:
  - Theorem: (YY†)₀₂ = 0 (no direct 1-3 mixing)
  - Winding number argument: w_total = N-1 = 6
  - Selectivity: only V_ub corrected, not V_us or V_cb
  - Formula: s13 = s13_tree * K^(N-1)

### Subsections to ADD (new)

**12.6 PMNS neutrino mixing (NEW):**
- CKM-PMNS complementarity: theta_12^CKM + theta_12^PMNS = pi/4
  - From arctan(1/2) + arctan(1/3) = pi/4 (index-2 and index-3 subgroups)
- theta_23^PMNS = pi/4 (pair symmetry of index-2 subgroup)
- sin²(theta_13^PMNS) = (1/2)sin²(theta_C) (index-2 factor)
- delta_CP^PMNS = arctan(√7) (same Gauss sum)
- Testable prediction: DUNE and Hyper-K will measure delta_CP^PMNS

### Subsections that DON'T change

**12.2 The 2+1 mass pattern (line 2392):** Keeps its exact tree-level ratio.
**12.5+ onwards (Higgs mass, etc.):** Unchanged.

## What gets REMOVED

- The entire "Derivation: CKM phase from the Plancherel density" (lines 2606-2770)
- All references to tanh(pi), theta_CS * tanh(pi), "Plancherel density of the Dirac operator"
- All instances of 68.63° in this file (14 occurrences)
- The pair-based generation assignment language
- References to the RIGHT rotation M†M

## What gets ADDED

- The Gauss sum derivation as a new Theorem (replaces thm:ckm-phase)
- The instanton proof as a new Theorem
- The PMNS section with complementarity
- The orbit-based generation assignment
- The LEFT rotation statement
- The unified conformal dimension c = 1/2 + lambda/N
- Bernoulli phase assignment (N-k)/42

## Label mapping (old → new)

| Old label | New label | Content |
|-----------|-----------|---------|
| thm:ckm-phase | thm:ckm-phase (reused) | Gauss sum derivation (replaces Plancherel) |
| sec:ckm-phase | sec:ckm-phase (reused) | Same section, new content |
| sec:ckm-np | sec:ckm-mixing | Orbit-based CKM mixing angles |
| (new) | sec:pmns | PMNS neutrino mixing |
| (new) | thm:instanton-vub | K^(N-1) for V_ub |
| (new) | thm:complementarity | CKM-PMNS complementarity |

## Numerical values to use

All from the orbit_ckm.py computation at sigma=5 with correct F_IR:

| Observable | Value | PDG | Match |
|-----------|-------|-----|-------|
| delta_CKM | arctan(√7) = 69.3° | 69 ± 3° | 0.1σ |
| sin²(delta) | 7/8 | — | exact |
| s12 | 0.230 | 0.225 | 2% |
| s23 | 0.043 | 0.042 | 1% |
| s13_corrected | 0.0024 | 0.00365 | 35% |
| J | 2.1e-5 | 3.08e-5 | 31% |
| theta_12^PMNS | 32.9° | 33.4° | 0.5° |
| theta_23^PMNS | 45° | 49 ± 4° | 1σ |
| theta_13^PMNS | 9.3° | 8.5° | 0.8° |

## Files to modify

- `latex/paper-4-field-theory/main.tex` — rewrite ~400 lines in Section 12

## Cross-references

- Paper I: Theorem thm:bernoulli-havelock, Theorem thm:von-staudt-N (from Spec 3A)
- Paper I: Proposition prop:unified-conformal (from Spec 3A)
- Code: orbit_ckm.py, pmns_mixing.py, instanton_proof.py (from Spec 1)

## Success criteria

1. Paper IV compiles without errors
2. Zero instances of "68.63" remain in the file
3. Zero instances of "tanh.*pi" in the CKM context remain
4. Zero instances of "Plancherel" in the CKM derivation remain
5. All cross-references resolve (no undefined labels)
6. The Gauss sum derivation is self-contained (doesn't require reading the old version)
7. PMNS section states the delta_CP prediction explicitly as testable
