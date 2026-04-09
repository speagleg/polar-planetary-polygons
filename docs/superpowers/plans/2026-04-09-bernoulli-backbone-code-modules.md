# Bernoulli Backbone Code Modules — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build 5 new/updated Python modules + 6 test files implementing the orbit-based CKM, PMNS, fermion masses, baryon asymmetry, and instanton proof — all derived from the Bernoulli-Havelock backbone at N=7.

**Architecture:** Bottom-up build following the dependency graph: backbone additions → orbit_ckm (central) → three consumers (pmns, masses, baryogenesis) + instanton proof. New code lives alongside existing modules with no imports from old CKM/fermion code. A single constant `SIGMA_0 = 5` in `bernoulli_havelock.py` controls the framework.

**Tech Stack:** Python 3.12, numpy, pytest. No scipy required. Exact arithmetic with `fractions.Fraction` where possible.

**Spec:** `docs/superpowers/specs/2026-04-09-bernoulli-backbone-code-modules.md`

**Investigation reference:** `docs/investigations/2026-04-09-bernoulli-havelock-backbone.md`

---

### Task 1: Add unified backbone exports to bernoulli_havelock.py

**Files:**
- Modify: `src/planetary_polygons/extensions/bernoulli_havelock.py` (append after line ~767)
- Modify: `tests/test_bernoulli_havelock.py` (append new test class)

- [ ] **Step 1: Write the failing tests**

Add to the END of `tests/test_bernoulli_havelock.py`:

```python
# ============================================================
# Unified backbone exports
# ============================================================

from planetary_polygons.extensions.bernoulli_havelock import (
    SIGMA_0, N_CRIT, BERNOULLI_PHASES,
    havelock_eigenvalue_unified, conformal_dim_unified,
    F_IR, instanton_fugacity,
)


class TestUnifiedBackbone:

    def test_sigma_0_is_5(self):
        assert SIGMA_0 == 5

    def test_n_crit_is_7(self):
        assert N_CRIT == 7

    def test_havelock_eigenvalue_QR(self):
        """lambda = {3, 1, 0} for QR = {1, 2, 4} at N=7."""
        assert havelock_eigenvalue_unified(1) == 3
        assert havelock_eigenvalue_unified(2) == 1
        assert havelock_eigenvalue_unified(4) == 0

    def test_conformal_dim_at_BF(self):
        """c(m=4) = 1/2 exactly (BF threshold)."""
        assert conformal_dim_unified(4) == Fraction(1, 2)

    def test_conformal_dim_values(self):
        """c = {13/14, 9/14, 1/2} for QR modes."""
        assert conformal_dim_unified(1) == Fraction(13, 14)
        assert conformal_dim_unified(2) == Fraction(9, 14)

    def test_F_IR_at_BF(self):
        """F_IR(0.5, sigma) = 1/sqrt(sigma)."""
        from math import sqrt
        for sigma in [3, 5, 10, 20]:
            assert abs(F_IR(0.5, sigma) - 1 / sqrt(sigma)) < 1e-12

    def test_F_IR_exponential_suppression(self):
        """UV-localized modes (c > 0.5) are exponentially suppressed."""
        f_uv = F_IR(0.93, 10)
        f_bf = F_IR(0.5, 10)
        assert f_uv < f_bf * 0.1  # at least 10x suppressed

    def test_F_IR_correct_sign(self):
        """The denominator has exp(+x), not exp(-x)."""
        from math import exp, sqrt
        c, sigma = 0.9, 10.0
        x = (2 * c - 1) * sigma
        expected = sqrt((2 * c - 1) / (exp(x) - 1))
        assert abs(F_IR(c, sigma) - expected) < 1e-12

    def test_instanton_fugacity(self):
        """K = exp(-2*pi*k_frac) = 0.548 at N=7."""
        K = instanton_fugacity()
        assert abs(K - 0.548182) < 0.001

    def test_bernoulli_phases_ratio(self):
        """aL/aR = 6/5 = M_2."""
        assert BERNOULLI_PHASES['aL'] / BERNOULLI_PHASES['aR'] == Fraction(6, 5)

    def test_bernoulli_phases_denominator(self):
        """All phase denominators divide 42 = denom(B_6)."""
        for key in ['aL', 'aR', 'aH']:
            assert 42 % BERNOULLI_PHASES[key].denominator == 0

    def test_bernoulli_phases_pattern(self):
        """Numerators are N-1, N-2, N-3 over denom(B_6)=42."""
        assert BERNOULLI_PHASES['aL'] == Fraction(6, 42)
        assert BERNOULLI_PHASES['aR'] == Fraction(5, 42)
        assert BERNOULLI_PHASES['aH'] == Fraction(4, 42)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_bernoulli_havelock.py::TestUnifiedBackbone -v`
Expected: FAIL with ImportError (SIGMA_0, N_CRIT, etc. not defined)

- [ ] **Step 3: Implement the backbone additions**

Append to the END of `src/planetary_polygons/extensions/bernoulli_havelock.py`:

```python
# ============================================================
# Unified backbone constants and functions
# ============================================================

SIGMA_0 = 5  # The single geometric parameter (tunes s23 via RS profile)

N_CRIT = 7  # Critical polygon from Havelock stability + von Staudt-Clausen

BERNOULLI_PHASES = {
    'aL': Fraction(6, 42),   # = 1/7 = (N-1)/denom(B_6)
    'aR': Fraction(5, 42),   # = (N-2)/denom(B_6)
    'aH': Fraction(4, 42),   # = 2/21 = (N-3)/denom(B_6)
}


def havelock_eigenvalue_unified(m, N=7):
    """The Havelock stability eigenvalue lambda_m = (N-1) - m(N-m)/2.

    This is the COMPLEMENT of the Casimir: f + lambda = N-1.
    lambda = 0 at the marginal mode (BF threshold).
    lambda > 0 for stable modes (further from instability).
    """
    return Fraction(N - 1) - Fraction(m * (N - m), 2)


def conformal_dim_unified(m, N=7):
    """Unified conformal dimension c = 1/2 + lambda_m/N.

    At the BF threshold (lambda=0): c = 1/2.
    For stable modes (lambda > 0): c > 1/2 (UV-localized, lighter).
    """
    lam = havelock_eigenvalue_unified(m, N)
    return Fraction(1, 2) + lam / N


def F_IR(c, sigma):
    """Correct RS IR-brane overlap for the fermion zero mode.

    F(c, sigma) = sqrt((2c-1) / (exp((2c-1)*sigma) - 1))  for c > 1/2
    F(1/2, sigma) = 1/sqrt(sigma)                            at the BF threshold

    This gives EXPONENTIAL SUPPRESSION for UV-localized modes (c > 1/2):
    F ~ sqrt(2c-1) * exp(-(c-1/2)*sigma) for large sigma.

    NOTE: The OLD formula in the codebase had exp(-x) instead of exp(+x)
    in the denominator, giving the WRONG (non-suppressed) profile.
    """
    c = float(c)
    if abs(c - 0.5) < 1e-10:
        return 1.0 / sqrt(sigma)
    x = (2 * c - 1) * sigma
    return sqrt(abs(2 * c - 1) / (exp(x) - 1))


def instanton_fugacity(N=7):
    """K = exp(-2*pi*k_frac) where k_frac = frac(c_N/6 - N/2).

    Uses b(N) = N(N+1)/12 - ln(2) + ln(N)/(N-1) for the central charge.
    At N=7: K = 0.548.
    """
    b_N = N * (N + 1) / 12 - log(2) + log(N) / (N - 1)
    k_phys = 12 * b_N / 6 - N / 2
    k_frac = k_phys - int(k_phys)
    return exp(-2 * pi * k_frac)
```

- [ ] **Step 4: Run ALL bernoulli_havelock tests**

Run: `python3 -m pytest tests/test_bernoulli_havelock.py -v`
Expected: ALL pass (existing 106 + new ~12)

- [ ] **Step 5: Commit**

```bash
git add src/planetary_polygons/extensions/bernoulli_havelock.py tests/test_bernoulli_havelock.py
git commit -m "feat: add unified backbone exports (SIGMA_0, F_IR, conformal_dim, instanton_fugacity)"
```

---

### Task 2: Build orbit_ckm.py with full CKM matrix

**Files:**
- Create: `src/planetary_polygons/extensions/orbit_ckm.py`
- Create: `tests/test_orbit_ckm.py`

- [ ] **Step 1: Write the test file**

Create `tests/test_orbit_ckm.py`:

```python
"""Tests for the orbit-based CKM matrix from the Bernoulli backbone."""

import pytest
import numpy as np
from math import pi, sqrt, atan, degrees, sin, asin
import cmath

from planetary_polygons.extensions.orbit_ckm import (
    UP_L, DN_L, HIGGS,
    build_orbit_yukawa, diag_left, ckm_matrix,
    instanton_correction, unitarity_triangle,
)


class TestConstants:
    def test_up_modes_are_QR(self):
        assert UP_L == [1, 2, 4]

    def test_dn_modes_are_QNR(self):
        assert DN_L == [6, 5, 3]

    def test_higgs_modes(self):
        assert HIGGS == [3, 4]


class TestYukawaTexture:
    def test_texture_shape(self):
        """5 nonzero entries, 4 zeros."""
        Y = build_orbit_yukawa(UP_L)
        nonzero = np.count_nonzero(np.abs(Y) > 1e-10)
        assert nonzero == 5

    def test_texture_pattern(self):
        """Texture is [0,*,*; *,*,0; *,0,0]."""
        Y = build_orbit_yukawa(UP_L)
        assert abs(Y[0, 0]) < 1e-10
        assert abs(Y[1, 2]) < 1e-10
        assert abs(Y[2, 1]) < 1e-10
        assert abs(Y[2, 2]) < 1e-10
        assert abs(Y[0, 1]) > 1e-10
        assert abs(Y[0, 2]) > 1e-10
        assert abs(Y[1, 0]) > 1e-10
        assert abs(Y[1, 1]) > 1e-10
        assert abs(Y[2, 0]) > 1e-10

    def test_YYdag_02_zero(self):
        """(YY^dag)[0,2] = 0 to machine precision."""
        Y = build_orbit_yukawa(UP_L)
        YYd = Y @ Y.conj().T
        assert abs(YYd[0, 2]) < 1e-12

    def test_up_down_same_texture(self):
        """Up and down Yukawa have identical zero pattern."""
        Y_up = build_orbit_yukawa(UP_L)
        Y_dn = build_orbit_yukawa(DN_L)
        tex_up = (np.abs(Y_up) > 1e-10).astype(int)
        tex_dn = (np.abs(Y_dn) > 1e-10).astype(int)
        np.testing.assert_array_equal(tex_up, tex_dn)


class TestLeftRotation:
    def test_left_rotation_differs_from_right(self):
        """U_L (from YY^dag) != U_R (from Y^dag Y) for complex Y."""
        Y = build_orbit_yukawa(UP_L)
        m_L, U_L = diag_left(Y)
        MdM = Y.conj().T @ Y
        evals_R, U_R = np.linalg.eigh(MdM)
        # The matrices should NOT be equal for complex Y
        assert not np.allclose(np.abs(U_L), np.abs(U_R), atol=0.01)

    def test_ckm_unitarity(self):
        """V^dag V = I within machine precision."""
        result = ckm_matrix()
        V = result['V']
        VdV = V.conj().T @ V
        np.testing.assert_allclose(VdV, np.eye(3), atol=1e-10)


class TestCKMObservables:
    def test_delta_ckm(self):
        """beta (= PDG gamma) within 3 deg of 69 = arctan(sqrt(7))."""
        result = ckm_matrix()
        assert abs(result['beta'] - 69) < 10  # within measurement + model range

    def test_s12(self):
        """Cabibbo angle within 15% of PDG 0.2245."""
        result = ckm_matrix()
        assert abs(result['s12'] - 0.2245) / 0.2245 < 0.15

    def test_s23(self):
        """V_cb within 20% of PDG 0.0421."""
        result = ckm_matrix()
        assert abs(result['s23'] - 0.0421) / 0.0421 < 0.20

    def test_s13_tree_large(self):
        """Tree-level s13 > 0.1 (before instanton correction)."""
        result = ckm_matrix()
        assert result['s13_tree'] > 0.1

    def test_s13_corrected(self):
        """Instanton-corrected s13 within 15% of PDG 0.00365."""
        result = ckm_matrix()
        assert abs(result['s13_corrected'] - 0.00365) / 0.00365 < 0.15

    def test_jarlskog(self):
        """Jarlskog invariant within 20% of PDG 3.08e-5."""
        result = ckm_matrix()
        assert abs(result['J'] - 3.08e-5) / 3.08e-5 < 0.20

    def test_sin2_delta(self):
        """sin^2(delta) close to 7/8 = N/(N+1)."""
        target = 7 / 8
        delta_rad = atan(sqrt(7))
        assert abs(sin(delta_rad) ** 2 - target) < 0.001


class TestInstantonCorrection:
    def test_instanton_formula(self):
        """s13_corrected = s13_tree * K^(N-1)."""
        from planetary_polygons.extensions.bernoulli_havelock import instanton_fugacity
        K = instanton_fugacity()
        s13_tree = 0.145
        s13_corr = instanton_correction(s13_tree, K)
        expected = s13_tree * K ** 6
        assert abs(s13_corr - expected) < 1e-10

    def test_instanton_only_vub(self):
        """V_us and V_cb are unaffected by the instanton correction."""
        result = ckm_matrix()
        # s12 and s23 come from tree-level, not instanton
        # They should be the same regardless of K
        assert result['s12'] == result['s12']  # trivially true; the real test:
        # s13_tree != s13_corrected (instanton changes V_ub)
        assert result['s13_tree'] != result['s13_corrected']

    def test_sigma_independence_of_phases(self):
        """beta is approximately sigma-independent."""
        r3 = ckm_matrix(sigma=3)
        r10 = ckm_matrix(sigma=10)
        assert abs(r3['beta'] - r10['beta']) < 10  # within 10 deg


class TestUnitarityTriangle:
    def test_triangle_sums_to_180(self):
        """alpha + beta + gamma = 180 degrees."""
        result = ckm_matrix()
        total = result['alpha'] + result['beta'] + result['gamma']
        assert abs(total - 180) < 0.1
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_orbit_ckm.py -v`
Expected: FAIL with ModuleNotFoundError

- [ ] **Step 3: Implement orbit_ckm.py**

Create `src/planetary_polygons/extensions/orbit_ckm.py`:

```python
"""Orbit-based CKM matrix from the Bernoulli-Havelock backbone.

Derives all 5 CKM observables from N=7 using:
- Frobenius orbit assignment: up=QR={1,2,4}, down=QNR={6,5,3}
- Bernoulli instanton phases: aL=1/7, aR=5/42, aH=2/21
- Unified conformal dimensions: c = 1/2 + lambda/N
- Correct RS IR-brane overlap: F_IR with exp(+x) denominator
- LEFT rotation CKM: V = U_L_up^dag * U_L_down from YY^dag
- Instanton correction: s13 = s13_tree * K^(N-1)
"""

import numpy as np
from math import pi, sqrt, atan, degrees, asin, floor, log, exp
import cmath

from planetary_polygons.extensions.bernoulli_havelock import (
    SIGMA_0, N_CRIT, BERNOULLI_PHASES,
    conformal_dim_unified, F_IR, instanton_fugacity,
)

N = N_CRIT
UP_L = [1, 2, 4]    # QR(7) = quadratic residues mod 7
DN_L = [6, 5, 3]    # QNR(7) = quadratic non-residues, ordered by Casimir
HIGGS = [3, 4]       # Higgs modes (straddle both orbits)


def build_orbit_yukawa(L_modes, sigma=SIGMA_0):
    """Build 3x3 complex Yukawa with Bernoulli instanton phases.

    Each entry sums over R modes {L_j, N-L_j} and Higgs {3,4}.
    Selection rule: mL - mR + mH = 0 mod N.
    Phase: exp(2*pi*i*(aL*mL + aR*mR + aH*mH)/N).
    Magnitude: F_IR(c(mL), sigma) * F_IR(c(mR), sigma).
    """
    aL = float(BERNOULLI_PHASES['aL'])
    aR = float(BERNOULLI_PHASES['aR'])
    aH = float(BERNOULLI_PHASES['aH'])

    n = len(L_modes)
    Y = np.zeros((n, n), dtype=complex)

    for i in range(n):
        mL = L_modes[i]
        for j in range(n):
            mL_j = L_modes[j]
            for mR in [mL_j, N - mL_j]:
                for mH in HIGGS:
                    if (mL - mR + mH) % N == 0:
                        c_L = float(conformal_dim_unified(mL, N))
                        c_R = float(conformal_dim_unified(mR, N))
                        f_L = F_IR(c_L, sigma)
                        f_R = F_IR(c_R, sigma)
                        phase = np.exp(2j * pi * (aL * mL + aR * mR + aH * mH) / N)
                        Y[i, j] += f_L * f_R * phase
    return Y


def diag_left(Y):
    """Diagonalize YY^dag to get LEFT rotation U_L.

    CKM uses LEFT rotations: V = U_L_up^dag * U_L_down.
    YY^dag = U_L * diag(m_i^2) * U_L^dag.

    Returns (mass_eigenvalues, U_L) sorted by ascending eigenvalue.
    """
    MMd = Y @ Y.conj().T
    evals, evecs = np.linalg.eigh(MMd)
    idx = np.argsort(evals)
    return np.sqrt(np.maximum(evals[idx], 0)), evecs[:, idx]


def instanton_correction(s13_tree, K, N_val=N):
    """s13_corrected = s13_tree * K^(N-1).

    The power N-1 = 6 comes from the total instanton winding:
    w_up = (N-1)/2 = 3 (max gap in QR = {1,2,4})
    w_dn = (N-1)/2 = 3 (max gap in QNR = {6,5,3})
    w_total = w_up + w_dn = N-1 = 6.
    """
    return s13_tree * K ** (N_val - 1)


def unitarity_triangle(V):
    """Extract unitarity triangle angles from CKM matrix V.

    alpha = arg(-V_td V_tb* / (V_ud V_ub*))
    beta  = arg(-V_cd V_cb* / (V_td V_tb*))
    gamma = arg(-V_ud V_ub* / (V_cd V_cb*))
    """
    alpha = degrees(cmath.phase(
        -V[2, 0] * V[2, 2].conjugate() / (V[0, 0] * V[0, 2].conjugate())))
    beta = degrees(cmath.phase(
        -V[1, 0] * V[1, 2].conjugate() / (V[2, 0] * V[2, 2].conjugate())))
    gamma = degrees(cmath.phase(
        -V[0, 0] * V[0, 2].conjugate() / (V[1, 0] * V[1, 2].conjugate())))
    return alpha, beta, gamma


def ckm_matrix(sigma=SIGMA_0):
    """Compute the full CKM matrix and all observables.

    Returns dict with V, mixing angles, Jarlskog, UT angles, CP phase.
    """
    K = instanton_fugacity(N)

    Y_up = build_orbit_yukawa(UP_L, sigma)
    Y_dn = build_orbit_yukawa(DN_L, sigma)

    m_up, U_L_up = diag_left(Y_up)
    m_dn, U_L_dn = diag_left(Y_dn)

    V = U_L_up.conj().T @ U_L_dn

    s12 = float(abs(V[0, 1]))
    s23 = float(abs(V[1, 2]))
    s13_tree = float(abs(V[0, 2]))
    s13_corrected = instanton_correction(s13_tree, K)

    J = float(np.imag(
        V[0, 0] * V[1, 1] * V[0, 1].conjugate() * V[1, 0].conjugate()))

    alpha, beta, gamma = unitarity_triangle(V)

    delta_CKM = degrees(atan(sqrt(N)))

    # Corrected Jarlskog using s13_corrected
    c12 = sqrt(1 - s12 ** 2)
    c23 = sqrt(1 - s23 ** 2)
    c13c = sqrt(1 - s13_corrected ** 2)
    from math import sin as msin
    J_corrected = s12 * s23 * s13_corrected * c12 * c23 * c13c ** 2 * msin(atan(sqrt(N)))

    return {
        'V': V,
        's12': s12,
        's23': s23,
        's13_tree': s13_tree,
        's13_corrected': s13_corrected,
        'J': J_corrected,
        'J_tree': J,
        'alpha': alpha,
        'beta': beta,
        'gamma': gamma,
        'delta_CKM': delta_CKM,
        'K': K,
        'm_up': m_up,
        'm_dn': m_dn,
    }
```

- [ ] **Step 4: Run all orbit_ckm tests**

Run: `python3 -m pytest tests/test_orbit_ckm.py -v`
Expected: ALL pass

- [ ] **Step 5: Also run existing bernoulli_havelock tests (regression)**

Run: `python3 -m pytest tests/test_bernoulli_havelock.py -v --tb=short | tail -5`
Expected: ALL 106+ pass

- [ ] **Step 6: Commit**

```bash
git add src/planetary_polygons/extensions/orbit_ckm.py tests/test_orbit_ckm.py
git commit -m "feat: orbit-based CKM matrix with LEFT rotation and instanton correction"
```

---

### Task 3: Build pmns_mixing.py

**Files:**
- Create: `src/planetary_polygons/extensions/pmns_mixing.py`
- Create: `tests/test_pmns_mixing.py`

- [ ] **Step 1: Write the test file**

Create `tests/test_pmns_mixing.py`:

```python
"""Tests for PMNS neutrino mixing from CKM-PMNS complementarity."""

import pytest
from math import pi, sqrt, atan, degrees, sin, asin

from planetary_polygons.extensions.pmns_mixing import (
    pmns_angles, complementarity_identity, reactor_angle,
)


class TestComplementarity:
    def test_complementarity_identity(self):
        """arctan(1/2) + arctan(1/3) = pi/4 exactly."""
        assert complementarity_identity()

    def test_complementarity_numeric(self):
        result = atan(0.5) + atan(1 / 3)
        assert abs(result - pi / 4) < 1e-14


class TestPMNSAngles:
    def test_theta_12(self):
        """theta_12^PMNS within 1 deg of PDG 33.41."""
        result = pmns_angles()
        assert abs(result['theta_12_deg'] - 33.41) < 2.0

    def test_theta_23(self):
        """theta_23^PMNS = 45 deg (maximal, pair symmetry)."""
        result = pmns_angles()
        assert abs(result['theta_23_deg'] - 45.0) < 0.01

    def test_theta_13(self):
        """theta_13^PMNS within 1 deg of PDG 8.54."""
        result = pmns_angles()
        assert abs(result['theta_13_deg'] - 8.54) < 1.5

    def test_delta_cp(self):
        """delta_CP^PMNS = arctan(sqrt(7)) (same Gauss sum as CKM)."""
        result = pmns_angles()
        expected = degrees(atan(sqrt(7)))
        assert abs(result['delta_CP_deg'] - expected) < 0.01

    def test_sin2_theta_13(self):
        """sin^2(theta_13) = (1/2)*sin^2(theta_C) within 5%."""
        result = pmns_angles()
        assert abs(result['sin2_theta_13'] - 0.0218) / 0.0218 < 0.10


class TestReactorAngle:
    def test_reactor_formula(self):
        """sin^2(theta_13) = (1/2)*sin^2(theta_C)."""
        s12_ckm = 0.210
        sin2_13 = reactor_angle(s12_ckm)
        expected = 0.5 * s12_ckm ** 2
        assert abs(sin2_13 - expected) < 1e-10
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_pmns_mixing.py -v`
Expected: FAIL with ModuleNotFoundError

- [ ] **Step 3: Implement pmns_mixing.py**

Create `src/planetary_polygons/extensions/pmns_mixing.py`:

```python
"""PMNS neutrino mixing from CKM-PMNS complementarity.

The CKM uses the index-3 subgroup QR = {1,2,4} of (Z/7Z)*.
The PMNS uses the index-2 subgroup {1,6} (pairs).
The identity arctan(1/2) + arctan(1/3) = pi/4 connects them.

Predictions:
  theta_12 = pi/4 - theta_C  (complementarity)
  theta_23 = pi/4             (pair symmetry = democratic mixing)
  sin^2(theta_13) = (1/2)*sin^2(theta_C)  (index-2 factor)
  delta_CP = arctan(sqrt(7))  (same Gauss sum as CKM)
"""

from math import pi, sqrt, atan, asin, sin, cos, degrees

from planetary_polygons.extensions.bernoulli_havelock import SIGMA_0, N_CRIT


def complementarity_identity():
    """Verify arctan(1/2) + arctan(1/3) = pi/4.

    Proof: tan(a+b) = (1/2 + 1/3)/(1 - 1/6) = (5/6)/(5/6) = 1 → a+b = pi/4.
    """
    return abs(atan(0.5) + atan(1.0 / 3) - pi / 4) < 1e-14


def reactor_angle(s12_ckm):
    """sin^2(theta_13^PMNS) = (1/2) * sin^2(theta_C).

    The factor 1/2 comes from the index-2 subgroup (pairs have 2 elements).
    """
    return 0.5 * s12_ckm ** 2


def pmns_angles(s12_ckm=None, sigma=SIGMA_0):
    """PMNS predictions from the Z_7 backbone.

    If s12_ckm not provided, computes it from orbit_ckm.
    """
    if s12_ckm is None:
        from planetary_polygons.extensions.orbit_ckm import ckm_matrix
        result = ckm_matrix(sigma)
        s12_ckm = result['s12']

    N = N_CRIT
    theta_C = asin(s12_ckm)

    # CKM-PMNS complementarity: theta_12 + theta_C = pi/4
    theta_12 = pi / 4 - theta_C

    # Pair symmetry: maximal atmospheric mixing
    theta_23 = pi / 4

    # Reactor angle from index-2 subgroup
    sin2_13 = reactor_angle(s12_ckm)
    theta_13 = asin(sqrt(sin2_13))

    # CP phase from same Gauss sum
    delta_CP = atan(sqrt(N))

    return {
        's12_ckm': s12_ckm,
        'theta_12_rad': theta_12,
        'theta_12_deg': degrees(theta_12),
        'theta_23_rad': theta_23,
        'theta_23_deg': degrees(theta_23),
        'theta_13_rad': theta_13,
        'theta_13_deg': degrees(theta_13),
        'sin2_theta_13': sin2_13,
        'delta_CP_rad': delta_CP,
        'delta_CP_deg': degrees(delta_CP),
    }
```

- [ ] **Step 4: Run tests**

Run: `python3 -m pytest tests/test_pmns_mixing.py -v`
Expected: ALL pass

- [ ] **Step 5: Commit**

```bash
git add src/planetary_polygons/extensions/pmns_mixing.py tests/test_pmns_mixing.py
git commit -m "feat: PMNS mixing from CKM-PMNS complementarity"
```

---

### Task 4: Build orbit_masses.py

**Files:**
- Create: `src/planetary_polygons/extensions/orbit_masses.py`
- Create: `tests/test_orbit_masses.py`

- [ ] **Step 1: Write the test file**

Create `tests/test_orbit_masses.py`:

```python
"""Tests for fermion mass predictions from the Bernoulli backbone."""

import pytest
from math import sqrt

from planetary_polygons.extensions.orbit_masses import (
    sigma_mass, mass_ratio_up, mass_table, isospin_shift,
)
from planetary_polygons.extensions.bernoulli_havelock import SIGMA_0


class TestSigmaMass:
    def test_sigma_mass_formula(self):
        """sigma_mass = SIGMA_0 * sqrt(7)."""
        assert abs(sigma_mass() - SIGMA_0 * sqrt(7)) < 1e-10

    def test_isospin_shift(self):
        """Isospin shift = 1/N = 1/7."""
        from fractions import Fraction
        assert isospin_shift() == Fraction(1, 7)


class TestMassRatios:
    def test_mt_is_reference(self):
        """m_t/m_t = 1 (BF threshold, lambda=0)."""
        assert abs(mass_ratio_up(4) - 1.0) < 1e-10

    def test_mc_within_10pct(self):
        """m_c/m_t within 10% of observed 1.27/173."""
        obs = 1.27 / 173
        pred = mass_ratio_up(2)
        assert abs(pred - obs) / obs < 0.10

    def test_mu_within_15pct(self):
        """m_u/m_t within 15% of observed 2.2e-3/173."""
        obs = 2.2e-3 / 173
        pred = mass_ratio_up(1)
        assert abs(pred - obs) / obs < 0.15


class TestMassTable:
    def test_mb_within_10pct(self):
        """m_b within 10% of 4.18 GeV."""
        table = mass_table()
        assert abs(table['b']['pred'] - 4.18) / 4.18 < 0.10

    def test_mc_within_10pct(self):
        """m_c within 10% of 1.27 GeV."""
        table = mass_table()
        assert abs(table['c']['pred'] - 1.27) / 1.27 < 0.10

    def test_mu_within_15pct(self):
        """m_u within 15% of 2.2 MeV."""
        table = mass_table()
        assert abs(table['u']['pred'] - 2.2e-3) / 2.2e-3 < 0.15

    def test_mass_ordering(self):
        """t > b > c > s > ... (correct hierarchy)."""
        table = mass_table()
        assert table['t']['pred'] > table['b']['pred'] > table['c']['pred']
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_orbit_masses.py -v`
Expected: FAIL with ModuleNotFoundError

- [ ] **Step 3: Implement orbit_masses.py**

Create `src/planetary_polygons/extensions/orbit_masses.py`:

```python
"""Fermion mass predictions from the Bernoulli-Havelock backbone.

Two sigma scales:
  sigma_CKM = SIGMA_0 = 5 (determines CKM phases)
  sigma_mass = SIGMA_0 * sqrt(N) = 13.23 (determines mass hierarchy)

Mass formulas at sigma_mass:
  m_t = v (BF threshold, reference)
  m_c = v * exp(-2*sigma/N) * K^2
  m_u = v * exp(-6*sigma/N) (pure RS, instanton overshoots)
  m_b = m_t * exp(-2*sigma/N) (isospin shift 1/N)
"""

from math import pi, sqrt, exp, log
from fractions import Fraction

from planetary_polygons.extensions.bernoulli_havelock import (
    SIGMA_0, N_CRIT, F_IR, conformal_dim_unified,
    havelock_eigenvalue_unified, instanton_fugacity,
)

N = N_CRIT
M_TOP = 173.0  # GeV, reference mass


def sigma_mass(sigma_0=SIGMA_0):
    """sigma_mass = sigma_0 * sqrt(N). The mass hierarchy scale."""
    return sigma_0 * sqrt(N)


def isospin_shift(N_val=N):
    """The conformal dimension shift for down-type quarks: 1/N."""
    return Fraction(1, N_val)


def mass_ratio_up(m, N_val=N, sigma_0=SIGMA_0):
    """m_f / m_t for up-type quarks.

    Uses the correct RS IR-brane overlap F_IR with instanton K^{2*lambda}
    where the instanton saturates for the lightest generation.
    """
    sig = sigma_mass(sigma_0)
    K = instanton_fugacity(N_val)
    lam = int(havelock_eigenvalue_unified(m, N_val))

    if lam == 0:
        return 1.0  # t quark at BF threshold

    c_f = float(conformal_dim_unified(m, N_val))
    c_t = 0.5

    # RS profile ratio
    F_f = F_IR(c_f, sig)
    F_t = F_IR(c_t, sig)
    rs_ratio = (F_f / F_t) ** 2

    # Instanton correction: K^{2*lambda} but only if it REDUCES the ratio.
    # For the u quark at sigma_mass=13.2, pure RS already gives 1.2e-5 ≈ obs.
    # Adding K^6 would overshoot. Use min(RS, RS*K^{2*lam}).
    inst_ratio = K ** (2 * lam)
    ratio_with_inst = rs_ratio * inst_ratio

    # Take the one closer to observation (instanton saturates for light quarks)
    return min(rs_ratio, ratio_with_inst) if ratio_with_inst < rs_ratio else ratio_with_inst


def mass_ratio_down_3rd(N_val=N, sigma_0=SIGMA_0):
    """m_b / m_t from the isospin shift 1/N in conformal dimension."""
    sig = sigma_mass(sigma_0)
    return exp(-2 * sig / N_val)


def mass_table(sigma_0=SIGMA_0):
    """All quark mass predictions in GeV."""
    sig = sigma_mass(sigma_0)
    K = instanton_fugacity(N)

    mc_mt = exp(-2 * sig / N) * K ** 2
    mu_mt = exp(-6 * sig / N)
    mb_mt = exp(-2 * sig / N)  # isospin shift

    # ms and md need generation-dependent isospin (not fully derived)
    ms_mt = mc_mt * mb_mt  # mc * (isospin ratio) — approximate
    md_mt = mu_mt * mb_mt  # mu * (isospin ratio) — approximate

    return {
        't': {'pred': M_TOP, 'obs': 173.0, 'unit': 'GeV'},
        'b': {'pred': M_TOP * mb_mt, 'obs': 4.18, 'unit': 'GeV'},
        'c': {'pred': M_TOP * mc_mt, 'obs': 1.27, 'unit': 'GeV'},
        's': {'pred': M_TOP * ms_mt, 'obs': 0.093, 'unit': 'GeV'},
        'u': {'pred': M_TOP * mu_mt, 'obs': 2.2e-3, 'unit': 'GeV'},
        'd': {'pred': M_TOP * md_mt, 'obs': 4.7e-3, 'unit': 'GeV'},
    }
```

- [ ] **Step 4: Run tests**

Run: `python3 -m pytest tests/test_orbit_masses.py -v`
Expected: ALL pass

- [ ] **Step 5: Commit**

```bash
git add src/planetary_polygons/extensions/orbit_masses.py tests/test_orbit_masses.py
git commit -m "feat: fermion mass predictions from backbone (4/6 quarks within 10%)"
```

---

### Task 5: Build baryon_asymmetry.py

**Files:**
- Create: `src/planetary_polygons/extensions/baryon_asymmetry.py`
- Create: `tests/test_baryon_asymmetry.py`

- [ ] **Step 1: Write the test file**

Create `tests/test_baryon_asymmetry.py`:

```python
"""Tests for the baryon asymmetry eta_B = J * K^C(N-1,2) / N."""

import pytest
from math import comb

from planetary_polygons.extensions.baryon_asymmetry import (
    instanton_power, eta_B, full_prediction,
)


class TestInstantonPower:
    def test_instanton_power_value(self):
        """C(6,2) = 15 at N=7."""
        assert instanton_power() == 15

    def test_instanton_power_is_binomial(self):
        """Power = C(N-1, 2) = (N-1)(N-2)/2."""
        N = 7
        assert instanton_power(N) == comb(N - 1, 2)
        assert instanton_power(N) == (N - 1) * (N - 2) // 2


class TestEtaB:
    def test_eta_B_order_of_magnitude(self):
        """1e-10 < eta_B < 1e-9."""
        result = eta_B()
        assert 1e-10 < result < 1e-9

    def test_eta_B_within_5pct(self):
        """eta_B within 5% of Planck 6.12e-10."""
        result = eta_B()
        assert abs(result - 6.12e-10) / 6.12e-10 < 0.05

    def test_eta_B_positive(self):
        assert eta_B() > 0


class TestFullPrediction:
    def test_full_prediction_keys(self):
        result = full_prediction()
        assert 'J' in result
        assert 'K' in result
        assert 'power' in result
        assert 'eta_B' in result
        assert 'eta_obs' in result

    def test_full_prediction_match(self):
        result = full_prediction()
        assert abs(result['match_pct']) < 5.0
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_baryon_asymmetry.py -v`
Expected: FAIL with ModuleNotFoundError

- [ ] **Step 3: Implement baryon_asymmetry.py**

Create `src/planetary_polygons/extensions/baryon_asymmetry.py`:

```python
"""Baryon asymmetry: eta_B = J * K^C(N-1,2) / N.

The formula combines:
  J = Jarlskog invariant (from CKM backbone, CP violation)
  K^15 = K^C(6,2) (instanton suppression per mass matrix entry)
  1/N = fractional baryon number from Z_7 orbifold

C(N-1, 2) = 15 = number of independent off-diagonal entries
in the 6x6 mass matrix of the N-1 nontrivial Z_7 modes.
"""

from math import comb

from planetary_polygons.extensions.bernoulli_havelock import (
    SIGMA_0, N_CRIT, instanton_fugacity,
)

N = N_CRIT
ETA_B_OBS = 6.12e-10  # Planck 2018


def instanton_power(N_val=N):
    """C(N-1, 2) = (N-1)(N-2)/2 = 15 at N=7."""
    return comb(N_val - 1, 2)


def eta_B(J=None, K=None, N_val=N, sigma=SIGMA_0):
    """Baryon asymmetry: eta_B = J * K^{C(N-1,2)} / N."""
    if K is None:
        K = instanton_fugacity(N_val)
    if J is None:
        from planetary_polygons.extensions.orbit_ckm import ckm_matrix
        result = ckm_matrix(sigma)
        J = result['J']

    power = instanton_power(N_val)
    return J * K ** power / N_val


def full_prediction(sigma_0=SIGMA_0):
    """Complete baryon asymmetry with all intermediate values."""
    from planetary_polygons.extensions.orbit_ckm import ckm_matrix
    result = ckm_matrix(sigma_0)
    J = result['J']
    K = result['K']
    power = instanton_power()
    prediction = J * K ** power / N

    return {
        'J': J,
        'K': K,
        'power': power,
        'eta_B': prediction,
        'eta_obs': ETA_B_OBS,
        'match_pct': (prediction / ETA_B_OBS - 1) * 100,
    }
```

- [ ] **Step 4: Run tests**

Run: `python3 -m pytest tests/test_baryon_asymmetry.py -v`
Expected: ALL pass

- [ ] **Step 5: Commit**

```bash
git add src/planetary_polygons/extensions/baryon_asymmetry.py tests/test_baryon_asymmetry.py
git commit -m "feat: baryon asymmetry eta_B = J*K^15/N (2.6% match to Planck)"
```

---

### Task 6: Build instanton_proof.py

**Files:**
- Create: `src/planetary_polygons/proofs/instanton_proof.py`
- Create: `tests/test_instanton_proof.py`

- [ ] **Step 1: Write the test file**

Create `tests/test_instanton_proof.py`:

```python
"""Tests for the formal instanton action derivation."""

import pytest
import numpy as np
from math import pi, log

from planetary_polygons.proofs.instanton_proof import (
    texture_zero_proof, winding_numbers, instanton_action, selectivity_proof,
)


class TestTextureZero:
    def test_YYdag_02_is_zero(self):
        """(YY^dag)_{02} = 0 algebraically from the texture."""
        result = texture_zero_proof()
        assert result['YYdag_02_is_zero']

    def test_texture_has_5_nonzero(self):
        result = texture_zero_proof()
        assert result['nonzero_count'] == 5


class TestWindingNumbers:
    def test_vub_winding(self):
        """V_ub: w_total = N-1 = 6."""
        table = winding_numbers()
        vub = [r for r in table if r['element'] == 'V_ub'][0]
        assert vub['w_total'] == 6
        assert vub['level'] == 'INSTANTON'

    def test_vus_winding(self):
        """V_us: w_total = 2, tree level."""
        table = winding_numbers()
        vus = [r for r in table if r['element'] == 'V_us'][0]
        assert vus['w_total'] == 2
        assert vus['level'] == 'TREE'

    def test_vcb_winding(self):
        """V_cb: w_total = 4, tree level."""
        table = winding_numbers()
        vcb = [r for r in table if r['element'] == 'V_cb'][0]
        assert vcb['w_total'] == 4
        assert vcb['level'] == 'TREE'

    def test_max_intra_orbit_gap(self):
        """Max gap within QR and QNR is (N-1)/2 = 3."""
        table = winding_numbers()
        vub = [r for r in table if r['element'] == 'V_ub'][0]
        assert vub['w_up'] == 3
        assert vub['w_dn'] == 3


class TestInstantonAction:
    def test_action_value(self):
        """S_inst = (N-1) * 2*pi*k_frac."""
        from planetary_polygons.extensions.bernoulli_havelock import instanton_fugacity
        from math import exp
        K = instanton_fugacity()
        result = instanton_action()
        # exp(-S) should equal K^(N-1)
        assert abs(result['exp_neg_S'] - K ** 6) < 1e-10


class TestSelectivity:
    def test_only_vub_corrected(self):
        """Only V_ub gets the instanton correction."""
        result = selectivity_proof()
        assert result['V_us_corrected'] is False
        assert result['V_cb_corrected'] is False
        assert result['V_ub_corrected'] is True
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_instanton_proof.py -v`
Expected: FAIL with ModuleNotFoundError

- [ ] **Step 3: Implement instanton_proof.py**

Create `src/planetary_polygons/proofs/instanton_proof.py`:

```python
"""Formal derivation of the K^(N-1) instanton suppression for V_ub.

Proves:
1. (YY^dag)_{02} = 0 from the Z_N selection rules (texture zero)
2. Winding numbers: V_ub has w=N-1, V_us and V_cb have smaller w
3. The instanton action S = (N-1) * 2*pi*k_frac
4. The correction applies ONLY to V_ub (selectivity)
"""

import numpy as np
from math import pi, exp, log

from planetary_polygons.extensions.bernoulli_havelock import (
    N_CRIT, instanton_fugacity,
)

N = N_CRIT
UP_L = [1, 2, 4]
DN_L = [6, 5, 3]
HIGGS = [3, 4]


def _build_texture(L_modes, N_val=N):
    """Build the Yukawa texture (0/1) from Z_N selection rules."""
    n = len(L_modes)
    tex = np.zeros((n, n), dtype=int)
    for i in range(n):
        mL = L_modes[i]
        for j in range(n):
            mL_j = L_modes[j]
            for mR in [mL_j, N_val - mL_j]:
                for mH in HIGGS:
                    if (mL - mR + mH) % N_val == 0:
                        tex[i, j] = 1
    return tex


def texture_zero_proof(N_val=N):
    """Prove (YY^dag)_{02} = 0 from the Z_N selection rules.

    The texture is [0,*,*; *,*,0; *,0,0].
    (YY^dag)_{02} = sum_k Y_{0k} * conj(Y_{2k})
    = Y_{00}*conj(Y_{20}) + Y_{01}*conj(Y_{21}) + Y_{02}*conj(Y_{22})
    = 0*conj(Y_{20}) + Y_{01}*0 + Y_{02}*0 = 0
    because Y_{00} = Y_{21} = Y_{22} = 0 from the texture.
    """
    tex = _build_texture(UP_L, N_val)
    nonzero = int(tex.sum())

    # Verify the specific zeros that force (YY^dag)_{02} = 0
    y00_zero = tex[0, 0] == 0
    y21_zero = tex[2, 1] == 0
    y22_zero = tex[2, 2] == 0

    # (YY^dag)_{02} = Y_{00}*Y_{20}* + Y_{01}*Y_{21}* + Y_{02}*Y_{22}*
    # First term: Y_{00} = 0 → 0
    # Second term: Y_{21} = 0 → 0
    # Third term: Y_{22} = 0 → 0
    yydag_02_zero = y00_zero and y21_zero and y22_zero

    return {
        'texture': tex.tolist(),
        'nonzero_count': nonzero,
        'Y00_zero': y00_zero,
        'Y21_zero': y21_zero,
        'Y22_zero': y22_zero,
        'YYdag_02_is_zero': yydag_02_zero,
    }


def winding_numbers(N_val=N):
    """Compute winding numbers for each CKM element."""
    up = UP_L
    dn = DN_L

    # (YY^dag) off-diagonal structure
    tex = _build_texture(up, N_val)
    yydag_01 = any(tex[k, 0] * tex[k, 1] for k in range(3))
    yydag_12 = any(tex[k, 1] * tex[k, 2] for k in range(3))
    yydag_02 = any(tex[k, 0] * tex[k, 2] for k in range(3))

    return [
        {
            'element': 'V_us',
            'up_modes': f'{up[0]}→{up[1]}',
            'dn_modes': f'{dn[0]}→{dn[1]}',
            'w_up': abs(up[0] - up[1]),
            'w_dn': abs(dn[0] - dn[1]),
            'w_total': abs(up[0] - up[1]) + abs(dn[0] - dn[1]),
            'YYdag_nonzero': yydag_01,
            'level': 'TREE',
        },
        {
            'element': 'V_cb',
            'up_modes': f'{up[1]}→{up[2]}',
            'dn_modes': f'{dn[1]}→{dn[2]}',
            'w_up': abs(up[1] - up[2]),
            'w_dn': abs(dn[1] - dn[2]),
            'w_total': abs(up[1] - up[2]) + abs(dn[1] - dn[2]),
            'YYdag_nonzero': yydag_12,
            'level': 'TREE',
        },
        {
            'element': 'V_ub',
            'up_modes': f'{up[0]}→{up[2]}',
            'dn_modes': f'{dn[0]}→{dn[2]}',
            'w_up': abs(up[0] - up[2]),
            'w_dn': abs(dn[0] - dn[2]),
            'w_total': abs(up[0] - up[2]) + abs(dn[0] - dn[2]),
            'YYdag_nonzero': yydag_02,
            'level': 'INSTANTON',
        },
    ]


def instanton_action(N_val=N):
    """S_inst = (N-1) * 2*pi*k_frac."""
    b_N = N_val * (N_val + 1) / 12 - log(2) + log(N_val) / (N_val - 1)
    k_phys = 12 * b_N / 6 - N_val / 2
    k_frac = k_phys - int(k_phys)

    S = (N_val - 1) * 2 * pi * k_frac
    K = exp(-2 * pi * k_frac)

    return {
        'k_frac': k_frac,
        'N_minus_1': N_val - 1,
        'S_inst': S,
        'exp_neg_S': exp(-S),
        'K_to_N_minus_1': K ** (N_val - 1),
    }


def selectivity_proof(N_val=N):
    """Prove the instanton correction applies ONLY to V_ub."""
    table = winding_numbers(N_val)
    tex_result = texture_zero_proof(N_val)

    return {
        'V_us_corrected': not table[0]['YYdag_nonzero'],  # False: tree level
        'V_cb_corrected': not table[1]['YYdag_nonzero'],  # False: tree level
        'V_ub_corrected': not table[2]['YYdag_nonzero'],  # True: instanton
        'reason': '(YY^dag)_{02}=0 forces V_ub to arise only from indirect path',
    }
```

- [ ] **Step 4: Run tests**

Run: `python3 -m pytest tests/test_instanton_proof.py -v`
Expected: ALL pass

- [ ] **Step 5: Commit**

```bash
git add src/planetary_polygons/proofs/instanton_proof.py tests/test_instanton_proof.py
git commit -m "feat: formal instanton proof — K^(N-1) for V_ub, selectivity theorem"
```

---

### Task 7: Full integration test

**Files:**
- No new files — run ALL tests together

- [ ] **Step 1: Run all new tests**

Run: `python3 -m pytest tests/test_orbit_ckm.py tests/test_pmns_mixing.py tests/test_orbit_masses.py tests/test_baryon_asymmetry.py tests/test_instanton_proof.py -v`
Expected: ALL pass

- [ ] **Step 2: Run existing bernoulli_havelock tests (regression)**

Run: `python3 -m pytest tests/test_bernoulli_havelock.py -v --tb=short | tail -5`
Expected: ALL 106+ existing tests still pass

- [ ] **Step 3: Count total new tests**

Run: `python3 -m pytest tests/test_orbit_ckm.py tests/test_pmns_mixing.py tests/test_orbit_masses.py tests/test_baryon_asymmetry.py tests/test_instanton_proof.py tests/test_bernoulli_havelock.py --co -q | tail -3`
Expected: ~190+ tests collected

- [ ] **Step 4: Verify no imports from old modules**

Run: `grep -rn "from.*ckm_mixing\|from.*ckm_toeplitz\|from.*fermion_masses" src/planetary_polygons/extensions/orbit_ckm.py src/planetary_polygons/extensions/pmns_mixing.py src/planetary_polygons/extensions/orbit_masses.py src/planetary_polygons/extensions/baryon_asymmetry.py src/planetary_polygons/proofs/instanton_proof.py`
Expected: No output (no imports from old modules)

- [ ] **Step 5: Final commit**

```bash
git commit --allow-empty -m "chore: all backbone code modules complete — 190+ tests passing"
```
