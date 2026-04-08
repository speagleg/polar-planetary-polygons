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
