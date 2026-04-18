# Session 24d — ℤ_7 torsion flux moduli-dependence derivation

**Status**: Derivation complete. NEGATIVE result — all channels parallel to existing terms.
Session 18 §R.28.4 was right but attributed to wrong term (not A_F, rather A_C^fib and A_R).

## §1. Setup

Seifert M_3 = S¹ → M_3 → H²/Z_7 has H²(M_3; ℤ) = ℤ ⊕ ℤ_7. The ℤ factor was
tested in Session 18 §R.24-R.30 as continuous H-flux (scaling (-3,-6), parallel
to Λ_7). This session tests the ℤ_7 TORSION factor.

Physical realization: flat B-field with holonomy 2πt/7 around the torsion 2-cycle
γ_tors ⊂ M_3. Since 7t = 0, representative satisfies 7B_t = dΛ globally — B_t is
flat (dB_t = 0) but non-trivial in cohomology.

## §2. Kinetic term vanishes

For B_t flat: S_kin = (1/4·3!) ∫ √g_7 |dB_t|² = 0. The continuous-flux mechanism
(V_H ∝ p²/(α³γ⁶)) does not apply. Any t-dependence must come from topological
or holonomy/twisted-boundary-condition effects.

## §3. Five channels enumerated

### Channel A: WZ coupling B ∧ X_5

Possible 7D coupling: S_WZ = (1/(2π)) ∫_{M_3 × Σ_4} B ∧ X_5(F, R).

- X_5 = (1/2) F ∧ F (FR flux): F ∧ F pairs with 4-cycles, not 2-cycles.
  Zero for smooth FR flux. **Vanishes.**
- X_5 = tr(R ∧ R)/(8π²) (gravitational): gives (t/7)·(topological χ-invariant) ·
  pure number. **Scaling (0, 0), constant shift to V_*.**

### Channel B: Flat Wilson line around fiber

Torsion ↔ flat abelian connection with holonomy e^(2πit/7) around S¹_fiber.
Twists KK mass spectrum: n/L_fiber → (n + t/7)/L_fiber.

One-loop fiber Casimir with Wilson line a = t/7:
    E_Cas^fib(a) ∼ (1/L_fib⁴) · Re[ζ_H(-3; a) - ζ_H(-3; 0)]
               ∼ (t/7)² · 1/α⁴ (leading small-a)

The twist MULTIPLIES the fiber Casimir expression by [1 + c·(t/7)² + O((t/7)⁴)],
preserving its scaling. **Scaling (-6, -4) — PARALLEL to A_C^fib.**

Leading correction: δA_C^fib / A_C^fib ∼ (1/49) at t=1 ≈ 2%.

### Channel C: DHVW discrete torsion phase

Vafa 1986: orbifold partition function admits discrete torsion phases in
H²(G; U(1)). For G = ℤ_7:
    H²(ℤ_7; U(1)) = 0

(Schur multipliers of prime-order cyclic groups vanish.)

**Channel C FORBIDDEN.**

### Channel D: Cone-point Wilson lines

Equivalent to Channel B (gauge redundancy between "continuous Wilson line" and
"flux localized at cone points" — both realize the same ℤ_7 torsion class).

**Same as Channel B: (-6, -4), parallel to A_C^fib.**

### Channel E: Base-Laplacian twist

Torsion class acts on base-propagating scalars via flat connection on Σ:
    Δ_Σ → Δ_Σ + (2π t/(7γ))² · P_charged

where P_charged projects onto 1/7 of modes.

Twisted base Casimir expansion:
    δE_Cas^base(t) ≈ (1/2)·(4π² t²/(49γ²))·A_Σ·b_0·(1/7)
                  ≈ C_E · t²  (γ-independent: the γ² in A_Σ cancels the 1/γ² twist)

Post fiber integration and Weyl rescaling:
    V_t^(E) = (2π C_E/K²) · t² · α^(-1) γ^(-4)

**Scaling (-1, -4) — PARALLEL to A_R (base Ricci).**

Coefficient: δA_R/A_R ≈ 0.5% at t=1. Sub-dominant.

### Channel F: Seifert linking form

Non-degenerate Q: ℤ_7 × ℤ_7 → ℚ/ℤ with Q(1,1) = 1/14. Enters partition function
as phase e^(2πi Q(t,t)·t²) multiplying each torsion sector.

**Superselection phase, NOT an additive V term.**

## §4. Summary table

| Channel | Scaling | Parallel to | Coefficient at t=1 |
|---|---|---|---|
| A (WZ) | (0,0) or zero | constant | shifts V_* only |
| B (fiber Wilson) | (-6,-4) | A_C^fib | ~2% renorm |
| C (DHVW) | forbidden | H²(Z_7;U(1))=0 | zero |
| D (cone Wilson) | (-6,-4) | A_C^fib (=B) | same as B |
| E (base twist) | (-1,-4) | A_R | ~0.5% renorm |
| F (linking) | phase | not potential | — |

**Every channel parallel to existing term.** §R.28.4 dismissal was correct but
attributed to wrong term. **Corrected**: torsion renormalizes A_C^fib and A_R
(not A_F) by ~1-2%. No new scaling direction.

## §5. Session 23 stable-region comparison

All ℤ_7 torsion channels are explicitly excluded by Session 23's `is_parallel`
filter (line 108). None of the 33 stable directions can be reached by ℤ_7
torsion.

Small coefficient renormalizations (1-2%) cannot cure the tachyon (Session 22
demonstrated robust persistence across |C_base| ∈ [0.05, 0.30]).

## §6. Corrected §R.28.4 statement

Session 18 §R.28.4 wrote:
> "Seifert torsion flux renormalizes A_F... Does not help."

Corrected statement:
> **"Seifert torsion flux renormalizes A_C^fib (by ~2%) and A_R (by ~0.5%) via
> Wilson-line twists on fiber and base respectively. Neither renormalization is
> large enough to resolve the tachyon, and neither introduces a new scaling
> direction. The FR mechanism is NOT involved (wrong dimensional pairing).
> DHVW discrete torsion is forbidden (H²(ℤ_7; U(1))=0)."**

## §7. Final summary

1. **Scaling (p_torsion, q_torsion)**: no single scaling — multiple channels at
   (-6,-4), (-1,-4), (0,0). All parallel to existing.
2. **In Session 23 stable region?** No.
3. **Coefficient at t=1**: 1-2% renormalization of A_C^fib and A_R.
4. **Is this the mechanism?** No.

## References

- Session 18 §R.24-R.30, §R.28.4 (partially corrected here)
- Session 23 scan_generic.py lines 105-112 (parallel exclusion)
- Vafa 1986 "Modular invariance and discrete torsion" Nucl. Phys. B 273, 592
- Dixon-Harvey-Vafa-Witten 1985-86 "Strings on orbifolds"
- Freed 1986 "Determinants, torsion, and strings"
