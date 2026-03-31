# Series Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix all reviewer-identified issues across Papers I-VI to raise the series average from 5.7 to 7.5+ without sacrificing any core mathematical arguments or physical derivations.

**Architecture:** Seven parallel workstreams (one per paper + one cross-cutting). Each task is a self-contained edit pass that can be committed independently. All removals tracked in `latex/REMOVED_CONTENT.md`.

**Tech Stack:** LaTeX editing, `python3 -m pytest tests/ -q` for verification after each task.

---

## File Map

| File | Tasks | Key changes |
|------|-------|-------------|
| `latex/paper-1-mathematics/main.tex` | 1, 7, 8 | B2/K-theory decision, code refs, sentences |
| `latex/paper-2-physics/main.tex` | 2, 7, 8 | Galois 3x, notation, code refs, sentences |
| `latex/paper-3-gravity/main.tex` | 3, 7, 8 | C1 notation, main theorem placement, Onsager-WDW compress, code refs |
| `latex/paper-4-field-theory/main.tex` | 4, 7, 8 | K notation, step numbering, R inconsistency, code refs |
| `latex/paper-5-cosmology/main.tex` | 5, 7, 8 | Break mega-section, add conclusion, fix \SPaper, Lambda notation |
| `latex/paper-6-discussion/main.tex` | 6, 8 | Split Discussion into subsections, fix c notation, orphaned footnote |
| `latex/REMOVED_CONTENT.md` | All | Track every removal |

---

### Task 1: Paper I — Structure and Redundancy

**Files:**
- Modify: `latex/paper-1-mathematics/main.tex`
- Modify: `latex/REMOVED_CONTENT.md`

**Estimated savings:** ~200 lines (from Section 6 trim + K-theory intro trim + sentence fixes)

- [ ] **Step 1: Trim Section 6 (B2 organising principle) from ~155 to ~40 lines**

Keep: the stability polynomial paragraph (2437-2452) and the growth law connection.
Cut: "csc^2 kernel in seven contexts" (87 lines, self-described "no new claims"), the 4/3 self-interaction identity (17 lines, tenuous connection), the B2-loop-through-index-theorem paragraph (17 lines, chain of associations without proof).
Replace with: a single remark listing the seven contexts with citations (10 lines) + forward reference to Paper III for the index-theorem connection.
Log all cuts in REMOVED_CONTENT.md.

- [ ] **Step 2: Trim Section 7 (K-theory) introduction from ~40 to ~15 lines**

The three-stage overview (lines 2581-2618) is 37 lines. Compress to 15 lines stating: (i) elementary invariant classifies phases, (ii) Selberg trace formula computes corrections on arithmetic surfaces, (iii) Kasparov product captures fractional Morse indices at thresholds.

- [ ] **Step 3: Fix Remark 2.1 — compress from 28 to 12 lines**

Keep: Cauchy functional equation statement, N-body lift reference, scale-independence conclusion.
Cut: re-explanation of dilation invariance (already in Proposition 2.1), prior work comparison (belongs in "Prior work" paragraph in Section 5).

- [ ] **Step 4: Fix Remark 5.2 item 3 — cut forward ref to Paper II**

Line ~924: "The quartic coefficient alpha_0 = 45/14 that resolves the marginal N=7 case is established in companion Paper II" — this is a forward reference inside a remark. Replace with: "The quartic coefficient that resolves the marginal N=7 case is positive (Paper II, Section 5)."

- [ ] **Step 5: Fix labels**

- Double label at Section 5 header: remove `\label{sec:curvature-invariant}`, keep `\label{sec:curvature-thresholds}`, update any refs.
- Conjecture label `prop:higher-genus` → `conj:higher-genus`, update refs.
- `rmk:csc2-universality` on a `\paragraph` → wrap in `\begin{remark}` or remove label.

- [ ] **Step 6: Fix line 1160 self-assessment**

"the results of this subsection are likely the most novel part" → "Systematic stability tables for N-gons on H^2 do not appear in the existing literature."

- [ ] **Step 7: Fix line 953 dismissive phrasing**

"A specialist who worked through the Boatto-Cabral calculation would likely have noticed this" → "The separation is implicit in the Boatto-Cabral calculation; we make it explicit and extend to H^2."

- [ ] **Step 8: Run tests, commit**

Run: `python3 -m pytest tests/ -q`
Expected: 1644 passed
Commit: "Paper I: trim B2 survey, compress K-theory intro, fix labels and tone"

---

### Task 2: Paper II — Redundancy, Notation, Structure

**Files:**
- Modify: `latex/paper-2-physics/main.tex`
- Modify: `latex/REMOVED_CONTENT.md`

**Estimated savings:** ~120 lines

- [ ] **Step 1: Consolidate Galois rationality (lines ~460-491) from 3x to 1x**

Keep lines 460-462 (the Galois argument). Cut the restatements at 472-477 and 483-487. Replace with: "The value 153/7 is confirmed by exact rational arithmetic and Richardson extrapolation to 50 decimal places."

- [ ] **Step 2: Compress N=6 central vortex example (lines ~386-418) from 32 to ~8 lines**

Keep: the result kappa_crit(6) = -1/4 and the physical interpretation. Cut: the full substitution derivation and dynamical-stability cross-check.

- [ ] **Step 3: Richardson extrapolation (lines ~520-534) — move detail to footnote**

Replace 14-line parenthetical with: "Richardson extrapolation at four step sizes confirms 135/7 to 50 decimal places."

- [ ] **Step 4: Fix notation collisions — add disambiguation**

Add after the notation section (or at first use):
- epsilon: "We use epsilon for blob width throughout; the N=7 perturbation amplitude is denoted A."
- eta: Use eta for deformation ratio, chi for Stuart parameter, keep eta_k for disorder.
- Rename sigma_eta to sigma_disorder where it collides with jet width sigma.

- [ ] **Step 5: Fix orphaned labels**

Remove `\label{part:pvd}` (line ~40) and `\label{part:extensions}` (line ~726). Remove duplicate section labels (keep one per section).

- [ ] **Step 6: Fix formatting bugs**

- Line ~1069: `\textsc{numerical}` → `\textit{numerical}`
- Lines ~1928-1930: merge stacked paragraph headers

- [ ] **Step 7: Split intro sentences**

Line 35 (56 words) → 3 sentences. Line 37 (56 words) → 2 sentences.

- [ ] **Step 8: Run tests, commit**

Run: `python3 -m pytest tests/ -q`
Commit: "Paper II: consolidate Galois 3x→1x, fix notation, compress examples"

---

### Task 3: Paper III — Notation, Structure, Compression

**Files:**
- Modify: `latex/paper-3-gravity/main.tex`
- Modify: `latex/REMOVED_CONTENT.md`

**Estimated savings:** ~150 lines

- [ ] **Step 1: Fix C1 notation collision**

Replace all instances of the Green's function offset `C_1^{GF}` with a new symbol `\Phi(\rho)` or `\mathcal{C}(\rho)`. Update the notation clarification paragraph (lines ~1189-1206) to define both symbols clearly. Use the new symbol consistently in the WDW section and proof of Theorem 6.1. Delete the 18-line clarification paragraph and replace with a 3-line definition.

- [ ] **Step 2: Compress four-role consistency from 3 instances to 1**

Keep the Introduction statement (lines 74-84). Replace lines 1259-1265 with "The four-role consistency (Introduction, Section 1) is preserved." Replace lines 1491-1502 with a 3-line version citing the Introduction.

- [ ] **Step 3: Fix the "Weyl anomaly" naming**

Replace "Weyl anomaly" for delta_m with "Havelock remainder" or "lattice correction" throughout (avoiding confusion with the CFT trace anomaly). ~15 instances to update.

- [ ] **Step 4: State main theorem early**

After the Introduction (line ~83), add a ~10-line "Main result" paragraph stating Theorem 6.1 informally: "The main result of this paper (Theorem 6.1, proved in Section 10) is that conditions (H1)-(H3) imply R = const on any 2D surface, i.e., the vacuum Einstein equations." Then in Section 10 the full formal statement and proof.

- [ ] **Step 5: Compress Onsager-WDW section from ~394 to ~280 lines**

Target cuts:
- "mathematical identity, not physical derivation" stated twice (lines ~2927-2938 and ~3290-3292) → keep first, cut second
- CL conditions checklist (lines ~3112-3133) → compress from 21 to 8 lines
- Quantum corrections discussion (lines ~3144-3170) → compress from 26 to 10 lines (overlaps WDW section)
- "Classical origin of b(N)" was already cut from Paper IV; verify no duplicate in the moved section

- [ ] **Step 6: Fix sentence fragment (line ~2844)**

"The Lashkari entanglement argument:" → "The entanglement argument of Lashkari (2014) shows that..."

- [ ] **Step 7: Fix grammar error (line ~364)**

"computed Stieltjes-Wigert polynomials" → "computed using Stieltjes-Wigert polynomials"

- [ ] **Step 8: Run tests, commit**

Commit: "Paper III: fix C1 notation, state main theorem early, compress Onsager-WDW"

---

### Task 4: Paper IV — Notation, Step Numbering, Consistency

**Files:**
- Modify: `latex/paper-4-field-theory/main.tex`
- Modify: `latex/REMOVED_CONTENT.md`

**Estimated savings:** ~80 lines

- [ ] **Step 1: Fix K notation collision (3 meanings → 3 symbols)**

- Gaussian curvature K = -1 → use kappa or K_geom (only ~3 instances)
- Instanton fugacity K = e^{-2pi k_frac} → rename to \mathcal{K} throughout (~12 instances)
- U(1) CS level K = 1 → keep as K (most standard usage)

Search-and-replace with verification that no math is broken.

- [ ] **Step 2: Fix step numbering in Proposition 4.1 proof**

Proposition uses (i)-(iv). Proof must match: rename "Step 2" → "Step (ii)", "Step 3" → "Step (iv)", etc.

- [ ] **Step 3: Fix SU(3) proof step numbering**

Part (b) currently continues from Part (a) numbering (Step 6a, 6b, 7a, 7b, 8). Restart: relabel as Steps B1-B5. Add a one-sentence summary before Step B1 (the dreibein chain): "The dreibein chain converts vortex displacements into CS gauge-field perturbations through five algebraic steps."

- [ ] **Step 4: Fix R_S1 inconsistency**

Line ~200: "R ~ 10^{-20} m" vs lines ~360, ~2111: "R ~ 10^{-21} m". Standardize to 10^{-21} m (which is 1/M_poly at ~300 TeV). Fix all 3 instances.

- [ ] **Step 5: Fix "AND" in caps (line ~704)**

"representation structure AND dynamics" → "representation structure and dynamics"

- [ ] **Step 6: Compress linearised/nonlinear toggling (lines ~815-852)**

Replace 37 lines of back-and-forth with: "The CS/WZW theorem (Witten 1989) provides the nonlinear result directly. The dreibein chain (Step B1) serves as an independent linearised-level verification."

- [ ] **Step 7: Fix label on non-environment (line ~1817)**

`\label{sec:ckm-np}` on a `\noindent\textbf{}` block → wrap in `\paragraph{Non-perturbative CKM.}` with proper label.

- [ ] **Step 8: Run tests, commit**

Commit: "Paper IV: fix K/R notation, step numbering, linearised/nonlinear compression"

---

### Task 5: Paper V — Structure, Notation, Conclusion

**Files:**
- Modify: `latex/paper-5-cosmology/main.tex`
- Modify: `latex/REMOVED_CONTENT.md`

**Estimated net change:** +30 lines (adding conclusion + section breaks, offset by compression)

- [ ] **Step 1: Break 900-line Section 3 into proper sections**

Current Section 3 ("The cosmological energy budget") runs lines ~131-1029. Promote existing subsections to top-level sections:

- Section 3: The cosmological constant from the N=11 instanton (Theorem 3.1 + proof, ~180 lines)
- Section 4: The N selection principle (Theorem + exhaustive elimination, ~210 lines)
- Section 5: The electroweak hierarchy (Theorem + Pell proof, ~200 lines)
- Section 6: The cosmological energy budget (Proposition + DM/baryon, ~200 lines)

Renumber subsequent sections accordingly (baryogenesis → 7, neutrinos → 8, inflation → 9, DM detection → 10).

- [ ] **Step 2: Extract Euler-Mascheroni sub-proof into standalone Lemma**

Lines ~201-252 (50-line sub-proof inside an enumerated list inside a proof) → new Lemma before Theorem 3.1: "The one-loop determinant correction to the BO tunnelling action is -gamma/2." Cite from the main proof.

- [ ] **Step 3: Add conclusion section**

After the DM detection section, add Section 11: Conclusion (~20 lines):
- Summary: from N=11 and the Seifert manifold, derive H_0, Omega_Lambda, Omega_DM, Omega_b, neutrino mass ratio, baryon asymmetry.
- Key testable predictions: normal hierarchy, w=-1, no 0nubb.
- Forward ref to Paper VI for full accounting.

- [ ] **Step 4: Fix \SPaper compilation error (line ~109)**

`\SPaper~VI` → `Paper~VI`

- [ ] **Step 5: Unify Lambda notation**

5 notations (bare Lambda, Lambda_3, Lambda_4, Lambda_Hav, Lambda_phys) → 2: Lambda_3 (3D) and Lambda_4 (4D physical). Define once in Proposition 2.1. Update ~15 instances.

- [ ] **Step 6: Fix duplicate section/paragraph heading**

Line ~1282: `\section{Dark matter detection}` followed by `\paragraph{Dark matter detection.}` → delete the `\paragraph`.

- [ ] **Step 7: Fix duplicate neutrino mass ratio**

Lines ~1210-1211 and ~1222-1223 state the same ratio. Delete the second instance.

- [ ] **Step 8: Fix H_0 precision claim**

Abstract says 0.001%. Body shows 0.002% (from log comparison). Change abstract to "0.002%" or "matching to 5 significant figures in the exponent."

- [ ] **Step 9: Convert structural \emph{} to \paragraph{}**

~30 instances of `\emph{Physical mechanism.}`, `\emph{Cancellation.}` etc. → `\paragraph{Physical mechanism.}`, `\paragraph{Cancellation.}`

- [ ] **Step 10: Run tests, commit**

Commit: "Paper V: break mega-section, add conclusion, fix notation and precision"

---

### Task 6: Paper VI — Structure, Notation, Redundancy

**Files:**
- Modify: `latex/paper-6-discussion/main.tex`

**Estimated savings:** ~40 lines

- [ ] **Step 1: Split monolithic Discussion into subsections**

Current Section 3 "Discussion" is 380 lines with 13 `\paragraph` headings. Promote to `\subsection`:
- 3.1 Status classification
- 3.2 Structural choices
- 3.3 Cumulative uncertainty
- 3.4 Structural limitations
- 3.5 Two precision regimes
- 3.6 Comparison to other frameworks
- 3.7 Falsifiable predictions
- 3.8 Input-output classification

- [ ] **Step 2: Fix c notation collision**

Line ~102: c = central charge. Line ~115: c = conformal dimension. Replace conformal dimension with Delta_c or h_c throughout (~5 instances in the BF threshold discussion).

- [ ] **Step 3: Fix orphaned dagger footnote**

The table has footnotes *, ddagger but the dagger footnote (line ~232, about m_s/m_b) has no corresponding marker in the table. Add dagger to the m_s/m_b row.

- [ ] **Step 4: Fix BF threshold duplication**

Lines 68-92 and 110-131 both explain k=K=1. Delete lines 128-131 (4 lines that restate 82-91 verbatim).

- [ ] **Step 5: Fix predictions listed twice**

Lines 294-300 list binary tests. Lines 394-406 list the same tests again. Delete lines 294-300 and add a forward ref: "The binary tests are enumerated in Section 3.7 below."

- [ ] **Step 6: Tone down promotional comparison**

Lines 376-382: "only entry with zero free parameters... milestones of theoretical physics" → "Among frameworks with zero free parameters, this is the first to simultaneously predict fermion mass ratios, CKM elements, and cosmological parameters."

- [ ] **Step 7: Fix abstract "two inputs" framing**

Abstract says "two inputs" but body acknowledges six structural choices + one calibration. Rewrite: "From one discrete input (N=7), one dimensionful scale (M_P), and six structural identifications forced by the geometry..."

- [ ] **Step 8: Run tests, commit**

Commit: "Paper VI: split Discussion, fix notation/footnote, honest abstract framing"

---

### Task 7: Cross-Cutting — Code References (All Papers)

**Files:**
- Modify: all 6 paper main.tex files

**Total code refs:** I=5, II=15, III=13, IV=6, V=1, VI=0 = **40 total**

- [ ] **Step 1: Add "Code availability" paragraph to each paper**

Before the bibliography in Papers I-V, add:
```latex
\paragraph{Code availability.}
All numerical verifications and computational proofs are
available in the companion code repository
(\texttt{src/planetary\_polygons/} and \texttt{tests/}).
```

- [ ] **Step 2: Replace all inline code refs in Paper I (5 instances)**

Replace each `(\texttt{proofs/...})` or `(\texttt{extensions/...})` with "(verified numerically; see Code Availability)".

- [ ] **Step 3: Replace all inline code refs in Paper II (15 instances)**

Same pattern. For refs inside proofs, replace with "verified to machine precision" or "confirmed by exact rational arithmetic."

- [ ] **Step 4: Replace all inline code refs in Paper III (13 instances)**

Same pattern.

- [ ] **Step 5: Replace all inline code refs in Paper IV (6 instances)**

Same pattern.

- [ ] **Step 6: Run tests, commit**

Commit: "All papers: consolidate code refs into Code Availability paragraphs"

---

### Task 8: Cross-Cutting — Sentence Length Pass (All Papers)

**Files:**
- Modify: all 6 paper main.tex files

This is the final polish pass. Target: no sentence over 40 words.

- [ ] **Step 1: Paper I — break flagged sentences**

Priority targets (from reviewer):
- Line ~830-831 (88 words): split inline equation into displayed + explanation
- Line ~874 (74 words): break parenthetical into separate sentences
- Line ~1886 (75 words): split Chebyshev primitive into 3 sentences
- Line ~2933 (52 words): split into 2 sentences
- Lines ~164-168 (55 words): split

- [ ] **Step 2: Paper II — break flagged sentences**

Priority targets:
- Line ~35 (56 words) — already noted, split into 3
- Line ~37 (56 words) — split into 2
- Lines ~85-94 (72 words): split Mobius paragraph
- Lines ~95-102 (62 words): split uniqueness claim
- Lines ~520-532 (72 words): Richardson parenthetical → footnote
- Line ~959-978 (80+ words): Proposition statement → split

- [ ] **Step 3: Paper III — break flagged sentences**

Priority targets:
- Lines ~116-119 (41 words): acceptable, minor tweak
- Lines ~326-337 (58 words): split CS partition function sentence
- Lines ~1320-1322 (63 words): move parenthetical to proof
- Lines ~3290-3292 (77 words): split Feynman-Kac into 3 sentences

- [ ] **Step 4: Paper IV — break flagged sentences**

Priority targets:
- Line ~388 (90+ words): split KK reduction into 2 sentences
- Lines ~1490-1561: add paragraph breaks in mass hierarchy wall
- Lines ~765-813: add orienting sentence before Step B1 sub-list

- [ ] **Step 5: Paper V — break flagged sentences**

Priority targets:
- Line ~78 (42 words): move forward-ref out of proposition
- Lines ~91-94 (43 words): split KK reduction sentence
- Lines ~538-546 (44 words): split enumerated item

- [ ] **Step 6: Paper VI — break flagged sentences**

Priority targets:
- Lines ~84-88 (42 words): split k=1 explanation
- Lines ~384-391 (55 words): split V_cb/H_0 sentence
- Lines ~409-413 (38 words with heavy parenthetical): split

- [ ] **Step 7: Run tests, final line counts, commit**

Run: `python3 -m pytest tests/ -q`
Report final line counts for all 6 papers.
Commit: "All papers: break sentences over 40 words"

---

## Execution Order

Tasks 1-6 are independent (one per paper) and can be executed in parallel.
Task 7 (code refs) depends on no other task and can run in parallel.
Task 8 (sentence pass) should run last, after all structural changes are complete.

Recommended order for serial execution:
1. Task 5 (Paper V — biggest structural change, highest risk)
2. Task 3 (Paper III — C1 notation affects many lines)
3. Task 4 (Paper IV — K notation collision)
4. Task 1 (Paper I — B2/K-theory trim)
5. Task 2 (Paper II — Galois + notation)
6. Task 6 (Paper VI — structural split)
7. Task 7 (code refs — mechanical)
8. Task 8 (sentences — final polish)

## Expected Final State

| Paper | Current | Target | Cut |
|-------|---------|--------|-----|
| I | 3355 | ~3100 | -255 |
| II | 2280 | ~2150 | -130 |
| III | 3328 | ~3100 | -228 |
| IV | 2396 | ~2300 | -96 |
| V | 1307 | ~1350 | +43 (conclusion + section breaks) |
| VI | 546 | ~510 | -36 |
| **Total** | **13,212** | **~12,510** | **-702** |

Target reviewer score: 7.5+ average (from current 5.7).
