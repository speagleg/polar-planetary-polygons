# Session Integration Catalog

**Purpose:** Catalog of all computation scripts, mathematical results, and code changes from
this work session (H² stability, N_crit theorem, γ coefficient) for integration into the new
repo build. Written for a downstream agent to act on directly.

**Date:** 2026-03-18
**Branch context:** `main` — all temp files in `/tmp/` and `/tmp/polygon_reviewer_scratch/`

---

## 1. New Mathematical Results (Must Be Encoded)

These are the core deliverables of the session. Each needs to exist in both the source code
and the paper.

### 1.1 Exact C₁ Formula for H²

```
C₁(H², ξ) = (N−1)(1+ξ²) / (1−ξ)²,    ξ = r_E²/a² = |K|·r_E²
```

Where:
- `r_E` = Euclidean ring radius in Poincaré disk model
- `a` = curvature radius, `K = −1/a²`
- `ξ` is the square of the Euclidean radius in units of the curvature radius

This formula is **exact** (derived from the H² Green's function `h = −ln sinh(d/(2a))`),
verified numerically to ~10⁻⁵ against finite-difference Hessian computations.

**Analogous sphere formula:** `C₁(S², ξ) = (N−1)(1−ξ)/(1+ξ)`, ξ = KR² > 0

The Riemannian Havelock identity in the correct form is:
```
λ_m · r_E² + m(N−m)/2 = C₁(H², ξ)
```
Note: the existing `riemannian_havelock.py` uses the WRONG form `λ_m + m(N-m)/2 = C₁`,
which is only correct when r_E = 1.

### 1.2 Exact 7→8 Stability Threshold

Setting `C₁(H², ξ) = m(N−m)/2|_{N=8, m=4} = 8` gives the quadratic:
```
ξ² − 16ξ + 1 = 0   →   ξ* = 8 − 3√7 ≈ 0.0627
```

In geodesic coordinates: `ρ/a ≈ 0.52`, equivalently `|K|ρ² ≈ 0.27`.

### 1.3 Exact γ Coefficient

```
γ = 1/(ξ*)² = 127 + 48√7 ≈ 254
```

Algebraic verification: `(8 − 3√7)²(127 + 48√7) = 127² − 48²·7 = 16129 − 16128 = 1 ✓`

Physical meaning: the 7→8 jump occurs at `|K|·r_E² = ξ* = γ^{−1/2}`.

### 1.4 Eigenvalue Expansion (O(K) behavior)

For the N=7 ring, most-dangerous mode m=3:
```
λ₃(N=7, ξ) = 12|K| / (1−ξ)² = 12|K| + O(K²r_E²)
```
This is **positive at first order in |K|** — N=7 is stabilized immediately by H² curvature.

For the N=8 ring, critical mode m=4:
```
λ₄(N=8) = [−1 + 14ξ + 28ξ² + ...] / r_E²
         = −1/r_E² − 14K + 28K²r_E² + O(K³)
```

### 1.5 Critical Sign Fix in Ω Formula

The angular velocity Ω for the ring equilibrium on H² requires:
```python
# WRONG (pre-session):
dH_dx0 = +(N-1)/(2*r_E) - (N-1)*r_E/(a**2 - r_E**2)

# CORRECT:
dH_dx0 = -(N-1)/(2*r_E) - (N-1)*r_E/(a**2 - r_E**2)
```
The flat-plane contribution `∂H_flat/∂x_0 = −(N−1)/(2r_E)` is **negative** because the
gradient of `H = −Σ ln|z_j − z_k|` points away from other vortices. This sign error caused
all eigenvalues to be wrong (all negative) in previous versions.

### 1.6 Corrected Riemannian Havelock Normalization

The C₁ in `riemannian_havelock.py` is dimensionless. The eigenvalue λ_m has units [1/r_E²].
The correct identity is:
```
λ_m · r_E² = C₁(H², ξ) − m(N−m)/2
```
The existing `havelock_sum` function computes `T_m = m(N−m)` correctly, but the connection
to the H² eigenvalue with correct r_E² scaling is missing.

### 1.7 N_crit Table (Verified, Corrected)

| ρ/a | N_crit | Notes |
|------|--------|-------|
| 0.30–0.50 | 7 | No change from flat |
| ≈0.52 | 8 | Exact threshold: ξ* = 8−3√7 |
| 0.65–0.75 | 9 | |
| 0.80 | 10 | |
| 0.90 | 11 | |
| 1.0 | 12 | |
| 1.2 | 16 | |
| ≥1.5 | ≥24 | Tested to N=24 |

---

## 2. Temp Scripts: Location and Status

All scripts are in `/tmp/` or `/tmp/polygon_reviewer_scratch/` and will be lost on session
end. They need to be copied to the repo.

### 2.1 Core H² Stability Scripts

#### `/tmp/ncrit_h2_sweep.py` — **PRIMARY, USE THIS**
Comprehensive N_crit sweep + corrected Riemannian Havelock verification.

Key content:
- `H_hyp(z_re, z_im, a)` — correct H² Hamiltonian
- `J_hyp(z_re, z_im, a)` — correct SO(2,1) moment map
- `get_Omega(N, r_E, a)` — correct Ω with fixed sign
- `fourier_eigenvalue(m, N, rho, a)` — Lagrangian eigenvalue via FD Hessian
- `min_eigenvalue(N, rho, a)` — minimum over all modes
- Fine grid N_crit sweep (ρ/a = 0.30 to 3.0)
- N=8 transition scan (ρ/a = 0.40 to 0.70 in steps of 0.02)
- Riemannian Havelock verification: `c1 = lam * r_E**2 + m*(N-m)/2` (mode-independent to 10⁻⁵)

**Target:** `src/planetary_polygons/extensions/h2_stability.py` (new file)

#### `/tmp/ncrit_h2_v3.py` — **SECONDARY, for equilibrium gradient check**
Same core functions as sweep but includes an explicit equilibrium gradient sanity check
(`∂F/∂x_0 ≈ 10⁻⁹`). Good for the test suite.

**Target:** Extract `equilibrium_gradient_check()` function for tests.

#### `/tmp/ncrit_h2_v2.py` — Historical, do not use
Contains the wrong `get_Omega` sign. Kept for reference only.

#### `/tmp/ncrit_h2_clean.py` — Historical alternative implementation
Contains an analytic eigenvalue computation (different approach: explicit pair summation
with hyperbolic correction terms). Useful as cross-check. Has the wrong sign too.

#### `/tmp/ncrit_exact.py` — Perturbative model (DIFFERENT physics)
Uses the flat-constraint model with exact curved Green's function, not the full H²
dynamics. Gives different N_crit because it uses flat-plane angular momentum constraint
rather than the H² moment map J. Do **not** merge into the main H² module — label as
"flat-constraint approximation" or keep separate.

#### `/tmp/ncrit_curvature.py` — Flat-constraint perturbative model
Derives `N_crit(K) ≈ 7 − (7/9)KR²` from the leading-order K correction with flat
constraint. This formula is **not** the H² result — it's an approximation valid for the
flat-constraint + curved Green's function model. Should go in a `perturbative/` section
or notebook, labeled clearly.

#### `/tmp/ncrit_fixed.py` — Bug-fixed flat-plane eigenvalue
Corrects a bug where the Hessian summed only over pairs involving vortex 0 instead of all
N(N-1)/2 pairs. This is now superseded by the H² scripts. May be useful as a standalone
flat-plane test utility.

### 2.2 Gamma Coefficient Script

#### `/tmp/gamma_coeff.py`
Attempted numerical extraction of γ via large-a limit of `a⁴ · λ₃(N=7)`. The numerical
approach fails due to catastrophic cancellation (H_hyp and Ω·J are each O(a²), their
difference is O(1/a⁴) — below double-precision range at large a).

The script confirms this numerically and pivots to the analytical result. Key output:
```python
xi_star = 8 - 3*np.sqrt(7)   # = 0.06274606...
gamma = 127 + 48*np.sqrt(7)  # exact
# Verify: (8-3*sqrt(7))**2 * (127+48*sqrt(7)) == 1  ✓
```
**Target:** The analytical result belongs in `h2_stability.py`. The catastrophic-cancellation
note is worth a comment. The script itself is documentation, not production code.

### 2.3 Reviewer Verification Scripts (polygon_reviewer_scratch)

These were written to address specific reviewer comments. Each is standalone.

#### `/tmp/polygon_reviewer_scratch/verify_quartic_n7.py` — N=7 quartic per-pair
Shows all 21 pairs in the quartic sum explicitly. Verifies `d⁴H/dt⁴ = 153/7` for radial
m=3, tangential m=3, and mixed modes. Verifies Z_7 symmetry. Also has a constraint
correction via polynomial fit (less precise than v2/v3).

**Target:** `notebooks/verify_n7_quartic.ipynb` or extend `n7_bifurcation.py` with the
per-pair table output.

#### `/tmp/polygon_reviewer_scratch/verify_quartic_n7_v2.py` — High-precision, mpmath
Uses `mpmath` at 50 decimal places. Has the correct 2D neutral subspace identification
(`{radial cos m=3, radial sin m=3}` — NOT `{radial, tangential}`). Newton projection via
`H_constrained_mp`. Richardson extrapolation. Best numerical result:
```
Constrained quartic  ≈ 19.27–19.29  (Richardson)
Correction Δ         ≈ 2.57–2.58
α₀ = quartic/6       ≈ 3.21
```
**Note:** The existing `n7_bifurcation.py` docstring says `≈ 19.28–19.29`. The v2/v3 scripts
confirm this range.

**Target:** The Richardson extrapolation method and the correct neutral subspace identification
(radial, not tangential) should update the docstring and `constrained_quartic_n7()` function
in `n7_bifurcation.py`.

#### `/tmp/polygon_reviewer_scratch/verify_quartic_n7_v3.py` — Log-ratio method
Avoids catastrophic cancellation by computing `dH(h) = H_constrained(h) − H(0)` as a sum
of log-ratios. Clean Richardson extrapolation. Same results as v2 but more numerically
stable. Does NOT require mpmath.

**Target:** Replace or supplement `constrained_quartic_n7()` in `n7_bifurcation.py` with
the log-ratio approach. This is the most production-worthy version.

#### `/tmp/polygon_reviewer_scratch/onsager_n_selection.py` — Onsager N-selection theorem
New result not yet in the repo. Proves `H(N+1) − H(N) > 0` for `κ₀/κ ≥ 1/2` and `R > 1`
(in core-radius units). Analytic formula:
```
H(N+1) − H(N) = Γ² · [(2r−1)/(2N(N+1)) · ln R + (ln N/N − ln(N+1)/(N+1))/2]
```
Both terms are non-negative for `r ≥ 1/2`, `R > 1`. Applied to Jupiter (r ≈ 0.7, R ≈ 10.7):
confirms N=8 selection. This is a **complete standalone theorem**.

**Target:** New file `src/planetary_polygons/extensions/onsager_selection.py`

#### `/tmp/polygon_reviewer_scratch/injection_restoring_ratio.py` — Jupiter timescales
Computes injection-to-restoring timescale ratio for Jupiter's N=8 polar cyclone ring using
Juno (Adriani 2018) parameters. Result: τ_inject/τ_restore ≫ 1, supporting dynamical
maintenance. Addresses a reviewer question about whether the ring can be sustained.

Key numbers:
```
Orbital period T_orb  ≈ 65 days
Restoring τ (λ_eff=3) ≈ 37 days
Injection τ (tropo)   ≈ 7800 days
Ratio                 ≈ 210
```

**Target:** `src/planetary_polygons/verification/jupiter.py` (extend existing file) or
`notebooks/jupiter_timescales.ipynb`

---

## 3. Repo Files Requiring Updates

### 3.1 CRITICAL: `src/planetary_polygons/extensions/curved_surfaces.py`

**Problem:** `hyperbolic_ncrit(N, R_over_a, a)` uses a hardcoded heuristic calibration:
```python
C_geom = 7.0 / (12.0 * 11.0)
curvature_correction = N * (N - 1) * C_geom * R_over_a**2
```
This is a fudge factor ("calibrated so that N=12 is marginally stable at R=a"). It has no
physical derivation and will give wrong N_crit for other values of R/a.

**Fix:** Replace with the exact C₁ formula:
```python
def hyperbolic_ncrit_exact(N, R_over_a, a=1.0):
    """
    Exact N-ring stability on H² using the closed-form C₁ formula.

    C₁(H², ξ) = (N-1)(1+ξ²)/(1-ξ)²  where ξ = r_E²/a²
    r_E = a * tanh(ρ/(2a)), ρ = R_over_a * a (geodesic ring radius)

    λ_m * r_E² = C₁(H², ξ) - m(N-m)/2
    Ring stable iff min over m=1..N//2 of λ_m ≥ 0.
    """
    rho = R_over_a * a
    r_E = a * np.tanh(rho / (2 * a))
    xi = (r_E / a) ** 2
    C1 = (N - 1) * (1 + xi**2) / (1 - xi)**2
    lam_min = min(C1 - m*(N-m)/2 for m in range(1, N//2 + 1)) / r_E**2
    return lam_min
```

**Also add** the N=8 exact threshold:
```python
XI_STAR_78 = 8 - 3 * np.sqrt(7)   # exact 7→8 threshold, ξ = r_E²/a²
GAMMA_78 = 127 + 48 * np.sqrt(7)  # = 1/ξ*², exact
```

### 3.2 IMPORTANT: `src/planetary_polygons/extensions/riemannian_havelock.py`

**Problems:**
1. The module docstring describes `C₁ = λ_m + m(N-m)/2` as the Riemannian Havelock identity.
   This is dimensionally inconsistent — the correct form is `λ_m · r_E² + m(N-m)/2 = C₁`.
2. No `C₁` function for H² (or sphere) is provided.
3. `trace_formula_delta` gives sphere/torus corrections but not the H² formula.

**Fix — add these functions:**
```python
def C1_hyperbolic(N, xi):
    """
    Exact C₁ coefficient for N-vortex ring on H².
    C₁(H², ξ) = (N-1)(1+ξ²)/(1-ξ)²
    ξ = r_E²/a², where r_E is Euclidean ring radius, a is curvature radius.
    """
    return (N - 1) * (1 + xi**2) / (1 - xi)**2

def C1_sphere(N, xi):
    """
    Exact C₁ coefficient for N-vortex ring on S².
    C₁(S², ξ) = (N-1)(1-ξ)/(1+ξ)
    ξ = KR² = R²/a², where R is Euclidean ring radius, a is sphere radius.
    """
    return (N - 1) * (1 - xi) / (1 + xi)

def riemannian_havelock_eigenvalue(N, m, xi, surface='hyperbolic', r_E=1.0):
    """
    Lagrangian eigenvalue from Riemannian Havelock identity.
    λ_m = [C₁(surface, ξ) - m(N-m)/2] / r_E²
    """
    if surface == 'hyperbolic':
        C1 = C1_hyperbolic(N, xi)
    elif surface == 'sphere':
        C1 = C1_sphere(N, xi)
    else:
        raise ValueError(f"Unknown surface: {surface!r}")
    return (C1 - m * (N - m) / 2) / r_E**2
```

**Update module docstring** to state the correct Riemannian Havelock form.

### 3.3 MEDIUM: `src/planetary_polygons/extensions/n7_bifurcation.py`

**Problems:**
1. The docstring says the neutral subspace modes are angular (tangential). They are RADIAL.
   From `verify_quartic_n7_v2.py`: "Correct 2D neutral subspace: {cos-radial m=3, sin-radial
   m=3} — NOT {radial, tangential} (tangential m=3 has eigenvalue +6, not 0)."
2. The constrained quartic value ≈19.28 is correct but the method used should be
   documented (Newton projection with log-ratio delta-H, not polynomial fit).
3. The correction Δ ≈ 2.58 should be stated explicitly (paper says "≈2.39" in one place —
   needs reconciliation).

**Fix:**
- Update docstring on neutral subspace
- Verify `constrained_quartic_n7()` uses the log-ratio approach from v3 (or Richardson)
- Reconcile the Δ value between paper and code

### 3.4 LOW: `tests/test_curved_surfaces.py`

The current test file presumably checks `hyperbolic_ncrit` with the heuristic formula.
After 3.1 is fixed, tests need to cover:
- `hyperbolic_ncrit_exact(N=7, R_over_a=0.5)` ≥ 0 (stable)
- `hyperbolic_ncrit_exact(N=8, R_over_a=0.52)` ≥ 0 (just stable — near threshold)
- `hyperbolic_ncrit_exact(N=8, R_over_a=0.1)` < 0 (unstable at small ρ/a)
- `hyperbolic_ncrit_exact(N=12, R_over_a=1.0)` ≥ 0 (stable at R/a=1)
- `hyperbolic_ncrit_exact(N=13, R_over_a=1.0)` < 0 (unstable at R/a=1)

### 3.5 LOW: `tests/test_riemannian_havelock.py`

Add tests for new C₁ functions:
```python
def test_C1_flat_limit():
    # C₁(H², ξ→0) → N-1 (flat-plane limit)
    assert abs(C1_hyperbolic(7, 1e-6) - 6) < 1e-5

def test_C1_threshold_N8():
    # C₁(H², ξ*) = 8 (defines 7→8 threshold)
    xi_star = 8 - 3*np.sqrt(7)
    assert abs(C1_hyperbolic(8, xi_star) - 8) < 1e-10
```

---

## 4. New Files to Create

### 4.1 `src/planetary_polygons/extensions/h2_stability.py` (NEW)

Complete module for H² vortex stability. Should contain:

```python
"""
Point vortex ring stability on the hyperbolic plane H². (§5.x)

Exact computation using the Poincaré disk model:
  H_hyp = -Σ_{j<k} ln|z_j - z_k| + (N-1)/2 · Σ_k ln(a² - |z_k|²)
  J_hyp = Σ_k (a² + |z_k|²)/(a² - |z_k|²)   [SO(2,1) moment map]

Equilibrium: N-vortex ring at Euclidean radius r_E = a·tanh(ρ/(2a))
  Ω = [−(N−1)/(2r_E) − (N−1)r_E/(a²−r_E²)] / [4a²r_E/(a²−r_E²)²]

Riemannian Havelock identity (EXACT):
  λ_m · r_E² = C₁(H², ξ) − m(N−m)/2
  C₁(H², ξ) = (N−1)(1+ξ²)/(1−ξ)²,   ξ = r_E²/a²

7→8 transition threshold (EXACT):
  ξ* = 8 − 3√7 ≈ 0.0627
  γ = 1/ξ*² = 127 + 48√7 ≈ 254
"""
```

Functions to include (copy from `/tmp/ncrit_h2_sweep.py`):
- `H_hyp(z_re, z_im, a)`
- `J_hyp(z_re, z_im, a)`
- `get_Omega(N, r_E, a)`
- `fourier_eigenvalue(m, N, rho, a, h_fd=1e-5)` — FD Hessian approach
- `min_eigenvalue(N, rho, a)` — min over m
- `ncrit_h2(rho, a, N_max=24)` — find N_crit numerically
- `C1_h2_exact(N, xi)` — exact formula
- `ncrit_h2_exact(rho, a, N_max=24)` — from exact C₁ formula (fast, no FD)
- `threshold_78_exact()` — returns (xi_star, gamma)
- `ncrit_h2_table(rho_vals, a=1.0)` — tabulate the N_crit table

Constants:
```python
XI_STAR_78 = 8 - 3 * np.sqrt(7)
GAMMA_78 = 127 + 48 * np.sqrt(7)
```

### 4.2 `src/planetary_polygons/extensions/onsager_selection.py` (NEW)

Onsager N-selection theorem. Copy from `/tmp/polygon_reviewer_scratch/onsager_n_selection.py`.

```python
"""
Onsager N-selection: H(N+1) > H(N) for kappa_0/kappa >= 1/2. (§4.x)
"""
def H_N(N, R, r, Gamma=1.0):
    """Thomson ring + central vortex Hamiltonian."""
    ...

def H_diff(N, R, r, Gamma=1.0):
    """H(N+1) - H(N) analytic formula."""
    ...

def verify_monotonicity(r_min=0.5, r_max=1.5, N_max=12, R_min=1.01, R_max=1000):
    """Returns True if H is monotone increasing in N for all r >= r_min."""
    ...
```

### 4.3 `notebooks/verify_n7_quartic.ipynb` (NEW)

Convert `/tmp/polygon_reviewer_scratch/verify_quartic_n7_v3.py` to a notebook showing:
1. All 21 pairs in the quartic sum
2. Z_7 symmetry check (cos, sin, mix all give 153/7)
3. Constraint correction via log-ratio delta-H method
4. Richardson extrapolation → constrained quartic ≈ 19.29

### 4.4 `notebooks/hyperbolic_stability.ipynb` (NEW)

Visualization notebook for the H² N_crit results:
1. N_crit table vs ρ/a
2. C₁(H², ξ) curve with the threshold ξ* marked
3. Eigenvalue λ₃(N=7) and λ₄(N=8) as functions of ξ
4. Comparison with sphere result

---

## 5. LaTeX Paper Changes (Already Applied)

These changes are already in `latex/paper/main.tex` as of this session.

### 5.1 Added: Exact C₁ Formula (new equation `\eqref{eq:C1_H2}`)

**Location:** Lines ~963–972 (after "The Riemannian Havelock identity...")

```latex
\begin{equation}
  C_1(\mathbf{H}^2,\,\xi)
    = \frac{(N-1)(1+\xi^2)}{(1-\xi)^2},
  \qquad \xi = \frac{r_E^2}{a^2} = |K|\,r_E^2 ,
  \label{eq:C1_H2}
\end{equation}
```

### 5.2 Replaced: "Near-K=0 behavior" paragraph (lines ~984–1019)

**Old content:** Incorrectly stated "first-order shift δλ_m = 0 at O(K)" and attributed it
to a cancellation. Also stated `N_crit(K) = 7 + O(K²R⁴)`.

**New content:**
- States `λ₃(N=7) = 12|K|/(1−ξ)²` — stabilized at first order (new `\eqref{eq:lam3_H2}`)
- Derives exact threshold `ξ* = 8−3√7` from `ξ²−16ξ+1=0` (new `\eqref{eq:xi_star}`)
- States `γ = 127+48√7` with algebraic verification (new `\eqref{eq:gamma}`)

**Equation labels introduced:** `eq:C1_H2`, `eq:lam3_H2`, `eq:xi_star`, `eq:gamma`

---

## 6. Outstanding Issues / Caveats for Agent

### 6.1 Wrong docstring in `curved_surfaces.py`

The module docstring says:
```
H² Green's function: G(d) = -(1/2pi) ln(tanh(d/(2a)))
```
The actual Green's function used in the session scripts is:
```
H_hyp = -Σ_{j<k} ln|z_j-z_k| + (N-1)/2 · Σ_k ln(a²-|z_k|²)
```
which comes from `h(d) = −ln sinh(d/(2a))` (not `tanh`). The `tanh` form is a different
normalization convention that appears in some references. Verify which convention the paper
uses and make the module consistent.

### 6.2 Quartic Δ value discrepancy

Different scripts report slightly different values for the constraint correction Δ:
- `verify_quartic_n7_v3.py` (log-ratio): Δ ≈ 2.57–2.58
- `verify_quartic_n7_v2.py` (mpmath): Δ ≈ 2.57–2.58
- `n7_bifurcation.py` docstring: "correction Δ ≈ 2.58"
- Paper currently says "Δ ≈ 2.39" in one place

The best estimates are from v2/v3 scripts (high-precision Richardson): **Δ ≈ 2.57–2.58**.
The "2.39" in the paper appears to be a stale value from an earlier computation and should
be updated.

### 6.3 The flat-constraint model vs full H² model

`/tmp/ncrit_curvature.py` and `/tmp/ncrit_exact.py` implement a different physics model:
they use the flat-plane angular impulse constraint `L = Σ|z_k|²` with a curved Green's
function, rather than the full H² dynamics with the H² moment map `J = Σ(a²+r²)/(a²-r²)`.
These give different N_crit values and should not be conflated. The paper uses the full H²
model. The flat-constraint model is only a perturbative approximation valid for |K|R² << 1.

### 6.4 N_crit computation method

The exact C₁ formula gives N_crit analytically (much faster than FD Hessian). The FD
approach in `ncrit_h2_sweep.py` is the gold standard for verification, but the production
code should use `C1_h2_exact` for speed. Both should be in the new module.

---

## 7. Quick Reference: Files to Copy

| Source (temp) | Destination (repo) | Action |
|---|---|---|
| `/tmp/ncrit_h2_sweep.py` | `src/.../extensions/h2_stability.py` | New module (clean up) |
| `/tmp/gamma_coeff.py` | Constants in `h2_stability.py` | Extract ξ*, γ |
| `/tmp/polygon_reviewer_scratch/verify_quartic_n7_v3.py` | `notebooks/verify_n7_quartic.ipynb` | Convert to notebook |
| `/tmp/polygon_reviewer_scratch/verify_quartic_n7_v2.py` | Reference for `n7_bifurcation.py` updates | Extract neutral subspace fix |
| `/tmp/polygon_reviewer_scratch/onsager_n_selection.py` | `src/.../extensions/onsager_selection.py` | New module |
| `/tmp/polygon_reviewer_scratch/injection_restoring_ratio.py` | `src/.../verification/jupiter.py` | Extend existing |

## 8. Files NOT to Use

| File | Reason |
|---|---|
| `/tmp/ncrit_h2_v2.py` | Wrong Omega sign (pre-fix) |
| `/tmp/ncrit_h2_clean.py` | Wrong Omega sign (pre-fix) |
| `/tmp/ncrit_fixed.py` | Flat-plane only, superseded |
| `/tmp/polygon_reviewer_scratch/verify_quartic_n7.py` | Superseded by v2/v3 |

---

*End of catalog. All temp files at `/tmp/ncrit_*.py` and `/tmp/polygon_reviewer_scratch/*.py`.*
