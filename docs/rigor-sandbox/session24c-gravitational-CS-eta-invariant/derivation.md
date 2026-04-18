# Session 24c — Gravitational Chern-Simons / η-invariant contribution

**Status**: Derivation complete. NEGATIVE result — parallel to V_base direction.

## §1. Setup

Sessions 18-23 established the 5-ingredient CW+FR potential on N=7 Seifert.
Session 23 scan found stable directions require q > 0. This session tests
whether the gravitational CS action on the Seifert manifold provides a new
direction.

## §2. Inputs from Paper IV

- Internal 3-manifold: Seifert S¹ → M_3 → H²/Z_7 with Euler class e = 7/2
- Base orbifold Σ: three cone points order 7, χ_orb = -4/7, area 8π/7·γ²
- Fiber circumference: 2πα
- V_3 = K·α·γ² with K = 16π²/7

From Paper IV §5: c(7) = 12 b(7) = 51.57, k(7) = c/6 = 2·b(7) = 8.596.

## §3. CS level identification

Two candidates for k_grav:
- (a) k_grav = c/24 (Witten-Zograf framing anomaly)
- (b) k_grav = c/6 = 2 b(N) (CS level multiplying ∫ CS_3[ω])

Paper IV §7 uses (b). The framing anomaly is already absorbed in η.

**k_grav(7) = 2 b(7) = 8.596** at tree level.

1-loop η-invariant shift: η(M_3) = -(N-1)(2N-5)/(6N) = -9/7 at N=7
(Paper IV eq `eta-grav` line 1033).

k_grav,eff = 8.596 - 9/14 = 7.953.

## §4. Moduli dependence

### 4.1 Action evaluated on Seifert

Using Kirk-Klassen / Bismut-Cheeger-Dai adiabatic-limit decomposition:

    ∫_{M_3} CS_3[ω_spin] = CS_3[ω_Σ] ∧ (dφ + ω_seif) + ω_Σ ∧ F_seif + α²-terms

Integration over fiber (length 2πα) leaves topological base integral:

    ∫_{M_3} CS_3[ω] = (2πα) · (4π e χ_orb) · (1 + O(η/k))
                    = 8π² α · (7/2) · (-4/7) = -16π² α

Pre-Weyl: S_gCS^{(pre)} = (k_grav/4π) · (-16π² α) = **-4π k_grav α**.

### 4.2 Weyl rescaling

Multiplying by 1/V_3² = 1/(K² α² γ⁴):

    V_gCS(α, γ) = -4π k_grav α / (K² α² γ⁴) = **-(4π k_grav/K²) / (α γ⁴)**

**Scaling: (p_gCS, q_gCS) = (-1, -4).**

This is IDENTICAL to V_base = A_R/(αγ⁴) — parallel to the Ricci/base-CC direction.

### 4.3 Coefficient

δA_R^{gCS} = -4π k_grav/K² = -4π · 8.596 / (16π²/7)² = **-0.212** in G_7=1 units.

Compare A_R = 0.001764. The gCS correction is 120× larger and opposite sign,
giving:

    A_R^{eff} = 0.001764 - 0.212 = **-0.210**

The sign FLIPS.

## §5. Does the sign flip help?

No. Renormalizing A_R changes coefficients on an existing structure but doesn't
introduce a new Hessian direction. The ρ-tachyon at V_*=0 originates from the
competition between (−2,−8) [B_base] and (+1,−6) [V_F], unchanged by A_R
renormalization.

Quick check: critical-point γ* barely shifts (0.105 → 0.106). Λ_7 required
for V=0 changes slightly. Hessian structure identical. Tachyon survives.

## §6. Subleading η_grav moduli dependence

η(Σ) itself is a topological invariant: scaling (0, 0), parallel to Λ_eff.

1-loop Selberg-zeta corrections on hyperbolic Σ with cone points give
δη(γ) ~ c_1·log(γ/γ_0) + c_2·ζ'_Σ(0)·γ⁻² + ...

Leading log-γ: after Weyl, scaling (-1, -2), parallel to Λ_7.
Sub-leading γ⁻²: after Weyl, scaling (-1, -4), parallel to V_base.

**NO NEW SCALING DIRECTION from η_grav at any subleading order.**

## §7. Session 23 comparison

(p_gCS, q_gCS) = (-1, -4) is explicitly in Session 23's `existing` exclusion list
(line 105). Not in the stable region.

All 33 stable directions require q > 0 (growing-at-large-γ). gCS gives q = -4.
Wrong side of the stability wedge.

## §8. Final summary

1. **k_grav at N=7**: 8.596 at tree, 7.953 after η shift.
2. **Scaling**: (-1, -4), parallel to V_base.
3. **In Session 23 stable region?** No.
4. **Coefficient**: δA_R^{gCS} = -0.212 (120× A_R, opposite sign).
5. **Physical mechanism?** No — renormalizes A_R only.

Combined with Sessions 18-24a: we've now found that ALL V_3-dependent or
α-only-with-standard-Weyl contributions give scalings parallel to existing
directions. Need something with INDEPENDENT γ-growth.

## References

- Paper IV §5, §7, §12, §20
- Paper III §1 (SL(2,R) CS)
- Session 18 (5-term setup), 22 (B_base sign), 23 (stable region)
- Kirk-Klassen 1990, Bismut-Cheeger-Dai 1995, Atiyah-Patodi-Singer 1975
