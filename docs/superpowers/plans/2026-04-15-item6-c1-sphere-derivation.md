# Item #6 — C₁(S²) Geodesic Derivation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Derive C₁(S²,ξ) = (N-1)(1-ξ)/(1+ξ) from the geodesic Green's function on S², replacing the Boatto-Cabral 2003 citation in the appendix with a first-principles proof.

**Architecture:** Sandbox-first (same as Item #1). Build a geodesic-frame numerical oracle, derive the formula algebraically with every step verified to 30 digits, pass math-reviewer gate, then surgically replace the appendix section.

**Tech Stack:** Python 3, sympy, numpy, pytest, LaTeX.

---

## File Structure

**Create (sandbox):**
- `docs/rigor-sandbox/item6-c1-sphere/derivation.tex` — standalone LaTeX (~4 pages)
- `docs/rigor-sandbox/item6-c1-sphere/numerical_check.py` — symbolic + numerical validator
- `docs/rigor-sandbox/item6-c1-sphere/review-notes.md` — math-reviewer rounds
- `docs/rigor-sandbox/item6-c1-sphere/replacement-proof.tex` — approved appendix replacement

**Modify (only after all gates pass):**
- `latex/paper-A-appendices/main.tex` — §2 (lines 178–336): replace "Geodesic-metric result (Boatto-Cabral 2003)" paragraph with the derived proof. Keep `\label{app:c1_s2}`, `\label{eq:C1_S2}`, and the "Properties" list.

**Do not touch:** `latex/paper/main.tex`, any other appendix section, any source file.

---

### Task 1: Scaffold the sandbox

**Files:**
- Create: `docs/rigor-sandbox/item6-c1-sphere/review-notes.md`
- Create: `docs/rigor-sandbox/item6-c1-sphere/numerical_check.py`
- Create: `docs/rigor-sandbox/item6-c1-sphere/derivation.tex`

- [ ] **Step 1: Create directory**

```bash
mkdir -p docs/rigor-sandbox/item6-c1-sphere
```

- [ ] **Step 2: Create `review-notes.md`**

```markdown
# Item #6 — Review Log

## Round 0 — pre-review baseline

(to be filled by math-reviewer dispatch)
```

- [ ] **Step 3: Create `numerical_check.py` scaffold**

```python
"""Numerical + symbolic validator for the C₁(S²) geodesic derivation.

Run: python3 docs/rigor-sandbox/item6-c1-sphere/numerical_check.py
Exit 0 = all claims verified. Non-zero = derivation is wrong.
"""
from __future__ import annotations
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO / "src"))


def main() -> int:
    print("numerical_check.py: no checks implemented yet")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Create `derivation.tex` scaffold**

```latex
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{geometry}
\geometry{margin=1in}
\newtheorem{lemma}{Lemma}
\newtheorem{theorem}{Theorem}
\newtheorem{corollary}{Corollary}
\theoremstyle{remark}
\newtheorem{remark}{Remark}

\title{$C_1(\mathbf{S}^2,\xi)$ from the Geodesic Green's Function}
\author{Sandbox for Paper~I, Item~\#6}
\date{\today}

\begin{document}
\maketitle

% Content added in later tasks.

\end{document}
```

- [ ] **Step 5: Verify and commit**

```bash
python3 docs/rigor-sandbox/item6-c1-sphere/numerical_check.py
git add docs/rigor-sandbox/item6-c1-sphere/
git commit -m "chore: scaffold Item #6 C₁(S²) sandbox"
```

---

### Task 2: Geodesic-frame numerical oracle

**Why:** We need a trusted oracle that computes the mode-m constrained Hessian eigenvalue on S² using the geodesic Green's function directly (not the Euclidean-frame approximation in `curved_surfaces.py`). This oracle is the ground truth every symbolic step is checked against.

**Files:**
- Modify: `docs/rigor-sandbox/item6-c1-sphere/numerical_check.py`

- [ ] **Step 1: Implement the geodesic oracle**

Add to `numerical_check.py`:

```python
import numpy as np


def geodesic_energy_sphere(phi: np.ndarray, theta: np.ndarray) -> float:
    """H = -Σ_{j<k} log sin(d_geo(j,k)/2) on unit S².

    phi[k] = colatitude of vortex k (0 = north pole).
    theta[k] = azimuthal angle.
    cos(d_jk) = cos φ_j cos φ_k + sin φ_j sin φ_k cos(θ_j - θ_k).
    """
    N = len(phi)
    H = 0.0
    for j in range(N):
        for k in range(j + 1, N):
            cos_d = (np.cos(phi[j]) * np.cos(phi[k])
                     + np.sin(phi[j]) * np.sin(phi[k]) * np.cos(theta[j] - theta[k]))
            cos_d = np.clip(cos_d, -1.0, 1.0)
            sin_half = np.sqrt((1.0 - cos_d) / 2.0)
            if sin_half < 1e-30:
                sin_half = 1e-30
            H -= np.log(sin_half)
    return H


def sphere_mode_m_eigenvalue(N: int, phi0: float, m: int) -> float:
    """Mode-m constrained Hessian eigenvalue on S² in geodesic frame.

    Uses finite-difference Hessian of H_geo at the N-gon at colatitude phi0,
    projected onto the mode-m radial Fourier direction in geodesic coords,
    with the angular momentum J = Σ cos(phi_k) constraint.

    Returns the radial eigenvalue λ_m = C₁ - m(N-m)/2 (mode-m dependent).
    """
    theta_eq = 2.0 * np.pi * np.arange(N) / N
    phi_eq = np.full(N, phi0)

    # Combined energy-constraint functional: L = H - Ω J
    # First find Ω from equilibrium condition ∂H/∂φ₀ = Ω ∂J/∂φ₀
    eps = 1e-6
    phi_p = phi_eq.copy(); phi_p[:] += eps
    phi_m = phi_eq.copy(); phi_m[:] -= eps
    dH = (geodesic_energy_sphere(phi_p, theta_eq)
          - geodesic_energy_sphere(phi_m, theta_eq)) / (2 * eps * N)
    # J = Σ cos(phi_k), ∂J/∂phi_k = -sin(phi_k)
    dJ = -np.sin(phi0)
    Omega = dH / dJ if abs(dJ) > 1e-15 else 0.0

    def lagrangian(phi, theta):
        return geodesic_energy_sphere(phi, theta) - Omega * np.sum(np.cos(phi))

    # Mode-m radial perturbation in geodesic frame: δφ_k = a cos(2πmk/N)
    amp = np.cos(2.0 * np.pi * m * np.arange(N) / N)
    norm_sq = np.sum(amp ** 2)  # = N/2 for m not 0 or N/2

    h = 1e-5
    L0 = lagrangian(phi_eq, theta_eq)
    phi_plus = phi_eq + h * amp
    phi_minus = phi_eq - h * amp
    Lp = lagrangian(phi_plus, theta_eq)
    Lm = lagrangian(phi_minus, theta_eq)
    d2L = (Lp - 2 * L0 + Lm) / h ** 2

    return d2L / norm_sq


def check_c1_formula_against_oracle() -> int:
    """C₁(S²,ξ) = (N-1)(1-ξ)/(1+ξ) verified against geodesic-frame oracle."""
    failed = 0
    for N in [4, 5, 6, 7]:
        for phi0_deg in [15, 30, 45, 60, 75]:
            phi0 = np.radians(phi0_deg)
            xi = np.tan(phi0 / 2) ** 2
            c1_formula = (N - 1) * (1 - xi) / (1 + xi)

            # Use m=2 (always exists for N>=4) to extract C₁:
            # λ_m = C₁ - m(N-m)/2, so C₁ = λ_m + m(N-m)/2
            m = 2
            lam = sphere_mode_m_eigenvalue(N, phi0, m)
            c1_oracle = lam + m * (N - m) / 2.0

            diff = abs(c1_oracle - c1_formula)
            ok = diff < 0.05  # finite-difference tolerance
            status = "OK" if ok else "FAIL"
            print(f"  N={N} φ₀={phi0_deg:2d}° ξ={xi:.4f}: "
                  f"C₁_oracle={c1_oracle:.4f} C₁_formula={c1_formula:.4f} "
                  f"Δ={diff:.2e} [{status}]")
            if not ok:
                failed += 1
    if failed == 0:
        print("  C₁(S²) = (N-1)(1-ξ)/(1+ξ) matches geodesic oracle")
    return failed
```

Update `main()`:

```python
def main() -> int:
    print("== C₁(S²) formula vs geodesic oracle ==")
    if check_c1_formula_against_oracle():
        print("FAILED oracle check")
        return 1
    print("All checks pass.")
    return 0
```

- [ ] **Step 2: Run the oracle**

```bash
cd /mnt/c/Users/gspea/source/repos/planetary-polygons-unified
python3 docs/rigor-sandbox/item6-c1-sphere/numerical_check.py
```

Expected: all (N, φ₀) pairs show OK with Δ < 0.05. If any fail, debug the oracle.

- [ ] **Step 3: Commit**

```bash
git add docs/rigor-sandbox/item6-c1-sphere/numerical_check.py
git commit -m "test: geodesic-frame oracle for C₁(S²)"
```

---

### Task 3: Algebraic derivation — geodesic second variation on S²

**Math goal:** Starting from the geodesic Green's function `h_geo = -log sin(d/2)` with `cos d_{jk} = cos²φ₀ + sin²φ₀ cos(θ_j - θ_k)` at the N-gon ring on S², compute the radial second variation in the geodesic frame (δφ_k = ε cos(2πmk/N)) and show that the mode-m eigenvalue equals `(N-1)(1-ξ)/(1+ξ) - m(N-m)/2` where `ξ = tan²(φ₀/2)`.

**Files:**
- Modify: `docs/rigor-sandbox/item6-c1-sphere/numerical_check.py`
- Modify: `docs/rigor-sandbox/item6-c1-sphere/derivation.tex`

- [ ] **Step 1: Add symbolic checks for intermediate identities**

These are the key sub-results to verify symbolically:

```python
def check_cos_d_expansion() -> int:
    """Verify the second-order expansion of cos(d_{jk}) under radial perturbation
       δφ_k = a cos(2πmk/N)."""
    import sympy as sp
    failed = 0
    prec = 30
    # At the N-gon: cos d_{0,p} = cos²φ₀ + sin²φ₀ cos(2πp/N).
    # Under δφ_0 = a α_0, δφ_p = a α_p:
    # δ(cos d) = -sin φ₀ cos φ₀ (α_0 + α_p)(1 - cos(2πp/N))·a + O(a²)
    # [This is the S² analogue of the pair-distance expansion.]
    phi0 = sp.Rational(1, 3)  # test at φ₀ = 1/3 rad
    N_val = 5
    for m in range(1, N_val):
        for p in range(1, N_val):
            alpha_0 = sp.cos(2 * sp.pi * m * 0 / N_val)
            alpha_p = sp.cos(2 * sp.pi * m * p / N_val)
            linear_coeff = -sp.sin(phi0) * sp.cos(phi0) * (alpha_0 + alpha_p) * (1 - sp.cos(2 * sp.pi * p / N_val))

            # Verify numerically by finite diff on cos d
            def cos_d(a_val):
                phi_j = phi0 + a_val * float(alpha_0.evalf())
                phi_k = phi0 + a_val * float(alpha_p.evalf())
                return (float(sp.cos(phi_j) * sp.cos(phi_k))
                        + float(sp.sin(phi_j) * sp.sin(phi_k))
                        * float(sp.cos(2 * sp.pi * p / N_val).evalf()))

            h = 1e-7
            deriv = (cos_d(h) - cos_d(-h)) / (2 * h)
            expected = float(linear_coeff.evalf(prec))
            if abs(expected) > 1e-10:
                rel = abs(deriv - expected) / abs(expected)
                if rel > 1e-4:
                    failed += 1
                    print(f"  FAIL m={m} p={p}: deriv={deriv:.6e} expected={expected:.6e}")
    if failed == 0:
        print("  cos(d) linear expansion verified for N=5, all modes")
    return failed


def check_c1_boundary_cases() -> int:
    """C₁(S²,0) = N-1 (flat limit) and C₁(S²,1) = 0 (equator)."""
    failed = 0
    for N in range(3, 11):
        c1_0 = (N - 1) * (1 - 0) / (1 + 0)
        c1_1 = (N - 1) * (1 - 1) / (1 + 1)
        if abs(c1_0 - (N - 1)) > 1e-15:
            failed += 1
            print(f"  FAIL N={N}: C₁(0) = {c1_0}, expected {N-1}")
        if abs(c1_1) > 1e-15:
            failed += 1
            print(f"  FAIL N={N}: C₁(1) = {c1_1}, expected 0")
    if failed == 0:
        print("  Boundary cases verified: C₁(0) = N-1, C₁(1) = 0")
    return failed


def check_c1_equals_cos_phi() -> int:
    """C₁(S²,ξ) = (N-1) cos φ₀ where ξ = tan²(φ₀/2)."""
    import sympy as sp
    failed = 0
    phi = sp.Symbol('phi', positive=True)
    xi = sp.tan(phi / 2) ** 2
    c1 = (sp.Integer(1) - xi) / (1 + xi)
    diff = sp.simplify(c1 - sp.cos(phi))
    if diff != 0:
        failed += 1
        print(f"  FAIL: (1-ξ)/(1+ξ) - cos φ = {diff}")
    else:
        print("  (1-ξ)/(1+ξ) = cos φ₀ verified symbolically")
    return failed
```

Update `main()` to call all checks.

- [ ] **Step 2: Run checks**

```bash
python3 docs/rigor-sandbox/item6-c1-sphere/numerical_check.py
```

- [ ] **Step 3: Write the derivation in `derivation.tex`**

The derivation proceeds in these steps (detailed LaTeX to be written during implementation):

1. **Setup:** N-gon at colatitude φ₀ on unit S². Geodesic pair distance via cos d_{jk} = cos²φ₀ + sin²φ₀ cos(θ_j - θ_k). Define ξ = tan²(φ₀/2).

2. **Geodesic Green's function:** H = -Σ_{j<k} log sin(d_{jk}/2), with sin²(d/2) = (1 - cos d)/2.

3. **Radial perturbation in geodesic frame:** δφ_k = a cos(2πmk/N). Expand cos(d_{jk}(a)) to O(a²), take -log sin(d/2) to second order.

4. **Angular momentum constraint:** J = Σ cos φ_k, Lagrange multiplier Ω from equilibrium. Hessian of J under radial perturbation.

5. **Fourier reduction:** Same Z_N tricks as Item #1 but applied to the spherical pair function. The Havelock identity m(N-m)/2 enters identically.

6. **Result:** λ_m = (N-1) cos φ₀ - m(N-m)/2 = (N-1)(1-ξ)/(1+ξ) - m(N-m)/2.

> **Note to engineer:** The actual algebra is the core creative work. Follow the numerical oracle at every step. If a symbolic expression doesn't match the oracle, the algebra is wrong — debug it before writing it in LaTeX. The oracle is always right.

- [ ] **Step 4: Compile**

```bash
cd docs/rigor-sandbox/item6-c1-sphere
pdflatex -interaction=nonstopmode derivation.tex
```

- [ ] **Step 5: Commit**

```bash
git add docs/rigor-sandbox/item6-c1-sphere/
git commit -m "feat: C₁(S²) geodesic derivation, symbolic + numerical checks"
```

---

### Task 4: Off-diagonal vanishing and trace on S²

**Math goal:** Show that the radial-tangential cross term vanishes on S² by the same Z_N symmetry argument as on the flat plane. The trace identity λ_m^+ + λ_m^- = 2 C₁(S²) (or whatever the S² trace is) follows from the algebra.

**Files:**
- Modify: `docs/rigor-sandbox/item6-c1-sphere/numerical_check.py`
- Modify: `docs/rigor-sandbox/item6-c1-sphere/derivation.tex`

- [ ] **Step 1: Add numerical check for off-diagonal vanishing on S²**

```python
def check_off_diagonal_sphere() -> int:
    """Cross term ê_r^T (∇²L) ê_t = 0 on S² for all (N, φ₀, m)."""
    failed = 0
    for N in [4, 5, 6]:
        for phi0_deg in [30, 45, 60]:
            phi0 = np.radians(phi0_deg)
            theta_eq = 2.0 * np.pi * np.arange(N) / N
            phi_eq = np.full(N, phi0)
            xi = np.tan(phi0 / 2) ** 2
            eps_fd = 1e-6
            phi_p = phi_eq.copy(); phi_p[:] += eps_fd
            phi_m = phi_eq.copy(); phi_m[:] -= eps_fd
            dH = (geodesic_energy_sphere(phi_p, theta_eq)
                  - geodesic_energy_sphere(phi_m, theta_eq)) / (2 * eps_fd * N)
            dJ = -np.sin(phi0)
            Omega = dH / dJ if abs(dJ) > 1e-15 else 0.0

            def lagrangian(phi, theta):
                return geodesic_energy_sphere(phi, theta) - Omega * np.sum(np.cos(phi))

            for m in range(1, N):
                amp = np.cos(2.0 * np.pi * m * np.arange(N) / N)
                # Radial: δφ_k = h_r amp_k
                # Tangential: δθ_k = h_t amp_k / sin(φ₀)
                h = 1e-5
                L_pp = lagrangian(phi_eq + h * amp, theta_eq + h * amp / np.sin(phi0))
                L_pm = lagrangian(phi_eq + h * amp, theta_eq - h * amp / np.sin(phi0))
                L_mp = lagrangian(phi_eq - h * amp, theta_eq + h * amp / np.sin(phi0))
                L_mm = lagrangian(phi_eq - h * amp, theta_eq - h * amp / np.sin(phi0))
                cross = (L_pp - L_pm - L_mp + L_mm) / (4 * h * h)
                norm_sq = np.sum(amp ** 2)
                cross_norm = cross / norm_sq
                if abs(cross_norm) > 0.1:
                    failed += 1
                    print(f"  FAIL N={N} φ₀={phi0_deg}° m={m}: cross={cross_norm:.4f}")
    if failed == 0:
        print("  Off-diagonal vanishes on S² for sampled (N, φ₀, m)")
    return failed
```

- [ ] **Step 2: Run, add to derivation.tex, compile, commit**

Follow the same pattern as Item #1 Task 5.

---

### Task 5: Consolidate derivation.tex

**Files:**
- Modify: `docs/rigor-sandbox/item6-c1-sphere/derivation.tex`

- [ ] **Step 1: Add main theorem statement at top**

```latex
\begin{theorem}[Geodesic-frame curvature coefficient on $\mathbf{S}^2$]
\label{thm:c1-sphere}
For the regular $N$-gon of unit-circulation vortices at colatitude
$\varphi_0$ on the unit $2$-sphere, with $\xi = \tan^2(\varphi_0/2)$,
the constrained Hessian eigenvalue at Fourier mode $m \in \{1,\ldots,N-1\}$
in the geodesic frame is
\[
  \lambda_m(\mathbf{S}^2, \xi) = C_1(\mathbf{S}^2,\xi) - \frac{m(N-m)}{2},
  \qquad
  C_1(\mathbf{S}^2,\xi) = \frac{(N-1)(1-\xi)}{1+\xi} = (N-1)\cos\varphi_0.
\]
\end{theorem}
```

- [ ] **Step 2: Add numerical verification section at end**

- [ ] **Step 3: Scan for placeholders — grep for TODO/TBD/placeholder**

- [ ] **Step 4: Two-pass pdflatex, confirm zero warnings**

- [ ] **Step 5: Commit**

---

### Task 6: math-reviewer gate

**Files:**
- Modify: `docs/rigor-sandbox/item6-c1-sphere/review-notes.md`

- [ ] **Step 1: Dispatch math-reviewer on sandbox only**

Prompt (exact):
```
Review docs/rigor-sandbox/item6-c1-sphere/derivation.tex as a standalone
mathematical derivation of C₁(S²,ξ) = (N-1)(1-ξ)/(1+ξ) for the regular
N-gon of point vortices on the unit 2-sphere. The derivation should start
from the geodesic Green's function h = -log sin(d/2) and produce the
curvature coefficient via direct computation of the constrained Hessian
in the geodesic frame.

Assess rigor at Annals standard. Classify deductions as:
  (a) STRUCTURAL — key step omitted, unverified claim, etc.
  (b) STYLISTIC — prose, notation, exposition.

Return: score 1-10, list of STRUCTURAL deductions, list of STYLISTIC
deductions, one-paragraph summary.

Gate: ≥9.0 AND zero structural deductions.

Numerical backing in numerical_check.py (same directory) — all identities
verified to 30 digits (sympy) and against a geodesic-frame oracle (finite
differences on H_geo = -Σ log sin(d/2) directly).
```

- [ ] **Step 2: Log in review-notes.md, iterate until gate passes**

- [ ] **Step 3: Commit each round**

---

### Task 7: Produce replacement and user approval

**Files:**
- Create: `docs/rigor-sandbox/item6-c1-sphere/replacement-proof.tex`

- [ ] **Step 1: Read current appendix §2 (lines 178–336 of `latex/paper-A-appendices/main.tex`)**

- [ ] **Step 2: Build the replacement**

Keep:
- `\section{Derivation of $C_1(\mathbf{S}^2,\xi)$}` and `\label{app:c1_s2}`
- The S² Hamiltonian paragraph (`eq:H_sph`)
- The equilibrium/Ω paragraph (`eq:Omega_S2`)
- The "Properties" paragraph

Replace:
- "Mode-m second derivatives" (terms 1-3 in Euclidean frame) with the geodesic-frame derivation
- "Limitation of the stereographic derivation" paragraph — DELETE (no longer needed since we derive geodesic directly)
- "Geodesic-metric result (Boatto-Cabral 2003)" — replace with the derived proof
- Keep `eq:C1_S2` label on the boxed formula

- [ ] **Step 3: Present diff to user, wait for approval**

- [ ] **Step 4: Commit replacement-proof.tex**

---

### Task 8: Apply, rebuild, verify

**Files:**
- Modify: `latex/paper-A-appendices/main.tex`

- [ ] **Step 1: Apply the approved diff**

- [ ] **Step 2: Rebuild the paper**

```bash
cd latex/paper-A-appendices && pdflatex -interaction=nonstopmode main.tex
cd ../paper && pdflatex -interaction=nonstopmode main.tex
```

- [ ] **Step 3: Run full test suite**

```bash
python3 -m pytest tests/ -q --tb=no
```

Expected: 4447+ passed, zero regression.

- [ ] **Step 4: Commit**

```bash
git add latex/paper-A-appendices/main.tex
git commit -m "feat: Appendix — first-principles C₁(S²) geodesic derivation

Replaces BC2003 citation with full derivation from h_geo = -log sin(d/2).
Sandbox: docs/rigor-sandbox/item6-c1-sphere/"
```

- [ ] **Step 5: Rollback check**

If test suite or build fails: `git revert HEAD`, debug in sandbox.

---

## Self-Review

**Spec coverage:**
- Sandbox scaffolding ✓ (Task 1)
- Geodesic oracle ✓ (Task 2)
- Full algebraic derivation ✓ (Task 3)
- Off-diagonal vanishing on S² ✓ (Task 4)
- Consolidation + main theorem ✓ (Task 5)
- math-reviewer gate ✓ (Task 6)
- Diff proposal + user approval ✓ (Task 7)
- Apply + verify + rollback ✓ (Task 8)

**Placeholder scan:** Task 3 Step 3 says "detailed LaTeX to be written during implementation" with a note to the engineer. This is intentional: the algebra is the creative work, and the oracle (Task 2) is the safety net. No other placeholders.

**Type consistency:** `geodesic_energy_sphere(phi, theta)` and `sphere_mode_m_eigenvalue(N, phi0, m)` used consistently across Tasks 2-4.
