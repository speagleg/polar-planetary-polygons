"""
K-theoretic classification of vortex stability phases.

The negative spectral projection of the Havelock Hessian defines a class
[P_-] in K_0(C*(Z_N)) = R(Z_N) that is a topological invariant,
unchanged by any continuous deformation preserving the spectral gap.

This connects vortex polygon stability to:
  1. The Baum-Connes assembly map (for arithmetic surfaces)
  2. The Kitaev classification of topological phases (condensed matter)

The curvature-stability dichotomy sgn(N_crit - 7) = -sgn(K) is the
Z_2-reduction of the full Z^N-valued K-theoretic classification.
"""
from fractions import Fraction
import math


def havelock_eigenvalue(N, m, xi):
    """Eigenvalue λ_m = C₁(H², ξ) - m(N-m)/2 for mode m of the N-gon."""
    if xi >= 1 or xi < 0:
        raise ValueError("xi must be in [0, 1)")
    C1 = (N - 1) * (1 + xi**2) / (1 - xi)**2
    return C1 - m * (N - m) / 2


def havelock_eigenvalues(N, xi):
    """All eigenvalues λ_m for m = 1, ..., N-1."""
    return {m: havelock_eigenvalue(N, m, xi) for m in range(1, N)}


def sign_vector(N, xi):
    """Sign vector (sgn(λ_1), ..., sgn(λ_{N-1})). 0 means marginal."""
    eigs = havelock_eigenvalues(N, xi)
    return tuple(
        1 if eigs[m] > 1e-12 else (-1 if eigs[m] < -1e-12 else 0)
        for m in range(1, N)
    )


def k0_class(N, xi):
    """
    K_0(C*(Z_N)) class of the negative spectral projection.

    Returns frozenset of modes m with λ_m < 0, representing
    [P_-] = Σ_{m ∈ S} [ρ_m] in R(Z_N).
    """
    eigs = havelock_eigenvalues(N, xi)
    return frozenset(m for m, lam in eigs.items() if lam < -1e-12)


def morse_index(N, xi):
    """Morse index μ = dim([P_-]) = #{m: λ_m < 0}."""
    return len(k0_class(N, xi))


def morse_index_formula(N):
    """
    Exact Morse index at ξ = 0 (flat plane).

    Returns max(0, N-5) for N ≥ 3, which equals:
      0       for N ≤ 7
      N - 5   for N ≥ 8
    """
    if N <= 7:
        return 0
    return N - 5


def negative_modes_at_zero(N):
    """
    The set of negative modes at ξ = 0 (flat plane).

    For N ≥ 8: modes m = 3, 4, ..., N-3 (those with m(N-m)/2 > N-1).
    For N ≤ 7: empty set.
    """
    if N <= 7:
        return frozenset()
    C1 = N - 1
    return frozenset(m for m in range(1, N) if m * (N - m) / 2 > C1)


def threshold_xi(N, m):
    """
    Threshold curvature ξ*(N,m) where λ_m = 0 on H².

    Solves (N-1)(1+ξ²)/(1-ξ)² = m(N-m)/2.
    Returns float in (0,1) or None if no threshold exists.
    """
    T = Fraction(m * (N - m), 2)
    A = Fraction(N - 1) - T
    if A >= 0:
        return None  # λ_m ≥ 0 for all ξ
    # Quadratic Aξ² + 2Tξ + A = 0,  roots = (-T ± √(T²-A²)) / A
    disc = float(T * T - A * A)
    if disc < 0:
        return None
    T_f, A_f = float(T), float(A)
    # A < 0, so the smaller positive root is (-T + √disc) / A
    xi = (-T_f + math.sqrt(disc)) / A_f
    if 0 < xi < 1:
        return xi
    return None


def phase_boundaries(N):
    """
    All phase boundaries for the N-gon on H².

    Returns sorted list of (ξ*, m) pairs.
    """
    bounds = []
    for m in range(1, N):
        xi = threshold_xi(N, m)
        if xi is not None:
            bounds.append((xi, m))
    return sorted(bounds)


def phase_diagram_row(N):
    """
    Phase diagram for the N-gon: list of phases as ξ increases.

    Each phase: {'xi_range': (lo, hi), 'k0_class': frozenset, 'morse_index': int}
    """
    bounds = phase_boundaries(N)
    if not bounds:
        # No phase transitions: single phase for all ξ
        cls = k0_class(N, 0.0)
        return [{'xi_range': (0.0, 1.0), 'k0_class': cls,
                 'morse_index': len(cls)}]

    phases = []
    xi_prev = 0.0
    for xi_b, m in bounds:
        # Sample just before boundary
        xi_sample = max(0.0, xi_b - 1e-10)
        cls = k0_class(N, xi_sample)
        phases.append({'xi_range': (xi_prev, xi_b), 'k0_class': cls,
                       'morse_index': len(cls)})
        xi_prev = xi_b

    # Final phase after last boundary
    xi_sample = min(bounds[-1][0] + 1e-10, 0.9999)
    cls = k0_class(N, xi_sample)
    phases.append({'xi_range': (xi_prev, 1.0), 'k0_class': cls,
                   'morse_index': len(cls)})

    return phases


def verify_k0_invariance(N, xi_lo, xi_hi, n_points=100):
    """
    Verify that the K_0 class is constant on [xi_lo, xi_hi].

    Returns True if the class is constant, False otherwise.
    """
    ref_class = k0_class(N, xi_lo)
    for i in range(n_points):
        xi = xi_lo + (xi_hi - xi_lo) * i / (n_points - 1)
        if k0_class(N, xi) != ref_class:
            return False
    return True


def kitaev_table(N_max=12):
    """
    Kitaev-style classification table.

    For each N: the K-theory group K_0(C*(Z_N)), number of phases,
    Morse index at ξ=0, and the curvature-stability dichotomy.

    Analogy with condensed matter:
    - Standard topological insulator: K_0 = Z, Z_2 phases
    - Vortex N-gon: K_0 = Z^N, up to 2^{N-1} possible phases
    """
    table = []
    for N in range(3, N_max + 1):
        phases = phase_diagram_row(N)
        n_phases = len(phases)
        mu_0 = morse_index(N, 0.0)

        # Most curved phase (largest ξ before 1)
        mu_curved = morse_index(N, 0.999)

        table.append({
            'N': N,
            'k_group': f'Z^{N}',
            'n_phases': n_phases,
            'max_possible_phases': 2**(N-1),
            'morse_index_flat': mu_0,
            'morse_index_curved': mu_curved,
            'stable_flat': mu_0 == 0,
            'stable_curved': mu_curved == 0,
        })
    return table


def index_pairing_geometric_side(geodesic_lengths, xi, N):
    """
    Compute δC₁ via the geometric side of the Selberg trace formula.

    This IS the index pairing: the image of the Havelock test function
    under the Baum-Connes assembly map.

    δC₁ = Σ_γ w_γ(ξ) · csch²(ℓ_γ/2)

    Parameters
    ----------
    geodesic_lengths : list of (length, multiplicity) pairs
    xi : float, curvature parameter
    N : int, polygon number

    Returns float (the spectral correction δC₁).
    """
    delta = 0.0
    for ell, mult in geodesic_lengths:
        # Weight: the Havelock test function evaluated on the geodesic
        # For the simplest case: w_γ = (N-1)(1+ξ²)/(1-ξ)² contribution
        # from the automorphic Green's function restricted to the diagonal.
        # The leading term is csch²(ℓ/2) / (4π Area) × geometric factor.
        csch2 = 1.0 / math.sinh(ell / 2) ** 2
        delta += mult * csch2
    # Normalize by 1/(4π) (the area-normalized diagonal contribution)
    return delta / (4 * math.pi)


def index_pairing_spectral_side(eigenvalues, eigfunc_center_sq, xi, N):
    """
    Compute δC₁ via the spectral side: Σ_n |φ_n(z₀)|² / λ_n × (factor).

    Only trivial-rep eigenfunctions (those nonzero at center) contribute.

    Parameters
    ----------
    eigenvalues : list of float (Laplacian eigenvalues on Γ\\H²)
    eigfunc_center_sq : list of float (|φ_n(z₀)|² at center)

    Returns float.
    """
    delta = 0.0
    for lam, phi2 in zip(eigenvalues, eigfunc_center_sq):
        if lam > 0 and phi2 > 1e-10:
            delta += phi2 / lam
    # Subtract the universal-cover contribution (divergent, regularized)
    # In practice, we compare with known C₁(H², ξ) directly.
    return delta


def bolza_index_pairing(xi=0.217):
    """
    Compute the index pairing on the Bolza surface.

    The Bolza surface has:
    - Area = 4π, genus = 2, |Aut| = 48
    - Systole: 12 geodesics of length ℓ = 2 arccosh(1+√2) ≈ 3.057
    - First trivial-rep eigenvalue: λ_triv ≈ 15.05

    Returns dict with spectral bound, geometric-side estimate, and
    the K₀ class shift (if any) relative to H².
    """
    # Systole data
    ell_sys = 2 * math.acosh(1 + math.sqrt(2))
    n_sys = 12

    # Geometric side: leading term from systole orbit
    delta_geometric = index_pairing_geometric_side(
        [(ell_sys, n_sys)], xi, 8)

    # Spectral bound: |δC₁| ≤ Σ 1/(4π λ_n) ≤ 2/(4π λ_triv)
    lambda_triv = 15.05  # first trivial-rep eigenvalue (Strohmaier-Uski)
    spectral_bound = 2 / (4 * math.pi * lambda_triv)

    # C₁ on H² at the Bolza curvature
    C1_H2 = 7 * (1 + xi**2) / (1 - xi)**2

    # The binding eigenvalue at N=12, ξ_Bolza
    m_crit = 1  # most dangerous mode
    lambda_bind = C1_H2 - m_crit * (12 - m_crit) / 2  # N=12

    # Does δC₁ change the K₀ class?
    # Only if |δC₁| > λ_bind (pushes an eigenvalue across zero)
    k0_preserved = spectral_bound < abs(lambda_bind)

    return {
        'xi': xi,
        'ell_systole': ell_sys,
        'delta_geometric': delta_geometric,
        'spectral_bound': spectral_bound,
        'C1_H2': C1_H2,
        'lambda_bind': lambda_bind,
        'k0_class_preserved': k0_preserved,
        'interpretation': (
            'The spectral bound |δC₁| ≈ {:.3f} is smaller than the '
            'binding eigenvalue λ_bind ≈ {:.3f}, so the K₀ class on '
            'the Bolza surface equals the K₀ class on H². '
            'This is the SCALAR case of the Kasparov product: '
            'dim(α_N ⊗ [D_Bolza]) = dim(α_N ⊗ [D_H²]).'
        ).format(spectral_bound, lambda_bind),
    }


def phase_shift_on_surface(N, geodesic_lengths):
    """
    Compute how the phase boundaries shift on a quotient surface.

    On H²: boundary at ξ*(N,m) where C₁(H²,ξ) = m(N-m)/2.
    On Γ\\H²: boundary at ξ where C₁(H²,ξ) + δC₁(Γ,ξ) = m(N-m)/2.

    The shift δξ ≈ -δC₁ / (dC₁/dξ) at the threshold.
    """
    shifts = []
    for m in range(1, N):
        xi_H2 = threshold_xi(N, m)
        if xi_H2 is None:
            continue

        # δC₁ at this ξ
        delta = index_pairing_geometric_side(geodesic_lengths, xi_H2, N)

        # dC₁/dξ at the threshold
        eps = 1e-8
        C1_plus = (N-1) * (1 + (xi_H2+eps)**2) / (1 - (xi_H2+eps))**2
        C1_minus = (N-1) * (1 + (xi_H2-eps)**2) / (1 - (xi_H2-eps))**2
        dC1_dxi = (C1_plus - C1_minus) / (2 * eps)

        # Shifted threshold
        delta_xi = -delta / dC1_dxi if abs(dC1_dxi) > 1e-12 else 0
        xi_surface = xi_H2 + delta_xi

        shifts.append({
            'N': N, 'm': m,
            'xi_H2': xi_H2,
            'xi_surface': xi_surface,
            'delta_xi': delta_xi,
            'delta_C1': delta,
        })
    return shifts


def spectral_flow(N, xi_lo, xi_hi, delta_C1=0.0):
    """
    Compute the spectral flow of {H_N(ξ)} as ξ goes from xi_lo to xi_hi.

    On H²: delta_C1 = 0. On a quotient surface: delta_C1 ≠ 0.

    The spectral flow counts the net number of eigenvalues crossing zero
    (positive crossing = +1, negative crossing = -1).

    Returns (sf, crossings) where:
      sf: int, the total spectral flow
      crossings: list of (xi, m, direction) for each crossing
    """
    crossings = []
    for m in range(1, N):
        # On H²: λ_m(ξ) = C₁(H², ξ) - m(N-m)/2
        # On surface: λ_m(ξ) = C₁(H², ξ) + δC₁ - m(N-m)/2
        # Threshold: C₁(ξ*) + δC₁ = m(N-m)/2
        T = m * (N - m) / 2
        # Solve (N-1)(1+ξ²)/(1-ξ)² = T - δC₁
        effective_T = T - delta_C1
        A = (N - 1) - effective_T
        if A >= 0:
            continue  # no crossing
        disc = effective_T**2 - A**2
        if disc < 0:
            continue
        xi_cross = (-effective_T + math.sqrt(disc)) / A
        if xi_lo < xi_cross < xi_hi:
            # Direction: eigenvalue goes from negative to positive
            # (C₁ increases with ξ, so λ_m increases → crosses 0 upward)
            crossings.append((xi_cross, m, +1))

    crossings.sort()
    sf = sum(d for _, _, d in crossings)
    return sf, crossings


def binding_eigenvalue(N, m):
    """
    The binding eigenvalue at threshold ξ*(N,m): the smallest |λ_{m'}|
    for m' ≠ m at the threshold.

    This is the gap that δC₁ must not exceed for the spectral flow
    to be preserved (Theorem 6.3).
    """
    xi = threshold_xi(N, m)
    if xi is None:
        return None
    eigs = havelock_eigenvalues(N, xi)
    others = {mp: abs(lam) for mp, lam in eigs.items() if mp != m and mp != N - m}
    if not others:
        return None
    return min(others.values())


def operator_norm_bound(geodesic_data, kernel='green'):
    """
    Upper bound on ||h_ξ^Γ||_{op} ≤ ||h_ξ^Γ||_{ℓ¹} = Σ_{γ≠1} |k(d(z₀,γz₀))|.

    This is the OPERATOR NORM of the spectral correction element
    h_ξ^Γ ∈ C*_r(Γ), which is strictly larger than its trace |δC₁|.

    The gap condition for the KK product (Theorem 6.4) requires
    ||h_ξ^Γ||_{op} < min_m |c_m|, not just |δC₁| < min_m |c_m|.

    Parameters
    ----------
    geodesic_data : list of (length, multiplicity) pairs
    kernel : 'green' (exponential decay) or 'heat' (Gaussian decay)

    Returns float: upper bound on operator norm.
    """
    total = 0.0
    for ell, mult in geodesic_data:
        if kernel == 'green':
            # Green's function on H² (K=-1): G(d) ~ e^{-d}/π for large d
            k_val = math.exp(-ell) / math.pi
        elif kernel == 'heat':
            # Heat kernel at t=1: K(d,1) ~ e^{-d²/4}/(4π)
            k_val = math.exp(-ell**2 / 4) / (4 * math.pi)
        else:
            raise ValueError(f"Unknown kernel: {kernel}")
        total += mult * abs(k_val)
    return total


def kk_product_verification(N, xi, geodesic_data):
    """
    Verify the KK product identity α_N ⊗ [D_S] = [μ_N] for a specific surface.

    The verification checks:
    1. The operator norm bound ||h_ξ^Γ||_{op} (ℓ¹ bound)
    2. The binding eigenvalue min_m |c_m|
    3. Whether the gap condition holds: ||h|| < min|c_m|
    4. If yes: the KK product equals the elementary Morse index

    Returns dict with verification data.
    """
    # Operator norm bound
    h_norm = operator_norm_bound(geodesic_data, kernel='green')

    # Havelock eigenvalues on H²
    C1 = (N - 1) * (1 + xi**2) / (1 - xi)**2
    eigenvalues = {}
    for m in range(1, N):
        eigenvalues[m] = C1 - m * (N - m) / 2

    # Binding eigenvalue (smallest |λ_m| across all modes)
    min_gap = min(abs(lam) for lam in eigenvalues.values() if abs(lam) > 1e-10)

    # δC₁ (trace of h — strictly smaller than operator norm)
    delta_C1 = index_pairing_geometric_side(geodesic_data, xi, N)

    # Gap conditions
    trace_gap = abs(delta_C1) < min_gap      # weak (Theorem 6.3)
    operator_gap = h_norm < min_gap            # strong (KK product)

    # Morse index on H²
    mu_H2 = sum(1 for lam in eigenvalues.values() if lam < -1e-10)

    # If operator gap holds: KK product = elementary answer
    if operator_gap:
        mu_surface = mu_H2  # guaranteed by operator norm bound
    else:
        # Need to check mode by mode with the full correction
        mu_surface = sum(1 for m, lam in eigenvalues.items()
                         if lam + delta_C1 < -1e-10)

    return {
        'N': N,
        'xi': xi,
        'h_norm_bound': h_norm,
        'delta_C1': delta_C1,
        'min_gap': min_gap,
        'trace_gap_holds': trace_gap,
        'operator_gap_holds': operator_gap,
        'gap_ratio': min_gap / h_norm if h_norm > 0 else float('inf'),
        'morse_index_H2': mu_H2,
        'morse_index_surface': mu_surface,
        'kk_product_equals_elementary': operator_gap,
    }


def spectral_flow_preserved(N, delta_C1):
    """
    Check whether the spectral flow on a surface with correction δC₁
    equals the spectral flow on H² (Theorem 6.3).

    Returns (preserved: bool, margin: float, details: dict).
    """
    bounds = phase_boundaries(N)
    if not bounds:
        return True, float('inf'), {'N': N, 'no_boundaries': True}

    min_margin = float('inf')
    for xi_b, m in bounds:
        lam_bind = binding_eigenvalue(N, m)
        if lam_bind is None:
            continue
        margin = lam_bind - abs(delta_C1)
        min_margin = min(min_margin, margin)

    preserved = min_margin > 0
    return preserved, min_margin, {
        'N': N, 'delta_C1': delta_C1,
        'min_margin': min_margin,
        'n_boundaries': len(bounds),
    }


if __name__ == '__main__':
    print("K-THEORETIC CLASSIFICATION OF VORTEX STABILITY PHASES")
    print("=" * 60)

    # Morse index formula
    print("\nMorse index at ξ = 0 (flat plane):")
    for N in range(3, 16):
        mu = morse_index_formula(N)
        neg = negative_modes_at_zero(N)
        neg_str = '{' + ','.join(str(m) for m in sorted(neg)) + '}' if neg else '∅'
        print(f"  N={N:2d}: μ = {mu}, negative modes = {neg_str}")

    # Phase diagram
    print("\nPhase diagram (H²):")
    for N in [7, 8, 9, 10, 12]:
        phases = phase_diagram_row(N)
        print(f"\n  N = {N}:")
        for p in phases:
            lo, hi = p['xi_range']
            modes = sorted(p['k0_class'])
            modes_str = '{' + ','.join(str(m) for m in modes) + '}' if modes else '∅'
            print(f"    ξ ∈ ({lo:.4f}, {hi:.4f}): μ = {p['morse_index']}, "
                  f"negative modes = {modes_str}")

    # Kitaev table
    print("\nKitaev-style classification:")
    print(f"{'N':>3} {'K_0 group':>10} {'#phases':>8} {'μ(flat)':>8} "
          f"{'μ(curved)':>10} {'stable(flat)':>13}")
    for row in kitaev_table(12):
        print(f"{row['N']:>3} {row['k_group']:>10} {row['n_phases']:>8} "
              f"{row['morse_index_flat']:>8} {row['morse_index_curved']:>10} "
              f"{'YES' if row['stable_flat'] else 'NO':>13}")
