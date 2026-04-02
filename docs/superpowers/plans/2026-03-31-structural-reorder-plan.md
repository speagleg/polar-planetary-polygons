# Series Structural Reorder Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorder sections in Papers III and V to put main theorems first; extract heavy proof blocks to a supplement; split Paper IV consistency section; expand Paper II introduction.

**Architecture:** Each task handles one paper. Section reordering is done by cut-paste of LaTeX blocks with updated cross-references. Supplement material goes to `latex/supplement-proofs/main.tex`. All 1644 tests must pass after each task.

**Tech Stack:** LaTeX, git

**Constraints:**
- Keep anomaly structure subsection in Paper III (will develop later)
- All supplement blocks must be cited from main text with forward references
- Maintain logical narrative flow — no dangling forward references within papers
- Every \label must survive the move (other papers reference them via \externaldocument)

---

### Task 1: Create the supplement file

**Files:**
- Create: `latex/supplement-proofs/main.tex`
- Modify: `latex/shared/preamble.tex` (if needed for supplement)

- [ ] **Step 1:** Create `latex/supplement-proofs/main.tex` with preamble, title, empty sections for each paper's supplemental material:
  - S1: Paper I supplemental proofs (K-theory details, Bolza convergence)
  - S2: Paper II supplemental proofs (multi-ring casework)
  - S3: Paper III supplemental material (BTZ Lorentzian, spectral statistics)
  - S4: Paper V supplemental material (Pell identity proof)

- [ ] **Step 2:** Add `\externaldocument[S-]{../supplement-proofs/main}` to each paper's main.tex that references supplement content.

- [ ] **Step 3:** Verify tests pass: `python3 -m pytest tests/ -q`

- [ ] **Step 4:** Commit: `git commit -m "Create supplement-proofs file for extracted blocks"`

---

### Task 2: Paper III — Move main theorem from §11 to §3

This is the biggest and most impactful change. The Einstein derivation section (lines 1878-2720) moves to become §3, right after the graviton section.

**Files:**
- Modify: `latex/paper-3-gravity/main.tex`

- [ ] **Step 1:** Cut the entire Einstein section (lines 1878-2720, `\section{From polygon stability to the Einstein equations}` through end of its subsections, stopping before `\section{The Onsager--Wheeler--DeWitt correspondence}`).

- [ ] **Step 2:** Paste it after the current §2 (The graviton at N=7), before the current §3 (The spectral bound). Insert after line ~362 (end of the CS lift paragraph, before `\section{The spectral bound}`).

- [ ] **Step 3:** Update the introduction's reading guide (lines 77-85) — remove "the impatient reader may proceed directly to §9" since the theorem is now §3. Replace with: "The central theorem is proved in \S\ref{sec:lichnerowicz}, immediately following the graviton identification. Sections 4--11 develop the supporting infrastructure and consequences."

- [ ] **Step 4:** Check all internal \ref and \eqref cross-references within the moved block. Key refs to verify:
  - `\ref{thm:polygon-einstein}` — should still resolve
  - `\ref{prop:variation}` — moves with the theorem
  - `\ref{lem:onsager-regge}` — moves with the theorem
  - `\ref{cor:onsager-contraction}` — moves with the theorem
  - References TO the moved section from other sections (holographic, BTZ, WDW, three-layer, Onsager-WDW) — these now point backward, which is correct
  - `\ref{eq:C1-expansion-proof}` — defined within the moved block
  - `\ref{prop:wdw-lambda}` — defined within the moved block

- [ ] **Step 5:** Verify tests pass: `python3 -m pytest tests/ -q`

- [ ] **Step 6:** Commit: `git commit -m "Paper III: move Einstein theorem from §11 to §3"`

---

### Task 3: Paper III — Extract BTZ Lorentzian + spectral statistics to supplement

**Files:**
- Modify: `latex/paper-3-gravity/main.tex`
- Modify: `latex/supplement-proofs/main.tex`

- [ ] **Step 1:** Identify the Lorentzian continuation block (starts at `\paragraph{Lorentzian continuation and the BTZ horizon.}`, approximately line 1082 in the CURRENT file — line numbers will have shifted after Task 2). Runs ~54 lines to the end of the GUE/Tracy-Widom discussion.

- [ ] **Step 2:** Cut the block from Paper III. Replace with:
```latex
The Lorentzian continuation, including the analytic continuation
of the Green's function, the van Hove singularity at the threshold,
and the connection to GUE spectral statistics, is developed in
Supplement~S, \S\ref*{S-sec:btz-lorentzian}.
```

- [ ] **Step 3:** Paste the block into the supplement file under §S3.

- [ ] **Step 4:** Verify tests pass.

- [ ] **Step 5:** Commit: `git commit -m "Paper III: extract BTZ Lorentzian to supplement"`

---

### Task 4: Paper V — Swap hierarchy and CC sections

**Files:**
- Modify: `latex/paper-5-cosmology/main.tex`

- [ ] **Step 1:** Cut the electroweak hierarchy section (currently §5, starting at `\section{The electroweak hierarchy}` line 514, ending before `\section{The cosmological energy budget}` line 654). This is ~140 lines.

- [ ] **Step 2:** Paste it BEFORE the CC instanton section (currently §3, `\section{The cosmological constant from the $N=11$ instanton}` line 133). The new order will be:
  - §2: Λ₃ from fiber flux (unchanged)
  - §3: N-selection principle (move from current §4 to here)
  - §4: Electroweak hierarchy (moved from §5)
  - §5: CC from N=11 instanton (was §3)

- [ ] **Step 3:** Also cut the N-selection section (currently §4, `\section{The $N$ selection principle}` line 376) and paste it before the hierarchy section.

- [ ] **Step 4:** In the CC instanton proof, remove the forward reference to hierarchy. The proof at line ~268 says "from the $N = 7$ hierarchy exponent $\mathcal{H}_7 = ...$, Theorem~\ref{thm:hierarchy}" — this now points BACKWARD, which is correct. Verify no dangling forward refs remain.

- [ ] **Step 5:** Add a sentence at the start of the CC instanton section: "With the electroweak VEV $v = 245.9$\,GeV determined by the $N = 7$ hierarchy (Theorem~\ref{thm:hierarchy}), the $N = 11$ tunnelling action fixes the curvature radius~$\ell$."

- [ ] **Step 6:** Verify tests pass.

- [ ] **Step 7:** Commit: `git commit -m "Paper V: reorder sections for linear derivation chain"`

---

### Task 5: Paper V — Move Pell identity proof to supplement

**Files:**
- Modify: `latex/paper-5-cosmology/main.tex`
- Modify: `latex/supplement-proofs/main.tex`

- [ ] **Step 1:** Cut the appendix section (starts at `\appendix`, `\section{Proof of the Pell identity}`, line ~1145 to end of proof before `\bibliography`). This is ~90 lines.

- [ ] **Step 2:** In the main text where the Pell proof is referenced (line ~629, "Proof in Appendix~\ref{app:pell}"), change to: "The proof via the Klein quartic and Selberg trace formula is in Supplement~S, \S\ref*{S-sec:pell-proof}."

- [ ] **Step 3:** Remove the `\appendix` command from Paper V (the Pell section was the only appendix).

- [ ] **Step 4:** Paste the proof into the supplement file under §S4.

- [ ] **Step 5:** Verify tests pass.

- [ ] **Step 6:** Commit: `git commit -m "Paper V: move Pell identity proof to supplement"`

---

### Task 6: Paper I — Extract K-theory Kasparov + Bolza convergence to supplement

**Files:**
- Modify: `latex/paper-1-mathematics/main.tex`
- Modify: `latex/supplement-proofs/main.tex`

- [ ] **Step 1:** Identify the Kasparov product subsection (starts at `\subsection{The Kasparov product}` line 2703, ends before `\subsection{The gap-free regime}` line 2901). This is ~198 lines.

- [ ] **Step 2:** Cut the Kasparov subsection. Replace with:
```latex
\subsection{The Kasparov product}
\label{sec:kk-programme}

The Kasparov product
$KK(C^*(\mathbb{Z}_N),\, C^*_r(\Gamma))$ captures the
fractional $L^2$-Morse index at palindromic thresholds where
the spectral gap fails.
The full construction (assembly map, product identity, and
verification on the Bolza surface) is in
Supplement~S, \S\ref*{S-sec:kasparov}.
The main result is:
```
Then keep the fractional Morse index theorem statement (Theorem 11) and the wall-crossing formula — just remove the proofs and the Kasparov construction.

- [ ] **Step 3:** Identify the Bolza convergence narrative (starts around `Truncating $\Gamma$ to word length~$3$`, ~line 2986, runs ~85 lines through the isotypic-component analysis). Cut it and replace with:
```latex
The Bolza surface computation gives $\tau(P_-) \approx 0.644$
(details in Supplement~S, \S\ref*{S-sec:bolza-convergence}).
```

- [ ] **Step 4:** Paste both blocks into the supplement under §S1.

- [ ] **Step 5:** Verify tests pass.

- [ ] **Step 6:** Commit: `git commit -m "Paper I: extract Kasparov + Bolza to supplement"`

---

### Task 7: Paper II — Extract multi-ring proof details to supplement

**Files:**
- Modify: `latex/paper-2-physics/main.tex`
- Modify: `latex/supplement-proofs/main.tex`

- [ ] **Step 1:** In the multi-ring section, find the "Extension to all M >= 2" block (starts at `\emph{Extension to all $M \ge 2$ (complete proof).}` line ~573). This contains Part 1 (exact rational arithmetic, 12 cases), Part 2 (M >= 8 analytical), and the Mechanism paragraph. ~50 lines.

- [ ] **Step 2:** Replace with a proof sketch + supplement reference:
```latex
\emph{Complete proof.}
The twelve Thomson-stable cases ($N \le 7$, $2 \le M \le N{-}1$)
are verified by exact rational arithmetic (certificates in
Supplement~S, \S\ref*{S-sec:multiring}).
For $M \ge 8$: the inner ring's own Thomson instability
($N_{\mathrm{crit}} = 7$) produces a negative eigenvalue
that survives coupling to the outer ring
(analytical bound: Supplement~S).
The mechanism is Fourier-mode frustration: an inner ring
couples modes non-uniformly and cannot compensate all
negative eigenvalues simultaneously.
```

- [ ] **Step 3:** Paste the full proof into the supplement under §S2.

- [ ] **Step 4:** Verify tests pass.

- [ ] **Step 5:** Commit: `git commit -m "Paper II: extract multi-ring proof to supplement"`

---

### Task 8: Paper II — Expand introduction

**Files:**
- Modify: `latex/paper-2-physics/main.tex`

- [ ] **Step 1:** Replace the current 6-sentence introduction (lines 32-41) with a proper 3-paragraph introduction:
  - Paragraph 1: Physical motivation (planetary polygons, the Thomson-Onsager tension)
  - Paragraph 2: Main result (constrained minimum + quartic normal form) and five extensions
  - Paragraph 3: Applications (BEC, superconductors, quantum Hall, gravity) + series context

- [ ] **Step 2:** Verify tests pass.

- [ ] **Step 3:** Commit: `git commit -m "Paper II: expand introduction with physical motivation"`

---

### Task 9: Paper IV — Split consistency section

**Files:**
- Modify: `latex/paper-4-field-theory/main.tex`

- [ ] **Step 1:** Find the Higgs mass paragraph within the consistency section (currently inside `\subsection{Gauge-theory consistency}`, the `\paragraph{Higgs mass.}` block). Promote it to its own section after fermion masses: `\section{The Higgs mass}`.

- [ ] **Step 2:** Find the nonlinear Einstein theorem (currently inside `\subsection{Gravitational consistency}`, `\begin{theorem}[Full nonlinear $4$D Einstein equations]`). Keep it in the gravitational consistency subsection but ensure it has appropriate prominence.

- [ ] **Step 3:** Rename `\section{Consistency checks}` to `\section{Consistency checks and predictions}`.

- [ ] **Step 4:** Verify tests pass.

- [ ] **Step 5:** Commit: `git commit -m "Paper IV: promote Higgs mass, rename consistency section"`

---

### Task 10: Paper I — Move constrained-minimum theorem

**Files:**
- Modify: `latex/paper-1-mathematics/main.tex`

- [ ] **Step 1:** Find Theorem 4 (constrained energy minimum, `\begin{theorem}[Constrained energy minimum]`, line ~383) and Remark 5 (unconstrained saddle, line ~441) in Section 2.

- [ ] **Step 2:** Cut both and paste at the end of Section 3 (after the sign rule proof, before Section 4). Add a transition sentence: "The sign rule establishes $H''(0) < 0$; we now show the angular-impulse constraint rescues stability."

- [ ] **Step 3:** Verify all \ref{thm:constrained-min} cross-references still resolve.

- [ ] **Step 4:** Verify tests pass.

- [ ] **Step 5:** Commit: `git commit -m "Paper I: move constrained-min theorem to after sign rule"`

---

### Task 11: Final verification and cleanup

- [ ] **Step 1:** Run full test suite: `python3 -m pytest tests/ -q`
- [ ] **Step 2:** Verify line counts for all papers: `wc -l latex/paper-*/main.tex latex/supplement-proofs/main.tex`
- [ ] **Step 3:** Grep for any dangling `\ref*{S-` references that point to labels not yet in the supplement.
- [ ] **Step 4:** Update `PICKUP_20260331_session3.md` with final state.
- [ ] **Step 5:** Commit: `git commit -m "Final verification after structural reorder"`
