# Session 39 — 2-modulus CW+FR at N=11 (B3 path)

## Bottom line

**Scenario β confirmed**: 2-modulus reformulation at N=11 gives a stable AdS_4
minimum with radion masses [56.5, 97.7] M_poly on the Thurston ray. V_*=0
Minkowski branch exists for all |C_base| ≥ 0.005 but is TACHYONIC SADDLE (not
stable), same qualitative structure as N=7. The σ-direction mass in the
2-modulus treatment equals Paper VI's single-modulus ω (unit-conversion
modulo), and the ρ-direction adds a new heavy mode. Neither changes the 1.4σ
Planck tension.

## Geometric setup at N=11

- |χ_orb|(11) = 8/11 (three Z_11 cone points)
- K = 4π²|χ_orb| = 32π²/11 ≈ 28.72
- e = N/2 = 11/2
- **r_T(11) = 11√22/8 ≈ 6.449** (not 11√11/4; correct formula is e/√|χ_orb|)
- b(11) = 10.547, c_11 = 126.56

## Coefficients at N=11 (G_7 = 1 units)

| | N=7 | N=11 |
|---|---|---|
| A_R = 1/(32π³·|χ_orb|) | 0.001764 | 0.001386 |
| A_F = e²/(128π³·|χ_orb|³) | 0.01654 | 0.01982 |
| A_L = A_R | 0.001764 | 0.001386 |
| A_C_fib = \|C_fib\|/(16π⁴·|χ_orb|²) | 0.07139 | 0.04408 |
| K | 22.56 | 28.72 |

(|C_fib| = 36.33 assumed N-independent; Scherk-Schwarz fermion antiperiodicity
at e = odd-half holds for both N=7 and N=11.)

## Branch (a): Thurston ray, no base Casimir — STABLE AdS_4 minimum

Newton solve of {∂_α V = ∂_γ V = 0} on α = r_T γ:

    α_* = 0.55666,  γ_* = 0.08631,  r_* = 6.44932 = r_T ✓
    Λ_7 = -3.995×10⁵
    V_* = -8.01×10⁴ (AdS_4)
    ∂_α V = 1.5×10⁻¹⁰, ∂_γ V = 1.4×10⁻⁹ (stationary ✓)

Hessian in (log α, log γ) basis:
    H = [[8.55×10⁵, 2.14×10⁵], [2.14×10⁵, 8.57×10⁵]]
    tr H = 1.71×10⁶, det H = 6.84×10¹¹

Physical masses (eigenvalues of G⁻¹ H, G_ij = [[3/4, 1/2], [1/2, 2]]):
    m²_- = 4.27×10⁵ (dim-less, M_P² units)
    m²_+ = 1.28×10⁶

Dimensional restoration (L_0(11) = r_T/M_poly ≈ 11.59/M_poly):
    L_0⁻² = 0.00745 M_poly²
    **m_- = 56.40 M_poly (~17 PeV at M_poly = 300 TeV)**
    **m_+ = 97.68 M_poly (~29 PeV)**

Both eigenvalues positive → STABLE MINIMUM.

## Branch (c): V_*=0 Minkowski scan — TACHYONIC for all physical |C_base|

Newton solve of {V = 0, ∂_α V = 0, ∂_γ V = 0} over range:

| |C_base| | α_* | γ_* | Λ_7 | m²_- | m²_+ | Status |
|---|---|---|---|---|---|---|
| 0.005 | 0.518 | 0.0507 | -4.15×10⁵ | -4.03×10⁶ | +1.99×10⁷ | SADDLE |
| 0.010 | 0.555 | 0.0646 | -1.81×10⁵ | -1.01×10⁶ | +4.98×10⁶ | SADDLE |
| 0.020 | 0.595 | 0.0823 | -7.88×10⁴ | -2.52×10⁵ | +1.25×10⁶ | SADDLE |
| 0.050 | 0.652 | 0.1135 | -2.63×10⁴ | -4.04×10⁴ | +2.00×10⁵ | SADDLE |
| 0.100 | 0.699 | 0.1446 | -1.14×10⁴ | -1.01×10⁴ | +4.99×10⁴ | SADDLE |
| 0.150 | 0.728 | 0.1666 | -7.04×10³ | -4.50×10³ | +2.22×10⁴ | SADDLE |

**Every critical point has one negative eigenvalue.** V_*=0 Minkowski is a
tachyonic saddle at N=11 for all tested |C_base|, same qualitative result as N=7.

Difference from N=7: at N=7, Session 31 showed V_*=0 doesn't even EXIST for
|C_base| < 0.025. At N=11, V_*=0 solutions exist down to |C_base| = 0.005, but
they're all tachyonic saddles, not stable minima.

## Comparison with Paper VI / Session 35

Paper VI's single-modulus ω = 6.77 (Session 34-35) corresponds to the σ-direction
eigenvalue of the 2-modulus system after unit matching. The 2-modulus treatment
does NOT give a different σ-mass; it adds a ρ-mode as a new heavy modulus.

**If F_DE = b(N) + Σ_i (1/2)m_i with both modes** (σ + ρ):
    F_DE = b(11) + (m_- + m_+)/2 = ... much larger than single-modulus value
    → Ω_Λ would INCREASE, **worsening** the 1.4σ Planck tension

**If F_DE counts only the σ-mode** (Paper VI convention):
    F_DE = b(11) + σ_mass/2 (matches single-modulus)
    → Ω_Λ = 0.695, same 1.4σ tension

**Either way, 2-modulus doesn't help close the gap.**

## Verdict (consolidated B1+B2+B3)

All three paths confirm:

**The 1.4σ Planck tension on Ω_Λ is INTRINSIC to Paper VI's framework at
current 1-loop rigor.** The gap CANNOT be closed by:
- B1 direct single-modulus analysis (Sessions 34-35)
- B2 missing-physics search (9 candidates ruled out, Session 38)
- B3 2-modulus reformulation (Session 39, this session)

Honest framework parameters:
- Ω_Λ = 0.695 ± 0.005 (derived from M_Planck + pure math)
- Planck 2018: Ω_Λ = 0.685 ± 0.007
- Tension: +1.4σ ± 0.7σ (within 2σ, not sub-σ)

## What Paper VI needs to say

1. **Line 1049**: remove "stabilized at unit radius" (σ_min = 1.35, not 1)
2. **Line 1050**: remove "M_rad = N/2" assertion; replace with derived ω ≈ 6.77
   (G_11 = 3/4 Ferrara-Kounnas kinetic normalization)
3. **Paper IV line 241-243**: correct math (N/(2e) = 1 when e = N/2, not N/2)
4. **prop:cosmology**: Planck tension 0.3σ → 1.4σ
5. **Paper VI CC**: acknowledge AdS_4 natural vacuum; Minkowski emerges via
   external mechanism not closed at 1-loop

## Verification files

- `solve_N11.py` — main Newton solver for critical points (Branches a, b, c)
- `check_Minkowski_stability.py` — confirms V_*=0 branch is tachyonic at N=11

Both scripts run with numpy only (no scipy required).

## Context

- Session 33-38 (audit, single-modulus, missing physics)
- Session 18 (N=7 2-modulus machinery)
- Session 31 (N=7 |C_base| = 0.0065 via Selberg)
- Paper VI §cc-instanton, prop:lambda, eq:V-radion
