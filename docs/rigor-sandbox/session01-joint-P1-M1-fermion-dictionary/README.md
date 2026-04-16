# Session 1 (joint P1 + M1): KK chirality & fermion dictionary

**Date**: 2026-04-16
**Scope**: Issues **M1** (γ⁵ Clifford decomposition) and **P1** (KK-mode → Weyl-fermion dictionary) from `docs/PAPER4_RIGOROUS_DERIVATION_PLAN.md`.
**Rationale for joint scope**: the chirality projector γ⁵ determines which KK modes become L vs R Weyl fermions in 4D — this is the mode-counting input P1 needs. Doing P1 without M1 locked first forces unverified guesses about the projection structure. Gordon confirmed joint scope 2026-04-16.

## Layout

```
session01-joint-P1-M1-fermion-dictionary/
├── README.md                    # this file
├── M1-chirality/                # γ⁵ action on KK modes
│   ├── derivation.md            # formal computation + result
│   ├── clifford_oracle.py       # sympy/numpy verification of γ matrices
│   └── review-notes.md          # reviewer feedback
└── P1-dictionary/               # (m_7, m_4, χ) → SM Weyl fermion map
    ├── derivation.md            # exploration report (current) / derivation (final)
    ├── oracle.py                # anomaly check over candidate dictionaries
    └── review-notes.md          # reviewer feedback
```

## Sequencing

1. **M1 first** (self-contained Clifford computation): determine the explicit action of γ⁵ on 4D Dirac KK modes on R × H² × S¹. Verify or refute the paper's claim `γ⁵ → γ^(3) · e^{iπm}` in the KK basis (§8.1 Step 2, lines 975–981 of `latex/paper-4-field-theory/main.tex`).
2. **P1 second**: with the M1 chirality structure fixed, build and verify the (m_7, m_4, χ) → (SU(3), SU(2), Y) dictionary. Address the 56 vs 48 Weyl counting gap identified in the exploration report.
3. **Review gate**: dispatch physics-reviewer AND math-reviewer on the combined deliverable once both M1 and P1 derivations are stable.
4. **Integration deferred**: Gordon decides paper integration AFTER reviewer sign-off.

## Current status

- **M1**: to start.
- **P1**: exploration report complete (`P1-dictionary/derivation.md`), oracle validated against SM reference (`P1-dictionary/oracle.py`). Blocked on M1 for chirality structure.
