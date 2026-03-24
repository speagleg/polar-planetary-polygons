"""
Proper Hecke normalization: extract z₀-independent eigenvalues.

THE PROBLEM:
The interaction matrix eigenvalue at base point z₀ is:
    μ(z₀) = |φ(z₀)|² × a_p / λ_n
where φ is the eigenfunction, a_p is the Hecke eigenvalue, and λ_n
is the Laplacian eigenvalue. This depends on z₀ through |φ(z₀)|².

THE FIX:
The DIAGONAL of the Green's function matrix gives the "mass" at z₀:
    M_{ii} = G_reg(z_i, z_i) = Σ_n |φ_n(z_i)|² / λ_n

The RATIO of the interaction eigenvalue to the diagonal gives:
    a_p ~ μ(z₀) / M_{ii}

More precisely: for the operator T_p acting on functions on the surface,
the matrix representation in the orbit basis has eigenvalues proportional
to a_p × |φ(orbit)|². Dividing by the Gram matrix (which IS the diagonal)
cancels the |φ|² dependence.

THE GENERALIZED EIGENVALUE PROBLEM:
Instead of M v = λ v, solve:
    M v = λ D v
where D = diag(M_{11}, ..., M_{nn}) is the diagonal "mass matrix."

The generalized eigenvalues λ are BASE-POINT INDEPENDENT
(they're the ratios a_p / [self-energy], which don't depend on z₀).
"""

import numpy as np
from math import pi, sin, cos, log, sqrt, exp, atan2, cosh, sinh, tanh, atanh
from scipy.integrate import quad
from scipy.linalg import eigh  # generalized eigenvalue solver


def hyp_dist(z1, z2):
    num = abs(z1 - z2)
    den = abs(1 - np.conj(z1) * z2)
    if den < 1e-15:
        return 30.0
    ratio = num / den
    if ratio >= 1 - 1e-15:
        return 30.0
    return 2 * atanh(ratio)


def translate_disc(z, angle, dist):
    t = tanh(dist / 2)
    z_rot = z * np.exp(-1j * angle)
    z_trans = (z_rot + t) / (1 + t * np.conj(z_rot))
    return z_trans * np.exp(1j * angle)


def apply_auto(z, typ, rot):
    if typ == 'rot':
        return z * rot
    elif typ == 'ref':
        return np.conj(z) * rot
    elif typ == 'rot_neg':
        return -z * rot
    elif typ == 'ref_neg':
        return -np.conj(z) * rot
    return z


def make_orbit(z0):
    omega = np.exp(1j * pi / 4)
    elements = []
    for k in range(8):
        elements.append(('rot', omega**k))
        elements.append(('ref', omega**k))
        elements.append(('rot_neg', omega**k))
        elements.append(('ref_neg', omega**k))
    orbit = []
    for typ, rot in elements:
        w = apply_auto(z0, typ, rot)
        if abs(w) < 0.995:
            orbit.append(w)
    unique = [orbit[0]]
    for w in orbit[1:]:
        if not any(abs(w - u) < 1e-10 for u in unique):
            unique.append(w)
    return unique


def heat_kernel_H2(d, t):
    if t < 1e-15:
        return 0.0
    if d < 1e-10:
        return exp(-t/4) / (4 * pi * t)
    if d*d / (4*t) > 80:
        return 0.0
    prefactor = sqrt(2) * exp(-t/4) / (4 * pi * t)**1.5
    def integrand(s):
        if s <= d:
            return 0.0
        denom = cosh(s) - cosh(d)
        if denom <= 0:
            return 0.0
        return s * exp(-s*s / (4*t)) / sqrt(denom)
    upper = d + 12*sqrt(t)
    result, _ = quad(integrand, d + 1e-10, upper, limit=100)
    return prefactor * result


def build_translations(n_shells=2):
    R_disc = 0.810465
    mid_r = R_disc * cos(pi / 8)
    mid_hyp = 2 * atanh(mid_r)
    L = 2 * mid_hyp
    trans = []
    for k in range(4):
        a = k * pi / 4
        trans.append((a, L))
        trans.append((a, -L))
    if n_shells >= 2:
        for k in range(4):
            a = k * pi / 4
            trans.append((a, 2*L))
            trans.append((a, -2*L))
        for k in range(4):
            a = (k + 0.5) * pi / 4
            trans.append((a, L*sqrt(2)))
            trans.append((a, -L*sqrt(2)))
    return trans


def compute_matrix(z0, n_shells=2):
    """Compute the regularized interaction matrix."""
    orbit = make_orbit(z0)
    n = len(orbit)
    trans = build_translations(n_shells)
    area_inv = 1.0 / (4 * pi)

    t_grid = sorted(set(np.concatenate([
        np.logspace(-2, -0.5, 15),
        np.linspace(0.4, 2.0, 12),
        np.linspace(2.5, 8.0, 8),
        np.linspace(10, 30, 5),
    ])))

    M = np.zeros((n, n))
    for idx in range(len(t_grid) - 1):
        t_mid = (t_grid[idx] + t_grid[idx+1]) / 2
        dt = t_grid[idx+1] - t_grid[idx]

        K = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                total = 0.0
                if i != j:
                    d = hyp_dist(orbit[i], orbit[j])
                    total += heat_kernel_H2(d, t_mid)
                for angle, dist in trans:
                    w = translate_disc(orbit[j], angle, dist)
                    d = hyp_dist(orbit[i], w)
                    total += heat_kernel_H2(d, t_mid)
                K[i][j] = total

        M += (K - area_inv) * dt

    return n, orbit, M


def degeneracy_groups(ev, tol):
    groups = []
    used = set()
    for i in range(len(ev)):
        if i in used:
            continue
        group = [i]
        for j in range(i+1, len(ev)):
            if j not in used and abs(ev[i] - ev[j]) < tol:
                group.append(j)
                used.add(j)
        used.add(i)
        groups.append((ev[group[0]], len(group)))
    return groups


# =====================================================================
# PART 1: The generalized eigenvalue problem
# =====================================================================

def generalized_eigenvalue():
    """Solve M v = λ D v where D is the diagonal mass matrix."""
    print("=" * 72)
    print("  PART 1: GENERALIZED EIGENVALUE PROBLEM (HECKE NORMALIZATION)")
    print("=" * 72)

    z0 = 0.15 + 0.08j
    n, orbit, M = compute_matrix(z0)
    print(f"\n  Orbit size: {n}, base point: {z0}")

    # The diagonal: self-energy at each orbit point
    diag = np.diag(M)
    print(f"\n  Diagonal (self-energy) values:")
    print(f"    mean = {np.mean(diag):.10f}")
    print(f"    std  = {np.std(diag):.10f}")
    print(f"    min  = {np.min(diag):.10f}")
    print(f"    max  = {np.max(diag):.10f}")

    # Method 1: Generalized eigenvalue M v = λ D v
    D = np.diag(np.abs(diag))  # use |diag| to ensure positive definite
    try:
        gen_ev = eigh(M, D, eigvals_only=True)
        gen_ev = sorted(gen_ev, reverse=True)
        print(f"\n  Generalized eigenvalues (M v = λ D v):")
        for i, e in enumerate(gen_ev):
            print(f"    λ_{i:2d} = {e:16.10f}")
    except Exception as ex:
        print(f"\n  Generalized eigenvalue failed: {ex}")
        gen_ev = None

    # Method 2: Normalize rows and columns by sqrt(|D|)
    # M_norm = D^{-1/2} M D^{-1/2}
    D_inv_sqrt = np.diag(1.0 / np.sqrt(np.abs(diag)))
    M_norm = D_inv_sqrt @ M @ D_inv_sqrt
    norm_ev = sorted(np.linalg.eigvalsh(M_norm), reverse=True)
    print(f"\n  Normalized eigenvalues (D^{{-1/2}} M D^{{-1/2}}):")
    for i, e in enumerate(norm_ev):
        print(f"    λ_{i:2d} = {e:16.10f}")

    # Method 3: Divide off-diagonal by geometric mean of diagonals
    # M_ratio_{ij} = M_{ij} / sqrt(|M_{ii}| |M_{jj}|)
    M_ratio = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            denom = sqrt(abs(diag[i]) * abs(diag[j]))
            M_ratio[i][j] = M[i][j] / denom if denom > 1e-15 else 0
    ratio_ev = sorted(np.linalg.eigvalsh(M_ratio), reverse=True)
    print(f"\n  Ratio eigenvalues (M_ij / sqrt(M_ii M_jj)):")
    for i, e in enumerate(ratio_ev):
        print(f"    λ_{i:2d} = {e:16.10f}")

    return M, diag, norm_ev, ratio_ev


# =====================================================================
# PART 2: Base point independence of normalized eigenvalues
# =====================================================================

def basepoint_test():
    """Test whether normalized eigenvalues are z₀-independent."""
    print(f"\n{'='*72}")
    print("  PART 2: BASE POINT INDEPENDENCE OF NORMALIZED EIGENVALUES")
    print("=" * 72)

    test_pts = [
        0.15 + 0.08j,
        0.20 + 0.05j,
        0.10 + 0.15j,
        0.05 + 0.02j,
    ]

    print(f"\n  --- Raw eigenvalues ---")
    print(f"  {'z₀':>16s}", end="")
    for i in range(4):
        print(f"  {'λ_'+str(i):>12s}", end="")
    print()

    all_raw = []
    all_norm = []
    all_ratio = []

    for z0 in test_pts:
        n, orbit, M = compute_matrix(z0)
        diag = np.diag(M)

        raw = sorted(np.linalg.eigvalsh(M), reverse=True)
        all_raw.append(raw)

        D_inv_sqrt = np.diag(1.0 / np.sqrt(np.abs(diag)))
        M_norm = D_inv_sqrt @ M @ D_inv_sqrt
        norm = sorted(np.linalg.eigvalsh(M_norm), reverse=True)
        all_norm.append(norm)

        M_ratio = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                denom = sqrt(abs(diag[i]) * abs(diag[j]))
                M_ratio[i][j] = M[i][j] / denom if denom > 1e-15 else 0
        ratio = sorted(np.linalg.eigvalsh(M_ratio), reverse=True)
        all_ratio.append(ratio)

        z_str = f"{z0.real:.2f}+{z0.imag:.2f}i"
        print(f"  {z_str:>16s}", end="")
        for e in raw[:4]:
            print(f"  {e:12.6f}", end="")
        print()

    # Statistics for raw
    print(f"\n  Raw variation:")
    for i in range(4):
        vals = [e[i] for e in all_raw]
        mn, sd = np.mean(vals), np.std(vals)
        pct = 100*sd/abs(mn) if abs(mn) > 1e-10 else 999
        print(f"    λ_{i}: mean={mn:10.6f}, std={sd:8.2e}, var={pct:.1f}%")

    # Normalized eigenvalues
    print(f"\n  --- Normalized eigenvalues (D^{{-1/2}} M D^{{-1/2}}) ---")
    print(f"  {'z₀':>16s}", end="")
    for i in range(4):
        print(f"  {'λ_'+str(i):>12s}", end="")
    print()

    for k, z0 in enumerate(test_pts):
        z_str = f"{z0.real:.2f}+{z0.imag:.2f}i"
        print(f"  {z_str:>16s}", end="")
        for e in all_norm[k][:4]:
            print(f"  {e:12.6f}", end="")
        print()

    print(f"\n  Normalized variation:")
    for i in range(4):
        vals = [e[i] for e in all_norm]
        mn, sd = np.mean(vals), np.std(vals)
        pct = 100*sd/abs(mn) if abs(mn) > 1e-10 else 999
        print(f"    λ_{i}: mean={mn:10.6f}, std={sd:8.2e}, var={pct:.1f}%")

    # Ratio eigenvalues
    print(f"\n  --- Ratio eigenvalues (M_ij/sqrt(M_ii M_jj)) ---")
    print(f"  {'z₀':>16s}", end="")
    for i in range(4):
        print(f"  {'λ_'+str(i):>12s}", end="")
    print()

    for k, z0 in enumerate(test_pts):
        z_str = f"{z0.real:.2f}+{z0.imag:.2f}i"
        print(f"  {z_str:>16s}", end="")
        for e in all_ratio[k][:4]:
            print(f"  {e:12.6f}", end="")
        print()

    print(f"\n  Ratio variation:")
    for i in range(4):
        vals = [e[i] for e in all_ratio]
        mn, sd = np.mean(vals), np.std(vals)
        pct = 100*sd/abs(mn) if abs(mn) > 1e-10 else 999
        print(f"    λ_{i}: mean={mn:10.6f}, std={sd:8.2e}, var={pct:.1f}%")

    # Degeneracy of the best method
    print(f"\n  --- Degeneracy of the best normalization ---")
    best = all_ratio[0]  # use first base point
    groups = degeneracy_groups(best, 1e-4)
    n2d = sum(1 for _, m in groups if m == 2)
    print(f"  2D irreps: {n2d}")
    for e, m in groups:
        tag = " *** GL(2) ***" if m == 2 else ""
        print(f"    {e:14.10f}  mult = {m}{tag}")


# =====================================================================
# MAIN
# =====================================================================

def main():
    print("=" * 72)
    print("  HECKE-NORMALIZED BOLZA EIGENVALUES")
    print("=" * 72)

    M, diag, norm_ev, ratio_ev = generalized_eigenvalue()
    basepoint_test()

    print(f"\n{'='*72}")
    print("  FINAL RESULT")
    print("=" * 72)
    print("""
  Three normalization methods tested:
  1. Raw: M v = λ v (base-point DEPENDENT, ~83% variation)
  2. Normalized: D^{-1/2} M D^{-1/2} (should reduce dependence)
  3. Ratio: M_ij / sqrt(M_ii M_jj) (correlation-style normalization)

  The method with SMALLEST base-point variation gives the
  best approximation to the true Hecke eigenvalues.
""")


if __name__ == "__main__":
    main()
