# Session 35 — Kinetic normalization for Paper VI's N=11 radion

## Bottom line

**γ is frozen by convention (Case I) in Paper VI: the H² base radius is set to unity
by Paper IV's metric ansatz.** No dynamical γ stabilization.

**Correct K_ψ = 3/4** in log-σ frame (same as Session 18's G_11 for 2-modulus case
restricted to α variation).

**ω = σ_*·√(V''/G_11) = 6.767 at N=11** (confirms Session 34 Scenario D).

**Ω_Λ = 0.6950, Planck tension = +1.42σ.** Within 2σ but NOT sub-σ. Paper VI's
claimed 0.3σ was an artifact of the unverified assertion M_rad = N/2.

## 1. How γ is fixed in Paper VI

Paper IV eq:metric-4d (line 342):
    ds² = -dt² + ds²_{H²} + (dφ + A)²

H² base has NO γ prefactor — base radius set to unity by coordinate convention.
Paper VI inherits this. γ is NOT a dynamical modulus in Paper VI.

**Case I confirmed**: literal freezing via unit-radius convention, not:
- Case II (γ integrated out at mass scale)
- Case III (γ fixed by flux quantization)

## 2. K_σ from first-principles Weyl rescaling

Ferrara-Kounnas 2-modulus kinetic matrix (Session 18 §2.2, DPN eq 3.10):
    G_ij = [[3/4, 1/2], [1/2, 2]]

with (d_ext, d_int) = (4, (1, 2)). Derivation:
    G_ii = (1/2)[d_i + d_i²/(d_ext − 2)]
    G_11 = (1/2)(1 + 1/2) = 3/4
    G_22 = (1/2)(2 + 4/2) = 2
    G_12 = (1/2)(0 + 2/2) = 1/2

Restriction to γ = 1 (Case I): kinetic term becomes
    L_kin = -(M_P²/2) · G_11 · (∂ log σ)² = -(3M_P²/8)(∂σ/σ)²

**K_ψ = 3/4 in log-σ frame** — rigorous first-principles result.

## 3. Frame equivalence (log vs linear σ)

Log frame: V_ψψ(ψ_*) = σ_*²V''(σ_*) = 34.346 at N=11.
ω² = V_ψψ/K_ψ = 34.346/0.75 = 45.795 → ω = 6.767.

Linear frame: K_σ(σ) = G_11/σ² = 3/(4σ²) (σ-dependent!).
ω² = V''(σ_*)/K_σ(σ_*) = V''(σ_*) · σ_*²/G_11 = same 45.795.

**Both frames give ω = 6.767 identically** (as they must, for physical frequency).

Session 34's "linear K=1" row was WRONG because K_σ = 1 in linear frame is
equivalent to K_ψ = σ_*² = 1.81 in log frame — unphysical.

## 4. Why K=1 in log-frame (Session 34 Scenario B) is wrong

Scenario B used K_ψ = 1 giving ω = 5.86. But K_ψ = 1 doesn't arise from any
physical reduction of the 7D action. It was an ad hoc choice that happened to
be closer to N/2 = 5.5.

The RIGOROUS K is G_11 = 3/4 from Ferrara-Kounnas + Paper IV's unit-radius
convention.

## 5. Cross-check at N=7

ω = 3.98 at N=7 (13.7% above N/2 = 3.5).
ω = 6.77 at N=11 (23% above N/2 = 5.5).

Ratio grows monotonically with N in the K_ψ = 3/4 frame. Session 34 Scenario B
(K=1) had SIGN FLIP between N=7 and N=11, indicating it was frame-artifact, not
physics. Scenario D (K_ψ = 3/4) has no sign flip — physically self-consistent.

## 6. Impact on Ω_Λ

| Derivation | M_rad | F_DE | Ω_Λ | Planck tension |
|---|---|---|---|---|
| Paper VI assertion | 5.500 | 13.297 | 0.6849 | +0.07σ |
| **Session 34-35 derivation** | **6.767** | **13.931** | **0.6950** | **+1.42σ** |

Planck 2018: Ω_Λ = 0.685 ± 0.007.

**1.42σ is within 2σ but not within 1σ.** Framework prediction survives but precision
degrades from Paper VI's claimed 0.3σ.

## 7. Sanity check — is σ_min = 1?

Paper VI line 1049 says "stabilized at unit radius." For σ_min = 1 to satisfy
V'(σ) = 0 at N=11 we'd need N²/4 = c_N/12 + Λ, i.e. 30.25 = 10.547 + 6.5625 = 17.1.
Not equal. **σ_min = 1 is NOT a minimum** of V(σ).

Paper VI line 1598 correctly says σ_min ≈ 1.35. Line 1049 is factually wrong.

## 8. What Λ would give ω = N/2?

From Session 34: Λ ≈ 5.36 would give ω = 5.5 exactly. Paper VI has Λ = 6.5625
(from (N²-16)/16 = 105/16). These don't match — gap is 22%.

Closing this gap would require either:
- A correction to Paper VI's Λ_3 derivation (but the derivation is geometrically
  clean: Λ_3 = -K_base + (1/4)|F|² = 1 + N²/16 − 1 − ... which the agent verified).
- A new term in V(σ) that shifts V''(σ_*) without shifting σ_*. Hard to engineer
  naturally.
- A different kinetic normalization. But G_11 = 3/4 is rigorous.

## 9. Tier 4.1 status

**CLOSED at 1.42σ precision, not sub-σ.**

- Ω_Λ = 0.6950 (predicted) vs 0.685 ± 0.007 (Planck)
- Tension: +1.42σ
- Framework prediction is DERIVED from M_Planck + pure math — no curve-fitting
- Paper VI's 0.3σ claim was artifact of unverified M_rad = N/2 assertion
- The derived M_rad = ω = 6.77 is the CORRECT value in Paper VI's own conventions

## 10. Recommended Paper VI edits

1. **Line 1049**: remove "stabilized at unit radius" or correct to "σ_min ≈ 1.35".
2. **Line 1050**: replace "M_rad = N/2" with "M_rad = √(σ_*²·V''(σ_*)/G_11) = 6.77 at N=11, derived in Session 35 via Ferrara-Kounnas kinetic matrix G_11 = 3/4".
3. **Planck tension column** in prop:cosmology: 0.3σ → 1.42σ for Ω_Λ.

## References

- Paper IV eq:metric-4d (line 342)
- Paper VI eq:V-radion (line 1592), line 1048-1052 (assertion being corrected)
- Session 18 §2.2 (Ferrara-Kounnas matrix G_ij = [[3/4, 1/2], [1/2, 2]])
- Session 34 (σ_*, V'' computation)
- Session 33 (CC audit identifying M_rad = N/2 as load-bearing assertion)
- Ferrara-Kounnas, Nucl. Phys. B328 (1989) 406 — kinetic matrix
- Duff, Pope, Nilsson, Phys. Rep. 130 (1986) — KK reduction
