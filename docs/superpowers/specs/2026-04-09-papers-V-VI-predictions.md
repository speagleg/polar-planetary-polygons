# Papers V+VI: Baryogenesis, Strong CP, Predictions — Spec 3C of 4

## Goal

Update Paper V (cosmology) with the new baryon asymmetry formula and strong CP result. Update Paper VI (discussion) with the complete prediction table and testable predictions. Both papers consume results from Papers I (Spec 3A) and IV (Spec 3B).

## Paper V changes

### Section: Baryogenesis (line 1168)

**Current:** eta_B ≈ 2e-9, factor of 3 above observed. Uses sin(2*pi*k_frac) as the CP source with sphaleron transport.

**New:** Replace with the Bernoulli backbone formula:
  eta_B = J * K^{C(N-1,2)} / N = J * K^15 / 7

Where:
- J = Jarlskog invariant (from Paper IV orbit-based CKM)
- K = exp(-2*pi*k_frac) = 0.548 (instanton fugacity)
- C(N-1,2) = C(6,2) = 15 (off-diagonal entries in mass matrix)
- 1/N = fractional baryon number from Z_7 orbifold

Result: eta_B = 5.96e-10 (obs 6.12e-10, 2.6% match).

This REPLACES the transport-equation derivation. The new formula is algebraic (no transport coefficients, no v_w dependence, no Yukawa rate Gamma_y).

**Also update:**
- Line 1193: 68.63° → arctan(√7)
- Line 1199: Remove arg Gamma(1/2+i) reference
- Lines 1275-1301: Replace factor-of-3 discussion with 2.6% match

### Section: Strong CP (NEW)

Add after baryogenesis:
- theta_QCD = arg(det(Y_u * Y_d)) = pi/N = pi/7 (topological, sigma-independent)
- Nelson-Barr mechanism: CP violation is spontaneous (from Gauss sum, not theta)
- Loop suppression: theta_phys ~ (m_u*m_d)/(m_c*m_s) * alpha_s * pi/7 ~ 10^{-12} < 10^{-10}
- Testable: theta_QCD ~ 10^{-12} for next-gen neutron EDM experiments

### Section: Fermion masses (update existing)

Update with the unified formula c = 1/2 + lambda/N:
- sigma_mass = sigma_CKM * sqrt(N) = 5*sqrt(7) = 13.2
- mt, mb, mc, mu predictions (4/6 within 7%)
- Isospin shift 1/N for down-type
- Note ms and md need generation-dependent isospin

## Paper VI changes

### Prediction summary table (line 289 area)

Replace/expand with the COMPLETE backbone table:

| Observable | Prediction | PDG | Match | Source |
|-----------|-----------|-----|-------|--------|
| delta_CKM | arctan(√7) | 69±3° | 0.1σ | Gauss sum |
| s12 | 0.230 | 0.225 | 2% | Bernoulli phases |
| s23 | 0.043 | 0.042 | 1% | RS at sigma=5 |
| s13 | 0.0024 | 0.00365 | 35% | K^(N-1) instanton |
| J | 2.1e-5 | 3.08e-5 | 31% | from above |
| theta_12^PMNS | 32.9° | 33.4° | 0.5° | complementarity |
| theta_23^PMNS | 45° | 49±4° | 1σ | pair symmetry |
| theta_13^PMNS | 9.3° | 8.5° | 0.8° | (1/2)sin²(theta_C) |
| sin²theta_W | 3/11 | 0.231 | known | B_2 evaluations |
| eta_B | 5.96e-10 | 6.12e-10 | 2.6% | J*K^15/N |
| mt | 173 GeV | 173 GeV | ref | BF threshold |
| mb | 3.95 GeV | 4.18 GeV | 5.5% | isospin shift |
| mc | 1.19 GeV | 1.27 GeV | 6.5% | RS + K^2 |
| mu | 2.06 MeV | 2.2 MeV | 6.4% | RS profile |
| theta_QCD | <10^{-10} | <10^{-10} | Nelson-Barr | pi/N loop-suppressed |

### Testable predictions section (NEW or expand existing)

- delta_CP^PMNS = arctan(√7) = 69.3° (DUNE, Hyper-K)
- theta_QCD ~ 10^{-12} (next-gen neutron EDM)
- sin²(theta_13^PMNS) = (1/2)sin²(theta_C) = 0.022 (reactor experiments, already measured)
- CKM-PMNS complementarity: theta_12^CKM + theta_12^PMNS = pi/4 (precision tests)

### Line-by-line 68.63 replacements

- Line 57: 68.63° → arctan(√7) = 69.3°
- Line 158: formula update 2*theta_CS*tanh(pi) → arctan(√7) from Gauss sum
- Line 289: table update
- Line 697: statement update

## Files to modify

- `latex/paper-5-cosmology/main.tex`
- `latex/paper-6-discussion/main.tex`

## Success criteria

1. Both papers compile
2. Zero instances of 68.63 remain in either file
3. eta_B formula is the algebraic backbone version (not transport equation)
4. Strong CP section exists with Nelson-Barr mechanism
5. Complete 15-observable prediction table in Paper VI
6. Testable predictions section names specific experiments
