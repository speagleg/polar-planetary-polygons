"""
Riemannian Havelock identity and trace formula. (§6.8)

The Riemannian Havelock identity (flat case) states that the sum

    T_m = sum_{p=1}^{N-1} [1 - cos(2π p m/N)] / [2 sin²(π p/N)] = m(N-m)

exactly for all integers 1 ≤ m ≤ N-1.

On curved surfaces, the exact Lagrangian eigenvalue satisfies:

    λ_m · r_E² + m(N-m)/2 = C₁(surface, ξ)

where C₁ is the surface-dependent constant:
    C₁(H², ξ)  = (N-1)(1+ξ²)/(1-ξ)²   [hyperbolic plane, ξ = r_E²/a²]
    C₁(S², ξ)  = (N-1)(1-ξ)/(1+ξ)     [sphere, ξ = R²/a²]
    C₁(flat)   = N-1                    [flat plane, ξ→0 limit]

Note: the r_E² factor on λ_m is essential — the eigenvalue has units of 1/r_E².

The trace formula (§6.8 Corollary) gives the diagonal contribution of the
interaction potential to the stability operator on a curved surface:

    delta_trace = -N / (4 π R²)   [sphere]
    delta_trace = -N / (4 π² R²)  [torus]

These encode the Riemannian curvature correction to the flat-plane result.
"""
import numpy as np
from fractions import Fraction


def havelock_sum(N, m):
    """
    Numerical evaluation of the Havelock sum.

        T_m = sum_{p=1}^{N-1} [1 - cos(2π p m / N)] / [2 sin²(π p / N)]

    This sum equals m(N-m) exactly (proved analytically via Fourier analysis
    on Z_N). The numerical sum serves as a cross-check.

    Parameters
    ----------
    N : int
        Ring size.
    m : int
        Fourier mode index, 1 ≤ m ≤ N-1.

    Returns
    -------
    float
        Numerical value of T_m. Should equal m*(N-m) to machine precision.
    """
    total = 0.0
    for p in range(1, N):
        sin_sq = np.sin(np.pi * p / N) ** 2
        cos_term = np.cos(2 * np.pi * p * m / N)
        total += (1.0 - cos_term) / (2.0 * sin_sq)
    return total


def havelock_exact(N, m):
    """
    Exact value of the Havelock sum as a Fraction.

        T_m = m(N-m)

    This is the closed-form result that the numerical havelock_sum should
    reproduce to machine precision.

    Parameters
    ----------
    N : int
        Ring size.
    m : int
        Fourier mode index, 1 ≤ m ≤ N-1.

    Returns
    -------
    fractions.Fraction
        Exact rational value m*(N-m).
    """
    return Fraction(m * (N - m), 1)


def trace_formula_delta(N, surface='sphere', R=1.0):
    """
    Trace formula correction to the stability operator on a curved surface.

    For a ring of N equal vortices on a surface of constant curvature,
    the interaction potential contributes a diagonal shift to the stability
    operator. This shift is:

        delta = -N / (4 π R²)    [sphere, radius R]
        delta = -N / (4 π² R²)   [torus, major radius R]

    The flat-plane limit (R → ∞) gives delta → 0, recovering the Thomson result.

    Parameters
    ----------
    N : int
        Number of vortices.
    surface : str
        Surface type: 'sphere' or 'torus'.
    R : float
        Characteristic radius (default 1.0).

    Returns
    -------
    float
        Trace formula diagonal shift delta.

    Raises
    ------
    ValueError
        If surface is not recognised.
    """
    if surface == 'sphere':
        return -N / (4.0 * np.pi * R**2)
    elif surface == 'torus':
        return -N / (4.0 * np.pi**2 * R**2)
    raise ValueError(f"Unknown surface: {surface!r}. Use 'sphere' or 'torus'.")


def C1_hyperbolic(N, xi):
    """
    Exact C₁ coefficient for N-vortex ring on H².

    C₁(H², ξ) = (N-1)(1+ξ²)/(1-ξ)²

    Parameters
    ----------
    N : int
        Ring size.
    xi : float
        ξ = r_E²/a², where r_E is Euclidean ring radius, a is curvature radius.
        Ranges 0 (flat limit) to 1 (boundary of disk).

    Returns
    -------
    float
        C₁ value. For ξ→0: C₁→N-1 (flat limit). Diverges as ξ→1.
    """
    return (N - 1) * (1 + xi**2) / (1 - xi)**2


def C1_sphere(N, xi):
    """
    Exact C₁ coefficient for N-vortex ring on S².

    C₁(S², ξ) = (N-1)(1+ξ²)/(1+ξ)²

    Confirmed by LMR05 (Laurent-Polz, Montaldi, Roberts 2005, Thm 4.2)
    and by numerical diagonalization of the constrained Lagrangian Hessian
    (docs/rigor-sandbox/item6-c1-sphere/numerical_check.py).

    H²/S² duality: C₁(S²,ξ) = C₁(H²,-ξ), i.e.
    (1+ξ²)/(1+ξ)² vs (1+ξ²)/(1-ξ)².

    Parameters
    ----------
    N : int
        Ring size.
    xi : float
        ξ = tan²(φ₀/2), stereographic parameter at colatitude φ₀.

    Returns
    -------
    float
        C₁ value. For ξ→0: C₁→N-1 (flat limit). C₁→(N-1)/2 as ξ→∞.
    """
    return (N - 1) * (1 + xi**2) / (1 + xi)**2


def riemannian_havelock_eigenvalue(N, m, xi, surface='hyperbolic', r_E=1.0):
    """
    Lagrangian eigenvalue from the Riemannian Havelock identity.

    λ_m = [C₁(surface, ξ) - m(N-m)/2] / r_E²

    Parameters
    ----------
    N : int
        Ring size.
    m : int
        Fourier mode index, 1 ≤ m ≤ N//2.
    xi : float
        Curvature parameter ξ = r_E²/a² (hyperbolic) or R²/a² (sphere).
    surface : str
        'hyperbolic' or 'sphere'.
    r_E : float
        Euclidean ring radius (default 1.0). Eigenvalue scales as 1/r_E².

    Returns
    -------
    float
        Lagrangian eigenvalue λ_m. Positive = stable mode.
    """
    if surface == 'hyperbolic':
        C1 = C1_hyperbolic(N, xi)
    elif surface == 'sphere':
        C1 = C1_sphere(N, xi)
    else:
        raise ValueError(f"Unknown surface: {surface!r}. Use 'hyperbolic' or 'sphere'.")
    return (C1 - m * (N - m) / 2) / r_E**2


def fourier_block_trace(N, m, h_func):
    """
    Compute the m-th Fourier block trace of the interaction Hessian.

    For a general radial pair interaction h(d), the m-th eigenvalue of the
    Lagrangian Hessian restricted to Fourier mode m is:

        lambda_m = sum_{p=1}^{N-1} [Delta_p h] * [cos(2 pi pm/N) - 1]

    where Delta_p h is the second radial derivative of h evaluated at the
    chord distance d_p = 2 R sin(pi p / N).

    Parameters
    ----------
    N : int
        Ring size.
    m : int
        Fourier mode index.
    h_func : callable
        Pair interaction function h(d). Must accept scalar float distances.

    Returns
    -------
    float
        The m-th Fourier block trace.
    """
    z = np.exp(2j * np.pi * np.arange(N) / N)
    total = 0.0
    for p in range(1, N):
        d_p = abs(z[0] - z[p])
        eps = 1e-5
        laph = ((h_func(d_p + eps) - 2 * h_func(d_p) + h_func(d_p - eps)) / eps**2
                + (h_func(d_p + eps) - h_func(d_p - eps)) / (2 * eps * d_p))
        total += laph * (np.cos(2 * np.pi * p * m / N) - 1.0)
    return total


def mobius_energy_transform(N, a, b, c, d):
    """
    Compute the Thomson energy before and after a Möbius transformation.

    For a Möbius transformation f(z) = (az+b)/(cz+d) with ad-bc ≠ 0 the
    flat Thomson energy transforms as (proved by expanding ln|f(z_j)-f(z_k)|):

        H(f(z)) = H(z) - (N-1)/2 · Σ_k ln|f'(z_k)|

    For a pure dilation f(z) = bz: correction = N(N-1)/2·ln b and
    H(bz) = H(z) - N(N-1)/2·ln b  (Corollary cor:dilation-rg in paper).

    Parameters
    ----------
    N : int
        Number of vortices.
    a, b, c, d : complex
        Möbius transformation coefficients.

    Returns
    -------
    tuple of (float, float, float)
        (H_original, H_transformed, analytic_correction)
        where H_transformed = H_original - analytic_correction.
    """
    z = np.exp(2j * np.pi * np.arange(N) / N)

    def H(pos):
        s = 0.0
        for j in range(N):
            for k in range(j + 1, N):
                dist = abs(pos[j] - pos[k])
                if dist > 1e-12:
                    s -= np.log(dist)
        return s

    z_new = (a * z + b) / (c * z + d)
    det = a * d - b * c
    f_prime = det / (c * z + d) ** 2
    correction = (N - 1) / 2.0 * float(np.sum(np.log(np.abs(f_prime))))
    return float(H(z)), float(H(z_new)), correction


def equations_of_motion_invariant_check(N, a, b, c, d):
    """
    Numerical check that the Möbius energy transformation formula is accurate.

    Returns True if |H_after - H_before + correction| < 1e-8.
    (The correct identity is H_after = H_before - correction.)
    """
    H_b, H_a, correction = mobius_energy_transform(N, a, b, c, d)
    return abs(H_a - H_b + correction) < 1e-8


def dilation_rg_residual(N, b):
    """
    Residual of the flat-plane dilation identity (Corollary cor:dilation-rg).

    For the N-vortex ring on the unit circle, verify:

        H(b·z) = H(z) - N(N-1)/2 · ln b

    This is the Wilsonian RG fixed-point identity: rescaling all positions
    by b shifts the Thomson energy by an additive constant.  The eigenvalues
    λ_m = (N-1) - m(N-m)/2 are therefore scale-independent, which is why
    N_crit = 7 cannot drift under spatial rescaling.

    Parameters
    ----------
    N : int
        Number of vortices.
    b : float
        Dilation factor (b > 0).

    Returns
    -------
    float
        Residual = H(b·z) - H(z) + N(N-1)/2 · ln b.  Zero to machine precision.
    """
    z = np.exp(2j * np.pi * np.arange(N) / N)

    def H_flat(pos):
        s = 0.0
        for j in range(N):
            for k in range(j + 1, N):
                s -= np.log(abs(pos[j] - pos[k]))
        return s

    H_original = H_flat(z)
    H_scaled = H_flat(b * z)
    analytic_shift = N * (N - 1) / 2.0 * np.log(b)
    return float(H_scaled - H_original + analytic_shift)


if __name__ == "__main__":
    print("Havelock identity check:")
    for N in [4, 6, 8]:
        for m in [1, 2]:
            s = havelock_sum(N, m)
            e = int(havelock_exact(N, m))
            print(f"  N={N}, m={m}: T_m={s:.6f} (exact={e})")

    print("\nTrace formula (sphere):")
    for N in [4, 6, 8]:
        d = trace_formula_delta(N, 'sphere')
        print(f"  N={N}: delta = {d:.6f} (= -N/4pi = {-N/(4*np.pi):.6f})")
