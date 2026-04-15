"""
Focused analysis: WHY is the Schur complement correction O(ε⁴), not O(ε⁶)?

The paper's (wrong) argument:
  ‖H_cs‖² = O(ε⁴/d⁶)   [from quadrupole coupling]
  λ_min(H_ss) = O(1/ε²)  [from wrong Poincaré inequality]
  correction = O(ε⁴/d⁶) / O(1/ε²) = O(ε⁶/d⁶)   ← WRONG

Correct analysis:
  λ_min(H_ss) = O(ε²)    [H⁻¹ norm scales as ε²]

But the correction is NOT ‖H_cs‖² / λ_min(H_ss) = O(ε⁴/d⁶) / O(ε²) = O(ε²/d⁶).
Instead it's O(ε⁴/d⁶).  Why?

Because H_cs projects onto LOW angular modes (m=2 quadrupole) where H_ss
eigenvalues are O(ε²) with a LARGE prefactor c_m.  The effective denominator
is c_2 ε² (mode-2 eigenvalue), and the coupling amplitude carries an extra ε²
from the radial integral.

Specifically:
  coupling to mode m = ∫ ∇G(z_j, z_k+ξ) · cos(mθ) ξ^{stuff} dξ
  ~ (ε^{m+1} / d^{m+1}) (from multipole + radial integral r^m dr)

  H_ss eigenvalue for mode m ~ ε² c_m (scale-invariant H⁻¹ norm)

  contribution from mode m: |coupling_m|² / λ_m
  ~ ε^{2m+2} / (d^{2m+2} ε² c_m) = ε^{2m} / (d^{2m+2} c_m)

  Leading term (m=2): O(ε⁴ / d⁶)  ← THIS is the correct scaling

This script verifies the mode-by-mode decomposition numerically.
"""
import numpy as np
from numpy.linalg import eigh, solve, norm


def ring_positions(N):
    return np.exp(2j * np.pi * np.arange(N) / N)


def d_min_val(N):
    return 2 * np.sin(np.pi / N)


def polar_grid(eps, Nr=20, Ntheta=40):
    r_pts = eps * np.linspace(0.05, 0.95, Nr)
    theta_pts = np.linspace(0, 2*np.pi, Ntheta, endpoint=False)
    R, Theta = np.meshgrid(r_pts, theta_pts, indexing='ij')
    dr = r_pts[1] - r_pts[0]
    dtheta = theta_pts[1] - theta_pts[0]
    W = R * dr * dtheta
    return R.ravel(), Theta.ravel(), R.ravel()*np.cos(Theta.ravel()), \
           R.ravel()*np.sin(Theta.ravel()), W.ravel()


def analyze_coupling_per_mode(N, eps, max_m=8):
    """
    Decompose the center-shape coupling by angular mode m.
    Show that dominant coupling is to m=2 (quadrupole).
    """
    z = ring_positions(N)
    zx, zy = z.real, z.imag
    _, Theta_flat, gx, gy, weights = polar_grid(eps)
    n_grid = len(gx)

    print(f"N={N}, ε={eps}, d_min={d_min_val(N):.4f}")
    print(f"{'mode m':>8s}  {'‖coupling‖':>12s}  {'λ_m(H_ss)':>12s}  {'ratio':>12s}")

    for m in range(2, max_m+1):
        # Basis function: cos(mθ), normalized
        f = np.cos(m * Theta_flat)
        nrm = np.sqrt(np.sum(f**2 * weights))
        if nrm < 1e-14:
            continue
        f_norm = f / nrm

        # Coupling: H_cs[x_0, mode m of blob 1]
        # (representative pair: blob 0 center, blob 1 shape)
        j, k = 0, 1
        abs_x = gx + zx[k]
        abs_y = gy + zy[k]
        dx = zx[j] - abs_x
        dy = zy[j] - abs_y
        r2_reg = dx**2 + dy**2 + 2*eps**2
        dGdx = -(1/(2*np.pi)) * dx / r2_reg
        dGdy = -(1/(2*np.pi)) * dy / r2_reg

        coup_x = np.sum(f_norm * dGdx * weights)
        coup_y = np.sum(f_norm * dGdy * weights)
        coup_norm = np.sqrt(coup_x**2 + coup_y**2)

        # H_ss eigenvalue for this mode (self-energy)
        # G_ij on the disk, projected onto mode m
        G_mat = np.zeros((n_grid, n_grid))
        for i in range(n_grid):
            dx_g = gx[i] - gx
            dy_g = gy[i] - gy
            r2 = dx_g**2 + dy_g**2 + 2*eps**2  # regularized
            G_mat[i, :] = -np.log(r2) / (4*np.pi)

        fw = f_norm * weights
        hss_val = fw @ G_mat @ fw  # ⟨f, G f⟩_w

        ratio = coup_norm**2 / hss_val if hss_val > 1e-20 else np.inf

        print(f"{m:>8d}  {coup_norm:>12.4e}  {hss_val:>12.4e}  {ratio:>12.4e}")


def verify_coupling_scaling():
    """
    Verify coupling_m ~ ε^{m+1} by varying ε for fixed mode m.
    """
    N = 6
    print(f"\n=== Coupling scaling verification, N={N} ===")

    for m in [2, 3, 4]:
        eps_vals = [0.15, 0.10, 0.07, 0.05, 0.03, 0.02]
        coups = []
        for eps in eps_vals:
            z = ring_positions(N)
            zx, zy = z.real, z.imag
            _, Theta_flat, gx, gy, weights = polar_grid(eps)

            f = np.cos(m * Theta_flat)
            nrm = np.sqrt(np.sum(f**2 * weights))
            f_norm = f / nrm

            j, k = 0, 1
            abs_x = gx + zx[k]
            abs_y = gy + zy[k]
            dx = zx[j] - abs_x
            dy = zy[j] - abs_y
            r2_reg = dx**2 + dy**2 + 2*eps**2
            dGdx = -(1/(2*np.pi)) * dx / r2_reg
            coup_x = np.sum(f_norm * dGdx * weights)
            coups.append(abs(coup_x))

        coups = np.array(coups)
        eps_vals = np.array(eps_vals)
        # Fit power law
        valid = coups > 0
        if np.sum(valid) >= 2:
            p = np.polyfit(np.log(eps_vals[valid]), np.log(coups[valid]), 1)[0]
            print(f"mode m={m}: coupling ~ ε^{p:.2f} (expected ε^{m+1}={m+1})")
            for i in range(len(eps_vals)):
                print(f"  ε={eps_vals[i]:.3f}  coupling={coups[i]:.4e}")


def verify_hss_eigenvalue_scaling():
    """
    Verify λ_m(H_ss) ~ ε² for each angular mode m.
    """
    print(f"\n=== H_ss eigenvalue scaling ===")

    for m in [2, 3, 4]:
        eps_vals = [0.15, 0.10, 0.07, 0.05, 0.03, 0.02]
        hss_vals = []
        for eps in eps_vals:
            _, Theta_flat, gx, gy, weights = polar_grid(eps)
            n_grid = len(gx)

            f = np.cos(m * Theta_flat)
            nrm = np.sqrt(np.sum(f**2 * weights))
            f_norm = f / nrm

            G_mat = np.zeros((n_grid, n_grid))
            for i in range(n_grid):
                dx_g = gx[i] - gx
                dy_g = gy[i] - gy
                r2 = dx_g**2 + dy_g**2 + 2*eps**2
                G_mat[i, :] = -np.log(r2) / (4*np.pi)

            fw = f_norm * weights
            hss_val = fw @ G_mat @ fw
            hss_vals.append(hss_val)

        hss_vals = np.array(hss_vals)
        eps_vals = np.array(eps_vals)
        valid = hss_vals > 0
        if np.sum(valid) >= 2:
            p = np.polyfit(np.log(eps_vals[valid]), np.log(hss_vals[valid]), 1)[0]
            print(f"mode m={m}: λ(H_ss) ~ ε^{p:.2f} (expected ε^2)")
            for i in range(len(eps_vals)):
                print(f"  ε={eps_vals[i]:.3f}  λ={hss_vals[i]:.4e}")


def verify_schur_contribution_scaling():
    """
    Verify that mode-m Schur contribution ~ ε^{2m}.
    Leading m=2 gives ε⁴.
    """
    N = 6
    print(f"\n=== Mode-resolved Schur contribution scaling, N={N} ===")

    for m in [2, 3, 4]:
        eps_vals = [0.15, 0.10, 0.07, 0.05, 0.03, 0.02]
        contribs = []
        for eps in eps_vals:
            z = ring_positions(N)
            zx, zy = z.real, z.imag
            _, Theta_flat, gx, gy, weights = polar_grid(eps)
            n_grid = len(gx)

            f = np.cos(m * Theta_flat)
            nrm = np.sqrt(np.sum(f**2 * weights))
            f_norm = f / nrm

            # Coupling
            j, k = 0, 1
            abs_x = gx + zx[k]
            abs_y = gy + zy[k]
            dx = zx[j] - abs_x
            dy = zy[j] - abs_y
            r2_reg = dx**2 + dy**2 + 2*eps**2
            dGdx = -(1/(2*np.pi)) * dx / r2_reg
            coup = np.sum(f_norm * dGdx * weights)

            # H_ss
            G_mat = np.zeros((n_grid, n_grid))
            for i in range(n_grid):
                dx_g = gx[i] - gx
                dy_g = gy[i] - gy
                r2 = dx_g**2 + dy_g**2 + 2*eps**2
                G_mat[i, :] = -np.log(r2) / (4*np.pi)

            fw = f_norm * weights
            hss_val = fw @ G_mat @ fw

            contrib = coup**2 / hss_val if hss_val > 1e-20 else np.nan
            contribs.append(contrib)

        contribs = np.array(contribs)
        eps_vals = np.array(eps_vals)
        valid = np.isfinite(contribs) & (contribs > 0)
        if np.sum(valid) >= 2:
            p = np.polyfit(np.log(eps_vals[valid]), np.log(contribs[valid]), 1)[0]
            print(f"mode m={m}: contribution ~ ε^{p:.2f} (expected ε^{2*m})")
            for i in range(len(eps_vals)):
                print(f"  ε={eps_vals[i]:.3f}  contrib={contribs[i]:.4e}")


if __name__ == "__main__":
    for N in [4, 6]:
        analyze_coupling_per_mode(N, eps=0.05, max_m=6)
        print()

    verify_coupling_scaling()
    verify_hss_eigenvalue_scaling()
    verify_schur_contribution_scaling()
