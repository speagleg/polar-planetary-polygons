# Palindromic Census of Arithmetic Fuchsian Groups

**Date:** 2026-03-20
**Status:** VERIFIED COMPUTATION, integrated into Paper I

## Key Result

**Non-solvable palindromic polynomials exist and provide concrete test cases for the Langlands programme.**

For arithmetic Fuchsian groups with trace field degree d ≥ 5, the palindromic polynomial Q(ξ) = ξ^d P(ξ + 1/ξ) generically has non-solvable Galois group (S_d for d ≥ 5). Each such polynomial gives a concrete instance where:
1. Vortex physics predicts a specific numerical stability threshold
2. The palindromic polynomial has a specific non-solvable Galois group
3. Langlands reciprocity predicts an automorphic form on GL(n)/Q
4. But the automorphic form's existence is CONJECTURAL (not proved)

## Three Explicit Non-Solvable Palindromic Polynomials

### 1. disc = 38569 (S_5)
- Trace field polynomial: P(u) = u⁵ - 5u³ + 4u - 1
- Palindromic: Q(ξ) = ξ¹⁰ - ξ⁶ - ξ⁵ - ξ⁴ + 1
- Coefficients: [1, 0, 0, 0, -1, -1, -1, 0, 0, 0, 1]
- Threshold: ξ* ≈ 0.8221

### 2. disc = 65657 (S_5)
- Trace field polynomial: P(u) = u⁵ - u⁴ - 5u³ + 4u² + 5u - 3
- Palindromic: Q(ξ) = ξ¹⁰ - ξ⁹ - ξ⁵ - ξ + 1
- Coefficients: [1, -1, 0, 0, 0, -1, 0, 0, 0, -1, 1]
- Threshold: ξ* ≈ 0.7478

### 3. disc = 24217 (S_5)
- Trace field polynomial: P(u) = u⁵ - 5u³ - u² + 3u + 1
- Palindromic: Q(ξ) = ξ¹⁰ - ξ⁷ - 2ξ⁶ - ξ⁵ - 2ξ⁴ - ξ³ + 1
- Coefficients: [1, 0, 0, -1, -2, -1, -2, -1, 0, 0, 1]
- Threshold: ξ* ≈ 0.6606

## Galois Group Classification

Verified by Chebotarev density theorem (mod-p factorization patterns for p < 500):

| Degree d | Group | Solvable | # in census |
|----------|-------|----------|-------------|
| 1 | trivial | Yes | 1 |
| 2 | C_2 | Yes | 5 |
| 3 | C_3, S_3 | Yes | 3 |
| 4 | V_4, D_4, S_4 | Yes | 3 |
| 5 | C_5 | Yes | 1 |
| 5 | D_5 | Yes | 1 |
| 5 | **S_5** | **No** | **3** |
| 6 | C_6 | Yes | 1 |

## Langlands Connection

For S_5 palindromic polynomials:
- The 4-dimensional standard representation of S_5 restricts to a faithful representation of A_5 ≅ PSL(2, F_5)
- Langlands predicts: L(s, std) = L(s, π) for some automorphic π on GL(4)/Q
- Status: **CONJECTURAL** — the A_5 composition factor is the original Langlands obstruction
- Partial progress: Buzzard-Dickinson-Shepherd-Barron-Taylor (2001) for dim 2; dim 4 is OPEN

## Voight Census Extrapolation

Among ~25,000 arithmetic Fuchsian groups (Voight 2021):
- Degree 1-4: ~16,000 groups, all solvable
- Degree ≥ 5: ~9,000 groups, generically S_d (non-solvable)
- Estimated ~7,000 Langlands test cases
- By Bhargava's density results (2010): fraction with S_d → 1 as disc → ∞

## What Is Proven vs Conjectural

| Claim | Status |
|-------|--------|
| Palindromic construction (Prop 6.5) | PROVEN |
| Three S_5 polynomials are palindromic | VERIFIED (47 tests pass) |
| Galois group = S_5 | VERIFIED (Chebotarev, 500 primes) |
| Arithmetic Fuchsian groups exist with these trace fields | PROVEN (Voight, Theorem 14.6.1) |
| Langlands reciprocity for solvable case | PROVEN (Langlands-Tunnell et al.) |
| Langlands reciprocity for S_5 case | CONJECTURAL |
| ~7,000 test cases in Voight census | ESTIMATE (Bhargava density) |

## Code

- Module: `src/planetary_polygons/extensions/palindromic_census.py`
- Tests: `tests/test_palindromic_census.py` (47 tests)
- Paper: `latex/paper-1-mathematics/main.tex`, §A.8 (Prop A.8 + Remark A.9)
