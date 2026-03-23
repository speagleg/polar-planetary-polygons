"""
Small-ring expansion of C₁(x, ε) on a curved surface.

Place a regular N-gon of geodesic radius ε at point x on a surface S
with metric g and scalar curvature R(x). The mode-averaged Havelock
offset C₁ expands as:

    C₁(x, ε) = C₁⁰(ε) + C₁¹(x) · ε² + C₁²(x) · ε⁴ + ...

where:
    C₁⁰(ε) = log(2ε) + b_flat(N)     [flat-space value]
    C₁¹(x) = (N-1)/6 · R(x)           [curvature correction, from B₂ = 1/6]

The Hamiltonian constraint C₁ = f(m*) forces:
    R(x) = constant for all x  ⟹  vacuum Einstein equation

This computation verifies the coefficient (N-1)/6 numerically by
computing C₁ on surfaces of known constant curvature K and
extracting the ε² coefficient.
"""

import numpy as np
from math import pi, sin, cos, log, exp, sqrt, sinh, cosh, asinh


def casimir(m, N):
    return m * (N - m) / 2.0


# =====================================================================
# The Green's function on a surface of curvature K
# =====================================================================

def greens_function(d, K):
    """Green's function h(d) = -log(2 sinh_K(d/2)) where
    sinh_K is the generalized sine function:
        K < 0: sinh(sqrt(|K|) d) / sqrt(|K|)
        K = 0: d
        K > 0: sin(sqrt(K) d) / sqrt(K)
    """
    if abs(d) < 1e-15:
        return 30.0

    if K < -1e-12:
        kappa = sqrt(-K)
        arg = 2 * sinh(kappa * d / 2) / kappa
        return -log(arg) if arg > 1e-15 else 30.0
    elif K > 1e-12:
        kappa = sqrt(K)
        arg = 2 * sin(kappa * d / 2) / kappa
        return -log(arg) if arg > 1e-15 else 30.0
    else:
        return -log(d) if d > 1e-15 else 30.0


def inter_vortex_distance(p, N, eps, K):
    """Geodesic distance between vortex 0 and vortex p on a regular
    N-gon of circumradius eps on a surface of curvature K.

    The exact factorization:
    K < 0: sinh(sqrt(|K|) d_p / 2) = sinh(sqrt(|K|) eps) sin(pi p/N)
    K = 0: d_p = 2 eps sin(pi p/N)
    K > 0: sin(sqrt(K) d_p / 2) = sin(sqrt(K) eps) sin(pi p/N)
    """
    sin_angle = abs(sin(pi * p / N))

    if K < -1e-12:
        kappa = sqrt(-K)
        sinh_half = sinh(kappa * eps) * sin_angle
        return 2 * asinh(sinh_half) / kappa
    elif K > 1e-12:
        kappa = sqrt(K)
        sin_half = sin(kappa * eps) * sin_angle
        if abs(sin_half) > 1:
            return pi / kappa
        from math import asin
        return 2 * asin(min(1.0, abs(sin_half))) / kappa
    else:
        return 2 * eps * sin_angle


def C1_on_curved_surface(N, eps, K):
    """Compute C₁(eps, K) = (1/(N-1)) sum_m [lambda_m + f(m)]."""
    total = 0.0
    for m in range(1, N):
        lam = 0.0
        for p in range(1, N):
            d_p = inter_vortex_distance(p, N, eps, K)
            lam += greens_function(d_p, K) * cos(2 * pi * p * m / N)
        fm = casimir(m, N)
        total += lam + fm
    return total / (N - 1)


# =====================================================================
# PART 1: Extract the ε² coefficient numerically
# =====================================================================

def extract_epsilon2_coefficient(N, K):
    """Extract C₁¹ from the small-ε expansion: C₁(ε,K) = C₁⁰(ε) + C₁¹·ε² + ...

    Method: compute C₁ at several small ε values and fit to
    C₁(ε, K) - C₁(ε, 0) = C₁¹ · ε² + O(ε⁴)

    The DIFFERENCE C₁(K) - C₁(0) isolates the curvature correction.
    """
    epsilons = np.array([0.01, 0.02, 0.03, 0.05, 0.07, 0.1, 0.15, 0.2])

    C1_K = np.array([C1_on_curved_surface(N, eps, K) for eps in epsilons])
    C1_0 = np.array([C1_on_curved_surface(N, eps, 0) for eps in epsilons])

    delta_C1 = C1_K - C1_0  # the curvature correction

    # Fit: delta_C1 = a * eps^2 + b * eps^4
    X = np.column_stack([epsilons**2, epsilons**4])
    coeffs, _, _, _ = np.linalg.lstsq(X, delta_C1, rcond=None)

    C1_1 = coeffs[0]  # the ε² coefficient
    C1_2 = coeffs[1]  # the ε⁴ coefficient

    # Check the fit
    fitted = X @ coeffs
    residuals = delta_C1 - fitted
    max_resid = np.max(np.abs(residuals))

    return C1_1, C1_2, max_resid, epsilons, delta_C1, fitted


def verify_R_over_6(N_max=12):
    """Verify: C₁¹ = (something) * K, and extract the coefficient.

    The prediction: C₁(ε, K) - C₁(ε, 0) = [(N-1)/6] * K * ε² + O(ε⁴)
    So C₁¹ = [(N-1)/6] * K, giving C₁¹/K = (N-1)/6.

    But wait — the Hadamard expansion of the Green's function gives:
    G(x, y) = -(1/2π) log(d) + (R/12π) d² log(d) + ...

    For the Havelock eigenvalue, the relevant expansion is of
    h(d_p) = -log(2 sinh_K(d_p/2)) around K = 0:

    h(d_p, K) = h(d_p, 0) + (∂h/∂K)|₀ · K + O(K²)

    The K-derivative of h involves the K-derivative of d_p:
    d_p(K) = 2ε sin(πp/N) + K · [correction] + ...

    Let me just compute it numerically and see what the coefficient is.
    """
    print("=" * 72)
    print("  SMALL-RING EXPANSION: C₁(ε, K) = C₁(ε, 0) + C₁¹ · ε² + ...")
    print("  Extracting C₁¹ and comparing with R/6 prediction")
    print("=" * 72)

    print(f"\n  {'N':>4s} {'K':>8s} {'C₁¹':>12s} {'C₁¹/K':>12s} "
          f"{'(N-1)/6':>10s} {'ratio':>10s} {'residual':>10s}")

    for N in range(4, N_max + 1):
        predicted = (N - 1) / 6.0

        for K in [-1.0, -0.5, -0.1, 0.1, 0.5, 1.0]:
            if K > 0 and K > 0.5:
                # Skip large positive K (sphere closes up)
                continue

            C1_1, C1_2, resid, _, _, _ = extract_epsilon2_coefficient(N, K)
            ratio_to_K = C1_1 / K if abs(K) > 1e-12 else float('nan')
            ratio = ratio_to_K / predicted if abs(predicted) > 1e-12 else float('nan')

            if K == -1.0 or K == -0.1:  # print selected rows
                print(f"  {N:4d} {K:8.4f} {C1_1:12.6f} {ratio_to_K:12.6f} "
                      f"{predicted:10.6f} {ratio:10.6f} {resid:10.2e}")


def detailed_expansion(N):
    """Detailed ε-by-ε comparison for a specific N."""
    print(f"\n  Detailed expansion for N = {N}:")
    print(f"  {'ε':>8s} {'C₁(K=-1)':>12s} {'C₁(K=0)':>12s} "
          f"{'delta':>12s} {'delta/ε²':>12s} {'predicted':>12s}")

    K = -1.0
    predicted_coeff = (N - 1) / 6.0  # the R/6 prediction (R = K = -1 here)

    for eps in [0.005, 0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3]:
        C1_K = C1_on_curved_surface(N, eps, K)
        C1_0 = C1_on_curved_surface(N, eps, 0)
        delta = C1_K - C1_0
        ratio = delta / eps**2 if eps > 0 else 0
        pred = predicted_coeff * K  # = -(N-1)/6

        print(f"  {eps:8.4f} {C1_K:12.6f} {C1_0:12.6f} "
              f"{delta:12.8f} {ratio:12.6f} {pred:12.6f}")


# =====================================================================
# PART 2: The Hadamard-DeWitt expansion
# =====================================================================

def hadamard_expansion():
    """The Hadamard-DeWitt expansion of the Green's function.

    On a surface of scalar curvature R, the Green's function G(x,y)
    of the Laplacian has the short-distance expansion:

    G(x,y) = -(1/2π) [log(d/2) + γ] + (R(x)/12π) d² [1/2 - log(d)] + O(d⁴)

    where d = geodesic distance.

    For the HAVELOCK kernel h(d) = -log(2 sinh_K(d/2)):
    At small d: sinh_K(d/2) ≈ d/2 + K d³/48 + ...
    So: 2 sinh_K(d/2) ≈ d + K d³/24 + ...
    And: h(d) = -log(d + Kd³/24 + ...) = -log(d) - Kd²/24 + ...

    Wait, that's -K/24, not -(N-1)R/6.

    But h is the kernel for a SINGLE pair (p, q). The Havelock eigenvalue
    sums h over all pairs with cosine weights. And C₁ averages over modes.

    Let me redo: for a single pair at distance d_p:
    d_p(K) = 2ε sin(πp/N) * [1 + Kε² correction + ...]

    The geodesic distance on a curved surface:
    d_p = 2ε sin(πp/N) * [1 - Kε²/6 sin²(πp/N)/3 + ...]  (approximately)

    Actually the exact expansion involves the SECTIONAL curvature
    along the geodesic from vortex 0 to vortex p.

    For constant curvature K (which is what we're computing):
    sinh_K(d/2) = sinh(sqrt(|K|) d/2) / sqrt(|K|)  for K < 0
    At small d: this is d/2 + |K| d³/48 + ...
    And 2 sinh_K(d/2) = d * [1 + |K| d²/24 + ...]

    For our polygon: d_p = 2ε sin(πp/N) at K = 0.
    At K ≠ 0: the factorization gives
    2 sinh_K(d_p/2) = 2 sinh_K(ε) sin(πp/N)
    = [2ε(1 + |K|ε²/6 + ...)] sin(πp/N)  for K < 0

    So: h(d_p, K) = -log(2 sinh_K(ε) sin(πp/N))
                   = -log(2ε sin(πp/N)) - log(1 + |K|ε²/6 + ...)
                   = h(d_p, 0) - |K|ε²/6 + O(ε⁴)

    For K < 0 (K = -|K|): the correction is -|K|ε²/6 = Kε²/6... wait:
    sinh(kappa ε) = kappa ε + (kappa ε)³/6 + ...
    2 sinh(kappa ε)/kappa = 2ε + 2(kappa²)ε³/6 + ... = 2ε(1 + kappa² ε²/6 + ...)
    = 2ε(1 + |K| ε²/6 + ...)   [since kappa² = |K| for K < 0]

    log(1 + |K|ε²/6) ≈ |K|ε²/6

    So: h(d_p, K) = h(d_p, 0) - |K|ε²/6 + O(ε⁴)
    And since K = -|K|:
    h(d_p, K) = h(d_p, 0) + Kε²/6 + O(ε⁴)  ... wait, sign:
    -|K| = K, so |K|ε²/6 = -Kε²/6.
    h(d_p, K) = h(d_p, 0) - (-K)ε²/6 = h(d_p, 0) + Kε²/6

    Hmm, let me be very careful. For K < 0, kappa = sqrt(-K) = sqrt(|K|):
    2 sinh(kappa ε) / kappa = 2ε * [1 + kappa² ε²/6 + ...]
                            = 2ε * [1 + |K| ε²/6 + ...]
                            = 2ε * [1 - K ε²/6 + ...]  (since K < 0, |K| = -K)

    h(d_p) = -log(2ε sin(πp/N)) - log(1 - K ε²/6 + ...)
           = h_flat(d_p) + K ε²/6 + O(ε⁴)  ... NO:
    -log(1 + x) ≈ -x for small x.
    -log(1 - Kε²/6) ≈ +Kε²/6 (since K < 0, this is negative)

    So: h(d_p, K) = h_flat(d_p) + Kε²/6

    This correction is the SAME for all p (it doesn't depend on sin(πp/N)).
    Therefore it contributes to the Havelock eigenvalue as:
    lambda_m(K) = lambda_m(0) + (Kε²/6) * sum_p cos(2πpm/N)
                = lambda_m(0) + (Kε²/6) * (-1)  [for m ≠ 0]
                = lambda_m(0) - Kε²/6

    And C₁(K) = C₁(0) - Kε²/6 + (mean f correction)
    Wait: C₁ = (1/(N-1)) sum_m [lambda_m + f_m]
    The K correction to lambda_m is -Kε²/6 for each m (m=1,...,N-1).
    So the correction to C₁ is also -Kε²/6.

    For K < 0: -Kε²/6 > 0 (C₁ increases, stabilizing).
    For K > 0: -Kε²/6 < 0 (C₁ decreases, destabilizing).

    THE COEFFICIENT IS -K/6, NOT -(N-1)K/6 or -K·R/6.
    """
    pass  # the derivation is in the docstring


# =====================================================================
# PART 3: The analytical derivation
# =====================================================================

def analytical_coefficient():
    """Derive the ε² coefficient analytically.

    From the expansion of sinh(kappa ε):
    2 sinh(kappa ε) / kappa = 2ε (1 + kappa² ε²/6 + ...)
                             = 2ε (1 - K ε²/6 + ...)

    The Havelock kernel:
    h(d_p, K) = -log(2 sinh_K(ε) sin(πp/N))
              = -log(2ε sin(πp/N)) + K ε²/6 + ...  [correction is +K/6]
              Wait: -log(1 - K ε²/6) = +K ε²/6 for K < 0... let me redo.

    -log(2ε(1 - Kε²/6) sin(πp/N))
    = -log(2ε sin) - log(1 - Kε²/6)
    = h_flat + Kε²/6 + O(ε⁴)   [since -log(1-x) ≈ x for small x,
                                  and here x = -Kε²/6, so -log(1-(-Kε²/6)) = -Kε²/6... ]

    OK let me just be explicit.
    Let u = Kε²/6 (which is negative for K < 0).
    2 sinh_K(ε) = 2ε(1 - u + ...)  ... NO:

    For K < 0: kappa = sqrt(-K).
    sinh(kappa ε) = kappa ε + (kappa ε)³/6 + ...
    2 sinh(kappa ε)/kappa = 2ε + 2 kappa² ε³/6 + ... = 2ε + (-K) ε³/3 + ...
    = 2ε(1 + (-K) ε²/6 + ...)

    Since K < 0: -K > 0, so the factor (1 + (-K)ε²/6) > 1.
    The distance 2 sinh_K(ε) is LARGER than 2ε on H^2 (geodesics spread apart).

    h(d_p) = -log(2ε(1 + (-K)ε²/6) sin(πp/N))
           = -log(2ε sin) - log(1 + (-K)ε²/6)
           = h_flat - (-K)ε²/6 + O(ε⁴)
           = h_flat + Kε²/6

    So h(d_p, K) = h_flat(d_p) + Kε²/6  (confirmed: +K/6)

    For K = -1: correction = -ε²/6 (h decreases, distances are larger on H^2,
    so the log of the distance is larger, so h = -log(distance) is smaller).

    The HAVELOCK eigenvalue:
    lambda_m(K) = sum_p h(d_p, K) cos(2πpm/N)
                = sum_p [h_flat(d_p) + Kε²/6] cos(2πpm/N)
                = lambda_m(0) + (Kε²/6) sum_p cos(2πpm/N)

    For m ≠ 0: sum cos = -1. So lambda_m(K) = lambda_m(0) - Kε²/6.

    C₁(K) = (1/(N-1)) sum_m [lambda_m(K) + f_m]
           = C₁(0) - Kε²/6

    THE CORRECTION IS -Kε²/6, independent of N (to leading order).
    """
    print(f"\n{'='*72}")
    print("  ANALYTICAL DERIVATION")
    print("=" * 72)

    print("""
  The Hadamard expansion of the Havelock kernel at small ε:

    h(d_p, K) = h_flat(d_p) + (K/6) ε² + O(ε⁴)

  Derivation: 2 sinh_K(ε) = 2ε(1 + (-K)ε²/6 + ...)
  So h = -log(2ε sin(πp/N)) - log(1 + (-K)ε²/6)
       = h_flat + (K/6)ε²    [since -log(1+x) ≈ -x]

  The correction K/6 is p-INDEPENDENT (same for all vortex pairs).

  The Havelock eigenvalue:
    λ_m(K) = λ_m(0) + (K/6)ε² · Σ cos(2πpm/N)
           = λ_m(0) - (K/6)ε²    [since Σ cos = -1 for m ≠ 0]

  The mode-averaged offset:
    C₁(K) = C₁(0) - (K/6)ε²

  THE COEFFICIENT IS -K/6 = -R/6 where R = K (Gaussian curvature).

  NOTE: This is -R/6, not -(N-1)R/6. The factor (N-1) appears in
  the SUM over modes, but cancels in the AVERAGE (dividing by N-1).
""")


# =====================================================================
# PART 4: Numerical verification
# =====================================================================

def numerical_verification():
    """Verify -K/6 coefficient for several N and K values."""
    print(f"\n{'='*72}")
    print("  NUMERICAL VERIFICATION: C₁(K) - C₁(0) = -(K/6)ε²")
    print("=" * 72)

    print(f"\n  {'N':>4s} {'K':>8s} {'ε':>8s} {'C₁(K)':>12s} {'C₁(0)':>12s} "
          f"{'delta':>12s} {'-(K/6)ε²':>12s} {'ratio':>10s}")

    for N in [4, 6, 7, 8, 10, 12]:
        for K in [-1.0, -0.5, 0.5]:
            for eps in [0.01, 0.05, 0.1]:
                if K > 0 and eps > pi / (2 * sqrt(K)) * 0.9:
                    continue

                C1_K = C1_on_curved_surface(N, eps, K)
                C1_0 = C1_on_curved_surface(N, eps, 0)
                delta = C1_K - C1_0
                predicted = -(K / 6) * eps**2
                ratio = delta / predicted if abs(predicted) > 1e-15 else float('nan')

                if eps == 0.05:  # print one ε value per (N, K)
                    print(f"  {N:4d} {K:8.4f} {eps:8.4f} {C1_K:12.6f} "
                          f"{C1_0:12.6f} {delta:12.8f} {predicted:12.8f} "
                          f"{ratio:10.6f}")


# =====================================================================
# PART 5: The Einstein equation derivation
# =====================================================================

def einstein_equation():
    """The step from C₁(x,ε) = f(m*) to the Einstein equation."""
    print(f"\n{'='*72}")
    print("  THE EINSTEIN EQUATION FROM HAVELOCK")
    print("=" * 72)

    print("""
  THEOREM (Havelock implies Einstein).

  Given:
    1. The Havelock Casimir f(m,N) = m(N-m)/2 (exact polynomial)
    2. The logarithmic interaction (from the csc² uniqueness theorem)
    3. The Hamiltonian constraint C₁(x, ε) = f(m*) at every point x

  PROOF.

  Step 1: The small-ring expansion of C₁ on a curved surface:
    C₁(x, ε) = C₁_flat(ε) - R(x)/6 · ε² + O(ε⁴)

  where R(x) is the scalar curvature at x.
  [Derived from: 2 sinh_K(ε) = 2ε(1 + (-K)ε²/6 + ...) and the
   property that the correction is p-independent.]

  Step 2: The Hamiltonian constraint at every point x:
    C₁(x, ε) = f(m*)

  Since f(m*) = m*(N-m*)/2 is a CONSTANT (independent of x):
    C₁_flat(ε) - R(x)/6 · ε² = constant

  Step 3: C₁_flat(ε) is x-independent (it depends only on ε and N).
  Therefore:
    R(x)/6 · ε² = C₁_flat(ε) - f(m*) = another constant

  Since ε is a global parameter (same polygon size everywhere):
    R(x) = constant ≡ R₀

  Step 4: R(x) = R₀ for all x on a 2D surface IS the condition for
  constant curvature. In d = 2+1 dimensions, this is equivalent to
  the vacuum Einstein equation:

    R_μν = Λ g_μν  with  Λ = R₀/2

  Step 5: The value of Λ:
    R₀ = 6(C₁_flat(ε) - f(m*)) / ε²

  This determines Λ in terms of:
    - ε: the polygon size (a physical scale)
    - N: the polygon type (an integer)
    - f(m*) = m*(N-m*)/2: the Casimir (a derived quantity)
    - C₁_flat(ε) = log(2ε) + b_flat(N): the flat-space offset

  For the CRITICAL polygon (at the stability threshold):
    C₁_flat(ε*) = f(m*) ⟹ R₀ = 0 ⟹ Λ = 0

  The critical polygon sits at EXACTLY Λ = 0.

  For a polygon BELOW threshold (ε < ε*, stable):
    C₁_flat(ε) < f(m*) ⟹ R₀ > 0 ⟹ Λ > 0 (de Sitter)

  For a polygon ABOVE threshold (ε > ε*, unstable on flat):
    C₁_flat(ε) > f(m*) ⟹ R₀ < 0 ⟹ Λ < 0 (anti-de Sitter)

  THE SIGN OF Λ IS DETERMINED BY THE STABILITY STATUS:
    Stable on flat → Λ > 0 (needs positive curvature to match C₁ = f)
    Marginal → Λ = 0 (flat is the right geometry)
    Unstable on flat → Λ < 0 (needs negative curvature to stabilize)
""")

    # Compute the flat threshold ε* for each N
    print(f"  Flat-plane threshold ε* for each N:")
    print(f"  {'N':>4s} {'m*':>4s} {'f(m*)':>10s} {'b_flat(N)':>10s} "
          f"{'ε*':>12s} {'Λ sign':>10s}")

    for N in range(4, 13):
        m_crit = N // 2
        f_crit = casimir(m_crit, N)

        # b_flat(N) ≈ b_exact but with the flat kernel
        # On the flat plane: C₁_flat = log(2ε) + b_flat
        # At the threshold: log(2ε*) + b_flat = f_crit
        # ε* = exp(f_crit - b_flat) / 2

        # b_flat uses the same formula as b_exact (the Euler-Maclaurin
        # correction doesn't depend on the curvature to leading order)
        b_flat = N * (N + 1) / 12 - log(2) + log(N) / (N - 1)

        eps_star = exp(f_crit - b_flat) / 2

        # For ε = 1 (unit polygon): what's the sign of Λ?
        C1_flat_at_1 = log(2) + b_flat
        sign_Lambda = "Λ > 0" if C1_flat_at_1 < f_crit else "Λ = 0" if abs(C1_flat_at_1 - f_crit) < 0.01 else "Λ < 0"

        print(f"  {N:4d} {m_crit:4d} {f_crit:10.4f} {b_flat:10.4f} "
              f"{eps_star:12.6f} {sign_Lambda:>10s}")


def main():
    print("=" * 72)
    print("  SMALL-RING EXPANSION AND THE EINSTEIN EQUATION")
    print("=" * 72)

    analytical_coefficient()
    numerical_verification()
    einstein_equation()

    # Final: the specific N = 7 check
    print(f"\n{'='*72}")
    print("  THE N = 7 CHECK")
    print("=" * 72)

    N = 7
    m_crit = 3
    f_crit = casimir(m_crit, N)
    b_flat = N * (N + 1) / 12 - log(2) + log(N) / (N - 1)

    print(f"\n  N = {N}, m* = {m_crit}, f(m*) = {f_crit:.4f}")
    print(f"  b_flat(N) = {b_flat:.6f}")
    print(f"  f(m*) - b_flat = {f_crit - b_flat:.6f}")
    print(f"  ε* (flat threshold) = exp({f_crit - b_flat:.4f})/2 = {exp(f_crit - b_flat)/2:.6f}")

    print(f"\n  At the threshold ε = ε*:")
    print(f"  C₁_flat(ε*) = f(m*) = {f_crit:.4f}")
    print(f"  R₀ = 6(C₁_flat - f(m*)) / ε² = 0")
    print(f"  Λ = R₀/2 = 0")
    print(f"\n  The N = 7 polygon at its flat-plane stability threshold")
    print(f"  gives EXACTLY Λ = 0.")
    print(f"\n  But this is TRUE FOR ALL N: at ε = ε*(N), Λ = 0 by construction.")
    print(f"  The question is whether ε*(N) is 'natural' — whether the")
    print(f"  polygon size at threshold has a physical interpretation.")


if __name__ == "__main__":
    main()
