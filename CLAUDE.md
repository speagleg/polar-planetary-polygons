# CLAUDE.md — Planetary Polygons Unified

## What this is

A mathematics/mathematical-physics paper project with full computational infrastructure.
The paper argues that the regular N-polygon of point vortices is a **constrained energy
minimum** (not maximum) on the angular-impulse surface, and that this single fact —
combined with the 2D logarithmic Green's function — explains planetary polar polygons
(Saturn's hexagon N=6, Jupiter's octagon N=8).

**Central result**: Havelock eigenvalue $\lambda_m = (N-1) - m(N-m)/2$.
Stability iff all $\lambda_m > 0$, i.e. $N \le 7$ (flat plane).

## Repo layout

```
src/planetary_polygons/
├── core/                    # Havelock, sign rule, constrained Hessian
└── extensions/
    ├── h2_stability.py       # C₁(H²,ξ), min_eigenvalue, N_crit table
    ├── riemannian_havelock.py # C₁ on general surfaces, XI_STAR_78
    ├── algebraic_thresholds.py # Exact H²/S² thresholds, field extensions
    ├── circulation_disorder.py # Disordered H_κ, Monte Carlo P(unstable)
    ├── blob_correction.py    # O(ε²) Cauchy-blob eigenvalue corrections
    ├── curved_surfaces.py    # S² and torus stability
    ├── deformation_radius.py # K₀ finite-Rossby-radius suppression
    ├── bec_vortices.py       # BEC quantized-circulation predictions
    ├── bridge.py             # Blob and Rossby bridges, βR³/κ criterion
    ├── onsager_selection.py  # H_{N+1} > H_N monotonicity proof
    ├── multiring.py          # Two-ring stability
    └── n7_bifurcation.py     # Quartic normal form, α₀ ≈ 3.2

latex/paper/main.tex          # The paper (2300+ lines, all sections complete)
tests/                        # 70+ passing tests (scipy tests skip if not installed)
docs/investigations/          # Session research notes
```

## Python environment

```bash
cd /mnt/c/Users/gspea/source/repos/planetary-polygons-unified
# Run tests (numpy/fractions only — no scipy needed):
python3 -m pytest tests/test_algebraic_thresholds.py tests/test_h2_stability.py \
    tests/test_riemannian_havelock.py tests/test_blob_correction.py \
    tests/test_circulation_disorder.py -q
```

scipy is **not installed** in this environment. Tests requiring scipy will be
skipped/errored; that is expected. Do not attempt to install packages.

## Key formulas (do not recompute from scratch)

```python
# H² curvature coefficient
C1_H2(N, xi) = (N-1)*(1 + xi**2) / (1 - xi)**2   # ξ = r_E²/a²

# S² curvature coefficient
C1_S2(N, xi) = (N-1)*(1 - xi) / (1 + xi)          # = (N-1)*cos(φ)

# 7→8 transition threshold (THE key algebraic result)
XI_STAR_78 = 8 - 3*sqrt(7)   # = ε⁻¹, inverse fundamental unit of Z[√7]
# ε = 8 + 3√7,  ε·ε⁻¹ = 64-63 = 1

# S² exact thresholds (all rational)
# N=3: 1/3,  N=4: 1/5,  N=5: 1/7,  N=6: 1/19,  N≥7: None

# H² field extensions (N≥8):
# even N → Q(√sq_free(N-1)),  odd N → Q(√sq_free(N-3))
# N=10: sq_free(9)=1, so ξ*(10) = 1/7 ∈ Q  (unique rational case in N≤16)
```

## Paper status

All sections written. Key results by status:

| Result | Status | Location |
|--------|--------|----------|
| Havelock eigenvalue formula | Known (1931), re-derived | §3 |
| N-gon is constrained energy minimum | New to stat-mech literature | §3, Thm 3 |
| Sign rule H''(0) < 0 | New | §2, Thm 2 |
| N=7 quartic stability (α₀ ≈ 3.2) | New | §3.3 |
| Blob bridge, profile independence | New | §5.2 |
| ξ* = 8−3√7 = ε⁻¹ ∈ Z[√7] | In abstract + §4.3 | §4.3 |
| General H² field pattern | New (this session) | §4.3 |
| S² exact rational thresholds | New (this session) | §4.2 |
| Circulation disorder resilience | New (this session) | §5.4 |
| Onsager max-N selection | New | §5.1, Prop 7 |
| Rossby bridge (Saturn n*=6) | Known, formalized | §5.3 |
| χ enters at O(χ) not O(K²) | New remark | §4.3 |

## Preferences

- Every numerical claim must be backed by code in `tests/` or `src/`
- New results: write test first, then implementation, then paper text
- Label things PROVEN / NUMERICAL / CONJECTURE honestly
- Be direct; no filler
- The paper is in good shape — do not restructure, only extend
