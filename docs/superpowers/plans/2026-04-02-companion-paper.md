# Non-Technical Companion Paper Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Write a 55-75 page non-technical companion to the six-paper Havelock Field Theory series, accessible to readers with no science background, in Gordon's first-person voice.

**Architecture:** Single LaTeX file (`latex/companion/main.tex`) structured as Prologue + 6 Parts + Epilogue. Each Part mirrors one technical paper section-by-section. Every section opens with an italicized bottom-line sentence and closes with a `[Technical reference: Paper X, §Y]` tag. Equations appear sparingly with full symbol translation.

**Tech Stack:** LaTeX (shared preamble), no external dependencies. Voice reference at `docs/superpowers/specs/voice-reference-gordon.md`. Technical papers at `latex/paper-{1,2,3,4,5,6}-*/main.tex`.

---

## Critical Context for Every Task

**Before writing ANY prose, the implementer MUST:**
1. Read `docs/superpowers/specs/voice-reference-gordon.md` (Gordon's actual writing — the ground truth)
2. Read `docs/superpowers/specs/2026-04-02-companion-paper-design.md` (voice profile + anti-patterns)
3. Read the corresponding technical paper sections being translated

**Voice checklist (apply to every paragraph):**
- Does this sound like Gordon wrote it? Compare against the voice reference.
- Any AI shibboleths? (delve, tapestry, crucial, utilize, landscape, elegant, robust, comprehensive, groundbreaking, novel approach, at its core, shed light on, it turns out that, remarkably, interestingly)
- Semicolons and colons for connective tissue? Dashes for asides?
- Varied sentence length? Short punches mixed with longer explanations?
- Concrete and specific? (name the book, name the number, name the equation)
- Honest about limitations? No false modesty, no arrogance?

---

### Task 1: Create LaTeX skeleton and Prologue

**Files:**
- Create: `latex/companion/main.tex`

**Context:** This task creates the document and writes the Prologue ("The Polygon Number"). The Prologue is 3-5 pages, no equations, punchline-first. It must hook a reader who knows nothing about physics.

- [ ] **Step 1: Read voice reference and spec**

Read these files completely before writing anything:
- `docs/superpowers/specs/voice-reference-gordon.md`
- `docs/superpowers/specs/2026-04-02-companion-paper-design.md`

- [ ] **Step 2: Read Paper VI status table for the scorecard**

Read `latex/paper-6-discussion/main.tex` lines 192-300 to extract the 17 predictions, their status (Theorem/Derivation/Conjecture), and match values. This becomes the plain-English scorecard table.

- [ ] **Step 3: Write the LaTeX skeleton + Prologue**

Create `latex/companion/main.tex` with:
- Shared preamble input
- Title: "Why Rotating Fluids Make Polygons: A Companion for the Curious Reader"
- Author: Gordon Speagle
- The full Prologue with 5 subsections:
  1. Opening hook (Saturn's hexagon, Jupiter's octagon)
  2. The one idea (polygon stability splits into two parts, threshold N=7)
  3. The scorecard (plain-English table from Paper VI data)
  4. The honest disclaimer (Theorem/Derivation/Conjecture translated)
  5. The map (one paragraph per paper)
- Placeholder `\section` headers for all remaining Parts (I-VI) and Epilogue (empty, to be filled in subsequent tasks)

The Prologue must:
- Be entirely in Gordon's voice (first person, discovery narrative)
- Contain zero equations
- Hook the reader in the first paragraph
- Include the full scorecard table translated into plain English
- Set up the three-tier status system using everyday language

- [ ] **Step 4: Compile and verify**

```bash
cd latex/companion && pdflatex main.tex
```

Verify: compiles without error, prologue text renders, section headers present.

- [ ] **Step 5: Commit**

```bash
git add latex/companion/main.tex
git commit -m "Companion: LaTeX skeleton + Prologue (The Polygon Number)"
```

---

### Task 2: Part I — "The Mathematics of Polygons"

**Files:**
- Modify: `latex/companion/main.tex`

**Context:** This Part mirrors Paper I (`latex/paper-1-mathematics/main.tex`). It has 6 sections covering: logarithmic uniqueness, sign rule, Havelock formula, N=7 threshold, curved surfaces + algebraic number theory, stability phase diagram. This is where the central equation λ_m = C₁ - m(N-m)/2 is presented and translated.

- [ ] **Step 1: Read Paper I sections**

Read `latex/paper-1-mathematics/main.tex`:
- §1-2 (Introduction + logarithmic interaction): lines 36-389
- §3 (Sign rule): lines 390-567
- §4 (Havelock identity): lines 568-931
- §5-6 (Curvature thresholds + algebraic structure): lines 932-2418
- §7 (K-theory): lines 2419-2938

Extract the key results, theorems, and numerical values that need translating.

- [ ] **Step 2: Write Part I (6 sections)**

Replace the placeholder Part I in `latex/companion/main.tex` with:

1. **"Why logarithms are special"** [Technical reference: Paper I, §1-2]
   - Explain that in 2D, the natural force law is logarithmic (1/distance)
   - Why this is the unique scale-independent interaction
   - Analogy: logarithms are to 2D what gravity (1/r²) is to 3D
   - Status: **(Proved)**

2. **"The sign rule: bowls, not hilltops"** [Technical reference: Paper I, §3]
   - The polygon sits at the bottom of an energy valley, not the top of a hill
   - Previous literature assumed the hilltop; this series proves it's a bowl
   - Bowl analogy: marble in a bowl vs balanced on a dome
   - Status: **(Proved)**

3. **"The Havelock formula: one equation, two parts"** [Technical reference: Paper I, §4]
   - Present the equation: $\lambda_m = C_1 - m(N-m)/2$
   - Translate EVERY symbol: λ_m = stability of the m-th wobble mode; C₁ = one number from the surface; m(N-m)/2 = a counting pattern from pure geometry
   - "In words: the stability of any polygon on any surface splits cleanly into a piece from the surface and a piece from pure counting."
   - Status: **(Proved)**

4. **"Why seven is the magic number"** [Technical reference: Paper I, §4-5]
   - On a flat surface, C₁ = N-1
   - The polygon breaks when C₁ < m(N-m)/2
   - At N=7, m=3: C₁ = 6 = 3×4/2 = 6. Exactly balanced.
   - At N=8, m=4: C₁ = 7 < 4×4/2 = 8. Unstable.
   - The round-table analogy
   - Status: **(Proved)**

5. **"Curved surfaces and algebraic number theory"** [Technical reference: Paper I, §5-6]
   - On curved surfaces, C₁ changes and the threshold shifts
   - H² thresholds live in quadratic number fields
   - ξ* = 8 - 3√7 = inverse fundamental unit of Z[√7]
   - For science-adjacent: the palindromic quadratic explained term by term
   - Show the equation $\xi^2 - 16\xi + 1 = 0$ and translate: "a quadratic that reads the same forwards and backwards"
   - Status: **(Proved)**

6. **"The stability phase diagram"** [Technical reference: Paper I, §7]
   - Different surfaces create stability zones with sharp boundaries
   - These boundaries can't be smoothly deformed away (topological character)
   - No K-theory jargon; physical picture of a phase diagram
   - Status: **(Proved)**

Each section MUST open with an italicized bottom-line sentence.

- [ ] **Step 3: Compile and verify**

```bash
cd latex/companion && pdflatex main.tex
```

- [ ] **Step 4: Commit**

```bash
git add latex/companion/main.tex
git commit -m "Companion: Part I — The Mathematics of Polygons"
```

---

### Task 3: Part II — "The Physics of Vortex Rings"

**Files:**
- Modify: `latex/companion/main.tex`

**Context:** Mirrors Paper II (`latex/paper-2-physics/main.tex`). 4 blocks covering: vortex dynamics, central vortices + N=7 bifurcation, blob/Rossby corrections, vortex-gravity isomorphism.

- [ ] **Step 1: Read Paper II sections**

Read `latex/paper-2-physics/main.tex`:
- §1-3 (Dynamics + constrained landscape): lines 69-231
- §4-5 (Central vortex + N=7 bifurcation): lines 232-447
- §6-9 (Blob + Rossby + disorder + deformation): lines 562-1184
- §10-12 (Gravity + convergence): lines 1647-1924

- [ ] **Step 2: Write Part II (4 blocks)**

Replace the placeholder Part II with:

1. **"How vortices actually move"** [Technical reference: Paper II, §1-3]
   - Vortices aren't particles — tiny whirlpools with no inertia
   - They go wherever the other vortices push them
   - Constrained equilibrium: what it means physically

2. **"Stabilizing the unstable: central vortices and the N=7 bifurcation"** [Technical reference: Paper II, §4-5]
   - N≥8 polygons wobble apart unless held by a central vortex
   - Critical strength at N=8: central vortex must be half as strong
   - BEC prediction: integer circulation threshold
   - N=7 quartic: flat-bottomed bowl, α₀ = 45/14

3. **"From perfect to realistic"** [Technical reference: Paper II, §6-9]
   - Blob correction: finite cores, profile-independent
   - Rossby bridge: Saturn's hexagon (N=6) from known parameters
   - Circulation disorder: stability isn't a knife-edge

4. **"Vortices meet gravity"** [Technical reference: Paper II, §10-12]
   - In 2+1D gravity, deficit angle = vortex circulation
   - Same Green's function, same eigenvalues
   - Not an analogy — an isomorphism

Each section: italicized bottom line, [Technical reference] tag, status tags.

- [ ] **Step 3: Compile and verify**

```bash
cd latex/companion && pdflatex main.tex
```

- [ ] **Step 4: Commit**

```bash
git add latex/companion/main.tex
git commit -m "Companion: Part II — The Physics of Vortex Rings"
```

---

### Task 4: Part III — "How Gravity Emerges"

**Files:**
- Modify: `latex/companion/main.tex`

**Context:** Mirrors Paper III (`latex/paper-3-gravity/main.tex`). 5 blocks. This is the conceptual heart — the series' central theorem (polygon entropy → Einstein equations) must be explained to a layperson.

- [ ] **Step 1: Read Paper III sections**

Read `latex/paper-3-gravity/main.tex`:
- §1-2 (Intro + graviton): lines 40-403
- §3-4 (Einstein theorem + Onsager): lines 404-1542
- §5-7 (WDW + Clausius + spectral bound): lines 1543-1877
- §8-11 (Holographic + BTZ + OPE + three-layer): lines 1878-2782
- §12-13 (Partition function + Onsager-WDW correspondence): lines 3085-end

- [ ] **Step 2: Write Part III (5 blocks)**

1. **"The graviton is a wobble of seven"** [Technical reference: Paper III, §1-2]
   - Marginal mode at N=7 carries spin 2 = graviton
   - Pell equation uniqueness
   - "Which polygon produces a spin-2 particle? Seven. Only seven."

2. **"Why the universe has constant curvature"** [Technical reference: Paper III, §3-4]
   - Jensen's inequality: "the average of a curved function ≤ the function of the average"
   - Onsager principle: nature selects the entropy maximum
   - Together → R = const → Einstein's equation in 2+1D
   - Crumpled paper analogy (and where it breaks)

3. **"The cosmological constant and the breathing mode"** [Technical reference: Paper III, §5-7]
   - The polygon breathes — expands and contracts
   - WDW equation on the breathing mode
   - c = 12b(N) from Fisher-Rao (not a free parameter)
   - Λ = ground-state energy of breathing

4. **"Black holes, holograms, and the full Riemann tensor"** [Technical reference: Paper III, §8-11]
   - Heat the polygon → BTZ black hole phase transition
   - Holographic principle: boundary encodes bulk
   - Three-layer theorem: add one compact dimension → all 10 Weyl components from N

5. **"From statistics to quantum mechanics"** [Technical reference: Paper III, §12-13]
   - Feynman-Kac: thermodynamics IS quantum mechanics (not by analogy)
   - Self-decoherence: no external observer needed
   - Onsager-WDW correspondence in plain language

- [ ] **Step 3: Compile and verify**

```bash
cd latex/companion && pdflatex main.tex
```

- [ ] **Step 4: Commit**

```bash
git add latex/companion/main.tex
git commit -m "Companion: Part III — How Gravity Emerges"
```

---

### Task 5: Part IV — "The Particles Inside the Polygon"

**Files:**
- Modify: `latex/companion/main.tex`

**Context:** Mirrors Paper IV (`latex/paper-4-field-theory/main.tex`). 5 blocks. Most ambitious claims; needs especially clear translation. Key equations: sin²θ_W = 3/11 (show arithmetic), α_s = 1/(4π√2).

- [ ] **Step 1: Read Paper IV sections**

Read `latex/paper-4-field-theory/main.tex`:
- §1-2 (Spacetime + field content): lines 93-270
- §3-5 (Couplings + anomaly + gauge group): lines 420-565
- §6-8 (SU(3) + SU(2) + confinement): lines 566-1444
- §9-10 (Weinberg + action): lines 1445-1770
- §11-13 (Fermion masses + UV + corrections + consistency): lines 1917-end

- [ ] **Step 2: Write Part IV (5 blocks)**

1. **"The shape of spacetime is forced"** [Technical reference: Paper IV, §1-2]
   - N=4+7=11; Thurston classification; Seifert manifold
   - 4D graviton from boundary vibrations
   - "This isn't chosen; it's the only option left."

2. **"One number sets every coupling"** [Technical reference: Paper IV, §3-5]
   - c = 12b(N) determines all force strengths
   - α_s = 1/(4π√2) ≈ 0.056, runs to 0.118 at Z boson
   - Show: sin²θ_W = (1/4) ÷ (1/4 + 2/3) = 3/11, translate each fraction

3. **"Where the Standard Model gauge group comes from"** [Technical reference: Paper IV, §6-8]
   - Klein quartic → Frobenius orbits → McKay → SU(3)
   - SU(2) from N=4; U(1) from fiber rotation
   - Three generations = three palindromic pairs
   - Confinement: 1+ω+ω²=0

4. **"The Weinberg angle and the CKM phase"** [Technical reference: Paper IV, §9-10]
   - Weinberg angle: how EM and weak force split
   - CKM phase: why matter ≠ antimatter; δ = 70.2°
   - For science-adjacent: the integral explained step by step

5. **"Fermion masses, the Higgs, and consistency"** [Technical reference: Paper IV, §11-13]
   - Mass hierarchy from tunneling amplitudes
   - Higgs mass 122-128 GeV (measured: 125.1)
   - String tension σ/Λ² = 5.97 (lattice: 6.25 ± 0.5)
   - Proton stability, strong CP θ=0

- [ ] **Step 3: Compile and verify**

```bash
cd latex/companion && pdflatex main.tex
```

- [ ] **Step 4: Commit**

```bash
git add latex/companion/main.tex
git commit -m "Companion: Part IV — The Particles Inside the Polygon"
```

---

### Task 6: Part V — "The Numbers of the Universe"

**Files:**
- Modify: `latex/companion/main.tex`

**Context:** Mirrors Paper V (`latex/paper-5-cosmology/main.tex`). 4 blocks. Key equations: Λ₃ = (N²-16)/16, hierarchy decomposition 36.548 + 2.224 - 0.313 = 38.458.

- [ ] **Step 1: Read Paper V sections**

Read `latex/paper-5-cosmology/main.tex`:
- §1-4 (CC + N-selection + hierarchy): lines 69-437
- §5-6 (CC from instanton + verification): lines 438-738
- §7-9 (Energy budget + baryogenesis + neutrinos): lines 739-1296
- §10-12 (Inflation + DM detection + initial state): lines 1297-1502

- [ ] **Step 2: Write Part V (4 blocks)**

1. **"Why N=11, and the cosmological constant"** [Technical reference: Paper V, §1-4]
   - Flux additivity: 4+7=11
   - Elimination table in plain English
   - Show: Λ₃ = (N²-16)/16; at N=4: zero; at N=11: 105/16
   - Translate: "the curvature of the universe is set by one subtraction"

2. **"The hierarchy problem solved by tunneling"** [Technical reference: Paper V, §5-6]
   - Why gravity is 10¹⁶ times weaker than other forces
   - S_BO(7) = 18.274; the three components
   - Show: 36.548 + 2.224 - 0.313 = 38.458 vs observed 38.442
   - The Pell identity: hierarchy ratio = power of 8+3√7

3. **"The cosmic energy budget"** [Technical reference: Paper V, §7-9]
   - 69% dark energy, 26% dark matter, 5% ordinary matter
   - Tree-level = DE; one-loop = DM; tunneling = baryons
   - Instanton resummation for baryon fraction
   - η_B factor-of-3 limitation (lattice QCD, not the theory)

4. **"Neutrinos, inflation, and the beginning"** [Technical reference: Paper V, §10-12]
   - Neutrino masses from seesaw
   - Radion drives inflation
   - Penrose past hypothesis: initial Weyl curvature vanishes at threshold
   - Arrow of time from tunneling event

- [ ] **Step 3: Compile and verify**

```bash
cd latex/companion && pdflatex main.tex
```

- [ ] **Step 4: Commit**

```bash
git add latex/companion/main.tex
git commit -m "Companion: Part V — The Numbers of the Universe"
```

---

### Task 7: Part VI — "The Scorecard" + Epilogue

**Files:**
- Modify: `latex/companion/main.tex`

**Context:** Mirrors Paper VI (`latex/paper-6-discussion/main.tex`). 4 sections + Epilogue. Shorter than other Parts. Closes the loop back to Saturn's hexagon.

- [ ] **Step 1: Read Paper VI**

Read `latex/paper-6-discussion/main.tex` in full (751 lines).

- [ ] **Step 2: Write Part VI (4 sections) + Epilogue**

1. **"What goes in, what comes out"** [Technical reference: Paper VI, §1]
   - One integer (N=7), one scale (M_P), three identifications
   - 17 outputs
   - Plain-English parameter accounting table

2. **"How confident should you be?"** [Technical reference: Paper VI, §2-3]
   - Algebraic tier: exact (gauge group, generations, θ_QCD=0)
   - Geometric tier: ~5% (H₀, fermion masses, CKM)
   - Cumulative uncertainty in plain language

3. **"How to prove this wrong"** [Technical reference: Paper VI, §3]
   - Six binary pass/fail tests listed and explained
   - "If any one fails, the theory is wrong."

4. **"What remains open"** [Technical reference: Paper VI, §4]
   - DM production mechanism
   - η_B factor-of-3
   - Light quark masses 40-60%
   - No defensive hedging — just state what is and isn't known

**Epilogue: "One Formula"** (1-2 pages)
   - Return to Saturn's hexagon
   - One sentence per paper summarizing the path
   - Close: what confirmation/refutation looks like
   - Final line: invitation for feedback (matching Gordon's closing in his introduction)

- [ ] **Step 3: Compile and verify**

```bash
cd latex/companion && pdflatex main.tex
```

- [ ] **Step 4: Commit**

```bash
git add latex/companion/main.tex
git commit -m "Companion: Part VI (The Scorecard) + Epilogue (One Formula)"
```

---

### Task 8: Voice review and final polish

**Files:**
- Modify: `latex/companion/main.tex`

**Context:** Read the entire companion start to finish. Check every paragraph against the voice reference. Fix any AI shibboleths, hedging, or tone breaks.

- [ ] **Step 1: Full read-through with voice checklist**

Read the entire `latex/companion/main.tex`. For every paragraph, check:
- [ ] Does this sound like Gordon? Compare sentence structure against `docs/superpowers/specs/voice-reference-gordon.md`
- [ ] Any words from the AI shibboleth blacklist?
- [ ] Semicolons/colons for connective tissue? Dashes for asides?
- [ ] Varied sentence length?
- [ ] Concrete and specific (not vague)?
- [ ] Status tags on every factual claim?
- [ ] Cross-reference tags on every section header?
- [ ] Bottom-line italicized sentence at start of every section?

- [ ] **Step 2: Fix all voice issues found**

Make surgical edits. Do not rewrite passages that sound correct.

- [ ] **Step 3: Verify all cross-references are correct**

Check that every `[Technical reference: Paper X, §Y]` tag points to the right section by comparing against the technical paper section headers.

- [ ] **Step 4: Final compile**

```bash
cd latex/companion && pdflatex main.tex && pdflatex main.tex
```

(Two passes for references.)

- [ ] **Step 5: Commit**

```bash
git add latex/companion/main.tex
git commit -m "Companion: voice review and final polish"
```

- [ ] **Step 6: Push**

```bash
git push origin feature/algebraic-extensions
```
