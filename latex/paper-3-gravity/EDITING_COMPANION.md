# Paper III Editing Companion -- Content Index & Assessment

**File:** `latex/paper-3-gravity/main.tex`
**Total lines:** 3110
**Sections:** 11 (plus introduction)
**Formal statements:** 18 theorems/propositions/lemmas/corollaries

---

## Summary

Paper III ("Gravitational Theory") argues that the Havelock eigenvalue structure, combined with the Onsager selection principle at negative temperature, implies the vacuum Einstein equations in 2+1D. Threads through CMS--CS Casimir, holography, BTZ transition, WDW equation, higher-dimensional extension, and Theorem 6.1 (polygon entropy maximisation implies constant curvature).

**Strengths:** Argument arc is clear. Front-loads the graviton-at-N=7 payoff. Theorem 6.1 proof is thorough. C_1 notation clarification (line 1187) well placed.

**Weaknesses:** Theorem 6.1 proof is 596 lines with digressions (Szego--Toeplitz, shell dominance). Several passages repeat earlier content. BTZ section packs 7 topics without subsection headings.

---

## SECTION-BY-SECTION INDEX

### Abstract (lines 14--30) -- CORE
Good length. "Supporting infrastructure" is vague.

### Section 1: Introduction and summary (lines 33--83) -- CORE
Clean roadmap. Falsifiability claim (lines 72--83) is strong.

### Section 2: Graviton at N=7 and CS lift (lines 85--368)

| Lines | Content | Assessment | Notes |
|-------|---------|------------|-------|
| 105--160 | Prop 2.1 (CMS--CS Casimir identification) | CORE | Central result |
| 162--208 | Remark (Why CMS and CS share sl(2,R)) | CORE | Well organized |
| 242--276 | Prop 2.2 (Graviton identification) | CORE | Elegant Pell argument |
| 278--298 | Remark (Physical content) | SUPPLEMENTAL | Could shorten |
| 300--368 | CS lift paragraph | CORE | Lines 362--368 orphaned parenthetical |

### Section 3: Spectral bound (lines 370--519)

| Lines | Content | Assessment | Notes |
|-------|---------|------------|-------|
| 421--458 | Spectral computation of delta C_1 | CORE | Concrete numerical bound |
| 473--519 | Selberg dictionary table | SUPPLEMENTAL | Post-table paragraphs repeat table |

### Section 4: Holographic interpretation (lines 521--729)

| Lines | Content | Assessment | Notes |
|-------|---------|------------|-------|
| 563--596 | Prop 4.1 (Havelock = one-chiral OPE Casimir) | CORE | |
| 682--694 | Confining potential from OPE kernel | SUPPLEMENTAL | Two derivations "mathematically identical" |
| 696--729 | Conformal bootstrap | SUPPLEMENTAL | Concluding paragraph speculative |

### Section 5: OPE identification (lines 731--921)

| Lines | Content | Assessment | Notes |
|-------|---------|------------|-------|
| 782--891 | Thm 5.1 (Z_N conformal block = Havelock) | CORE | Identity block dominance long but necessary |
| 905--921 | Quantum correction | CORE | Compact |

### Section 6: BTZ transition (lines 924--1168)

| Lines | Content | Assessment | Notes |
|-------|---------|------------|-------|
| 924--1013 | Core BTZ: actions, temperature, negative mode, phase diagram | CORE | |
| 1015--1040 | Critical exponent | SUPPLEMENTAL | Dense |
| 1055--1086 | Microscopic entropy accounting | SUPPLEMENTAL | Could appendicize |
| 1088--1114 | One-loop correction | SUPPLEMENTAL | Bolza/Haldane digression |
| 1115--1168 | Lorentzian continuation | SUPPLEMENTAL | van Hove/Tracy-Widom feels detached |

**Needs subsection headings for 7 disparate topics.**

### Section 7: Wheeler--DeWitt equation (lines 1172--1361)

| Lines | Content | Assessment | Notes |
|-------|---------|------------|-------|
| 1187--1204 | C_1 notation clarification | CORE | Essential, well placed |
| 1257--1263 | Four-role consistency | REDUNDANT | Restates intro (lines 72--83) |
| 1313--1344 | Prop 7.1 (Eigenvalue non-crossing) | CORE | |

### Section 8: Three-layer decomposition (lines 1365--1601)

| Lines | Content | Assessment | Notes |
|-------|---------|------------|-------|
| 1365--1441 | Props 8.1--8.2 (Orbifold--Havelock, Todd class) | CORE | |
| 1453--1470 | delta_m=0 clarification | CORE | But stated twice (also line 1184) |
| 1523--1555 | Three-layer equation restated | REDUNDANT | 3rd time for this equation |
| 1557--1601 | Weyl norm, mergers, RG flow | SUPPLEMENTAL | 5 topics in 44 lines, unfocused |

### Section 9: Higher-dimensional extension (lines 1605--1817)

| Lines | Content | Assessment | Notes |
|-------|---------|------------|-------|
| 1669--1695 | Prop 9.1 (Soft Havelock in dim d) | CORE | |
| 1756--1805 | Thm 9.1 (RG monotonicity of Casimir ratio) | CORE | Careful proof |
| 1730--1754 | Transcendence remark + pentagon golden ratio | SUPPLEMENTAL | |

### Section 10: Triangle universality (lines 1820--1880)

| Lines | Content | Assessment | Notes |
|-------|---------|------------|-------|
| 1820--1865 | Thm 10.1 (Triangle universal stability) | CORE | Three independent arguments |
| 1867--1880 | Dynamical triangulation remark | SUPPLEMENTAL | Appropriately hedged |

### Section 11: Partition function (lines 1884--1948)

| Lines | Content | Assessment | Notes |
|-------|---------|------------|-------|
| 1884--1936 | Prop 11.1 + trace field table | CORE | |
| 1938--1948 | Baum-Connes paragraph | SUPPLEMENTAL | Dense; mystifying for gravity readers |

### Section 12: Einstein equations (lines 1951--3107) -- CENTRAL (37% of paper)

| Lines | Content | Assessment | Notes |
|-------|---------|------------|-------|
| 1954--1956 | Duplicated sentence | **BUG** | See R5 |
| 1986--2033 | Thm 12.1 (Central theorem) | CORE | Statement clear |
| 2044--2125 | Cor 12.1 (Onsager contraction) | CORE | |
| 2127--2188 | Proof Steps 1--2 | CORE | |
| 2190--2265 | Proof Step 3 (Jensen + Onsager) | CORE | |
| 2216--2242 | Embedded paragraph | REDUNDANT | Restates Step 3 |
| 2271--2411 | Regge calculus extension | CORE | |
| 2413--2601 | Szego--Toeplitz analysis (188 lines) | SUPPLEMENTAL | "may be skipped" -- appendicize |
| 2604--2657 | Partition fn + explicit dS/dg | CORE | |
| 2659--2723 | Step 4: Higher dimensions | CORE | |
| 2766--2816 | Prop 12.1 (Lambda from WDW) | CORE | |
| 2818--2828 | Cor 12.2 (Sign of Lambda) | CORE | |
| 2896--2923 | Raychaudhuri analogy | SUPPLEMENTAL | Non-rigorous |
| 2942--3089 | Clausius, Cardy, RT, partition fn verification | CORE | |
| 3102--3107 | Closing paragraph | SUPPLEMENTAL | Poetic but vague |

---

## REDUNDANCY MAP

| ID | Content | Appearances | Recommendation |
|----|---------|-------------|----------------|
| R1 | Four-role consistency of c=12b(N) | Lines 72--83, 1257--1263, 1489--1497 | Keep intro; one-sentence ref elsewhere |
| R2 | Three-layer equation | Lines 46, 1210, eq 20, eq 22, 2805 | Keep Prop 8.2; ref elsewhere |
| R3 | delta_m=0 on constant curvature | Lines 1184, 1453--1470, 1460 | Consolidate to one location |
| R4 | Bolza bound delta_C_1 <= 0.020 | Lines 444, 1097, 1465 | State once; cite by eqn number |
| R5 | Duplicated sentence (lines 1954--56) | Internal duplication | **Delete duplicate** |
| R6 | "may be skipped" (line 2421) | Duplicated within same parenthetical | Keep one |

---

## CROSS-REFERENCE PROBLEMS

### External refs to other papers

| Line | Target | Risk |
|------|--------|------|
| 45 | Paper II prop | OK |
| 151 | Paper I lemma | OK |
| 293 | Paper IV theorem | Distant; reader must trust |
| 313 | "Paper I, section 5" | **Hardcoded** -- use label |
| 685 | "Paper I, section 4" | **Hardcoded** -- use label |
| 822 | "Paper I, section 3" | **Hardcoded** -- use label |

### Self-reference bug
- **Line 2225**: "Paper~III" referring to itself. Change to "this paper" or just the section ref.

### Label problems
- **Line 2128**: `sec:einstein-derivation` on `\begin{proof}`, not a section
- **Line 2217**: `sec:vortex-gravity` dead label, never referenced
- **Line 2422**: `rem:szego-toeplitz` on paragraph, not a remark environment

---

## SENTENCE LENGTH VIOLATIONS (>40 words)

| Line | ~Words | Opening text |
|------|--------|-------------|
| 15--27 | ~65 | Abstract single sentence with H1/H2/H3 |
| 42--51 | ~55 | "The starting point is the observation..." |
| 96--103 | ~50 | "We now prove that the quadratic Casimir..." |
| 291--298 | ~55 | "In 2+1D, the boundary theory..." |
| 310--314 | ~60 | Parenthetical with b(N) formula |
| 326--332 | ~55 | CS partition function decomposition |
| 1319--1321 | ~55 | Central charge bound |
| 1381--1390 | ~60 | Matching uses c_orb |
| 1938--1948 | ~65 | Baum-Connes assembly map |
| 2340--2354 | ~65 | Regge Hamiltonian self-referential |
| 2370--2379 | ~60 | Uniform convergence conditions |
| 2462--2471 | ~55 | Wiener-Hopf condition |

---

## NOTATION ISSUES

| Symbol | Meanings | Severity |
|--------|----------|----------|
| C_1 | (1) C_1^GF(rho) = log(2sinh rho) + b(N); (2) C_1(xi) = (N-1)(1+xi^2)/(1-xi)^2 | **HIGH** -- GF superscript used only at lines 1188, 1202 |
| b | (1) b(N) = N(N+1)/12 - ln2 + ...; (2) b = -1/4 Weyl coefficient | Medium |
| sigma | 5 different meanings across paper | Medium |
| R | Scalar curvature, recursion operator, representation, R^2 stat | Low (standard) |
| f(m,N) vs f_m vs T_m | Related but inconsistent shorthand | Low -- state convention once |

---

## RECOMMENDED ACTIONS (by priority)

### Must fix
1. **R5**: Delete duplicated sentence at lines 1954--1956
2. **Line 2225**: Self-reference bug ("Paper III" referring to itself)
3. **Line 2128**: Label on proof block, not section
4. **Line 2217**: Dead label
5. **Line 2422**: Label on non-remark

### Should fix
6. **R1**: Four-role consistency -- one sentence ref, not restatement
7. **R4**: Bolza bound -- state once, cross-reference
8. **N1**: C_1^GF superscript -- apply consistently
9. **N2**: b = -1/4 Weyl -- rename to avoid b(N) collision
10. **Hardcoded section numbers** (lines 313, 685, 822) -- use labels
11. **BTZ section**: Add subsection dividers
12. **R6**: Duplicated "may be skipped"
13. **Lines 362--368**: Orphaned parenthetical
14. **Szego--Toeplitz** (lines 2413--2601): Move to appendix

### Consider
15. Abstract: expand H1/H2/H3 descriptions
16. Split Theorem 6.1 proof into proof + extension subsection
17. R2: Three-layer equation stated 4x -- keep one, ref elsewhere
18. N5: Distinguish sigma meanings in proof of Thm 6.1
19. Lines 3102--3107: Replace poetic closing with result restatement
20. Lines 2896--2923: Raychaudhuri analogy to footnote
21. Lines 1557--1601: 5 topics in 44 lines -- develop or appendicize
