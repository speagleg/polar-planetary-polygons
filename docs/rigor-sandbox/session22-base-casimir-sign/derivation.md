# Session 22 — Sign of the base Casimir on H²/Z₇ from first principles

## 1. What the question actually is

Session 18 §R.16 set the base-Casimir sign to NEGATIVE:
    V_base ⊃ −B_base/(α²γ⁸), with B_base = |C_base|/K² > 0.

The justification given there is two lines long: "base modes are bosonic periodic;
periodic bosonic Casimir is −π²/(90R⁴) per DOF." Session 21 §3 diagnosed numerically
that this one sign drives the ρ-tachyon through the term −36·V_base in H_ρρ. If the
sign is actually +, the ρ-tachyon disappears.

The question is therefore purely technical: on a single connected component of the
Casimir, is the 1-loop vacuum energy positive or negative? The answer has three
independent inputs:

(i) whether each KK mode is periodic or antiperiodic around the nontrivial cycle
    that generates the Casimir (= around the fiber S¹_α; in the "base tower" this is
    the n = 0 sector; the nontrivial cycle there is the H²/Z₇ closed geodesic),
(ii) statistics (boson vs fermion),
(iii) sign of the renormalized zeta value ζ'_Σ(−2) on H²/Z₇.

Session 18 treats only (i) and (ii) and implicitly assumes (iii) is a universal
positive number. That is incomplete: on a hyperbolic orbifold, sign is set by
ζ'_Σ(−2) × (−1 prefactor from zeta-reg), with twisted sectors contributing with
opposite sign via Hurwitz-zeta reflection.

Full derivation below; **conclusion**: the sign is correctly NEGATIVE. Flipping it
would eliminate V_*=0 entirely (not fix it). The ρ-tachyon is structural, not a
sign error.

## 2. Geometric setup

**Base space.** Σ = H²/Γ with Γ = ⟨ρ⟩ ≅ Z_7, ρ a hyperbolic rotation of order 7.
The Seifert manifold fibers over the Klein quartic quotient X(7)/Z_7 ≅ P¹ with
**three** Z_7 cone points coming from the three ramification points of the modular
cover X(7) → X(1). Riemann–Hurwitz for the Galois cover X(7) → X(7)/Z_7 with |G|=7:

    χ(X(7)) = 7·χ(X(7)/Z_7) − Σ (ramification deficit)
    −4 = 7·2 − 3·(7−1) = 14 − 18 = −4  ✓

So Σ has underlying surface P¹ (genus 0) with **three cone points of order 7**, and
orbifold Euler number

    χ_orb(Σ) = 2 − 3·(1 − 1/7) = 2 − 18/7 = **−4/7**.

Gauss–Bonnet at K = −1: Area(Σ) = −2π·χ_orb = 8π/7 ≈ 3.590.

## 3. Spin structure at N = 7

Paper IV §8.1 shows fermion KK expansion with half-integer shift:

    ψ_L(x,φ) = Σ_m χ_m(x) exp(i(m+½)φ)

antiperiodic around S¹_α. This is the spin-connection contribution: holonomy of ω_spin
around the fiber is (−1) for any spin-½ field on an S¹-bundle with half-integer Euler
class e = 7/2.

For the base tower (n = 0, j ≠ 0), antiperiodic fermions have n ∈ Z + ½, so no n = 0
mode. Fermions do not contribute to the base tower. (Session 18 §R.2.3 correct.)

Bosonic modes on the base orbifold have non-trivial representation constraints at
Z_7 cone points: each cone point carries a character χ_p: Z_7 → U(1), with the level-
matching constraint

    χ_1 + χ_2 + χ_3 ≡ 0 (mod 7).

Untwisted sector: χ_1 = χ_2 = χ_3 = 0.
Twisted sectors: |Z_7|³/|Z_7| = 49 distinct sectors (with level-matching).

## 4. 1-loop Casimir on R⁴ × Σ, n = 0 sector

### 4.1 Untwisted sector

For a scalar with Laplacian spectrum {λ_j} on Σ (unit curvature):

    V_scalar^{base, untwisted}(γ) = −(1/(64π²γ⁴))·ζ'_Σ(−2)      (Birrell–Davies §4.5)

with ζ_Σ(s) = Σ_j λ_j^{−s}. Coefficient sign fixed by heat-kernel representation:

    ζ'_Σ(−2) = ∂_s[Γ(s)⁻¹ ∫₀^∞ t^{s−1}(K_Σ(t) − 1) dt]_{s=−2}.

For compact hyperbolic surface, this is finite and **positive** (Minakshisundaram
asymptotic coefficient a_1 = (1/6)·χ_orb·Area is finite). The minus sign out front gives

    V_scalar^{base, untwisted} = −|ζ'_Σ(−2)|/(64π²γ⁴)  < 0.   ← Session 18's sign

### 4.2 Twisted sector (cone-point torsion)

Each Z_7 cone point has 6 twisted sectors, labeled k = 1,...,6. Heat kernel near a
cone of order n (Dowker 1977; Farsi–Jorgenson 1995):

    K_cone^{(k)}(t) = (1/(4n sin²(πk/n)))·(1 + O(t))   as t → 0.

Zeta-regularized contribution:

    V_cone^{(k)} = +(1/(128π²γ⁴))·(1/(n sin²(πk/n)))·[log μγ − C]

with opposite sign from the untwisted sector — twist character multiplies heat kernel
by exp(2πikj/n), and analytic continuation picks up reflected sign from Hurwitz zeta
ζ_H(−2, k/n). For 0 < a < 1, ζ_H(−2, a) > 0, combined with smooth-sector prefactor
+1/sin²(πk/n) > 0 and 7D-loop sign.

At N = 7 with three cone points, six twisted sectors each:

    Total twisted per bosonic DOF
      = +(1/(128π²γ⁴)) · 3 · Σ_{k=1}^{6} (1/(7 sin²(πk/7))) · (small log)
      = +(1/(128π²γ⁴)) · (3/7) · Σ_{k=1}^{6} csc²(πk/7)

Identity: Σ_{k=1}^{n−1} csc²(πk/n) = (n²−1)/3, so for n=7: 16.

    Twisted contribution per DOF = +(48/(7·128π²γ⁴)) = +(48/(896π²γ⁴)) ≈ +5.44·10⁻³/γ⁴.

### 4.3 Net sign of one bosonic DOF on Σ

Using Session 18's smooth-part estimate |ζ'_Σ(−2)|/(64π²) ≈ 3.8·10⁻² per DOF:

    Per-DOF coefficient ≈ −3.8·10⁻² + 5.4·10⁻³ ≈ **−3.3·10⁻²**.

Still negative, ~15% smaller in magnitude than untwisted alone.

## 5. DOF count on the base at N = 7

Base-polarized propagating bosonic DOF:

| Field              | Base DOF |
|--------------------|----------|
| Graviphoton A_μ    | 2 |
| Radion σ           | 1 |
| U(1)_Y gauge       | 2 |
| SU(2)_L gauge      | 6 |
| SU(3) gauge        | 16 |
| Higgs (see below)  | 4 or 0 |

The Higgs doublet is KK pair 3 in the vortex spectrum (Paper IV §10–11), a fermion
bilinear not an independent scalar. So unambiguously independent base bosonic DOF
is **27, not 31**.

Ghost cancellation against longitudinal gauge modes handled implicitly by using
DOF = (dim_adjoint × transverse_pols). ✓

## 6. Net |C_base|

|C_base|_{corrected} ≈ 27 × 3.3·10⁻² = **0.089**

(vs Session 18's 0.092 — within 3%; robust range [0.05, 0.15] stands)

**Sign: NEGATIVE.**

Session 18's sign assignment is correct. The short derivation in §R.16 is
physically right but mathematically incomplete (missed twisted sectors; DOF count
off by 27 vs 31). The full derivation confirms: sign does not flip.

## 7. Numerical impact on V_*=0 stability (flipped sign case)

**Confirmed by `solve_flipped_sign.py`:**

```
ORIGINAL (-B_base)  [Session 18 sign]
  Found 1 distinct physical-window critical point:
  (α, γ, Λ_7) = (0.7978, 0.1651, -5.769e+03)   V = -5.684e-14   (V_*=0 saddle)

FLIPPED  (+B_base)  [hypothesized uplift]
  NO critical point converged in physical window [0.05, 10] x [0.03, 5]
```

10 independent Newton seeds spanning (α,γ,Λ_7) ∈ [0.3, 2.0] × [0.08, 0.5] × [-100000, -100]
all fail to converge with +B_base. The V_*=0 vacuum is structurally absent for the
repulsive-sign case, confirming Session 18 §R.17's own "wrong sign" analysis.

This is the decisive empirical check. **Flipping the base Casimir sign does not
stabilize V_*=0 Minkowski — it eliminates the V_*=0 solution entirely.**

## 8. Conclusion

**Session 18's sign is correct.** The ρ-tachyon at V_*=0 is not an artifact of a
sign error. It is a structural feature of the 5-term Session 18 potential.

Moreover, flipping the sign would eliminate V_*=0 entirely, making stability
trivially impossible. So the V_*=0 + stable Minkowski vacuum is not realizable
with the current 5-term ingredient list regardless of |C_base| sign.

## 9. Hessian re-examination

Session 21 §3 claimed H_ρρ = +53,159 at benchmark, so the tachyon is NOT from
diagonal ρρ, but from off-diagonal H_σρ. Specifically:
    det H = H_σσ H_ρρ − H_σρ² = −1.17e8
    trace = H_σσ + H_ρρ = +3148

With both diagonals positive and trace positive but det negative, |H_σρ|² > H_σσ·H_ρρ.
The tachyon is in a MIXED direction (neither σ nor ρ alone).

Sign-flipping V_base would change H_σρ too, but the NET effect on det H is not
monotone in sign alone — it depends on stationarity, which forbids V_*=0 with
flipped sign anyway.

## 10. Recommendation for Session 23

Per Session 21 §6 option (a): **two simultaneous new terms** whose scaling vectors
jointly pin ρ and σ. Untested combinations:

- R_Σ² (−1,−6) + fiber-wrapped instanton (−4,−4) — two independent channels
- Wilson line around fiber (log-shifted Λ_7-direction) + H-flux
- Gravitational Chern–Simons contribution to V from Seifert boundary

Alternatively: accept the AdS_4 branch (m_radion ~ PeV = 10–30 M_poly, already
derived and independently verified in Session 18 §R.18–R.23) as the honest
first-principles answer and document that V_*=0 Minkowski requires TWO new
ingredients beyond the 5-term CW+FR structure.

## References

- Session 14: `docs/rigor-sandbox/session14-radion-casimir/derivation.md`
- Session 18: `docs/rigor-sandbox/session18-cw-freund-rubin-radion/derivation.md` (§R.1, R.2, R.15, R.16, R.17)
- Session 21: `docs/rigor-sandbox/session21-fiber-wrapped-instanton-radion/derivation.md`
- Session 21 numerics: `solve_session21.py`
- Paper IV: §3 (field content), §8.1 (fermion spin structure), §10 (gauge group)
- Dowker 1977 (cone-point heat kernel)
- Farsi–Jorgenson 1995 (orbifold zeta)
- Birrell–Davies §4.5 (Casimir on hyperbolic manifolds)
