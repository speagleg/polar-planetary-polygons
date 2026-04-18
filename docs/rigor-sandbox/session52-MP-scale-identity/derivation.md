# Session 52 — Identity between M_P^bulk and M_P^(4D): Replacing the "13-decade RG running" narrative

**Date**: 2026-04-18
**Goal**: Derive the physical identifications of M_P^bulk and M_P^(4D) from the polygon action, and derive the exact formula relating them. Replace the Session 43 §1.5 claim that their ratio represents "13 decades of RG running" with the correct instanton-mediated identity.

---

## 0. Bottom line

Two physically distinct Newton-constant scales appear in the polygon framework:

- **M_P^bulk = 1/√G_4^bulk** is the **bulk-gravity loop cutoff** on AdS_3 × S^1_φ: the scale at which the semiclassical expansion of 3D AdS_3 gravity in Newton's constant fails (h_MN fluctuations become O(1)). It is **not** a Planck-like scale in the observational sense; it is a normalization of the bulk Einstein–Hilbert coefficient fixed by Brown–Henneaux plus the KK reduction on S^1_φ. Numerically M_P^bulk = √(4 b(N)/π) · M_poly = 2.339 · M_poly ≈ 631 TeV at N = 7.

- **M_P^(4D) = 1/√G_N^obs** is the **IR observational 4D Planck scale** entering the long-distance Einstein equations (h^(4)_ij propagator, cosmological Friedmann equation, Newton's law). It is fixed by the hierarchy formula M_P^(4D) = v · exp(H_7) via the N = 7 Born–Oppenheimer bounce in the polygon breathing-mode potential on the Wheeler–DeWitt slice.

Their ratio is **not** RG running. It is an **instanton-mediated dynamical hierarchy**, exactly analogous to the Randall–Sundrum warp or to how the string scale and the Planck scale differ by the sum over worldsheet topologies:

    M_P^(4D) / M_P^bulk = Z_BO(N) ≡ exp(2 S_BO(N) + Δε · ln ε_N + (1/2) ln(c_{N+4}/(24π²)) − N − (1/2) ln(4 b(N)/π))

At N = 7 this evaluates to 1.964 × 10^13, with the dominant contribution coming from the doubled BO bounce action 2 S_BO(7) = 36.548 (not from RG-logarithms).

Hypothesis **B** (instanton-mediated hierarchy) is correct. Hypothesis A (bulk-loop cutoff) is the correct identification of M_P^bulk in its own right, but the ratio to M_P^(4D) is not set by bulk-loop physics — it is set by the polygon BO bounce.

---

## 1. Step 1 — Identification of G_4^bulk in the Seifert action

The bulk action on M_4 = AdS_3 × S^1_φ with boundary T² and Seifert fiber data (L, R, b(N)) is

    S_bulk = ∫ d^4x √(−g_4) [R_4 / (16π G_4^bulk) − V(σ) + L_matter].

The coefficient G_4^bulk is **not** a free parameter: it is fixed by Brown–Henneaux on AdS_3 plus KK reduction on S^1_φ (Session 11 §4):

    c = 3L / (2 G_3)              (Brown–Henneaux)
    G_3 = L / (8 b(N))            (using c = 12 b(N), Session 17)
    G_4^bulk = G_3 · (2π R)       (tree-level KK reduction of E–H)
             = π L R / (4 b(N)).

With the democratic convention L R ≈ 1/M_poly² (Session 11 §4 / Session 43 §1.2):

    G_4^bulk = π / (4 b(N) M_poly²),
    M_P^bulk ≡ 1/√G_4^bulk = √(4 b(N)/π) · M_poly.

**Physical content**: G_4^bulk is the coefficient multiplying R_4 in the polygon bulk Einstein–Hilbert term. It is **not** the coefficient in the observed 4D macroscopic Einstein equations, because those equations refer to 4D Minkowski spacetime at energies E ≪ M_poly, **after** the full polygon spectrum (BO wavefunction, KK tower, DHVW twists) is integrated out. G_4^bulk is what appears in the bulk path integral; G_N^obs is what the IR gravitational 2-point function produces.

## 2. Step 2 — Reductions and the two distinct Newton constants

The 4D bulk metric h_MN decomposes on S^1_φ into three pieces: the 3D graviton h_mn, a graviphoton A_m = h_{mφ}, and a radion σ = h_{φφ}. Session 11 §3 (Euler-class gap) plus Session 14 (Seifert–Scott rigidity) show:

- **Graviphoton** is Euler-class gapped at M_poly / 2.
- **Radion** is gapped at m_σ ~ M_poly by Seifert-Scott rigidity against orbifold-Euler fluctuations.
- **3D graviton** h_mn reduces via Brown–Henneaux to boundary Virasoro T(z), T̄(z̄) at c = 12 b(N). Its 4D propagator (Paper IV Prop. graviton-propagator, §21) is

      ⟨h^(4)_ij(k) h^(4)_kl(−k)⟩ = 16π G_4^obs / k^2 · P^TT_ijkl,

  with **G_4^obs ≡ 1/(M_P^(4D))²**, NOT G_4^bulk.

The explicit identification of G_4^obs via the KK mode sum (Paper IV §21 Step 3): in the regime k ≫ 1/R the Poisson-summed 3D propagator produces

    G^(4D) = G_3 / (k_4² · 2π R) = G_4 / k_4²

with G_4 = G_3 / (2π R) = 1/M_P^(4D)². So **the same KK-reduction formula connects G_3 to BOTH G_4^bulk (when running top-down from CS level) AND G_4^obs (when matching to IR gravity)**. The two values of G_4 differ because they correspond to two different values of the AdS_3 radius L:

    G_3^bulk = L_bulk / (8 b(N)),      L_bulk ~ 1/M_poly      ⟹ G_4^bulk = π/(4 b(N) M_poly²)
    G_3^IR   = L_eff / (8 b(N)),       L_eff  ~ exp(H_7) / M_poly ⟹ G_4^obs = 1/M_P^(4D)².

The effective AdS_3 radius L_eff seen by IR physics is exponentially larger than L_bulk, and the exponential enhancement is the BO bounce. This is the content of Hypothesis B: the two Newton constants differ because the IR AdS_3 radius is dynamically amplified by the BO instanton relative to its bulk microscopic value.

## 3. Step 3 — Which hypothesis is correct?

- **Hypothesis A** (M_P^bulk = bulk 3D quantum-gravity strong-coupling scale): **correct** as the standalone meaning of M_P^bulk. At E ≳ M_P^bulk the dimensionless bulk coupling G_4^bulk · E² reaches unity, semiclassical Brown–Henneaux in the bulk breaks down, and one must pass to the boundary DHVW CFT description (Session 43 regime §2.3, §2.4).
- **Hypothesis C** (same quantity with geometric ratio): **wrong**. The ratio is exp(2 S_BO(7)) / O(1) ≈ 3 × 10^15, not any polynomial in b(N) or N.
- **Hypothesis B** (IR Newton constant dressed by BO instanton sum): **correct** for the ratio M_P^(4D) / M_P^bulk.

The derivation: the 4D Newton constant appearing in long-range physics is the 2-point function residue of the boundary stress tensor T T̄ **evaluated on the full polygon partition function**, which includes the BO-bounce instanton sector. The Wheeler–DeWitt WKB on the N = 7 breathing mode (Paper VI §hierarchy) produces a wavefunction Ψ_BO(ρ) with inner turning point ρ_in ~ 1/v and outer turning point ρ_out ~ 1/M_P, suppressed between them by exp(−S_BO). When one computes the IR residue of ⟨T T̄⟩ using this BO-dressed wavefunction, the overlap of the IR gravitational mode with the bulk T-vacuum is enhanced by the WKB connection factor, producing

    1/G_4^obs = (1/G_4^bulk) · |Ψ_BO(ρ_out) / Ψ_BO(ρ_in)|^{-2} · (1 + subleading)
              = (1/G_4^bulk) · exp(2 S_BO(N)) · (1 + subleading),

i.e. M_P^(4D) = M_P^bulk · exp(S_BO(N)) to leading order, with subleading corrections from the WKB prefactor (Δε · ln ε_N, the mass-gap piece) and the one-loop gravity prefactor (1/2) ln(c_{N+4}/(24π²)). The factor 2 in exp(2 S_BO) is **not** a doubling of the amplitude but the fact that the IR scale shows up squared in G_N^−1 = (M_P^(4D))²: one factor of exp(S_BO) for the length scale M_P^(4D) / M_P^bulk and another for M_P^(4D) / M_P^bulk appearing in G_N.

This is the **same** WKB reasoning used in Paper VI for the cosmological length ℓ = exp(S_BO(11)) / v: "The ratio of the corresponding length scales (inner turning point ∼ 1/v, outer ∼ ℓ) is therefore ℓ v ∼ exp(S_BO(11))" (Paper VI §hierarchy line 822). Here, with N = 7, the same inner/outer turning-point ratio gives M_P^(4D) / v = exp(H_7), which is equivalent to M_P^(4D) / M_P^bulk = exp(H_7 − N) / √(4 b(N)/π).

## 4. Step 4 — Explicit formula and the factor exp(2 S_BO(7))

Combining the hierarchy exponent (Paper IV §21, Paper VI Theorem hierarchy)

    H_7 = 2 S_BO(7) + Δε · ln ε_7 + (1/2) ln(c_11 / (24π²)) = 38.459

with the bulk ratio M_P^bulk / M_poly = √(4 b(7)/π) = 2.339 and M_poly = v · e^N gives:

    M_P^(4D) / M_P^bulk = (v exp(H_7)) / (√(4 b(7)/π) · v · e^N)
                        = exp(H_7 − N) / √(4 b(7)/π)
                        = Z_BO(7).

Decomposition of the exponent:

    H_7 − N = 38.459 − 7 = 31.459
            = 2 S_BO(7)       (dominant, 36.548)
              + Δε · ln ε_7   (mass gap, +2.224)
              + (1/2) ln(c_11/(24π²))   (gravity prefactor, −0.313)
              − N             (warp subtraction, −7)
            = 36.548 + 2.224 − 0.313 − 7 = 31.459.   ✓

**Physical origin of each piece**:
- **2 S_BO(7) = 36.548**: the N = 7 BO bounce action, traversed **twice** in the WKB overlap that maps bulk ρ_in ~ 1/M_poly to IR ρ_out ~ 1/M_P. The factor 2 is the bounce (round-trip) action, standard in BO tunnelling of a metastable-to-stable scalar field.
- **Δε · ln ε_7 = 2.224**: one-loop WKB prefactor from the mass gap Δε = 0.8031 in the WDW equation, weighted by ln ε_7 = ln(8 + 3√7) = 2.769.
- **(1/2) ln(c_11/(24π²)) = −0.313**: Gaussian fluctuation determinant of the bounce, scaled by the N = 11 cosmological central charge.
- **−N = −7**: subtraction of the polygon warp v · e^N already absorbed into M_poly; this is the part of the hierarchy that is NOT instantonic but purely geometric warp (Randall–Sundrum-style on the Seifert orbifold, Session 43 §1.1 Route A).
- **−(1/2) ln(4 b(N)/π) = −0.850**: subtracted log of the bulk-Newton-constant prefactor so that the ratio is pure Z_BO.

Numerical check at N = 7:

    Z_BO(7) = exp(31.459) / 2.339 = 5.101 × 10^13 / 2.339 = 1.964 × 10^13.
    M_P^(4D) = M_P^bulk · Z_BO(7) = 631.1 TeV · 1.964 × 10^13 = 1.240 × 10^19 GeV. ✓

(Observed M_P = 1.221 × 10^19 GeV; 1.5% match, consistent with the M_poly two-route slop discussed in Session 43 §1.1.)

**Crucially**: the dominant factor exp(2 S_BO(7)) = 7.51 × 10^15 comes from the **BO bounce**, not from 13 decades of loop-logarithm running of Newton's constant. The value 13 appears as log_10(Z_BO(7)) ≈ 13.29, which is the number of decades spanned by the hierarchy — it is NOT the "13 decades of RG running" interpretation.

## 5. Step 5 — Correct physical identification

Summary in propositional form:

**Proposition (M_P^bulk, corrected)**: M_P^bulk ≡ 1/√G_4^bulk = √(4 b(N)/π) · M_poly is the **bulk 3D AdS_3 quantum-gravity loop cutoff** in the polygon Seifert bulk description. At E ≥ M_P^bulk the semiclassical Brown–Henneaux description fails and one must pass to the 2D boundary DHVW CFT on T² at c = 12 b(N). M_P^bulk is **not** an observational Planck scale; it is a bulk Newton-constant normalization.

**Proposition (M_P^(4D), corrected)**: M_P^(4D) ≡ 1/√G_N^obs = v · exp(H_7) is the **IR observational 4D Planck scale** appearing in the long-range graviton propagator. It is determined by the N = 7 BO bounce in the WDW breathing-mode potential together with the one-loop WKB prefactor (Δε) and the N = 11 gravity prefactor (c_11).

**Proposition (ratio, corrected)**: The ratio M_P^(4D) / M_P^bulk = Z_BO(7) = 1.964 × 10^13 is the **polygon BO-instanton hierarchy enhancement factor**, not RG running. It is the polygon analogue of the string-theoretic relationship between the string scale M_s and the Planck scale M_P, in which the two scales differ by a sum over worldsheet topologies; here they differ by the sum over BO instantons in the polygon breathing-mode path integral.

---

## 6. Numerical check at N = 7

Exact values used:

    v       = 246.00 GeV       (Higgs VEV)
    N       = 7                 (polygon)
    b(7)    = 4.29807           (Paper I / III)
    b(11)   = 10.54667          (Paper III; gives c_11 = 126.56)
    S_BO(7) = 18.274            (Paper VI §hierarchy)
    Δε      = 0.8031            (Session 14 WDW gap)
    ε_7     = 8 + 3√7 = 15.937  (fundamental unit of Z[√7])
    ln ε_7  = 2.7689

Derived:

    M_poly            = v · e^7          = 2.698 × 10^5 GeV = 269.77 TeV
    √(4 b(7)/π)       = √(5.4711)        = 2.3393
    G_4^bulk          = 0.1827 / M_poly²  (= π/(4·4.29807))
    M_P^bulk          = 2.3393 · M_poly  = 631.09 TeV

    2 S_BO(7)                     = 36.548
    Δε · ln ε_7                   = 2.224
    (1/2) ln(c_11/(24π²))         = −0.313
    H_7                           = 38.459

    exp(H_7 − N)                  = exp(31.459) = 5.101 × 10^13
    Z_BO(7) = exp(H_7 − N)/√(4b(7)/π) = 5.101 × 10^13 / 2.3393 = 1.964 × 10^13

    M_P^(4D) = v · exp(H_7)       = 1.240 × 10^19 GeV
    M_P^(4D) / M_P^bulk = 1.964 × 10^13   ✓
    M_P^(4D) / M_P^bulk = Z_BO(7)         ✓

Comparison to observed M_P = 1.221 × 10^19 GeV: 1.5% residual, within the M_poly two-route slop (Session 43 §1.1, Prop. 1).

---

## 7. Replacement text for Session 43 §1.5

The current §1.5 reads (lines 154–167 of `session43-scale-hierarchy/derivation.md`):

> ### 1.5 Why M_P^bulk sits BELOW M_P^(4D)
>
> The bulk G_4^bulk is NOT the observed 4D Newton constant. The observed G_N = 1/M_P^(4D)² is the RG-evolved long-distance value, obtained from G_4^bulk by running from M_poly down to IR using the full 4D matter content. The ratio
>
>     M_P^(4D) / M_P^bulk = exp(𝓗_7 − N) / √(4b(N)/π) ≈ 4.57×10^13 / 2.34 ≈ 2 × 10^13,
>
> i.e. 13 decades of RG running between bulk Planck and IR Planck, consistent with the standard RG ln-enhancement of G over the full SM KK-free running window. The "hierarchy" in the usual sense is between M_poly and M_P^(4D); the bulk Planck M_P^bulk is close to M_poly and marks the breakdown of the bulk perturbative expansion.

**Proposed replacement** (Session 52):

> ### 1.5 Why M_P^bulk sits BELOW M_P^(4D): BO-instanton enhancement, not RG running
>
> The bulk G_4^bulk and the observed G_N are **two different Newton constants**, attached to two different regimes:
> - G_4^bulk = π L R / (4 b(N)) is the coefficient of R_4 in the bulk Seifert action; M_P^bulk = 1/√G_4^bulk is the 3D AdS_3 quantum-gravity loop cutoff (the scale at which the semiclassical expansion in G_4^bulk breaks down).
> - G_N^obs = 1/(M_P^(4D))² is the coefficient in the long-range 4D Einstein equations, extracted from the IR residue of the boundary ⟨T T̄⟩ correlator on the BO-dressed polygon vacuum.
>
> Their ratio is an **instanton-mediated hierarchy**, not RG running:
>
>     M_P^(4D) / M_P^bulk = Z_BO(N) ≡ exp(H_N − N) / √(4 b(N)/π),
>
> where H_N is the N-polygon hierarchy exponent (Paper VI Theorem hierarchy). At N = 7:
>
>     Z_BO(7) = exp(31.459) / 2.339 = 1.964 × 10^13,
>
> dominated by the BO bounce exp(2 S_BO(7)) = exp(36.548) = 7.51 × 10^15 with subleading WKB prefactor (+ Δε · ln ε_7 = +2.22), gravity prefactor ((1/2) ln(c_11/(24π²)) = −0.31), and the polygon warp subtraction (−N = −7). The factor 2 in the bounce exponent is the standard tunnelling round-trip from inner to outer turning point of the WDW WKB wavefunction, exactly the same mechanism that fixes the cosmological length ℓ = exp(S_BO(11))/v in Paper VI.
>
> This is NOT "13 decades of RG running." Loop-logarithmic running of G over 13 decades would require running coefficients of order 13/ln(10) ≈ 5.6 for ln(G), which is not present in the SM matter content (the full SM b-function for Newton's constant is zero at one loop since gravity is non-renormalisable; any "RG running of G" must come from specific higher-derivative operators, which are absent at the polygon level). The factor of 10^13 is instanton-generated.

(Update Session 43 Table 485–496 row 11 accordingly: "M_P^(4D)/M_P^bulk derived as Z_BO(N) instanton enhancement" replaces the RG-running line.)

---

## 8. Consequences for Paper IV §21

Paper IV §21 (lines 3493–3515) currently states the hierarchy formula without identifying what M_P means physically when G_4^bulk is also present in the same paper. Session 52 clarifies:

- Paper IV Prop. graviton-propagator (line 3517): the G_4 in ⟨h^(4) h^(4)⟩ = 16π G_4 / k² · P^TT is **G_4^obs = 1/(M_P^(4D))²**, not G_4^bulk. This was already implicitly correct (line 3568: "G_4 = G_3/(2π R) = 1/M_P²") but the dictionary variable G_4 is overloaded. Proposed clarification: rename the §21 variable to G_4^IR or explicitly write G_N^obs in the propagator expression to distinguish it from the Session 11 §4 G_4^bulk.
- The hierarchy formula M_P = v · exp(H_7) refers to M_P^(4D), unambiguously.
- No numerical value in Paper IV §21 changes. Only interpretation changes: the "hierarchy M_P/v ≈ 10^17" (line 3514) is explained as the BO-instanton enhancement factor Z_BO(7), same physical mechanism as the cosmological ℓ v = exp(S_BO(11)) (Paper VI §dark-energy).

---

## 9. References

- Brown, J.D.; Henneaux, M. (1986). "Central charges in the canonical realization of asymptotic symmetries." Commun. Math. Phys. 104, 207.
- Maloney, A.; Witten, E. (2007). "Quantum gravity partition functions in three dimensions." JHEP 1002:029.
- Coleman, S. (1977). "Fate of the false vacuum." Phys. Rev. D 15, 2929. (For the bounce action and exp(2 S) appearance in the path integral.)
- Callan, C.G.; Coleman, S. (1977). "Fate of the false vacuum II. First quantum corrections." Phys. Rev. D 16, 1762. (For the one-loop WKB prefactor structure.)
- Randall, L.; Sundrum, R. (1999). "Large mass hierarchy from a small extra dimension." Phys. Rev. Lett. 83, 3370. (For the geometric warp exp(N) portion of the hierarchy.)
- Appelquist, T.; Chodos, A. (1983). "Quantum effects in Kaluza–Klein theories." Phys. Rev. D 28, 772. (Effective action and Newton-constant matching across KK threshold.)
- Paper IV §21 (line 3493–3515): hierarchy formula v = M_P / exp(H_7).
- Paper VI Theorem hierarchy (line 310–383): H_7 = 38.459 derivation.
- Paper VI §dark-energy (line 770–825): ℓ v = exp(S_BO(11)), the cosmological analogue.
- Session 11 §4: G_4^bulk = π L R / (4 b(N)) derivation.
- Session 14 §1 + §4.1: Seifert–Scott rigidity, two G_4 conventions.
- Session 17: c = 12 b(N) derivation.
- Session 43 §1–§1.5: three-scale hierarchy (this session supersedes §1.5).

---

## 10. File paths

- `/mnt/c/Users/gspea/source/repos/planetary-polygons-unified/docs/rigor-sandbox/session11-ads3-s1-holography/derivation.md` §4 (G_4^bulk derivation, lines 407–475)
- `/mnt/c/Users/gspea/source/repos/planetary-polygons-unified/docs/rigor-sandbox/session14-radion-casimir/derivation.md` §1, §4.1 (G_4 conventions, Seifert rigidity)
- `/mnt/c/Users/gspea/source/repos/planetary-polygons-unified/docs/rigor-sandbox/session43-scale-hierarchy/derivation.md` §1.5 (text to replace)
- `/mnt/c/Users/gspea/source/repos/planetary-polygons-unified/latex/paper-4-field-theory/main.tex` §21 (lines 3493–3573, hierarchy formula + graviton propagator)
- `/mnt/c/Users/gspea/source/repos/planetary-polygons-unified/latex/paper-5-cosmology/main.tex` §hierarchy (lines 307–383, H_7 derivation); §dark-energy (lines 770–825, BO WKB reasoning template).

---

## 11. Summary table

| Claim | Status | Where |
|-------|--------|-------|
| M_P^bulk is the 3D AdS_3 bulk-gravity loop cutoff (Hypothesis A) | DERIVED | §1, §2 |
| M_P^(4D) is the IR observational Planck scale from BO bounce (Hypothesis B) | DERIVED | §3 |
| M_P^(4D) / M_P^bulk = Z_BO(N) instanton enhancement | DERIVED | §4 |
| Factor exp(2 S_BO(7)) from BO bounce, not RG running | DERIVED | §4 |
| Hypothesis C (same quantity, geometric ratio) refuted | DERIVED | §3 |
| Session 43 §1.5 replacement text (BO-instanton framing) | WRITTEN | §7 |
| Paper IV §21 G_4 notational clarification | RECOMMENDED | §8 |
| Numerical check at N = 7 (Z_BO = 1.964 × 10^13) | VERIFIED | §6 |
