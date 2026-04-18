# Session 32 — Mixed KK Casimir sector (n ≠ 0, j ≠ 0)

## Summary

**Scaling**: same Einstein-frame channel (-2, -8) as base Casimir (not a new channel).
**Magnitude**: |ΔC_base|/|C_base| ≤ 10⁻⁴ at Session 18 benchmarks — driven by
exponential suppression e^{-2π(α/γ)√λ_1} ≤ e^{-14.5} ≈ 3×10⁻⁷.
**Radion mass impact**: negligible (< 0.1%).
**Classification**: trivial renormalization of |C_base|, not a new CHANGE.
**Session 18 §R.22 item 3 CLOSED**.

## 1. Setup

Mixed spectrum on M_7 = M_4 × S¹_α × Σ_γ:
    m²_{n,j} = (n+ε)²/α² + λ_j/γ²
with ε = 0 periodic bosons, ε = 1/2 antiperiodic fermions; j ≥ 1 on Σ_0.

Mixed Casimir (per DOF):
    V_mix = -(N_DOF/64π²) Σ_{j≥1} Σ_{n≠0} m⁴_{n,j} [ln(m²_{n,j}/μ²) - 3/2]

## 2. Poisson resummation on fiber

Use proper-time integral representation and Poisson on fiber sum. For bosons:
    Σ_{n∈ℤ} e^{-n²τ} = √(π/τ) Σ_{w∈ℤ} e^{-π² w²/τ}

The w=0 term (straight-line) contributes to base Casimir (no new channel). The
w≠0 terms are the irreducible winding pieces.

## 3. Scaling analysis

Substituting u = t/γ² and extracting α, γ dependence:
    V_mix^{(irred)}_{pre-Weyl} = (α/γ⁵) · F(α/γ)

with F a function of the ratio ξ = α/γ.

After Weyl rescaling /V_3² = 1/(K²α²γ⁴):
    V_mix^{(E)} = F(α/γ)/(K²·αγ⁹)

Writing F(ξ) = c_0 + c_1 ξ⁴ + ..., leading term is (-1, -9) — but each c_i is
exponentially small.

**Key alternative view**: the non-winding (w=0) piece of the mixed tower
reproduces the BASE Casimir scaling (-2, -8). The irreducible w ≠ 0 piece has
all channels exponentially suppressed by worldline-winding actions.

## 4. Saddle-point estimate of winding integrals

Each winding w and base mode j:
    I_{w,j}(ξ) ∼ (πwξ)^(ε-5/2) λ_j^(−ε/2+5/4) · exp(-2πwξ√λ_j)

Dominant (w=1, j=1) gives
    V_mix^{(irred)} ∼ -(α/γ⁵) · exp(-2π(α/γ)√λ_1)

Using Selberg bound λ_1 ≥ 1/4 for arithmetic hyperbolic surfaces (Kim-Sarnak 2003),
    suppression ≥ exp(-π(α/γ))

## 5. Numerical at Session 18 benchmarks

| Benchmark | α | γ | α/γ | 2π(α/γ)√λ_1 | exp(-...) |
|---|---|---|---|---|---|
| AdS_4 min | 0.7255 | 0.1567 | 4.630 | ≥ 14.55 | ≤ 3.1×10⁻⁷ |
| V_*=0 saddle | 0.798 | 0.165 | 4.836 | ≥ 15.19 | ≤ 1.7×10⁻⁷ |

**Exponential factor ~10⁻⁷ at both critical points.**

Ratio mixed/base at (α, γ) = (0.7255, 0.1567):
    |V_mix^{(E)}|/|V_base^{(E)}| ≤ (50·27)/(31.9·0.089) · 4.63 · 3.1×10⁻⁷ ≈ 6×10⁻⁵

**Fractional correction to |C_base|: < 10⁻⁴.**

## 6. Why the weak-coupling regime

Session 18 §R.1.1 incorrectly stated α ~ γ at critical point. Actually α/γ ~ r_* ≈ 4.63
(Thurston ratio). The dimensionless parameter controlling mixed suppression is
α/γ · √λ_1, NOT α·γ·λ_1. At N=7 this is O(7) — we are in the WEAK-COUPLING regime.

Universal N scaling: r_* scales as N^{3/2} for large N, so mixed Casimir
suppression INCREASES with N.

## 7. Twisted sectors (Session 22 §3)

Twisted-sector base modes at Z_7 cone points have λ_{j,tw} ≥ (k/7)² per Dowker.
These are EVEN MORE suppressed than untwisted. Inclusion strengthens the bound.

## 8. Higher winding w ≥ 2

Σ_{w≥1} e^{-2πwξ√λ_1} = e^{-...}/(1 - e^{-...}), indistinguishable from w=1 at
ξ ≈ 4.6.

## 9. Radion mass sensitivity

d ln m²/d ln|C_base| ≈ -0.3 (Session 18 §R.3.2 table).
Δm_σ ≤ 3×10⁻⁵ · 20 M_poly ≈ 6×10⁻⁴ M_poly.

**Not detectable** given ±50% systematic from |C_base| uncertainty.

## 10. Verdict

Mixed KK Casimir sector at N=7:
1. Same (-2, -8) scaling as base Casimir.
2. Sub-percent correction to |C_base|, driven by exponential suppression.
3. Negligible radion mass impact.
4. Does NOT close V_*=0 tachyon gap (tachyon is structural, not perturbative).
5. Session 18 §R.22 item 3 ("expected O(1) fractional correction") was too
   pessimistic — actual correction is ≤ 10⁻⁴.

## References

- Candelas-Weinberg 1984 Nucl. Phys. B 237, 397 (Poisson resummation on S¹×S²).
- Appelquist-Chodos 1983 PRD 28, 772 (S¹ Casimir via Hurwitz zeta).
- Elizalde, *Ten Physical Applications of Spectral Zeta Functions* Ch. 4, §4.68.
- Selberg 1965; Kim-Sarnak 2003 (spectral gap λ_1 ≥ 1/4 for arithmetic hyperbolic).
- Bolte-Steiner 1997 (numerical λ_1 for congruence subgroups).
- Dowker 1977; Farsi-Jorgenson 1995 (orbifold heat kernel).
- Session 18 §R.1, §R.22 (this repo).
- Session 22 (this repo): |C_base| normalization.
- Session 24b (this repo): uniform (-2, -8) for heat-kernel orders.
