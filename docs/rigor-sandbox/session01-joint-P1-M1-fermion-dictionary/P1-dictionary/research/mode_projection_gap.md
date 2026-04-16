# Major gap identified: mode projection selection rule

**Date**: 2026-04-16
**Issue**: working on G1 (SU(2)_L/R m_4 assignment derivation) revealed a deeper unresolved gap — a **selection rule projecting 40 of 56 KK modes out of the SM matter content**.

## The counting

**Full KK mode space per cusp (per generation)**:
- 7 m_7 values (on N=7 color sector)
- 4 m_4 values (on N=4 isospin sector)
- 2 chiralities (χ = L, R)
- Total: 7 × 4 × 2 = **56 Weyl modes per cusp**

**SM+ν_R matter per generation**: 16 Weyl.

**Projected modes per cusp**: 56 − 16 = **40 Weyl modes projected out**.

## The 16 used modes (from our dictionary)

In (4, 2, 1)_L: m_7 ∈ {0, 1, 2, 4} × m_4 ∈ {1, 2}, χ = L. 8 modes.
In (4̄, 1, 2)_L: m_7 ∈ {0, 3, 5, 6} × m_4 ∈ {0, 3}, χ = L. 8 modes.

Note: m_4 ∈ {1, 2} in (4, 2, 1) means these modes form an SU(2)_L doublet.
m_4 ∈ {0, 3} in (4̄, 1, 2) means these form an SU(2)_R doublet.

## The 40 projected modes per cusp

1. **All 28 χ=R modes** (Redlich parity anomaly, paper §8.1):
   - A^- CS sector gapped at m_R ~ 107 TeV
   - 28 χ=R modes projected out at low energy

2. **12 χ=L "wrong structure" modes**:
   - m_7 ∈ O+ (color 3) × m_4 ∈ {0, 3}: 3 × 2 = 6 modes
     - These would be "(3, 1, 2)" = colored SU(2)_R doublet. NOT in SM.
   - m_7 ∈ O- (color 3̄) × m_4 ∈ {1, 2}: 3 × 2 = 6 modes
     - These would be "(3̄, 2, 1)" = anti-colored SU(2)_L doublet. NOT in SM.

**The Redlich mechanism accounts for #1 (28 χ=R modes) naturally.**

**The 12 χ=L wrong-structure modes are NOT explained by Redlich.** They would need an ADDITIONAL projection mechanism.

## Structure of the 12 unprojected-but-absent modes

The correlation "O+ pairs with m_4 ∈ {1, 2}" (and "O- pairs with m_4 ∈ {0, 3}") is NOT derivable from:
- Simple mod-7 selection (checked: used mode residues mod 7 are not uniform)
- Simple mod-4 selection (checked: residues mod 4 ARE uniform)
- Simple mod-28 selection (checked: used residues don't form a coset)
- CP symmetry (checked: used and unused sets are both CP-closed)

Under σ_{28} = (σ_7, σ_4) CP-like action:
```
σ_{28}(O+ × {0, 3}) = (O- × {1, 2})
σ_{28}(O- × {1, 2}) = (O+ × {0, 3})
```
Both "used" and "unused" sets are CP-closed separately.

## Structural observation

The used modes have a CORRELATION between m_7 (color) and m_4 (isospin):
- "O+ correlates with m_4 ∈ {1, 2}"
- "O- correlates with m_4 ∈ {0, 3}"
- "m_7 = 0 allows both m_4 sets"

This is a LINKED color-isospin structure that doesn't factorize into m_7-only and m_4-only projections.

## Impossible to derive?

In Pati-Salam-like UV theory: the matter content (4, 2, 1) + (4̄, 1, 2) is POSTULATED (not derived). The "which m_4 is SU(2)_L vs SU(2)_R" is a choice within PS rep theory, not a derivation.

For the polygon theory to DERIVE this structure, we'd need a projection/selection mechanism that:
1. Keeps exactly the 16 "correct" modes per cusp
2. Projects out the 12 "wrong" modes
3. Arises naturally from polygon geometry (not imposed)

**Candidate mechanisms** (not yet derived):
- **Combined Z_7 × Z_4 orbifold**: the Z_{28} common overfield might have a specific Wilson line or modding that correlates m_7 and m_4.
- **4D chirality projection**: the SIGN of (m_7 - 3) × SIGN of (m_4 - 3/2) might select the correct modes.
- **Non-trivial global SECTOR STRUCTURE**: the polygon theory might have only the "diagonal" sector of Z_7 × Z_4, not the full product.

## Implications for the framework

**Significant**: without a selection mechanism for the 12 extra χ=L modes, the polygon theory as currently derived in the paper gives:
- 28 + 12 = 40 χ=L Weyl per cusp (instead of 16)
- + 28 χ=R Weyl per cusp (possibly gapped by Redlich)

This would mean the SM matter content is NOT cleanly reproduced from the paper's derivations — the 12 extra χ=L modes would be PHYSICAL and give non-SM fermion content.

**Unless**: these 12 extras are projected by some mechanism not yet identified. Our dictionary implicitly assumes this projection.

## Gap status: OPEN and structural

This is a real, structural gap in the framework. Unlike other gaps (quark K^n, PMNS fractions, etc.), this one affects the CORE MATTER CONTENT.

Priority: HIGH — need to identify the projection mechanism for a coherent framework.

Possible resolutions:
1. Find the orbifold selection rule in the polygon theory's construction
2. Accept the 12 extra modes and modify SM matter content predictions accordingly
3. Discover a new geometric/dynamical argument that excludes these modes

## Impact on Paper IV revision

The Paper IV revision draft (and Session 1 conclusions) need to be updated:
- We cannot claim the polygon theory "derives" SM matter content as cleanly as I initially described
- The mapping (m_7, m_4, χ) → SM fermion has an UNDERIVED SELECTION that picks 16 of 40 χ=L modes
- This selection is consistent with PS-style rep assignment but not derived from polygon structure

This is a MORE SIGNIFICANT gap than I initially identified. It needs closure for a truly unified framework.

## Updated framework status

Previously claimed: 11 verifications, with only technical gaps remaining.

Actually: the 11 verifications are correct GIVEN the correct matter content (the 16 modes per cusp). But the DERIVATION of which 16 modes corresponds to SM content is NOT in the paper or our session work.

This is a significant setback that requires further investigation.
