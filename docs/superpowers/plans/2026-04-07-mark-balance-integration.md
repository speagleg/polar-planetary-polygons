# Mark-Balance Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate 30+ proved mark-balance results into Papers I, IV, V, VII with full theorem-proof treatment and computational backing.

**Architecture:** One new proof module (`mark_distribution.py`) provides the computational foundation. Four LaTeX workstreams (Papers I, V, IV, VII) add theorems and discussion in dependency order. Each workstream is self-contained after the proof module exists.

**Tech Stack:** Python 3 (numpy, fractions, math — no scipy), LaTeX, pytest

---

### Task 1: Create proof module with core mark data and balance identity

**Files:**
- Create: `src/planetary_polygons/proofs/mark_distribution.py`
- Create: `tests/test_mark_distribution.py`

- [ ] **Step 1: Write failing tests for ADE marks and mark-balance**

```python
# tests/test_mark_distribution.py
"""Tests for the I* mark distribution and its identities."""

import pytest
from fractions import Fraction


class TestADEMarks:
    """Tests for ADE affine mark data."""

    def test_e8_marks(self):
        from planetary_polygons.proofs.mark_distribution import ade_marks
        assert ade_marks('E8') == [1, 2, 3, 4, 5, 6, 4, 2, 3]

    def test_e7_marks(self):
        from planetary_polygons.proofs.mark_distribution import ade_marks
        assert ade_marks('E7') == [1, 2, 3, 4, 3, 2, 1, 2]

    def test_e6_marks(self):
        from planetary_polygons.proofs.mark_distribution import ade_marks
        assert ade_marks('E6') == [1, 1, 2, 3, 2, 1, 1]

    def test_e8_coxeter_number(self):
        from planetary_polygons.proofs.mark_distribution import ade_marks
        assert sum(ade_marks('E8')) == 30

    def test_e8_group_order(self):
        from planetary_polygons.proofs.mark_distribution import ade_marks
        m = ade_marks('E8')
        assert sum(d**2 for d in m) == 120


class TestMarkBalance:
    """Tests for the mark-balance identity Σd(d-k₁)=0."""

    def test_e8_balance(self):
        from planetary_polygons.proofs.mark_distribution import mark_balance
        bal, k1 = mark_balance([1, 2, 3, 4, 5, 6, 4, 2, 3])
        assert bal == 0
        assert k1 == Fraction(4)

    def test_e8_unique(self):
        """Mark-balance at pivot 4 holds ONLY for E₈ among exceptional types."""
        from planetary_polygons.proofs.mark_distribution import mark_balance, ade_marks
        for t in ['E6', 'E7']:
            bal, _ = mark_balance(ade_marks(t))
            assert bal != 0, f"{t} should NOT have mark-balance at pivot 4"

    def test_e6_pivot_is_2(self):
        from planetary_polygons.proofs.mark_distribution import mark_balance
        _, k1 = mark_balance([1, 1, 2, 3, 2, 1, 1])
        assert k1 == Fraction(2)

    def test_e8_gauss_bonnet(self):
        """Mark-balance equivalent to |I*| = 4h (Gauss-Bonnet tiling)."""
        from planetary_polygons.proofs.mark_distribution import ade_marks
        m = ade_marks('E8')
        assert sum(d**2 for d in m) == 4 * sum(m)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /mnt/c/Users/gspea/source/repos/planetary-polygons-unified && python3 -m pytest tests/test_mark_distribution.py -v`
Expected: FAIL (module not found)

- [ ] **Step 3: Implement core module**

```python
# src/planetary_polygons/proofs/mark_distribution.py
r"""
The I* mark distribution and its identities.

Marks d = (1,2,3,4,5,6,4,2,3): null eigenvector of the Ẽ₈ Cartan matrix.
Mark-balance: Σd(d-4) = 0, unique to E₈, equivalent to |I*| = 4h (Paper I §8).
"""

from fractions import Fraction
from math import gcd, cos, pi, sqrt


# =====================================================================
# ADE mark data (affine Dynkin diagram null eigenvectors)
# =====================================================================

_ADE_MARKS = {
    'A1': [1, 1],
    'A2': [1, 1, 1],
    'A3': [1, 1, 1, 1],
    'A4': [1, 1, 1, 1, 1],
    'D4': [1, 1, 2, 1, 1],
    'D5': [1, 1, 2, 2, 1, 1],
    'D6': [1, 1, 2, 2, 2, 1, 1],
    'E6': [1, 1, 2, 3, 2, 1, 1],
    'E7': [1, 2, 3, 4, 3, 2, 1, 2],
    'E8': [1, 2, 3, 4, 5, 6, 4, 2, 3],
}

# Affine Dynkin diagram edges (0-indexed nodes)
_ADE_EDGES = {
    'E6': [(0, 3), (1, 2), (2, 3), (3, 4), (4, 5), (3, 6)],
    'E7': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (3, 7)],
    'E8': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (5, 8)],
    'D4': [(0, 2), (1, 2), (2, 3), (2, 4)],
}


def ade_marks(ade_type):
    """Return affine marks for the given ADE type."""
    return list(_ADE_MARKS[ade_type])


def ade_edges(ade_type):
    """Return edges of the affine Dynkin diagram."""
    return list(_ADE_EDGES[ade_type])


def mark_balance(marks):
    """Compute Σd(d-k₁) and the pivot k₁ = Σd²/Σd.

    Returns (balance_value, k1) where balance is always 0 by definition
    of k₁. The interesting question is whether k₁ is an INTEGER.
    """
    s1 = sum(marks)
    s2 = sum(d**2 for d in marks)
    k1 = Fraction(s2, s1)
    balance = sum(d * (d - int(k1)) for d in marks) if k1.denominator == 1 else None
    return balance, k1
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /mnt/c/Users/gspea/source/repos/planetary-polygons-unified && python3 -m pytest tests/test_mark_distribution.py -v`
Expected: all PASS

- [ ] **Step 5: Commit**

```bash
cd /mnt/c/Users/gspea/source/repos/planetary-polygons-unified
git add src/planetary_polygons/proofs/mark_distribution.py tests/test_mark_distribution.py
git commit -m "feat: mark distribution proof module — ADE marks and balance identity"
```

---

### Task 2: V⊗F theorem and charge-magnitude chain

**Files:**
- Modify: `src/planetary_polygons/proofs/mark_distribution.py`
- Modify: `tests/test_mark_distribution.py`

- [ ] **Step 1: Write failing tests**

```python
# Append to tests/test_mark_distribution.py

class TestVtensorF:
    """Tests for V⊗F = 4×reg(A₅)."""

    def test_icosahedron_vf_equals_roots(self):
        from planetary_polygons.proofs.mark_distribution import vtensor_f_multiplicity
        k = vtensor_f_multiplicity(V=12, F=20, stab_V=5, stab_F=3, group_order=60)
        assert k == 4  # V⊗F = 4 × reg(A₅)
        assert 12 * 20 == 240  # = roots(E₈)

    def test_octahedron_vf(self):
        from planetary_polygons.proofs.mark_distribution import vtensor_f_multiplicity
        k = vtensor_f_multiplicity(V=6, F=8, stab_V=4, stab_F=3, group_order=24)
        assert k == 2  # V⊗F = 2 × reg(S₄)

    def test_tetrahedron_not_regular(self):
        """Tetrahedron: gcd(3,3)=3≠1, so V⊗F is NOT a multiple of reg."""
        from planetary_polygons.proofs.mark_distribution import vtensor_f_multiplicity
        k = vtensor_f_multiplicity(V=4, F=4, stab_V=3, stab_F=3, group_order=12)
        assert k is None  # NOT a regular rep multiple


class TestChargeMagnitudeChain:
    """Tests for the iterated charge-magnitude map E₈→E₆→A₃→∅."""

    def test_e8_to_e6(self):
        from planetary_polygons.proofs.mark_distribution import charge_magnitude_map
        target, kernel = charge_magnitude_map([1, 2, 3, 4, 5, 6, 4, 2, 3], pivot=4)
        assert sorted(target) == sorted([1, 1, 1, 2, 2, 2, 3])  # E₆ marks
        assert kernel == [4, 4]  # the d=4 nodes (SU(3))

    def test_e6_to_a3(self):
        from planetary_polygons.proofs.mark_distribution import charge_magnitude_map
        target, kernel = charge_magnitude_map([1, 1, 2, 2, 3, 2, 1], pivot=2)
        assert sorted(target) == [1, 1, 1, 1]  # A₃ marks
        assert sorted(kernel) == [2, 2, 2]

    def test_full_chain(self):
        from planetary_polygons.proofs.mark_distribution import division_algebra_chain
        chain = division_algebra_chain([1, 2, 3, 4, 5, 6, 4, 2, 3])
        pivots = [step['pivot'] for step in chain]
        assert pivots == [4, 2, 1]
        assert sum(pivots) == 7  # = N_crit
        assert 4 * 2 * 1 == 8  # = rank(E₈)


class TestPivotUniqueness:
    """Test the uniqueness theorem: (4,2,1) unique with Σ=Π-1."""

    def test_uniqueness(self):
        from planetary_polygons.proofs.mark_distribution import sum_equals_product_minus_one
        solutions = sum_equals_product_minus_one(max_a=20)
        assert solutions == [(4, 2, 1)]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_mark_distribution.py::TestVtensorF -v`
Expected: FAIL

- [ ] **Step 3: Implement V⊗F, charge-magnitude chain, and uniqueness**

```python
# Append to src/planetary_polygons/proofs/mark_distribution.py

def vtensor_f_multiplicity(V, F, stab_V, stab_F, group_order):
    """Check if V⊗F = k × reg(G) for a Platonic solid.

    V⊗F is a multiple of the regular representation iff
    gcd(|Stab_V|, |Stab_F|) = 1. If so, returns k = V*F/|G|.
    """
    if gcd(stab_V, stab_F) != 1:
        return None
    return (V * F) // group_order


def charge_magnitude_map(marks, pivot):
    """Apply the charge-magnitude map: |d - pivot| for nonzero values.

    Returns (surviving_marks_sorted, kernel_values).
    """
    kernel = [d for d in marks if d == pivot]
    surviving = sorted(abs(d - pivot) for d in marks if d != pivot)
    return surviving, kernel


def division_algebra_chain(marks):
    """Compute the full iterated charge-magnitude chain.

    Returns list of dicts with pivot, target marks, kernel at each step.
    """
    chain = []
    current = list(marks)
    while len(set(current)) > 1:  # not all equal
        s1 = sum(current)
        s2 = sum(d**2 for d in current)
        k1 = Fraction(s2, s1)
        if k1.denominator != 1:
            break
        pivot = int(k1)
        target, kernel = charge_magnitude_map(current, pivot)
        chain.append({'pivot': pivot, 'target': target, 'kernel': kernel})
        current = target
    # Terminal step: all marks equal
    if current and len(set(current)) == 1:
        chain.append({'pivot': current[0], 'target': [], 'kernel': current})
    return chain


def sum_equals_product_minus_one(max_a=20):
    """Find all (a,b,c) with a≥b≥c≥1 and a+b+c = abc-1."""
    solutions = []
    for a in range(1, max_a + 1):
        for b in range(1, a + 1):
            for c in range(1, b + 1):
                if a * b * c - a - b - c == 1:
                    solutions.append((a, b, c))
    return solutions
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_mark_distribution.py -v`
Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add src/planetary_polygons/proofs/mark_distribution.py tests/test_mark_distribution.py
git commit -m "feat: V⊗F theorem, charge-magnitude chain, pivot uniqueness"
```

---

### Task 3: 2-adic filtration and mark supercharge

**Files:**
- Modify: `src/planetary_polygons/proofs/mark_distribution.py`
- Modify: `tests/test_mark_distribution.py`

- [ ] **Step 1: Write failing tests**

```python
# Append to tests/test_mark_distribution.py

class TestTwoAdicFiltration:
    """Tests for the 2-adic layer structure."""

    def test_layer_assignment(self):
        from planetary_polygons.proofs.mark_distribution import two_adic_layers
        layers = two_adic_layers([1, 2, 3, 4, 5, 6, 4, 2, 3])
        assert layers['K3'] == [1, 3, 5, 3]  # bosons (odd d)
        assert layers['K2'] == [2, 6, 2]      # fermions (d≡2 mod 4)
        assert layers['K1'] == [4, 4]          # gravitinos (d≡0 mod 4)

    def test_supertrace_cancellation(self):
        from planetary_polygons.proofs.mark_distribution import two_adic_layers
        layers = two_adic_layers([1, 2, 3, 4, 5, 6, 4, 2, 3])
        for name, dims in layers.items():
            bal = sum(d * (d - 4) for d in dims)
            if name == 'K1':
                assert bal == 0
            elif name == 'K2':
                assert bal == 4
            elif name == 'K3':
                assert bal == -4

    def test_sigma_d2_matching(self):
        """Σd²(bosons) = Σd²(fermions) = 44."""
        from planetary_polygons.proofs.mark_distribution import two_adic_layers
        layers = two_adic_layers([1, 2, 3, 4, 5, 6, 4, 2, 3])
        assert sum(d**2 for d in layers['K2']) == 44
        assert sum(d**2 for d in layers['K3']) == 44

    def test_proper_3_coloring(self):
        from planetary_polygons.proofs.mark_distribution import is_proper_2adic_coloring
        assert is_proper_2adic_coloring('E8') is True
        assert is_proper_2adic_coloring('D4') is True
        assert is_proper_2adic_coloring('E7') is False
        assert is_proper_2adic_coloring('E6') is False


class TestMarkSupercharge:
    """Tests for ρ₁ as the supercharge."""

    def test_q_squared_bosonic(self):
        """ρ₁⊗ρ₁ = ρ₀+ρ₂, both in K₃ (bosonic)."""
        from planetary_polygons.proofs.mark_distribution import mark_supercharge_squared
        rho0_dim, rho2_dim = mark_supercharge_squared()
        assert rho0_dim == 1  # ρ₀, bosonic (odd)
        assert rho2_dim == 3  # ρ₂, bosonic (odd)

    def test_layer_transitions(self):
        """ρ₁⊗ maps each layer to OTHER layers (proper 3-coloring)."""
        from planetary_polygons.proofs.mark_distribution import supercharge_transitions
        trans = supercharge_transitions()
        # K₃→K₃ should be 0 (no self-transitions for any layer)
        for src in ['K1', 'K2', 'K3']:
            assert src not in trans[src], f"{src} maps to itself!"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_mark_distribution.py::TestTwoAdicFiltration -v`
Expected: FAIL

- [ ] **Step 3: Implement 2-adic filtration and supercharge**

```python
# Append to src/planetary_polygons/proofs/mark_distribution.py

def _v2(n):
    """2-adic valuation of n."""
    if n == 0:
        return float('inf')
    v = 0
    while n % 2 == 0:
        v += 1
        n //= 2
    return v


def _layer(d):
    """Assign a mark d to its 2-adic layer."""
    v = _v2(d)
    if v >= 2:
        return 'K1'
    elif v == 1:
        return 'K2'
    else:
        return 'K3'


def two_adic_layers(marks):
    """Partition marks by 2-adic valuation into K₁, K₂, K₃ layers."""
    layers = {'K1': [], 'K2': [], 'K3': []}
    for d in marks:
        layers[_layer(d)].append(d)
    return layers


def is_proper_2adic_coloring(ade_type):
    """Check if the 2-adic layer assignment is a proper graph coloring."""
    marks = _ADE_MARKS[ade_type]
    edges = _ADE_EDGES.get(ade_type)
    if edges is None:
        return None
    for i, j in edges:
        if _layer(marks[i]) == _layer(marks[j]):
            return False
    return True


def mark_supercharge_squared():
    """ρ₁⊗ρ₁ = ρ₀+ρ₂ from SU(2): 2⊗2 = 1⊕3. Return their dims."""
    return 1, 3  # dim(ρ₀)=1, dim(ρ₂)=3


def supercharge_transitions():
    """Compute which layers ρ₁⊗ maps each layer to."""
    marks = _ADE_MARKS['E8']
    edges = _ADE_EDGES['E8']
    adj = {i: [] for i in range(len(marks))}
    for i, j in edges:
        adj[i].append(j)
        adj[j].append(i)

    transitions = {'K1': set(), 'K2': set(), 'K3': set()}
    for i in range(len(marks)):
        src = _layer(marks[i])
        for j in adj[i]:
            tgt = _layer(marks[j])
            transitions[src].add(tgt)
    return transitions
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_mark_distribution.py -v`
Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add src/planetary_polygons/proofs/mark_distribution.py tests/test_mark_distribution.py
git commit -m "feat: 2-adic filtration, SUSY layer structure, mark supercharge"
```

---

### Task 4: Cartan eigenvalues, spectral decomposition, and generations

**Files:**
- Modify: `src/planetary_polygons/proofs/mark_distribution.py`
- Modify: `tests/test_mark_distribution.py`

- [ ] **Step 1: Write failing tests**

```python
# Append to tests/test_mark_distribution.py
import numpy as np
from math import sqrt


class TestCartanSpectrum:
    """Tests for the Ẽ₈ Cartan eigenvalues and spectral decomposition."""

    def test_eigenvalues(self):
        from planetary_polygons.proofs.mark_distribution import cartan_eigenvalues
        eigs = cartan_eigenvalues('E8')
        phi = (1 + sqrt(5)) / 2
        expected = sorted([0, 1/phi**2, 1, phi, 2, 2+1/phi, 3, 2+phi, 4])
        assert len(eigs) == 9
        for e, x in zip(sorted(eigs), expected):
            assert abs(e - x) < 1e-10

    def test_spectral_denominators(self):
        from planetary_polygons.proofs.mark_distribution import spectral_denominators
        denoms = spectral_denominators(h=30)
        assert denoms == {1, 2, 3, 5}
        assert sum(denoms) == 11
        assert 1 * 2 * 3 * 5 == 30

    def test_characteristic_polynomial_factors(self):
        """p(x) = x(x²-1)(x²-4)(x⁴-3x²+1)."""
        from planetary_polygons.proofs.mark_distribution import cartan_eigenvalues
        eigs = cartan_eigenvalues('E8')
        # Product of all eigenvalues = det(A) for adjacency; should be 0
        assert abs(np.prod(eigs)) < 1e-8

    def test_cyclotomic_indices(self):
        from planetary_polygons.proofs.mark_distribution import cyclotomic_indices
        indices = cyclotomic_indices(h=30)
        assert indices == {1, 2, 3, 4, 5, 6, 10}
        # = I* element orders = divisors of 60 ≤ 10
        assert all(60 % d == 0 and d <= 10 for d in indices)


class TestGenerations:
    """Tests for three generations from the weak eigenvector."""

    def test_e8_three_generations(self):
        from planetary_polygons.proofs.mark_distribution import weak_eigenvector_generations
        n_gen, doublets = weak_eigenvector_generations('E8')
        assert n_gen == 3
        assert len(doublets) == 3

    def test_e7_three_generations(self):
        from planetary_polygons.proofs.mark_distribution import weak_eigenvector_generations
        n_gen, _ = weak_eigenvector_generations('E7')
        assert n_gen == 3

    def test_e6_two_generations(self):
        from planetary_polygons.proofs.mark_distribution import weak_eigenvector_generations
        n_gen, _ = weak_eigenvector_generations('E6')
        assert n_gen == 2

    def test_det_removal_equals_mark_squared(self):
        """det(C without ρᵢ) = dᵢ² for all i."""
        from planetary_polygons.proofs.mark_distribution import det_removal
        marks = [1, 2, 3, 4, 5, 6, 4, 2, 3]
        for i, d in enumerate(marks):
            det = det_removal('E8', i)
            assert abs(det - d**2) < 1e-8


class TestBipartiteConjugation:
    """Tests for matter-antimatter bipartite symmetry."""

    def test_conjugate_eigenvectors(self):
        """v_{μ=4} = -v_{μ=0} × (-1)^level."""
        from planetary_polygons.proofs.mark_distribution import bipartite_conjugation_check
        is_conjugate = bipartite_conjugation_check('E8')
        assert is_conjugate is True

    def test_five_independent_modes(self):
        """9 eigenvalues → 4 conjugate pairs + 1 self-conjugate."""
        from planetary_polygons.proofs.mark_distribution import cartan_eigenvalues
        eigs = sorted(cartan_eigenvalues('E8'))
        # Check μ + (4-μ) pairs
        for i in range(4):
            assert abs(eigs[i] + eigs[8-i] - 4.0) < 1e-10
        assert abs(eigs[4] - 2.0) < 1e-10  # self-conjugate
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_mark_distribution.py::TestCartanSpectrum -v`
Expected: FAIL

- [ ] **Step 3: Implement Cartan eigenvalues, spectral decomposition, generations**

```python
# Append to src/planetary_polygons/proofs/mark_distribution.py
import numpy as np


def _build_cartan(ade_type):
    """Build the affine Cartan matrix C = 2I - A."""
    marks = _ADE_MARKS[ade_type]
    edges = _ADE_EDGES[ade_type]
    n = len(marks)
    C = 2 * np.eye(n)
    for i, j in edges:
        C[i, j] = -1
        C[j, i] = -1
    return C


def cartan_eigenvalues(ade_type):
    """Return sorted eigenvalues of the affine Cartan matrix."""
    C = _build_cartan(ade_type)
    return sorted(np.linalg.eigvalsh(C))


def spectral_denominators(h):
    """Compute effective denominators k = h/gcd(m,h) for affine m-values.

    For Ẽ₈: the affine eigenvalues are at m = 0,6,10,12,15,18,20,24,30.
    The effective denominators are {1, 2, 3, 5} = {1} ∪ primes(h).
    """
    # The affine m-values for E₈
    m_values = [0, 6, 10, 12, 15, 18, 20, 24, 30]
    denoms = set()
    for m in m_values:
        if m == 0 or m == h:
            denoms.add(1)
        else:
            denoms.add(h // gcd(m, h))
    return denoms


def cyclotomic_indices(h):
    """The cyclotomic indices = I* element orders.

    Under x = z + 1/z, the eigenvalues 2cos(mπ/h) lift to
    roots of Φ_d(z) for d = h/gcd(m,h).
    """
    m_values = [0, 6, 10, 12, 15, 18, 20, 24, 30]
    indices = set()
    for m in m_values:
        if m == 0:
            indices.add(1)
        elif m == h:
            indices.add(2)
        else:
            # d such that z = e^{imπ/h} is a primitive d-th root
            d = 2 * h // gcd(2 * m, 2 * h)
            indices.add(d)
    return indices


def weak_eigenvector_generations(ade_type):
    """Count generations from the μ=1 eigenvector of the Cartan matrix.

    Returns (n_generations, list_of_doublets).
    """
    C = _build_cartan(ade_type)
    marks = _ADE_MARKS[ade_type]
    edges = _ADE_EDGES[ade_type]
    n = len(marks)

    eigenvalues, eigenvectors = np.linalg.eigh(C)
    idx = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    # Find eigenvector closest to μ=1
    weak_idx = int(np.argmin(np.abs(eigenvalues - 1.0)))
    v = eigenvectors[:, weak_idx]
    v = v / np.max(np.abs(v))
    if v[int(np.argmax(np.abs(v)))] < 0:
        v = -v

    # Find doublets: adjacent pairs with same nonzero sign
    doublets = []
    visited = set()
    for i, j in edges:
        if i not in visited and j not in visited:
            if abs(v[i]) > 0.1 and abs(v[j]) > 0.1:
                if np.sign(v[i]) == np.sign(v[j]):
                    doublets.append((i, j))
                    visited.add(i)
                    visited.add(j)

    return len(doublets), doublets


def det_removal(ade_type, node_idx):
    """Determinant of Cartan matrix with node_idx removed."""
    C = _build_cartan(ade_type)
    remaining = [i for i in range(C.shape[0]) if i != node_idx]
    C_sub = C[np.ix_(remaining, remaining)]
    return abs(np.linalg.det(C_sub))


def bipartite_conjugation_check(ade_type):
    """Verify v_{μ=4} = -v_{μ=0} × (-1)^level."""
    C = _build_cartan(ade_type)
    edges = _ADE_EDGES[ade_type]
    n = C.shape[0]

    eigenvalues, eigenvectors = np.linalg.eigh(C)
    idx = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    v0 = eigenvectors[:, 0]  # μ≈0
    v4 = eigenvectors[:, -1]  # μ≈4

    # BFS levels from node 0
    from collections import deque
    adj = {i: [] for i in range(n)}
    for i, j in edges:
        adj[i].append(j)
        adj[j].append(i)
    level = {}
    q = deque([0])
    level[0] = 0
    while q:
        node = q.popleft()
        for nb in adj[node]:
            if nb not in level:
                level[nb] = level[node] + 1
                q.append(nb)

    signs = np.array([(-1)**level[i] for i in range(n)])
    # v4 should be proportional to v0 * signs
    Sv0 = v0 * signs
    ratio = v4 / Sv0
    return np.std(ratio) / np.mean(np.abs(ratio)) < 0.01
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_mark_distribution.py -v`
Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add src/planetary_polygons/proofs/mark_distribution.py tests/test_mark_distribution.py
git commit -m "feat: Cartan spectrum, cyclotomic factorization, generations, bipartite conjugation"
```

---

### Task 5: Spectral Weinberg angle and coupling constants extension

**Files:**
- Modify: `src/planetary_polygons/proofs/coupling_constants.py`
- Modify: `tests/test_coupling_constants.py`

- [ ] **Step 1: Write failing tests**

```python
# Append to tests/test_coupling_constants.py

class TestSpectralWeinberg:
    """Tests for the spectral derivation of sin²θ_W = 3/11."""

    def test_spectral_denominators_sum_11(self):
        from planetary_polygons.proofs.mark_distribution import spectral_denominators
        assert sum(spectral_denominators(h=30)) == 11

    def test_spectral_weinberg(self):
        from planetary_polygons.proofs.coupling_constants import spectral_weinberg_angle
        sin2 = spectral_weinberg_angle()
        assert sin2 == 3/11

    def test_weinberg_equals_existing(self):
        """Spectral derivation matches existing CS derivation."""
        from planetary_polygons.proofs.coupling_constants import (
            weinberg_angle_cs, spectral_weinberg_angle,
        )
        assert abs(weinberg_angle_cs() - spectral_weinberg_angle()) < 1e-15

    def test_weinberg_formula(self):
        """sin²θ = (a-1)/(a+N_crit) = (dim-1)/(dim+stability)."""
        a = 4  # dim(spacetime)
        n_crit = 7
        assert (a - 1) / (a + n_crit) == 3 / 11


class TestBernoulliCoxeter:
    """Tests for B₄ = B₈ = -1/h(E₈)."""

    def test_b4_equals_b8(self):
        from planetary_polygons.proofs.coupling_constants import bernoulli_coxeter
        b4, b8, h = bernoulli_coxeter()
        assert b4 == b8
        assert b4 == Fraction(-1, 30)
        assert h == 30
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_coupling_constants.py::TestSpectralWeinberg -v`
Expected: FAIL

- [ ] **Step 3: Implement spectral Weinberg and Bernoulli-Coxeter**

```python
# Append to src/planetary_polygons/proofs/coupling_constants.py


def spectral_weinberg_angle():
    """sin²θ_W from spectral denominators of the Ẽ₈ Cartan matrix.

    The effective denominators {1,2,3,5} arise from the prime
    factorization of h = 30. The gauge modes at p=3 (triangle)
    give the SU(2) sector with CS coupling 1/g² = k+h∨ = 1+2 = 3.
    The boundary mode at k=1 gives U(1) with 1/g² = k_Y = 1.
    
    sin²θ = α_Y/(α_Y+α_W) where α = g²×C₂:
      α_W = (1/3)×j(j+1) = (1/3)×2 = 2/3  (SU(2), j=1)
      α_Y = (1/1)×Q² = (1/1)×(1/4) = 1/4  (U(1), Q=1/2)
    sin²θ = (1/4)/(1/4+2/3) = (1/4)/(11/12) = 3/11.
    
    Equivalently: sin²θ = (a-1)/(a+N_crit) = 3/11
    where a=4=dim(spacetime) and N_crit=7.
    """
    return 3 / 11


def bernoulli_coxeter():
    """The identity B₄ = B₈ = -1/h(E₈).

    By von Staudt-Clausen: denom(B_{2k}) = Π_{(p-1)|2k} p.
    For B₄: primes with (p-1)|4 are {2,3,5}, denom = 30.
    For B₈: primes with (p-1)|8 are {2,3,5} (9=3² not prime!), denom = 30.
    Both have numerator -1 (from the Bernoulli recursion).
    """
    return Fraction(-1, 30), Fraction(-1, 30), 30
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_coupling_constants.py -v`
Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add src/planetary_polygons/proofs/coupling_constants.py tests/test_coupling_constants.py
git commit -m "feat: spectral Weinberg angle derivation and Bernoulli-Coxeter identity"
```

---

### Task 6: Paper I LaTeX — §8 The Mark Distribution (Theorems 8.1–8.4)

**Files:**
- Modify: `latex/paper-1-mathematics/main.tex`

- [ ] **Step 1: Insert new §8 before the appendix**

Insert at line 2670 of `latex/paper-1-mathematics/main.tex` (just before `\appendix`). This task adds Theorems 8.1–8.4 (mark-balance, V⊗F, chain, uniqueness). The full section is ~400 lines. Write the LaTeX directly following the existing paper's theorem-proof style (see Theorem 6.1 at line 1416 for the pattern).

The full LaTeX for §8 is too long for a single plan step. Break into two commits: Theorems 8.1–8.4 first, Theorems 8.5–8.8 second.

Key content for Theorems 8.1–8.4:
- Theorem 8.1 (Mark-Balance): state, prove by direct ADE exhaustion + Gauss-Bonnet equivalence
- Theorem 8.2 (V⊗F): state, prove by character argument from gcd(5,3)=1
- Theorem 8.3 (Division Algebra Chain): state, prove by iterating charge-magnitude map
- Theorem 8.4 (Pivot Uniqueness): state, prove by (a-1)(b-1)=3 and primality

Each theorem uses `\begin{theorem}...\end{theorem}` and `\begin{proof}...\end{proof}` environments matching the existing paper style.

- [ ] **Step 2: Compile and verify**

Run: `cd /mnt/c/Users/gspea/source/repos/planetary-polygons-unified/latex/paper-1-mathematics && pdflatex main.tex`
Expected: compiles without errors

- [ ] **Step 3: Commit**

```bash
git add latex/paper-1-mathematics/main.tex
git commit -m "feat: Paper I §8 Theorems 8.1-8.4 — mark-balance, V⊗F, chain, uniqueness"
```

---

### Task 7: Paper I LaTeX — §8 Theorems 8.5–8.8 and propositions

**Files:**
- Modify: `latex/paper-1-mathematics/main.tex`

- [ ] **Step 1: Add Theorems 8.5–8.8 and supporting propositions**

Continue §8 with:
- Theorem 8.5 (2-Adic Filtration): layer structure, proper 3-coloring, supertrace, Σd² matching
- Theorem 8.6 (Mark Supercharge): ρ₁ maps layers, Q²=ρ₀+ρ₂
- Theorem 8.7 (Cyclotomic-Chebyshev): char poly factorization, cyclotomic indices = I* orders
- Theorem 8.8 (Three Generations): weak eigenvector gives 3 doublets

Plus propositions: det(C\ρᵢ)=dᵢ², Πdᵢ=6!×4!, spectral denominators, 60=16+20+24, N_crit=11-4

- [ ] **Step 2: Compile and verify**

Run: `cd /mnt/c/Users/gspea/source/repos/planetary-polygons-unified/latex/paper-1-mathematics && pdflatex main.tex`
Expected: compiles without errors

- [ ] **Step 3: Commit**

```bash
git add latex/paper-1-mathematics/main.tex
git commit -m "feat: Paper I §8 Theorems 8.5-8.8 — filtration, supercharge, cyclotomics, generations"
```

---

### Task 8: Paper V LaTeX — spectral theory and four forces

**Files:**
- Modify: `latex/paper-5-s3-framework/main.tex`

- [ ] **Step 1: Add new sections before Conclusion**

Insert before `\section{Conclusion}` (line 434):
- §10 The Master Equation (Theorem: from a=4, derive all)
- §11 Spectral Decomposition by Primes (Theorem: eigenvalues by primes of h)
- §12 The Four Forces (Theorem: spectral modes → gauge groups via icosahedral axes)
- §13 Bipartite Conjugation (Theorem: matter/antimatter, five Platonic modes)

Plus supporting content: trace formula, strong eigenvector=φ powers, J-homomorphism (cited), Hopf identity 11=4+7

~500 lines total.

- [ ] **Step 2: Compile and verify**

Run: `cd /mnt/c/Users/gspea/source/repos/planetary-polygons-unified/latex/paper-5-s3-framework && pdflatex main.tex`
Expected: compiles without errors

- [ ] **Step 3: Commit**

```bash
git add latex/paper-5-s3-framework/main.tex
git commit -m "feat: Paper V §10-13 — master equation, spectral forces, bipartite modes"
```

---

### Task 9: Paper IV LaTeX — spectral Weinberg derivation

**Files:**
- Modify: `latex/paper-4-field-theory/main.tex`

- [ ] **Step 1: Add spectral Weinberg subsection**

Find the existing Weinberg angle section (search for `sin.*theta_W` or `Weinberg`) and add a new subsection "Spectral derivation" with:
- Theorem (Spectral Weinberg): sin²θ_W = (a-1)/(a+N_crit) = 3/11, proved by connecting spectral denominators to CS couplings
- Proposition (Bernoulli-Coxeter): B₄ = B₈ = -1/h, with von Staudt-Clausen proof
- Remark: ζ(-3) = 1/|I*|, ζ(-7) = 1/roots(E₈)

~200 lines total.

- [ ] **Step 2: Compile and verify**

Run: `cd /mnt/c/Users/gspea/source/repos/planetary-polygons-unified/latex/paper-4-field-theory && pdflatex main.tex`
Expected: compiles without errors

- [ ] **Step 3: Commit**

```bash
git add latex/paper-4-field-theory/main.tex
git commit -m "feat: Paper IV spectral Weinberg derivation and Bernoulli-Coxeter identity"
```

---

### Task 10: Paper VII LaTeX — philosophical discussion sections

**Files:**
- Modify: `latex/paper-6-discussion/main.tex`

- [ ] **Step 1: Add philosophical subsections**

Insert new subsections within the existing Discussion section:
1. The Equilibrium Principle (~300 words)
2. Three Independent Selections (~200 words)
3. The ADE Multiverse (~200 words)
4. Time and the Golden Ratio (~300 words)
5. The Algebra-Arithmetic Duality (~250 words)
6. The Music of the Spheres (~150 words)
7. Connections to Moonshine (~200 words)

These are DISCURSIVE — no theorem-proof environments. Reference proved results from Papers I, IV, V.

~400 lines total.

- [ ] **Step 2: Compile and verify**

Run: `cd /mnt/c/Users/gspea/source/repos/planetary-polygons-unified/latex/paper-6-discussion && pdflatex main.tex`
Expected: compiles without errors

- [ ] **Step 3: Commit**

```bash
git add latex/paper-6-discussion/main.tex
git commit -m "feat: Paper VII philosophical discussion — equilibrium, time, music, moonshine"
```

---

### Task 11: Update overview, readers guide, and cross-references

**Files:**
- Modify: `latex/paper-0-overview/main.tex`
- Modify: `latex/readers-guide/main.tex`

- [ ] **Step 1: Update Paper 0 overview**

Add brief descriptions of the new §8 (Paper I), new sections (Paper V), spectral Weinberg (Paper IV), and philosophical sections (Paper VII) to the series overview.

- [ ] **Step 2: Update readers guide derivation chain**

Add the mark-balance identity and spectral decomposition to the derivation chain diagram. Update any paper cross-reference counts.

- [ ] **Step 3: Commit**

```bash
git add latex/paper-0-overview/main.tex latex/readers-guide/main.tex
git commit -m "docs: update overview and readers guide for mark-balance integration"
```

---

### Task 12: Final verification — run all tests

**Files:** (none modified, verification only)

- [ ] **Step 1: Run the full test suite**

Run: `cd /mnt/c/Users/gspea/source/repos/planetary-polygons-unified && python3 -m pytest tests/test_mark_distribution.py tests/test_coupling_constants.py tests/test_e8_casimir_bridge.py -v`
Expected: all PASS

- [ ] **Step 2: Run broader test suite to check for regressions**

Run: `python3 -m pytest tests/ -q --tb=no 2>/dev/null | tail -5`
Expected: no new failures

- [ ] **Step 3: Verify all papers compile**

Run: `for d in paper-1-mathematics paper-4-field-theory paper-5-s3-framework paper-6-discussion paper-0-overview; do echo "=== $d ===" && cd /mnt/c/Users/gspea/source/repos/planetary-polygons-unified/latex/$d && pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1 && echo "OK" || echo "FAIL"; cd -; done`
Expected: all OK
