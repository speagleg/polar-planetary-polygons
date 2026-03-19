# Paper Series Split — Design Spec

## Goal

Split the monolithic 59-page paper into 5 independently compilable PDFs
(overview, mathematics, physics, planets, appendices) with automatic
cross-references via `xr-hyper`. Each paper can be reviewed, edited, and
compiled independently. A build script compiles all in dependency order.
A combined PDF concatenates everything for eventual submission.

## Directory Structure

```
latex/
├── shared/
│   ├── preamble.tex          # Common packages, theorem defs, macros
│   ├── refs.bib              # Shared bibliography
│   └── xr-setup.tex          # \externaldocument declarations (per-paper)
├── paper-0-overview/
│   ├── main.tex              # Preface + Abstract + Series ToC
│   └── main.pdf
├── paper-1-mathematics/
│   ├── main.tex              # Part I: §§1-6
│   └── main.pdf
├── paper-2-physics/
│   ├── main.tex              # Part II+III: §§7-15
│   └── main.pdf
├── paper-3-planets/
│   ├── main.tex              # Part IV + Discussion: §§16-21
│   └── main.pdf
├── paper-A-appendices/
│   ├── main.tex              # Appendices + Open Problems + Code
│   └── main.pdf
├── combined/
│   ├── main.tex              # \input concatenation of all
│   └── main.pdf
└── build.sh                  # Compiles all in order
```

## Content Split

### Paper 0: Overview (4-5 pages)
- `\section*{Preface}` (Gordon's personal introduction)
- `\begin{abstract}` (the full abstract)
- Series introduction: what each paper covers, how to read them
- Combined table of contents (listing all sections across all papers)

### Paper 1: Mathematical Foundations (18-20 pages)
Current §§1-6 plus the Havelock appendix content (already moved to §4):
- §1: Introduction (the scientific question)
- §2: The logarithmic interaction: uniqueness and symmetry
  - Dilation invariance, Möbius covariance, RG classification
  - Loxodromic thread (Remark 2.3)
- §3: The sign rule for general pairwise interactions
- §4: The Havelock identity and its metric-independence
  - Classical identity, Riemannian Havelock, representation theory remark
- §5: Stability thresholds on constant-curvature surfaces
  - Sphere, hyperbolic plane, curvature-stability dichotomy
  - Morse index theorem, spectral flow
- §6: Algebraic structure of the stability boundary
  - Field extensions, algebraic-integer classification, Pell connection
  - Golden ratio, binary subdivision, continued fractions
  - Regulator, Galois action

### Paper 2: Classical and Quantum Physics (20-22 pages)
Current §§7-15:
- §7: Point vortex dynamics on a 2D surface
- §8: The constrained energy landscape
- §9: Central vortex stabilization
- §10: The N=7 bifurcation (with Landau interpretation)
- §11: Multi-ring configurations and center-ring dichotomy
- §12: From point vortices to continuous vorticity: the blob bridge
  - Inertia preservation, concentration condition
  - Corollaries for N≤6 and N=7
- §13: Finite Rossby deformation radius: K₀ interaction
  - K₀ + central vortex table
- §14: Circulation disorder and robustness
- §15: Predictions for quantum systems: BEC vortex clusters
  - Golden ratio on hyperbolic BEC lattice

### Paper 3: Planetary and Astrophysical Applications (16-18 pages)
Current §§16-21:
- §16: The three-scale selection mechanism
- §17: Wavenumber selection: constraint-intersection principle
  - Proposition (constraint-intersection), Remark (Laplacian unification)
  - Energy monotonicity and max-N selection
- §18: Saturn's hexagon
  - Rossby stationarity, eigenvalue branch disconnection
  - Quantitative bridge (Saturn σ/R verification)
- §19: Jupiter's polar polygons
- §20: Broader observational context and predictions
  - Polygon quality metrics, Neptune prediction, Uranus
- §21: Discussion and limitations
  - Why 2D, what is novel, limitations and scope
  - Dynamical maintenance, two-timescale Onsager-Arnold resolution
  - Toward first-principles prediction

### Paper A: Appendices (6-8 pages)
- Appendix A: Derivation of C₁(H², ξ)
- Appendix B: Code availability and reproducibility
- Appendix C: Open problems (from docs/OPEN_PROBLEMS.md)

## Cross-Reference Mechanism

### Shared preamble (`shared/preamble.tex`)
```latex
\documentclass[12pt, a4paper]{article}
\usepackage{amsmath, amsthm, amssymb, mathtools}
\usepackage[margin=1in]{geometry}
\usepackage{xr-hyper}
\usepackage[colorlinks=true]{hyperref}
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

% Paper series title
\newcommand{\seriestitle}{Why Rotating Fluids Make Polygons}
```

### Per-paper xr declarations
Each paper includes (e.g., Paper 2):
```latex
\input{../shared/preamble}
\externaldocument[I-]{../paper-1-mathematics/main}
\externaldocument[III-]{../paper-3-planets/main}
\externaldocument[A-]{../paper-A-appendices/main}
```

Cross-references use prefixes: `\ref{I-thm:sign-rule}` renders as
the theorem number from Paper 1. If Paper 1 hasn't been compiled,
it shows `??` (harmless for individual review).

### Label preservation
All existing `\label{...}` names are PRESERVED unchanged. The `xr`
prefix (e.g., `I-`) is added only at the `\ref` call site, not at
the `\label` definition. This means:
- Within a paper: `\ref{thm:sign-rule}` works as before
- Across papers: `\ref{I-thm:sign-rule}` with the paper prefix

## Build Process

### `latex/build.sh`
```bash
#!/bin/bash
# Build all papers in dependency order
cd paper-1-mathematics && pdflatex main && bibtex main && pdflatex main && pdflatex main && cd ..
cd paper-2-physics && pdflatex main && bibtex main && pdflatex main && pdflatex main && cd ..
cd paper-3-planets && pdflatex main && bibtex main && pdflatex main && pdflatex main && cd ..
cd paper-A-appendices && pdflatex main && bibtex main && pdflatex main && pdflatex main && cd ..
cd paper-0-overview && pdflatex main && pdflatex main && cd ..
# Optional: combined
# cd combined && pdflatex main && bibtex main && pdflatex main && pdflatex main && cd ..
```

### Single-paper build (for review)
```bash
cd latex/paper-2-physics && pdflatex main && pdflatex main
```
Cross-refs to other papers show `??` but the paper compiles and
renders correctly otherwise.

## Section Numbering

Each paper restarts numbering at §1. In cross-references, the paper
is identified by the prefix:
- "Theorem I-2.1" = Theorem 2.1 in Paper 1
- "Proposition III-17.1" = Proposition 17.1 in Paper 3

Within a paper, no prefix is needed: "Theorem 2.1" suffices.

## Per-Paper Abstracts

Each paper gets a 1-paragraph abstract:

- **Paper 1**: "We establish the mathematical foundations..."
- **Paper 2**: "Building on the mathematical framework of Paper I..."
- **Paper 3**: "Applying the constraint-intersection principle..."
- **Paper A**: "This appendix collects technical derivations..."

## Migration Checklist

For each paper:
1. Extract the relevant `\section{}` blocks from the monolith
2. Add `\input{../shared/preamble}` and xr declarations
3. Add per-paper title, author, abstract
4. Convert cross-part `\ref{}` to prefixed `\ref{I-...}` etc.
5. Add `\bibliography{../shared/refs}` at the end
6. Compile and verify: 0 undefined references within the paper
7. Compile full build and verify: 0 undefined cross-references

## What Does NOT Change

- All `\label` names stay exactly the same
- All theorem/proposition/corollary content unchanged
- All proofs unchanged
- Section ordering within each paper unchanged
- Bibliography entries unchanged
- The combined PDF reproduces the current monolith exactly
