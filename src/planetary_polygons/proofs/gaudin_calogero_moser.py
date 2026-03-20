"""
Verification that Hess(H_CM) = [Hess(H_log)]² at the regular N-gon.

The Calogero-Moser Hamiltonian:
    H_CM = Σ_{j<k} 1/|z_j - z_k|²

The log-gas Hamiltonian:
    H_log = -Σ_{j<k} ln|z_j - z_k|

Claim (Agarwal et al. 2019, verified for Hermite zeros on the line):
    At common critical points, Hess(H_CM) = [Hess(H_log)]²

If this holds at the regular N-gon on the unit circle, then:
    CM eigenvalues = (Havelock eigenvalues)²
    μ_m = λ_m² = [(N-1) - m(N-m)/2]²

Consequences:
    - CM equilibria at regular N-gons are ALWAYS stable (μ_m ≥ 0)
    - μ_m = 0 exactly when λ_m = 0 (N=7, m=3,4)
    - On H²: μ_m(ξ) = [C₁(ξ) - m(N-m)/2]²
    - Palindromic Pell thresholds mark degenerate CM minima

Run: PYTHONPATH=src python3 -m planetary_polygons.proofs.gaudin_calogero_moser
"""
import numpy as np
from fractions import Fraction


def ngon_positions(N, R=1.0):
    """Regular N-gon on circle of radius R."""
    return R * np.exp(2j * np.pi * np.arange(N) / N)


# ============================================================
# Hessian of H_log = -Σ ln|z_j - z_k|
# ============================================================

def hessian_log(N, R=1.0):
    """
    Full 2N×2N Hessian of H_log = -Σ_{j<k} ln|z_j - z_k|
    at the regular N-gon.

    Layout: [x_0,...,x_{N-1}, y_0,...,y_{N-1}].

    For pair (j,k), d = |z_j - z_k|, w = z_j - z_k:
      h(d) = -ln(d), h'(d) = -1/d, h''(d) = 1/d²
      off-diagonal: H_{jk,ab} = (h'' - h'/d)(w_a w_b/d²) + (h'/d)δ_{ab}
                                = (2/d²)(w_a w_b/d²) + (-1/d²)δ_{ab}
      diagonal: H_{jj,ab} = -Σ_{k≠j} H_{jk,ab}
    """
    z = ngon_positions(N, R)
    H = np.zeros((2 * N, 2 * N))

    for j in range(N):
        for k in range(N):
            if j == k:
                continue
            w = z[j] - z[k]
            dx, dy = w.real, w.imag
            d2 = dx**2 + dy**2
            d4 = d2**2

            # h'' - h'/d = 1/d² - (-1/d)/d = 2/d²
            # h'/d = -1/d²
            A = 2.0 / d2   # anisotropy
            B = -1.0 / d2   # isotropic

            hxx = A * dx**2 / d2 + B
            hyy = A * dy**2 / d2 + B
            hxy = A * dx * dy / d2

            # Off-diagonal
            H[j, k] += hxx
            H[j + N, k + N] += hyy
            H[j, k + N] += hxy
            H[j + N, k] += hxy

            # Diagonal
            H[j, j] -= hxx
            H[j + N, j + N] -= hyy
            H[j, j + N] -= hxy
            H[j + N, j] -= hxy

    return H


# ============================================================
# Hessian of H_CM = Σ_{j<k} 1/|z_j - z_k|²
# ============================================================

def hessian_cm(N, R=1.0):
    """
    Full 2N×2N Hessian of H_CM = Σ_{j<k} 1/|z_j - z_k|²
    at the regular N-gon.

    For pair (j,k), g(d) = 1/d², g'(d) = -2/d³, g''(d) = 6/d⁴
    The energy is H_CM = -Σ_{j<k} g(d) with g(d) = -1/d², so we use
    h(d) = -1/d²: h'(d) = 2/d³, h''(d) = -6/d⁴

    Actually: H_CM = Σ_{j<k} |z_j-z_k|^{-2} = Σ_{j<k} g(d_{jk})
    where g(d) = d^{-2}.

    For the Hessian of H_CM = -Σ(-g) = -Σ h where h = -g = -1/d²:
    No, simpler: H_CM = Σ g(d) directly.

    ∂²g/∂x_j∂x_k for j≠k with g(d) = d^{-2}:
    g'(d) = -2d^{-3}, g''(d) = 6d^{-4}
    ∂d/∂x_j = (x_j-x_k)/d, ∂d/∂x_k = -(x_j-x_k)/d

    ∂²g/∂x_j∂x_k = g''(d)·(-w_x²/d²) + g'(d)·(-1/d + w_x²/d³)
                   = -(g'' - g'/d)(w_x/d)² - g'/d

    For H_CM = Σ_{j<k} g(d), the Hessian contribution from pair (j,k):
    ∂²H_CM/∂x_j∂x_k = -(g'' - g'/d)(w_x/d)² - g'/d

    Diagonal: ∂²H_CM/∂x_j² from pair (j,k) = +(g'' - g'/d)(w_x/d)² + g'/d
    """
    z = ngon_positions(N, R)
    H = np.zeros((2 * N, 2 * N))

    for j in range(N):
        for k in range(N):
            if j == k:
                continue
            w = z[j] - z[k]
            dx, dy = w.real, w.imag
            d2 = dx**2 + dy**2
            d = np.sqrt(d2)

            # g(d) = 1/d², g'(d) = -2/d³, g''(d) = 6/d⁴
            gpp = 6.0 / d2**2          # g''
            gp_over_d = -2.0 / d2**2   # g'/d = (-2/d³)/d = -2/d⁴
            A = gpp - gp_over_d         # g'' - g'/d = 6/d⁴ + 2/d⁴ = 8/d⁴
            B = gp_over_d               # g'/d = -2/d⁴

            # Off-diagonal (j,k): -(A)(w_a w_b/d²) - B·δ_{ab}
            hxx = -(A * dx**2 / d2 + B)
            hyy = -(A * dy**2 / d2 + B)
            hxy = -A * dx * dy / d2

            H[j, k] += hxx
            H[j + N, k + N] += hyy
            H[j, k + N] += hxy
            H[j + N, k] += hxy

            # Diagonal (j,j): +(A)(w_a w_b/d²) + B·δ_{ab}
            H[j, j] -= hxx
            H[j + N, j + N] -= hyy
            H[j, j + N] -= hxy
            H[j + N, j] -= hxy

    return H


# ============================================================
# Test: Hess(CM) = [Hess(log)]² ?
# ============================================================

def verify_hessian_squaring(N, R=1.0, tol=1e-8):
    """
    Test whether Hess(H_CM) = c · [Hess(H_log)]² for some constant c
    at the regular N-gon.

    Returns (matches, constant_c, max_residual).
    """
    H_log = hessian_log(N, R)
    H_cm = hessian_cm(N, R)
    H_log_sq = H_log @ H_log

    # Find the proportionality constant c
    # H_cm = c * H_log_sq
    # Use Frobenius inner product: c = tr(H_cm^T H_log_sq) / tr(H_log_sq^T H_log_sq)
    numer = np.trace(H_cm.T @ H_log_sq)
    denom = np.trace(H_log_sq.T @ H_log_sq)

    if abs(denom) < 1e-20:
        return False, 0.0, float('inf')

    c = numer / denom
    residual = H_cm - c * H_log_sq
    max_res = np.max(np.abs(residual))
    rel_res = max_res / np.max(np.abs(H_cm)) if np.max(np.abs(H_cm)) > 0 else max_res

    return rel_res < tol, c, rel_res


def eigenvalue_comparison(N, R=1.0):
    """
    Compare eigenvalues of H_CM with eigenvalues of [H_log]².

    If Hess(CM) = c·[Hess(log)]², their eigenvalues should satisfy
    μ_k(CM) = c · λ_k(log)².
    """
    H_log = hessian_log(N, R)
    H_cm = hessian_cm(N, R)
    H_log_sq = H_log @ H_log

    eigs_log = np.sort(np.linalg.eigvalsh(H_log))
    eigs_cm = np.sort(np.linalg.eigvalsh(H_cm))
    eigs_log_sq = np.sort(np.linalg.eigvalsh(H_log_sq))

    return eigs_log, eigs_cm, eigs_log_sq


def havelock_eigenvalue(m, N):
    """λ_m = (N-1) - m(N-m)/2."""
    return (N - 1) - m * (N - m) / 2.0


def radial_fourier_mode(N, m, R=1.0):
    """Radial Fourier mode: δz_j = z_j · cos(2πmj/N), normalized."""
    k = np.arange(N)
    z = R * np.exp(2j * np.pi * k / N)
    amp = np.cos(2 * np.pi * m * k / N)
    dz = z * amp
    v = np.concatenate([dz.real, dz.imag])
    norm = np.linalg.norm(v)
    return v / norm if norm > 1e-14 else v


def compute_omega_log(N, R=1.0):
    """Rotation frequency for H_log at the N-gon."""
    z = R * np.exp(2j * np.pi * np.arange(N) / N)
    grad_x = 0.0
    for p in range(1, N):
        w = z[0] - z[p]
        d = abs(w)
        grad_x += (1.0 / d) * w.real / d  # -h'(d) * w_x/d, h'=-1/d
    return -grad_x / R


def compute_omega_cm(N, R=1.0):
    """Rotation frequency for H_CM at the N-gon."""
    z = R * np.exp(2j * np.pi * np.arange(N) / N)
    grad_x = 0.0
    for p in range(1, N):
        w = z[0] - z[p]
        d = abs(w)
        # g(d) = 1/d², g'(d) = -2/d³
        # ∂H_CM/∂x_0 from pair (0,p) = g'(d)·(x_0-x_p)/d = -2/d³ · w_x/d
        grad_x += (-2.0 / d**3) * w.real / d
    return -grad_x / R


def constrained_eigenvalue_log(N, m, R=1.0):
    """Constrained Havelock eigenvalue: λ_m = -Ω - v^T·H·v."""
    H = hessian_log(N, R)
    v = radial_fourier_mode(N, m, R)
    Omega = compute_omega_log(N, R)
    return -Omega - float(v @ H @ v)


def constrained_eigenvalue_cm(N, m, R=1.0):
    """Constrained CM eigenvalue: μ_m = -Ω_CM - v^T·H_CM·v."""
    H = hessian_cm(N, R)
    v = radial_fourier_mode(N, m, R)
    Omega = compute_omega_cm(N, R)
    return -Omega - float(v @ H @ v)


def verify_eigenvalue_squaring(N, R=1.0):
    """
    Test whether the constrained CM eigenvalues equal
    c · (constrained log eigenvalues)² for some constant c.
    """
    results = []
    for m in range(1, N):
        lam_log = constrained_eigenvalue_log(N, m, R)
        mu_cm = constrained_eigenvalue_cm(N, m, R)
        lam_hav = havelock_eigenvalue(m, N)
        results.append({
            'm': m,
            'lambda_log': lam_log,
            'lambda_havelock': lam_hav,
            'mu_cm': mu_cm,
            'lambda_sq': lam_log**2,
        })
    return results


if __name__ == '__main__':
    print("=" * 70)
    print("Gaudin/Calogero-Moser Hessian Squaring at the Regular N-gon")
    print("=" * 70)

    # Test 1: Full matrix squaring Hess(CM) = c·[Hess(log)]²
    print("\n--- Test 1: Hess(H_CM) = c · [Hess(H_log)]² ---")
    print(f"{'N':>3} {'match':>6} {'c':>12} {'rel residual':>14}")
    for N in range(3, 13):
        match, c, res = verify_hessian_squaring(N)
        print(f"{N:3d} {'✓' if match else '✗':>6} {c:12.6f} {res:14.2e}")

    # Test 2: Constrained eigenvalue comparison
    print("\n--- Test 2: Constrained eigenvalues ---")
    for N in [6, 7, 8, 10]:
        print(f"\nN = {N}:")
        results = verify_eigenvalue_squaring(N)
        print(f"  {'m':>3} {'λ_log':>10} {'λ_hav':>10} {'μ_CM':>12} "
              f"{'λ²':>12} {'μ/λ²':>10}")
        for r in results:
            ratio = (r['mu_cm'] / r['lambda_sq']
                     if abs(r['lambda_sq']) > 1e-14 else float('inf'))
            print(f"  {r['m']:3d} {r['lambda_log']:10.4f} "
                  f"{r['lambda_havelock']:10.4f} {r['mu_cm']:12.4f} "
                  f"{r['lambda_sq']:12.4f} {ratio:10.4f}")

    # Test 3: Eigenvalue spectrum comparison
    print("\n--- Test 3: Full eigenvalue spectra ---")
    for N in [6, 8]:
        eigs_log, eigs_cm, eigs_log_sq = eigenvalue_comparison(N)
        print(f"\nN = {N}:")
        print(f"  H_log eigenvalues:    {np.round(eigs_log, 4)}")
        print(f"  H_CM eigenvalues:     {np.round(eigs_cm, 4)}")
        print(f"  [H_log]² eigenvalues: {np.round(eigs_log_sq, 4)}")
        if np.max(np.abs(eigs_log_sq)) > 1e-10:
            ratios = eigs_cm / eigs_log_sq
            ratios[np.abs(eigs_log_sq) < 1e-10] = 0
            print(f"  Ratios H_CM/[H_log]²: {np.round(ratios, 4)}")
