"""
Script 2: Cat's-eye Hessian eigenvalue analysis for the Rossby bridge.

Computes the energy-Casimir Hessian eigenvalues for cat's-eye vorticity
distributions and compares them to the point vortex Havelock eigenvalues.

Two models are tested:
  1. Stuart vortex (smooth): omega = (1-eps^2)/sigma^2 / (cosh(y/sigma) - eps*cos(n*theta))^2
  2. Prandtl-Batchelor (step PV): q = q_trap inside separatrix, q = q_bg(y) outside

For each model, the Hessian of E[omega] + mu*L[omega] is computed on the
2N-dimensional center-translation subspace and its eigenvalues compared
to the Havelock spectrum.

The key question: do the Hessian eigenvalues have the same signs as the
Havelock eigenvalues? If yes, the bridge closes for that model class.

Mathematical framework:
  E[omega] = (1/2) integral integral omega(x) G(x,y) omega(y) dx dy
  L[omega] = integral |x|^2 omega(x) dx  (angular impulse)

  For a Z_N-symmetric configuration, the Hessian restricted to
  center translations has 2N eigenvalues.  Prop 8 (inertia preservation)
  says these should match the Havelock eigenvalues for concentrated patches.

All computations use numpy only (no scipy required).
"""
import numpy as np


# ---------------------------------------------------------------------------
# Green's function and energy computation
# ---------------------------------------------------------------------------

def log_greens_function(x1, y1, x2, y2):
    """G(r1, r2) = -(1/2pi) ln|r1 - r2| for 2D log interaction."""
    d = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return -np.log(d + 1e-30) / (2.0 * np.pi)


def pairwise_energy_grid(omega, y_grid, x_grid):
    """
    Compute log-interaction energy E = (1/2) sum_{i!=j} omega_i G_ij omega_j dA^2.

    Uses direct pairwise summation on the grid (O(n^2) — only feasible for
    small grids or coarsened fields).
    """
    dy = y_grid[1] - y_grid[0]
    dx = x_grid[1] - x_grid[0]
    dA = dy * dx
    ny, nx = len(y_grid), len(x_grid)
    Y, X = np.meshgrid(y_grid, x_grid, indexing='ij')

    # Flatten
    omega_flat = omega.flatten()
    x_flat = X.flatten()
    y_flat = Y.flatten()
    n_pts = len(omega_flat)

    E = 0.0
    for i in range(n_pts):
        if abs(omega_flat[i]) < 1e-20:
            continue
        for j in range(i + 1, n_pts):
            if abs(omega_flat[j]) < 1e-20:
                continue
            d = np.sqrt((x_flat[i] - x_flat[j])**2 +
                        (y_flat[i] - y_flat[j])**2)
            if d < 1e-15:
                continue
            E -= omega_flat[i] * omega_flat[j] * np.log(d) * dA**2
    return E / (2.0 * np.pi)


# ---------------------------------------------------------------------------
# Lobe-based Hessian: treat each lobe as a "super-vortex"
# ---------------------------------------------------------------------------

def extract_lobe_properties(omega, lobe_labels, y_grid, x_grid):
    """
    Extract circulation and centroid for each lobe.

    Returns
    -------
    circulations : (n_lobes,) array of kappa_k
    centroids : (n_lobes, 2) array of (x_c, y_c)
    """
    dy = y_grid[1] - y_grid[0]
    dx = x_grid[1] - x_grid[0]
    dA = dy * dx
    Y, X = np.meshgrid(y_grid, x_grid, indexing='ij')

    n_lobes = int(lobe_labels.max())
    circulations = np.zeros(n_lobes)
    centroids = np.zeros((n_lobes, 2))

    for k in range(n_lobes):
        mask = (lobe_labels == k + 1)
        w = omega[mask]
        kappa = np.sum(w) * dA
        circulations[k] = kappa
        if abs(kappa) > 1e-30:
            centroids[k, 0] = np.sum(X[mask] * w) * dA / kappa  # x_c
            centroids[k, 1] = np.sum(Y[mask] * w) * dA / kappa  # y_c

    return circulations, centroids


def point_vortex_hessian(circulations, centroids):
    """
    Compute the constrained Hessian of H = -sum_{j<k} kappa_j kappa_k ln|z_j - z_k|
    on the constraint surface L = sum kappa_k |z_k|^2 = const.

    This is the Havelock Hessian for the given (possibly non-uniform)
    circulations and positions.

    Parameters
    ----------
    circulations : (N,) array
    centroids : (N, 2) array of (x_k, y_k)

    Returns
    -------
    eigenvalues : sorted array of 2N eigenvalues
    H_constrained : (2N, 2N) constrained Hessian matrix
    """
    N = len(circulations)
    z = centroids[:, 0] + 1j * centroids[:, 1]
    kappa = circulations

    # Build Hessian of H = -sum_{j<k} kappa_j kappa_k ln|z_j - z_k|
    H = np.zeros((2 * N, 2 * N))
    for j in range(N):
        for k in range(N):
            if j == k:
                continue
            dz = z[j] - z[k]
            dx_jk, dy_jk = dz.real, dz.imag
            d2 = dx_jk**2 + dy_jk**2
            if d2 < 1e-30:
                continue

            # Second derivatives of -kappa_j * kappa_k * ln|z_j - z_k|
            # = -kappa_j * kappa_k * (1/2) ln((x_j-x_k)^2 + (y_j-y_k)^2)
            coeff = kappa[j] * kappa[k]

            h_xx = coeff * (dy_jk**2 - dx_jk**2) / d2**2
            h_yy = coeff * (dx_jk**2 - dy_jk**2) / d2**2
            h_xy = -coeff * 2 * dx_jk * dy_jk / d2**2

            # Diagonal blocks (d^2H / dz_j dz_j)
            H[j, j] -= h_xx
            H[j + N, j + N] -= h_yy
            H[j, j + N] -= h_xy
            H[j + N, j] -= h_xy

            # Off-diagonal blocks (d^2H / dz_j dz_k)
            H[j, k] += h_xx
            H[j + N, k + N] += h_yy
            H[j, k + N] += h_xy
            H[j + N, k] += h_xy

    # Constraint: L = sum kappa_k |z_k|^2
    # grad L = [2*kappa_0*x_0, ..., 2*kappa_{N-1}*x_{N-1},
    #           2*kappa_0*y_0, ..., 2*kappa_{N-1}*y_{N-1}]
    L_grad = np.concatenate([2 * kappa * centroids[:, 0],
                             2 * kappa * centroids[:, 1]])
    L_norm = np.linalg.norm(L_grad)
    if L_norm < 1e-30:
        return np.sort(np.linalg.eigvalsh(H)), H

    L_hat = L_grad / L_norm

    # Lagrange multiplier
    mu_L = float(L_hat @ H @ L_hat)

    # Constrained Hessian: project out the constraint direction
    H_lagr = H - mu_L * np.outer(L_hat, L_hat)
    P = np.eye(2 * N) - np.outer(L_hat, L_hat)
    H_constr = P @ H_lagr @ P

    evals = np.sort(np.linalg.eigvalsh(H_constr))
    return evals, H_constr


def havelock_eigenvalues(N, R=1.0):
    """
    Exact Havelock eigenvalues for equal-circulation N-ring of radius R.

    lambda_m = (N-1)/2 - m*(N-m)/2  for m = 0, 1, ..., floor(N/2)

    Returns sorted array of the distinct eigenvalues (each with multiplicity 2
    except m=0 and m=N/2 if N even).
    """
    evals = []
    for m in range(N):
        lam = ((N - 1) - m * (N - m)) / 2.0
        evals.append(lam)
    return np.sort(evals)


# ---------------------------------------------------------------------------
# Stuart vortex Hessian analysis
# ---------------------------------------------------------------------------

def stuart_lobe_hessian(eps, sigma=0.5, n=6, ny=512, nx=512):
    """
    Compute the effective point-vortex Hessian from a Stuart vortex.

    Extracts lobe circulations and centroids, then computes the
    constrained Hessian as if the lobes were point vortices.

    Returns
    -------
    dict with:
        'eigenvalues'    : sorted Hessian eigenvalues
        'havelock_evals' : reference Havelock eigenvalues for comparison
        'circulations'   : lobe circulations
        'centroids'      : lobe centroids
        'n_lobes'        : number of lobes detected
    """
    from planetary_polygons.extensions.catseye_decomposition import (
        stuart_stream_function, stuart_vorticity,
        stuart_separatrix_level, classify_regions,
        label_individual_lobes,
    )

    domain_half = 6.0 * sigma
    y_grid = np.linspace(-domain_half, domain_half, ny)
    x_grid = np.linspace(0, 2 * np.pi, nx, endpoint=False)

    omega = stuart_vorticity(y_grid, x_grid, sigma, eps, n)
    Psi = stuart_stream_function(y_grid, x_grid, sigma, eps, n)
    psi_sep = stuart_separatrix_level(sigma, eps)
    braid_hw = 0.05 * sigma**2

    mask = classify_regions(Psi, psi_sep, braid_hw)
    labels = label_individual_lobes(mask)
    n_lobes = int(labels.max())

    if n_lobes < 2:
        return {'eigenvalues': np.array([]), 'n_lobes': 0}

    circs, cents = extract_lobe_properties(omega, labels, y_grid, x_grid)

    # Handle the periodic boundary: if n_lobes = n+1, merge first and last
    if n_lobes == n + 1:
        # Check if first and last lobe are the same (wrapped around x=0/2pi)
        x_first, x_last = cents[0, 0], cents[-1, 0]
        if x_first < 0.3 and x_last > 2 * np.pi - 0.3:
            # Merge: add circulations, average centroids
            kappa_merged = circs[0] + circs[-1]
            if abs(kappa_merged) > 1e-30:
                x_merged = (circs[0] * cents[0, 0] +
                            circs[-1] * (cents[-1, 0] - 2 * np.pi)) / kappa_merged
                y_merged = (circs[0] * cents[0, 1] +
                            circs[-1] * cents[-1, 1]) / kappa_merged
            else:
                x_merged, y_merged = 0.0, 0.0
            circs = np.concatenate([[kappa_merged], circs[1:-1]])
            cents = np.vstack([[x_merged, y_merged], cents[1:-1]])
            n_lobes -= 1

    evals, _ = point_vortex_hessian(circs, cents)
    hav = havelock_eigenvalues(n_lobes)

    return {
        'eigenvalues': evals,
        'havelock_evals': hav,
        'circulations': circs,
        'centroids': cents,
        'n_lobes': n_lobes,
    }


# ---------------------------------------------------------------------------
# Prandtl-Batchelor cat's-eye
# ---------------------------------------------------------------------------

def prandtl_batchelor_catseye(y_grid, x_grid, sigma, eps, n=6,
                               transition_width=0.02):
    """
    Construct a Prandtl-Batchelor cat's-eye vorticity field.

    Inside the separatrix: PV is homogenized to q_trap (constant).
    Outside: PV follows the background profile q_bg(y) = -sech^2(y/sigma)/sigma^2.
    Transition: smooth tanh profile of width `transition_width * sigma^2`
    in Psi-space.

    Parameters
    ----------
    y_grid, x_grid : 1D arrays
    sigma, eps, n : Stuart vortex parameters (geometry matches Stuart)
    transition_width : float
        Transition layer width in units of sigma^2.

    Returns
    -------
    omega_pb : (ny, nx) Prandtl-Batchelor vorticity field
    Psi : (ny, nx) stream function (still Stuart geometry)
    mask : (ny, nx) region classification
    """
    from planetary_polygons.extensions.catseye_decomposition import (
        stuart_stream_function, stuart_vorticity,
        stuart_separatrix_level, stuart_background_vorticity,
        classify_regions,
    )

    Y, X = np.meshgrid(y_grid, x_grid, indexing='ij')
    Psi = stuart_stream_function(y_grid, x_grid, sigma, eps, n)
    psi_sep = stuart_separatrix_level(sigma, eps)

    # Stuart vorticity (smooth reference)
    omega_stuart = stuart_vorticity(y_grid, x_grid, sigma, eps, n)

    # Background vorticity (zonal mean = eps=0 limit)
    omega_bg = stuart_background_vorticity(y_grid, sigma)

    # Trapped PV value: average of Stuart vorticity inside separatrix
    inside = (Psi > psi_sep)
    if np.any(inside):
        q_trap = float(np.mean(omega_stuart[inside]))
    else:
        q_trap = float(np.max(omega_stuart))

    # Smooth transition using tanh profile in Psi-space
    delta = transition_width * sigma**2
    # s = 1 deep inside lobes, s = 0 far outside
    s = 0.5 * (1.0 + np.tanh((Psi - psi_sep) / delta))

    # Prandtl-Batchelor field: interpolate between q_trap and omega_bg
    omega_pb = s * q_trap + (1.0 - s) * omega_bg[:, None]

    # Region classification
    braid_hw = 0.05 * sigma**2
    mask = classify_regions(Psi, psi_sep, braid_hw)

    return omega_pb, Psi, mask


def pb_lobe_hessian(eps, sigma=0.5, n=6, ny=512, nx=512,
                     transition_width=0.02):
    """
    Compute effective point-vortex Hessian from a Prandtl-Batchelor cat's-eye.

    Same as stuart_lobe_hessian but using the step-PV (PB) vorticity field.
    """
    from planetary_polygons.extensions.catseye_decomposition import (
        stuart_stream_function, stuart_separatrix_level,
        classify_regions, label_individual_lobes,
    )

    domain_half = 6.0 * sigma
    y_grid = np.linspace(-domain_half, domain_half, ny)
    x_grid = np.linspace(0, 2 * np.pi, nx, endpoint=False)

    omega_pb, Psi, mask = prandtl_batchelor_catseye(
        y_grid, x_grid, sigma, eps, n, transition_width
    )
    labels = label_individual_lobes(mask)
    n_lobes = int(labels.max())

    if n_lobes < 2:
        return {'eigenvalues': np.array([]), 'n_lobes': 0}

    circs, cents = extract_lobe_properties(omega_pb, labels, y_grid, x_grid)

    # Merge wrapped lobes
    if n_lobes == n + 1:
        x_first, x_last = cents[0, 0], cents[-1, 0]
        if x_first < 0.3 and x_last > 2 * np.pi - 0.3:
            kappa_merged = circs[0] + circs[-1]
            if abs(kappa_merged) > 1e-30:
                x_m = (circs[0] * cents[0, 0] +
                       circs[-1] * (cents[-1, 0] - 2 * np.pi)) / kappa_merged
                y_m = (circs[0] * cents[0, 1] +
                       circs[-1] * cents[-1, 1]) / kappa_merged
            else:
                x_m, y_m = 0.0, 0.0
            circs = np.concatenate([[kappa_merged], circs[1:-1]])
            cents = np.vstack([[x_m, y_m], cents[1:-1]])
            n_lobes -= 1

    evals, _ = point_vortex_hessian(circs, cents)
    hav = havelock_eigenvalues(n_lobes)

    return {
        'eigenvalues': evals,
        'havelock_evals': hav,
        'circulations': circs,
        'centroids': cents,
        'n_lobes': n_lobes,
    }


# ---------------------------------------------------------------------------
# Comparison analysis
# ---------------------------------------------------------------------------

def compare_hessian_eigenvalues(result, label=""):
    """Print eigenvalue comparison between cat's-eye and Havelock."""
    if result['n_lobes'] == 0:
        print(f"  {label}: no lobes detected")
        return

    N = result['n_lobes']
    evals = result['eigenvalues']
    hav = result['havelock_evals']

    # The constrained Hessian has one zero eigenvalue (constraint direction)
    # and potentially more from symmetry.  Compare the non-trivial eigenvalues.

    # For the point vortex N-ring: 2N eigenvalues, 1 zero (constraint),
    # 2 zero (translation), leaves 2N-3 non-trivial.
    # The Havelock eigenvalues lambda_m for m=1,...,N-1 give the N-1
    # non-trivial eigenvalues (each with multiplicity 2 except endpoints).

    print(f"\n  {label}: N = {N} lobes")
    print(f"  Circulations: {result['circulations']}")

    # Count positive, zero, negative eigenvalues
    tol = 0.01 * max(abs(evals.max()), abs(evals.min()), 1e-10)
    n_pos = np.sum(evals > tol)
    n_zero = np.sum(np.abs(evals) <= tol)
    n_neg = np.sum(evals < -tol)
    print(f"  Eigenvalue inertia: {n_pos}+, {n_zero}zero, {n_neg}-")

    # Havelock reference
    hav_pos = np.sum(hav > 0.01)
    hav_zero = np.sum(np.abs(hav) <= 0.01)
    hav_neg = np.sum(hav < -0.01)
    print(f"  Havelock reference:  {hav_pos}+, {hav_zero}zero, {hav_neg}-")

    # Sign agreement
    sign_match = (n_neg == hav_neg)
    print(f"  Signs match: {'YES' if sign_match else 'NO'}")

    # Print sorted eigenvalues
    print(f"  Cat's-eye evals (sorted): {np.sort(evals)[:8]}")
    print(f"  Havelock evals:           {np.sort(hav)[:8]}")

    return sign_match


def run_hessian_analysis(verbose=True):
    """
    Main analysis: compare Stuart and PB cat's-eye Hessians to Havelock.
    """
    eps_values = [0.5, 0.7, 0.8, 0.9, 0.95, 0.98]
    sigma = 0.5

    if verbose:
        print("Cat's-eye Hessian eigenvalue analysis")
        print("=" * 70)
        print(f"sigma = {sigma}, n = 6")

    results = {'stuart': [], 'pb': []}

    for eps in eps_values:
        if verbose:
            print(f"\n{'='*70}")
            print(f"eps = {eps} (1-eps = {1-eps:.4f})")
            print(f"{'='*70}")

        # Stuart vortex
        r_stuart = stuart_lobe_hessian(eps, sigma=sigma, n=6)
        results['stuart'].append(r_stuart)
        if verbose:
            compare_hessian_eigenvalues(r_stuart, "Stuart")

        # Prandtl-Batchelor
        r_pb = pb_lobe_hessian(eps, sigma=sigma, n=6)
        results['pb'].append(r_pb)
        if verbose:
            compare_hessian_eigenvalues(r_pb, "Prandtl-Batchelor")

    if verbose:
        print(f"\n{'='*70}")
        print("SUMMARY")
        print(f"{'='*70}")
        print(f"\n{'eps':>6} | {'Stuart signs':>15} | {'PB signs':>15} | "
              f"{'Stuart match':>12} | {'PB match':>12}")
        print("-" * 70)
        for i, eps in enumerate(eps_values):
            r_s = results['stuart'][i]
            r_p = results['pb'][i]
            for label, r in [('Stuart', r_s), ('PB', r_p)]:
                if r['n_lobes'] == 0:
                    continue
            s_evals = r_s['eigenvalues']
            p_evals = r_p['eigenvalues']
            tol_s = 0.01 * max(abs(s_evals).max(), 1e-10)
            tol_p = 0.01 * max(abs(p_evals).max(), 1e-10)
            s_inertia = f"{np.sum(s_evals>tol_s)}+/{np.sum(s_evals<-tol_s)}-"
            p_inertia = f"{np.sum(p_evals>tol_p)}+/{np.sum(p_evals<-tol_p)}-"

            hav = r_s.get('havelock_evals', np.array([]))
            hav_neg = np.sum(hav < -0.01)
            s_match = "YES" if np.sum(s_evals < -tol_s) == hav_neg else "NO"
            p_match = "YES" if np.sum(p_evals < -tol_p) == hav_neg else "NO"

            print(f"{eps:6.2f} | {s_inertia:>15} | {p_inertia:>15} | "
                  f"{s_match:>12} | {p_match:>12}")

    return results


if __name__ == "__main__":
    run_hessian_analysis(verbose=True)
