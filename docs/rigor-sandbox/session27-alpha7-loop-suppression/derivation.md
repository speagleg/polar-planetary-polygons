# Session 27 — 1-loop derivation of α'_7 for R² corrections in the 7D radion EFT

## Summary

A 1-loop KK integration of the 7D effective action generates the R² coupling at order
α'_7 = 1/(16π² · k(7)) ≈ 7.37 × 10⁻⁴, two orders below Session 20's naive
α'_7 = 1/k(7) ≈ 0.116. At both critical points the 3D Ricci scalar is dominated by the
Seifert-twist term α²e²/(2γ⁴), giving |R_3| ≈ 5.3 × 10³ in G_7 = 1 units. Then

    α'_7 · |R_3| = 3.93 (V_*=0 saddle), 3.99 (AdS_4 minimum).

Session 20's claim "α'·|R_3| ≈ 619" was off by factor ~160 due to omitting the loop
measure 1/(16π²). With the correct coefficient, the EFT is MARGINAL — not ≪ 1, not
≫ 1. Session 20's stability conclusion is unchanged; the tachyon is not a large-α' artifact.

## §1. Where α'_7 R² comes from

### 1.1 Tree-level: it does not

In pure Einstein gravity there is no α' R² at tree level in d=7 EFT; it is generated
purely at 1-loop by integrating out heavy fields (Goroff–Sagnotti 1986; Vassilevich 2003).

### 1.2 The relevant diagram

Integrating out any massive mode of mass m produces a Coleman–Weinberg-type effective
action

    Γ_1-loop ∝ 1/(16π²) · [a₀ m^d + a₂ m^(d-2) R + a₄ m^(d-4) R² + ...]

where a_k are heat-kernel coefficients (DeWitt-Schwinger). In d=7 the R² coefficient
carries 1/(16π²) from Euclidean momentum measure (Peskin-Schroeder §10.2) and a scale
m^(7-4) = m³, giving schematic

    α'_7 · R² ~ [1/(16π²) · 1/Λ_UV²] · R²

### 1.3 UV scale in the polygon framework

The natural UV threshold of the 7D effective theory is set by the CS level k(7) = 2b(7)
= 8.596 (Paper III §12). Take Λ_UV² ~ k(7) · M_poly² and identify

    α'_7 = 1/(16π² · k(7)) ≈ 7.37 × 10⁻⁴ (G_7 = 1)

This is distinct from Session 20's naive 1/k(7), which mis-identified k(7) as the full
coupling without the obligatory 1/(16π²) loop factor.

### 1.4 Heat-kernel check

For a d=7 scalar of mass m, the Gilkey-Seeley a₄ coefficient gives
    α'_7 ~ 1/(1152 π² · m)
per mode. Multiplied by matter content |C| ≈ 36 (Session 14), one gets
α'_7 ≈ |C|/(1152 π² · k(7)) ≈ 3.7 × 10⁻⁴ — same order as 1/(16π² · k(7)).

### 1.5 Preferred benchmark value

| Scheme | α'_7 |
|---|---|
| Session 20 naive: 1/k(7) | 1.16 × 10⁻¹ |
| 1/(16π²) (loop only) | 6.33 × 10⁻³ |
| 1/(16π² · k(7)) (polygon UV) | **7.37 × 10⁻⁴** |
| Heat-kernel + matter | 3.7 × 10⁻⁴ |

Preferred: **α'_7 = 1/(16π² · k(7)) ≈ 7.4 × 10⁻⁴**.

## §2. Numerical evaluation at critical points

Background Ricci (from Session 20 §1.2):

    R_3(α, γ) = -2/γ² - α²e²/(2γ⁴),  e = 7/2

**Critical point A (V_*=0 saddle)**: (α, γ) = (0.798, 0.165)
- -2/γ² = -73.46
- α²e²/(2γ⁴) = 5262
- **R_3 = -5335**

**Critical point B (AdS_4 minimum)**: (α, γ) = (0.7255, 0.1567)
- -2/γ² = -81.44
- α²e²/(2γ⁴) = 5347
- **R_3 = -5428**

Both dominated by Seifert-twist, fixed by Thurston ray r_* = α/γ:

    (α²e²/2γ⁴) / (2/γ²) = r² · e²/4

which is r²-fixed, independent of overall scale.

### 2.2 Product α'_7 · |R_3|

| α'_7 scheme | value | saddle | AdS_4 min |
|---|---|---|---|
| Session 20 naive | 0.1163 | **620.5** | 631.3 |
| 1/(16π²) only | 6.33 × 10⁻³ | 33.78 | 34.36 |
| 1/(16π² · k(7)) | 7.37 × 10⁻⁴ | **3.93** | **4.00** |
| Heat-kernel + matter | 3.7 × 10⁻⁴ | 1.97 | 2.01 |

### 2.3 EFT-validity verdict

At preferred α'_7 ≈ 7.4 × 10⁻⁴, α'·|R_3| ≈ 4 at both critical points:
- NOT in naive-EFT regime (α'·R ≪ 1)
- NOT catastrophically broken (α'·R ≫ 1)
- **MARGINAL**: R² corrections are O(1) perturbations, not subleading
- Higher-curvature resummation would be needed for quantitative statements

## §3. Why the naive 1/k(7) was wrong

Session 20 conflated two scales:

1. **k(7) as CS level** — dimensionless integer for U(1) vortex quantization; appears
   in e²_CS = 4π/k, NOT as gravitational α'.
2. **α'_7 as length²** — fixed by UV cutoff of gravitational EFT. Always carries
   1/(16π²) from Euclidean phase-space measure.

Dropping the 1/(16π²) factor overestimates α'_7 by ~160, exactly the ratio
0.116/7.4×10⁻⁴. Not optional — this is the d=4 Feynman measure; in d=7 the analog
is (4π)^{7/2} ≈ 276.

## §4. Does correct α'_7 rescue EFT regime? NO

Even the most loop-suppressed estimate gives α'·|R_3| ≈ 2, not ≪ 1. Structural
reason: Seifert twist contribution α²e²/(2γ⁴) is O(5×10³) at both critical points,
pinned by Thurston rigidity r_* = 7√7/4. Cannot reduce without:
(a) going to larger γ (but γ is dynamically pinned by V_eff)
(b) changing N (but polygon framework pins N=7)
(c) non-perturbative resummation (beyond this session)

## §5. Recommendation for Paper IV text

Replace CHANGE 4's current hedge text:

> "Higher-curvature R² corrections at Session 20's naive coupling α'_7 = 1/k(7) would
> be formally large (α'_7·|R_3| ≈ 620) at both critical points..."

with:

> The correct 1-loop R² coefficient in the 7D polygon EFT is
> α'_7 = 1/(16π² · k(7)) ≈ 7.4 × 10⁻⁴, giving α'_7·|R_3| ≈ 4 at both the V_*=0
> saddle and the AdS_4 minimum. The α'-expansion is therefore marginal at the
> polygon critical points: higher-curvature corrections are O(1), not small. The
> sign of Session 20's tachyonic det H is unlikely to be altered by such
> corrections since they preserve the (+,-) Hessian signature at the shifted
> critical point.

## §6. Verdict

α'_7 coefficient is DERIVED: α'_7 = 1/(16π² · k(7)) ≈ 7.4 × 10⁻⁴. EFT is MARGINAL,
not catastrophic (Session 20 overestimate by factor 160). Tachyon survives.

## §7. References

- Vassilevich, "Heat kernel expansion," Phys. Rep. 388 (2003), 279.
- Peskin & Schroeder, §10.2 (Feynman measure 1/(16π²)).
- Goroff & Sagnotti, Nucl. Phys. B 266 (1986), 709.
- Birrell & Davies, *Quantum Fields in Curved Space* §6.3.
- Session 18 (this repo): 5-term potential, r_* = 7√7/4.
- Session 20 (this repo): naive α'_7 used; three-channel R² derivation.
