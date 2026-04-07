# Figure Placement Plan

## Critical Finding
16 existing figure assets in `figures/` are orphaned — no `\includegraphics` in any LaTeX file.

## Existing Assets (16 files in figures/)
- `01_spiral_to_polygon.png`, `02_energy_curvature.png`, `03_cross_planetary.png`
- `04_complete_chain.png`, `05_thomson_stability.png`
- `fig_eigenvalue_threshold.pdf`, `fig_ncrit_phase_diagram.pdf`
- `fig_oblateness_signflip.pdf`, `fig_constraint_intersection.pdf`
- `fig_wdw_potential.pdf`, `fig_energy_budget.pdf`
- `fig_hierarchy_decomposition.pdf`, `fig_frobenius_orbits.pdf`
- `fig_scorecard_predicted_vs_observed.pdf`, `fig_penrose_arrow.pdf`
- `fig_cross_system_universality.pdf`

Also 3 PDFs in `latex/paper/figures/`.

## New Figures Needed (8)

| ID | Paper | Section | Content | Priority |
|----|-------|---------|---------|----------|
| V-1 | V | §2.2 | G(χ) plot on S³ | High |
| V-2 | V | §3.1 | 600-cell distance class histogram | High |
| V-3 | V | §4 | K-matrix eigenvalue spectrum (d² degeneracies) | High |
| V-4 | V | §7 | Phase transition energy gap ΔE(R) | Medium |
| V-5 | V | §8 | 120/128 Coxeter decomposition visual | Medium |
| 0-1 | 0 | §1 | Thurston geometry triptych (S³→R³→SL̃(2,R)) | High |
| I-1 | I | §7 | McKay/Ẽ₈ Dynkin with golden ratio eigenvalues | High |
| I-2 | I | §6 | Icosahedron bridge identity visualization | Medium |

## Immediate Actions
1. Wire existing orphaned figures into Papers I-VI where they belong
2. Generate the 8 new figures using existing plotting code + new scripts
3. Add \includegraphics calls to LaTeX source
