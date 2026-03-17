# Public Repo Readiness — Design Spec
**Date:** 2026-03-17
**Repo:** `planetary-polygons-unified`
**Goal:** All tests green, all paper computations executable, one notebook per paper section, ready for fine-tooth-comb public scrutiny.

---

## Approach

Layer-by-layer (Option B):
1. Fix environment and make all existing tests pass
2. Reorganize source into subpackages matching paper structure
3. Add missing source modules (one per paper section gap)
4. Add supplementary scripts for Proposition 4 and Proposition 8
5. Add notebooks (one per paper section, regenerating all figures)

---

## Layer 1: Environment

- Migrate to `uv` with `uv sync`
- Update `pyproject.toml`:
  - Add `uv` as build backend
  - Add missing declared dependencies: `matplotlib>=3.8`, `jupyter>=1.0`, `sympy>=1.12`, `ipykernel>=6`
  - Current declared: `numpy>=1.26`, `scipy>=1.11` — keep these
  - Dev extras: `pytest>=7.4`, `nbmake` (notebook testing)
- Add `uv.lock` to repo
- Verify: `uv sync && uv run pytest tests/ -q` → all 109 tests green

---

## Layer 2: Source Package Reorganization

Rename flat `src/*.py` into `src/planetary_polygons/` with subpackages matching paper sections:

```
src/planetary_polygons/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── hessian.py           ← constrained_hessian.py
│   ├── sign_rule.py         ← sign_rule_proof.py
│   ├── thomson.py           ← thomson.py
│   ├── variational.py       ← variational.py
│   └── rossby.py            ← rossby.py + qgpv.py (merged)
├── data/
│   ├── __init__.py
│   ├── saturn.py            ← saturn_data.py + cassini_winds.py (merged)
│   └── jupiter.py           ← jupiter_data.py
├── verification/
│   ├── __init__.py
│   ├── saturn.py            ← saturn_verification.py
│   ├── jupiter.py           ← jupiter_verification.py
│   └── sigma_geometric.py   ← sigma_geometric.py
├── extensions/
│   ├── __init__.py
│   ├── curved_surfaces.py   ← NEW (§6.1)
│   ├── deformation_radius.py← NEW (§6.2)
│   ├── n7_bifurcation.py    ← NEW (§6.3)
│   ├── blob_correction.py   ← NEW (§6.4); absorbs blob logic from matching.py
│   ├── multiring.py         ← NEW (§6.5); absorbs n8_instability.py logic
│   ├── bec_vortices.py      ← NEW (§6.6)
│   ├── bridge.py            ← NEW (§6.7); absorbs matching.py + jupiter_verification.py
│   └── riemannian_havelock.py ← NEW (§6.8)
└── viz/
    ├── __init__.py
    └── figures.py           ← all figure generation (currently scattered)
```

Update `pyproject.toml` `pythonpath` to `["src"]` (Python finds `planetary_polygons` as a package).
Update all test imports from `from constrained_hessian import ...` to `from planetary_polygons.core.hessian import ...`.
All 109 existing tests must still pass after this step.

---

## Layer 3: New Source Modules

Each module exposes clean public functions, returns structured results (dataclasses or dicts), no side effects at import, `if __name__ == "__main__"` demo block.

### `extensions/n7_bifurcation.py` (§6.3)
Key functions:
- `unconstrained_quartic(N, mode_m)` → exact float using pair formula `6C²/A² - 12B²C/A³ + 3B⁴/A⁴`
- `quartic_exact_n7()` → returns `Fraction(153, 7)`
- `constrained_quartic_n7()` → Newton-projected constraint surface, returns ≈19.47
- `constraint_correction_n7()` → ≈2.39
- `alpha_0_n7()` → constrained_quartic/6 ≈ 3.24

Paper numbers: 153/7, α₀ ≈ 3.2, correction ≈ 2.39

### `extensions/blob_correction.py` (§6.4)
Key functions:
- `compute_Pm(N)` → exact rational using Cauchy-blob pair formula
- `blob_correction_table(N_range=range(3,9))` → dict with `shift`, `Pm`, `cm` for each N
- `stabilization_threshold(N)` → ε > 1/√cm

Paper numbers: P₃=−1/3, P₄=1/4, P₅=1, P₆=4, P₇=8, P₈=65/4; cm=−1 for N≤5

### `extensions/curved_surfaces.py` (§6.1)
Key functions:
- `sphere_constrained_eigenvalues(N, colatitude_deg)` → array of eigenvalues
- `ncrit_sphere(colatitude_deg)` → largest stable N at given colatitude
- `phi_crit_table(N_range=range(3,9))` → colatitude boundary for each N
- `hyperbolic_ncrit(N, R_over_a)` → stability on hyperbolic plane
- `ncrit_vs_curvature_table()` → reproduces paper table

Paper numbers: N_crit=12 at R/a=1, N_crit≥14 at R/a=2, 7→8 transition at R/a≈0.5

### `extensions/deformation_radius.py` (§6.2)
Key functions:
- `K0_eigenvalue(N, m, R_over_Rd)` → eigenvalue with finite deformation radius
- `suppression_transition(N=6)` → R/R_d value where K₀ reduces N_crit below N
- `K0_correction_table()` → eigenvalue shifts vs R/R_d for N=6,7,8

Paper number: suppression transition at R/R_d ≈ 1.29 for N=6

### `extensions/bec_vortices.py` (§6.6)
Key functions:
- `bec_kappa_crit(N)` → maps from point-vortex κ_crit formula to BEC quantized winding numbers
- `bec_stability_table()` → N=5..9 predictions with quantized q₀
- `bec_frequency_shift(N, q0)` → frequency shift prediction

Paper number: N=8 stabilized by q₀=1 > κ_crit=1/2

### `extensions/bridge.py` (§6.7)
Key functions:
- `blob_convergence_rate(N, eps_values)` → eigenvalue vs ε, fits O(ε²) rate
- `profile_independence_check(N)` → compare Cauchy vs Gaussian vs compact blobs
- `rossby_bridge_estimate(saturn_params)` → cat's-eye concentration estimate

Paper numbers: O(ε²) convergence, analytic correction coefficients

### `extensions/riemannian_havelock.py` (§6.8)
Key functions:
- `havelock_sum(N, m)` → T_m numerically, verify = m(N−m)/2
- `trace_formula_delta(N, surface='sphere', **kwargs)` → δ = −N/Vol(M)
- `fourier_block_trace(N, m, green_function)` → H_rr^(m) + H_tt^(m) from first principles
- `mobius_energy_transform(positions, f_mobius)` → verify covariance formula
- `equations_of_motion_invariant_check(N, f_mobius)` → verify ∂H/∂z_j unchanged

Paper numbers: T_m = m(N−m)/2 exact, δ = −N/(4πR²) on sphere

---

## Layer 4: Supplementary Scripts

### `scripts/prop4_characteristic_polynomial.py`
Standalone. Uses `sympy`. Computes:
1. Symbolic characteristic polynomial of constrained Hessian for N=6 with central vortex strength κ₀ (symbolic)
2. Factors the polynomial in κ₀/κ
3. Solves for κ_crit = −1/4 as exact symbolic root
4. Numerical verification: eigenvalue sign at κ₀/κ = −1/4 ± ε
5. Prints characteristic polynomial and stability boundary in LaTeX-ready format

### `scripts/prop_inertia_verification.py`
Standalone. Verifies three functional-analytic claims of Proposition 8:

**(a) Center eigenvalue convergence:** For N=3..7, compute full blob Hessian eigenvalues at ε = 0.1, 0.05, 0.01, 0.005. Fit convergence rate to O(εᵅ). Print table: Havelock limit, observed rate α, PASS if α ≥ 1.8.

**(b) Shape-sector lower bound:** For Gaussian blob at each ε, find smallest shape-sector eigenvalue. Confirm scales as c/ε². Print ratio (observed eigenvalue × ε²) — should be constant. PASS if variation < 5%.

**(c) Center-shape coupling:** Measure off-diagonal coupling block magnitude at each ε. Fit to A·ε⁻¹·exp(−d_min/ε). Print exponential fit quality. PASS if residual < 1%.

Final: verify full-blob inertia = point-vortex inertia at each ε. PASS/FAIL per N.

---

## Layer 5: Notebooks

One notebook per paper section. Each:
- Imports from `planetary_polygons.*`
- Runs top-to-bottom in < 2 minutes
- Final cell prints all paper-cited numbers with PASS/FAIL
- Regenerates the section's figures into `figures/`

```
notebooks/
├── 01_energy_curvature.ipynb          # §3.1 — Theorem 1
├── 02_sign_rule.ipynb                  # §3.2 — Theorem 2
├── 03_constrained_minimum.ipynb        # §3.3 — Theorem 3
├── 04_central_vortex.ipynb             # §3.4 — Prop 4, char. polynomial
├── 05_planetary_verification.ipynb     # §4   — σ_geom, Saturn/Jupiter
├── 06_curved_surfaces.ipynb            # §6.1 — sphere/hyperbolic
├── 07_deformation_radius.ipynb         # §6.2 — K₀
├── 08_n7_bifurcation.ipynb             # §6.3 — 153/7, α₀
├── 09_blob_correction.ipynb            # §6.4 — P_m table
├── 10_multiring.ipynb                  # §6.5 — two-ring
├── 11_bec_vortices.ipynb               # §6.6 — BEC
├── 12_bridge.ipynb                     # §6.7 — bridges
└── 13_riemannian_havelock.ipynb        # §6.8 — Havelock, trace, Möbius
```

---

## Test Coverage

All new modules in `extensions/` get corresponding test files in `tests/`:

```
tests/
├── test_n7_bifurcation.py      # quartic=153/7, α₀≈3.24, correction≈2.39
├── test_blob_correction.py     # full P_m table exact values
├── test_curved_surfaces.py     # sphere eigenvalues, hyperbolic N_crit
├── test_deformation_radius.py  # K₀ transition at R/Rd≈1.29
├── test_bec_vortices.py        # κ_crit mapping, N=8 prediction
├── test_bridge.py              # O(ε²) convergence rate
└── test_riemannian_havelock.py # T_m identity, δ formula, Möbius invariance
```

Target: ≥ 150 total tests passing.

---

## Success Criteria

- [ ] `uv sync` installs all dependencies from lockfile
- [ ] `uv run pytest tests/ -q` → all tests green, 0 failures
- [ ] Every number cited in the paper has a corresponding test asserting it to stated precision
- [ ] `jupyter nbconvert --to notebook --execute notebooks/*.ipynb` runs all notebooks without error
- [ ] Each notebook regenerates the figures for its section
- [ ] `python scripts/prop4_characteristic_polynomial.py` prints κ_crit = −1/4 symbolically
- [ ] `python scripts/prop_inertia_verification.py` prints PASS for all three claims A/B/C
