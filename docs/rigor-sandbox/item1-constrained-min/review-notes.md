# Item #1 — Review Log

## Round 1 — 2026-04-14

**Score: 8.0 / 10**
**Structural deductions: 5** (gate fails — need zero)
**Stylistic deductions: 7**

### Structural

1. **m = N/2 case dismissed by "continuity"** (invalid for integer parameter). Need explicit parallel computation showing ||e_r||² = N (not N/2) at m=N/2, and that the factor-of-2 difference in the norm is compensated by factor-of-2 in each elementary sum.
2. **Only cosine sub-mode computed.** For each m, the real Z_N isotypic component is 4-dim (cos·r, sin·r, cos·t, sin·t). Need a Lemma using SO(2) rotational invariance to show the 4×4 block decomposes as two identical 2×2 blocks.
3. **Havelock/Dirichlet identity (Lemma 1) cited, not proved.** Need the 8-line inline proof via `|Σ_{k=0}^{m-1} e^{i(2k+1-m)πp/N}|² = sin²(πmp/N)/sin²(πp/N)` and interchange-of-summations.
4. **Cosecant-squared sum (Lemma 2) cited, not proved.** Derive inline or as a corollary of Lemma 1.
5. **Z_N equivariance of perturbation parametrization asserted, not verified.** 2-sentence explicit statement that the local (radial, tangential) frame transforms covariantly under the cyclic permutation.

### Stylistic

1. Trace lemma (Lemma 4) forward-references eq (25). Move after §6 or cite directly.
2. "Factor of 2 converting Σ_{j<k} to Σ_{j≠k} cancels half of it" — explanatory clause obscures more than clarifies.
3. Symbol `L` overloaded (Lagrangian vs. linear coefficient in §4). Rename one.
4. "By continuity" for integer argument (also flagged structurally in #1).
5. Lemma 5 cross-product chain benefits from intermediate line: `PR = 4(α_j²-α_k²)(1-cos)(sin)`, then apply `1-cos = U/2`.
6. Numerical verification language: foreground 30-digit symbolic as primary; 10⁻² finite-difference as sanity check.
7. Verify `\ref{lem:offdiag}` resolves correctly in compiled output.

### Summary

"All five structural deductions concern completeness of the in-document proof, not correctness. All are short fixes (a paragraph each, plus inline proofs of the two lemmas). With those addressed, the derivation would meet the ≥9.0 threshold cleanly."

### Resolution plan

Apply all 5 structural fixes + 5 stylistic (1, 2, 3, 5, 6). Stylistic 4 duplicates structural 1. Stylistic 7 is already correct (verified by `pdflatex` cross-refs with zero warnings).
