"""
Numerical oracle for Proposition 17 (inertia preservation).

Strategy: discretize the full Hessian of E[ω_ε] + μ_L L[ω_ε] on a
finite-dimensional space (center translations + angular shape modes),
compute the block structure, and verify:

  1. H_ss is positive definite (self-energy Hessian on shape modes)
  2. Schur complement S = H_cc - H_cs H_ss^{-1} H_cs^T has the same
     inertia as H_cc (the point vortex Havelock Hessian)
  3. The correction ‖H_cs H_ss^{-1} H_cs^T‖ → 0 as ε → 0
  4. Identify the correct ε₀(N) threshold

Uses Cauchy blob: φ_ε(x) = (ε/π) / (|x|² + ε²)
Regularized Green's function: G_ε(x,y) = -(1/4π) ln(|x-y|² + 2ε²)

No scipy required — numpy only.  All loops vectorized.
"""
import numpy as np
from numpy.linalg import eigh, norm, solve


# ──────────────────────────────────────────────
# Ring geometry
# ──────────────────────────────────────────────

def ring_positions(N):
    """Unit-circle N-gon vertices as complex array."""
    return np.exp(2j * np.pi * np.arange(N) / N)


def d_min_val(N):
    """Minimum inter-vortex distance on unit circle."""
    return 2 * np.sin(np.pi / N)


# ──────────────────────────────────────────────
# Havelock eigenvalues (ground truth)
# ──────────────────────────────────────────────

def havelock_eigenvalues_direct(N):
    """
    Point vortex constrained Hessian eigenvalues on the unit circle.
    Returns the 2N-4 non-trivial eigenvalues (sorted ascending).
    """
    z = ring_positions(N)
    zx, zy = z.real, z.imag
    H = np.zeros((2*N, 2*N))

    for j in range(N):
        for k in range(N):
            if j == k:
                continue
            dx = zx[j] - zx[k]
            dy = zy[j] - zy[k]
            r2 = dx**2 + dy**2
            r4 = r2**2

            # G = -(1/4π) ln(r²) => G_xx = -(1/2π)(r²-2dx²)/r⁴, etc.
            Gxx = -(1/(2*np.pi)) * (r2 - 2*dx**2) / r4
            Gyy = -(1/(2*np.pi)) * (r2 - 2*dy**2) / r4
            Gxy =  (1/(2*np.pi)) * 2*dx*dy / r4

            H[j, k] += Gxx;       H[j, k+N] += Gxy
            H[j+N, k] += Gxy;     H[j+N, k+N] += Gyy
            H[j, j] -= Gxx;       H[j, j+N] -= Gxy
            H[j+N, j] -= Gxy;     H[j+N, j+N] -= Gyy

    # Project out translations (2), rotation (1), radial/constraint (1)
    t1 = np.zeros(2*N); t1[:N] = 1; t1 /= norm(t1)
    t2 = np.zeros(2*N); t2[N:] = 1; t2 /= norm(t2)
    rot = np.zeros(2*N); rot[:N] = -zy; rot[N:] = zx; rot /= norm(rot)
    rad = np.zeros(2*N); rad[:N] = zx; rad[N:] = zy; rad /= norm(rad)
    modes = np.column_stack([t1, t2, rot, rad])
    P = np.eye(2*N) - modes @ modes.T
    H_proj = P @ H @ P

    evals = np.sort(eigh(H_proj)[0])
    return evals[4:]


# ──────────────────────────────────────────────
# Polar grid + shape basis on a single disk
# ──────────────────────────────────────────────

def polar_grid(eps, Nr=16, Ntheta=32):
    """
    Polar grid on disk of radius ε.
    Returns (x, y, weights) as 1D arrays of length Nr*Ntheta.
    """
    # Gauss-type radial spacing (cluster near center for better accuracy)
    r_pts = eps * np.linspace(0.05, 0.95, Nr)
    theta_pts = np.linspace(0, 2*np.pi, Ntheta, endpoint=False)
    R, Theta = np.meshgrid(r_pts, theta_pts, indexing='ij')
    dr = r_pts[1] - r_pts[0]
    dtheta = theta_pts[1] - theta_pts[0]
    W = R * dr * dtheta
    return R.ravel(), Theta.ravel(), R.ravel() * np.cos(Theta.ravel()), \
           R.ravel() * np.sin(Theta.ravel()), W.ravel()


def shape_basis(Theta_flat, weights, N_modes=4):
    """
    Angular Fourier basis for mean-zero, center-preserving perturbations.
    Modes m = 2, 3, ..., N_modes+1 (skip m=0 mean, m=1 dipole).
    Returns (n_basis, n_grid) array, each row L²-normalized.
    """
    basis_list = []
    for m in range(2, N_modes + 2):
        for func in [np.cos, np.sin]:
            f = func(m * Theta_flat)
            nrm = np.sqrt(np.sum(f**2 * weights))
            if nrm > 1e-14:
                basis_list.append(f / nrm)
    return np.array(basis_list)


# ──────────────────────────────────────────────
# Green's function matrix (vectorized)
# ──────────────────────────────────────────────

def green_matrix(x1, y1, x2, y2, eps=0.0):
    """
    G_ij = -(1/4π) ln(|r_i - r_j|² + 2ε²).
    x1, y1: (n,) source points; x2, y2: (m,) target points.
    Returns (n, m) matrix.
    """
    dx = x1[:, None] - x2[None, :]   # (n, m)
    dy = y1[:, None] - y2[None, :]
    r2 = dx**2 + dy**2 + 2 * eps**2
    return -np.log(r2) / (4 * np.pi)


# ──────────────────────────────────────────────
# H_ss: self-energy Hessian (per blob, vectorized)
# ──────────────────────────────────────────────

def compute_Hss_block(basis, gx, gy, weights, eps):
    """
    H_ss for a single blob: (n_basis × n_basis).
    H_ss[a,b] = ∫∫ f_a(x) G(x,y) f_b(y) w(x) w(y) dx dy
    where G is the 2D Green's function (regularized at coincident points).
    """
    n_grid = len(gx)
    # Build Green's matrix between grid points
    G = green_matrix(gx, gy, gx, gy, eps=eps)

    # Weight the basis functions: basis_w[a, i] = basis[a, i] * sqrt(w[i])
    # Then H_ss[a,b] = (basis_w @ G_w @ basis_w.T)[a,b]
    # where G_w[i,j] = G[i,j] * w[i] * w[j]
    # Actually: H_ss[a,b] = Σ_{ij} basis[a,i] * G[i,j] * basis[b,j] * w[i] * w[j]
    #                      = (basis * w) @ G @ (basis * w).T
    BW = basis * weights[None, :]  # (n_basis, n_grid)
    return BW @ G @ BW.T


# ──────────────────────────────────────────────
# H_cs: center-shape coupling (vectorized)
# ──────────────────────────────────────────────

def compute_Hcs_block(j, k, zx, zy, basis_k, gx_k, gy_k, weights_k, eps):
    """
    Coupling between center displacement of blob j and shape modes of blob k.

    H_cs[x_j, α_b^k] = ∫ (∂G/∂x_j)(z_j, x') f_b(x' - z_k) w(x') dx'

    where x' runs over grid points of blob k.
    Returns (2, n_basis) array: rows = (x_j, y_j) components.
    """
    # Grid points of blob k in absolute coordinates
    abs_x = gx_k + zx[k]
    abs_y = gy_k + zy[k]

    dx = zx[j] - abs_x   # (n_grid,)
    dy = zy[j] - abs_y
    r2_reg = dx**2 + dy**2 + 2*eps**2

    # ∂G_ε/∂x_j = -(1/2π) dx / (r² + 2ε²)
    dGdx = -(1/(2*np.pi)) * dx / r2_reg   # (n_grid,)
    dGdy = -(1/(2*np.pi)) * dy / r2_reg

    BW = basis_k * weights_k[None, :]  # (n_basis, n_grid)

    coupling_x = BW @ dGdx   # (n_basis,)
    coupling_y = BW @ dGdy

    return np.vstack([coupling_x, coupling_y])  # (2, n_basis)


# ──────────────────────────────────────────────
# Full assembly
# ──────────────────────────────────────────────

def assemble_hessian(N, eps, N_shape_modes=4, Nr=16, Ntheta=32):
    """
    Build the full block Hessian:
      H = [[H_cc, H_cs], [H_cs^T, H_ss]]

    Returns H_cc (2N×2N), H_cs (2N×dim_s), H_ss (dim_s×dim_s).
    """
    z = ring_positions(N)
    zx, zy = z.real, z.imag

    # Grid and basis (same for all blobs by Z_N symmetry)
    _, Theta_flat, gx, gy, weights = polar_grid(eps, Nr, Ntheta)
    basis = shape_basis(Theta_flat, weights, N_shape_modes)
    n_basis = basis.shape[0]
    dim_s = n_basis * N

    # --- H_cc: point vortex Hessian (exact) ---
    H_cc = np.zeros((2*N, 2*N))
    for j in range(N):
        for k in range(N):
            if j == k:
                continue
            dx = zx[j] - zx[k]
            dy = zy[j] - zy[k]
            r2 = dx**2 + dy**2
            r4 = r2**2
            Gxx = -(1/(2*np.pi)) * (r2 - 2*dx**2) / r4
            Gyy = -(1/(2*np.pi)) * (r2 - 2*dy**2) / r4
            Gxy =  (1/(2*np.pi)) * 2*dx*dy / r4
            H_cc[j, k] += Gxx;       H_cc[j, k+N] += Gxy
            H_cc[j+N, k] += Gxy;     H_cc[j+N, k+N] += Gyy
            H_cc[j, j] -= Gxx;       H_cc[j, j+N] -= Gxy
            H_cc[j+N, j] -= Gxy;     H_cc[j+N, j+N] -= Gyy

    # --- H_ss: self-energy blocks (block-diagonal by blob) ---
    Hss_one = compute_Hss_block(basis, gx, gy, weights, eps)
    H_ss = np.zeros((dim_s, dim_s))
    for j in range(N):
        s, e = j*n_basis, (j+1)*n_basis
        H_ss[s:e, s:e] = Hss_one

    # Also add inter-blob shape-shape coupling (usually negligible)
    # Skip for now — these are O(ε²/d_min²) relative to self-energy

    # --- H_cs: center-shape coupling ---
    H_cs = np.zeros((2*N, dim_s))
    for j in range(N):
        for k in range(N):
            if j == k:
                continue
            block = compute_Hcs_block(j, k, zx, zy, basis, gx, gy, weights, eps)
            # block is (2, n_basis): coupling of (x_j, y_j) to shape modes of k
            s = k * n_basis
            H_cs[j,   s:s+n_basis] += block[0, :]
            H_cs[j+N, s:s+n_basis] += block[1, :]

    return H_cc, H_cs, H_ss


# ──────────────────────────────────────────────
# Inertia computation
# ──────────────────────────────────────────────

def inertia(evals, tol=1e-10):
    """(positive, zero, negative) eigenvalue counts."""
    return (int(np.sum(evals > tol)),
            int(np.sum(np.abs(evals) <= tol)),
            int(np.sum(evals < -tol)))


def constrained_projection(N):
    """Projector onto constrained subspace (remove translations, rotation, radial)."""
    z = ring_positions(N)
    zx, zy = z.real, z.imag
    t1 = np.zeros(2*N); t1[:N] = 1; t1 /= norm(t1)
    t2 = np.zeros(2*N); t2[N:] = 1; t2 /= norm(t2)
    rot = np.zeros(2*N); rot[:N] = -zy; rot[N:] = zx; rot /= norm(rot)
    rad = np.zeros(2*N); rad[:N] = zx; rad[N:] = zy; rad /= norm(rad)
    modes = np.column_stack([t1, t2, rot, rad])
    return np.eye(2*N) - modes @ modes.T


# ──────────────────────────────────────────────
# Main oracle
# ──────────────────────────────────────────────

def verify_inertia(N, eps_values=None):
    """
    Core verification: for each ε, check that Schur complement inertia
    matches point vortex Havelock inertia.
    """
    if eps_values is None:
        eps_values = [0.3, 0.2, 0.1, 0.05, 0.02]

    dm = d_min_val(N)
    P = constrained_projection(N)

    # Ground truth
    hav = havelock_eigenvalues_direct(N)
    hav_in = inertia(hav)
    print(f"=== N = {N}, d_min = {dm:.4f} ===")
    print(f"Havelock eigenvalues: {np.round(hav, 6)}")
    print(f"Havelock inertia (p,z,n): {hav_in}")
    print()

    results = []

    for eps in eps_values:
        ratio = eps / dm
        H_cc, H_cs, H_ss = assemble_hessian(N, eps)

        # 1. Check H_ss > 0
        ss_evals = np.sort(eigh(H_ss)[0])
        ss_min = ss_evals[0]

        # 2. Schur complement (only if H_ss > 0)
        if ss_min > 1e-14:
            correction = H_cs @ solve(H_ss, H_cs.T)
            S = H_cc - correction
            S_proj = P @ S @ P
            s_evals = np.sort(eigh(S_proj)[0])[4:]
            s_in = inertia(s_evals)
            corr_norm = np.max(np.abs(eigh(correction)[0]))
            match = (s_in == hav_in)
        else:
            s_evals = None
            s_in = None
            corr_norm = None
            match = False

        print(f"ε={eps:.3f}  ε/d={ratio:.3f}  λ_min(H_ss)={ss_min:.4e}"
              f"  ‖corr‖={corr_norm:.4e}" if corr_norm is not None else
              f"ε={eps:.3f}  ε/d={ratio:.3f}  λ_min(H_ss)={ss_min:.4e}  H_ss NOT pos def")
        if s_in is not None:
            print(f"  Schur inertia: {s_in}  match={match}")
            print(f"  Schur evals: {np.round(s_evals, 6)}")
        print()

        results.append({
            'eps': eps, 'ratio': ratio,
            'ss_min': ss_min, 'corr_norm': corr_norm,
            'match': match, 's_in': s_in
        })

    return results


def scaling_test(N):
    """
    Test the ε-scaling of the correction term.
    If ‖correction‖ ~ ε^p, find p.
    """
    dm = d_min_val(N)
    eps_vals = np.array([0.15, 0.10, 0.07, 0.05, 0.03, 0.02])
    norms = []
    ss_mins = []

    print(f"\n=== Scaling test for N = {N} ===")
    for eps in eps_vals:
        H_cc, H_cs, H_ss = assemble_hessian(N, eps)
        ss_evals = eigh(H_ss)[0]
        ss_min = np.min(ss_evals)
        ss_mins.append(ss_min)

        if ss_min > 1e-14:
            correction = H_cs @ solve(H_ss, H_cs.T)
            cn = np.max(np.abs(eigh(correction)[0]))
        else:
            cn = np.nan
        norms.append(cn)

    norms = np.array(norms)
    ss_mins = np.array(ss_mins)

    # Fit power law: log(norm) = p*log(eps) + const
    valid = np.isfinite(norms) & (norms > 0)
    if np.sum(valid) >= 2:
        log_e = np.log(eps_vals[valid])
        log_n = np.log(norms[valid])
        p = np.polyfit(log_e, log_n, 1)[0]

        log_s = np.log(ss_mins[valid])
        p_ss = np.polyfit(log_e, log_s, 1)[0]

        print(f"{'eps':>8s}  {'‖corr‖':>12s}  {'λ_min(H_ss)':>12s}")
        for i, eps in enumerate(eps_vals):
            print(f"{eps:8.4f}  {norms[i]:12.4e}  {ss_mins[i]:12.4e}")
        print(f"\n‖correction‖ ~ ε^{p:.2f}")
        print(f"λ_min(H_ss) ~ ε^{p_ss:.2f}")
    else:
        print("Not enough valid data points for scaling fit")


if __name__ == "__main__":
    # Havelock verification
    print("=== Havelock eigenvalue verification ===")
    for N in range(3, 9):
        evals = havelock_eigenvalues_direct(N)
        formula = [(N-1) - m*(N-m)/2 for m in range(1, N//2 + 1)]
        print(f"N={N}: computed={np.round(evals, 4)}, formula={formula}")
    print()

    # Main inertia verification
    for N in [4, 5, 6, 7]:
        verify_inertia(N, eps_values=[0.2, 0.1, 0.05, 0.02])
        print("=" * 60)

    # Scaling test
    for N in [4, 5, 6]:
        scaling_test(N)
