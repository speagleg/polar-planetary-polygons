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
  - Fix build backend from private `setuptools.backends._legacy:_Backend` to public `setuptools.build_meta`
  - Add missing declared dependencies: `matplotlib>=3.8`, `jupyter>=1.0`, `sympy>=1.12`, `ipykernel>=6`
  - Current declared: `numpy>=1.26`, `scipy>=1.11` — keep these
  - Dev extras: `pytest>=7.4`, `nbmake>=1.5` (notebook testing via `pytest --nbmake`)
- Run `uv lock` to generate `uv.lock`; add both to repo
- Canonical notebook test command: `uv run pytest --nbmake notebooks/` (not nbconvert)
- Verify: `uv sync && uv run pytest tests/ -q` → all 109 tests green

---

## Layer 2: Source Package Reorganization

Rename flat `src/*.py` into `src/planetary_polygons/` with subpackages matching paper sections.

**Complete file mapping (every existing file accounted for):**

```
src/planetary_polygons/
├── __init__.py
├── core/                              # §1–5: setup and main results
│   ├── __init__.py
│   ├── hessian.py           ← constrained_hessian.py
│   ├── sign_rule.py         ← sign_rule_proof.py
│   ├── thomson.py           ← thomson.py
│   ├── variational.py       ← variational.py
│   ├── rossby.py            ← rossby.py + qgpv.py (merged; qgpv functions become
│   │                           rossby.py submodule — no public API change)
│   ├── logarithmic_specialness.py  ← theorem4_reformulated.py
│   │                           (contains complementary_selection_table,
│   │                            logarithmic_specialness, galerkin_test_summary)
│   └── amplitude.py         ← matching.py (Saturn amplitude formula:
│                               hexagon_amplitude_analytic, matching_constant,
│                               MatchedAsymptoticSolver — stays in core, NOT bridge)
├── data/
│   ├── __init__.py
│   ├── saturn.py            ← saturn_data.py + cassini_winds.py (merged)
│   └── jupiter.py           ← jupiter_data.py
├── verification/
│   ├── __init__.py
│   ├── saturn.py            ← saturn_verification.py
│   │                           (imports core.amplitude for verify_theorem5_amplitude;
│   │                            imports core.amplitude.LoxodromicFlow — classmethod
│   │                            from_velocity_ratio must be implemented in Layer 3)
│   ├── jupiter.py           ← jupiter_verification.py
│   │                           (single-ring N=8 analysis; does NOT move to multiring)
│   └── sigma_geometric.py   ← sigma_geometric.py
├── extensions/
│   ├── __init__.py
│   ├── curved_surfaces.py   ← NEW (§6.1)
│   ├── deformation_radius.py← NEW (§6.2)
│   ├── n7_bifurcation.py    ← NEW (§6.3)
│   ├── blob_correction.py   ← NEW (§6.4); blob logic from core/amplitude.py extracted here
│   ├── multiring.py         ← NEW (§6.5); n8_instability.py single-ring functions
│   │                           (jupiter_north_analysis, jupiter_south_analysis,
│   │                            stability_diagram, constrained_energy_landscape_slice)
│   │                           MOVE HERE — verification/jupiter.py imports from here
│   ├── bec_vortices.py      ← NEW (§6.6)
│   ├── bridge.py            ← NEW (§6.7); blob convergence + Rossby bridge only
│   │                           (does NOT absorb matching.py amplitude functions)
│   └── riemannian_havelock.py ← NEW (§6.8)
└── viz/
    ├── __init__.py
    └── figures.py           ← figure generation (see Layer 3 for API)
```

**Key import chain fixes required in this layer:**
- `saturn_verification.py` calls `LoxodromicFlow.from_velocity_ratio(...)` — this classmethod must be stubbed in `core/amplitude.py` (raises `NotImplementedError`) so imports don't break; full implementation deferred to Layer 3
- `jupiter_verification.py` imports from `n8_instability` — update to `from planetary_polygons.extensions.multiring import ...`
- All test imports updated to new paths; all 109 tests must pass after this layer

---

## Layer 3: New Source Modules and Missing Implementations

Each module: clean public functions, structured return types (dataclasses or dicts), no import-time side effects, `if __name__ == "__main__"` demo block.

### `core/amplitude.py` — complete `LoxodromicFlow.from_velocity_ratio`
This classmethod was missing (build-breaking for `saturn_verification.py`):
```python
@classmethod
def from_velocity_ratio(cls, ratio: float, U_max: float, A: complex = 1.0) -> 'LoxodromicFlow':
    """Construct from radial/total velocity ratio at jet boundary.
    sigma ≈ ratio - 1 for ratio near 1 (Theorem 3 identification)."""
    sigma = ratio - 1.0
    alpha = np.pi / 3  # n=6 hexagonal mode
    return cls(A=A, s=complex(sigma, alpha))
```

### `extensions/n7_bifurcation.py` (§6.3)
Key functions:
- `unconstrained_quartic(N, mode_m)` → exact float using pair formula `6C²/A² - 12B²C/A³ + 3B⁴/A⁴`
  where `A = |w|²`, `B = 2Re(w·conj(v))`, `C = |v|²` for each pair (j,k)
- `quartic_exact_n7()` → returns `Fraction(153, 7)`
- `constrained_quartic_n7(h=5e-4)` → Newton-projected constraint surface, returns ≈19.47
- `constraint_correction_n7()` → ≈2.39
- `alpha_0_n7()` → constrained_quartic/6 ≈ 3.24

Paper numbers: 153/7, α₀ ≈ 3.2, correction ≈ 2.39

### `extensions/blob_correction.py` (§6.4)

The Cauchy blob is `h_ε(d) = -½ ln(d² + 2ε²)`. Taylor expanding:
`h_ε = -ln d - ε²/d² + O(ε⁴)`.
The O(ε²) correction to the pair (j,k) Hessian diagonal is
`δH_xx^(j,k) = (2ε²/d⁶)(d_y² - 3d_x²)` and similarly for other components.
`P_m` is the projection of this correction onto the critical radial Fourier eigenvector.

Key functions:
- `blob_pair_hessian_correction(z_j, z_k, u_j, u_k)` → O(ε²)/ε² coefficient for one pair
- `compute_Pm(N)` → P_m by summing over all N(N-1)/2 pairs, projected onto critical mode
- `blob_correction_table(N_range=range(3,9))` → dict with `shift=-(N²-1)/12`, `Pm`, `cm=shift+Pm`
- `stabilization_threshold(N)` → ε > 1/√cm (only meaningful for cm > 0, i.e. N≥6)

Paper numbers: P₃=−1/3, P₄=1/4, P₅=1, P₆=4, P₇=8, P₈=65/4; cm=−1 for N≤5

### `extensions/curved_surfaces.py` (§6.1)

**Green's function on the sphere:** `G(γ) = -(1/4π) ln(2 - 2cosγ)` where γ is the geodesic angle.
This differs from the flat `G(r) = -ln r` by terms proportional to `1/R²`.
**Source of paper numbers:** These were computed numerically by evaluating the constrained
Hessian eigenvalues using the spherical Green's function at each colatitude. The hyperbolic
numbers (N_crit=12 at R/a=1) are also purely numerical. Both are HIGH-RISK: implement
numerically first, flag as "computed" in the paper if they can't be analytically derived.

Key functions:
- `spherical_pair_interaction(gamma, R)` → h(γ) using spherical Green's function
- `sphere_constrained_eigenvalues(N, colatitude_deg, R=1.0)` → array of constrained Hessian eigenvalues
- `ncrit_sphere(colatitude_deg)` → largest stable N at given colatitude
- `phi_crit_table(N_range=range(3,9))` → critical colatitude for each N
- `hyperbolic_pair_interaction(d, a)` → h(d) using hyperbolic Green's function `G = -(1/2π)ln(tanh(d/2a))`
- `hyperbolic_ncrit(N, R_over_a)` → N_crit on hyperbolic plane
- `ncrit_vs_curvature_summary()` → reproduces paper table (computed, not analytic)

Paper numbers (numerically computed): N_crit=12 at R/a=1, N_crit≥14 at R/a=2, 7→8 at R/a≈0.5

### `extensions/deformation_radius.py` (§6.2)
Key functions:
- `K0_modified_interaction(d, Rd)` → modified Bessel `K₀(d/Rd)` interaction
- `K0_eigenvalue(N, m, R_over_Rd)` → constrained Hessian eigenvalue with K₀ interaction
- `suppression_transition(N=6)` → R/R_d where eigenvalue crosses zero
- `K0_correction_table()` → eigenvalue vs R/R_d for N=6,7,8

Paper number: suppression transition at R/R_d ≈ 1.29 for N=6

### `extensions/bec_vortices.py` (§6.6)
Key functions:
- `bec_kappa_crit(N)` → κ_crit mapped to BEC quantized winding number q₀ = round(κ_crit * κ / κ_single)
- `bec_stability_table(N_range=range(5,10))` → for each N: κ_crit, minimum integer q₀, stable?
- `bec_frequency_shift(N, q0, omega_rot)` → precession frequency shift from central vortex

Paper number: N=8 stabilized by q₀=1 > κ_crit=1/2

### `extensions/bridge.py` (§6.7)
Key functions:
- `blob_convergence_rate(N, eps_values)` → dict of eigenvalue vs ε, convergence rate fit
- `profile_independence_check(N, profiles=['cauchy','gaussian','compact'])` → correction coefficient per profile
- `rossby_bridge_estimate(saturn_params)` → cat's-eye half-width / jet width ratio

Paper numbers: O(ε²) convergence, correction coefficients from blob_correction table

### `extensions/riemannian_havelock.py` (§6.8)
Key functions:
- `havelock_sum(N, m)` → T_m numerically (should equal m(N−m)/2 to machine precision)
- `havelock_exact(N, m)` → returns `Fraction(m*(N-m), 2)`
- `trace_formula_delta(N, surface='sphere', R=1.0)` → δ = −N/Vol(M) for given surface
- `fourier_block_trace(N, m, h_func)` → H_rr^(m) + H_tt^(m) from Fourier block construction
- `mobius_energy_transform(positions, a, b, c, d)` → verify H maps to H + Σ½ln|f'(z_k)|
- `equations_of_motion_invariant_check(N, a, b, c, d)` → verify ∂H/∂z_j unchanged for j≠k

Paper numbers: T_m = m(N−m)/2 exact, δ = −N/(4πR²) on sphere of radius R

### `viz/figures.py` — figure generation API
One function per paper figure, named by figure number:
- `fig1_spiral_to_polygon(r_values, outdir)` → saves `figures/01_spiral_to_polygon.png`
- `fig2_energy_curvature(N_range, outdir)` → saves `figures/02_energy_curvature.png`
- `fig3_cross_planetary(outdir)` → saves `figures/03_cross_planetary.png`
- `fig4_complete_chain(outdir)` → saves `figures/04_complete_chain.png`
- `fig5_thomson_stability(outdir)` → saves `figures/05_thomson_stability.png`
- `fig_extension(section, outdir)` → extension figures for §6.1–6.8 by section number
Each function takes an `outdir` defaulting to `"figures/"` and returns the filepath.

---

## Layer 4: Supplementary Scripts

### `scripts/prop4_characteristic_polynomial.py`
Standalone. Uses `sympy`. Computes:
1. Symbolic constrained Hessian for N=6 ring + central vortex with strength `kappa_0` (symbolic)
2. Characteristic polynomial of the Hessian in `kappa_0/kappa`
3. Exact symbolic root `kappa_crit = -1/4` — asserts `abs(float(root) + 0.25) < 1e-10`
4. Numerical sign check: eigenvalue at `kappa_0/kappa = -1/4 + 0.01` (positive) and `-1/4 - 0.01` (negative)
5. Prints polynomial and stability boundary in LaTeX format

### `scripts/prop_inertia_verification.py`
Standalone. Verifies three functional-analytic claims of Proposition 8 (Inertia Preservation):

**(a) Center eigenvalue convergence (claim (a) in proof):**
For N=3..7, compute blob Hessian center-sector eigenvalues at ε = 0.1, 0.05, 0.01, 0.005.
Fit convergence rate to O(εᵅ). Print table: Havelock limit, observed α, PASS if α ≥ 1.8.

**(b) Shape-sector lower bound (claim (b) in proof):**
For Gaussian blob at each ε ∈ {0.1, 0.05, 0.01}, compute smallest shape-sector eigenvalue.
Print ratio `(eigenvalue × ε²)` — PASS if variation across ε < 5%.

**(c) Center-shape coupling (claim (c) in proof):**
Measure coupling block Frobenius norm at each ε. Fit to `A·ε⁻¹·exp(−d_min/ε)`.
PASS if exponential fit R² > 0.99.

Final table: for each N, full-blob inertia vs point-vortex inertia — PASS if equal.

---

## Layer 5: Notebooks

One notebook per paper section. Each:
- Imports exclusively from `planetary_polygons.*`
- Runs top-to-bottom in < 2 minutes
- Final cell prints every paper-cited number with PASS/FAIL verdict
- Regenerates the section's figures into `figures/`
- Tested via `uv run pytest --nbmake notebooks/`

```
notebooks/
├── 01_energy_curvature.ipynb          # §3.1 — Theorem 1, N-gon energy curves
├── 02_sign_rule.ipynb                  # §3.2 — Theorem 2, all interaction classes
├── 03_constrained_minimum.ipynb        # §3.3 + §3.5 — Theorem 3, eigenvalue table,
│                                       #   why -ln r is special (logarithmic_specialness)
├── 04_central_vortex.ipynb             # §3.4 — Prop 4, κ_crit, char. polynomial
├── 05_planetary_verification.ipynb     # §4   — σ_geom, Saturn/Jupiter cross-comparison
├── 06_curved_surfaces.ipynb            # §6.1 — sphere φ_crit(N), hyperbolic N_crit
├── 07_deformation_radius.ipynb         # §6.2 — K₀ suppression, R/R_d transition
├── 08_n7_bifurcation.ipynb             # §6.3 — quartic 153/7, α₀≈3.2
├── 09_blob_correction.ipynb            # §6.4 — P_m table, profile independence
├── 10_multiring.ipynb                  # §6.5 — N=8 single-ring analysis (jupiter_north/south),
│                                       #   stability diagram; "multiring" = the §6.5 section name
├── 11_bec_vortices.ipynb               # §6.6 — BEC κ_crit, N=8 prediction
├── 12_bridge.ipynb                     # §6.7 — Γ-convergence, both bridges
└── 13_riemannian_havelock.ipynb        # §6.8 — Havelock T_m, trace formula δ, Möbius
```

---

## Test Coverage

All new modules in `extensions/` get corresponding test files. The `kappa_crit = -1/4` result
must be tested to exact precision (not just a loose bracket):

```
tests/
├── test_n7_bifurcation.py      # quartic==153/7 exact, α₀≈3.24 (tol 0.01), correction≈2.39
├── test_blob_correction.py     # full P_m table: assert Pm == Fraction(expected) for each N
├── test_curved_surfaces.py     # sphere eigenvalues shape/sign, hyperbolic N_crit=12 at R/a=1
├── test_deformation_radius.py  # K₀ transition: 1.2 < R_Rd_transition < 1.4
├── test_bec_vortices.py        # assert kappa_crit(8) < 1.0 and q0_min(8) == 1
├── test_bridge.py              # convergence rate α: assert 1.8 < alpha < 2.2
├── test_riemannian_havelock.py # T_m==m(N-m)/2 for all N=3..9, δ formula on sphere
└── test_prop4_kappa_crit.py    # assert abs(kappa_crit_sympy(6) + 0.25) < 1e-10
                                #   imports: from planetary_polygons.core.hessian import kappa_crit_sympy
```

**New public function required in `core/hessian.py`:**
`kappa_crit_sympy(N)` — uses sympy to compute the exact κ_crit for the N-gon ring stabilized
by a central vortex, returning a sympy Rational. For N=6 must return `-1/4`. This function
is the importable counterpart to the standalone script in `scripts/prop4_characteristic_polynomial.py`.

Also update existing tests for new import paths. Target: ≥ 150 total tests passing.

---

## Success Criteria

- [ ] `uv sync` installs all dependencies from lockfile without errors
- [ ] `uv run pytest tests/ -q` → all tests green, 0 failures, ≥ 150 tests
- [ ] `uv run pytest --nbmake notebooks/` → all 13 notebooks execute without error
- [ ] Every number cited in the paper has a corresponding test asserting it to stated precision
- [ ] Each notebook regenerates its section's figures (files written to `figures/`)
- [ ] `uv run python scripts/prop4_characteristic_polynomial.py` → prints `κ_crit = -1/4` and asserts it symbolically
- [ ] `uv run python scripts/prop_inertia_verification.py` → prints PASS for claims A, B, C and all N
