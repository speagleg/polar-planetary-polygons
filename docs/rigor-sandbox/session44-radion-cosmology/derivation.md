# Session 44 — Cosmological role of the stabilized radion σ_*
## Tier 4.3 sub-item 4.3B: inflaton / dark matter / spectator?

**Date**: 2026-04-18
**Goal**: Determine the cosmological role of the stabilized radion σ_* given
the derived radion potential V(σ) = N²/(8σ²) − c_N/(12σ) + Λ_3·σ, the
minimum σ_* ≈ 1.347 at N=11, and the mass range m_σ ∈ [16, 98] M_poly
(≈ 5–30 PeV) from Sessions 31/34/39.

---

## 0. Bottom line

The stabilized polygon radion is a **cosmological spectator that decays
before BBN, triggering reheating to T_rh ~ 0.2–3 GeV**. It is not a
viable inflaton (standard slow-roll at the paper's "inflection point" is
far from slow-roll, and the ADM 2008 formula cited in Paper VI is
misapplied); it is not dark matter (decay well before BBN via
gravitational portal); it is a transient ingredient that sets the
reheating temperature and dilutes any prior relic. Paper VI's
Ω_Λ = 0.695 and Ω_b = 0.049 are not destabilized — they were derived
at the radion minimum and correspond to the late-time cosmology after
σ has settled.

**Verdict on the three candidate roles**:

| Role | Verdict | Key number |
|------|---------|------------|
| (A) Inflaton | **NO** (at standard slow-roll level) | ε(σ_infl)=0.032, n_s=0.81, r=0.52 |
| (B) Dark matter | **NO** (decays before BBN) | τ_σ ∈ [4×10⁻⁹, 9×10⁻⁷] s ≪ 1 s |
| (C) Spectator / reheater | **YES** | T_rh ∈ [0.2, 3] GeV, safe for BBN |

The AdS_4 vacuum at V(σ_*) ≈ +9.35 (polygon units at N=11) does
**NOT** have a known closed uplift mechanism to Minkowski/de Sitter
within the framework; this remains the single genuine open problem of
Tier 4.3 and is explicitly flagged below (§6).

---

## 1. Setup

### 1.1 Radion potential and minimum (Paper VI eq. V-radion, line 1591–1599)

$$
V(\sigma) \;=\; \frac{N^{2}}{8\sigma^{2}} \;-\; \frac{c_{N}}{12\sigma} \;+\; \Lambda_{3}\sigma,
\qquad c_{N} = 12\,b(N),\quad \Lambda_{3} = \frac{N^{2}-16}{16}.
$$

At N=11: b(11) = 10.5466, c_11 = 126.56, Λ_3 = 105/16 = 6.5625.

Critical-point data (verified numerically, see §7):
- σ_* (minimum): 1.3471,  V(σ_*) = 9.346,  V''(σ_*) = 18.93
- σ_infl (V'' = 0): 4.3023,  V(σ_infl) = 26.60,  V'(σ_infl) = 6.752
- σ_start (from N-selection, 3·σ_infl per Paper VI line 1606): 12.907

### 1.2 Radion mass

From Session 39 (2-modulus at N=11, correct Thurston ratio):
$$
m_{-}= 56.40\,M_{\mathrm{poly}},\qquad m_{+}= 97.68\,M_{\mathrm{poly}}.
$$
From Session 31 (single-modulus, corrected |C_base| = 0.0065): m_σ ∈
[16, 28] M_poly on the AdS_4 branch.

With M_poly = 300 TeV:
- Single modulus: m_σ ∈ [4.8, 8.4] PeV.
- Two-modulus (heavy ρ mode): m_{+} up to ~30 PeV.

This places the radion **far above the electroweak scale** and
**far below the Planck scale**.

### 1.3 Three candidate roles

(A) Inflaton: σ slow-rolls from σ_start to σ_*, driving inflation.
(B) Dark matter: stable on cosmological timescales, misalignment relic.
(C) Spectator: reaches minimum rapidly, decays to SM, irrelevant to
    late cosmology.

---

## 2. (A) Inflaton candidate — does NOT survive standard slow-roll

### 2.1 What Paper VI claims (§ 18, lines 1620–1639)

Cites Allahverdi–Dutta–Mazumdar 2008 (ADM) "inflection-point inflation":
$$
n_{s} \;=\; 1 \;-\; \frac{8}{3\sqrt{3}\,N_{e}},
\qquad r \sim 10^{-6}.
$$

### 2.2 Issue — ADM 2008 regime does NOT apply

The ADM 2008 formula derives from a **pure cubic normal form**
V(φ) = V₀ + (λ/6)(φ − φ_infl)³ around an inflection point where
**both V' = 0 AND V'' = 0**. In that regime V'/V is parametrically
small and slow-roll is automatic.

In the polygon radion at N=11, **V'(σ_infl) = 6.75 is non-zero**
(V(σ_infl) = 26.6, so V'/V = 0.254). There is no inflection point
with V' ≈ 0; only V'' = 0. This is dominated by the linear Λ_3·σ
piece, making the potential LINEAR-PLUS-small-corrections for
σ ≳ σ_infl, not cubic-plus-inflection.

### 2.3 Standard slow-roll at σ_infl

$$
\epsilon_{V} \;=\; \tfrac{1}{2}\!\left(\frac{V'}{V}\right)^{2}_{\!\sigma_{\mathrm{infl}}}
\;=\; \tfrac{1}{2}\!\left(\frac{6.752}{26.60}\right)^{2} = 0.0322,
$$
$$
\eta_{V} \;=\; \left.\frac{V''}{V}\right|_{\sigma_{\mathrm{infl}}} = 0
\quad\text{(definition of }\sigma_{\mathrm{infl}}\text{)}.
$$

Therefore at σ_infl:
$$
n_{s} \;=\; 1 - 6\epsilon_{V} + 2\eta_{V} \;=\; 0.807,
\qquad r \;=\; 16\epsilon_{V} \;=\; 0.515.
$$

**Both badly off**: Planck 2018 gives n_s = 0.9665 ± 0.0038 (40σ
tension), BICEP/Keck gives r < 0.036 (14× over the bound).

### 2.4 Slow-roll at σ_start = 12.9 (the initial condition Paper VI assumes)

At σ_start the linear term dominates and V(σ) ≈ Λ_3·σ:
$$
\epsilon_{V}(\sigma_{\mathrm{start}}) = 3.10\times 10^{-3},
\qquad \eta_{V}(\sigma_{\mathrm{start}}) = -7.79\times 10^{-5}.
$$

These ARE slow-roll. But the single-field slow-roll prediction for a
LINEAR potential V = Λσ is n_s = 1 − 3/N_e, giving at N_e = 60
**n_s = 0.950** (vs Planck 0.967, 4σ off) and
$$
r = \frac{4}{N_{e}} = 0.067
$$
which **exceeds BICEP/Keck r < 0.036 by nearly 2×**.

Number of e-folds from σ_infl to σ_start (direct quadrature):
$$
N_{e} \;=\; \int_{\sigma_{\mathrm{infl}}}^{\sigma_{\mathrm{start}}} \frac{V}{V'}\,\mathrm{d}\sigma \;=\; 71.6.
$$

Sufficient e-folds exist, but the tilt and tensor ratio are in tension
with Planck and BICEP/Keck.

### 2.5 Conclusion on inflaton role

**The radion is not a viable inflaton at standard slow-roll order.** The
ADM 2008 inflection-point regime cited in Paper VI §18 does not apply
because the radion potential has V'(σ_infl) ≠ 0 at the "inflection
point". The polygon radion potential in the slow-roll regime behaves
as a **linear inflaton**, which is disfavoured by Planck 2018 and
excluded by BICEP/Keck on r.

**GAP**: Paper VI's §18 inflation section conflates "inflection point"
(V'' = 0) with "ADM inflection point" (V' = V'' = 0). The r ~ 10⁻⁶
claim is not supported for this potential.

---

## 3. (B) Dark matter candidate — does NOT survive decay kinematics

### 3.1 Radion decay channels

Because the radion couples to the 4D trace of the SM stress-energy
T^μ_μ via the standard moduli-gravitational portal (coefficient
1/M_P^{bulk} after Weyl rescaling), the decay rate to any SM channel
kinematically below 2m_σ is parametrically
$$
\Gamma_{\sigma \to XX} \;\sim\; \frac{m_{\sigma}^{3}}{M_{P}^{2}},
$$
up to O(1) coefficients that depend on the channel.

Available channels at m_σ ∈ [5, 30] PeV:
- σ → hh (dominant — universal Higgs-portal mass term from Weyl
  rescaling, branching ratio O(1/4)).
- σ → W⁺W⁻, ZZ (gauge-boson pair, branching O(1/10) each).
- σ → t̄t, b̄b, … (loop-suppressed for σ–Higgs trace coupling).
- σ → γγ, gg (one-loop, small).
- σ → KK modes: **kinematically forbidden** (first KK has
  m ≥ M_poly/2 ≈ 150 TeV ≫ m_σ/2 — wait: actually m_σ/2 ≈ 2.4 PeV ≫
  M_poly/2 ≈ 150 TeV, so KK IS accessible; revised below).

**Correction on KK kinematics**: m_σ ∈ [4.8, 30] PeV ≫ M_poly = 300 TeV.
Therefore **KK modes ARE kinematically accessible** (m_σ ≳ 16·M_poly,
so first several KK layers up to KK number n ≈ 8 are on shell).
Decays σ → 2·KK dominate with parametrically equivalent rate
Γ ~ m_σ³/M_P².

Total width (order of magnitude):
$$
\Gamma_{\sigma}^{\mathrm{tot}} \;\approx\; c\cdot \frac{m_{\sigma}^{3}}{M_{P}^{2}},
\qquad c \in [1, 10]\text{ from counting channels}.
$$

### 3.2 Lifetime

$$
\tau_{\sigma} \;=\; \frac{1}{\Gamma_{\sigma}} \;=\;
\frac{M_{P}^{2}}{c\cdot m_{\sigma}^{3}}.
$$

Numerical values (c = 1):

| m_σ | Γ_σ (GeV) | τ_σ (s) |
|---|---|---|
| 4.8 PeV (low single-mod) | 7.4×10⁻¹⁹ | 8.9×10⁻⁷ |
| 8.4 PeV (high single-mod) | 4.0×10⁻¹⁸ | 1.65×10⁻⁷ |
| 17 PeV (low 2-mod) | 3.2×10⁻¹⁷ | 2.1×10⁻⁸ |
| 29 PeV (high 2-mod) | 1.7×10⁻¹⁶ | 3.9×10⁻⁹ |

**All lifetimes are ≪ 1 second**, the BBN onset time. Including the
channel-multiplicity factor c ~ 10 would shrink τ by another order of
magnitude.

### 3.3 Relic-abundance assessment

The radion decays well before any epoch where a DM relic could be
stored: **by t ≈ 10⁻⁷ s** the radion is gone. Independent of the
initial σ-displacement from σ_*, misalignment oscillations at
H ~ m_σ damp as R⁻³ until decay, and the decay is complete by
T ≈ 1 GeV (see §3.4). No radion DM relic survives. ✗

### 3.4 Reheating temperature

Assuming instantaneous decay at H ~ Γ_σ (standard sudden-decay
approximation), the radion radiation-dominates and sets
$$
T_{\mathrm{rh}} \;\approx\; \left(\frac{90}{g_{*}\,\pi^{2}}\right)^{1/4}\!
\sqrt{\Gamma_{\sigma}\,M_{P}} \;\approx\; 0.2\!\cdot\!\sqrt{\Gamma_{\sigma}\,M_{P}}.
$$
With g_* ≈ 106.75 (SM relativistic DOF at GeV scale):

| m_σ | T_rh (GeV) |
|---|---|
| 4.8 PeV | 0.18 |
| 8.4 PeV | 0.41 |
| 17 PeV | 1.15 |
| 29 PeV | 2.66 |

All ≳ 1 MeV (BBN onset), ≲ 3 GeV (before QCD transition at
≈ 150 MeV for most of the range, above for the heaviest end).
**BBN is safe**; primordial nucleosynthesis proceeds in a
radiation-dominated universe seeded by radion decay.

### 3.5 Conclusion on DM role

**The radion is not dark matter.** Lifetime 10⁻⁹–10⁻⁷ s is too short
by 25+ orders of magnitude. It **decays into SM and KK radiation well
before BBN**, setting T_rh ∈ [0.2, 3] GeV depending on the chosen
radion-mass value within the derived range.

---

## 4. (C) Spectator / reheater — confirmed

From §2 (not an inflaton) and §3 (not DM), the remaining role is
spectator: σ reaches σ_* during/after the N-selection tunnelling
event, oscillates, and decays. Let's verify this is self-consistent.

### 4.1 Timeline

1. **N-selection tunnelling** at ρ*_11 = 4.45 (Paper VI §n-selection).
   σ initial value σ_start ≈ 12.9 (Paper VI line 1605).
2. **Oscillation onset** at H ≈ m_σ, corresponding to
   t_osc ≈ 1/m_σ ≈ 3×10⁻²⁹ s (for m_σ = 5 PeV).
3. **Oscillation phase**: σ behaves as pressureless matter with
   energy density ρ_σ ∝ R⁻³ (coherent oscillations).
4. **Decay** at t ≈ τ_σ ∈ [10⁻⁹, 10⁻⁷] s.
5. **Reheating**: radiation-dominated universe at T_rh ∈ [0.2, 3] GeV.
6. **BBN** at t ≈ 1 s, T ≈ 1 MeV: standard outcome.
7. **Subsequent evolution**: standard Big Bang with SM + polygon-sector
   dark matter (frozen Havelock modes, Paper VI §19).

### 4.2 Energy budget during oscillation phase

The radion dominates the energy density from t_osc to τ_σ. During
this matter-dominated phase, the standard Lyth-lower-bound-style
analysis applies and the universe is radiation-dominated AFTER decay.
Paper VI's CC budget (Ω_Λ = 0.695) is an **asymptotic late-time**
statement; the radion oscillation–decay phase is a transient with
duration ≲ 10⁻⁷ s and no impact on late observables.

### 4.3 Consistency with Paper VI Ω_Λ, Ω_b predictions

Paper VI Proposition "cosmology" (table at line 1071–1074):
Ω_Λ = 68.3%, Ω_DM = 26.7%, Ω_b = 4.97%. These are derived from
the polygon action at the stabilized vacuum σ = σ_*, with Λ_4 =
Λ_3 / ℓ². Since σ sits at its minimum at all epochs probed by Planck
(z ≤ 1100), Paper VI's energy-budget predictions are **unaffected**
by radion dynamics in the early universe. ✓

The radion's zero-point energy (1/2)m_σ in Paper VI eq. F-DE contributes
N/4 to F_DE; this is the zero-point energy AT the minimum and is
unchanged. ✓

---

## 5. Falsifiable signatures

Even as a "spectator" the polygon radion is NOT unobservable. Four
potentially detectable signatures:

### 5.1 Reheating temperature T_rh ≤ 3 GeV

The polygon framework predicts T_rh ∈ [0.2, 3] GeV, well below the
electroweak scale. This has two consequences:
- **Leptogenesis must occur at T > T_rh**, or equivalently via
  post-reheating dynamics (e.g., low-scale leptogenesis at T ~ GeV).
  Paper VI's η_B = 6.1×10⁻¹⁰ (§ cosmology-sector) must be tested
  against this temperature constraint.
- **WIMP-like relics with m > 100 GeV and standard freeze-out are
  impossible** in this framework (they never thermalize). This
  **independently rules out the polygon framework if TeV-scale WIMP DM is
  discovered at freeze-out abundance**.

### 5.2 No primordial gravitational waves

The radion is not an inflaton in the standard slow-roll sense (§2),
so the polygon framework predicts **no polygon-radion-sourced inflation
and no polygon-sourced primordial tensor modes r**. If a separate
inflation sector exists (e.g., Higgs inflation in the SM), that must
supply N_e ≳ 60 and the observed n_s. The framework, as currently
formulated, does not identify such a sector.

**Falsification**: a robust primordial-GW detection at r ~ 10⁻³ tied to
specifically radion-driven inflation (e.g., with n_s = 1 − 8/(3√3 N_e))
is NOT expected; detection of any primordial-GW signal leaves the
polygon framework agnostic but does not falsify it. Non-detection of
r > 0.03 is fully consistent.

### 5.3 Gravitational-wave echoes from radion oscillation

During the oscillation–decay phase the radion may source a
stochastic GW background at frequency
$$
f_{\mathrm{GW}}^{\mathrm{today}} \;\sim\; \left(\frac{T_{\mathrm{rh}}}{100\,\mathrm{GeV}}\right)\!\times 10^{2}\,\mathrm{Hz} \;\sim\; 0.2\,\mathrm{Hz}
$$
for T_rh ≈ 0.2 GeV. The amplitude is parametrically
Ω_GW ~ (m_σ / M_P)² ~ 10⁻²⁵, far below LISA sensitivity (~10⁻¹²).
**Not detectable**.

### 5.4 Radion-induced CMB spectral distortion

The radion decays at T_rh ~ 1 GeV ≫ T_CMB,eq = 1 eV, so its SM decay
products fully thermalize before recombination; **no CMB μ or y
distortions beyond the standard reionization bath**. Null observation
of CMB spectral distortions at PIXIE sensitivity is consistent.

### 5.5 Scenario-specific "smoking gun"

The **specific prediction that survives** from the polygon radion:
no WIMP-DM freeze-out at m > 1 TeV within the polygon framework.
This distinguishes the polygon framework from generic GUT or
SUSY-based moduli scenarios where T_rh can reach the TeV scale
(reheating from PeV moduli gives T_rh ~ few GeV at most).

---

## 6. Uplift mechanism for the AdS_4 vacuum — open problem

### 6.1 The deep question

At σ = σ_* the potential value is V(σ_*) = 9.35 (in polygon natural
units; §1.1 above). In the full multi-modulus treatment (Session 18,
39), V_* ≈ −8×10⁴ corresponds to a 4D AdS vacuum with Λ_4 ~ −M_poly⁴
(Session 39 §Λ_7 = −8×10⁴ gives Λ_4 ~ Λ_7/ℓ² after dimensional
restoration). The observed universe is de Sitter with Λ_4 > 0.

**Paper VI's resolution**: line 1049 (original) stated "stabilized at
unit radius by the flux N/2"; CHANGE 9 from Session 39 updates this
to "σ_* ≈ 1.35 in an AdS_4 natural vacuum, Minkowski/dS emerges via
an external mechanism not closed at 1-loop."

### 6.2 Uplift candidates considered and ruled out (Session 39 §all-B paths)

1. **KKLT-type brane uplift**: requires anti-D3-branes or similar;
   polygon framework has no branes. **Not available**.
2. **Non-perturbative uplift (Euclidean-instanton uplift)**:
   exponentially suppressed by S_inst ≈ 2π k_frac ≈ 0.6 (too small
   to matter) or S_BO = 102.7 (gives a shift of
   O(e⁻¹⁰² M_poly⁴) ~ 10⁻⁴⁵ M_poly⁴, too tiny).
3. **Ω second modulus ρ adjusts V_* = 0**: Session 39 showed the ρ
   direction is **tachyonic** at V_* = 0 for all tested |C_base|;
   fails.
4. **Bulk-BO instanton Λ ≈ 0.695 as the uplift**: Paper VI's CC chain
   assigns Λ_4 = Λ_3/ℓ² ≈ 10⁻⁸⁴ GeV², which is EXACTLY the observed
   CC. The conjecture that the BO-instanton Λ_3 = (N²−16)/16 already
   acts as the uplift on top of the AdS_4 V_* is attractive, but
   requires matching the scale of the AdS_4 V_* ~ −25 M_poly⁴ (Session
   39) against Λ_4(obs) ~ 10⁻⁴⁷ M_poly⁴, a fine-tuning gap of ~48
   orders of magnitude.

### 6.3 Honest status

The **AdS_4 → Minkowski uplift is an open problem** within the polygon
framework at the rigour achieved in Sessions 18, 39. It is inherited
from the broader moduli-stabilisation literature (KKLT, the swampland)
and is NOT solved by the polygon construction alone.

However, the AdS_4 character at σ_* is an **EFT-level property at one
loop**. At full quantum gravity level (E → M_P^(4D)) Paper IV §20 claims
UV completeness via the 2D boundary CFT at c = 12·b(N); the cosmological
constant of the full theory is set by the boundary BO-instanton action
S_BO(11) = 102.7, not by the bulk radion potential at σ_*. The two
statements are compatible because they refer to different energy
regimes (Session 43 table §4). In this sense, the radion's AdS_4
behaviour in the 4D EFT is a feature of the low-energy effective
action that does NOT feed directly into the observed Λ_4, which comes
from a different (non-perturbative, S_BO) saddle.

**Net**: the polygon framework has TWO candidate cosmological-constant
contributions — the one-loop radion V_* (AdS_4, O(M_poly⁴)) and the
non-perturbative S_BO-instanton Λ ~ e⁻²ᴼᴮᴼ M_P⁴ (observed 10⁻¹²⁰).
Paper VI takes the second as physical and implicitly assumes the
first is cancelled by an unknown mechanism. This is the standard
"old cosmological constant problem" and is **not claimed to be solved**
in the polygon framework. The radion's cosmological role in this
session (§§1–5) is evaluated on the ASSUMPTION that this cancellation
holds; none of the verdicts change if the AdS_4 scale is shifted by
the putative uplift.

---

## 7. Numerical verification

Compute all key values independently (with scipy for numerical
root-finding):

```
b(11) = 10.5466
c_11 = 126.5597
Lambda_3 = 6.5625
σ_min = 1.3471,  V(σ_min) = 9.346,  V''(σ_min) = 18.93
σ_infl = 4.3023,  V(σ_infl) = 26.60,  V'(σ_infl) = 6.752
σ_start = 3·σ_infl = 12.907
At σ_infl: ε_V = 0.0322, η_V = 0 → n_s = 0.807, r = 0.515 (TENSION)
At σ_start: ε_V = 3.10×10⁻³, η_V = −7.79×10⁻⁵ → linear-inflation
  r = 4/N_e ≈ 0.067 at N_e=60 (fails BICEP/Keck)
N_e integral σ_infl → σ_start: 71.6 (sufficient if parameters worked)

Radion mass → gravitational decay:
  m_σ = 4.8 PeV: Γ = 7.4×10⁻¹⁹ GeV, τ = 8.9×10⁻⁷ s, T_rh ≈ 0.18 GeV
  m_σ = 8.4 PeV: Γ = 4.0×10⁻¹⁸ GeV, τ = 1.65×10⁻⁷ s, T_rh ≈ 0.41 GeV
  m_σ = 17  PeV: Γ = 3.2×10⁻¹⁷ GeV, τ = 2.1×10⁻⁸ s,  T_rh ≈ 1.15 GeV
  m_σ = 29  PeV: Γ = 1.7×10⁻¹⁶ GeV, τ = 3.9×10⁻⁹ s,  T_rh ≈ 2.66 GeV

All τ ≪ 1 s = BBN onset.
All T_rh ≫ 4 MeV = BBN temperature (safe).
```

These are reproduced in
`/mnt/c/Users/gspea/source/repos/planetary-polygons-unified/docs/rigor-sandbox/session44-radion-cosmology/derivation.md §7`.

---

## 8. Paper edits required

### CHANGE 11 (PAPER4_REVISION_DRAFT.md) — NOT applied in this session

The following edits SHOULD be prepared for the next revision round
but are **NOT applied automatically** per session rules:

**Paper VI §18 (lines 1587–1639)**:
1. The ADM 2008 inflection-point formula n_s = 1 − 8/(3√3 N_e) does
   not apply to eq. V-radion at N=11, because V'(σ_infl) = 6.75 ≠ 0.
   Standard slow-roll gives n_s = 0.807, r = 0.52 at σ_infl; large
   slow-roll at σ_start gives r = 4/N_e ≈ 0.067 (in 2σ tension with
   BICEP/Keck).
2. The claim "r ~ 10⁻⁶ (negligible)" is NOT supported by the derived
   radion potential; it would require an ADM-type inflection where
   V' vanishes at the inflection point, which this potential does
   not have.
3. **Recommended replacement**: re-label §18 from "Radion inflation"
   to "Radion cosmology" or drop the inflaton identification entirely,
   acknowledging the radion as a spectator that reheats to
   T_rh ∈ [0.2, 3] GeV. A separate (non-polygon) inflation sector
   (e.g., Higgs inflation) must supply the observed n_s and
   sufficient e-folds; the polygon framework does not derive the
   observed inflationary spectrum.
4. The radion's observable signature is T_rh ≤ 3 GeV, which
   constrains (not falsifies) any post-inflation thermalization
   scenario in the framework.

**Paper VI §dark-matter (lines 1643–1700)**:
No change. The dark-matter candidate in Paper VI is the FROZEN
HAVELOCK MODES at ρ = ρ*, not the radion. The current §19 analysis
applies unchanged. The fact that the radion itself is NOT a DM
candidate is consistent with Paper VI's existing architecture
(which already attributes DM to frozen Havelock modes, not to σ).

**Paper VI line 1048–1052** (already flagged by Session 39 CHANGE 9):
"stabilized at unit radius by the flux N/2" → "stabilized at σ_* ≈
1.35 by the balance between flux and Casimir+Λ, with mass
m_σ ∈ [16, 98] M_poly (≈ 5–30 PeV)."

### Paper IV edits (none)

Paper IV does not claim radion inflation. Its §20 UV-completeness
claim (Session 43 closure) is independent of the radion's cosmological
role.

---

## 9. What remains open after this session

**Tier 4.3B is CLOSED** in the following precise sense:
- The radion's role has been classified (spectator; not inflaton, not
  DM).
- The decay rate, reheat temperature, and impact on BBN have all been
  computed at O(1) precision.
- Paper VI's Ω_Λ, Ω_DM, Ω_b predictions are shown to be robust to
  radion dynamics (they are late-time asymptotic).

**Open for Tier 4.3C (next sub-item)**:
- Inflation sector identification: the polygon framework does not
  currently supply an inflaton that produces the observed n_s =
  0.9665 and r < 0.036. A companion non-polygon mechanism (e.g.,
  Higgs inflation or Starobinsky) must be assumed or derived.
- N-selection tunnelling rate: Paper VI §n-selection asserts
  σ_start ≈ 3 σ_infl; an independent check of this initial condition
  from the Born-Oppenheimer tunnelling wavefunction is a natural
  Tier 4.3C item.
- Uplift mechanism for AdS_4 → Minkowski: explicitly not closed (§6
  above).

**Other Tier 4.3 sub-items**:
- 4.3A: spectator vs. inflaton (this session, closed as SPECTATOR).
- 4.3B: DM candidate analysis (this session, closed as NOT DM).
- 4.3C: inflation sector (open; companion mechanism needed).
- 4.3D: N-selection tunnelling rate (open).

---

## 10. References

- Allahverdi, R.; Dutta, B.; Mazumdar, A. (2008). "Inflection-point
  inflation and post-inflationary physics." Phys. Rev. D 81, 083538.
  (Cited in Paper VI §18 but regime does NOT apply — see §2.2.)
- Coughlan, G.D.; Fischler, W.; Kolb, E.W.; Raby, S.; Ross, G.G.
  (1983). "Cosmological problems for the Polonyi potential." Phys.
  Lett. B 131, 59. (Original moduli-decay problem.)
- Banks, T.; Kaplan, D.B.; Nelson, A.E. (1994). "Cosmological
  implications of dynamical supersymmetry breaking." Phys. Rev. D
  49, 779. (Moduli decay rate Γ ~ m³/M_P².)
- Kofman, L.; Linde, A.; Starobinsky, A.A. (1994, 1997). "Reheating
  after inflation." Phys. Rev. Lett. 73, 3195; Phys. Rev. D 56, 3258.
- Randall, L.; Sundrum, R. (1999). "Large mass hierarchy from a
  small extra dimension." Phys. Rev. Lett. 83, 3370. (Radion in
  warped compactifications.)
- Kachru, S.; Kallosh, R.; Linde, A.; Trivedi, S.P. (2003). "De
  Sitter vacua in string theory." Phys. Rev. D 68, 046005. (KKLT
  uplift; referenced in §6 as not applicable.)
- Planck Collaboration (2020). "Planck 2018 results. X. Constraints
  on inflation." Astron. Astrophys. 641, A10.
- BICEP/Keck Collaboration (2021). "Improved constraints on
  primordial gravitational waves from BICEP/Keck Array and Planck."
  Phys. Rev. Lett. 127, 151301.

Internal:
- Session 14: radion 1-loop Casimir.
- Session 18: CW+FR 2-modulus potential, Hessian, BF bound.
- Session 31: |C_base| = 0.0065 from Selberg trace; radion mass
  [16, 28] M_poly single-modulus AdS_4.
- Session 33: Paper VI CC audit, M_rad = N/2 assertion.
- Session 34-35: single-modulus σ mass ω = 6.77.
- Session 39: 2-modulus at N=11, masses [56.40, 97.68] M_poly.
- Session 40-43: UV completion audit and scale hierarchy.
- Paper VI §18 radion inflation (lines 1587–1639), §19 DM
  (lines 1643–1700), §cosmology-sector Proposition (line 1061–1077).

---

## 11. Status table

| Claim | Status | Where |
|-------|--------|-------|
| Radion role: spectator (not inflaton, not DM) | DERIVED | §0, §2, §3 |
| Standard slow-roll at σ_infl: n_s = 0.807, r = 0.52 | DERIVED | §2.3 |
| ADM 2008 formula misapplied in Paper VI §18 | DERIVED | §2.2 |
| Linear-potential slow-roll at σ_start: n_s=0.95, r=0.07 | DERIVED | §2.4 |
| N_e = 71.6 from σ_infl to σ_start | DERIVED (quadrature) | §2.4 |
| Radion lifetime τ ∈ [4×10⁻⁹, 9×10⁻⁷] s | DERIVED | §3.2 |
| Reheat temperature T_rh ∈ [0.2, 3] GeV | DERIVED | §3.4 |
| Paper VI Ω_Λ, Ω_b unaffected by radion dynamics | DERIVED | §4.3 |
| T_rh ≤ 3 GeV as smoking gun (no TeV WIMP freeze-out) | DERIVED | §5.1 |
| AdS_4 → Minkowski uplift | OPEN | §6 |
| Tier 4.3B closure | CLOSED | §9 |
