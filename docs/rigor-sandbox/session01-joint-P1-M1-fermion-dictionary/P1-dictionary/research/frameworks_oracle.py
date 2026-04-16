"""
Framework oracle: systematically test candidate KK → SM-fermion dictionaries.
=============================================================================

For each candidate framework F1..F8 (see RESEARCH_PLAN.md), generate the
implied fermion content as a list of WeylFermion entries, then check:

  1. Total Weyl count per generation == 16 (SM + ν_R)
  2. All 5 SM anomaly traces vanish
  3. SM rep content matches Q_L + u_R + d_R + L_L + e_R + ν_R

Frameworks tested here (incremental — add as we go):

  F1: m_4-decoloration
      m_4 ∈ {1, 2}  (up-type, μ_4 = 1/2):  SU(3) rep = Frobenius orbit
      m_4 ∈ {0, 3}  (down-type, μ_4 = 3/2): SU(3) rep = singlet

Run: python3 frameworks_oracle.py
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from pathlib import Path
from typing import List, Optional

# Import the SM oracle from the parent directory
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))
from oracle import (  # type: ignore
    WeylFermion, SM_GENERATION,
    trace_Y, trace_Y3, trace_T3sq_Y, trace_Csu3_Y, trace_Csu3_3,
    check_anomalies, is_anomaly_free,
    frobenius_orbit,
)


# -------------------------------------------------------------
# Structural inputs from Paper IV / V
# -------------------------------------------------------------

N_COLOR = 7    # polygon for SU(3)
N_ISOSPIN = 4  # polygon for SU(2)

FERMION_M7_PAIRS = [(1, 6), (2, 5), (3, 4)]   # three generations (Paper V Cor. 4)

# Fermion KK mass on N=4: μ₄^f = |m₄ − 3/2|
#   m₄ = 1, 2  →  μ₄ = 1/2  ("up-type")
#   m₄ = 0, 3  →  μ₄ = 3/2  ("down-type")
M4_UP_MODES = {1, 2}
M4_DOWN_MODES = {0, 3}

# Chirality: ±1 (left-handed ↔ −1, right-handed ↔ +1 in one common convention;
# use just ±1 abstractly here)
CHIRALITIES = [+1, -1]


# -------------------------------------------------------------
# Utilities
# -------------------------------------------------------------

def sm_multiset(fields: List[WeylFermion]) -> dict:
    """Return dict {(color_rep, isospin, Y): multiplicity_in_Weyl_count}.

    color_rep: 3, -3 (for 3̄), or 1
    isospin:   2 or 1
    Y:         hypercharge (Fraction)
    """
    counts: dict = {}
    for f in fields:
        key = (f.color, f.isospin, f.Y)
        counts[key] = counts.get(key, 0) + f.multiplicity
    return counts


def sm_target() -> dict:
    return sm_multiset(SM_GENERATION + [
        WeylFermion(color=0, isospin=1, Y=Fraction(0), label="ν_R^c")
    ])


def total_weyl(fields: List[WeylFermion]) -> int:
    return sum(f.multiplicity for f in fields)


def report_framework(name: str, fields: List[WeylFermion],
                     target_per_generation: dict,
                     n_generations: int = 3) -> bool:
    print(f"\n{'=' * 72}")
    print(f"Framework: {name}")
    print(f"{'=' * 72}")

    n_weyl = total_weyl(fields)
    print(f"  Total Weyl: {n_weyl}  (target: {16 * n_generations} "
          f"for {n_generations} generations of SM+ν_R)")

    anom = check_anomalies(fields, label=name)
    ok_anom = is_anomaly_free(anom)
    print(f"\n  Anomaly-free: {ok_anom}")

    # Compare multiset to n_generations × SM+ν_R target
    got = sm_multiset(fields)
    expected = {k: v * n_generations for k, v in target_per_generation.items()}
    print("\n  Content comparison (got vs expected):")
    all_keys = sorted(set(got.keys()) | set(expected.keys()),
                      key=lambda k: (k[0], k[1], float(k[2])))
    match = True
    for key in all_keys:
        g = got.get(key, 0)
        e = expected.get(key, 0)
        flag = "✓" if g == e else "✗"
        color_name = {1: "3  ", -1: "3bar", 0: "1  "}[key[0]]
        print(f"    {flag} (color={color_name}, T={key[1]}, Y={key[2]}): "
              f"got {g:>3d}, expected {e:>3d}")
        if g != e:
            match = False

    if ok_anom and match and n_weyl == 16 * n_generations:
        print(f"\n  ✓✓✓ FRAMEWORK PASSES: anomaly-free AND matches SM content.")
        return True
    else:
        print(f"\n  ✗ Framework FAILS on at least one criterion.")
        return False


# -------------------------------------------------------------
# Framework F1: m_4-decoloration
# -------------------------------------------------------------
# Rule: (m_7, m_4, χ) → Weyl fermion with
#   SU(3) rep:   frobenius_orbit(m_7) if m_4 ∈ M4_UP_MODES
#                1 (singlet)          if m_4 ∈ M4_DOWN_MODES
#   SU(2) rep:   TBD (parametrized — try: doublet if m_4 ∈ {1, 2}, singlet otherwise?)
#   Y:           TBD (search for a linear formula Y(m_7, m_4, χ) that
#                gives anomaly cancellation)
# -------------------------------------------------------------

def framework_F1_enumerate(
    su2_doublet_pairs_m4: List[frozenset],    # e.g. [frozenset({1, 3}), ...] — which m_4 subsets form SU(2) doublets
    y_formula,                                  # function (m_7, m_4, chi) -> Fraction
    color_rule,                                 # function (m_7, m_4) -> int in {-1, 0, +1}
    chirality_lock: Optional[dict] = None,      # optional: restrict which (m_7_orbit, m_4) give which χ
) -> List[WeylFermion]:
    """Enumerate all (m_7, m_4, χ) and build Weyl fermion list under F1."""
    fields: List[WeylFermion] = []
    for m7 in range(N_COLOR):
        for m4 in range(N_ISOSPIN):
            col = color_rule(m7, m4)
            # SU(2) assignment: is (m4) in a doublet orbit?
            iso = None
            for pair in su2_doublet_pairs_m4:
                if m4 in pair:
                    # Doublet: we count the PAIR as one SU(2) doublet field.
                    # To avoid double-counting, only count once (use the smaller element).
                    if m4 != min(pair):
                        iso = "skip"
                    else:
                        iso = 2
                    break
            if iso is None:
                iso = 1
            if iso == "skip":
                continue
            assert isinstance(iso, int)
            for chi in CHIRALITIES:
                if chirality_lock is not None:
                    locked_chi = chirality_lock.get((col, m4), None)
                    if locked_chi is not None and locked_chi != chi:
                        continue
                Y = y_formula(m7, m4, chi)
                # For a triplet: the single m_7 within an orbit represents
                # the full 3-rep. So when we enumerate m_7 ∈ O+, we need
                # to count only ONE m_7 per orbit (not 3).
                if col != 0:
                    # Pick a canonical representative for each Frobenius orbit
                    if col == +1:
                        if m7 != min({1, 2, 4}):
                            continue
                    else:  # col == -1
                        if m7 != min({3, 5, 6}):
                            continue
                fields.append(WeylFermion(
                    color=col, isospin=iso, Y=Y,
                    label=f"(m7={m7}, m4={m4}, chi={'+' if chi>0 else '-'})"
                ))
    return fields


def try_F1_basic():
    """A first pass at F1 with the simplest assumptions.

    Rules:
    - SU(3) = Frobenius orbit when m_4 ∈ {1, 2} (up-type); singlet otherwise.
    - SU(2) = doublet when m_4 ∈ {1, 2} (one pair, adjacent modes); singlet otherwise.
    - Y = (m_7 − N_C/2)/N_C + (m_4 − N_I/2)/N_I  ← linear ansatz
    - No chirality lock (both chiralities contribute).
    - Use one canonical representative per Frobenius orbit to avoid triple-counting.
    """
    def y_formula(m7, m4, chi):
        # Linear ansatz for Y
        return Fraction(m7, N_COLOR) + Fraction(m4, N_ISOSPIN) - Fraction(1, 2)

    def color_rule(m7, m4):
        if m4 in M4_UP_MODES:
            return frobenius_orbit(m7)
        else:
            return 0  # singlet

    # SU(2) doublet: m_4 ∈ {1, 2} forms ONE doublet (up-type gets doublet)
    fields = framework_F1_enumerate(
        su2_doublet_pairs_m4=[frozenset({1, 2})],
        y_formula=y_formula,
        color_rule=color_rule,
    )
    return fields


def main():
    print("Framework oracle — test candidate KK→SM-fermion dictionaries\n")

    # Reference: SM+ν_R per generation
    target = sm_target()
    print("Target content per generation (SM+ν_R):")
    for (col, iso, Y), mult in sorted(target.items(),
                                       key=lambda x: (x[0][0], x[0][1], float(x[0][2]))):
        color_name = {1: "3", -1: "3bar", 0: "1"}[col]
        print(f"    ({color_name}, T={iso}, Y={Y}): {mult} Weyl")
    print(f"  Total: {sum(target.values())} Weyl")

    # F1 basic test
    fields = try_F1_basic()
    report_framework("F1 (basic: m_4-decoloration + linear Y ansatz)",
                     fields, target, n_generations=3)


if __name__ == "__main__":
    main()
