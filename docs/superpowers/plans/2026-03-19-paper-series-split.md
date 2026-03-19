# Paper Series Split Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Split the monolithic 59-page paper (`latex/paper/main.tex`, 4332 lines) into 5 independently compilable PDFs with `xr-hyper` cross-references.

**Architecture:** Extract line ranges from the monolith into per-paper `main.tex` files, each including a shared preamble. Cross-paper references use `xr-hyper` with prefixes (I-, II-, III-, A-). A build script compiles all papers in dependency order.

**Tech Stack:** LaTeX, xr-hyper, pdflatex, bibtex, bash

---

## Source Line Ranges (from current `latex/paper/main.tex`)

| Paper | Lines | Content |
|-------|-------|---------|
| 0: Overview | 1-30 (preamble) + 108-205 (preface+abstract) | Preface, abstract |
| 1: Mathematics | 206-285 (intro) + 286-1592 (Part I) | §§1-6 |
| 2: Physics | 1593-3255 (Parts II+III) | §§7-15 |
| 3: Planets | 3256-4205 (Part IV + Discussion) | §§16-21 |
| A: Appendices | 4206-4332 (appendix + bib) | Derivations, code |

## Files to Create

```
latex/shared/preamble.tex         # Common packages, theorems, macros
latex/shared/refs.bib             # Shared bibliography (copy from paper/)
latex/paper-0-overview/main.tex   # Paper 0
latex/paper-1-mathematics/main.tex # Paper 1
latex/paper-2-physics/main.tex    # Paper 2
latex/paper-3-planets/main.tex    # Paper 3
latex/paper-A-appendices/main.tex # Paper A
latex/build.sh                    # Build all in order
```

## Cross-Reference Conversion

Within a paper: `\ref{thm:sign-rule}` (unchanged).
Across papers: `\ref{I-thm:sign-rule}` (add prefix).

The 54 cross-part references need prefix conversion:
- Paper 2 referencing Paper 1: add `I-` prefix (5 refs)
- Paper 3 referencing Paper 1: add `I-` prefix (9 refs)
- Paper 3 referencing Paper 2: add `II-` prefix (8 refs)
- Paper 3 referencing Paper 3 Extensions: add `II-` prefix (8 refs)
- Paper 1 referencing forward: add `II-` or `III-` prefix (7 refs)
- All papers referencing appendices: add `A-` prefix

---

### Task 1: Create shared preamble and directory structure

**Files:**
- Create: `latex/shared/preamble.tex`
- Create: `latex/shared/refs.bib` (copy from `latex/paper/refs.bib`)
- Create: directories `latex/paper-{0-overview,1-mathematics,2-physics,3-planets,A-appendices}`

- [ ] **Step 1: Create directories**
```bash
mkdir -p latex/shared latex/paper-{0-overview,1-mathematics,2-physics,3-planets,A-appendices}
```

- [ ] **Step 2: Create shared preamble**

Write `latex/shared/preamble.tex`:
```latex
\documentclass[12pt, a4paper]{article}
\usepackage{amsmath, amsthm, amssymb, mathtools}
\usepackage[margin=1in]{geometry}
\usepackage{xr-hyper}
\usepackage[colorlinks=true,linkcolor=blue,citecolor=blue]{hyperref}
\usepackage{cleveref}
\usepackage{graphicx, subcaption}
\usepackage{natbib}
\usepackage{booktabs}

\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{corollary}[theorem]{Corollary}
\newtheorem{definition}{Definition}[section]
\newtheorem{remark}{Remark}[section]
\numberwithin{equation}{section}

\newcommand{\dd}{\mathrm{d}}
\newcommand{\seriestitle}{Why Rotating Fluids Make Polygons}
```

- [ ] **Step 3: Copy bibliography**
```bash
cp latex/paper/refs.bib latex/shared/refs.bib
```

- [ ] **Step 4: Commit**
```bash
git add latex/shared/ latex/paper-*/
git commit -m "series-split: create directory structure and shared preamble"
```

---

### Task 2: Extract Paper 1 — Mathematics

**Files:**
- Create: `latex/paper-1-mathematics/main.tex`
- Source: `latex/paper/main.tex` lines 206-1592

- [ ] **Step 1: Write a Python script to extract Paper 1**

The script reads the monolith, extracts lines 206-1592 (Introduction + Part I), wraps with the shared preamble, adds a per-paper title/abstract, and writes to `latex/paper-1-mathematics/main.tex`.

Key transformations:
- Replace `\input{...}` of preamble with `\input{../shared/preamble}`
- Add `\externaldocument[II-]{../paper-2-physics/main}` etc.
- Add paper-specific title and abstract
- Forward references to Parts II-IV get prefixed (I→II, etc.)
- Keep all `\label{}` names unchanged
- Add `\bibliography{../shared/refs}` at end

- [ ] **Step 2: Run the extraction script**

- [ ] **Step 3: Compile Paper 1 standalone**
```bash
cd latex/paper-1-mathematics && pdflatex main && bibtex main && pdflatex main && pdflatex main
```
Expected: compiles with some `??` for cross-paper refs, 0 errors.

- [ ] **Step 4: Verify page count (~18-20 pages)**

- [ ] **Step 5: Commit**
```bash
git add latex/paper-1-mathematics/
git commit -m "series-split: extract Paper 1 — Mathematical Foundations"
```

---

### Task 3: Extract Paper 2 — Physics

**Files:**
- Create: `latex/paper-2-physics/main.tex`
- Source: `latex/paper/main.tex` lines 1593-3255

- [ ] **Step 1: Extract lines 1593-3255** (Parts II + III)

Key: references back to Part I (theorems, propositions) get `I-` prefix.
References to Part IV get `III-` prefix.

- [ ] **Step 2: Add paper-specific title, abstract, xr declarations**

- [ ] **Step 3: Compile standalone**
```bash
cd latex/paper-2-physics && pdflatex main && bibtex main && pdflatex main && pdflatex main
```

- [ ] **Step 4: Verify page count (~20-22 pages)**

- [ ] **Step 5: Commit**
```bash
git add latex/paper-2-physics/
git commit -m "series-split: extract Paper 2 — Classical and Quantum Physics"
```

---

### Task 4: Extract Paper 3 — Planets

**Files:**
- Create: `latex/paper-3-planets/main.tex`
- Source: `latex/paper/main.tex` lines 3256-4205

- [ ] **Step 1: Extract lines 3256-4205** (Part IV + Discussion)

Key: heavy cross-referencing to Papers 1 and 2. ~23 refs need prefixing.

- [ ] **Step 2: Add paper-specific title, abstract, xr declarations**

- [ ] **Step 3: Compile standalone**

- [ ] **Step 4: Verify page count (~16-18 pages)**

- [ ] **Step 5: Commit**
```bash
git add latex/paper-3-planets/
git commit -m "series-split: extract Paper 3 — Planetary Applications"
```

---

### Task 5: Extract Paper A — Appendices

**Files:**
- Create: `latex/paper-A-appendices/main.tex`
- Source: `latex/paper/main.tex` lines 4206-4332 + `docs/OPEN_PROBLEMS.md`

- [ ] **Step 1: Extract appendix content**

Add the C₁ derivation, code availability section, and convert OPEN_PROBLEMS.md to a LaTeX appendix.

- [ ] **Step 2: Compile standalone**

- [ ] **Step 3: Commit**
```bash
git add latex/paper-A-appendices/
git commit -m "series-split: extract Paper A — Appendices"
```

---

### Task 6: Create Paper 0 — Overview

**Files:**
- Create: `latex/paper-0-overview/main.tex`
- Source: Preface (lines 108-205), Abstract (lines 28-100)

- [ ] **Step 1: Write Paper 0**

Contains:
- The full preface (Gordon's personal introduction)
- The full abstract
- A "Guide to the Series" section explaining what each paper covers
- A combined table of contents (manually listing key sections from all papers)

- [ ] **Step 2: Compile standalone**

- [ ] **Step 3: Commit**
```bash
git add latex/paper-0-overview/
git commit -m "series-split: create Paper 0 — Overview"
```

---

### Task 7: Build script and full verification

**Files:**
- Create: `latex/build.sh`

- [ ] **Step 1: Write build script**

```bash
#!/bin/bash
set -e
echo "Building Paper 1: Mathematics..."
cd paper-1-mathematics && pdflatex -interaction=nonstopmode main && bibtex main && pdflatex -interaction=nonstopmode main && pdflatex -interaction=nonstopmode main && cd ..
echo "Building Paper 2: Physics..."
cd paper-2-physics && pdflatex -interaction=nonstopmode main && bibtex main && pdflatex -interaction=nonstopmode main && pdflatex -interaction=nonstopmode main && cd ..
echo "Building Paper 3: Planets..."
cd paper-3-planets && pdflatex -interaction=nonstopmode main && bibtex main && pdflatex -interaction=nonstopmode main && pdflatex -interaction=nonstopmode main && cd ..
echo "Building Paper A: Appendices..."
cd paper-A-appendices && pdflatex -interaction=nonstopmode main && bibtex main && pdflatex -interaction=nonstopmode main && pdflatex -interaction=nonstopmode main && cd ..
echo "Building Paper 0: Overview..."
cd paper-0-overview && pdflatex -interaction=nonstopmode main && pdflatex -interaction=nonstopmode main && cd ..
echo "All papers built successfully."
```

- [ ] **Step 2: Run full build**
```bash
cd latex && chmod +x build.sh && ./build.sh
```

- [ ] **Step 3: Verify all cross-references resolve**
```bash
for d in paper-{0-overview,1-mathematics,2-physics,3-planets,A-appendices}; do
  echo "=== $d ===" && grep -c "undefined" $d/main.log || echo "0 undefined"
done
```
Expected: 0 undefined references in all papers (except possibly Fetter2009).

- [ ] **Step 4: Verify total page count**
Sum of all PDFs should be ~59-62 pages (close to the original 59).

- [ ] **Step 5: Commit**
```bash
git add latex/build.sh
git commit -m "series-split: build script and full verification"
```

---

### Task 8: Cross-reference conversion (the hard part)

This task runs DURING Tasks 2-5 but is separated here for clarity.

**The 54 cross-part references need manual conversion:**

For each paper, grep for `\ref{` and check if the label is defined
in that paper. If not, add the appropriate prefix:

```bash
# In paper-2-physics: find refs to Paper 1 labels
grep -n '\\ref{' latex/paper-2-physics/main.tex | while read line; do
  label=$(echo "$line" | grep -oP '\\ref\{\K[^}]+')
  if ! grep -q "\\label{$label}" latex/paper-2-physics/main.tex; then
    echo "CROSS-REF: $line -> needs prefix"
  fi
done
```

For each cross-ref found:
- If the label is in Paper 1: change `\ref{label}` to `\ref{I-label}`
- If the label is in Paper 2: change to `\ref{II-label}`
- If the label is in Paper 3: change to `\ref{III-label}`
- If the label is in Appendices: change to `\ref{A-label}`

This is mechanical but must be done carefully.

---

## Verification Checklist

After all tasks:
- [ ] Each paper compiles independently with `pdflatex`
- [ ] Full build (`build.sh`) produces 5 PDFs with 0 undefined refs
- [ ] All `\label` names preserved (no renames)
- [ ] Cross-paper `\ref{I-...}` resolve correctly
- [ ] Total page count ≈ 59-62
- [ ] All 398 Python tests still pass (code unchanged)
- [ ] The original monolith `latex/paper/main.tex` is preserved (not deleted)
