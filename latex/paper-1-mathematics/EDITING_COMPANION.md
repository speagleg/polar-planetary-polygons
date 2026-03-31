# Paper I Editing Companion — Content Index & Assessment

## Summary
~3450 lines (after constrained-minimum theorem insertion). 7 sections + bibliography.
Core math in Sections 1–5. Supplemental/physics in Section 6 (B2) and Section 7 (K-theory).

**UPDATE 2026-03-31:** Theorem 2.2 (Constrained energy minimum) + proof + Remark inserted
at lines 425–487, replacing the old Remark 2.7 that deferred to Paper II. Paper I is now
self-contained on its central stability claim. Line numbers below Sec 2 are shifted ~45 lines.

---

## SECTION-BY-SECTION INDEX

### Abstract (lines 16–28) — CORE
States: decomposition, sign rule, Riemannian extension, algebraic-integer classification, geodesic correspondence.
**Issues:** Doesn't state the main theorem explicitly. Second sentence is 63 words.

### Section 1: Introduction (lines 31–132) — CORE
- Lines 34–45: Central decomposition equation
- Lines 47–68: Six routes enumerated
- Lines 71–114: "What this paper proves" (5 items)
- Lines 117–126: Structure paragraph
- **Issue line 49:** "fully revealed" — grammatically malformed, typo "distnct" on line 50

### Section 2: Logarithmic interaction (lines 134–432) — CORE
All standalone mathematics. No physics dependencies.

| Lines | Content | Assessment |
|-------|---------|------------|
| 141–172 | **Remark 2.1**: Cauchy functional equation, dilation invariance | CORE (1st of 3 statements of Cauchy) |
| 175–207 | **Prop 2.1**: Scale classification (RG analogy) | CORE |
| 209–219 | Blob bridge mention, **Paper II reference** | SUPPLEMENTAL — line 218 refs Paper II |
| 221–287 | **Prop 2.2**: Isotropic marginality at α=2 | CORE — clean 4-step proof |
| 289–328 | **Remark 2.4**: RG vs stability table | CORE |
| 330–343 | Validity of first-order theory | CORE |
| 345–353 | Curvature dichotomy preview | REDUNDANT — stated formally as Prop 5.5 (line 2160) |
| 354–409 | **Prop 2.3**: Möbius covariance + **Cor 2.4**: Dilation subgroup | CORE |
| 411–423 | **Remark**: Loxodromic thread | CORE (synthesis) |
| 425–487 | **Theorem 2.2**: Constrained energy minimum (N<=7 is minimum on L=const surface) + proof + Remark | CORE — **FIXED**: now self-contained, no longer defers to Paper II |

### Section 3: Sign rule (lines 437–562) — CORE
Entirely standalone. The best-written section per reviewer.

| Lines | Content | Assessment |
|-------|---------|------------|
| 440–533 | **Theorem 3.1**: Sign rule + 5-step proof | CORE — self-contained |
| 535–562 | **Remark 3.1**: Borderline status, 3 classes | CORE |

### Section 4: Havelock identity & metric-independence (lines 565–887) — CORE (mostly)

| Lines | Content | Assessment |
|-------|---------|------------|
| 571–598 | **Lemma 3.1**: Classical Havelock identity | CORE — "model proof" |
| 600–618 | **Remark**: CMS integrable systems interpretation | CORE (math context) |
| 623–657 | **Theorem 3.2**: Riemannian Havelock | CORE — central result |
| 658–818 | Proof (Steps 1–3, product formula) | CORE |
| 819–821 | **Remark**: Compact quotients | CORE — but 90-word sentence needs breaking |
| 832–866 | **Remark 3.5**: Rep-theoretic content | CORE items 1-2; item 3 (line 862) refs Paper II for α₀ = SUPPLEMENTAL |
| 867–887 | Geometric origin of C₁=N-1 | REDUNDANT — Cauchy eq stated for 3rd time |

### Section 5: Stability thresholds on constant-curvature surfaces (lines 890–2470) — CORE + PHYSICS DIGRESSIONS

| Lines | Content | Assessment |
|-------|---------|------------|
| 894–911 | Prior work paragraph | CORE — but line 907 dismissive tone |
| 913–968 | **§5.1**: Spherical stability boundary | CORE math |
| 955–967 | Saturn/Jupiter illustration | **PHYSICS — REMOVE** (refs Paper V which doesn't exist) |
| 969–1101 | Derivation of C₁(S²), exact thresholds, staircase | CORE |
| 1032–1050 | **Remark**: Pattern break at N=6 | CORE |
| 1052–1101 | **Remark**: Stability staircase, counting function | CORE math |
| 1111–1370 | **§5.2**: Hyperbolic plane, C₁(H²) derivation | CORE — central result |
| 1134–1145 | **Remark**: Order of curvature correction | CORE |
| 1200–1268 | Proof of C₁(H²) formula | CORE |
| 1279–1306 | **Prop 5.3**: Monotonicity of N_crit | CORE |
| 1308–1370 | Near-K=0, ξ*=8-3√7, Pell unit interpretation | CORE — most memorable result |
| 1372–1473 | **§5.3**: Algebraic structure, palindromic quadratic, field pattern | CORE |
| 1475–1543 | **Prop 5.1**: Algebraic-integer classification | CORE |
| 1544–1558 | Golden ratio terminal case | CORE |
| 1560–1567 | Binary subdivision | CORE |
| 1569–1606 | **Prop 5.2**: CF of palindromic units | CORE |
| 1608–1622 | Regulator as physical accessibility | CORE (pure math, despite "physical" in name) |
| 1624–1699 | Growth law f_crit - b ~ N²/24, proof of b(N) identity | CORE |
| 1700–1722 | **Remark**: Bernoulli-Dedekind connection | CORE (number theory) |
| 1724–1751 | **Prop 5.4**: Galois group = conformal inversion | CORE |
| 1753–1845 | Geodesic structural observation + proof | CORE — but line 1844 is 72-word sentence |
| 1847–1886 | **Remarks**: Automorphic correction, conductor sensitivity | CORE |
| 1888–1936 | Higher-genus generalization + Bolza conjecture | CORE |
| 1938–2084 | **Prop 5.5**: Legendre selection rule + **Cor**: fully visible primes | CORE (deep number theory) |
| 2086–2128 | **Theorem 5.12**: Universality of N_crit=7 | CORE — "short, elegant" |
| 2130–2144 | **Remark**: Topology as curvature correction | CORE |
| 2146–2158 | Curvature dichotomy re-statement | **REDUNDANT** — 3rd time (lines 345, 1123, 2160) |
| 2160–2213 | **Prop 5.5**: Curvature-stability dichotomy + **Prop 5.6**: Morse index | CORE |
| 2215–2224 | **Cor**: Why N_crit=7 | CORE |
| 2226–2264 | Spectral flow monotonicity + **Remark**: Robustness | CORE |
| 2267–2297 | **Theorem**: Index pairing (K₀) | CORE (K-theory light) |
| 2299–2327 | IQHE staircase analogy table | **SUPPLEMENTAL** — analogy only, no theorem |
| 2329–2363 | **Theorem**: Algebraic origin of N_crit=7 | CORE — clean factorization proof |
| 2365–2437 | **Physical realization** (hyperbolic lattices) | **PHYSICS — REMOVE or RELOCATE** |
| 2441–2470 | **Open problems** | **RELOCATE** to end of paper |

### Section 6: The B₂ organising principle (lines 2473–2627) — SUPPLEMENTAL
No new theorems. Self-described: "we make no new claims here" (line 2531).

| Lines | Content | Assessment |
|-------|---------|------------|
| 2473–2521 | B₂ = 1/6 organizing principle, stability polynomial | SUPPLEMENTAL — interesting but no theorem |
| 2523–2592 | csc² kernel in 7 contexts (CMS, Dyson, HS, Laughlin, Selberg, W_N, AGT) | **SUPPLEMENTAL** — catalogue, no new result |
| 2593–2609 | B₂ loop through index theorem | SUPPLEMENTAL — refs Paper III |
| 2610–2627 | 4/3 self-interaction identity | **SUPPLEMENTAL** — refs Paper III |

### Section 7: K-theoretic classification (lines 2629–3397) — SUPPLEMENTAL (advanced)
Contains real theorems but is a different paper's worth of machinery.

| Lines | Content | Assessment |
|-------|---------|------------|
| 2633–2669 | Three-stage overview | CORE framing |
| 2671–2700 | **§7.1**: Elementary invariant | CORE (but elementary, as noted) |
| 2701–2892 | **§7.2**: Index pairing via Selberg trace formula | ADVANCED CORE — real theorem |
| 2893–2903 | Bolza verification | CORE |
| 2904–2981 | **§7.3**: Spectral flow stability | CORE — proves spectral flow = Morse index on quotients |
| 2982–3166 | **§7.4**: Kasparov product | ADVANCED — one numerical result (Bolza 0.644) |
| 3168–3365 | Bolza computation details, convergence analysis | ADVANCED — could be appendix |
| 3367–3385 | **Remark**: Topological phases | SUPPLEMENTAL (IQHE parallel) |
| 3387–3397 | Number-theoretic extensions teaser | **REMOVE** — dangling ref to Supplement A |

---

## REDUNDANCY MAP

| Content | Occurrences | Keep | Remove |
|---------|-------------|------|--------|
| Cauchy functional equation | Lines 152, 548, 882 | Line 152 (first) | Lines 548 (brief), 882 (full re-derive) |
| Curvature-stability dichotomy | Lines 345, 1123 table, 2146, 2160 | Line 2160 (formal Prop) + 1123 (table) | Lines 345 (preview), 2146 (re-statement) |
| Dilation invariance → N_crit=7 | Lines 161-171, 385-408, 867-887 | Remark 2.1 + Cor 2.4 | Lines 867-887 |
| Scale independence | Many | Once in Remark 2.1 | Elsewhere |

---

## CROSS-REFERENCE PROBLEMS

| Line | Reference | Problem |
|------|-----------|---------|
| 218 | Paper II (blob bridge, K₀ interaction) | Forward ref to concepts not in this paper |
| ~431 | Paper II (quartic normal form refinement) | OK — Paper I now proves the linear result; Paper II refines at quartic order |
| 862 | Paper II (quartic α₀) | Forward ref |
| 958 | Paper V | **BROKEN**: Paper V doesn't exist |
| 2437 | Paper II (BEC predictions) | Forward ref |
| 2457 | Paper IV (Saturn) | Forward ref to wrong paper? Should be Paper II |
| 2602 | Paper III, Prop (Riemann-Roch) | Forward ref |
| 2615 | Paper III, Step 4 | Forward ref |
| 3391-3397 | Supplement A | Dangling teaser |

---

## SENTENCE LENGTH VIOLATIONS (>40 words)

| Line | ~Words | Severity |
|------|--------|----------|
| 148-154 | 72 | REWRITE |
| 155-160 | 62 | REWRITE |
| 161-167 | 58 | IMPROVE |
| 776-777 | 65 | REWRITE (inline equation) |
| 820 | 90 | REWRITE (single remark sentence) |
| 1340-1344 | 50 | IMPROVE |
| 1356-1361 | 55 | IMPROVE |
| 1844 | 72 | REWRITE (proof step) |
| 2253-2258 | 52 | IMPROVE |
| 2985 | 55 | REWRITE |

---

## NOTATION ISSUES

| Symbol | Meanings | Collision severity |
|--------|----------|-------------------|
| ξ | tan²(φ₀/2) on S², r_E²/a² on H² | Medium — different surfaces |
| γ | Group element (§7), curvature coeff (line 1336), geodesic separation (line 972) | HIGH |
| c | Casimir ratio (line 1197), SL(2,Z) trace (line 1799), Laplacian constant | HIGH |
| C₁ | C₁(surface), C₁(ξ), C₁(H²,ξ) — varying argument lists | LOW |

---

## RECOMMENDED ACTIONS (by priority)

### Must fix before submission
1. **Line 49**: Fix "fully revealed" and "distnct" typo
2. ~~**Line 431**: Either prove constrained minimum here or clearly state as assumption~~ **DONE** — Theorem 2.2 inserted
3. **Line 958**: Fix "Paper V" → "Paper II"
4. **Line 2457**: Fix "Paper IV" → "Paper II"
5. **Break monster sentences**: Lines 820, 776, 1844, 148-160

### Should fix (structural)
6. **Remove physics digressions**: Lines 955-967 (Saturn/Jupiter), 2365-2437 (experiments)
7. **Remove redundancy**: Lines 345-353, 867-887, 2146-2158
8. **Move open problems** (lines 2441-2470) to end
9. **Remove Section 6** or reduce to a single remark
10. **Remove lines 3387-3397** (dangling Supplement A teaser)

### Consider (optional)
11. Rename γ (curvature coeff) to avoid collision with Fuchsian group element
12. Add ξ-definition note at start of Section 5
13. Consolidate code references into one "Code availability" note
14. Shorten Section 7 K-theory or split to separate paper/appendix
