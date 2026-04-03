# Notebook Audit Results

**Date**: 2026-04-03
**Total notebooks**: 28

## Summary

| Category | Count | Notebooks |
|----------|-------|-----------|
| MASTER | 1 | 00 |
| ESSENTIAL | 7 | 01-07 |
| SUPPLEMENTARY | 20 | 08-10, 12-27 (excl 11) |
| EXPLORATORY | 1 | 11 |

All 28 executable non-interactively via `jupyter nbconvert --execute`.

## Essential (7) — compute non-duplicated paper claims

- 01_Havelock_Eigenvalues — Paper I §3: eigenvalue formula + Lagrange multiplier
- 02_N7_Quartic_Exact — Paper I §6.3: constrained quartic 135/7, α₀ = 45/14
- 03_S2_Rational_Thresholds — Paper I §4.2: {1/3, 1/5, 1/7, 1/19}
- 04_H2_Algebraic_Thresholds — Paper I §4.3: ξ*=8-3√7, field extensions
- 05_Blob_Correction — Paper I §6.4: correction table, Proposition 8
- 06_Catseye_Bridge — Paper II §5: braid vanishing law, Hessian inertia
- 07_Circulation_Disorder — Paper II §8: Monte Carlo instability probability

## Supplementary (20) — duplicate test coverage, add narrative

08-Universal_Framework, 09-Orbifold_CFT, 10-Ncrit_Delta, 12-Stability_Counting_S2,
13-Growth_Law_Bernoulli, 14-Analytical_Gap_Bound, 15-Ncrit_By_Dimension,
16-Number_Theory_Bridge, 17-BTZ_Critical_Exponent, 18-Blob_Catseye_Proofs,
19-K_Theory_Assembly_Map, 20-Wheeler_DeWitt_Lorentzian, 21-Gravity_Partition,
22-Finite_c_Equivariant_RR, 23-Sign_Rule_Constrained_Minimum,
24-Onsager_Selection_BEC, 25-Bolza_GPY, 26-BTZ_Entropy, 27-Einstein_From_Polygons

## Clean repo recommendation

Include ALL 28 in clean repo — they form a comprehensive verification corpus.
The 7 ESSENTIAL are mandatory; the 20 SUPPLEMENTARY provide pedagogical depth;
the MASTER notebook is the integration harness.
