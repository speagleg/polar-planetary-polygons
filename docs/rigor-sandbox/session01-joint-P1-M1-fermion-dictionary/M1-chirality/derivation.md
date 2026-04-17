# M1 — γ⁵ Clifford decomposition on KK modes

**Target claim (Paper IV §8.1 Step 2, lines 975–981 of `latex/paper-4-field-theory/main.tex`)**:

> "γ⁵ = γ⁰γ¹γ²γ³ reduces to γ^(3) · e^{iπm} in the KK basis"

**Finding**: The formula is **imprecise as stated**. Numerically and algebraically, γ⁵ acts as a fixed matrix on KK modes; the scalar fiber wavefunction exp(i(m+1/2)φ) is a c-number that commutes with all γ-matrices. There is no e^{iπm} factor.

The correct statement (which is what the paper needs for its chirality argument) is

> **Theorem (γ⁵ factorization on H² × S¹)**. In the 4D Clifford algebra with signature (+,−,−,−), taking the S¹ coordinate to be x³ = φ (spacelike) and the base M₃ = ℝ × H² to span (x⁰, x¹, x²),
> ```
> γ⁵ ≡ iγ⁰γ¹γ²γ³ = γ^(3) · γ³,
> ```
> where γ^(3) ≡ iγ⁰γ¹γ² is the 3D volume element. γ^(3) commutes with γ^a (a = 0, 1, 2), anticommutes with γ³, and satisfies (γ^(3))² = +1. γ⁵ is a fixed matrix independent of any KK mode index. On a KK-decomposed 4D spinor ψ(x,φ) = Σ_m χ_m(x) · exp(i(m+1/2)φ), the action of γ⁵ is
> ```
> γ⁵ ψ(x,φ) = Σ_m (γ⁵ χ_m(x)) · exp(i(m+1/2)φ),
> ```
> i.e. γ⁵ acts on the 4-component spinor index of χ_m; the 4D chirality eigenvalue of each KK mode equals the 4D chirality of the parent field.

**Proof**: explicit computation in `clifford_oracle.py` (sympy, exact arithmetic). Verified:

1. Clifford algebra `{γ^μ, γ^ν} = 2η^{μν}` and anticommutation `{γ⁵, γ^μ} = 0`, `(γ⁵)² = 1` — all ✓ in the Weyl basis.
2. Commutation structure of γ^(3):
   - `[γ^(3), γ^a] = 0` for a = 0, 1, 2 ✓
   - `{γ^(3), γ³} = 0` ✓
   - `(γ^(3))² = +1` ✓
3. Matrix identity `γ⁵ = γ^(3) · γ³` ✓.
4. KK-mode action: `γ⁵ · (χ · e^{i(m+1/2)φ}) = (γ⁵ χ) · e^{i(m+1/2)φ}`, with NO additional phase. ∎

## Why the paper's "e^{iπm}" formula does not arise from the Clifford algebra

γ⁵ is an operator on the 4-component Dirac spinor index. The KK fiber wavefunction is a c-number on a 1D spatial coordinate. c-numbers commute with the Clifford algebra. Hence γ⁵ cannot act on the KK mode index to produce an m-dependent phase.

The paper's intuition — that L vs R 4D chirality determines which 3D CS sector (A⁺ vs A⁻) the KK modes couple to — is physically sound (see §6 below). But the stated formula is not the mechanism by which this happens.

## KK reduction of the 4D Dirac equation (the correct statement)

Starting from the massless 4D Dirac equation on M₃ × S¹:
```
iγ^μ ∂_μ ψ = 0       (μ = 0, 1, 2, φ)
```

KK-decompose ψ(x, φ) = Σ_m χ_m(x) · exp(i(m+α)φ), where α ∈ {0, 1/2} is the spin-structure shift (α = 1/2 for antiperiodic fermions on S¹, i.e. the genuine spin structure). Substituting and equating Fourier coefficients:
```
iγ^a ∂_a χ_m(x) − (m + α)/R · γ³ χ_m(x) = 0        (a = 0, 1, 2).
```

This is a **3D Dirac equation on M₃ for a 4-component spinor χ_m with γ³ playing the role of a "mass matrix"** and effective mass parameter M_m = (m + α)/R.

### Spectral decomposition via γ^(3)

Since γ^(3) commutes with γ^a (a = 0, 1, 2) and anticommutes with γ³, we can diagonalize γ^(3) without affecting the 3D kinetic term. γ^(3) has eigenvalues ±1, each with multiplicity 2 on the 4-component spinor. Split χ_m into γ^(3)-eigenstates:
```
χ_m = χ_m^{(+)} + χ_m^{(−)},    γ^(3) χ_m^{(±)} = ±χ_m^{(±)}.
```

Since γ³ anticommutes with γ^(3), it swaps the ± sectors. In the (+, −) block basis γ³ takes the form
```
γ³ = ( 0         M
       M'        0 )
```
for some 2×2 blocks M, M' with MM' = (γ³)² |_{+sector} = −1 (spacelike).

The 3D Dirac equation then couples χ_m^{(+)} and χ_m^{(−)}:
```
iγ^a ∂_a χ_m^{(+)}  −  (m+α)/R · M  χ_m^{(−)} = 0,
iγ^a ∂_a χ_m^{(−)}  −  (m+α)/R · M' χ_m^{(+)} = 0.
```

This is a pair of coupled 2-component 3D Dirac equations, equivalent to a single 4-component 3D Dirac equation with a single mass m+α.

### 4D chirality per KK mode

The identity γ⁵ = γ^(3) · γ³ (sympy-verified in `clifford_oracle.py`) is a matrix identity on the 4-component spinor space. Its algebraic properties:

- (γ⁵)² = +1, with eigenvalues ±1 and two-dimensional eigenspaces (the 4D left- and right-handed Weyl components).
- γ^(3) ≡ i γ⁰γ¹γ² commutes with γ^a for a = 0, 1, 2 and anticommutes with γ³; (γ^(3))² = +1.
- γ³ anticommutes with all other γ^μ; (γ³)² = −1 (mostly-plus metric convention used here), so γ³ has eigenvalues ±i.
- (γ⁵)² = γ^(3) γ³ γ^(3) γ³ = −(γ^(3))² (γ³)² = −(+1)(−1) = +1, confirming ±1 eigenvalues despite γ³'s ±i spectrum: the factors γ^(3) and γ³ do not commute, so eigenvalues of the product are not products of eigenvalues.

Physical content: γ⁵ eigenvalues label 4D chirality (±1 = L/R); the factorization γ⁵ = γ^(3)·γ³ says that the 4D chirality operator splits into a 3D volume-form action (γ^(3)) and a fiber-direction action (γ³). Under Witten's CS splitting of 2+1D gravity into SL(2,ℝ)_L × SL(2,ℝ)_R, the γ^(3) eigenvalue identifies which CS sector a given 4D Weyl component couples to. This is preserved per KK mode because γ⁵ acts on the spinor index only, not on the scalar KK wavefunction e^{i(m+1/2)φ}.

## What to write in Paper IV

Replace the current Step 2 passage (lines 975–981):

> "Under KK reduction, γ⁵-eigenvalue maps to the 3D CS sector: 4D left-handed ↔ couples to A⁺ (the dreibein component along S¹ determines the chirality projection, because γ³ = γ^φ is the fiber direction, and γ⁵ = γ⁰γ¹γ²γ³ reduces to γ^(3) · e^{iπm} in the KK basis)."

with (proposed language — Gordon approves final):

> "Under KK reduction, γ⁵-eigenvalue is preserved per KK mode: 4D Weyl fermion ψ with γ⁵ψ = ±ψ decomposes as ψ = Σ_m χ_m(x) e^{i(m+1/2)φ} with γ⁵ χ_m = ±χ_m for every m. The identity γ⁵ = γ^(3) · γ³, where γ^(3) ≡ iγ⁰γ¹γ² is the 3D volume element (commutes with γ^a for a = 0, 1, 2; anticommutes with γ³ = γ^φ), identifies the sign-of-γ⁵ sector with the sign-of-γ^(3) sector on the γ³-eigenbasis. In the Witten CS splitting [A^+, A^-] of 2+1D gravity, γ^(3)-eigenstates couple to A^+ and A^- respectively: the 4D left-chiral sector (γ⁵ = +1) and right-chiral sector (γ⁵ = -1) map one-to-one onto the A^+ and A^- CS sectors."

This (a) states a true mathematical identity, (b) captures the physics of chirality-to-sector matching, and (c) avoids the unjustified e^{iπm} factor.

## Implications for P1 (KK-mode → fermion dictionary)

**Key output**: For each 4D Dirac KK mode χ_{m_7, m_4}, the 4 complex components decompose as:
- 2 components with γ⁵ = +1 (4D right-handed Weyl χ_R)
- 2 components with γ⁵ = −1 (4D left-handed Weyl χ_L)

A 4D Dirac KK mode therefore gives 2 Weyl fermions in 4D: one L, one R. Both have the same (m_7, m_4) labels but opposite 4D chirality.

The 3D dynamics per KK mode is governed by the 3D Dirac equation (iγ^a ∂_a − M_m γ³), with M_m = (m+α)/R. The Redlich-parity-anomaly argument (§8.1 Step 3) selects one CS sector (A⁺) to survive at low energy; this breaks 4D parity by projecting out half the Weyl content of each KK mode.

**Counting chain for P1** (resolved in PAPER4_REVISION_DRAFT.md):
- 28 KK mode pairs (m_7, m_4) × 2 chiralities (L, R) × 2-component Weyl = 112 real dof per fixed cusp
- After the Redlich projection (A⁻ sector gapped at m_R ~ 107 TeV), only the A⁺ sector (χ = L) survives at E ≪ M_poly: **28 complex Weyl components per cusp**.
- After Legendre projection (Lemma lem:legendre): 16 complex Weyl survive per cusp.
- Across three Z/7-fixed cusps on X(7) (Theorem thm:three-gens, DHVW twisted-sector construction): 3 × 16 = **48 Weyl per 3 generations = 16 per generation**, matching SM + ν_R.

The full chain 56 → 28 → 16 → 48 is documented in PAPER4_REVISION_DRAFT.md; M1 handles the first arrow (the γ⁵ projection).

## Status

**M1 derivation**: ✓ complete
- Clifford identity `γ⁵ = γ^(3) · γ³` derived
- Paper's e^{iπm} claim shown to be imprecise
- KK-mode chirality structure rigorously established
- Proposed replacement language for Paper IV §8.1 Step 2
- Counting chain closed via Legendre + 3-cusp multiplier (see PAPER4_REVISION_DRAFT.md).

## Next steps

- M1 ready for reviewer cycle.
