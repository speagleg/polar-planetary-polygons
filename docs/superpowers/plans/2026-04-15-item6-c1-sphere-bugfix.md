# Item #6 — C₁(S²) Bugfix + Pell Unification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the incorrect C₁(S²) = (N-1)(1-ξ)/(1+ξ) formula throughout the codebase and papers, replacing it with the correct C₁(S²) = (N-1)(1+ξ²)/(1+ξ)² (already derived in the appendix as C₁^eucl). Update S² thresholds from {1/3, 1/5, 1/7, 1/19} to Pell units {1, 2-√3, 3-2√2, 9-4√5}. Rewrite the "rational vs irrational" narrative as a Pell unification.

**Architecture:** Start with numerical verification of the correct formula (already done in Task 2), fix code and tests, then fix papers. Same sandbox gates as Item #1.

**Tech Stack:** Python 3, sympy, numpy, pytest, LaTeX.

---

## File Structure

**Modify (Python source — 4 files):**
- `src/planetary_polygons/extensions/riemannian_havelock.py:147-165` — `C1_sphere()`
- `src/planetary_polygons/extensions/algebraic_thresholds.py:142-176` — `sphere_stability_threshold()`, `sphere_threshold_table()`
- `src/planetary_polygons/extensions/oblate_spheroid.py:68-75` — `C1_sphere()`
- `src/planetary_polygons/extensions/spheroidal_havelock.py:147-149` — `C1_sphere_formula()`

**Modify (tests — 1 primary file):**
- `tests/test_algebraic_thresholds.py:169-229` — 6 threshold assertions + C₁ condition test

**Modify (LaTeX — appendix + main paper + others):**
- `latex/paper-A-appendices/main.tex:277-335` — remove "Limitation" paragraph, update boxed formula
- `latex/paper/main.tex:1046-1133` — §4.2 threshold table + rationality claims
- `latex/companion/main.tex` — threshold explanation
- `CLAUDE.md` — formula reference

**Existing sandbox (from earlier Tasks 1-2):**
- `docs/rigor-sandbox/item6-c1-sphere/numerical_check.py` — oracle already confirms C₁^eucl

---

### Task 1: Verify new thresholds and Pell structure in sandbox

**Files:**
- Modify: `docs/rigor-sandbox/item6-c1-sphere/numerical_check.py`

- [ ] **Step 1: Add threshold verification checks**

Append to `numerical_check.py`:

```python
def check_new_thresholds() -> int:
    """Verify the correct S² thresholds are Pell units.

    Threshold equation: (N-1)(1+ξ²)/(1+ξ)² = m(N-m)/2
    Quadratic: (N-1-T)ξ² - 2Tξ + (N-1-T) = 0, T = m(N-m)/2
    Solution: ξ* = (T - √(T² - A²)) / A where A = N-1-T.
    """
    from mpmath import mp, mpf, sqrt as msqrt
    mp.dps = 50
    import sympy as sp

    cases = [
        # (N, m, expected_xi_exact_str, expected_float)
        (3, 1, "1", 1.0),
        (4, 2, "2 - sqrt(3)", 2 - 3**0.5),
        (5, 2, "3 - 2*sqrt(2)", 3 - 2 * 2**0.5),
        (6, 3, "9 - 4*sqrt(5)", 9 - 4 * 5**0.5),
    ]
    failed = 0
    for N, m, expr_str, xi_expected in cases:
        T = mpf(m * (N - m)) / 2
        A = mpf(N - 1) - T
        if A > 0:
            disc = T ** 2 - A ** 2
            xi_calc = (T - msqrt(disc)) / A
        else:
            xi_calc = mpf(0)

        # Verify C₁^eucl(xi*) = T
        c1 = (N - 1) * (1 + xi_calc ** 2) / (1 + xi_calc) ** 2
        diff_c1 = abs(c1 - T)

        # Verify against expected float
        diff_xi = abs(float(xi_calc) - xi_expected)

        ok = diff_c1 < 1e-30 and diff_xi < 1e-10
        status = "OK" if ok else "FAIL"
        print(f"  N={N} m={m}: xi*={float(xi_calc):.10f} ({expr_str}) "
              f"C1(xi*)={float(c1):.10f} T={float(T)} [{status}]")
        if not ok:
            failed += 1

    # Verify H²/S² duality: C₁^{S²}(ξ) = C₁^{H²}(-ξ)
    # H²: (N-1)(1+ξ²)/(1-ξ)²   S²: (N-1)(1+ξ²)/(1+ξ)²
    xi_sym = sp.Symbol('xi')
    c1_s2 = (1 + xi_sym ** 2) / (1 + xi_sym) ** 2
    c1_h2_neg = (1 + (-xi_sym) ** 2) / (1 - (-xi_sym)) ** 2
    diff = sp.simplify(c1_s2 - c1_h2_neg)
    if diff != 0:
        print(f"  FAIL: H²/S² duality broken: diff = {diff}")
        failed += 1
    else:
        print("  H²/S² duality C₁(S²,ξ) = C₁(H²,-ξ) verified symbolically")

    if failed == 0:
        print("  All new thresholds + Pell structure verified")
    return failed
```

Add to `main()`:

```python
    print("== New S² thresholds (Pell units) ==")
    if check_new_thresholds():
        print("FAILED thresholds")
        return 1
```

- [ ] **Step 2: Run**

```bash
python3 docs/rigor-sandbox/item6-c1-sphere/numerical_check.py
```

Expected: all checks pass including new thresholds.

- [ ] **Step 3: Commit**

```bash
git add docs/rigor-sandbox/item6-c1-sphere/
git commit -m "test: verify correct S² thresholds (Pell units) + H²/S² duality"
```

---

### Task 2: Fix `riemannian_havelock.py` C1_sphere()

**Files:**
- Modify: `src/planetary_polygons/extensions/riemannian_havelock.py:147-165`

- [ ] **Step 1: Update the function**

Replace lines 147-165:

```python
def C1_sphere(N, xi):
    """
    Exact C₁ coefficient for N-vortex ring on S².

    C₁(S², ξ) = (N-1)(1+ξ²)/(1+ξ)²

    This is the Hessian eigenvalue coefficient in the stereographic frame,
    matching the Euclidean-frame derivation in Appendix A and confirmed by
    LMR05 (Laurent-Polz, Montaldi, Roberts 2005, Theorem 4.2).

    The H²/S² duality is: C₁(S²,ξ) = C₁(H²,-ξ), i.e.
    (1+ξ²)/(1+ξ)² vs (1+ξ²)/(1-ξ)², related by sign-flipping ξ.

    Parameters
    ----------
    N : int
        Ring size.
    xi : float
        ξ = tan²(φ₀/2), stereographic parameter at colatitude φ₀.

    Returns
    -------
    float
        C₁ value. For ξ→0: C₁→N-1 (flat limit). C₁→(N-1)/2 as ξ→∞.
    """
    return (N - 1) * (1 + xi**2) / (1 + xi)**2
```

- [ ] **Step 2: Commit**

```bash
git add src/planetary_polygons/extensions/riemannian_havelock.py
git commit -m "fix: C1_sphere uses correct (1+ξ²)/(1+ξ)² formula"
```

---

### Task 3: Fix `algebraic_thresholds.py` sphere_stability_threshold()

**Files:**
- Modify: `src/planetary_polygons/extensions/algebraic_thresholds.py:142-176`

- [ ] **Step 1: Update the function**

Replace lines 142-176:

```python
def sphere_stability_threshold(N):
    """
    Exact destabilization threshold ξ_crit for the N-ring on S².

    On S², C₁(S², ξ) = (N-1)(1+ξ²)/(1+ξ)² decreases with ξ, so curvature
    gradually destabilizes the ring. Marginal stability at C₁ = T:

        (N-1-T) ξ² - 2T ξ + (N-1-T) = 0,   T = m(N-m)/2,  m = floor(N/2)

    Explicit closed form: ξ_crit = (T - √(T² - (N-1-T)²)) / (N-1-T).

    These are Pell-equation fundamental units in quadratic fields:
        N=3: ξ*=1, N=4: ξ*=2-√3, N=5: ξ*=3-2√2, N=6: ξ*=9-4√5.

    Returns
    -------
    float or None
        Exact threshold (as float), or None if N ≥ 7 (unstable at all ξ>0).
    """
    m = N // 2
    T = m * (N - m) / 2.0
    A = (N - 1) - T
    if A <= 0:
        # N >= 7: T >= N-1, no positive threshold
        return None
    disc = T * T - A * A
    if disc < 0:
        return None
    import math
    xi_crit = (T - math.sqrt(disc)) / A
    return xi_crit if xi_crit > 0 else None


def sphere_threshold_table(N_max=12):
    """
    Table of S² destabilization thresholds for N = 3, ..., N_max.

    Returns list of dicts with keys: N, xi_crit (float or None).
    Only N ≤ 6 return non-None values.
    """
    return [{'N': N, 'xi_crit': sphere_stability_threshold(N)}
            for N in range(3, N_max + 1)]
```

- [ ] **Step 2: Commit**

```bash
git add src/planetary_polygons/extensions/algebraic_thresholds.py
git commit -m "fix: sphere thresholds use correct quadratic formula (Pell units)"
```

---

### Task 4: Fix `oblate_spheroid.py` and `spheroidal_havelock.py`

**Files:**
- Modify: `src/planetary_polygons/extensions/oblate_spheroid.py:68-75`
- Modify: `src/planetary_polygons/extensions/spheroidal_havelock.py:147-149`

- [ ] **Step 1: Fix oblate_spheroid.py**

Replace the C1_sphere function body (line 74-75):

Old: `return (N - 1) * (1 - xi) / (1 + xi)`
New: `return (N - 1) * (1 + xi**2) / (1 + xi)**2`

Update docstring to match.

- [ ] **Step 2: Fix spheroidal_havelock.py**

Replace line 149:

Old: `return (N - 1) * (1 - xi) / (1 + xi)`
New: `return (N - 1) * (1 + xi**2) / (1 + xi)**2`

Update docstring to match.

- [ ] **Step 3: Commit**

```bash
git add src/planetary_polygons/extensions/oblate_spheroid.py src/planetary_polygons/extensions/spheroidal_havelock.py
git commit -m "fix: C1_sphere in oblate_spheroid and spheroidal_havelock"
```

---

### Task 5: Fix tests

**Files:**
- Modify: `tests/test_algebraic_thresholds.py:169-229`

- [ ] **Step 1: Update threshold assertions**

Replace lines 169-186:

```python
def test_sphere_threshold_n3():
    xi = sphere_stability_threshold(3)
    assert abs(xi - 1.0) < 1e-12, f"N=3: expected 1, got {xi}"


def test_sphere_threshold_n4():
    xi = sphere_stability_threshold(4)
    import math
    assert abs(xi - (2 - math.sqrt(3))) < 1e-12, f"N=4: expected 2-√3, got {xi}"


def test_sphere_threshold_n5():
    xi = sphere_stability_threshold(5)
    import math
    assert abs(xi - (3 - 2 * math.sqrt(2))) < 1e-12, f"N=5: expected 3-2√2, got {xi}"


def test_sphere_threshold_n6():
    xi = sphere_stability_threshold(6)
    import math
    assert abs(xi - (9 - 4 * math.sqrt(5))) < 1e-12, f"N=6: expected 9-4√5, got {xi}"
```

- [ ] **Step 2: Update C₁ condition test (lines 199-211)**

Replace:

```python
def test_sphere_threshold_satisfies_C1_condition():
    """
    For N ≤ 6, at ξ_crit on S², C₁(S², ξ_crit) = m(N-m)/2.
    C₁(S², ξ) = (N-1)(1+ξ²)/(1+ξ)².
    """
    for N in range(3, 7):
        xi = sphere_stability_threshold(N)
        assert xi is not None
        m = N // 2
        T_half = m * (N - m) / 2.0
        C1 = (N - 1) * (1 + xi**2) / (1 + xi)**2
        assert abs(C1 - T_half) < 1e-10, f"N={N}: C1={C1} != T_half={T_half}"
```

- [ ] **Step 3: Run the tests**

```bash
python3 -m pytest tests/test_algebraic_thresholds.py -v
```

Expected: all pass.

- [ ] **Step 4: Run full test suite**

```bash
python3 -m pytest tests/ -q --tb=short 2>&1 | tail -20
```

Expected: some tests in `test_spheroidal_havelock.py`, `test_oblate_spheroid.py`, `test_riemannian_havelock.py` may fail if they assert old numerical values. Fix any remaining failures by updating expected values in those test files.

- [ ] **Step 5: Commit**

```bash
git add tests/
git commit -m "fix: update all S² threshold tests for correct Pell-unit values"
```

---

### Task 6: Fix appendix

**Files:**
- Modify: `latex/paper-A-appendices/main.tex:262-335`

- [ ] **Step 1: Read current appendix §2 (lines 262-335)**

- [ ] **Step 2: Remove "Limitation" paragraph (lines 277-294)**

Delete the paragraph starting "The formula~\eqref{eq:C1-eucl-frame} gives the second variation in the \emph{Euclidean stereographic frame}..." through "...not the intrinsic sphere."

- [ ] **Step 3: Remove "Geodesic-metric result" paragraph (lines 296-316)**

Delete the paragraph citing BC2003 and the boxed formula eq:C1_S2 with the WRONG formula.

- [ ] **Step 4: Replace with corrected text after eq:C1-eucl-frame**

After the existing eq:C1-eucl-frame (line 275), add:

```latex
\paragraph{The correct stability coefficient.}
The formula~\eqref{eq:C1-eucl-frame} is the correct $C_1$ for stability
analysis on~$\mathbf{S}^2$.  The radial eigenvalue of the constrained
Hessian $\nabla^2(H_{\mathrm{sph}} - \Omega J)$ in the stereographic
frame at mode~$m$ is $[C_1 - m(N{-}m)/2]/\xi$, and the tangential
eigenvalue is $m(N{-}m)/(2\xi)$ (by the Riemannian Havelock identity:
the tangential second variation depends only on the azimuthal structure,
which is conformally invariant).  Positive semi-definiteness therefore
requires $C_1 \ge m(N{-}m)/2$.

Renaming for consistency with the main text:
\begin{equation}\label{eq:C1_S2}
  \boxed{C_1(\mathbf{S}^2,\xi)
    \;=\; \frac{(N-1)(1+\xi^2)}{(1+\xi)^2}.}
\end{equation}
This matches the stability condition of
\citet{LaurentPolzMontaldiRoberts2005} (Theorem~4.2), which gives
marginal stability at $\cos^2\!\varphi_0 = (\ell{-}1)(N{-}\ell{-}1)/(N{-}1)$,
equivalent to $C_1 = \ell(N{-}\ell)/2$ via the identity
$C_1 = (N{-}1)(1 + \cos^2\!\varphi_0)/2$.
Numerical verification against direct diagonalization of the constrained
Lagrangian Hessian for $N \in \{4, \ldots, 7\}$ at
$\xi \in \{0.15, 0.3, 0.5, 0.7\}$ confirms the formula to $10^{-7}$
(\texttt{docs/rigor-sandbox/item6-c1-sphere/numerical\_check.py}).

\paragraph{$\mathbf{H}^2$/$\mathbf{S}^2$ duality.}
On the hyperbolic plane, $C_1(\mathbf{H}^2, \xi) = (N{-}1)(1+\xi^2)/(1-\xi)^2$.
The two formulas are related by $\xi \to -\xi$ (equivalently, by
flipping the sign of the Gaussian curvature $K$), giving a clean
duality:
\[
  C_1(\mathbf{S}^2, \xi) = \frac{(N-1)(1+\xi^2)}{(1+\xi)^2},
  \qquad
  C_1(\mathbf{H}^2, \xi) = \frac{(N-1)(1+\xi^2)}{(1-\xi)^2}.
\]
```

- [ ] **Step 5: Update "Properties" list (lines 318-335)**

Replace the properties list:

```latex
\paragraph{Properties.}
\begin{itemize}
\item At the pole ($\xi=0$): $C_1 = N-1$, recovering the flat-plane Havelock value.
\item $C_1$ decreases monotonically from $N-1$ at the pole to $(N-1)/2$
  as $\xi \to \infty$; the equator ($\xi = 1$) gives $C_1 = (N-1)/2$.
\item The threshold equation $C_1 = m(N{-}m)/2$ yields a quadratic in $\xi$:
  $(N{-}1{-}T)\xi^2 - 2T\xi + (N{-}1{-}T) = 0$ with $T = m(N{-}m)/2$,
  $m = \lfloor N/2 \rfloor$.  The smaller root is
  $\xi^*(N) = (T - \sqrt{T^2 - (N{-}1{-}T)^2})/(N{-}1{-}T)$.
\item Explicit thresholds:
  $\xi^*(3) = 1$, $\xi^*(4) = 2 - \sqrt{3}$,
  $\xi^*(5) = 3 - 2\sqrt{2}$, $\xi^*(6) = 9 - 4\sqrt{5}$.
  These are fundamental units (Pell solutions) in the quadratic fields
  $\mathbb{Q}(\sqrt{3})$, $\mathbb{Q}(\sqrt{2})$, $\mathbb{Q}(\sqrt{5})$,
  mirroring the $\mathbf{H}^2$ thresholds.
\item For $N \ge 7$, $C_1(\mathbf{S}^2,0) = N-1 < m(N{-}m)/2$ at
  $m = \lfloor N/2\rfloor$, so the polygon is unstable at every latitude.
\end{itemize}
```

- [ ] **Step 6: Compile appendix**

```bash
cd latex/paper-A-appendices && pdflatex -interaction=nonstopmode main.tex
```

- [ ] **Step 7: Commit**

```bash
git add latex/paper-A-appendices/main.tex
git commit -m "fix: appendix C₁(S²) — remove wrong BC2003 citation, use correct (1+ξ²)/(1+ξ)²"
```

---

### Task 7: Fix paper/main.tex §4.2 threshold section

**Files:**
- Modify: `latex/paper/main.tex:1046-1133`

- [ ] **Step 1: Read current §4.2 (lines 1046-1133)**

- [ ] **Step 2: Replace eq:C1_S2 (line 1069-1071)**

Old:
```latex
  C_1(\mathbf{S}^2,\,\xi) = \frac{(N-1)(1-\xi)}{1+\xi} = (N-1)\cos\varphi_0,
```

New:
```latex
  C_1(\mathbf{S}^2,\,\xi) = \frac{(N-1)(1+\xi^2)}{(1+\xi)^2},
```

- [ ] **Step 3: Replace the marginal stability discussion (lines 1074-1082)**

Old discusses cos φ_crit being rational and ξ_crit ∈ Q. Replace with the quadratic equation and Pell-unit structure. Keep eq:cos_crit and eq:xi_crit_S2 labels but with corrected content.

- [ ] **Step 4: Replace the threshold table (lines 1085-1099)**

New table with correct ξ* values: 1, 2-√3, 3-2√2, 9-4√5 and updated colatitudes.

- [ ] **Step 5: Replace the rationality paragraph (lines 1101-1106)**

Old: "The thresholds ... are exact rational numbers..."
New: discuss Pell-unit structure and H²/S² duality.

- [ ] **Step 6: Update the Remark (lines 1108-1126)**

The 1/(2N-3) pattern and N=6 break are for the OLD formula. Rewrite with the correct quadratic structure.

- [ ] **Step 7: Compile and commit**

```bash
cd latex/paper && pdflatex -interaction=nonstopmode main.tex
git add latex/paper/main.tex
git commit -m "fix: Paper I §4.2 — correct S² thresholds (Pell units, not rational)"
```

---

### Task 8: Fix companion, CLAUDE.md

**Files:**
- Modify: `latex/companion/main.tex` — threshold explanation (~lines 648-680)
- Modify: `CLAUDE.md` — formula reference

- [ ] **Step 1: Update companion threshold section**

Find and replace the "thresholds are all rational numbers" discussion. Replace threshold values. Update the explanation from "linear dependence on cos φ₀" to "quadratic equation producing Pell units."

- [ ] **Step 2: Update CLAUDE.md**

Replace:
```
# S² exact thresholds (all rational)
# N=3: 1/3,  N=4: 1/5,  N=5: 1/7,  N=6: 1/19,  N≥7: None
```

With:
```
# S² exact thresholds (Pell units in quadratic fields)
# N=3: 1,  N=4: 2-√3,  N=5: 3-2√2,  N=6: 9-4√5,  N≥7: None
# C₁(S²,ξ) = (N-1)(1+ξ²)/(1+ξ)²  [NOT the old (N-1)(1-ξ)/(1+ξ)]
```

Also update the C1_S2 formula line.

- [ ] **Step 3: Commit**

```bash
git add latex/companion/main.tex CLAUDE.md
git commit -m "fix: companion + CLAUDE.md — correct S² thresholds and formula"
```

---

### Task 9: Fix paper-2, paper-3, paper-4 references

**Files:**
- Modify: `latex/paper-2-physics/main.tex` — formula reference (~line 1532)
- Modify: `latex/paper-3-gravity/main.tex` — table entry (~line 3752)
- Modify: `latex/paper-4-field-theory/main.tex` — formula reference (~line 118, 288)

- [ ] **Step 1: Find and fix each reference**

Search each file for `(1-xi)/(1+xi)` or `(1{-}\xi)/(1{+}\xi)` or `C_1.*S.*2` and replace with the correct formula.

- [ ] **Step 2: Compile each paper**

```bash
for d in paper-2-physics paper-3-gravity paper-4-field-theory; do
    cd latex/$d && pdflatex -interaction=nonstopmode main.tex; cd ../..
done
```

- [ ] **Step 3: Commit**

```bash
git add latex/paper-2-physics/ latex/paper-3-gravity/ latex/paper-4-field-theory/
git commit -m "fix: correct C₁(S²) formula in Papers II, III, IV"
```

---

### Task 10: math-reviewer on corrected appendix

**Files:**
- Modify: `docs/rigor-sandbox/item6-c1-sphere/review-notes.md`

- [ ] **Step 1: Dispatch math-reviewer on the corrected appendix §2 only**

Focus: does the corrected appendix correctly derive C₁(S²) = (N-1)(1+ξ²)/(1+ξ)² from the stereographic Hamiltonian? Is the "Limitation" paragraph correctly removed? Is the H²/S² duality stated rigorously?

Gate: ≥9.0, zero structural deductions.

- [ ] **Step 2: Iterate until gate passes**

- [ ] **Step 3: Commit review notes**

---

### Task 11: Full verification

- [ ] **Step 1: Run full test suite**

```bash
python3 -m pytest tests/ -q --tb=no
```

Expected: 4447+ passed, zero failures.

- [ ] **Step 2: Rebuild all papers**

```bash
for d in paper paper-A-appendices paper-2-physics paper-3-gravity paper-4-field-theory companion; do
    cd latex/$d && pdflatex -interaction=nonstopmode main.tex 2>&1 | grep "Error" | head -3; cd ../..
done
```

- [ ] **Step 3: Final commit**

```bash
git commit --allow-empty -m "verified: all tests pass, all papers build after C₁(S²) bugfix"
```

---

## Self-Review

**Spec coverage:**
- Sandbox verification ✓ (Task 1)
- 4 Python source fixes ✓ (Tasks 2-4)
- Test fixes ✓ (Task 5)
- Appendix fix ✓ (Task 6)
- Main paper §4.2 fix ✓ (Task 7)
- Companion + CLAUDE.md ✓ (Task 8)
- Papers II/III/IV ✓ (Task 9)
- math-reviewer gate ✓ (Task 10)
- Full verification ✓ (Task 11)

**Placeholder scan:** Task 7 Steps 3-6 describe what to change rather than giving exact LaTeX — this is intentional because the exact replacement text depends on reading the current prose and adapting it. The engineer must read the current text and rewrite, not paste a template.

**Scope note:** The `test_spheroidal_havelock.py` and `test_oblate_spheroid.py` tests may break after Task 4. Task 5 Step 4 handles this by running the full suite and fixing any remaining failures.
