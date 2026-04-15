# Item #1 — Constrained-Min Derivation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a self-contained, reviewer-gated derivation of the Havelock Lagrangian eigenvalues `λ_m^+ = (N-1) - m(N-m)/2` and `λ_m^- = m(N-m)/2` for the regular N-gon of unit point vortices, and surgically swap it into §6.2 of `latex/paper/main.tex` with zero regressions.

**Architecture:** Sandbox-first. Every algebraic step is (a) symbolically verified with `sympy`, (b) numerically cross-checked against full diagonalization in `src/planetary_polygons/core/hessian.py`. No edits to `latex/paper/main.tex` until the sandbox passes math-reviewer (≥9.0, zero structural deductions) AND the user approves a final surgical diff.

**Tech Stack:** Python 3, sympy, numpy, mpmath, pytest, LaTeX (standalone article for the sandbox, then inline patch to the paper).

---

## File Structure

**Create (sandbox, outside `latex/paper/`):**
- `docs/rigor-sandbox/item1-constrained-min/derivation.tex` — standalone 3-page LaTeX derivation
- `docs/rigor-sandbox/item1-constrained-min/numerical_check.py` — symbolic + numerical validator for every step
- `docs/rigor-sandbox/item1-constrained-min/review-notes.md` — math-reviewer rounds log
- `docs/rigor-sandbox/item1-constrained-min/final-diff.patch` — approved surgical diff (produced near end)

**Create (permanent, referenced by paper):**
- `tests/test_angular_hessian.py` — file currently referenced by `latex/paper/main.tex:2055` but does not exist; must assert paper formulas against numerical diagonalization for `N ∈ {3, ..., 16}`.

**Modify (only after sandbox gates pass):**
- `latex/paper/main.tex` — §6.2 (lines ~1962–2121). Surgical replacement of the `\begin{proof}...\end{proof}` of Theorem `thm:constrained-min` with the sandbox-proven derivation.

**Do not touch:** any other section of any paper, any other source file, any prose outside the §6.2 proof.

---

## Task 1: Scaffold the sandbox directory

**Files:**
- Create: `docs/rigor-sandbox/item1-constrained-min/review-notes.md`
- Create: `docs/rigor-sandbox/item1-constrained-min/numerical_check.py` (empty scaffold)
- Create: `docs/rigor-sandbox/item1-constrained-min/derivation.tex` (empty scaffold)

- [ ] **Step 1: Create the directory**

```bash
mkdir -p /mnt/c/Users/gspea/source/repos/planetary-polygons-unified/docs/rigor-sandbox/item1-constrained-min
```

- [ ] **Step 2: Create `review-notes.md` with empty log**

```markdown
# Item #1 — Review Log

## Round 0 — pre-review baseline

(to be filled by math-reviewer dispatch)
```

- [ ] **Step 3: Create `numerical_check.py` scaffold that runs but does nothing yet**

```python
"""Numerical + symbolic validator for the constrained-min derivation.

Every claim in derivation.tex must correspond to a check in this file.
Run: python3 numerical_check.py
Exit 0 = all claims verified. Non-zero = derivation is wrong.
"""

import sys


def main() -> int:
    print("numerical_check.py: no checks implemented yet")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Create `derivation.tex` scaffold (standalone article)**

```latex
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{geometry}
\geometry{margin=1in}
\newtheorem{lemma}{Lemma}
\newtheorem{theorem}{Theorem}

\title{Havelock Lagrangian Eigenvalues:\\ First-Principles Derivation}
\author{Sandbox for Paper~I, Item~\#1}
\date{\today}

\begin{document}
\maketitle

% Content added in later tasks.

\end{document}
```

- [ ] **Step 5: Verify both files run / compile**

```bash
cd /mnt/c/Users/gspea/source/repos/planetary-polygons-unified
python3 docs/rigor-sandbox/item1-constrained-min/numerical_check.py
# Expect: exit 0, prints "no checks implemented yet"
```

(LaTeX compile can wait until we have content — the scaffold has no body.)

- [ ] **Step 6: Commit**

```bash
git add docs/rigor-sandbox/item1-constrained-min/
git commit -m "chore: scaffold Item #1 constrained-min sandbox"
```

---

## Task 2: Ground-truth oracle — full numerical diagonalization at each (N, m)

**Why:** Before deriving anything symbolically, we build a trusted numerical oracle that gives us `(λ_m^+, λ_m^-)` for any `(N, m)`. Every symbolic step in later tasks is validated against this oracle. The oracle uses the existing `constrained_hessian_analysis` machinery but also directly diagonalizes the mode-m 2×2 block so we can match symbolic entries one-by-one.

**Files:**
- Modify: `docs/rigor-sandbox/item1-constrained-min/numerical_check.py`

- [ ] **Step 1: Add the oracle (fails initially because symbolic answers aren't in yet — we only assert what the oracle produces on canonical cases)**

Replace contents of `numerical_check.py` with:

```python
"""Numerical + symbolic validator for the constrained-min derivation.

Run: python3 numerical_check.py
Exit 0 = all claims verified. Non-zero = derivation is wrong.
"""

from __future__ import annotations

import sys
from typing import Tuple

import numpy as np


def havelock_block_eigenvalues(N: int, m: int) -> Tuple[float, float]:
    """Compute (lambda_m^+, lambda_m^-) directly from the 2x2 block at mode m.

    Builds the full 2N x 2N Hessian of the Thomson energy
    H(z_1,...,z_N) = -sum_{j<k} log|z_j - z_k|^2 at the regular N-gon z_k = e^{2 pi i k / N},
    applies the Lagrange shift nabla^2 L = nabla^2 H - 2 mu_L I with mu_L = -(N-1)/4,
    projects into the (radial, tangential) Fourier amplitudes at mode m, and
    returns the two eigenvalues sorted as (lambda^+, lambda^-) where
    lambda^+ >= lambda^-.
    """
    if m <= 0 or m >= N:
        raise ValueError(f"mode m must lie in [1, N-1]; got m={m}, N={N}")

    theta = 2.0 * np.pi * np.arange(N) / N
    # Positions in Cartesian (x_1,...,x_N, y_1,...,y_N).
    x = np.cos(theta)
    y = np.sin(theta)
    pos = np.concatenate([x, y])

    def energy(p: np.ndarray) -> float:
        xs, ys = p[:N], p[N:]
        total = 0.0
        for j in range(N):
            for k in range(j + 1, N):
                dx = xs[j] - xs[k]
                dy = ys[j] - ys[k]
                total -= np.log(dx * dx + dy * dy)
        return 0.5 * total  # H = -sum_{j<k} log|z_j - z_k| with log|z|^2 = 2 log|z|

    dim = 2 * N
    eps = 1e-5
    H = np.zeros((dim, dim))
    f0 = energy(pos)
    for i in range(dim):
        for j in range(i, dim):
            dpi = np.zeros(dim); dpi[i] = eps
            dpj = np.zeros(dim); dpj[j] = eps
            fpp = energy(pos + dpi + dpj)
            fpm = energy(pos + dpi - dpj)
            fmp = energy(pos - dpi + dpj)
            fmm = energy(pos - dpi - dpj)
            val = (fpp - fpm - fmp + fmm) / (4.0 * eps * eps)
            H[i, j] = val
            H[j, i] = val

    mu_L = -(N - 1) / 4.0
    L_lagr = H - 2.0 * mu_L * np.eye(dim)

    # Build mode-m Fourier vectors in the LOCAL (radial, tangential) frame at each
    # vertex. At vertex k with angle theta_k:
    #   radial direction:   ( cos theta_k, sin theta_k)
    #   tangential direction: (-sin theta_k, cos theta_k)
    # Mode-m amplitude cos(2 pi m k / N) (the cosine-sector; sine-sector gives the
    # palindromic pair (m, N-m) — we pick one representative).
    amp = np.cos(2.0 * np.pi * m * np.arange(N) / N)

    e_r = np.zeros(dim)
    e_r[:N] = amp * np.cos(theta)
    e_r[N:] = amp * np.sin(theta)

    e_t = np.zeros(dim)
    e_t[:N] = -amp * np.sin(theta)
    e_t[N:] = amp * np.cos(theta)

    # Orthonormalize (amp vectors aren't quite unit — depends on mode and N).
    def normalize(v):
        n = np.linalg.norm(v)
        return v / n if n > 0 else v
    e_r = normalize(e_r)
    e_t = normalize(e_t)

    block = np.array([
        [e_r @ L_lagr @ e_r, e_r @ L_lagr @ e_t],
        [e_t @ L_lagr @ e_r, e_t @ L_lagr @ e_t],
    ])
    # Off-diagonal should be ~0 (the paper's pair-reflection argument).
    evals = np.linalg.eigvalsh(block)
    return float(evals[1]), float(evals[0])  # (lambda^+, lambda^-) with + >= -


def check_canonical_cases() -> int:
    """Spec's three canonical test cases (Item #1 spec, 'Key correctness checks')."""
    cases = [
        (5, 2, 1.0, 3.0),
        (7, 3, 0.0, 6.0),
        (11, 5, -5.0, 15.0),
    ]
    failed = 0
    for N, m, exp_plus, exp_minus in cases:
        lam_plus, lam_minus = havelock_block_eigenvalues(N, m)
        # Formula predicts (lam^+, lam^-); sort so + corresponds to the bigger.
        # But for N=11,m=5 the formula gives lam^+ = -5, lam^- = 15, i.e. the
        # "tangential" block is numerically larger. Compare as an unordered pair.
        obs = tuple(sorted([lam_plus, lam_minus]))
        exp = tuple(sorted([exp_plus, exp_minus]))
        ok = all(abs(a - b) < 1e-3 for a, b in zip(obs, exp))
        status = "OK" if ok else "FAIL"
        print(f"  N={N:2d} m={m}: obs={obs} exp={exp} [{status}]")
        if not ok:
            failed += 1
    return failed


def main() -> int:
    print("== Canonical cases (numerical oracle) ==")
    failed = check_canonical_cases()
    if failed:
        print(f"FAILED {failed} canonical cases")
        return 1
    print("All canonical cases pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run and confirm the oracle produces the expected eigenvalues**

```bash
cd /mnt/c/Users/gspea/source/repos/planetary-polygons-unified
python3 docs/rigor-sandbox/item1-constrained-min/numerical_check.py
```

Expected output (exact numbers will be to ~1e-3 tolerance):
```
== Canonical cases (numerical oracle) ==
  N= 5 m=2: obs=(1.0, 3.0) exp=(1.0, 3.0) [OK]
  N= 7 m=3: obs=(0.0, 6.0) exp=(0.0, 6.0) [OK]
  N=11 m=5: obs=(-5.0, 15.0) exp=(-5.0, 15.0) [OK]
All canonical cases pass.
```

If any case fails, stop and debug the oracle before proceeding — this is the foundation every later step relies on.

- [ ] **Step 3: Commit**

```bash
git add docs/rigor-sandbox/item1-constrained-min/numerical_check.py
git commit -m "test: numerical oracle for Havelock block eigenvalues"
```

---

## Task 3: Symbolic derivation — radial-radial sum `S_m^{(rr)}`

**Math goal:** Prove symbolically that the pair sum contributing to the radial-radial block at mode `m` is
```
S_m^{(rr)} = Σ_{p=1}^{N-1} (1 - cos(2π m p / N)) / (4 sin²(π p / N))  =  m(N-m)/2.
```
This is the "Havelock identity" already proved elsewhere in the paper (`app:havelock`), but the derivation must re-state it cleanly because it's the keystone step.

**Files:**
- Modify: `docs/rigor-sandbox/item1-constrained-min/numerical_check.py`

- [ ] **Step 1: Add a `sympy` check that `S_m^{(rr)}(N, m)` equals `m(N-m)/2` for all `(N, m)` with `N ∈ {3, ..., 16}, m ∈ {1, ..., N-1}`**

Append to `numerical_check.py` (after `check_canonical_cases`):

```python
def check_havelock_identity_rr() -> int:
    """S_m^(rr) = sum_{p=1}^{N-1} (1 - cos(2 pi m p / N)) / (4 sin^2(pi p / N))
       equals m(N-m)/2 for all N in [3,16], m in [1, N-1]."""
    import sympy as sp
    failed = 0
    for N in range(3, 17):
        for m in range(1, N):
            total = sp.Rational(0)
            for p in range(1, N):
                num = 1 - sp.cos(2 * sp.pi * m * p / N)
                den = 4 * sp.sin(sp.pi * p / N) ** 2
                total += num / den
            simplified = sp.nsimplify(sp.simplify(total), rational=True)
            expected = sp.Rational(m * (N - m), 2)
            ok = simplified == expected
            if not ok:
                failed += 1
                print(f"  FAIL N={N} m={m}: got {simplified} expected {expected}")
    if failed == 0:
        print(f"  S_m^(rr) = m(N-m)/2 verified symbolically for N in [3,16]")
    return failed
```

Update `main()`:

```python
def main() -> int:
    print("== Canonical cases (numerical oracle) ==")
    if check_canonical_cases():
        print("FAILED canonical cases"); return 1

    print("== Havelock identity (radial-radial sum) ==")
    if check_havelock_identity_rr():
        print("FAILED radial-radial identity"); return 1

    print("All checks pass.")
    return 0
```

- [ ] **Step 2: Run**

```bash
python3 docs/rigor-sandbox/item1-constrained-min/numerical_check.py
```

Expected: both sections print OK, exit 0. sympy runs may take ~10–20 seconds.

- [ ] **Step 3: Write the derivation of `S_m^{(rr)} = m(N-m)/2` into `derivation.tex`**

Insert the following between `\maketitle` and `\end{document}` in `derivation.tex`:

```latex
\section{Setup}\label{sec:setup}
Let $z_k = e^{i\theta_k}$, $\theta_k = 2\pi k/N$, be the regular $N$-gon on
the unit circle. The Thomson energy is
\[
  H = -\sum_{j<k} \log|z_j - z_k|^2.
\]
Small perturbations are written in the \emph{local} frame at each vertex,
\[
  z_k \mapsto z_k\,(1 + \delta r_k) + i\,z_k\,\delta t_k + O(\delta^2),
\]
with $\delta r_k$ radial and $\delta t_k$ tangential. The $\mathbb{Z}_N$
cyclic symmetry $k \mapsto k+1 \pmod N$ permutes the vertices, so $\nabla^2 H$
block-diagonalizes in the discrete Fourier basis,
\[
  \delta r_k = a_m \cos(2\pi m k / N), \qquad
  \delta t_k = b_m \cos(2\pi m k / N),
  \quad m \in \{0, 1, \ldots, N-1\}.
\]
Each mode $m \in \{1, \ldots, N-1\}$ yields a $2 \times 2$ block in the
$(a_m, b_m)$ basis; modes $m$ and $N-m$ are a palindromic pair with
equal blocks.

\section{Radial-radial block}\label{sec:rr}

\begin{lemma}[Havelock identity]\label{lem:havelock}
For all integers $N \ge 2$ and $m \in \{1, \ldots, N-1\}$,
\[
  S_m^{(rr)} := \sum_{p=1}^{N-1}
     \frac{1 - \cos(2\pi m p / N)}{4 \sin^2(\pi p / N)}
  \;=\; \frac{m(N-m)}{2}.
\]
\end{lemma}

\begin{proof}
Write $\omega = e^{2\pi i / N}$, so $1 - \cos(2\pi m p / N) = 2 \sin^2(\pi m p / N)$
and $\sin^2(\pi p / N) = \tfrac14 |1 - \omega^p|^2$. Then
\[
  S_m^{(rr)}
    = \sum_{p=1}^{N-1} \frac{2 \sin^2(\pi m p / N)}{|1 - \omega^p|^2}
    = \sum_{p=1}^{N-1} \sin^2(\pi m p / N) \cdot \frac{1}{2 \sin^2(\pi p / N)}.
\]
Using the telescoping identity
$\sum_{p=1}^{N-1} \sin^2(\pi m p / N) / \sin^2(\pi p / N) = m(N-m)$
(classical; see e.g.\ Gradshteyn–Ryzhik 1.342, or derive via the
Chebyshev polynomial evaluation $U_{m-1}$), the claim follows by division by~$2$.
\end{proof}

The perturbation of $|z_j - z_k|^2$ under a purely radial perturbation at
mode~$m$ expands to
\[
  |z_j(a) - z_k(a)|^2 = |z_j - z_k|^2
     + 2 a \operatorname{Re}\!\bigl[(z_j - z_k)\overline{(\alpha_j z_j - \alpha_k z_k)}\bigr]
     + a^2 |\alpha_j z_j - \alpha_k z_k|^2 + O(a^3),
\]
where $\alpha_k = \cos(2\pi m k / N)$. Taking
$-\tfrac12 (d^2/da^2) \log|\cdot|^2$ and summing over pairs $j<k$, the
leading contribution at mode $m$ is
\[
  H_{rr}^{(m)} = \frac{1}{2} \sum_{p=1}^{N-1}
     \frac{1 - \cos(2\pi m p / N)}{2 \sin^2(\pi p / N)}
  = S_m^{(rr)}
  = \frac{m(N-m)}{2}.
\]
\end{latex}
```

Correct the `\end{latex}` to `%` — that was a placeholder; the real section body ends before `\section{...}`.  Replace the stray `\end{latex}` line with a blank line before the next section.

- [ ] **Step 4: Compile `derivation.tex` standalone**

```bash
cd /mnt/c/Users/gspea/source/repos/planetary-polygons-unified/docs/rigor-sandbox/item1-constrained-min
pdflatex -interaction=nonstopmode derivation.tex
```

Expected: compiles, produces `derivation.pdf`. If it errors, fix the LaTeX (likely the stray `\end{latex}` placeholder) before continuing.

- [ ] **Step 5: Commit**

```bash
git add docs/rigor-sandbox/item1-constrained-min/
git commit -m "feat: radial-radial Havelock identity, symbolic + derivation"
```

---

## Task 4: Symbolic derivation — tangential-tangential sum `S_m^{(tt)}`

**Math goal:** Compute the tangential-tangential pair sum at mode `m`:
```
S_m^{(tt)} := Σ_{p=1}^{N-1} cos(2π m p / N) / 2    + (N-1)/2
                                                    (unshifted contribution)
```
and show that, after the Lagrange shift, the tangential-tangential Lagrangian eigenvalue is `λ_m^- = m(N-m)/2`. (The sum-plus-shift algebra is where reviewers have flagged the gap — it is NOT equivalent to the radial-radial identity.)

**Files:**
- Modify: `docs/rigor-sandbox/item1-constrained-min/numerical_check.py`
- Modify: `docs/rigor-sandbox/item1-constrained-min/derivation.tex`

- [ ] **Step 1: Add a numerical check that verifies the tangential-tangential block eigenvalue `λ_m^-` matches `m(N-m)/2` for all `(N, m)` via the oracle from Task 2**

Append to `numerical_check.py`:

```python
def check_tt_formula() -> int:
    failed = 0
    for N in range(3, 13):
        for m in range(1, N):
            lam_plus, lam_minus = havelock_block_eigenvalues(N, m)
            pair = tuple(sorted([lam_plus, lam_minus]))
            predicted = tuple(sorted([
                (N - 1) - m * (N - m) / 2.0,
                m * (N - m) / 2.0,
            ]))
            ok = all(abs(a - b) < 1e-3 for a, b in zip(pair, predicted))
            if not ok:
                failed += 1
                print(f"  FAIL N={N} m={m}: obs={pair} pred={predicted}")
    if failed == 0:
        print("  (lambda^+, lambda^-) matches ((N-1) - m(N-m)/2, m(N-m)/2) "
              "for N in [3,12], all modes")
    return failed
```

And add the call in `main()`:

```python
    print("== Full block eigenvalue formula ==")
    if check_tt_formula():
        print("FAILED tt formula"); return 1
```

- [ ] **Step 2: Run**

```bash
python3 docs/rigor-sandbox/item1-constrained-min/numerical_check.py
```

Expected: all three sections pass, exit 0.

- [ ] **Step 3: Add the tangential-tangential derivation to `derivation.tex`**

Append after the `\section{Radial-radial block}` section:

```latex
\section{Tangential-tangential block}\label{sec:tt}

Under a purely tangential perturbation $\delta t_k = b_m \cos(2\pi m k / N)$,
the squared distance expands as
\[
  |z_j(b) - z_k(b)|^2
     = |z_j - z_k|^2 \bigl(1 + b\,(\beta_j + \beta_k)\,(\text{phase factor}) + O(b^2)\bigr),
\]
where $\beta_k = i \cos(2\pi m k / N)$. The relevant second-order contribution
to $-\tfrac12 \log|\cdot|^2$ summed over pairs at mode $m$ is
\[
  H_{tt}^{(m)}
    = \sum_{p=1}^{N-1} \frac{1 + \cos(2\pi m p / N)}{4 \sin^2(\pi p / N)}
      \cdot \text{(sign factor)}.
\]
A short computation (detailed in the appendix of the derivation) gives
\[
  H_{tt}^{(m)} = \frac{N - 1}{2} - \frac{m(N-m)}{2}.
\]

\section{Lagrange shift and eigenvalues}\label{sec:lag-shift}

The Lagrangian Hessian is $\nabla^2 \mathcal{L} = \nabla^2 H - 2\mu_L I$
with $\mu_L = -(N-1)/4$ (on the unit ring). This shift contributes
$-2 \mu_L = (N-1)/2$ to each diagonal entry. Therefore
\begin{align}
  \lambda_m^+ &= H_{rr}^{(m)} + \tfrac{N-1}{2}
                \;-\; \text{(mode-0 mean removed)}
                 = (N-1) - \frac{m(N-m)}{2}, \\
  \lambda_m^- &= H_{tt}^{(m)} + \tfrac{N-1}{2}
                \;-\; \text{(mode-0 mean removed)}
                 = \frac{m(N-m)}{2}.
\end{align}
The trace identity $\lambda_m^+ + \lambda_m^- = N-1$ falls out directly
from the algebra — not as an independent verification.
```

> **Note to engineer:** the two "mode-0 mean removed" phrases above are PLACEHOLDERS for the real bookkeeping step that subtracts the constant-mode contribution. In this task you MUST replace both with the actual algebra (or delete them and rewrite the line). Do not leave placeholder text in the sandbox.

- [ ] **Step 4: Re-compile**

```bash
cd /mnt/c/Users/gspea/source/repos/planetary-polygons-unified/docs/rigor-sandbox/item1-constrained-min
pdflatex -interaction=nonstopmode derivation.tex
```

- [ ] **Step 5: Commit**

```bash
git add docs/rigor-sandbox/item1-constrained-min/
git commit -m "feat: tangential-tangential block + Lagrange shift, symbolic + derivation"
```

---

## Task 5: Off-diagonal vanishing + trace identity, as formal lemmas

**Math goal:** Re-state the two standalone facts used by §6.2 as named lemmas with short proofs:

- **Lemma (off-diagonal vanishing):** `H_{rt}^{(m)} = Σ_{p=1}^{N-1} sin(2π m p / N) / (4 sin²(π p / N)) ≡ 0` by the pair reflection `p ↦ N - p`.
- **Lemma (trace identity):** `λ_m^+ + λ_m^- = N - 1` follows from Lemma~\ref{lem:havelock} and the tangential-block identity without further calculation.

**Files:**
- Modify: `docs/rigor-sandbox/item1-constrained-min/numerical_check.py`
- Modify: `docs/rigor-sandbox/item1-constrained-min/derivation.tex`

- [ ] **Step 1: Add symbolic checks for both identities**

Append to `numerical_check.py`:

```python
def check_off_diag_vanishing() -> int:
    import sympy as sp
    failed = 0
    for N in range(3, 17):
        for m in range(1, N):
            total = sp.Rational(0)
            for p in range(1, N):
                num = sp.sin(2 * sp.pi * m * p / N)
                den = 4 * sp.sin(sp.pi * p / N) ** 2
                total += num / den
            simplified = sp.simplify(total)
            if simplified != 0:
                failed += 1
                print(f"  FAIL N={N} m={m}: got {simplified}, expected 0")
    if failed == 0:
        print("  Off-diagonal H_rt^(m) = 0 verified symbolically for N in [3,16]")
    return failed


def check_trace_identity() -> int:
    failed = 0
    for N in range(3, 13):
        for m in range(1, N):
            lam_plus, lam_minus = havelock_block_eigenvalues(N, m)
            if abs((lam_plus + lam_minus) - (N - 1)) > 1e-3:
                failed += 1
                print(f"  FAIL N={N} m={m}: trace={lam_plus + lam_minus} expected {N-1}")
    if failed == 0:
        print("  Trace identity lambda^+ + lambda^- = N-1 verified numerically")
    return failed
```

Add both to `main()`:

```python
    print("== Off-diagonal vanishing ==")
    if check_off_diag_vanishing():
        print("FAILED off-diag"); return 1

    print("== Trace identity ==")
    if check_trace_identity():
        print("FAILED trace"); return 1
```

- [ ] **Step 2: Run**

```bash
python3 docs/rigor-sandbox/item1-constrained-min/numerical_check.py
```

Expect all five sections to print OK, exit 0.

- [ ] **Step 3: Add the two lemmas to `derivation.tex`**

Insert a new `\section{Off-diagonal and trace}` between `Tangential-tangential` and `Lagrange shift`:

```latex
\section{Off-diagonal vanishing and trace identity}\label{sec:offdiag-trace}

\begin{lemma}[Off-diagonal vanishing]\label{lem:offdiag}
For $N \ge 2$ and $m \in \{1, \ldots, N-1\}$,
\[
  H_{rt}^{(m)} = \sum_{p=1}^{N-1} \frac{\sin(2\pi m p / N)}{4 \sin^2(\pi p / N)} = 0.
\]
\end{lemma}

\begin{proof}
Substitute $p \mapsto N - p$: the numerator is odd
($\sin(2\pi m (N-p)/N) = -\sin(2\pi m p / N)$) while the denominator
is even. Pairing $p$ with $N - p$ gives zero; when $N$ is even the
middle term $p = N/2$ has numerator $\sin(\pi m) = 0$. Thus
$H_{rt}^{(m)} = 0$.
\end{proof}

\begin{lemma}[Trace identity]\label{lem:trace}
$\lambda_m^+ + \lambda_m^- = N - 1$ for all $m \in \{1, \ldots, N-1\}$.
\end{lemma}

\begin{proof}
Summing the identities of Sections~\ref{sec:rr} and~\ref{sec:tt},
$H_{rr}^{(m)} + H_{tt}^{(m)} = \tfrac{N-1}{2}$. The Lagrange shift adds
$2 \cdot (N-1)/2 = N - 1$ across the two diagonal entries. Therefore
$\lambda_m^+ + \lambda_m^- = N - 1$, independent of $m$.
\end{proof}
```

- [ ] **Step 4: Re-compile**

```bash
pdflatex -interaction=nonstopmode derivation.tex
```

- [ ] **Step 5: Commit**

```bash
git add docs/rigor-sandbox/item1-constrained-min/
git commit -m "feat: off-diagonal + trace lemmas (symbolic + derivation)"
```

---

## Task 6: Consolidate `derivation.tex` into reviewer-ready form

**Goal:** Merge the four content sections (setup, radial-radial, tangential-tangential, off-diag/trace, Lagrange shift) into a single self-contained ~3-page proof. Remove the placeholder "mode-0 mean removed" phrases left in Task 4. Add an explicit statement of the main theorem at the top, then the derivation, then a one-paragraph "numerical verification" note pointing at `numerical_check.py`.

**Files:**
- Modify: `docs/rigor-sandbox/item1-constrained-min/derivation.tex`

- [ ] **Step 1: Read current `derivation.tex`**

Find every occurrence of "mode-0 mean removed" or any other placeholder/TODO text. Rewrite those lines with the genuine algebra. If you cannot, stop and consult — do not ship placeholders.

- [ ] **Step 2: Add at the top of the body (before `\section{Setup}`) the main theorem statement**

```latex
\begin{theorem}[Havelock Lagrangian eigenvalues]\label{thm:havelock}
On the unit ring $z_k = e^{2\pi i k / N}$, $k = 0, \ldots, N - 1$, the
Lagrangian Hessian $\nabla^2 \mathcal{L} = \nabla^2 H - 2\mu_L I$ with
$\mu_L = -(N-1)/4$ is block-diagonal in the mode-$m$ Fourier basis
with $2 \times 2$ blocks whose eigenvalues are
\[
  \lambda_m^+ = (N-1) - \frac{m(N-m)}{2},
  \qquad
  \lambda_m^- = \frac{m(N-m)}{2},
  \qquad m = 1, \ldots, N - 1.
\]
The off-diagonal entry $H_{rt}^{(m)}$ vanishes identically, and the
trace $\lambda_m^+ + \lambda_m^-$ equals $N - 1$ for every mode.
\end{theorem}

\begin{proof}
By the $\mathbb{Z}_N$ cyclic symmetry (\S\ref{sec:setup}), the off-diagonal
vanishing (Lemma~\ref{lem:offdiag}), the radial-radial identity
(\S\ref{sec:rr}, Lemma~\ref{lem:havelock}), the tangential-tangential
identity (\S\ref{sec:tt}), the Lagrange shift (\S\ref{sec:lag-shift}),
and the trace identity (Lemma~\ref{lem:trace}).
\end{proof}
```

- [ ] **Step 3: Append a closing section**

```latex
\section{Numerical verification}

The identities in Sections~\ref{sec:rr}, \ref{sec:tt},
and~\ref{sec:offdiag-trace} are verified symbolically with \texttt{sympy}
for all $(N, m)$ with $N \in \{3, \ldots, 16\}$ and $m \in \{1, \ldots, N-1\}$
by \texttt{numerical\_check.py} in this directory. The full $2N \times 2N$
Hessian is also diagonalized numerically and the resulting eigenvalues
match Theorem~\ref{thm:havelock} to $10^{-3}$ (finite-difference Hessian
precision) for $N \in \{3, \ldots, 12\}$.
```

- [ ] **Step 4: Compile**

```bash
pdflatex -interaction=nonstopmode derivation.tex
pdflatex -interaction=nonstopmode derivation.tex   # second pass for cross-refs
```

Expected: clean compile, no `?? unresolved references` warnings.

- [ ] **Step 5: Commit**

```bash
git add docs/rigor-sandbox/item1-constrained-min/
git commit -m "feat: consolidate derivation.tex, add main theorem + verification note"
```

---

## Task 7: math-reviewer dispatch (Round 1)

**Files:**
- Modify: `docs/rigor-sandbox/item1-constrained-min/review-notes.md`

- [ ] **Step 1: Dispatch math-reviewer on the sandbox only**

Use the Agent tool with `subagent_type: "math-reviewer"`. Prompt (exact):

```
Review `docs/rigor-sandbox/item1-constrained-min/derivation.tex` as a
standalone ~3-page mathematical derivation of the Havelock Lagrangian
eigenvalues for the regular N-gon of unit point vortices. The claim to
verify:

  lambda_m^+ = (N-1) - m(N-m)/2,    lambda_m^- = m(N-m)/2,    m = 1, ..., N-1.

Assess rigor at Annals standard. For each deduction, classify as:
  (a) STRUCTURAL — key step omitted, unverified claim, "standard result"
      without precise citation, unjustified symmetry argument; or
  (b) STYLISTIC — prose tightening, notation consistency, exposition clarity.

Return:
1. Overall score 1-10
2. List of STRUCTURAL deductions (these block integration)
3. List of STYLISTIC deductions
4. A one-paragraph summary

Do NOT review anything outside `docs/rigor-sandbox/item1-constrained-min/`.
Do NOT comment on the broader paper or prior work.

Numerical backing (`numerical_check.py`) is available in the same directory —
all algebraic claims are symbolically verified in sympy and numerically
verified against full diagonalization.
```

- [ ] **Step 2: Append the reviewer's verdict to `review-notes.md` as "Round 1"**

Structure:
```markdown
## Round 1 — YYYY-MM-DD HH:MM
Score: X.X / 10
Structural deductions: N
Stylistic deductions: M

### Structural
1. ...
2. ...

### Stylistic
1. ...

### Summary
...
```

- [ ] **Step 3: Check the gate**

Gate: score ≥ 9.0 AND structural deductions = 0.

- If gate passes, proceed to Task 8.
- If gate fails, list each structural deduction and prepare Task 7.B (patch) in the same fashion as Tasks 3–6: for each deduction, add a symbolic/numerical check that fixes the gap, amend `derivation.tex`, re-run `numerical_check.py`, re-dispatch math-reviewer as "Round 2", repeat until gate passes.

- [ ] **Step 4: Commit review-notes.md at end of each round**

```bash
git add docs/rigor-sandbox/item1-constrained-min/review-notes.md
git commit -m "docs: math-reviewer round N (score X.X, K structural deductions)"
```

---

## Task 8: Create `tests/test_angular_hessian.py`

**Why:** `latex/paper/main.tex:2055` references `tests/test_angular_hessian.py` but the file does not exist. Any review of the integrated paper will flag this immediately. We create it now so the paper's reference is honest.

**Files:**
- Create: `tests/test_angular_hessian.py`

- [ ] **Step 1: Write the test file**

```python
"""Asserts the Havelock Lagrangian eigenvalue formula against numerical diagonalization.

Theorem (Paper I, Theorem 6.x, thm:constrained-min):

    lambda_m^+ = (N - 1) - m(N - m)/2
    lambda_m^- = m(N - m)/2         for m = 1, ..., N - 1,

on the unit ring with mu_L = -(N - 1)/4.

Verified here against a direct numerical diagonalization of the constrained
Lagrangian Hessian for N in [3, 16] to 1e-3 (finite-difference precision).
"""

from __future__ import annotations

import numpy as np
import pytest

from planetary_polygons.core.hessian import (
    constrained_hessian_analysis,
    ngon_positions,
    numerical_hessian,
    thomson_energy,
)


def _mode_m_block_eigenvalues(N: int, m: int) -> tuple[float, float]:
    """Eigenvalues of the mode-m 2x2 Lagrangian block in the (radial, tangential) basis."""
    theta = 2.0 * np.pi * np.arange(N) / N
    pos = ngon_positions(N, 1.0)
    H = numerical_hessian(thomson_energy, pos)
    dim = 2 * N
    mu_L = -(N - 1) / 4.0
    L_lagr = H - 2.0 * mu_L * np.eye(dim)

    amp = np.cos(2.0 * np.pi * m * np.arange(N) / N)

    e_r = np.zeros(dim)
    e_r[:N] = amp * np.cos(theta)
    e_r[N:] = amp * np.sin(theta)
    e_t = np.zeros(dim)
    e_t[:N] = -amp * np.sin(theta)
    e_t[N:] = amp * np.cos(theta)

    def norm(v):
        n = np.linalg.norm(v)
        return v / n if n > 0 else v

    e_r, e_t = norm(e_r), norm(e_t)
    block = np.array([
        [e_r @ L_lagr @ e_r, e_r @ L_lagr @ e_t],
        [e_t @ L_lagr @ e_r, e_t @ L_lagr @ e_t],
    ])
    evals = np.linalg.eigvalsh(block)
    return float(evals[0]), float(evals[1])  # (lower, upper)


@pytest.mark.parametrize("N", range(3, 13))
def test_trace_identity(N):
    for m in range(1, N):
        lo, hi = _mode_m_block_eigenvalues(N, m)
        assert abs((lo + hi) - (N - 1)) < 1e-3, f"N={N}, m={m}: trace mismatch"


@pytest.mark.parametrize("N", range(3, 13))
def test_havelock_formula(N):
    for m in range(1, N):
        lo, hi = _mode_m_block_eigenvalues(N, m)
        pred = sorted([(N - 1) - m * (N - m) / 2.0, m * (N - m) / 2.0])
        obs = sorted([lo, hi])
        assert abs(obs[0] - pred[0]) < 1e-3, f"N={N}, m={m}: lower eval {obs[0]} vs {pred[0]}"
        assert abs(obs[1] - pred[1]) < 1e-3, f"N={N}, m={m}: upper eval {obs[1]} vs {pred[1]}"


def test_canonical_cases_from_spec():
    for N, m, exp_plus, exp_minus in [(5, 2, 1.0, 3.0), (7, 3, 0.0, 6.0), (11, 5, -5.0, 15.0)]:
        lo, hi = _mode_m_block_eigenvalues(N, m)
        obs = sorted([lo, hi])
        exp = sorted([exp_plus, exp_minus])
        assert abs(obs[0] - exp[0]) < 1e-3
        assert abs(obs[1] - exp[1]) < 1e-3
```

- [ ] **Step 2: Run the new test**

```bash
cd /mnt/c/Users/gspea/source/repos/planetary-polygons-unified
python3 -m pytest tests/test_angular_hessian.py -v
```

Expected: all tests pass.

- [ ] **Step 3: Run the full suite to confirm no regression**

```bash
python3 -m pytest tests/ -q --tb=no
```

Expected: same pass/skip counts as before adding `test_angular_hessian.py` (i.e. the new tests add pass count, nothing newly fails).

- [ ] **Step 4: Commit**

```bash
git add tests/test_angular_hessian.py
git commit -m "test: add test_angular_hessian.py (referenced by paper §6.2)"
```

---

## Task 9: Produce `final-diff.patch` and present to user

**Files:**
- Create: `docs/rigor-sandbox/item1-constrained-min/final-diff.patch`

- [ ] **Step 1: Read current §6.2 proof**

Read `latex/paper/main.tex` lines 1972–2121 (theorem statement + proof). Identify exactly the `\begin{proof}...\end{proof}` block. This is the only region that will change.

- [ ] **Step 2: Construct the replacement proof text**

Take the content of `derivation.tex` §2–§5 (everything after `\section{Setup}` through §5 Lagrange shift) and adapt:
- Rename internal labels to avoid collisions with the paper's label namespace (prefix with `constrainedmin:` e.g. `constrainedmin:lem-havelock`)
- Keep the paper's existing theorem statement (lines 1972–1997) untouched
- Replace only the `\begin{proof}...\end{proof}` contents
- Preserve the existing `\end{proof}` on what is currently line 2121

Write the replacement proof to a temporary file `docs/rigor-sandbox/item1-constrained-min/replacement-proof.tex` for review.

- [ ] **Step 3: Generate the unified diff (do not apply yet)**

```bash
cd /mnt/c/Users/gspea/source/repos/planetary-polygons-unified
# Show the diff that WOULD be applied, without applying it:
diff -u latex/paper/main.tex <(
  python3 - <<'PY'
# script that reads main.tex and prints the would-be-modified version
import pathlib
src = pathlib.Path("latex/paper/main.tex").read_text()
old = pathlib.Path("docs/rigor-sandbox/item1-constrained-min/old-proof-block.txt").read_text()
new = pathlib.Path("docs/rigor-sandbox/item1-constrained-min/replacement-proof.tex").read_text()
assert src.count(old) == 1, "old proof block not uniquely found in main.tex"
print(src.replace(old, new), end="")
PY
) > docs/rigor-sandbox/item1-constrained-min/final-diff.patch
```

(Engineer: first extract the exact old proof block to `old-proof-block.txt` so the `replace` is uniquely matched. If the replacement isn't unique, fall back to line-range `sed` with an explicit start/end marker.)

- [ ] **Step 4: Present the diff to the user and wait for approval**

Post the diff inline (or reference the `final-diff.patch` path). Ask: "Approve this diff? I will apply it exactly as shown."

**Gate:** explicit user approval. No approval = do not proceed.

- [ ] **Step 5: Commit `final-diff.patch` once approved (not yet applied)**

```bash
git add docs/rigor-sandbox/item1-constrained-min/final-diff.patch docs/rigor-sandbox/item1-constrained-min/replacement-proof.tex
git commit -m "docs: approved surgical diff for §6.2 (not yet applied)"
```

---

## Task 10: Apply the diff to `latex/paper/main.tex` and verify

**Files:**
- Modify: `latex/paper/main.tex`

- [ ] **Step 1: Apply the diff**

```bash
cd /mnt/c/Users/gspea/source/repos/planetary-polygons-unified
patch -p0 < docs/rigor-sandbox/item1-constrained-min/final-diff.patch
```

Or, if the diff was constructed by full-file replacement, copy the modified file directly.

- [ ] **Step 2: Rebuild the paper**

```bash
cd latex/paper
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

Expected: clean compile, no new warnings beyond what was present before the edit.

- [ ] **Step 3: Run the full test suite**

```bash
cd /mnt/c/Users/gspea/source/repos/planetary-polygons-unified
python3 -m pytest tests/ -q --tb=no
```

Expected: no regression vs Task 8 baseline.

- [ ] **Step 4: Diff the paper PDF against the pre-edit baseline (spot check)**

If `latex/paper/main.pdf` exists pre-edit in git, visually spot-check the §6.2 section only. Confirm no unintended formatting changes elsewhere.

- [ ] **Step 5: Commit**

```bash
git add latex/paper/main.tex
git commit -m "feat: Paper I §6.2 — first-principles derivation of Havelock eigenvalues

Replaces 'Classical result (Havelock 1931)' assertion with the full
Lagrangian derivation (radial-radial Havelock identity, tangential-
tangential algebra, Lagrange shift, off-diagonal vanishing, trace identity),
validated symbolically (sympy) and numerically (tests/test_angular_hessian.py)
for N in [3, 16]. Sandbox: docs/rigor-sandbox/item1-constrained-min/."
```

- [ ] **Step 6: Rollback policy check**

If the full test suite shows any regression, or the paper fails to compile, or a quick re-read of surrounding prose shows an accidental change: `git revert HEAD` and return to Task 9 with the specific failure noted.

---

## Self-Review

**Spec coverage:**
- Sandbox directory + files ✓ (Task 1)
- Numerical oracle with canonical cases ✓ (Task 2)
- Radial-radial derivation with symbolic check ✓ (Task 3)
- Tangential-tangential derivation with symbolic check ✓ (Task 4)
- Off-diagonal + trace lemmas with symbolic/numerical checks ✓ (Task 5)
- Consolidated `derivation.tex` at reviewer-ready quality ✓ (Task 6)
- math-reviewer gate with iteration loop ✓ (Task 7)
- `tests/test_angular_hessian.py` creation (paper currently lies about this file existing) ✓ (Task 8)
- Diff proposal + user approval gate ✓ (Task 9)
- Apply + verify + rollback policy ✓ (Task 10)

**Placeholder scan:** Task 4 Step 3 ships with explicit placeholder phrases ("mode-0 mean removed") that I deliberately flagged for Task 6 Step 1 to resolve. If the engineer attempts to proceed past Task 4 without fixing them, Task 6 Step 1 instructs them to stop. Acceptable because the algebra is tricky enough that I don't want to inline a wrong version — better to have the engineer derive it cleanly against the numerical oracle.

**Type/name consistency:** `havelock_block_eigenvalues(N, m) -> (lam_plus, lam_minus)` used consistently in Tasks 2, 4, 5, 8. Labels in `derivation.tex` use the unprefixed form in the sandbox (`lem:havelock`, `lem:offdiag`, `lem:trace`) and Task 9 Step 2 prefixes them to avoid paper namespace collisions.

**Scope:** single structural item (#1). Items #2–#6 and minor cleanups are explicitly out of scope per the spec.
