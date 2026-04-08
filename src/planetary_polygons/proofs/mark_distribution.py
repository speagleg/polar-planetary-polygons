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
    'E6': [1, 1, 2, 2, 3, 2, 1],
    'E7': [1, 2, 3, 4, 3, 2, 1, 2],
    'E8': [1, 2, 3, 4, 5, 6, 4, 2, 3],
}

# Affine Dynkin diagram edges (0-indexed nodes)
_ADE_EDGES = {
    'D4': [(0, 2), (1, 2), (2, 3), (2, 4)],
    'D5': [(0, 2), (1, 2), (2, 3), (3, 4), (3, 5)],
    'D6': [(0, 2), (1, 2), (2, 3), (3, 4), (4, 5), (4, 6)],
    'E6': [(0, 3), (1, 2), (2, 3), (3, 4), (4, 5), (3, 6)],
    'E7': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (3, 7)],
    'E8': [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (5, 8)],
}


def ade_marks(ade_type):
    """Return affine marks for the given ADE type."""
    return list(_ADE_MARKS[ade_type])


def ade_edges(ade_type):
    """Return edges of the affine Dynkin diagram."""
    return list(_ADE_EDGES[ade_type])


def mark_balance(marks):
    """Compute Σd(d-k₁) and the pivot k₁ = Σd²/Σd.

    Returns (balance_value, k1). If k₁ is not an integer,
    balance_value is computed at the nearest integer pivot (4)
    to test the E₈-specific identity.
    """
    s1 = sum(marks)
    s2 = sum(d**2 for d in marks)
    k1 = Fraction(s2, s1)
    if k1.denominator == 1:
        balance = sum(d * (d - int(k1)) for d in marks)
    else:
        # Test at pivot 4 (the E₈ value)
        balance = sum(d * (d - 4) for d in marks)
    return balance, k1


# =====================================================================
# V⊗F theorem
# =====================================================================

def vtensor_f_multiplicity(V, F, stab_V, stab_F, group_order):
    """Check if V⊗F = k × reg(G) for a Platonic solid.

    V⊗F is a multiple of the regular representation iff
    gcd(|Stab_V|, |Stab_F|) = 1. If so, returns k = V*F/|G|.
    """
    if gcd(stab_V, stab_F) != 1:
        return None
    return (V * F) // group_order


# =====================================================================
# Charge-magnitude chain
# =====================================================================

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
    while len(set(current)) > 1:
        s1 = sum(current)
        s2 = sum(d**2 for d in current)
        k1 = Fraction(s2, s1)
        if k1.denominator != 1:
            break
        pivot = int(k1)
        target, kernel = charge_magnitude_map(current, pivot)
        chain.append({'pivot': pivot, 'target': target, 'kernel': kernel})
        current = target
    if current and len(set(current)) == 1:
        chain.append({'pivot': current[0], 'target': [], 'kernel': current})
    return chain


# =====================================================================
# Pivot uniqueness
# =====================================================================

def sum_equals_product_minus_one(max_a=20):
    """Find all (a,b,c) with a≥b≥c≥1 and a+b+c = abc-1."""
    solutions = []
    for a in range(1, max_a + 1):
        for b in range(1, a + 1):
            for c in range(1, b + 1):
                if a * b * c - a - b - c == 1:
                    solutions.append((a, b, c))
    return solutions


# =====================================================================
# 2-adic filtration
# =====================================================================

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


# =====================================================================
# Mark supercharge
# =====================================================================

def mark_supercharge_squared():
    """ρ₁⊗ρ₁ = ρ₀+ρ₂ from SU(2): 2⊗2 = 1⊕3. Return their dims."""
    return 1, 3


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
