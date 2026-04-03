# Clean Publication Repository Design

**Date**: 2026-04-03
**Status**: Approved

## Purpose

Migrate the verified, tested, paper-backing content from the development repo into a new clean publication repository. The clean repo is the permanent, citable, independently verifiable artifact for the paper series.

## Clean Repo Name

To be created by Gordon. Suggested: `planetary-polygons` or `havelock-field-theory`.

## Structure

```
planetary-polygons/
├── README.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── .gitignore
│
├── src/planetary_polygons/
│   ├── __init__.py
│   ├── core/                          # 10 files
│   │   ├── __init__.py
│   │   ├── sign_rule.py
│   │   ├── thomson.py
│   │   ├── variational.py
│   │   ├── rossby.py
│   │   ├── hessian.py
│   │   ├── laplacian_unification.py
│   │   ├── universal_selection.py
│   │   ├── logarithmic_specialness.py
│   │   ├── amplitude.py
│   │   └── first_principles.py
│   │
│   ├── data/                          # 2 files
│   │   ├── __init__.py
│   │   ├── saturn.py
│   │   └── jupiter.py
│   │
│   ├── verification/                  # 3 files
│   │   ├── __init__.py
│   │   ├── saturn.py
│   │   ├── jupiter.py
│   │   └── sigma_geometric.py
│   │
│   ├── extensions/                    # 53 files (tested, paper-backing)
│   │   ├── __init__.py
│   │   ├── number_theory/             # 4 files
│   │   │   ├── __init__.py
│   │   │   ├── arithmetic.py
│   │   │   ├── bolza_form.py
│   │   │   ├── l_functions.py
│   │   │   └── singular_series.py
│   │   ├── algebraic_thresholds.py
│   │   ├── baryogenesis.py
│   │   ├── baryogenesis_transport.py
│   │   ├── bec_vortices.py
│   │   ├── blob_correction.py
│   │   ├── bridge.py
│   │   ├── btz_entropy.py
│   │   ├── catseye_decomposition.py
│   │   ├── circulation_disorder.py
│   │   ├── ckm_mixing.py
│   │   ├── ckm_toeplitz.py
│   │   ├── curved_surfaces.py
│   │   ├── dark_sector.py
│   │   ├── deformation_radius.py
│   │   ├── developing_map.py
│   │   ├── dimension_proof.py
│   │   ├── dimensional_uniqueness.py
│   │   ├── entropy_bridge.py
│   │   ├── fermion_masses.py
│   │   ├── frobenius_census.py
│   │   ├── graviton_4d.py
│   │   ├── gravity_partition.py
│   │   ├── h2_stability.py
│   │   ├── hierarchy.py
│   │   ├── jacobson_derivation.py
│   │   ├── k0_central_vortex.py
│   │   ├── k_theoretic_stability.py
│   │   ├── lichnerowicz_havelock.py
│   │   ├── loop_corrections.py
│   │   ├── n7_bifurcation.py
│   │   ├── n_selection.py
│   │   ├── ncrit_delta.py
│   │   ├── neutrino_masses.py
│   │   ├── oblate_spheroid.py
│   │   ├── onsager_selection.py
│   │   ├── packing_analysis.py
│   │   ├── palindromic_census.py
│   │   ├── pell_identity_proof.py
│   │   ├── penrose_arrow.py
│   │   ├── penrose_weyl.py
│   │   ├── polygon_btz_action.py
│   │   ├── radion_inflation.py
│   │   ├── rg_stability.py
│   │   ├── riemannian_havelock.py
│   │   ├── spheroidal_havelock.py
│   │   ├── spheroidal_eigenvalues.py
│   │   ├── standard_model_gauge.py
│   │   ├── tessellation_stability.py
│   │   ├── two_ring.py
│   │   ├── universal_selection.py
│   │   ├── virasoro_block.py
│   │   ├── wdw_initial_conditions.py
│   │   └── zn_conformal_block.py
│   │
│   ├── proofs/                        # 13 files (tested formal proofs)
│   │   ├── __init__.py
│   │   ├── aps_index_proof.py
│   │   ├── casimir_equals_havelock.py
│   │   ├── clausius_cardy_rt.py
│   │   ├── cs_to_4d_bridge.py
│   │   ├── entropy_regularization.py
│   │   ├── eta_invariant_seifert.py
│   │   ├── identity_block_dominance.py
│   │   ├── jensen_epsilon4_bound.py
│   │   ├── mass_hierarchy.py
│   │   ├── oneloop_exactness.py
│   │   ├── riemannian_havelock_step3.py
│   │   ├── self_decoherence.py
│   │   ├── spectral_edge_transition.py
│   │   └── topological_protection.py
│   │
│   └── viz/                           # 1 file
│       ├── __init__.py
│       └── figures.py
│
├── tests/                             # 91 test files, 1935 tests
│   ├── test_sign_rule.py
│   ├── test_thomson.py
│   ├── ... (all 91 test files)
│   ├── test_onsager_contraction.py    # NEW: Paper III gaps
│   ├── test_paper4_algebraic.py       # NEW: Paper IV algebraic
│   └── test_partial_promotions.py     # NEW: PARTIAL → VERIFIED
│
├── notebooks/                         # 38 notebooks, all executing
│   ├── 00_Master_Verification.ipynb
│   ├── 01_Havelock_Eigenvalues.ipynb
│   ├── ... (all 38)
│   └── 37_Penrose_Initial_State.ipynb
│
├── mathematica/                       # 12 symbolic proof files
│   ├── 01_energy_maximum_proof.wl
│   ├── ... (all 12)
│   └── 12_constrained_hessian_proof.wl
│
├── latex/
│   ├── shared/
│   │   ├── preamble.tex
│   │   └── refs.bib
│   ├── paper-1-mathematics/
│   │   └── main.tex
│   ├── paper-2-physics/
│   │   └── main.tex
│   ├── paper-3-gravity/
│   │   └── main.tex
│   ├── paper-4-field-theory/
│   │   └── main.tex
│   ├── paper-5-cosmology/
│   │   └── main.tex
│   ├── paper-6-discussion/
│   │   └── main.tex
│   ├── supplement-proofs/
│   │   └── main.tex
│   ├── supplement-number-theory/
│   │   └── main.tex
│   ├── companion/
│   │   └── main.tex
│   ├── readers-guide/
│   │   └── main.tex
│   └── build.sh
│
├── figures/
│   ├── 01_spiral_to_polygon.png
│   ├── 02_energy_curvature.png
│   ├── 03_cross_planetary.png
│   ├── 04_complete_chain.png
│   └── 05_thomson_stability.png
│
└── docs/
    ├── paper-code-mapping.md
    ├── source-audit-results.md
    ├── notebook-audit-results.md
    └── mathematica-audit-results.md
```

## What is EXCLUDED

Everything not in the structure above. Specifically:

### Development artifacts
- 9 PICKUP_*.md session notes
- SESSION_INTEGRATION_CATALOG.md
- FRAMEWORK.md
- .claude/ directory (4 files)
- docs/superpowers/ (16 plans/specs)
- docs/investigations/ (73 research notes)
- docs/agents/ (3 reviewer configs)
- docs/review_prompt_*.md (2 review prompts)
- docs/theorem_status.md
- docs/OPEN_PROBLEMS.md
- docs/why-polygons-explained.md

### Legacy/draft LaTeX
- latex/staging/ (1 transition doc)
- latex/REMOVED_CONTENT.md
- latex/paper-0-overview/ (old monolithic overview)
- latex/paper-A-appendices/ (old appendices)
- latex/paper/ (old monolithic paper + sections/)
- latex/paper-4-planets/ (alternate Paper IV)
- All .pdf, .aux, .log, .bbl, .blg, .out files (build artifacts)
- paper.pdf (root-level old output)
- texput.log

### Dead/exploratory Python
- 5 duplicate root src/ files
- 10 standalone root src/ files (superseded by package)
- 55 DEAD extension files
- 34 EXPLORATORY number theory files
- 8 DEAD proof files
- 3 EXPLORATORY proof files

### Build/lock files
- uv.lock (391KB)

## File counts

| Category | Count |
|----------|-------|
| Python source | 86 |
| Python tests | 91 |
| Jupyter notebooks | 38 |
| Mathematica | 12 |
| LaTeX papers | 10 (6 main + 2 supp + companion + guide) |
| LaTeX shared | 3 (preamble + refs + build.sh) |
| Figures | 5 |
| Docs | 4 |
| Config | 4 (pyproject.toml, requirements.txt, .gitignore, LICENSE) |
| **Total** | **~253 files** |

Down from ~500+ in the development repo.

## Migration method

1. Gordon creates empty repo on GitHub
2. Copy the files listed above (preserving directory structure)
3. Fresh `git init`, single initial commit
4. No development history carried over (clean start)
5. Run `python3 -m pytest tests/ -q` to verify 1935 tests pass
6. Run all 38 notebooks to verify execution
7. Push to GitHub

## README for clean repo

The README should contain:
- Project title and one-paragraph description
- Link to the paper series (arXiv or journal)
- Quick start: install + run tests
- Notebook index: which notebook verifies which paper claim
- Paper-to-code mapping reference
- License
- Author + contact

## License

MIT or BSD-3-Clause (Gordon's choice).

## Dependencies

```
numpy>=1.26
scipy>=1.12
matplotlib>=3.8
sympy>=1.12
jupyter>=1.0
```

No other dependencies. Pure Python + standard scientific stack.
