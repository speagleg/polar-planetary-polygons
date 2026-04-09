# Bernoulli Backbone Code Modules — Spec 1 of 3

## Goal

Build the code infrastructure for the Bernoulli-Havelock backbone: 5 new/updated Python modules + 6 test files that implement the orbit-based CKM, PMNS, fermion masses, baryon asymmetry, and instanton proof. All 15+ derived observables from the investigation document are codified with tests against PDG values.

## Context

The investigation at `docs/investigations/2026-04-09-bernoulli-havelock-backbone.md` derives 15 observables from N=7. This session produced the formulas and numerical verification. This spec codifies them into testable, importable modules.

This is Spec 1 of 3:
- **Spec 1 (this):** New code modules alongside existing code
- **Spec 2 (future):** Legacy cleanup (fix L/R bug, remove stale formulas, reconcile)
- **Spec 3 (future):** Paper edits across all 6 papers

## Architecture

New modules are built ALONGSIDE existing code with NO imports from old CKM/fermion modules. A single constant `SIGMA_0 = 5` in `bernoulli_havelock.py` controls the entire framework.

### Dependency graph

```
bernoulli_havelock.py  (SIGMA_0, K, phases, F_IR, conformal_dim)
        |
        v
   orbit_ckm.py  (builds Yukawa, extracts CKM)
     /       \           \
    v         v           v
pmns_mixing.py  orbit_masses.py  baryon_asymmetry.py

instanton_proof.py  (standalone, imports only bernoulli_havelock for constants)
```

No circular dependencies. No imports from old modules (`ckm_mixing.py`, `ckm_toeplitz.py`, `fermion_masses.py`).

## Module Specifications

### Module 1: `src/planetary_polygons/extensions/bernoulli_havelock.py` (UPDATE)

**Existing:** 106 tests covering Gauss sum chain, Bernoulli identities, moment tower, CKM phase from Gauss sum.

**New exports to add:**

```python
SIGMA_0 = 5  # The single geometric parameter

N_CRIT = 7  # Critical polygon from Havelock stability

def havelock_eigenvalue_unified(m, N=7):
    """lambda_m = (N-1) - m(N-m)/2. The stability eigenvalue."""

def conformal_dim_unified(m, N=7):
    """c = 1/2 + lambda_m/N. Unified conformal dimension."""

def F_IR(c, sigma):
    """Correct RS IR-brane overlap.
    F(c, sigma) = sqrt((2c-1)/(exp((2c-1)*sigma) - 1)) for c > 1/2.
    F(1/2, sigma) = 1/sqrt(sigma).
    """

def instanton_fugacity(N=7):
    """K = exp(-2*pi*k_frac) where k_frac = frac(c_N/6 - N/2)."""

BERNOULLI_PHASES = {
    'aL': Fraction(1, 7),    # = (N-1)/denom(B_6) = 6/42
    'aR': Fraction(5, 42),   # = (N-2)/denom(B_6)
    'aH': Fraction(2, 21),   # = (N-3)/denom(B_6) = 4/42
}
```

Does NOT modify any existing functions. Pure additions.

### Module 2: `src/planetary_polygons/extensions/orbit_ckm.py` (NEW)

**Purpose:** Build orbit-based CKM matrix, extract all 5 observables.

**Constants:**
```python
UP_L = [1, 2, 4]    # QR(7) = quadratic residues
DN_L = [6, 5, 3]    # QNR(7) = quadratic non-residues
HIGGS = [3, 4]       # Higgs modes (straddle both orbits)
```

**Key functions:**

```python
def build_orbit_yukawa(L_modes, sigma=SIGMA_0):
    """Build 3x3 complex Yukawa with Bernoulli instanton phases.
    
    Each entry: sum over R modes {L_j, N-L_j} and Higgs {3,4}
    of F_IR(c(mL)) * F_IR(c(mR)) * exp(2pi*i*(aL*mL + aR*mR + aH*mH)/N)
    where the selection rule mL - mR + mH = 0 mod N is enforced.
    """

def diag_left(Y):
    """Diagonalize YY^dag (NOT Y^dag Y) to get LEFT rotation U_L.
    Returns (mass_eigenvalues, U_L).
    CKM uses LEFT rotations: V = U_L_up^dag * U_L_down.
    """

def ckm_matrix(sigma=SIGMA_0):
    """Compute the full CKM matrix and all observables.
    
    Returns dict with:
        V: 3x3 complex CKM matrix
        s12, s23, s13_tree, s13_corrected: mixing angles
        J: Jarlskog invariant
        beta, alpha, gamma: unitarity triangle angles
        delta_CKM: the CP phase = arctan(sqrt(7))
    """

def instanton_correction(s13_tree, K, N=7):
    """s13_corrected = s13_tree * K^(N-1).
    The N-1 power = 2*(N-1)/2 from max intra-orbit gap in both sectors.
    """

def unitarity_triangle(V):
    """Extract alpha, beta, gamma from CKM matrix V.
    Uses standard definitions:
        alpha = arg(-V_td V_tb* / (V_ud V_ub*))
        beta  = arg(-V_cd V_cb* / (V_td V_tb*))
        gamma = arg(-V_ud V_ub* / (V_cd V_cb*))
    """
```

### Module 3: `src/planetary_polygons/extensions/pmns_mixing.py` (NEW)

**Purpose:** PMNS neutrino mixing from CKM-PMNS complementarity.

```python
def pmns_angles(s12_ckm=None, sigma=SIGMA_0):
    """PMNS predictions from the Z_7 backbone.
    
    theta_12 = pi/4 - arcsin(s12_ckm)  [complementarity]
    theta_23 = pi/4                      [pair symmetry]
    sin^2(theta_13) = (1/2)*sin^2(arcsin(s12_ckm))  [index-2 factor]
    delta_CP = arctan(sqrt(7))           [same Gauss sum as CKM]
    
    If s12_ckm not provided, computes it from orbit_ckm.ckm_matrix().
    """

def complementarity_identity():
    """Verify arctan(1/2) + arctan(1/3) = pi/4.
    This identity connects the index-3 (CKM) and index-2 (PMNS)
    subgroups of (Z/7Z)*.
    """

def reactor_angle(s12_ckm):
    """sin^2(theta_13^PMNS) = (1/2)*sin^2(theta_C).
    The 1/2 comes from the index-2 subgroup structure.
    """
```

### Module 4: `src/planetary_polygons/extensions/orbit_masses.py` (NEW)

**Purpose:** Fermion mass predictions from the backbone.

```python
def sigma_mass(sigma_0=SIGMA_0):
    """sigma_mass = sigma_0 * sqrt(N). The mass hierarchy scale."""

def mass_ratio_up(m, N=7, sigma_0=SIGMA_0):
    """m_f/m_t for up-type quarks.
    
    For lambda=0 (t): ratio = 1 (BF threshold, reference)
    For lambda=1 (c): ratio = exp(-2*sigma_mass/N) * K^2
    For lambda=3 (u): ratio = exp(-6*sigma_mass/N)
        (pure RS at sigma_mass=13.2: the RS profile already gives 1.2e-5,
        matching obs 1.3e-5. Adding K^6 would overshoot by 35x.
        The instanton correction saturates when exp(-2*lam*sig/N) < K^{2*lam}.)
    """

def mass_ratio_down(m, N=7, sigma_0=SIGMA_0):
    """m_f/m_t for down-type quarks.
    
    Isospin shift: c_dn = c_up + 1/N.
    For 3rd gen: m_b/m_t = exp(-2*sigma_mass/N)
    """

def mass_table(sigma_0=SIGMA_0):
    """All 6 quark mass predictions in GeV.
    Returns dict: {t, b, c, s, u, d} with pred and obs values.
    """

def isospin_shift(N=7):
    """Returns 1/N = the conformal dimension shift for down-type quarks."""
```

### Module 5: `src/planetary_polygons/extensions/baryon_asymmetry.py` (NEW)

**Purpose:** eta_B = J * K^C(N-1,2) / N.

```python
def instanton_power(N=7):
    """C(N-1, 2) = (N-1)(N-2)/2 = 15 at N=7.
    Number of independent off-diagonal entries in the (N-1)x(N-1) mass matrix.
    """

def eta_B(J=None, K=None, N=7, sigma=SIGMA_0):
    """Baryon asymmetry: eta_B = J * K^{C(N-1,2)} / N.
    
    If J not provided, computes from orbit_ckm.ckm_matrix().
    If K not provided, computes from instanton_fugacity(N).
    """

def full_prediction(sigma_0=SIGMA_0):
    """Complete baryon asymmetry with all intermediate values.
    Returns dict with J, K, power, eta_B, eta_obs, match_pct.
    """
```

### Module 6: `src/planetary_polygons/proofs/instanton_proof.py` (NEW)

**Purpose:** Formal derivation of the K^(N-1) suppression for V_ub.

```python
def texture_zero_proof(N=7):
    """Prove (YY^dag)_{02} = 0 from the Z_N selection rules.
    
    Constructs the texture from mL - mR + mH = 0 mod N,
    then verifies algebraically that (YY^dag)_{02} = 0
    because Y_{00} = Y_{21} = Y_{22} = 0 in the texture.
    """

def winding_numbers(N=7):
    """Compute winding numbers for each CKM element.
    
    Returns table:
        V_us: w_up=1, w_dn=1, total=2, level=TREE  [(YY^dag)_{01} != 0]
        V_cb: w_up=2, w_dn=2, total=4, level=TREE  [(YY^dag)_{12} != 0]
        V_ub: w_up=3, w_dn=3, total=6, level=INST  [(YY^dag)_{02} = 0]
    """

def instanton_action(N=7):
    """S_inst = (N-1) * 2*pi*k_frac.
    
    Proof: w_total = w_up + w_dn = (N-1)/2 + (N-1)/2 = N-1
    because the max intra-orbit gap in QR (and QNR) is (N-1)/2.
    """

def selectivity_proof(N=7):
    """Prove the instanton correction applies ONLY to V_ub.
    
    Direct mixing: (YY^dag)_{01} != 0, (YY^dag)_{12} != 0 -> tree level
    Indirect mixing: (YY^dag)_{02} = 0 -> instanton level
    Therefore V_us, V_cb are uncorrected; V_ub gets K^(N-1).
    """
```

## Test Specifications

### `tests/test_bernoulli_havelock.py` (UPDATE — add ~15 tests)

**New Tier 1 tests:**
- `test_sigma_0_is_5`: SIGMA_0 == 5
- `test_havelock_eigenvalue_QR`: lambda = {3,1,0} for QR={1,2,4}
- `test_conformal_dim_at_BF`: c(m=4) = 1/2 exactly
- `test_F_IR_at_BF`: F_IR(0.5, sigma) = 1/sqrt(sigma)
- `test_F_IR_exponential_suppression`: F_IR(0.93, 10) << F_IR(0.5, 10)
- `test_bernoulli_phases_ratio`: aL/aR == Fraction(6,5)
- `test_bernoulli_phases_denominator`: all denominators divide 42

### `tests/test_orbit_ckm.py` (NEW — ~25 tests)

**Tier 1 (exact):**
- `test_up_modes_are_QR`: UP_L == [1,2,4]
- `test_texture_shape`: 5 nonzero entries, 4 zeros
- `test_YYdag_02_zero`: (YY^dag)[0,2] == 0 to machine precision
- `test_left_rotation_differs_from_right`: U_L != U_R for complex Y
- `test_ckm_unitarity`: V^dag V = I within 1e-12

**Tier 2 (PDG tolerance):**
- `test_delta_ckm`: beta within 3 deg of 69 (1 sigma)
- `test_s12`: within 10% of 0.2245
- `test_s23`: within 15% of 0.0421
- `test_s13_tree`: s13_tree > 0.1 (uncorrected)
- `test_s13_corrected`: within 10% of 0.00365
- `test_jarlskog`: within 15% of 3.08e-5
- `test_sin2_delta`: abs(sin^2 - 7/8) < 0.02

**Tier 3 (structural):**
- `test_instanton_only_vub`: V_us and V_cb don't change with K correction
- `test_sigma_independence_of_phases`: beta at sigma=3 == beta at sigma=10 within 5 deg
- `test_up_down_same_texture`: up and down Yukawa have identical zero pattern

### `tests/test_pmns_mixing.py` (NEW — ~10 tests)

**Tier 1:**
- `test_complementarity_identity`: arctan(1/2) + arctan(1/3) == pi/4
- `test_reactor_angle_formula`: sin^2 = (1/2)*sin^2(theta_C)

**Tier 2:**
- `test_theta_12`: within 1 deg of 33.41
- `test_theta_23`: within 5 deg of 49 (large experimental uncertainty)
- `test_theta_13`: within 1 deg of 8.54
- `test_delta_cp_pmns`: == arctan(sqrt(7)) (same as CKM)

### `tests/test_orbit_masses.py` (NEW — ~10 tests)

**Tier 1:**
- `test_sigma_mass_formula`: sigma_mass == SIGMA_0 * sqrt(7)
- `test_isospin_shift`: == 1/N

**Tier 2:**
- `test_mt`: reference (173 GeV)
- `test_mb`: within 10% of 4.18 GeV
- `test_mc`: within 10% of 1.27 GeV
- `test_mu`: within 10% of 2.2 MeV

### `tests/test_baryon_asymmetry.py` (NEW — ~8 tests)

**Tier 1:**
- `test_instanton_power`: C(6,2) == 15
- `test_instanton_power_is_binomial`: == (N-1)*(N-2)/2

**Tier 2:**
- `test_eta_B`: within 5% of 6.12e-10
- `test_eta_B_positive`: eta_B > 0
- `test_eta_B_order_of_magnitude`: 1e-10 < eta_B < 1e-9

### `tests/test_instanton_proof.py` (NEW — ~10 tests)

**Tier 1:**
- `test_texture_zero`: (YY^dag)_{02} == 0 algebraically
- `test_winding_vub`: w_total == N-1 == 6
- `test_winding_vus`: w_total == 2 (tree level)
- `test_winding_vcb`: w_total == 4 (tree level)
- `test_max_intra_orbit_gap`: == (N-1)/2 == 3 for QR and QNR
- `test_instanton_action`: S == (N-1) * 2*pi*k_frac
- `test_selectivity`: only V_ub gets correction

## Success Criteria

1. All new tests pass (`pytest tests/test_orbit_ckm.py tests/test_pmns_mixing.py tests/test_orbit_masses.py tests/test_baryon_asymmetry.py tests/test_instanton_proof.py -v`)
2. All existing 106 bernoulli_havelock tests still pass
3. No imports from old CKM/fermion modules
4. All 15 observables from the investigation doc are codified and tested
5. Total new tests: ~78 (15 + 25 + 10 + 10 + 8 + 10)

## Out of Scope (Spec 2 and 3)

- Fixing the L/R bug in existing `ckm_mixing.py`
- Removing stale 70.2 deg formula from `proofs/fermion_derivation.py`
- Reconciling the two CKM derivations (68.63 vs arctan(sqrt(7)))
- Any LaTeX paper edits
- Updating existing test assertions for old modules
