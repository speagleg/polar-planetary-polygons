# Paper Restructure: 4-Part, 20-Section Layout

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure the 3,696-line paper from 8 flat sections into a 4-Part, 20-Section hierarchy that separates mathematical foundations, point vortex physics, extensions/robustness, and planetary applications.

**Architecture:** Each Part becomes a `\part{}` divider. Sections are renumbered 1-20. All existing `\label{}` names are preserved (no ref breakage). Theorem numbering switches to per-section (`\numberwithin{theorem}{section}`). The restructuring is pure text movement — no new mathematical content.

**Tech Stack:** LaTeX, pdflatex, grep for verification

**Branch:** `restructure/four-part-layout`

---

## Current → Target Mapping

### Line ranges in current `main.tex` (3,696 lines)

| Current | Lines | Target |
|---------|-------|--------|
| Abstract | 25-90 | Abstract (unchanged) |
| §1 Introduction | 99-175 | §1 (add ToC after) |
| §2.1 Point vortex dynamics | 180-207 | **Part II** §6.1 |
| §2.2 Sign rule | 208-395 | **Part I** §2 |
| §2.3 Mobius covariance | 396-471 | **Part I** §1.2-1.3 |
| §3.1 Spiral deformation | 476-518 | **Part II** §6.3 |
| §3.2 Energy curvature | 519-547 | **Part II** §7.1 |
| §3.3 Constrained minimum | 548-687 | **Part II** §7.2-7.3 |
| §3.4 Central vortex | 688-807 | **Part II** §8 |
| §3.5 N=7 bifurcation | 808-920 | **Part II** §9 |
| §4 Curvature invariant | 921-942 | **Part I** §4 intro |
| §4.1 Riemannian Havelock | 943-1054 | **Part I** §3.2-3.4 |
| §4.2 Sphere | 1055-1193 | **Part I** §4.3 |
| §4.3 Hyperbolic plane | 1194-1487 | **Part I** §4.4, §5 |
| §5.1 Three-scale mechanism | 1488-1538 | **Part IV** §15 |
| §5.2 Constraint intersection | 1539-1875 | **Part IV** §16, §18 |
| §5.3 Saturn persistence | 1876-1919 | **Part IV** §17.2 |
| §5.4 Blob bridge | 1920-2638 | **Part III** §11, §13 |
| §5.5 Deformation radius | 2639-2918 | **Part III** §12 |
| §6 Planetary applications | 2919-3135 | **Part IV** §19 |
| §6.3 Multi-ring | 3061-3135 | **Part II** §10 |
| §7 BEC predictions | 3136-3213 | **Part III** §14 |
| §8 Discussion | 3214-3545 | §20 |
| App A Havelock | 3546-3577 | **Part I** §3.1 (moved forward) |
| App B C1 derivation | 3578-3696 | Appendix B (kept) |

## Strategy

**Critical constraint:** All `\label{}` names stay unchanged. The `\ref{}` system resolves by label name, not number, so moving text is safe as long as labels travel with their environments.

**Theorem numbering:** Add `\numberwithin{theorem}{section}` to preamble. This means Theorem 1 in §3 becomes Theorem 3.1, etc. All `\ref{thm:...}` calls auto-update.

**Execution order:** Work Part by Part, compiling after each to catch errors early.

---

## Task 1: Preamble and Infrastructure

**Files:**
- Modify: `latex/paper/main.tex:1-24`

- [ ] **Step 1:** Add `\numberwithin` and `\part` support to preamble

Add after line 14 (`\newtheorem{remark}{Remark}`):
```latex
\numberwithin{theorem}{section}
\numberwithin{definition}{section}
\numberwithin{remark}{section}
\numberwithin{equation}{section}
```

- [ ] **Step 2:** Add `\tableofcontents` after `\maketitle` and the abstract

- [ ] **Step 3:** Compile and verify — should produce a ToC on page 2

- [ ] **Step 4:** Commit
```
git commit -m "restructure: add theorem/eq numbering within sections, ToC"
```

---

## Task 2: Part I — Mathematical Foundations (§§1-5)

**Strategy:** Extract and reorder the pure math content. This is the biggest move.

**Source blocks to move:**
- §2.2 Sign rule (lines 208-395) → new §2
- §2.3 Mobius (lines 396-471) → new §1.2-1.3
- Appendix A Havelock identity (lines 3546-3577) → new §3.1
- §4.1 Riemannian Havelock (lines 943-1054) → new §3.2-3.4
- §4 intro + §4.2 Sphere (lines 921-1193) → new §4
- §4.3 Hyperbolic + algebraic structure (lines 1194-1487) → new §4.4, §5

- [ ] **Step 1:** Insert `\part{Mathematical Foundations}` before current §2
- [ ] **Step 2:** Create new §1 "The Logarithmic Interaction" from §2.3 (Mobius) + §2.2 Remarks 1-2
- [ ] **Step 3:** Create new §2 "The Sign Rule" from §2.2 Theorem 1 + proof
- [ ] **Step 4:** Create new §3 "The Havelock Identity" — move Appendix A forward, add §4.1 Riemannian content
- [ ] **Step 5:** Create new §4 "Stability Thresholds on Constant-Curvature Surfaces" from §4 intro + §4.2 + §4.3 first half
- [ ] **Step 6:** Create new §5 "Algebraic Structure of the Stability Boundary" from §4.3 second half
- [ ] **Step 7:** Compile and verify all Part I refs resolve
- [ ] **Step 8:** Commit
```
git commit -m "restructure: Part I — Mathematical Foundations (§§1-5)"
```

---

## Task 3: Part II — Point Vortex Dynamics (§§6-10)

**Source blocks:**
- §2.1 Point vortex dynamics (lines 180-207) → new §6.1
- §3.1 Spiral deformation (lines 476-518) → new §6.3
- §3.2 Energy curvature (lines 519-547) → new §7.1
- §3.3 Constrained minimum (lines 548-687) → new §7.2-7.3
- §3.4 Central vortex (lines 688-807) → new §8
- §3.5 N=7 bifurcation (lines 808-920) → new §9
- §6.3 Multi-ring (lines 3061-3135) → new §10

- [ ] **Step 1:** Insert `\part{Fundamental Physics — Point Vortex Dynamics}`
- [ ] **Step 2:** Create §6 "Point Vortex Dynamics on a 2D Surface" from §2.1 + §3.1
- [ ] **Step 3:** Create §7 "The Constrained Energy Landscape" from §3.2 + §3.3
- [ ] **Step 4:** Create §8 "Central Vortex Stabilization" from §3.4
- [ ] **Step 5:** Create §9 "The N=7 Bifurcation" from §3.5
- [ ] **Step 6:** Move §6.3 Multi-ring → §10 "Multi-Ring Configurations"
- [ ] **Step 7:** Compile and verify
- [ ] **Step 8:** Commit
```
git commit -m "restructure: Part II — Point Vortex Dynamics (§§6-10)"
```

---

## Task 4: Part III — Physical Extensions and Robustness (§§11-14)

**Source blocks:**
- §5.4 Blob bridge (lines 1920-2638) → new §11
- §5.5 Deformation radius (lines 2639-2918) → new §12
- §5.4.4 Disorder (embedded in §5.4) → new §13
- §7 BEC (lines 3136-3213) → new §14

- [ ] **Step 1:** Insert `\part{Physical Extensions and Robustness}`
- [ ] **Step 2:** Create §11 "From Point Vortices to Continuous Vorticity" from blob bridge
- [ ] **Step 3:** Create §12 "Finite Rossby Deformation Radius" from §5.5
- [ ] **Step 4:** Create §13 "Circulation Disorder and Robustness" from disorder subsection
- [ ] **Step 5:** Create §14 "Predictions for Quantum Systems" from §7 BEC
- [ ] **Step 6:** Compile and verify
- [ ] **Step 7:** Commit
```
git commit -m "restructure: Part III — Extensions and Robustness (§§11-14)"
```

---

## Task 5: Part IV — Planetary and Astrophysical Applications (§§15-19)

**Source blocks:**
- §5.1 Three-scale mechanism (lines 1488-1538) → new §15
- §5.2 Constraint intersection (lines 1539-1875) → new §16, §18
- §5.3 Saturn persistence (lines 1876-1919) → new §17.2
- Rossby bridge from §5.4.3 → new §17.3
- §6.1-6.2 Planetary applications (lines 2919-3060) → new §19
- §5.5 Jupiter paragraphs → new §18.5

- [ ] **Step 1:** Insert `\part{Planetary and Astrophysical Applications}`
- [ ] **Step 2:** Create §15 "The Three-Scale Selection Mechanism"
- [ ] **Step 3:** Create §16 "Wavenumber Selection: Constraint-Intersection"
- [ ] **Step 4:** Create §17 "Saturn's Hexagon" (Rossby + persistence + bridge)
- [ ] **Step 5:** Create §18 "Jupiter's Polar Polygons" (north + south + barotropic)
- [ ] **Step 6:** Create §19 "Broader Observational Context and Predictions"
- [ ] **Step 7:** Compile and verify
- [ ] **Step 8:** Commit
```
git commit -m "restructure: Part IV — Planetary Applications (§§15-19)"
```

---

## Task 6: §20 Discussion + Appendices + Final Cleanup

**Source blocks:**
- §8 Discussion → §20 (mostly in place, just renumber)
- Appendix A: already moved to §3.1, replace with cross-ref
- Appendix B: keep
- Add new Appendix C: Code Availability

- [ ] **Step 1:** Renumber Discussion to §20
- [ ] **Step 2:** Replace Appendix A with cross-reference to §3.1
- [ ] **Step 3:** Add Appendix C: Code Availability
- [ ] **Step 4:** Final compile — verify all refs, no undefined labels
- [ ] **Step 5:** Verify page count is reasonable (expect ~52-55 pages with ToC)
- [ ] **Step 6:** Commit
```
git commit -m "restructure: §20 Discussion, appendices, final cleanup"
```

---

## Verification Checklist

After all tasks:
- [ ] `pdflatex` compiles with 0 undefined references
- [ ] All `\label`/`\ref` pairs resolve (grep for `??`)
- [ ] ToC renders correctly with Part/Section hierarchy
- [ ] Page count is in expected range
- [ ] No content lost (diff line count within ~50 lines of original + additions)
- [ ] All 325 Python tests still pass (code untouched)
