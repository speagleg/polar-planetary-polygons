"""
Cat's-eye vorticity decomposition for the Rossby bridge gap analysis.

Uses the Stuart vortex — an exact steady Euler solution with analytical
cat's-eye structure — to model the nonlinear critical layer of a
saturated Rossby wave.

Stuart vortex stream function:
    Psi(x, y) = -sigma^2 * ln(cosh(y/sigma) - eps * cos(n*x))

Parameters:
    sigma : jet half-width (controls sharpness)
    eps   : cat's-eye amplitude, 0 < eps < 1
            eps -> 0 : weak wave, no trapped fluid
            eps -> 1 : strong concentration, point-vortex limit

Vorticity (exact):
    omega = (1 - eps^2) / sigma^2 / (cosh(y/sigma) - eps*cos(n*x))^2

Separatrix (exact): Psi_sep = -sigma^2 * ln(1 + eps)
    (at saddle points y=0, x = pi/n + 2*k*pi/n)

Regions:
    - Lobe:       closed streamlines inside separatrices (trapped fluid)
    - Braid:      thin layer near separatrices
    - Background: passing fluid outside cat's-eye

Key question for the bridge (Section 5.4.3):
    Does kappa_braid -> 0 as sigma -> 0?
    If yes, Proposition 8 (inertia preservation) applies to the lobe
    component and the Rossby bridge closes in the sharp-jet limit.

All computations use numpy only (no scipy required).
"""
import numpy as np


# ---------------------------------------------------------------------------
# Stuart vortex construction
# ---------------------------------------------------------------------------

def stuart_stream_function(y, x, sigma, eps, n=6):
    """
    Stuart vortex stream function on a 2D grid.

    Psi(x,y) = -sigma^2 * ln(cosh(y/sigma) - eps * cos(n*x))

    Parameters
    ----------
    y : (ny,) or (ny, nx) array
    x : (nx,) or (ny, nx) array
    sigma : float  — jet half-width
    eps : float    — cat's-eye parameter, 0 < eps < 1
    n : int        — azimuthal wavenumber

    Returns
    -------
    Psi : same shape as broadcast(y, x)
    """
    if y.ndim == 1 and x.ndim == 1:
        Y, X = np.meshgrid(y, x, indexing='ij')
    else:
        Y, X = y, x
    arg = np.cosh(Y / sigma) - eps * np.cos(n * X)
    # arg > 0 always since cosh >= 1 and eps < 1
    return -sigma**2 * np.log(arg)


def stuart_vorticity(y, x, sigma, eps, n=6):
    """
    Exact vorticity for the Stuart vortex.

    omega = (1 - eps^2) / sigma^2 / (cosh(y/sigma) - eps*cos(n*x))^2
    """
    if y.ndim == 1 and x.ndim == 1:
        Y, X = np.meshgrid(y, x, indexing='ij')
    else:
        Y, X = y, x
    denom = np.cosh(Y / sigma) - eps * np.cos(n * X)
    return (1.0 - eps**2) / sigma**2 / denom**2


def stuart_velocity(y, x, sigma, eps, n=6):
    """
    Velocity field (u, v) = (-dPsi/dy, dPsi/dx) for the Stuart vortex.

    u = sigma * sinh(y/sigma) / (cosh(y/sigma) - eps*cos(n*x))
    v = -sigma^2 * n * eps * sin(n*x) / (cosh(y/sigma) - eps*cos(n*x))
    """
    if y.ndim == 1 and x.ndim == 1:
        Y, X = np.meshgrid(y, x, indexing='ij')
    else:
        Y, X = y, x
    denom = np.cosh(Y / sigma) - eps * np.cos(n * X)
    u = sigma * np.sinh(Y / sigma) / denom
    v = -sigma**2 * n * eps * np.sin(n * X) / denom
    return u, v


def stuart_separatrix_level(sigma, eps):
    """Exact separatrix stream function value: Psi_sep = -sigma^2 * ln(1+eps)."""
    return -sigma**2 * np.log(1.0 + eps)


# ---------------------------------------------------------------------------
# Background vorticity (zonal mean = eps=0 limit)
# ---------------------------------------------------------------------------

def stuart_background_vorticity(y, sigma):
    """
    Background (zonal-mean) vorticity: omega_bg = 1/sigma^2 / cosh^2(y/sigma).

    This is the eps=0 limit, which is the sech^2 jet vorticity profile.
    """
    return 1.0 / sigma**2 / np.cosh(y / sigma)**2


# ---------------------------------------------------------------------------
# Region classification
# ---------------------------------------------------------------------------

def classify_regions(Psi, psi_sep, braid_half_width):
    """
    Classify each grid cell as lobe, braid, or background.

    Parameters
    ----------
    Psi : (ny, nx) stream function
    psi_sep : float — separatrix level
    braid_half_width : float — half-width of braid region in Psi-space.
        Cells with |Psi - psi_sep| < braid_half_width are classified
        as braid.

    Returns
    -------
    mask : (ny, nx) int array
        0 = background, 1 = lobe (inside separatrix), 2 = braid
    """
    mask = np.zeros_like(Psi, dtype=int)

    # Lobes: Psi > psi_sep + delta  (inside the separatrix, higher Psi)
    mask[Psi > psi_sep + braid_half_width] = 1

    # Braid: near the separatrix
    mask[np.abs(Psi - psi_sep) <= braid_half_width] = 2

    # Background: everything else (Psi < psi_sep - delta), stays 0
    return mask


def label_individual_lobes(mask):
    """
    Label individual lobes (connected x-segments where mask==1).

    Returns
    -------
    lobe_labels : (ny, nx) int array
        0 = not a lobe, 1..n_lobes = lobe index
    """
    lobe_x_profile = np.any(mask == 1, axis=0).astype(int)

    # Find connected x-segments
    segments = []
    in_seg = False
    for j in range(len(lobe_x_profile)):
        if lobe_x_profile[j] and not in_seg:
            seg_start = j
            in_seg = True
        elif not lobe_x_profile[j] and in_seg:
            segments.append((seg_start, j))
            in_seg = False
    if in_seg:
        segments.append((seg_start, len(lobe_x_profile)))

    lobe_labels = np.zeros_like(mask)
    for idx, (j0, j1) in enumerate(segments):
        col_mask = np.zeros(mask.shape[1], dtype=bool)
        col_mask[j0:j1] = True
        lobe_labels[:, col_mask] = np.where(
            mask[:, col_mask] == 1, idx + 1, 0
        )
    return lobe_labels


# ---------------------------------------------------------------------------
# Circulation and centroid computation
# ---------------------------------------------------------------------------

def circulation_partition(omega, omega_bg, mask, dy, dx):
    """
    Integrate vorticity anomaly in each region.

    Parameters
    ----------
    omega : (ny, nx) full vorticity field
    omega_bg : (ny,) or (ny, nx) background vorticity
    mask : (ny, nx) region classification (0=bg, 1=lobe, 2=braid)
    dy, dx : grid spacings

    Returns
    -------
    dict with kappa and area for each region
    """
    dA = dy * dx
    if omega_bg.ndim == 1:
        anom = omega - omega_bg[:, None]
    else:
        anom = omega - omega_bg

    result = {}
    for name, val in [('lobe', 1), ('braid', 2), ('background', 0)]:
        region = (mask == val)
        result[f'kappa_{name}'] = float(np.sum(anom[region]) * dA)
        result[f'area_{name}'] = float(np.sum(region) * dA)

    return result


def lobe_centroids(omega, lobe_labels, y_grid, x_grid):
    """
    Vorticity-weighted centroid of each lobe.

    Returns list of (y_c, x_c) tuples.
    """
    Y, X = np.meshgrid(y_grid, x_grid, indexing='ij')
    n_lobes = int(lobe_labels.max())
    centroids = []
    for k in range(1, n_lobes + 1):
        region = (lobe_labels == k)
        if not np.any(region):
            continue
        w = omega[region]
        total_w = np.sum(w)
        if abs(total_w) < 1e-30:
            centroids.append((0.0, 0.0))
            continue
        y_c = float(np.sum(Y[region] * w) / total_w)
        x_c = float(np.sum(X[region] * w) / total_w)
        centroids.append((y_c, x_c))
    return centroids


# ---------------------------------------------------------------------------
# Sigma scan: the main analysis
# ---------------------------------------------------------------------------

def sigma_scan(sigma_values, eps=0.8, n=6, ny=512, nx=512,
               braid_fraction=0.05, domain_factor=6.0):
    """
    Scan jet width sigma and measure circulation partition.

    Parameters
    ----------
    sigma_values : array-like
        Jet half-widths to scan.
    eps : float
        Cat's-eye amplitude parameter (fixed across scan).
    n : int
        Azimuthal wavenumber (default 6 for Saturn hexagon).
    ny, nx : int
        Grid resolution.
    braid_fraction : float
        Braid half-width as fraction of |Psi_lobe_center - Psi_sep|.
    domain_factor : float
        y-domain extends to ± domain_factor * max(sigma).

    Returns
    -------
    list of dicts, one per sigma value.
    """
    domain_half = domain_factor * max(sigma_values)
    x_grid = np.linspace(0, 2.0 * np.pi, nx, endpoint=False)

    results = []
    for sigma in sigma_values:
        y_grid = np.linspace(-domain_half, domain_half, ny)
        dy = y_grid[1] - y_grid[0]
        dx = x_grid[1] - x_grid[0]

        # Stream function and vorticity (analytical)
        Psi = stuart_stream_function(y_grid, x_grid, sigma, eps, n)
        omega = stuart_vorticity(y_grid, x_grid, sigma, eps, n)
        omega_bg = stuart_background_vorticity(y_grid, sigma)

        # Separatrix (exact)
        psi_sep = stuart_separatrix_level(sigma, eps)

        # Braid width: fixed fraction of sigma^2 (the natural Psi scale),
        # NOT proportional to psi_center - psi_sep (which diverges as eps->1).
        braid_hw = braid_fraction * sigma**2

        # Classify
        mask = classify_regions(Psi, psi_sep, braid_hw)
        lobe_lab = label_individual_lobes(mask)

        # Circulation partition
        circ = circulation_partition(omega, omega_bg, mask, dy, dx)
        centroids = lobe_centroids(omega, lobe_lab, y_grid, x_grid)

        # Total circulation per wavelength (analytical check)
        kappa_total_numerical = float(np.sum(omega) * dy * dx)
        # Analytical: integral of sech^2 jet over full domain ≈ 2/sigma * (2*pi)
        # (the Stuart vortex total circ per period = 2*pi*(1-eps^2)^{1/2}...
        #  but we compute numerically for the check)

        results.append({
            'sigma': sigma,
            'eps': eps,
            'n_lobes_detected': int(lobe_lab.max()),
            'lobe_centroids': centroids,
            'psi_sep': psi_sep,
            'braid_half_width': braid_hw,
            'kappa_total_numerical': kappa_total_numerical,
            **circ,
        })

    return results


def fit_scaling_law(sigma_values, kappa_values):
    """
    Fit |kappa| ~ C * sigma^alpha in log-log space.

    Returns (alpha, C, r_squared).
    """
    valid = np.array(kappa_values) != 0
    if np.sum(valid) < 2:
        return 0.0, 0.0, 0.0

    log_s = np.log(np.array(sigma_values)[valid])
    log_k = np.log(np.abs(np.array(kappa_values)[valid]))

    coeffs = np.polyfit(log_s, log_k, 1)
    alpha = coeffs[0]
    C = np.exp(coeffs[1])

    residuals = log_k - np.polyval(coeffs, log_s)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((log_k - np.mean(log_k))**2)
    r2 = 1.0 - ss_res / (ss_tot + 1e-15)

    return float(alpha), float(C), float(r2)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def run_bridge_analysis(verbose=True):
    """
    Run the sigma-scan and report whether the braid vanishes.

    Returns dict with scan results, scaling exponents, and bridge verdict.
    """
    sigma_values = np.array([1.0, 0.5, 0.3, 0.2, 0.15, 0.10, 0.07, 0.05])
    eps = 0.8  # moderately strong cat's-eye

    if verbose:
        print("Stuart vortex cat's-eye decomposition")
        print(f"eps = {eps},  n = 6,  scanning sigma...")
        print("=" * 90)

    scan = sigma_scan(sigma_values, eps=eps, n=6, ny=512, nx=512)

    sigmas = [r['sigma'] for r in scan]
    k_braid = [r['kappa_braid'] for r in scan]
    k_lobe = [r['kappa_lobe'] for r in scan]
    k_bg = [r['kappa_background'] for r in scan]

    alpha_braid, C_braid, r2_braid = fit_scaling_law(sigmas, k_braid)
    alpha_lobe, C_lobe, r2_lobe = fit_scaling_law(sigmas, k_lobe)

    if verbose:
        print(f"\n{'sigma':>8} {'n_lobe':>6} {'kappa_lobe':>12} "
              f"{'kappa_braid':>12} {'kappa_bg':>12} "
              f"{'A_lobe':>8} {'A_braid':>8} {'A_bg':>8} "
              f"{'|braid/lobe|':>12}")
        print("-" * 108)
        for r in scan:
            kl = r['kappa_lobe']
            kb = r['kappa_braid']
            ratio = abs(kb / kl) if abs(kl) > 1e-15 else float('inf')
            print(f"{r['sigma']:8.4f} {r['n_lobes_detected']:6d} "
                  f"{kl:12.6f} "
                  f"{kb:12.6f} "
                  f"{r['kappa_background']:12.6f} "
                  f"{r['area_lobe']:8.4f} "
                  f"{r['area_braid']:8.4f} "
                  f"{r['area_background']:8.4f} "
                  f"{ratio:12.6f}")

        print(f"\nScaling laws (log-log fit):")
        print(f"  kappa_braid ~ sigma^{alpha_braid:.3f}  "
              f"(R^2 = {r2_braid:.4f})")
        print(f"  kappa_lobe  ~ sigma^{alpha_lobe:.3f}  "
              f"(R^2 = {r2_lobe:.4f})")

        print(f"\nInterpretation:")
        if alpha_braid > alpha_lobe + 0.3:
            print(f"  >>> BRIDGE CLOSES: braid vanishes faster "
                  f"(sigma^{alpha_braid:.2f}) than lobe "
                  f"(sigma^{alpha_lobe:.2f}).")
            print(f"  >>> Ratio |braid/lobe| -> 0 as sigma -> 0.  "
                  f"Prop 8 applies.")
        elif alpha_braid > 0:
            print(f"  >>> PARTIAL: braid vanishes (sigma^{alpha_braid:.2f}) "
                  f"but lobe also vanishes (sigma^{alpha_lobe:.2f}).")
            print(f"  >>> Check the RATIO |braid/lobe| scaling.")
        else:
            print(f"  >>> GAP PERSISTS: braid exponent = {alpha_braid:.2f}.")

        # Ratio scaling
        ratios = [abs(kb / kl) if abs(kl) > 1e-15 else 0.0
                  for kb, kl in zip(k_braid, k_lobe)]
        alpha_ratio, _, r2_ratio = fit_scaling_law(sigmas, ratios)
        print(f"\n  |braid/lobe| ~ sigma^{alpha_ratio:.3f}  "
              f"(R^2 = {r2_ratio:.4f})")
        if alpha_ratio > 0.3:
            print(f"  >>> RATIO VANISHES: bridge closes in sharp-jet limit.")
        elif alpha_ratio > 0:
            print(f"  >>> RATIO DECREASES SLOWLY: bridge partially closes.")
        else:
            print(f"  >>> RATIO DOES NOT VANISH: bridge gap persists.")

    return {
        'scan_results': scan,
        'braid_exponent': alpha_braid,
        'braid_r2': r2_braid,
        'lobe_exponent': alpha_lobe,
        'lobe_r2': r2_lobe,
        'bridge_closes': alpha_braid > alpha_lobe + 0.3,
    }


def eps_scan(eps_values, sigma=0.5, n=6, ny=512, nx=512,
             braid_fraction=0.05, domain_factor=6.0):
    """
    Scan cat's-eye parameter eps at fixed sigma.

    As eps -> 1, the Stuart vortex approaches n point vortices.
    This is the concentration limit relevant to Proposition 8.
    """
    domain_half = domain_factor * sigma
    y_grid = np.linspace(-domain_half, domain_half, ny)
    x_grid = np.linspace(0, 2.0 * np.pi, nx, endpoint=False)
    dy = y_grid[1] - y_grid[0]
    dx = x_grid[1] - x_grid[0]
    omega_bg = stuart_background_vorticity(y_grid, sigma)

    results = []
    for eps in eps_values:
        Psi = stuart_stream_function(y_grid, x_grid, sigma, eps, n)
        omega = stuart_vorticity(y_grid, x_grid, sigma, eps, n)

        psi_sep = stuart_separatrix_level(sigma, eps)
        braid_hw = braid_fraction * sigma**2

        mask = classify_regions(Psi, psi_sep, braid_hw)
        lobe_lab = label_individual_lobes(mask)
        circ = circulation_partition(omega, omega_bg, mask, dy, dx)
        centroids = lobe_centroids(omega, lobe_lab, y_grid, x_grid)

        results.append({
            'eps': eps,
            'sigma': sigma,
            'one_minus_eps': 1.0 - eps,
            'n_lobes_detected': int(lobe_lab.max()),
            'lobe_centroids': centroids,
            **circ,
        })
    return results


def run_eps_analysis(verbose=True):
    """
    Scan eps -> 1 (concentration limit) at fixed sigma.

    This is the limit where the Stuart vortex approaches point vortices.
    The bridge closes if |braid/lobe| -> 0 as eps -> 1.
    """
    eps_values = np.array([0.3, 0.5, 0.7, 0.8, 0.9, 0.95, 0.98, 0.99, 0.995])
    sigma = 0.5

    if verbose:
        print("\nStuart vortex: eps scan (concentration limit)")
        print(f"sigma = {sigma},  n = 6,  scanning eps -> 1...")
        print("=" * 100)

    scan = eps_scan(eps_values, sigma=sigma, n=6, ny=512, nx=512)

    eps_list = [r['eps'] for r in scan]
    one_minus = [r['one_minus_eps'] for r in scan]
    k_braid = [r['kappa_braid'] for r in scan]
    k_lobe = [r['kappa_lobe'] for r in scan]

    if verbose:
        print(f"\n{'eps':>8} {'1-eps':>8} {'n_lobe':>6} {'kappa_lobe':>12} "
              f"{'kappa_braid':>12} {'kappa_bg':>12} "
              f"{'A_lobe':>8} {'A_braid':>8} "
              f"{'|braid/lobe|':>12}")
        print("-" * 108)
        for r in scan:
            kl = r['kappa_lobe']
            kb = r['kappa_braid']
            ratio = abs(kb / kl) if abs(kl) > 1e-15 else float('inf')
            print(f"{r['eps']:8.3f} {r['one_minus_eps']:8.5f} "
                  f"{r['n_lobes_detected']:6d} "
                  f"{kl:12.6f} "
                  f"{kb:12.6f} "
                  f"{r['kappa_background']:12.6f} "
                  f"{r['area_lobe']:8.4f} "
                  f"{r['area_braid']:8.4f} "
                  f"{ratio:12.6f}")

    # Fit ratio vs (1-eps)
    ratios = [abs(kb / kl) if abs(kl) > 1e-15 else 0.0
              for kb, kl in zip(k_braid, k_lobe)]
    alpha_ratio, _, r2_ratio = fit_scaling_law(one_minus, ratios)

    # Fit braid and lobe vs (1-eps)
    alpha_braid, _, r2_braid = fit_scaling_law(one_minus, k_braid)
    alpha_lobe, _, r2_lobe = fit_scaling_law(one_minus, k_lobe)

    if verbose:
        print(f"\nScaling laws vs (1-eps):")
        print(f"  kappa_braid ~ (1-eps)^{alpha_braid:.3f}  (R^2 = {r2_braid:.4f})")
        print(f"  kappa_lobe  ~ (1-eps)^{alpha_lobe:.3f}  (R^2 = {r2_lobe:.4f})")
        print(f"  |braid/lobe| ~ (1-eps)^{alpha_ratio:.3f}  "
              f"(R^2 = {r2_ratio:.4f})")

        if alpha_ratio > 0.3:
            print(f"\n  >>> BRIDGE CLOSES in concentration limit:")
            print(f"  >>> braid/lobe vanishes as (1-eps)^{alpha_ratio:.2f}.")
        elif alpha_ratio > 0:
            print(f"\n  >>> BRIDGE PARTIALLY CLOSES: ratio decreases slowly.")
        else:
            print(f"\n  >>> BRIDGE GAP PERSISTS at fixed sigma.")

    return {
        'scan_results': scan,
        'ratio_exponent': alpha_ratio,
        'ratio_r2': r2_ratio,
        'braid_exponent': alpha_braid,
        'lobe_exponent': alpha_lobe,
    }


if __name__ == "__main__":
    print("=" * 100)
    print("ANALYSIS 1: Sigma scan (fixed eps = 0.8)")
    print("=" * 100)
    run_bridge_analysis(verbose=True)

    print("\n\n")
    print("=" * 100)
    print("ANALYSIS 2: Eps scan (fixed sigma = 0.5, eps -> 1)")
    print("=" * 100)
    run_eps_analysis(verbose=True)
