# Source Code Audit Results

**Date**: 2026-04-03
**Total files analyzed**: 201 Python source files

## Summary

| Category | Count | % | Action |
|----------|-------|---|--------|
| KEEP | 80 | 45% | Goes in clean repo |
| DEAD | 55 | 31% | Archive — no tests, no imports, no paper backing |
| EXPLORATORY | 37 | 21% | Archive separately — number theory/Bolza investigations |
| DUPLICATE | 5 | 3% | Remove — identical root copies |

## Duplicates (remove)

These 5 root `src/` files are identical to their package equivalents:

| Root file | Package equivalent |
|-----------|-------------------|
| src/variational.py | src/planetary_polygons/core/variational.py |
| src/sign_rule_proof.py | src/planetary_polygons/core/sign_rule.py |
| src/thomson.py | src/planetary_polygons/core/thomson.py |
| src/jupiter_data.py | src/planetary_polygons/data/jupiter.py |
| src/sigma_geometric.py | src/planetary_polygons/verification/sigma_geometric.py |

## KEEP — Root standalone files (10)

These have no package equivalent and are imported by verification scripts:

- saturn_data.py (superseded by package — use package version)
- rossby.py (superseded by package — use package version)
- constrained_hessian.py (superseded by package — use package version)
- saturn_verification.py — imports qgpv, matching, cassini_winds
- jupiter_verification.py — baseline verification
- qgpv.py — standalone QGPV solver
- matching.py — BVP matching
- cassini_winds.py — Cassini wind analysis
- n8_instability.py — N=8 instability
- theorem4_reformulated.py — Theorem 4 exploration

## KEEP — Package files (70)

### Core (6): sign_rule, thomson, variational, rossby, hessian, laplacian_unification, universal_selection, logarithmic_specialness, amplitude, first_principles

### Data (2): saturn, jupiter

### Verification (3): saturn, jupiter, sigma_geometric

### Viz (1): figures

### Extensions — tested (53):
ads_cft_dictionary, algebraic_thresholds, baryogenesis, baryogenesis_transport, bec_vortices, blob_correction, bridge, btz_entropy, catseye_decomposition, circulation_disorder, ckm_mixing, ckm_toeplitz, curved_surfaces, dark_sector, deformation_radius, developing_map, dimension_proof, dimensional_uniqueness, entropy_bridge, fermion_masses, first_principles, frobenius_census, graviton_4d, gravity_partition, h2_stability, hierarchy, jacobson_derivation, k0_central_vortex, k_theoretic_stability, laplacian_unification, lichnerowicz_havelock, loop_corrections, n7_bifurcation, n_selection, ncrit_delta, neutrino_masses, oblate_spheroid, onsager_selection, packing_analysis, palindromic_census, pell_identity_proof, penrose_arrow, penrose_weyl, polygon_btz_action, radion_inflation, rg_stability, riemannian_havelock, tessellation_stability, two_ring, universal_selection, virasoro_block, zn_conformal_block, spheroidal_havelock

### Number theory — tested (4): arithmetic, bolza_form, l_functions, singular_series

### Proofs — tested (13):
aps_index_proof, casimir_equals_havelock, clausius_cardy_rt, cs_to_4d_bridge, entropy_regularization, identity_block_dominance, jensen_epsilon4_bound, mass_hierarchy, oneloop_exactness, riemannian_havelock_step3, self_decoherence, spectral_edge_transition, topological_protection

## DEAD — Extensions (47)

No tests, not imported, no paper backing:

anomaly_4d, bolza_fuchsian, bolza_spectral, born_oppenheimer, catseye_hessian, cft3_havelock, chern_simons_lift, cl_spectral_determinant, conformal_block_zn, cosmological_constant, cs_quantization, dark_ratio, dimensional_lift, dynamical_gauge, dynamical_matrix, einstein_4d, einstein_4d_exact, energy_budget, equivariant_index, fermions_uv, field_theory_4d, geometric_quantization, graviton_propagator, havelock_schrodinger, kaluza_klein_lift, lambda_landscape, langlands_test, large_n_gap, lorentzian_continuation, magri_hierarchy, magri_verify, mass_gap, metric_dynamics, multiring, one_loop_determinant, pbh_nselection, planck_sensitivity, quantum_regime, radion_power_spectrum, small_ring_expansion, symplectic_comparison, tiling_stability, wdw_2d_landscape, weyl_anomaly_cancellation, weyl_anomaly_delta, wheeler_dewitt, zamolodchikov_finite_c

## DEAD — Proofs (8)

cms_cs_isomorphism, cs_noncompact_welldefined, cs_sector_coexistence, eta_invariant_seifert, gaudin_calogero_moser, mass_gap_log_schrodinger, regge_entropy_szego, rg_stability_characterization, shell_dominance_bound

## EXPLORATORY — Number theory (34)

Langlands/Bolza investigations without paper backing:

adequacy_k9_to_k15, adequacy_test, bolza_48pt_vortex, bolza_gl2_identify, bolza_heat_kernel, bolza_hecke_normalize, bolza_hecke_operator, bolza_refined, bolza_spectral (nt), bolza_symk_propagation, bolza_to_rh, bolza_vortex, calegari_geraghty_verify, chebyshev_bias, consecutive_correlation, euler_product, functoriality, gap_analysis, gl3_and_higher, gpy_constrained, gpy_hecke, hilbert_modular_N7, langlands_all_N, langlands_connection, langlands_verify, level1_test, mellin_lfunc, modularity_lifting, n11_artin, n7_artin_rep, n7_hilbert_match, nonvanishing_symk, palindromic_comparison, sieve

## EXPLORATORY — Proofs (3)

dreibein_havelock, symbolic_two_ring_proof, (1 other)

## Clean Repo Target

~80 source files + 90 test files + 28 notebooks + 6 papers + companion + supplements
Down from 201 source files (60% reduction in source, zero reduction in verified content)
