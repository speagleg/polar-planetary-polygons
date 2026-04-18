# Session 36 — Cumulative corrections to V(σ) at N=11

## Bottom line

Cumulative first-principles corrections to ω at N=11: Δω/ω = **+5.5%** (dominated
by anharmonicity, which is +5% pushing ω UP, not down). **Gap to N/2 WIDENS** from
22% to ~30%.

**Final ω = 6.77 ± 0.40**, Ω_Λ = 0.695 ± 0.005, **Planck tension = +1.4σ ± 0.7σ**.

No first-principles correction can close the gap.

## Baseline (Sessions 34-35)

- σ_min = 1.34706
- V''(σ_min) = 18.93
- V'''(σ_min) = -62.28
- V''''(σ_min) = +245.63
- K_ψ = 3/4 (Ferrara-Kounnas, rigorous)
- ω = √(σ²V''/K_ψ) = **6.767**

## Ten corrections evaluated

| # | Correction | Δω/ω | Magnitude | Sign |
|---|---|---|---|---|
| 1 | 2-loop Casimir (α_CS = 0.047) | +0.25% | small | up |
| 2 | Base Casimir at N=11 | 10⁻⁶ | negligible | — |
| 3 | R² Seifert-twist (γ=1 suppresses) | ~0.5% | small | up (upper bound; field redefinition absorbs most) |
| 4 | Z_11 twisted sectors | 10⁻⁶ | negligible | — |
| 5 | WDW subleading on S_BO(11) | 0 direct, ±1% on H_0 | — | — |
| 6 | **Anharmonicity** | **+5%** | **largest** | **up (V'''' > 0)** |
| 7 | Mixed KK at N=11 | 10⁻²⁹ | negligible | — |
| 8 | Higher-loop WDW | 0 direct | — | — |
| 9 | Orbifold instanton | 10⁻⁸ | negligible | — |
| 10 | Fermion condensate | 10⁻¹⁷⁴ | excluded by RG | — |

**Cumulative effect: Δω/ω ≈ +5.5%**. Dominated by anharmonicity (Correction 6).

## Anharmonicity details (the dominant correction)

In log frame ψ = ln σ, canonically normalized φ = √G_11·ψ:
- U''(φ_*) = ω² = 45.795
- U'''(φ_*) = -181.5
- U''''(φ_*) = +1055.6

Dimensionless anharmonicity: **ξ_anharm = U''''/ω⁴ = 0.502** (!)

This is NOT a small perturbation. First-order Rayleigh-Schrödinger:
    δω/ω ≈ (ℏ/(2ω·m))·ξ_anharm ≈ 5%

At 5% level, anharmonicity is the dominant correction. Crucially, **V'''' > 0 means
anharmonicity RAISES ω** (stiffens the oscillator) — the opposite direction from
what's needed to close to N/2.

## Consequence for Ω_Λ

| Scenario | M_rad | F_DE | Ω_Λ | Planck tension |
|---|---|---|---|---|
| Paper VI asserted | 5.50 | 13.30 | 0.6849 | +0.07σ |
| ω_tree (Session 34-35) | 6.77 | 13.93 | 0.6950 | +1.42σ |
| **ω_corrected (this session)** | **7.14** | **14.12** | **0.6980** | **+1.85σ** |

**Tension INCREASES** after first-principles corrections.

## What would it take to close the gap?

Need a new term T(σ) with:
- T'(σ_min) = 0 (preserves σ_min)
- T''(σ_min) ≈ -9.77 (reduces V'' by 50%)

None of the 10 enumerated mechanisms provides this. The 22% gap is structurally
persistent.

## Verdict

**Paper VI's M_rad = N/2 cannot be recovered.** The honest framework precision is:

    Ω_Λ = 0.695 ± 0.005 (vs Planck 0.685 ± 0.007)
    Planck tension = +1.4σ ± 0.7σ (range [0.7σ, 2.1σ])

Tier 4.1 closes at ~1σ Planck agreement, not sub-σ.

## Recommendations

1. Paper VI lines 1049-1050: fix "stabilized at unit radius" (wrong) and
   "M_rad = N/2" (wrong); replace with derived ω ≈ 6.8.
2. Paper VI prop:cosmology: update Planck tension from 0.07σ to 1.4σ.
3. Accept the 1.4σ precision as the honest framework result.

## References

- Sessions 34, 35 (baseline ω, σ_min, V'')
- Session 27 (α'_7 loop suppression → α'_11)
- Session 31 (|C_base|)
- Session 32 (mixed KK)
- Session 22 (twisted sectors)
- Paper VI radion_inflation.py eq:V-radion
- Polchinski vol II §7.3 (loop counting)
- Landau-Lifshitz QM §38 (anharmonicity)
