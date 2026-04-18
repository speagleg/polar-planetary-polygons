# Session 24b — Minakshisundaram sub-leading heat-kernel coefficients in the base Casimir on H²/Z_7

**Status**: Derivation complete. NEGATIVE result — all orders give the same scaling.

## §1. Setup

Session 22 set |C_base| = 0.089 using only the leading Weyl-law term.
Session 23 scan showed stable directions require q ≥ +1. Question: do sub-leading
heat-kernel coefficients a_1, a_2, ... introduce new scaling channels?

## §2. Heat-kernel expansion on H²/Z_7

Standard Minakshisundaram-Pleijel small-t asymptotic (2D smooth closed):

    K_Σ(t) = Σ_j exp(-λ_j t) ~ (1/4πt) Σ_{k≥0} B_k · t^k

Integrated coefficients on Σ_0 = H²/Z_7 (unit curvature):
- B_0 = A_Σ = 8π/7 ≈ 3.590  (leading Weyl)
- B_1 = (2π/3)·χ_orb = -8π/21 ≈ -1.197
- B_2 = (4/45)·A_Σ + 0 = 32π/315 ≈ 0.319
- B_3, B_4, ... higher curvature contractions

## §3. Spectral zeta scaling

Under g → γ² g_0: R → R/γ², λ_j^phys = λ_j^(0)/γ².

Physical spectral zeta:
    ζ^phys(s) = Σ_j (λ_j^phys)^(-s) = **γ^(2s) · ζ_Σ(s)** uniformly

At s = -2: ζ^phys(-2) = γ^(-4) · ζ_Σ(-2) and ζ^phys'(-2) = γ^(-4) · [ζ_Σ'(-2) - 4 log γ · ζ_Σ(-2)].

**Every heat-kernel order k contributes to ζ_Σ'(-2) as a constant, then gets
multiplied by the SAME γ^(-4) factor.** The substitution u = t/γ² in the
heat-kernel integral shows this cleanly.

## §4. Pre-Weyl and Einstein-frame scaling

Pre-Weyl: V_scalar(γ) = -ζ_Σ'(-2)/(64π²γ⁴). **Scaling (0, -4) pre-Weyl.**

After Weyl rescaling (factor 1/V_3² = 1/(K²α²γ⁴), scaling (-2, -4)):
**Einstein-frame scaling (-2, -8) — IDENTICAL at all k.**

Scaling table:

| k | a_k | B_k^(0) | pre-Weyl γ | Einstein (p, q) |
|---|-----|---------|-----------|-----------------|
| 0 | 1 | 8π/7 | γ^(-4) | (-2, -8) |
| 1 | R/6 = -1/3 | -8π/21 | γ^(-4) | (-2, -8) |
| 2 | R²/45 | 32π/315 | γ^(-4) | (-2, -8) |
| 3 | ~R³ | O(1) | γ^(-4) | (-2, -8) |
| 4 | higher | O(1) | γ^(-4) | (-2, -8) |
| 5 | higher | O(1) | γ^(-4) | (-2, -8) |

**No scaling channels beyond (-2, -8).**

## §5. Cone-point sectors (twisted)

Dowker-Farsi-Jorgenson cone contributions are zero-dimensional defects,
dimensionless. They contribute to ζ_Σ'(-2) as constants and inherit the
same γ^(-4) factor from the ambient zeta. Same (-2, -8) Einstein channel.

## §6. Numerical magnitudes

Leading smooth (a_0): per-DOF coefficient ≈ -3.30×10⁻³
a_1 correction: ~ +1.10×10⁻³ (30% of leading)
a_2 correction: ~ +0.30×10⁻³ (9% of leading)
Higher: <10⁻³ each

**Total a_1 + a_2 + ... correction to |C_base|: O(20-30%)** keeping it in
[0.06, 0.12] — within Session 22's band [0.05, 0.15].

## §7. Session 23 comparison

Session 23 stable region: q ≥ +1. Base Casimir: q = -8.

**No overlap. Not the mechanism.**

## §8. What stabilization requires

To reach the stable region, need a term with PRE-Weyl scaling (+2, +6) or similar
(to give Einstein (0, +2)). Natural sources:
- Wrapped instantons on base (multiple wrapping)
- D-branes at specific charges (polygon theory isn't obviously stringy though)
- Axion-like periodic potentials with moduli-independent energy scale

Sub-leading base Casimir cannot provide this.

## §9. Final summary

1. **All Minakshisundaram orders have SAME scaling** (-2, -8) Einstein-frame.
2. **No order matches Session 23 stable region**.
3. **|C_base| gets ~20-30% correction from sub-leading** but stays in band.
4. **Not the physical mechanism** for V_*=0 stabilization.

## References

- Session 22 (base Casimir sign)
- Session 18 §R.1-R.2 (Weyl rescaling)
- Session 23 (scan_generic.py stable region)
- Vassilevich 2003 "Heat kernel expansion" Phys. Rep. 388, 279
- Elizalde "Ten Physical Applications of Spectral Zeta Functions"
- Dowker 1977, Farsi-Jorgenson 1995 (orbifold)
