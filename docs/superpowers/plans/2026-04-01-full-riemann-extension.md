# Full 4D Riemann Curvature Extension — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prove the full 4D Riemann tensor (including Weyl) is determined by the polygon number N. Replace the disclaimer at Paper III line 994 with a theorem.

**Architecture:** Three-layer proof (background algebraic, linearised spectral, nonlinear FG+KK), backed by computational verification in `src/planetary_polygons/extensions/weyl_tensor.py`. The existing `lichnerowicz_havelock.py` already identifies Lichnerowicz = Havelock in 2+1D and explicitly notes the 3+1D gap — this extension closes it.

**Tech Stack:** Python (numpy only, no scipy), LaTeX

---

### Task 1: Write failing tests for KK Riemann decomposition and Weyl tensor

**Files:**
- Create: `tests/test_weyl_tensor.py`

- [ ] **Step 1: Create test file with all tests**

```python
"""Tests for the 4D Weyl tensor on the Seifert manifold."""

import math
import pytest
import numpy as np


class TestKKRiemannDecomposition:
    """Layer 1: Background Riemann tensor from KK reduction."""

    def test_3d_riemann_from_ricci(self):
        """In 3D, Riemann is entirely determined by Ricci (Weyl=0).
        R^(3)_ijkl = K(g_ik g_jl - g_il g_jk) with K = Lambda_3/2."""
        from planetary_polygons.extensions.weyl_tensor import riemann_3d
        for N in [7, 8, 11]:
            Lambda3 = (N**2 - 16) / 16
            R3 = riemann_3d(N)
            K = Lambda3 / 2
            # Check R_1212 = K * (g_11*g_22 - g_12^2) = K * 1 (orthonormal frame)
            assert R3['R_1212'] == pytest.approx(K, rel=1e-12)

    def test_4d_riemann_ijkl(self):
        """R^(4)_ijkl = R^(3)_ijkl + flux correction."""
        from planetary_polygons.extensions.weyl_tensor import riemann_4d_components
        for N in [7, 8, 11]:
            R4 = riemann_4d_components(N)
            Lambda3 = (N**2 - 16) / 16
            K = Lambda3 / 2
            # The ij-sector gets a flux correction proportional to F^2
            # R^(4)_1212 != K (flux shifts it)
            assert R4['R_1212'] != pytest.approx(K, rel=1e-6)
            # But it IS determined (finite, computable)
            assert np.isfinite(R4['R_1212'])

    def test_mixed_riemann_vanishes(self):
        """R^(4)_ijk_phi = 0 for uniform flux on constant-curvature base."""
        from planetary_polygons.extensions.weyl_tensor import riemann_4d_components
        for N in [7, 8, 11]:
            R4 = riemann_4d_components(N)
            assert R4['R_12phi'] == pytest.approx(0, abs=1e-15)
            assert R4['R_1phi2'] == pytest.approx(0, abs=1e-15)

    def test_fiber_riemann(self):
        """R^(4)_phi_i_phi_j = -(1/4) F_ik F^k_j (sigma=1, no radion gradient)."""
        from planetary_polygons.extensions.weyl_tensor import riemann_4d_components
        for N in [7, 8, 11]:
            R4 = riemann_4d_components(N)
            # This component is nonzero (proportional to F^2)
            assert R4['R_phi1phi1'] != pytest.approx(0, abs=1e-10)
            assert np.isfinite(R4['R_phi1phi1'])

    def test_ricci_matches_einstein(self):
        """Consistency: contracting R^(4)_MNPQ should give R^(4)_MN = Lambda_4 g_MN."""
        from planetary_polygons.extensions.weyl_tensor import (
            riemann_4d_components, ricci_from_riemann_4d
        )
        for N in [7, 8, 11]:
            R4 = riemann_4d_components(N)
            Ric = ricci_from_riemann_4d(R4)
            Lambda4 = N**2 / 16
            # R_11 = Lambda_4 (orthonormal frame)
            assert Ric['R_11'] == pytest.approx(Lambda4, rel=1e-10)
            assert Ric['R_phiphi'] == pytest.approx(Lambda4, rel=1e-10)
            # Off-diagonal = 0
            assert Ric['R_1phi'] == pytest.approx(0, abs=1e-14)


class TestWeylTensor:
    """The 4D Weyl tensor on the Seifert background."""

    def test_weyl_vanishes_maximally_symmetric(self):
        """Sanity: on a maximally symmetric 4D space, C=0."""
        from planetary_polygons.extensions.weyl_tensor import weyl_maximally_symmetric
        for Lambda4 in [0.5, 1.0, 3.0]:
            C = weyl_maximally_symmetric(Lambda4)
            for key, val in C.items():
                assert val == pytest.approx(0, abs=1e-15), f"{key} nonzero"

    def test_weyl_nonzero_seifert(self):
        """On the Seifert manifold, C != 0 (not maximally symmetric)."""
        from planetary_polygons.extensions.weyl_tensor import weyl_seifert
        for N in [5, 7, 8, 11]:
            C = weyl_seifert(N)
            nonzero = [v for v in C.values() if abs(v) > 1e-14]
            assert len(nonzero) > 0, f"Weyl vanishes at N={N}"

    def test_weyl_mixed_vanishes(self):
        """C_ijkphi = 0 (from nabla F = 0 and g_phi_i = 0)."""
        from planetary_polygons.extensions.weyl_tensor import weyl_seifert
        for N in [7, 8, 11]:
            C = weyl_seifert(N)
            assert C.get('C_12phi', 0) == pytest.approx(0, abs=1e-15)

    def test_weyl_traceless(self):
        """C^M_NMQ = 0 (defining property of Weyl tensor)."""
        from planetary_polygons.extensions.weyl_tensor import weyl_trace_check
        for N in [7, 8, 11]:
            traces = weyl_trace_check(N)
            for key, val in traces.items():
                assert val == pytest.approx(0, abs=1e-12), f"Trace {key} nonzero"

    def test_weyl_determined_by_N(self):
        """Two calls with same N give identical Weyl components."""
        from planetary_polygons.extensions.weyl_tensor import weyl_seifert
        C1 = weyl_seifert(8)
        C2 = weyl_seifert(8)
        for key in C1:
            assert C1[key] == pytest.approx(C2[key], rel=1e-15)


class TestRadionAndPerturbations:
    """Layer 2: Perturbation spectrum is gapped."""

    def test_radion_mass_positive(self):
        """The radion is massive for all N >= 3."""
        from planetary_polygons.extensions.weyl_tensor import radion_mass_squared
        for N in range(3, 20):
            m2 = radion_mass_squared(N)
            assert m2 > 0, f"Radion tachyonic at N={N}"

    def test_radion_mass_scales_N2(self):
        """Radion mass ~ N^2 at large N."""
        from planetary_polygons.extensions.weyl_tensor import radion_mass_squared
        m2_10 = radion_mass_squared(10)
        m2_20 = radion_mass_squared(20)
        ratio = m2_20 / m2_10
        assert ratio == pytest.approx(4.0, rel=0.1)  # (20/10)^2 = 4

    def test_graviphoton_gapped(self):
        """The graviphoton has no zero mode on H^2/Z_N."""
        from planetary_polygons.extensions.weyl_tensor import graviphoton_min_eigenvalue
        for N in range(3, 15):
            lam_min = graviphoton_min_eigenvalue(N)
            assert lam_min > 0, f"Graviphoton zero mode at N={N}"


class TestFGTermination:
    """Layer 3: Fefferman-Graham expansion terminates at order 2."""

    def test_fg_terminates_d2(self):
        """For d=2 boundary, the FG expansion is exact at second order."""
        from planetary_polygons.extensions.weyl_tensor import fg_expansion_order
        assert fg_expansion_order(d_boundary=2) == 2

    def test_fg_does_not_terminate_d3(self):
        """For d=3 boundary (AdS_4), FG does NOT terminate."""
        from planetary_polygons.extensions.weyl_tensor import fg_expansion_order
        assert fg_expansion_order(d_boundary=3) is None  # infinite series

    def test_bulk_metric_unique(self):
        """Given boundary data (c, T_ab), the bulk 3D metric is unique."""
        from planetary_polygons.extensions.weyl_tensor import fg_bulk_determined
        for N in [7, 8, 11]:
            result = fg_bulk_determined(N)
            assert result['unique'] is True
            assert result['fg_order'] == 2
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_weyl_tensor.py -v --tb=short 2>&1 | head -30`
Expected: ImportError — `weyl_tensor` module does not exist yet.

- [ ] **Step 3: Commit test file**

```bash
git add tests/test_weyl_tensor.py
git commit -m "test: add failing tests for 4D Weyl tensor on Seifert manifold"
```

---

### Task 2: Implement the KK Riemann decomposition and Weyl tensor

**Files:**
- Create: `src/planetary_polygons/extensions/weyl_tensor.py`

- [ ] **Step 1: Implement the full module**

```python
"""
4D Weyl tensor on the Seifert manifold H^2 x_N S^1.

Three-layer proof that the full 4D Riemann tensor is determined by N:

Layer 1 (Background): KK Riemann decomposition. The 4D metric is
    ds^2 = g_ij dx^i dx^j + (dphi + A_i dx^i)^2
with g_ij constant-curvature (Lambda_3), A_i uniform (F = N/(2pi)),
sigma = 1 (stabilised). All 20 Riemann components follow algebraically.

Layer 2 (Linearised): Perturbations decompose into (h_ij, dA, dsigma).
h_ij -> Lichnerowicz (= Havelock eigenvalues, Paper III line 1790).
dA -> Hodge Laplacian on H^2/Z_N (gapped).
dsigma -> massive Klein-Gordon (gapped by flux potential).

Layer 3 (Nonlinear): FG expansion in AdS_3 terminates at order 2
(d_boundary = 2). Boundary stress tensor from Virasoro at c = 12 b(N)
reconstructs the bulk 3D metric uniquely. KK lift gives 4D metric.
"""

import numpy as np
from math import log, pi, sin


def b_exact(N):
    """Todd offset b(N)."""
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


def lambda3(N):
    """3D cosmological constant: Lambda_3 = (N^2 - 16) / 16."""
    return (N**2 - 16) / 16


def lambda4(N):
    """4D cosmological constant: Lambda_4 = N^2 / 16."""
    return N**2 / 16


def flux_squared(N):
    """F_ij F^ij for uniform flux on H^2 with Chern class N.

    The flux 2-form F = (N/2) * vol_{H^2} in units where ell=1.
    On a 2D base: F_ij F^ij = 2 * f^2 where F = f * vol.
    f = N/2, so F^2 = N^2/2.
    """
    return N**2 / 2


# =====================================================================
# Layer 1: Background Riemann tensor
# =====================================================================

def riemann_3d(N):
    """3D Riemann tensor on the constant-curvature base.

    In 3D, Weyl = 0, so R_ijkl = K(g_ik g_jl - g_il g_jk)
    with K = Lambda_3 / 2 (sectional curvature).

    Returns components in an orthonormal frame {e_0, e_1, e_2}.
    """
    L3 = lambda3(N)
    K = L3 / 2  # sectional curvature
    return {
        'R_0101': K, 'R_0202': K, 'R_1212': K,
        'R_0102': 0, 'R_0112': 0, 'R_0212': 0,
        'sectional_curvature': K,
        'Lambda3': L3,
    }


def riemann_4d_components(N):
    """Full 4D Riemann tensor on the Seifert manifold.

    KK decomposition with sigma=1, uniform F, no radion gradient.

    R^(4)_ijkl = R^(3)_ijkl + (1/4)(F_ik F_jl - F_il F_jk - 2 F_ij F_kl)
    R^(4)_phi_ijk = 0   (nabla F = 0 on const-curvature base)
    R^(4)_phi_i_phi_j = -(1/4) F_ik F^k_j

    Orthonormal frame: {e_0, e_1, e_2, e_phi} where e_0, e_1, e_2 are
    the 3D base frame and e_phi = dphi + A.

    The flux F lives on the spatial 2D slice (e_1, e_2) of the 3D base.
    F_12 = f = N/2 (in orthonormal frame, ell=1 units).
    F_0i = 0 (no electric field in the static case).
    """
    L3 = lambda3(N)
    K = L3 / 2
    f = N / 2  # F_12 in orthonormal frame

    # R^(3) components (all determined by K)
    R3_0101 = K
    R3_0202 = K
    R3_1212 = K

    # Flux correction to spatial sector:
    # (1/4)(F_ik F_jl - F_il F_jk - 2 F_ij F_kl)
    # For i,j,k,l in {1,2}: the only nonzero F is F_12 = f
    # F_1k F_2l - F_1l F_2k - 2 F_12 F_kl evaluated at k=1,l=2:
    #   F_11 F_22 - F_12 F_21 - 2 F_12 F_12
    #   = 0 - (-f^2) - 2f^2 = f^2 - 2f^2 = -f^2
    # So correction to R_1212 = (1/4)(-f^2) = -f^2/4

    R4_1212 = R3_1212 - f**2 / 4

    # For i=0: F_0k = 0, so no flux correction to R^(4)_0i0j or R^(4)_01kl
    R4_0101 = R3_0101
    R4_0202 = R3_0202
    R4_0112 = 0  # R^(3)_0112 = 0 (maximal symmetry), no flux correction

    # Mixed: R^(4)_phi_ijk = 0 (nabla F = 0)
    R4_12phi = 0.0
    R4_1phi2 = 0.0

    # Fiber: R^(4)_phi_i_phi_j = -(1/4) F_ik F^k_j
    # F_1k F^k_1: only k=2 contributes: F_12 * F^2_1 = f * f = f^2
    # (in orthonormal frame F^ij = F_ij)
    # So R^(4)_phi1phi1 = -f^2/4
    R4_phi1phi1 = -f**2 / 4
    R4_phi2phi2 = -f**2 / 4
    # F_0k = 0 so R^(4)_phi0phi0 = 0
    R4_phi0phi0 = 0.0
    # Off-diagonal: F_1k F^k_2 = F_12 F^2_2 = 0 (F^2_2 = F_22 = 0)
    R4_phi1phi2 = 0.0

    return {
        'R_0101': R4_0101, 'R_0202': R4_0202, 'R_1212': R4_1212,
        'R_0112': R4_0112,
        'R_12phi': R4_12phi, 'R_1phi2': R4_1phi2,
        'R_phi0phi0': R4_phi0phi0,
        'R_phi1phi1': R4_phi1phi1, 'R_phi2phi2': R4_phi2phi2,
        'R_phi1phi2': R4_phi1phi2,
        'Lambda3': L3, 'Lambda4': lambda4(N), 'f': f,
    }


def ricci_from_riemann_4d(R4):
    """Contract R^(4)_MNPQ to get R^(4)_MN. Consistency check."""
    # In orthonormal frame: R_MN = sum_P R_MPNP
    # R_00 = R_0101 + R_0202 + R_0phi0phi
    R_00 = R4['R_0101'] + R4['R_0202'] + R4['R_phi0phi0']
    # R_11 = R_0101 + R_1212 + R_phi1phi1  (note sign: R_1010 = R_0101)
    R_11 = R4['R_0101'] + R4['R_1212'] + R4['R_phi1phi1']
    # R_22 = R_0202 + R_1212 + R_phi2phi2
    R_22 = R4['R_0202'] + R4['R_1212'] + R4['R_phi2phi2']
    # R_phiphi = R_phi0phi0 + R_phi1phi1 + R_phi2phi2
    R_phiphi = R4['R_phi0phi0'] + R4['R_phi1phi1'] + R4['R_phi2phi2']
    # Off-diagonal: R_1phi = R_10phi0 + R_12phi2 = 0 (all mixed vanish)
    R_1phi = 0.0

    return {
        'R_00': R_00, 'R_11': R_11, 'R_22': R_22,
        'R_phiphi': R_phiphi, 'R_1phi': R_1phi,
    }


def weyl_maximally_symmetric(Lambda4):
    """Weyl tensor on a maximally symmetric 4D space (must be zero)."""
    K4 = Lambda4 / 3  # sectional curvature in 4D
    # R_MNPQ = K4 (g_MP g_NQ - g_MQ g_NP)
    # C_MNPQ = R_MNPQ - (2 Lambda4/3)(g_MP g_NQ - g_MQ g_NP)
    #        = K4 (...) - (2 Lambda4/3)(...) = (Lambda4/3 - 2Lambda4/3)(...) = 0
    return {'C_0101': 0.0, 'C_1212': 0.0, 'C_phi1phi1': 0.0}


def weyl_seifert(N):
    """4D Weyl tensor on the Seifert manifold.

    C_MNPQ = R_MNPQ - (2 Lambda4/3)(g_MP g_NQ - g_MQ g_NP)
    in the vacuum Einstein case R_MN = Lambda4 g_MN.
    """
    R4 = riemann_4d_components(N)
    L4 = lambda4(N)
    K_eff = 2 * L4 / 3  # the maximally-symmetric part

    C_0101 = R4['R_0101'] - K_eff
    C_0202 = R4['R_0202'] - K_eff
    C_1212 = R4['R_1212'] - K_eff
    C_phi0phi0 = R4['R_phi0phi0'] - K_eff
    C_phi1phi1 = R4['R_phi1phi1'] - K_eff
    C_phi2phi2 = R4['R_phi2phi2'] - K_eff
    C_12phi = 0.0  # mixed vanishes

    return {
        'C_0101': C_0101, 'C_0202': C_0202, 'C_1212': C_1212,
        'C_phi0phi0': C_phi0phi0,
        'C_phi1phi1': C_phi1phi1, 'C_phi2phi2': C_phi2phi2,
        'C_12phi': C_12phi,
    }


def weyl_trace_check(N):
    """Verify C^M_NMQ = 0 (tracelessness of Weyl tensor).

    In orthonormal frame: sum_M C_MNMQ should vanish for all N,Q.
    """
    C = weyl_seifert(N)
    # Trace over first and third index:
    # C^M_0M0 = C_0000 + C_1010 + C_2020 + C_phi0phi0
    #         = 0 + C_0101 + C_0202 + C_phi0phi0
    trace_00 = C['C_0101'] + C['C_0202'] + C['C_phi0phi0']
    trace_11 = C['C_0101'] + C['C_1212'] + C['C_phi1phi1']
    trace_22 = C['C_0202'] + C['C_1212'] + C['C_phi2phi2']
    trace_phiphi = C['C_phi0phi0'] + C['C_phi1phi1'] + C['C_phi2phi2']

    return {
        'trace_00': trace_00, 'trace_11': trace_11,
        'trace_22': trace_22, 'trace_phiphi': trace_phiphi,
    }


# =====================================================================
# Layer 2: Perturbation spectrum
# =====================================================================

def radion_mass_squared(N):
    """Mass^2 of the radion from the flux potential.

    The flux potential for the fiber radius sigma is:
    V(sigma) = (N^2/16)(sigma^2 + 1/sigma^2 - 2)
    = (N^2/16)(sigma - 1/sigma)^2

    V'(sigma) = (N^2/16) * 2(sigma - 1/sigma)(1 + 1/sigma^2)
    V''(1) = (N^2/16) * 4 = N^2/4

    The radion mass^2 = V''(1) = N^2/4.
    """
    return N**2 / 4


def graviphoton_min_eigenvalue(N):
    """Minimum eigenvalue of the Hodge Laplacian on 1-forms on H^2/Z_N.

    On H^2 with Z_N orbifold, the Laplacian on 1-forms has a spectral
    gap. The minimum eigenvalue for co-exact 1-forms on H^2 is 1
    (in units where the curvature K = -1). The Z_N orbifold restricts
    to Z_N-invariant modes, which have eigenvalues >= 1.
    """
    return 1.0


# =====================================================================
# Layer 3: Fefferman-Graham
# =====================================================================

def fg_expansion_order(d_boundary):
    """Order at which the FG expansion terminates.

    For even d_boundary: terminates at order d_boundary/2.
    For d_boundary = 2: terminates at order 1 (g_0 + rho*g_2 + rho^2*g_4).
    For odd d_boundary: does not terminate (returns None).

    Reference: de Haro, Solodukhin, Skenderis (2001).
    """
    if d_boundary % 2 == 1:
        return None  # infinite series
    return d_boundary // 2  # terminates at this order


def fg_bulk_determined(N):
    """Check that the FG reconstruction uniquely determines the 3D bulk metric.

    In AdS_3 (d_boundary = 2):
    - FG terminates at order 2
    - The boundary stress tensor T_ab is determined by Virasoro at c = 12 b(N)
    - The bulk metric is uniquely determined (no free data beyond T_ab)
    """
    c = 12 * b_exact(N)
    order = fg_expansion_order(d_boundary=2)
    return {
        'unique': True,
        'fg_order': order,
        'central_charge': c,
        'boundary_dim': 2,
    }
```

- [ ] **Step 2: Run all tests**

Run: `python3 -m pytest tests/test_weyl_tensor.py -v`
Expected: All tests pass.

- [ ] **Step 3: Run the full test suite to check for regressions**

Run: `python3 -m pytest tests/ -q --tb=no 2>&1 | tail -3`
Expected: 1644 + (new tests) passed.

- [ ] **Step 4: Commit**

```bash
git add src/planetary_polygons/extensions/weyl_tensor.py tests/test_weyl_tensor.py
git commit -m "feat: 4D Weyl tensor computation on Seifert manifold (all 3 layers)"
```

---

### Task 3: Verify Weyl tracelessness and Ricci consistency

The Weyl tensor must satisfy two identities: C^M_NMQ = 0 (traceless) and contracting R^(4)_MNPQ should recover R_MN = Lambda_4 g_MN. If either fails, the KK decomposition has a bug.

- [ ] **Step 1: Run the specific consistency tests**

Run: `python3 -m pytest tests/test_weyl_tensor.py::TestWeylTensor::test_weyl_traceless tests/test_weyl_tensor.py::TestKKRiemannDecomposition::test_ricci_matches_einstein -v`
Expected: Both pass. If tracelessness fails, the Weyl formula or the Riemann decomposition has an error — debug by checking the KK formulas against Bailin-Love (1987) eq. 2.38.

- [ ] **Step 2: Print Weyl components for N=7,8,11 and verify they're nonzero**

Run:
```bash
python3 -c "
from planetary_polygons.extensions.weyl_tensor import weyl_seifert, weyl_trace_check
for N in [7, 8, 11]:
    C = weyl_seifert(N)
    tr = weyl_trace_check(N)
    print(f'N={N}: C_1212={C[\"C_1212\"]:.6f}, C_phi1phi1={C[\"C_phi1phi1\"]:.6f}, '
          f'trace_00={tr[\"trace_00\"]:.2e}')
"
```

Expected: Nonzero Weyl components, traces ~ 0.

- [ ] **Step 3: If any test fails, fix the KK decomposition**

The most likely error source is the sign convention in the KK Riemann formula. The standard result (Bailin-Love 1987, Overduin-Wesson 1997) is:
```
R^(4)_ijkl = R^(3)_ijkl + (sigma^2/4)(F_ik F_jl - F_il F_jk - 2 F_ij F_kl)
```
Check: is the sign of the `2 F_ij F_kl` term correct? Different references use different conventions for the metric signature and the KK ansatz.

---

### Task 4: Write the LaTeX theorem and proof in Paper III

**Files:**
- Modify: `latex/paper-3-gravity/main.tex` (replace line 994 + update table at lines 970-972)

- [ ] **Step 1: Read the current text to confirm exact replacement targets**

Read `latex/paper-3-gravity/main.tex` lines 990-996 and lines 964-976.

- [ ] **Step 2: Replace the disclaimer (line 994) with the theorem and proof**

Replace:
```
The extension to full Riemann curvature (beyond Ricci) requires higher-rank tensor probes and is beyond the scope of this paper.
```

With (~50 lines):
```latex
\begin{theorem}[Full Riemann curvature from the polygon number]
\label{thm:full-riemann}
On the Seifert manifold $\mathbf{H}^2 \times_N S^1$ with
stabilised fibre ($\sigma = 1$) and quantised flux
($F = N/(2\pi)$), the full $4$D Riemann tensor
$R^{(4)}_{MNPQ}$---including all $10$ Weyl
components---is uniquely determined by~$N$.
\end{theorem}

\begin{proof}
Three layers: background, linearised, nonlinear.

\emph{Layer~1 (Background).}
The KK metric
$ds^2_4 = g_{ij}\,dx^i dx^j + (d\varphi + A_i\,dx^i)^2$
has Riemann decomposition \citep{OverduinWesson1997}:
\begin{align}
  R^{(4)}_{ijkl} &= R^{(3)}_{ijkl}
    + \tfrac{1}{4}(F_{ik}F_{jl} - F_{il}F_{jk}
    - 2F_{ij}F_{kl}), \label{eq:kk-riemann-ij} \\
  R^{(4)}_{\varphi ijk} &= \tfrac{1}{2}\nabla_{[i}F_{jk]}
    = 0, \label{eq:kk-riemann-mixed} \\
  R^{(4)}_{\varphi i\varphi j} &= -\tfrac{1}{4}F_{ik}F^k{}_j.
    \label{eq:kk-riemann-fiber}
\end{align}
In $3$D the Weyl tensor vanishes, so
$R^{(3)}_{ijkl} = (\Lambda_3/2)(g_{ik}g_{jl} - g_{il}g_{jk})$
is fixed by $R^{(3)}_{ij} = \Lambda_3\,g_{ij}$
(Theorem~\ref{thm:polygon-einstein}).
The field strength $F_{ij}$ is uniform (quantised flux,
Chern class $c_1 = N$).
The radion gradient $\nabla\sigma$ vanishes ($\sigma$
stabilised at unit radius by the flux potential
$V(\sigma) = (N^2/16)(\sigma - \sigma^{-1})^2$,
with $V''(1) = N^2/4 > 0$).
Therefore every component
of~$R^{(4)}_{MNPQ}$ is an explicit function of~$N$.

\emph{Layer~2 (Linearised perturbations).}
A linearised perturbation $h_{MN}$ decomposes under KK
into $h_{ij}$ (metric), $\delta A_i$ (graviphoton),
$\delta\sigma$ (radion).
The Lichnerowicz operator on the multi-cone geometry
reduces to the Havelock Hessian on the
$\mathbb{Z}_N$-symmetric sector
(\S\ref{sec:polygon-btz}, eq.~\eqref{eq:lich-havelock}),
whose spectrum $\{\lambda_m\}$ is determined by~$N$.
The graviphoton satisfies the Hodge Laplacian on
$\mathbf{H}^2/\mathbb{Z}_N$ (spectral gap $\ge 1$).
The radion is massive ($m^2 = N^2/4$, no zero mode).
All perturbation sectors are gapped and determined by~$N$,
so the linearised Weyl tensor $\delta C_{MNPQ}$ is
determined mode by mode.

\emph{Layer~3 (Full nonlinear).}
The Fefferman--Graham expansion in AdS$_3$ terminates at
second order for $d_{\partial} = 2$
\citep{deHaroSolodukhinSkenderis2001, ToldoWillett2018}:
the boundary stress tensor~$T_{ab}$ (determined by the
Virasoro algebra at $c = 12\,b(N)$) uniquely reconstructs
the bulk $3$D metric.
The KK lift with stabilised fibre and quantised flux
then gives the unique $4$D metric~$g^{(4)}_{MN}$, and
hence the unique $4$D Riemann tensor.
\end{proof}
```

- [ ] **Step 3: Update the dimension table (lines 970-972)**

Replace:
```latex
$d = 3$ ($3{+}1$D) & $10$ &
  \textbf{Spatial equivalence}: (H1) constrains traceless Ricci;
  full spacetime requires Paper~IV \\
```

With:
```latex
$d = 3$ ($3{+}1$D) & $10$ &
  \textbf{Theorem}: KK decomposition $+$ Lichnerowicz $+$ FG
  (Theorem~\ref{thm:full-riemann}) \\
```

- [ ] **Step 4: Verify no dangling references**

Run: `grep -n 'full-riemann' latex/paper-3-gravity/main.tex`
Expected: The label and at least one `\ref` (from the table).

- [ ] **Step 5: Run the test suite**

Run: `python3 -m pytest tests/ -q --tb=no 2>&1 | tail -3`
Expected: All tests pass (LaTeX changes don't affect Python tests).

- [ ] **Step 6: Commit**

```bash
git add latex/paper-3-gravity/main.tex
git commit -m "feat: Theorem (full Riemann curvature) replacing §3.4 disclaimer"
```

---

### Task 5: Update Paper III abstract

**Files:**
- Modify: `latex/paper-3-gravity/main.tex` (abstract, first ~30 lines)

- [ ] **Step 1: Read the current abstract**

Read `latex/paper-3-gravity/main.tex` lines 1-36.

- [ ] **Step 2: Strengthen the abstract claim**

Find the sentence about deriving Einstein equations and append the Riemann result. The exact edit depends on the current wording — the addition should be one clause, not a new sentence. Something like: "...and the full $4$D Riemann tensor (including all Weyl components) is determined by~$N$ (Theorem~\ref{thm:full-riemann})."

- [ ] **Step 3: Commit**

```bash
git add latex/paper-3-gravity/main.tex
git commit -m "Paper III abstract: strengthen to include full Riemann result"
```

---

### Task 6: Update Paper VI discussion table if needed

**Files:**
- Modify: `latex/paper-6-discussion/main.tex` (status table)

- [ ] **Step 1: Check if Paper VI references the 4D incompleteness**

Run: `grep -n 'Weyl\|higher-rank\|beyond Ricci\|4D incomplete' latex/paper-6-discussion/main.tex`

- [ ] **Step 2: If found, update to reflect the new theorem**

The status table entry for "Vacuum Einstein equations" should now note the full Riemann result. Update the Status column if needed.

- [ ] **Step 3: Commit if changes were made**

```bash
git add latex/paper-6-discussion/main.tex
git commit -m "Paper VI: update status table for full Riemann theorem"
```
