# Session 24a — N=11 Cosmological-Constant Mechanism: Moduli Scaling

**Date**: 2026-04-18
**Status**: Derivation complete. NEGATIVE result: the N=11 instanton does not supply a new scaling direction and does not rescue V_*=0 Minkowski stability.

## §1. Object of investigation

Paper V `sec:cc-instanton` defines an N=11 Born-Oppenheimer tunneling mechanism:

    ln(ℓ v) = S_BO(11) − γ_E/2 + O(1/c_{11}) = 102.435 ± 0.008
    Λ_4 = (N² − 16)/(16 ℓ²) = 105/(16 ℓ²) at N=11
    H_0 = √{Λ_4/(3 Ω_Λ)} = 67.4 km/s/Mpc

Question: does the N=11 instanton contribute a term V_N11(α, γ) to the 4D
effective potential with a NEW scaling direction in Session 23's stable region?

## §2. Role A vs Role B distinction

**Role A (constraint)**: WKB ratio fixes ℓ·v at the critical point. A relation
between two scales, not a term in V_eff(α, γ). This is how Paper V uses it.

**Role B (term in V_eff)**: if realized as semiclassical contribution,
    V_N11^{(B)}(α, γ) = 𝒞_{N11}(α, γ) · exp[−S_BO^E(11; α, γ)],
analogous to Session 19's N=7 treatment.

Paper V never exhibits Role B explicitly. §3 below derives it from first principles.

## §3. Direct derivation of V_N11(α, γ) in Role B

### 3.1 Bare action
    S_BO(11) = 102.724   (Paper V line 829)
    c_{11} = 12 b(11) = 126.56
    ρ*_{11} ≈ 4.45

### 3.2 Weyl rescaling
By the identical derivation as Session 19 §1.3-1.5:
    S_BO^E(11; α, γ) = S_BO(11) / √(V_3) = 102.724 / √(K_{11} α γ²)

where K_{11} = 4π²·(9/11) = 32.28 (area factor for H²/Z_{11}, |χ_orb| = 9/11).

Functional dependence of S_BO^E: **(p_S, q_S) = (−1/2, −1)**.

### 3.3 Prefactor
By universal Weyl prescription: 𝒞_{N11} = 𝒞_0 / (K_{11}² α² γ⁴), (p_C, q_C) = (−2, −4).

### 3.4 Full V_N11
    V_N11(α, γ) = (𝒞_0/(K_{11}² α² γ⁴)) · exp(−102.724/√(K_{11}αγ²))

Scaling vector of ln|V_N11| at (α, γ):
    ∂_{logα} ln V_N11 = −2 + (1/2)·S_BO^E(11)
    ∂_{logγ} ln V_N11 = −4 + 1·S_BO^E(11)

### 3.5 At Session 18 benchmark
(α_*, γ_*) = (0.798, 0.165). V_3^{(11)} = K_{11}·0.798·0.0273 = 0.702.
    S_BO^E(11) = 102.724 / √0.702 = 122.6

Scaling vector: **(p_N11, q_N11) = (−2, −4) + 122.6·(1/2, 1) = (59.3, 118.6)**.

### 3.6 Parallel-direction check
    q/p = 118.6/59.3 = 2.00 exactly ⇒ PARALLEL TO (1, 2) = NEGATIVE of Λ_7 direction.

Cross product with Λ_7 = (−1, −2):
    59.3·(−2) − (−1)·118.6 = −118.6 + 118.6 = 0.

**PARALLEL — excluded from Session 23's stable region by construction.**

## §4. Structural reason (universal theorem)

Any V_eff contribution whose moduli dependence enters ONLY through V_3 = K α γ²
has scaling vector parallel to (−1, −2). This includes:
- Bulk cosmological constant Λ_7
- H-flux ∫H = 2πp (Session 18 §R.27)
- BF-instantons at ANY N (Sessions 19, 24a)
- Bulk gravitational WKB tunneling amplitudes

Changing N (7 → 11) cannot break the parallel-direction obstruction because the
obstruction is a property of KK reduction geometry (single V_3 combining α, γ),
not of polygon content.

## §5. Coefficient estimate

Even if non-parallel, the exponential factor exp(−122.6) = 1.6×10⁻⁵⁴ at benchmark
makes V_N11 negligible. Required 𝒞_0 to compete: ~ 10⁵⁶, more than 50 orders
of magnitude above any natural bulk scale.

## §6. Reinterpretation: Role A is how Paper V actually uses it

Paper V equation `eq:ell-cc` is a relation ℓ·v = exp(S_BO(11) − γ_E/2) that
fixes the DIMENSIONFUL SCALE ℓ but does not add a term to V_eff. The moduli
stability question depends only on the scaling structure of V_eff, which is
unchanged by Role A.

## §7. Final summary

1. **Is V_N11 moduli-dependent?** Yes in Role B: V = (𝒞_0/(K²α²γ⁴))·exp(−S_BO(11)/√V_3).

2. **Scaling (p_N11, q_N11).** At benchmark (59.3, 118.6) ∥ (1, 2), same line as Λ_7.

3. **In Session 23 stable region?** NO. Excluded by parallel-to-(−1,−2) filter.

4. **Required coefficient.** 10⁵⁶ G_7=1 units — unphysical.

5. **Recommendation.** N=11 is NOT the mechanism. Must pursue one of:
   - R² higher-curvature (Session 20: already failed numerically)
   - Fiber-wrapped Wilson line (Session 21: already failed)
   - Hodge dual FR flux (untested)
   - Mixed KK/base modes with separate α, γ dependence

Universal theorem extends Session 19: all BF-instantons at any N are parallel.

## References

- Session 19: N=7 template
- Session 18 §R.27: parallel-direction obstruction for H-flux
- Session 23: scan_generic.py `is_parallel` filter line 108
- Paper V `sec:cc-instanton` lines 586-950
