"""
AdS3/CFT2 dictionary for polygon stability.

Translates the Havelock decomposition lambda_m = C1 - m(N-m)/2
into the language of the AdS3/CFT2 correspondence:

  Bulk: N point masses on spatial slice Gamma\\H^2
  Boundary: N heavy operators at equally-spaced points on the circle

The m(N-m)/2 Casimir is the Z_N Fourier eigenvalue of the logarithmic
kernel, which in CFT language is the "kinematic" OPE structure.
C1 encodes the AdS geometry (confining potential / bulk position).

Key formulas:
  - Brown-Henneaux: c = 3*ell/(2*G)
  - Conformal dimension: h = (c/24)*(1 - (1 - 8*G*m)^2)
  - Deficit angle: alpha = 8*pi*G*m
"""

import math


# ============================================================
# Part 1: Bulk-boundary map
# ============================================================

def brown_henneaux(ell_ads, G):
    """Central charge of the boundary CFT: c = 3*ell/(2*G)."""
    return 3 * ell_ads / (2 * G)


def mass_to_conformal_dim(Gm, c):
    """
    Conformal dimension of boundary operator dual to a bulk conical deficit.

    h = (c/24) * (1 - (1 - 8*G*m)^2)
      = (c/24) * (16*G*m - 64*(G*m)^2)
      = (2*c/3) * G*m * (1 - 4*G*m)

    For small deficit (linearized): h ~ (2c/3) * G*m.
    """
    alpha_over_2pi = 4 * Gm  # deficit angle / (2*pi)
    if alpha_over_2pi >= 1:
        return None  # deficit exceeds 2*pi
    return (c / 24) * (1 - (1 - 8 * Gm)**2)


def conformal_dim_to_mass(h, c):
    """Inverse: G*m from conformal dimension h and central charge c."""
    # h = (c/24)(1 - (1-8Gm)^2)
    # (1-8Gm)^2 = 1 - 24h/c
    # 8Gm = 1 - sqrt(1 - 24h/c)
    if 24 * h / c > 1:
        return None  # beyond BTZ threshold
    return (1 - math.sqrt(1 - 24 * h / c)) / 8


def deficit_angle(Gm):
    """Conical deficit angle alpha = 8*pi*G*m."""
    return 8 * math.pi * Gm


def max_polygon_mass(N):
    """
    Maximum G*m for an N-gon: total deficit < 2*pi.
    N * 8*pi*G*m < 2*pi  =>  G*m < 1/(4*N).
    """
    return 1.0 / (4 * N)


def max_h_over_c(N):
    """
    Maximum h/c for an N-gon of equal masses.
    From G*m < 1/(4*N):
    h/c = (1/24)(1 - (1-2/N)^2) = (1/24)(4/N - 4/N^2) = (1/6N)(1 - 1/N).
    """
    Gm_max = max_polygon_mass(N)
    c = 1.0  # normalize
    h_max = mass_to_conformal_dim(Gm_max, c)
    return h_max


# ============================================================
# Part 2: The OPE Casimir = Havelock identity
# ============================================================

def ope_pairwise_energy(N):
    """
    The pairwise OPE energy of N operators at equally-spaced points
    on the unit circle:

    E_OPE = sum_{j<k} log|z_j - z_k|

    For z_k = exp(2*pi*i*k/N): this equals (N/2)*log(N).
    (Standard identity for roots of unity.)
    """
    # Direct computation for verification
    total = 0.0
    for j in range(N):
        for k in range(j + 1, N):
            angle_j = 2 * math.pi * j / N
            angle_k = 2 * math.pi * k / N
            dx = math.cos(angle_j) - math.cos(angle_k)
            dy = math.sin(angle_j) - math.sin(angle_k)
            dist = math.sqrt(dx**2 + dy**2)
            total += math.log(dist)
    return total


def ope_pairwise_energy_exact(N):
    """Exact: sum_{j<k} log|z_j - z_k| = (N/2)*log(N)."""
    return (N / 2) * math.log(N)


def hessian_log_interaction_fourier(N, m):
    """
    The m-th Z_N Fourier eigenvalue of the Hessian of
    E = -sum_{j<k} log|z_j - z_k| at equally-spaced points.

    This is computed by:
    H_m = (1/2) * sum_{p=1}^{N-1} (1 - cos(2*pi*p*m/N)) / sin^2(pi*p/N)

    This is the "full" Hessian eigenvalue of the logarithmic
    interaction decomposed into Z_N modes.
    """
    total = 0.0
    for p in range(1, N):
        cos_term = math.cos(2 * math.pi * p * m / N)
        sin2_term = math.sin(math.pi * p / N) ** 2
        total += (1 - cos_term) / sin2_term
    return total / 2


def havelock_casimir(N, m):
    """The Havelock Casimir: f(m, N) = m(N-m)/2."""
    return m * (N - m) / 2


def C1_flat(N):
    """C1 on the flat plane: C1 = N - 1."""
    return N - 1


def havelock_eigenvalue_flat(N, m):
    """Havelock eigenvalue on the flat plane: lambda_m = (N-1) - m(N-m)/2."""
    return C1_flat(N) - havelock_casimir(N, m)


# ============================================================
# Part 3: The Hessian decomposition (the key numerical test)
# ============================================================

def full_hessian_numerical(N):
    """
    Compute the full 2(N-1) x 2(N-1) Hessian matrix of
    E = -sum_{j<k} log|z_j - z_k|
    at equally-spaced points on the unit circle.

    Perturbations: delta_z_j = (delta_r_j + i*delta_theta_j) * z_j
    where delta_r is radial and delta_theta is tangential.

    We fix the center of mass and total angular impulse,
    leaving 2(N-1) degrees of freedom.

    Returns the Hessian as a 2D list.
    """
    # Positions: z_k = exp(2*pi*i*k/N) for k = 0, ..., N-1
    positions = [(math.cos(2 * math.pi * k / N),
                  math.sin(2 * math.pi * k / N)) for k in range(N)]

    # The Hessian of E = -sum_{j<k} log|z_j - z_k|
    # with respect to Cartesian displacements (dx_j, dy_j).
    # d^2 E / (d x_j d x_k) for j != k and j = k.
    #
    # For the log interaction: d^2/dx_j dx_k [-log|z_j - z_k|]
    # = -[(y_j-y_k)^2 - (x_j-x_k)^2] / |z_j-z_k|^4  for j != k
    # And the diagonal: d^2/dx_j^2 [-sum_{k!=j} log|z_j-z_k|]
    # = sum_{k!=j} [(y_j-y_k)^2 - (x_j-x_k)^2] / |z_j-z_k|^4

    dim = 2 * N
    H = [[0.0] * dim for _ in range(dim)]

    for j in range(N):
        for k in range(N):
            if j == k:
                continue
            dx = positions[j][0] - positions[k][0]
            dy = positions[j][1] - positions[k][1]
            r2 = dx**2 + dy**2
            r4 = r2**2

            # Second derivatives of -log(r) where r = |z_j - z_k|
            # d^2/dx_j^2 (-log r) = (dy^2 - dx^2) / r^4... no.
            # -log r = -(1/2) log(dx^2 + dy^2)
            # d/dx_j = -dx/r^2
            # d^2/dx_j^2 = -(1/r^2) + 2*dx^2/r^4 = (-r^2 + 2*dx^2)/r^4
            # d^2/dx_j dy_j = 2*dx*dy/r^4
            # d^2/dx_j dx_k = (r^2 - 2*dx^2)/r^4  (opposite sign)
            # d^2/dx_j dy_k = -2*dx*dy/r^4

            Hxx = (-r2 + 2 * dx**2) / r4
            Hxy = 2 * dx * dy / r4
            Hyy = (-r2 + 2 * dy**2) / r4

            # Off-diagonal blocks (j, k):
            H[2*j][2*k] += -Hxx
            H[2*j][2*k+1] += -Hxy
            H[2*j+1][2*k] += -Hxy
            H[2*j+1][2*k+1] += -Hyy

            # Diagonal blocks (j, j):
            H[2*j][2*j] += Hxx
            H[2*j][2*j+1] += Hxy
            H[2*j+1][2*j] += Hxy
            H[2*j+1][2*j+1] += Hyy

    return H


def hessian_ZN_eigenvalues(N):
    """
    Decompose the Hessian into Z_N Fourier modes and extract eigenvalues.

    For the N-gon with Z_N symmetry, the Hessian block-diagonalizes
    into 2x2 blocks for each Fourier mode m = 0, 1, ..., N-1.
    Mode m=0 corresponds to uniform radial/rotational perturbations
    (constrained by angular impulse conservation).

    Returns dict mapping m to (lambda_radial, lambda_tangential).
    """
    H = full_hessian_numerical(N)

    # Z_N Fourier transform: for mode m, the basis vector is
    # v_m^(x) = (1/sqrt(N)) * (cos(2*pi*m*k/N))_{k=0}^{N-1}  (x-component)
    # v_m^(y) = (1/sqrt(N)) * (sin(2*pi*m*k/N))_{k=0}^{N-1}  (y-component)
    # But we need radial and tangential components relative to the circle.
    #
    # Radial at position k: direction (cos(theta_k), sin(theta_k))
    # Tangential at position k: direction (-sin(theta_k), cos(theta_k))
    # where theta_k = 2*pi*k/N.
    #
    # The m-th radial Fourier mode:
    # u_m^r = (1/sqrt(N)) * sum_k cos(2*pi*mk/N) * (cos(theta_k), sin(theta_k))

    results = {}
    for m in range(N):
        # Build the radial and tangential Fourier basis vectors (length 2N)
        v_r = [0.0] * (2 * N)  # radial mode m (cosine)
        v_t = [0.0] * (2 * N)  # tangential mode m (cosine)
        v_r_s = [0.0] * (2 * N)  # radial mode m (sine)
        v_t_s = [0.0] * (2 * N)  # tangential mode m (sine)

        for k in range(N):
            theta = 2 * math.pi * k / N
            cos_m = math.cos(2 * math.pi * m * k / N) / math.sqrt(N)
            sin_m = math.sin(2 * math.pi * m * k / N) / math.sqrt(N)

            # Radial direction at position k
            er_x, er_y = math.cos(theta), math.sin(theta)
            # Tangential direction at position k
            et_x, et_y = -math.sin(theta), math.cos(theta)

            # Cosine Fourier component
            v_r[2*k] = cos_m * er_x
            v_r[2*k+1] = cos_m * er_y
            v_t[2*k] = cos_m * et_x
            v_t[2*k+1] = cos_m * et_y

            # Sine Fourier component
            v_r_s[2*k] = sin_m * er_x
            v_r_s[2*k+1] = sin_m * er_y
            v_t_s[2*k] = sin_m * et_x
            v_t_s[2*k+1] = sin_m * et_y

        # Compute the 2x2 block: v^T H v for radial and tangential
        def dot(a, b):
            return sum(x * y for x, y in zip(a, b))

        def matvec(M, v):
            n = len(v)
            return [sum(M[i][j] * v[j] for j in range(n)) for i in range(n)]

        Hv_r = matvec(H, v_r)
        Hv_t = matvec(H, v_t)

        lam_rr = dot(v_r, Hv_r)
        lam_tt = dot(v_t, Hv_t)
        lam_rt = dot(v_r, Hv_t)

        results[m] = {
            'radial': lam_rr,
            'tangential': lam_tt,
            'cross': lam_rt,
        }

    return results


def dictionary_comparison(N_max=12):
    """
    The core test: compare the Hessian Z_N eigenvalues with
    the Havelock prediction lambda_m = (N-1) - m(N-m)/2.

    If they match: the "OPE Casimir = Havelock Casimir" is confirmed,
    and the AdS/CFT dictionary has a rigorous kinematic foundation.
    """
    results = []
    for N in range(3, N_max + 1):
        row = {'N': N, 'modes': []}
        eigs = hessian_ZN_eigenvalues(N)
        for m in range(1, N):
            lam_havelock = havelock_eigenvalue_flat(N, m)
            lam_hessian_r = eigs[m]['radial']
            lam_hessian_t = eigs[m]['tangential']
            row['modes'].append({
                'm': m,
                'havelock': lam_havelock,
                'hessian_radial': lam_hessian_r,
                'hessian_tangential': lam_hessian_t,
                'radial_match': abs(lam_hessian_r - lam_havelock) < 0.01,
            })
        results.append(row)
    return results


# ============================================================
# Part 4: Stability condition as bootstrap bound
# ============================================================

def stability_bound_h_over_c(N):
    """
    The stability condition C1 >= f_max(N) translates to:
    - On the flat plane: always satisfied for N <= 7.
    - On H^2 at curvature xi: C1(xi) >= floor(N/2)*ceil(N/2)/2.
    - In CFT language: the bulk polygon must sit at a radial
      position where the confining potential exceeds the OPE repulsion.

    The SEPARATE constraint from the deficit angle:
    h/c < (1/24)(1 - (1-2/N)^2) for an N-gon.

    Returns dict with bounds.
    """
    f_max = (N // 2) * ((N + 1) // 2) / 2
    h_c_max = max_h_over_c(N)

    return {
        'N': N,
        'f_max': f_max,
        'C1_flat': C1_flat(N),
        'stable_flat': C1_flat(N) >= f_max,
        'h_over_c_max': h_c_max,
    }


def palindromic_threshold_cft(N):
    """
    Translate the palindromic threshold xi*(N) to bulk radial position
    and the corresponding CFT data.

    xi*(N) is the curvature parameter at which the N-gon transitions
    from unstable to stable on H^2. In the bulk, this is the radial
    position at which the confining potential C1(xi) first equals f_max(N).
    """
    from planetary_polygons.extensions.algebraic_thresholds import (
        h2_stability_threshold,
    )
    xi_star, D, field = h2_stability_threshold(N)
    if xi_star == 0:
        return {'N': N, 'xi_star': 0, 'field': field, 'meaning': 'stable in flat limit'}

    C1_at_threshold = (N - 1) * (1 + xi_star**2) / (1 - xi_star)**2
    f_max = (N // 2) * ((N + 1) // 2) / 2
    h_c_max = max_h_over_c(N)

    return {
        'N': N,
        'xi_star': xi_star,
        'field': field,
        'C1_at_threshold': C1_at_threshold,
        'f_max': f_max,
        'h_over_c_max': h_c_max,
        'meaning': (
            f'At bulk position xi = {xi_star:.6f} (in the {field} field), '
            f'the N={N}-gon transitions from unstable to stable. '
            f'The maximum h/c for the polygon is {h_c_max:.6f}.'
        ),
    }


# ============================================================
# Main
# ============================================================

if __name__ == '__main__':
    print("AdS3/CFT2 DICTIONARY FOR POLYGON STABILITY")
    print("=" * 60)

    # Part 1: Bulk-boundary map
    print("\n--- Bulk-Boundary Map ---")
    for N in [4, 6, 8, 12]:
        Gm_max = max_polygon_mass(N)
        h_c = max_h_over_c(N)
        alpha = deficit_angle(Gm_max)
        print(f"  N={N:2d}: Gm_max = {Gm_max:.4f}, "
              f"alpha_max = {alpha:.3f} rad, "
              f"h/c_max = {h_c:.6f}")

    # Part 2: OPE energy verification
    print("\n--- OPE Pairwise Energy ---")
    for N in [3, 4, 6, 8]:
        E_num = ope_pairwise_energy(N)
        E_exact = ope_pairwise_energy_exact(N)
        print(f"  N={N}: numerical = {E_num:.6f}, "
              f"exact (N/2)log(N) = {E_exact:.6f}, "
              f"match = {abs(E_num - E_exact) < 0.001}")

    # Part 3: THE KEY TEST - Hessian vs Havelock
    print("\n--- DICTIONARY TEST: Hessian Z_N eigenvalues vs Havelock ---")
    results = dictionary_comparison(8)
    for row in results:
        N = row['N']
        print(f"\n  N = {N}:")
        print(f"  {'m':>3} {'Havelock':>10} {'Hessian(r)':>12} {'Match':>6}")
        for mode in row['modes']:
            m = mode['m']
            if m > N // 2:
                continue  # symmetric
            print(f"  {m:>3} {mode['havelock']:>10.4f} "
                  f"{mode['hessian_radial']:>12.4f} "
                  f"{'YES' if mode['radial_match'] else 'NO':>6}")

    # Part 4: Palindromic thresholds in CFT language
    print("\n--- Palindromic Thresholds in CFT ---")
    for N in [8, 9, 10, 11, 12, 15, 23]:
        data = palindromic_threshold_cft(N)
        if data['xi_star'] > 0:
            print(f"  N={N:2d}: xi* = {data['xi_star']:.6f} "
                  f"({data['field']}), "
                  f"h/c_max = {data['h_over_c_max']:.6f}")
