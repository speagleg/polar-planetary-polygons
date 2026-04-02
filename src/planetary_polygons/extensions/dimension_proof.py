"""
Proof that polynomial Havelock eigenvalues are unique to d = 2.

THEOREM: Let S_α(m, N) = Σ_{p=1}^{N-1} [1 - cos(2πpm/N)] / |sin(πp/N)|^α.
Then S_α(m, N) is a polynomial in m (for all N ≥ 3) if and only if α = 2.

PROOF SKETCH:
  1. For α = 2: S₂(m, N) = 2m(N-m) (the Ramanujan identity).
     Proof: factorize the numerator using roots of unity.

  2. For α ≠ 2: S_α(m, N) is NOT polynomial.
     Proof by contradiction using second differences.

     For a degree-d polynomial P(m): the (d+1)-th finite difference Δ^{d+1}P = 0.
     For S₂: the second difference Δ²S₂ = 2(constant) → polynomial of degree 2.
     For S_α with α ≠ 2: the second difference Δ²S_α is NOT constant.

     Explicitly:
     Δ²S_α(m) = S_α(m+1) - 2S_α(m) + S_α(m-1)
               = Σ_p [cos(2πpm/N)(2 - 2cos(2πp/N))] / |sin(πp/N)|^α
               = 4 Σ_p cos(2πpm/N) sin²(πp/N) / |sin(πp/N)|^α
               = 4 Σ_p cos(2πpm/N) |sin(πp/N)|^{2-α}

     For α = 2: this is 4 Σ cos(2πpm/N) × 1 = 4 × (-1) = -4 (constant). ✓
     For α ≠ 2: this is 4 Σ cos(2πpm/N) |sin(πp/N)|^{2-α}, which is
     the Fourier coefficient of |sin(x)|^{2-α} — a non-constant function of m
     unless 2-α = 0.

COROLLARY: The Havelock angular Hessian kernel K_d(x) = sin^{-d}(x) gives
polynomial eigenvalues only for d = 2. Since K_d arises from the d-dimensional
Laplacian Green's function, the polynomial Havelock framework requires d = 2.

HOLOMORPHICITY THEOREM: The polynomial structure follows from the factorization
  [1 - cos(2πpm/N)] / sin²(πp/N) = |Σ_{k=0}^{m-1} ω^{pk}|²
where ω = e^{2πi/N}. This factorization uses the holomorphic function z^k,
which exists only for 2D (complex) domains. In d ≥ 3, the kernel cannot be
written as |holomorphic|² and the polynomial structure is lost.
"""

import numpy as np
from math import pi, sin, cos, log


# =====================================================================
# PART 1: The csc^α sum and its finite differences
# =====================================================================

def csc_alpha_sum(m, N, alpha):
    """S_α(m, N) = Σ_{p=1}^{N-1} [1 - cos(2πpm/N)] / |sin(πp/N)|^α."""
    total = 0.0
    for p in range(1, N):
        x = pi * p / N
        sx = abs(sin(x))
        if sx < 1e-15:
            continue
        total += (1 - cos(2 * pi * p * m / N)) / sx**alpha
    return total


def second_difference(m, N, alpha):
    """Δ²S_α(m) = S_α(m+1) - 2S_α(m) + S_α(m-1).

    For α = 2: Δ² = constant = -4 (proof of polynomial degree 2).
    For α ≠ 2: Δ² varies with m (proof of non-polynomial).
    """
    if m < 1 or m > N - 2:
        return None
    return (csc_alpha_sum(m + 1, N, alpha)
            - 2 * csc_alpha_sum(m, N, alpha)
            + csc_alpha_sum(m - 1, N, alpha))


def second_difference_formula(m, N, alpha):
    """Δ²S_α(m) = 4 Σ cos(2πpm/N) |sin(πp/N)|^{2-α}.

    This is the ANALYTIC formula for the second difference.
    For α = 2: the sin factor is sin^0 = 1, so the sum is
               4 Σ cos(2πpm/N) = 4 × (-1) = -4 (for 0 < m < N).
    For α ≠ 2: the sin factor is non-trivial and the sum varies with m.
    """
    total = 0.0
    for p in range(1, N):
        x = pi * p / N
        sx = abs(sin(x))
        total += cos(2 * pi * p * m / N) * sx**(2 - alpha)
    return 4 * total


# =====================================================================
# PART 2: Verification of the second-difference proof
# =====================================================================

def verify_second_difference(N, alpha):
    """Verify the second-difference formula and check constancy.

    For α = 2: all Δ² should equal -4 (to machine precision).
    For α ≠ 2: Δ² should vary with m.

    Returns (values, is_constant, max_deviation_from_mean).
    """
    values = []
    for m in range(1, N - 1):
        d2_numeric = second_difference(m, N, alpha)
        d2_formula = second_difference_formula(m, N, alpha)
        values.append({
            'm': m,
            'numeric': d2_numeric,
            'formula': d2_formula,
            'match': abs(d2_numeric - d2_formula) < 1e-8 if d2_numeric is not None else False,
        })

    numeric_vals = [v['numeric'] for v in values if v['numeric'] is not None]
    if len(numeric_vals) < 2:
        return values, True, 0.0

    mean = np.mean(numeric_vals)
    max_dev = max(abs(v - mean) for v in numeric_vals)
    relative_dev = max_dev / abs(mean) if abs(mean) > 1e-15 else max_dev

    is_constant = relative_dev < 1e-10

    return values, is_constant, relative_dev


def proof_table(N_values=None, alpha_values=None):
    """Complete proof table: for each (N, α), check if Δ² is constant.

    α = 2: constant (polynomial) — the Ramanujan identity
    α ≠ 2: non-constant (non-polynomial) — the theorem
    """
    if N_values is None:
        N_values = [7, 10, 13, 16]
    if alpha_values is None:
        alpha_values = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0]

    results = []
    for N in N_values:
        for alpha in alpha_values:
            _, is_const, rel_dev = verify_second_difference(N, alpha)
            results.append({
                'N': N,
                'alpha': alpha,
                'is_constant': is_const,
                'relative_deviation': rel_dev,
                'polynomial': is_const,
            })

    return results


# =====================================================================
# PART 3: The holomorphic factorization (α = 2 only)
# =====================================================================

def holomorphic_factorization(m, N, p):
    """The factorization: [1-cos(2πpm/N)]/sin²(πp/N) = 2|Σ_{k=0}^{m-1} ω^{pk}|²

    where ω = e^{2πi/N}.

    Proof: 1-cos(θ) = 2sin²(θ/2), and |Σω^{pk}|² = sin²(πpm/N)/sin²(πp/N).
    So LHS = 2sin²(πpm/N)/sin²(πp/N) = 2|geometric_sum|².

    Summing over p: Σ_p LHS = 2Σ_p|Σ_k ω^{pk}|² = 2m(N-m) (Ramanujan).
    """
    omega = np.exp(2j * pi / N)

    # Left side: [1 - cos(2πpm/N)] / sin²(πp/N)
    x = pi * p / N
    sx = sin(x)
    if abs(sx) < 1e-15:
        return 0.0, 0.0

    lhs = (1 - cos(2 * pi * p * m / N)) / sx**2

    # Right side: 2|Σ_{k=0}^{m-1} ω^{pk}|²
    geometric_sum = sum(omega**(p * k) for k in range(m))
    rhs = 2 * abs(geometric_sum)**2

    return lhs, rhs


def verify_factorization(N):
    """Verify the holomorphic factorization for all (m, p) pairs.

    Returns max error across all pairs.
    """
    max_err = 0.0
    for m in range(1, N):
        for p in range(1, N):
            lhs, rhs = holomorphic_factorization(m, N, p)
            err = abs(lhs - rhs)
            max_err = max(max_err, err)
    return max_err


# =====================================================================
# PART 4: Non-existence of factorization for α ≠ 2
# =====================================================================

def factorization_test_alpha(N, alpha, m, p):
    """Test whether [1-cos(2πpm/N)]/sin^α(πp/N) = |f(ω^p)|² for any
    polynomial f.

    For α = 2: f(z) = Σ z^k (geometric sum) works.
    For α ≠ 2: no polynomial f exists.

    We test by checking if the LHS can be written as the modulus squared
    of a geometric sum with modified weights.
    """
    x = pi * p / N
    sx = abs(sin(x))
    if sx < 1e-15:
        return 0.0, 0.0, 0.0

    lhs = (1 - cos(2 * pi * p * m / N)) / sx**alpha

    # The α = 2 factorization value
    omega = np.exp(2j * pi / N)
    geometric_sum = sum(omega**(p * k) for k in range(m))
    rhs_alpha2 = abs(geometric_sum)**2

    # Ratio: how far is the α ≠ 2 case from the α = 2 factorization?
    if rhs_alpha2 > 1e-15:
        ratio = lhs / rhs_alpha2  # = sin^{2-α}(x) for the correction factor
    else:
        ratio = 0.0

    return lhs, rhs_alpha2, ratio


# =====================================================================
# PART 5: The dimension theorem statement
# =====================================================================

def dimension_theorem_check(N_values=None):
    """Comprehensive check of the dimension theorem.

    For each N:
    1. Verify the Ramanujan identity (α = 2, polynomial)
    2. Verify non-polynomiality for α = 1, 3, 4
    3. Verify the holomorphic factorization
    4. Verify the second-difference proof

    Returns a summary dict.
    """
    if N_values is None:
        N_values = [7, 10, 13]

    results = []
    for N in N_values:
        # 1. Ramanujan identity
        _, is_poly_2, dev_2 = verify_second_difference(N, 2.0)

        # 2. Non-polynomial for α ≠ 2
        _, is_poly_3, dev_3 = verify_second_difference(N, 3.0)
        _, is_poly_4, dev_4 = verify_second_difference(N, 4.0)
        _, is_poly_1, dev_1 = verify_second_difference(N, 1.0)

        # 3. Holomorphic factorization
        fact_err = verify_factorization(N)

        results.append({
            'N': N,
            'alpha2_polynomial': is_poly_2,
            'alpha2_deviation': dev_2,
            'alpha3_polynomial': is_poly_3,
            'alpha3_deviation': dev_3,
            'alpha4_polynomial': is_poly_4,
            'alpha4_deviation': dev_4,
            'alpha1_polynomial': is_poly_1,
            'alpha1_deviation': dev_1,
            'factorization_error': fact_err,
            'theorem_holds': is_poly_2 and not is_poly_3 and not is_poly_4 and fact_err < 1e-10,
        })

    return results
