"""
Session 1 (P1) numerical oracle
================================

Purpose: discover the KK-mode → SM Weyl-fermion dictionary consistent with
(a) the derived SU(3)/SU(2)/U(1) structure in Paper IV, and
(b) standard SM anomaly cancellation.

This oracle does NOT assume the final dictionary. It explores candidate
families of assignment rules and checks which (if any) satisfy the
five anomaly-cancellation conditions:

  A1. Tr(Y)              = 0    [gravitational / mixed]
  A2. Tr(Y^3)            = 0    [U(1)^3]
  A3. Tr(T_3^2 * Y)      = 0    [SU(2)^2 U(1)]
  A4. Tr(T_SU3^2 * Y)    = 0    [SU(3)^2 U(1)]
  A5. Tr(T_SU3^3)        = 0    [SU(3)^3, auto from vector-like color]

The reference SM content per generation (left-handed Weyl convention):

  Q_L     = (3, 2, +1/6)        6 components
  u_R^c   = (3bar, 1, -2/3)     3 components
  d_R^c   = (3bar, 1, +1/3)     3 components
  L_L     = (1, 2, -1/2)        2 components
  e_R^c   = (1, 1, +1)          1 component
  ---
  Total: 15 Weyl fermions per generation.

We first verify the oracle's anomaly calculator on the SM reference, then
apply it to candidate dictionaries.

Run: python3 oracle.py
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from typing import Iterable, List


# -------------------------------------------------------------
# 1. Data types
# -------------------------------------------------------------


@dataclass(frozen=True)
class WeylFermion:
    """One 4D left-handed Weyl fermion (complex 2-component spinor).

    Fields are Fraction so anomalies are computed in exact arithmetic.

    color:      3 (fundamental), -3 (antifundamental/3bar), 1 (singlet)
                encoded as +1 for 3, -1 for 3bar, 0 for 1
    isospin:    2 (doublet), 1 (singlet) — dimension
    Y:          hypercharge (Fraction)
    label:      human-readable label (for reporting)
    """

    color: int                   # +1 = 3,  -1 = 3bar,  0 = singlet
    isospin: int                 # 2 or 1
    Y: Fraction
    label: str = ""

    @property
    def color_dim(self) -> int:
        return 3 if self.color != 0 else 1

    @property
    def multiplicity(self) -> int:
        """Number of 2-component complex Weyl components in this field."""
        return self.color_dim * self.isospin


def trace_Y(fields: Iterable[WeylFermion]) -> Fraction:
    return sum((Fraction(f.multiplicity) * f.Y for f in fields), Fraction(0))


def trace_Y3(fields: Iterable[WeylFermion]) -> Fraction:
    return sum(
        (Fraction(f.multiplicity) * f.Y ** 3 for f in fields), Fraction(0)
    )


def trace_T3sq_Y(fields: Iterable[WeylFermion]) -> Fraction:
    """Tr(T_3^2 * Y) over SU(2) doublets only (singlets have T_3 = 0).

    For a doublet, sum_{T_3=±1/2} T_3^2 = 2 * (1/4) = 1/2 (per color state).
    So contribution per doublet field of SU(3)-dim D: (D) * (1/2) * Y.
    """
    total = Fraction(0)
    for f in fields:
        if f.isospin == 2:
            total += Fraction(f.color_dim) * Fraction(1, 2) * f.Y
    return total


def trace_Csu3_Y(fields: Iterable[WeylFermion]) -> Fraction:
    """Tr(T^a T^a * Y) where T^a are SU(3) generators in the given rep.

    Dynkin index normalization: Tr_R(T^a T^b) = T(R) delta^{ab}.
    T(3) = T(3bar) = 1/2. Singlet contributes 0.
    Factor of 8 (dim adjoint) is common to all; we drop it since we only
    check zero.
    Contribution per field: isospin * T(R) * Y where T(R) = 1/2 for 3, 3bar.
    """
    total = Fraction(0)
    for f in fields:
        if f.color != 0:
            total += Fraction(f.isospin) * Fraction(1, 2) * f.Y
    return total


def trace_Csu3_3(fields: Iterable[WeylFermion]) -> Fraction:
    """Tr(T^a T^b T^c) anomaly coefficient A(R) — for SU(3), A(3) = +1,
    A(3bar) = -1, A(1) = 0. Counts isospin copies per color field.
    """
    total = Fraction(0)
    for f in fields:
        if f.color != 0:
            total += Fraction(f.isospin) * Fraction(f.color)  # +/- 1
    return total


# -------------------------------------------------------------
# 2. The SM reference generation — sanity check
# -------------------------------------------------------------


SM_GENERATION: List[WeylFermion] = [
    WeylFermion(color=+1, isospin=2, Y=Fraction(1, 6),  label="Q_L"),
    WeylFermion(color=-1, isospin=1, Y=Fraction(-2, 3), label="u_R^c"),
    WeylFermion(color=-1, isospin=1, Y=Fraction(+1, 3), label="d_R^c"),
    WeylFermion(color=0,  isospin=2, Y=Fraction(-1, 2), label="L_L"),
    WeylFermion(color=0,  isospin=1, Y=Fraction(+1),    label="e_R^c"),
]


def check_anomalies(fields: List[WeylFermion], label: str = "") -> dict:
    """Compute all five anomaly traces. Return dict of results."""
    results = {
        "Tr(Y)":          trace_Y(fields),
        "Tr(Y^3)":        trace_Y3(fields),
        "Tr(T3^2 Y)":     trace_T3sq_Y(fields),
        "Tr(C_SU3 Y)":    trace_Csu3_Y(fields),
        "Tr(C_SU3^3)":    trace_Csu3_3(fields),
        "N_Weyl":         sum(f.multiplicity for f in fields),
    }
    if label:
        print(f"\n=== {label} ===")
        for k, v in results.items():
            print(f"  {k:20s} = {v}")
    return results


def is_anomaly_free(results: dict) -> bool:
    return all(
        results[k] == 0
        for k in ("Tr(Y)", "Tr(Y^3)", "Tr(T3^2 Y)", "Tr(C_SU3 Y)", "Tr(C_SU3^3)")
    )


# -------------------------------------------------------------
# 3. Candidate dictionary builder
# -------------------------------------------------------------
#
# Encoding the polygon-theory inputs:
#
# For N=7 (color sector), Frobenius orbits under m ↦ 2m mod 7:
#   {0}           → SU(3) singlet          (1)
#   {1, 2, 4}=O+  → SU(3) fundamental      (3)
#   {3, 5, 6}=O-  → SU(3) antifundamental  (3bar)
#
# For N=4 (isospin sector), σ_4: m_4 ↦ 4−m_4 orbits:
#   {0}           → CP fixed (if non-self)
#   {2}           → CP fixed (critical, j=1 adjoint of SU(2))
#   {1, 3}        → CP pair  → natural candidate for SU(2) doublet 2
#
# A single KK mode pair (m_7, m_4) is characterized by:
#   - SU(3) rep from O(m_7):  singlet / 3 / 3bar
#   - potential SU(2) assignment from m_4 orbit structure
#   - hypercharge Y from KK momenta: candidate rules below
#
# Candidate SU(2) assignment rules:
#   R_SU2_A: m_4 ∈ {1,3} → doublet (size 2, treated as one field of isospin 2),
#            m_4 ∈ {0, 2} → singlet
#   R_SU2_B: m_4 = 2 is adjoint, excluded from matter. m_4 ∈ {1,3} → doublet,
#            m_4 = 0 → singlet.
#
# Candidate Y formulas (for a given mode (m_7, m_4, χ) with chirality χ = ±):
#   Y1: Y = m_4/4 − 1/2
#   Y2: Y = (m_7 + m_4)/N_total − offset for some N_total
#   Y3: Y = α·(m_7 − 7/2)/7 + β·(m_4 − 2)/4 + γ, for integer search
#   Y4: Y = m_4/4 · color_sign + ε·color_shift  (color-dependent)
#
# We use Y3 as a flexible linear search: Y = α m_7 + β m_4 + γ (Fraction coefs).
# ------------------------------------------------------------


def frobenius_orbit(m7: int) -> int:
    """Return SU(3) color: +1 (=3), -1 (=3bar), 0 (=singlet)."""
    Op = {1, 2, 4}  # quadratic residues mod 7
    Om = {3, 5, 6}  # non-residues
    if m7 == 0:
        return 0
    if m7 in Op:
        return +1
    if m7 in Om:
        return -1
    raise ValueError(f"m7 out of range: {m7}")


# -------------------------------------------------------------
# 4. Main — sanity check SM first
# -------------------------------------------------------------


def main():
    print("Sanity check: SM reference generation")
    print("======================================")
    res = check_anomalies(SM_GENERATION, label="SM reference (one generation)")
    assert is_anomaly_free(res), "SM reference failed anomaly check — bug in oracle"
    assert res["N_Weyl"] == 15, f"expected 15 Weyl per gen, got {res['N_Weyl']}"
    print("\n✓ Oracle correctly computes SM anomaly cancellation.")
    print("✓ 15 Weyl fermions per generation reproduced.")

    # Now the informative part: what does ONE generation look like if we
    # ENUMERATE modes (m_7, m_4) on N=7 × N=4 with the orbit-based SU(3)
    # assignment and an as-yet-unknown SU(2) × Y assignment?
    print("\n\nKK mode inventory on (N=7) × (N=4) at fixed m_7 pair:")
    print("=====================================================")
    print("One 'generation pair' uses m_7 in {pair_plus, pair_minus}.")
    print("Example: pair 1 = {1, 6}  →  1 ∈ O+ (color 3), 6 ∈ O- (color 3bar).")
    print()
    for (m7, m4) in product(range(7), range(4)):
        col = frobenius_orbit(m7)
        col_name = {1: "3  ", -1: "3bar", 0: "1  "}[col]
        print(f"  (m_7={m7}, m_4={m4}):  SU(3) = {col_name}")

    print("\n\nNext step: build the SU(2) assignment + hypercharge rule.")
    print("See derivation.md for the structural derivation.")


if __name__ == "__main__":
    main()
