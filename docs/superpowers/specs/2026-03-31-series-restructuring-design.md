# Series Restructuring Design Spec

**Date:** 2026-03-31
**Status:** Draft — awaiting user approval

---

## Overview

Restructure the Havelock Field Theory series from 4 papers into a 9-document suite: a Reader's Guide, author-written philosophical intro, 5 derivation papers (I-V), a Discussion/Predictions paper (VI), and an author-written philosophical outro. The split is driven by logical dependency (N=7 vs N=11), audience focus, and the need to bring Paper IV (4483 lines) under control.

---

## Series Structure

### Reader's Guide: *The Havelock Field Theory: A Guide for Readers*
- **Role:** Series prologue. The front door for every reader.
- **Language:** Plain, accessible, no heavy jargon. A journalist should be able to follow it.
- **Content:**
  - One-paragraph series summary (what the series claims, in plain English)
  - Reader-type sections: planetary scientist, fluid dynamicist, mathematical physicist, particle physicist, cosmologist, skeptic/referee
  - Each section: 3-5 sentences pointing to specific papers and sections
  - A one-page visual map of the derivation chain (which paper feeds which)
  - No mathematics beyond λ_m = C₁ - m(N-m)/2
- **Length:** 3-5 pages
- **Format:** Standalone PDF, not a numbered paper. Posted as arXiv ancillary or series cover letter.

### Intro: Philosophical Introduction (author-written)
- **Role:** Sets the conceptual framework and motivation before the formal mathematics begins.
- **Author:** Gordon Speagle (not Claude). This is the author's voice and philosophical perspective.
- **Content:** Why this approach, what it means, the conceptual leap from vortex polygons to fundamental physics.
- **Position:** After the Reader's Guide, before Paper I.

### Paper I: Mathematical Foundations (~2800 lines target)
- **Content:** Sign rule, Havelock identity, Riemannian extension, spherical/hyperbolic thresholds, palindromic quadratics, Pell units, algebraic-integer classification, geodesic correspondence, universality of N_crit=7, constrained minimum theorem, K-theory classification.
- **Changes from current:**
  - Already done: constrained minimum theorem added, physics digressions removed, redundancy cut
  - Remaining: consider shortening Section 6 (B₂) and Section 7 (K-theory)
- **Ends with:** Forward reference to Paper VI for discussion and predictions.

### Paper II: Classical & Quantum Physics (~2000 lines target)
- **Content:** Constrained energy minimum (full quartic), central vortex, N=7 bifurcation, multi-ring dichotomy, blob bridge, Rossby bridge, deformation radius, circulation disorder, BEC predictions, gravitational polygon stability (Props 11.1-11.3).
- **Changes from current:**
  - Move Section 11.2 (three-layer decomposition, orbifold-Havelock, WDW) to Paper III
  - Move Remark 9.4 (TQFT independence) to Paper III
  - Fix broken refs already done
- **Ends with:** Forward reference to Paper VI.

### Paper III: Gravitational Theory (~2800 lines target)
- **Content (current):** CMS-CS Casimir, graviton at N=7, spectral bound, holographic interpretation, OPE identification, BTZ transition, WDW equation, three-layer decomposition, higher-dimensional extension, triangle universality, partition function, Einstein equations (Theorem 6.1).
- **Content added from Paper IV:**
  - Onsager-WDW correspondence (~370 lines → compress to ~250 during move)
  - Black hole entropy check (~20 lines)
  - Nonlinear 4D Einstein theorem (~100 lines — currently re-proved in IV; move to III, IV references it)
- **Content added from Paper II:**
  - Three-layer decomposition subsection (~70 lines)
  - TQFT independence remark (~38 lines)
- **Changes:** Szegő-Toeplitz (188 lines) → appendix or supplement
- **Ends with:** Forward reference to Paper VI.

### Paper IV: Gauge Theory & Particle Physics (~2200 lines target)
- **Scope:** Everything derivable from N=7 + Seifert manifold + M_P. No cosmology.
- **Content from current Paper IV:**
  - Introduction (rewritten for narrower scope)
  - The spacetime (Seifert manifold, Thurston classification)
  - Field content
  - Emergence of 4D graviton (theorem + proof; refs Paper III for nonlinear Einstein)
  - Couplings from c=12b(N)
  - Weyl anomaly
  - Standard Model gauge group (SU(3)×SU(2)×U(1))
  - Weinberg angle (sin²θ_W = 3/11)
  - UV completion
  - The action (complete 4D Lagrangian)
  - One-loop corrections
  - Fermion mass structure (hierarchy, CKM mixing, CKM phase δ=70.2°)
  - Gauge-sector consistency checks: graviton propagator, Newton's law, equivalence principle, anomaly cancellation, proton stability, Higgs mass
- **Content removed:**
  - Cosmological constant section → Paper V
  - N=11 selection → Paper V
  - Cosmological energy budget → Paper V
  - Baryogenesis → Paper V
  - Neutrino masses → Paper V
  - Radion inflation → Paper V
  - Dark matter spectrum → Paper V
  - Dark matter detection check → Paper V
  - Onsager-WDW → Paper III
  - Black hole entropy check → Paper III
  - Nonlinear Einstein re-proof → Paper III (referenced)
  - Parameter accounting → Paper VI
  - Status classification → Paper VI
  - Discussion → Paper VI
  - All defensive/redundant content already cut in this session
- **Ends with:** Forward reference to Paper VI.

### Paper V: Cosmological Parameters (~2000 lines target)
- **Scope:** Everything requiring N=11. The cosmology paper.
- **Content from current Paper IV:**
  - Introduction (new: explains the N=11 selection as the starting point)
  - Cosmological constant from the fiber
  - The N selection principle (N=4, N=7, N=11 from flux additivity)
  - Cosmological energy budget at N=11 (Ω_Λ, Ω_DM, Ω_b)
  - Dark matter spectrum (frozen KK modes)
  - Baryon fraction and mass gap
  - Baryogenesis (Sakharov conditions, transport equation)
  - Neutrino masses (seesaw from N=11 sector)
  - Radion inflation
  - Cosmology-sector consistency checks: dark matter detection, H₀ = 67.4
- **Infrastructure needed:** Paper V references the Seifert manifold (Paper IV), the BO potential (Paper III), the Havelock eigenvalues (Paper I). A brief (~20 line) "Setup and notation" section at the start establishes the link.
- **Ends with:** Forward reference to Paper VI.

### Paper VI: Discussion, Predictions & Status (~1000-1200 lines target)
- **Scope:** The series audit. No new derivations.
- **Content:**
  1. **Series summary** — one-page overview of the derivation chain
  2. **Parameter accounting** — the full input/constrained/calibration/prediction table covering all 5 derivation papers
  3. **Status classification** — every result labelled Theorem, Derivation, or Conjecture
  4. **Cumulative uncertainty analysis** — the derivation chain reliability assessment
  5. **Two precision regimes** — algebraic (< 5%) vs geometric (10-30%)
  6. **Falsifiable predictions** — binary tests (normal hierarchy, w=-1, no 0νββ, proton stable, θ_QCD=0)
  7. **Correlated observables** — predictions linked through the instanton fugacity K
  8. **Sensitivity analysis** — elasticities (dln|V_cb|/dlnρ* = -2.5, etc.)
  9. **Structural limitations** — what the framework cannot predict
  10. **Comparison to other frameworks** — string theory, loop quantum gravity, asymptotic safety
  11. **Experimental timeline** — which experiments test which predictions, by when
- **Sources:** Discussion section of current Paper IV, parameter accounting section, status tables, predictions tables, cumulative uncertainty paragraph, two-precision-regimes table, structural limitations paragraph, comparison paragraph.
- **Ends with:** Forward reference to the Outro.

### Outro: Philosophical Conclusion (author-written)
- **Role:** Reflection on what the series means and where it leads. The bookend to the Intro.
- **Author:** Gordon Speagle (not Claude). Personal voice.
- **Content:** What this means for physics, open questions, the broader programme, where the work goes next.
- **Position:** After Paper VI. The final document in the series.

---

## Content Migration Map

### From current Paper IV → Paper III
| Content | Current lines (approx) | Est. after compression |
|---------|----------------------|----------------------|
| Onsager-WDW correspondence (sec 21) | ~370 | ~250 |
| Black hole entropy check | ~20 | ~20 |
| Nonlinear 4D Einstein theorem | ~100 | ~100 |
| **Total** | **~490** | **~370** |

### From current Paper IV → Paper V
| Content | Current lines (approx) | Est. after compression |
|---------|----------------------|----------------------|
| Cosmological constant section | ~65 | ~60 |
| N selection principle (sec 15.1) | ~210 | ~180 |
| Cosmological energy budget (sec 15, rest) | ~900 | ~700 |
| Baryogenesis (sec 16) | ~120 | ~100 |
| Neutrino masses (sec 17) | ~80 | ~70 |
| Radion inflation (sec 18) | ~50 | ~45 |
| DM detection check | ~15 | ~15 |
| New intro + setup | 0 | ~40 |
| **Total** | **~1440** | **~1210** |

### From current Paper IV → Paper VI
| Content | Current lines (approx) | Est. after compression |
|---------|----------------------|----------------------|
| Parameter accounting (sec 19) | ~100 | ~100 |
| Discussion (sec 22, what remains) | ~350 | ~300 |
| Status tables | included above | included |
| New series summary + experimental timeline | 0 | ~200 |
| **Total** | **~450** | **~600** |

### From current Paper II → Paper III
| Content | Current lines (approx) |
|---------|----------------------|
| Three-layer decomposition (sec 11.2) | ~70 |
| TQFT independence remark | ~38 |
| **Total** | **~108** |

---

## Estimated Final Line Counts

| Document | Source lines | Compression | Target |
|----------|------------|-------------|--------|
| Reader's Guide | New | — | 150-250 |
| Paper I | 3348 | Minor remaining cuts | ~2800 |
| Paper II | 2378 - 108 | Bug fixes done | ~2200 |
| Paper III | 3109 + 370 + 108 - 188 (Szegő→appendix) | | ~3000 |
| Paper IV | 4483 - 1440 - 490 - 450 | Refocused | ~2100 |
| Paper V | 0 + 1210 | New paper | ~1200 |
| Paper VI | 0 + 600 | New paper | ~800-1000 |
| **Total** | 13,318 | | ~12,350-12,550 |

Series total drops ~800-1000 lines (6-7%) while gaining two new papers, because the split eliminates cross-domain redundancy that existed only because everything was crammed into Paper IV.

---

## Cross-Reference Architecture

Each paper uses `\externaldocument` for the others. The dependency graph:

```
Reader's Guide (standalone, no LaTeX cross-refs)

I ← (standalone, refs nothing)
II ← I
III ← I, II
IV ← I, II, III
V ← I, III, IV
VI ← I, II, III, IV, V
```

Papers I-V end with: "Discussion of these results, their status, and experimental predictions appears in Paper~VI."

Paper VI back-references specific theorems, propositions, and equations from I-V.

---

## Forward Reference Convention

Each of Papers I-V ends its final section with a standardized closing:

```latex
\paragraph{Discussion and predictions.}
The status classification, parameter accounting, cumulative
uncertainty analysis, and falsifiable predictions for the
results of this paper appear in Paper~VI
(\S\ref*{VI-sec:status}--\S\ref*{VI-sec:predictions}).
```

No paper contains its own Discussion section. Paper VI is the single location for all meta-commentary about the series.

---

## Implementation Order

1. **Create Paper V** — extract cosmological content from Paper IV into new `latex/paper-5-cosmology/main.tex`
2. **Create Paper VI** — extract discussion/predictions from Paper IV into new `latex/paper-6-discussion/main.tex`
3. **Move Onsager-WDW + gravity checks to Paper III** — from Paper IV
4. **Move three-layer + TQFT to Paper III** — from Paper II
5. **Rewrite Paper IV intro** — narrow scope to gauge theory
6. **Rewrite Paper V intro** — establish N=11 starting point
7. **Write Paper VI intro** — series summary
8. **Write Reader's Guide** — standalone document
9. **Update all cross-references** — externaldocument declarations, \ref prefixes
10. **Update all forward references** — each paper's closing paragraph
11. **Run tests** — verify nothing broke
12. **Review pass** — deploy harsh reviewer on each paper

---

## Decisions Log

| # | Decision | Choice | Rationale |
|---|----------|--------|-----------|
| A | Split principle | By derivation layer (N=7 vs N=11) | Matches mathematical structure |
| B | Onsager-WDW placement | Paper III | Completes the gravity+quantum-foundations paper |
| C | Consistency checks | Split across papers by topic | Each paper self-validating |
| D | Parameter accounting | Own paper (Paper VI) | Series-level audit belongs at the end |
| E | Discussion | Paper VI, after full derivation | Papers I-V stay pure derivation |
| F | Reader's Guide | Standalone document before Paper I | Front door for every reader type |
