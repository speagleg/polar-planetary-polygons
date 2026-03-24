"""
Heat kernel regularization of the Bolza vortex interaction matrix.

THE PROBLEM:
The Havelock kernel S(d) = -log(2sinh(d/2)) grows linearly for large d.
The lattice sum Σ_γ S(d(z, γw)) DIVERGES.

THE SOLUTION:
Use the HEAT KERNEL to regularize. The heat kernel on H²:

    K_{H²}(d, t) = (sqrt(2)/(4πt)^{3/2}) * e^{-t/4} * ∫_d^∞ r e^{-r²/(4t)} / sqrt(cosh(r) - cosh(d)) dr

decays as e^{-d²/(4t)} for large d -> EXPONENTIAL convergence of lattice sum.

The regularized Green's function:
    G_reg(z, w) = ∫_0^∞ [K_Bolza(z, w; t) - 1/Area] dt

where K_Bolza = Σ_γ K_{H²}(d(z,γw), t) is the Bolza heat kernel.

EQUIVALENTLY: use the spectral representation
    G_reg(z, w) = Σ_{n≥1} φ_n(z) φ_n(w) / λ_n

which converges absolutely (λ_n → ∞).

THIS COMPUTATION:
We use a TRUNCATED heat kernel approach:
1. For each time t: compute K_Bolza(z_i, z_j; t) by lattice sum (converges fast)
2. Integrate over t from ε to T
3. The t-integration gives the regularized Green's function
4. Build the 16×16 matrix and extract GL(2) eigenvalues
"""

import numpy as np
from math import pi, sin, cos, log, sqrt, exp, atan2, cosh, sinh, acosh, tanh, atanh
from scipy.integrate import quad  # type: ignore


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


def build_group():
    omega = np.exp(1j * pi / 4)
    elements = []
    for k in range(8):
        elements.append(('rot', omega**k))
    for k in range(8):
        elements.append(('ref', omega**k))
    for k in range(8):
        elements.append(('rot_neg', omega**k))
    for k in range(8):
        elements.append(('ref_neg', omega**k))
    return elements


def make_orbit(z0, elements):
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


# =====================================================================
# The H² heat kernel
# =====================================================================

def heat_kernel_H2(d, t):
    """Heat kernel on H² at hyperbolic distance d, diffusion time t.

    K(d, t) = (sqrt(2) / (4πt)^{3/2}) * e^{-t/4} * I(d, t)

    where I(d, t) = ∫_d^∞ r * e^{-r²/(4t)} / sqrt(cosh(r) - cosh(d)) dr

    For d = 0: K(0, t) = (1/(4πt)) * e^{-t/4} * Σ (from the expansion)

    Simpler formula for numerical use:
    K(d, t) = (1/(4πt)) * e^{-t/4} * (d/sinh(d)) * e^{-d²/(4t)} * correction

    Actually the standard formula is:
    K(d, t) = (sqrt(2) * e^{-t/4}) / (4*pi*t)^{3/2} * ∫_d^∞ s*e^{-s²/(4t)} / sqrt(cosh(s) - cosh(d)) ds
    """
    if t < 1e-15:
        return 0.0

    if d < 1e-10:
        # At d = 0: use the trace formula K(0,t) ~ (Area)^{-1} + Σ e^{-λ_n t}
        # For the universal cover H²: K(0,t) = e^{-t/4} / (4πt) * [series]
        # Leading: 1/(4πt) for small t
        return exp(-t/4) / (4 * pi * t)

    # Numerical integration of the standard formula
    prefactor = sqrt(2) * exp(-t/4) / (4 * pi * t)**1.5

    # Integrand: s * exp(-s²/(4t)) / sqrt(cosh(s) - cosh(d))
    def integrand(s):
        if s <= d + 1e-15:
            return 0.0
        denom = cosh(s) - cosh(d)
        if denom <= 0:
            return 0.0
        return s * exp(-s*s / (4*t)) / sqrt(denom)

    # The integral from d to infinity
    # For large s: integrand ~ s * exp(-s²/(4t)) * exp(-s/2) / sqrt(2sinh(d))
    # Effectively: Gaussian cutoff at s ~ 2*sqrt(t)
    # Integration range: [d, d + 10*sqrt(t)]
    upper = max(d + 20*sqrt(t), d + 5)

    try:
        result, error = quad(integrand, d + 1e-10, upper, limit=200)
    except Exception:
        # Manual trapezoidal integration
        n_pts = 2000
        ds = (upper - d - 1e-10) / n_pts
        result = 0.0
        for i in range(n_pts + 1):
            s = d + 1e-10 + i * ds
            val = integrand(s)
            weight = 1.0 if (i == 0 or i == n_pts) else 2.0
            result += weight * val
        result *= ds / 2

    return prefactor * result


# =====================================================================
# The regularized Green's function via heat kernel
# =====================================================================

def greens_function_reg(d, t_min=0.01, t_max=20.0, n_t=200):
    """Regularized Green's function via heat kernel integration.

    G_reg(d) = ∫_{t_min}^{t_max} [K_{H²}(d, t) - 1/(4π)] dt

    The subtraction of 1/(4π) = 1/Area_{Bolza} regularizes the integral.
    (Area of the Bolza surface = 4π, so 1/Area = 1/(4π))
    """
    area_inv = 1.0 / (4 * pi)  # 1/Area of Bolza surface

    total = 0.0
    dt = (t_max - t_min) / n_t

    for i in range(n_t + 1):
        t = t_min + i * dt
        K = heat_kernel_H2(d, t)
        integrand = K - area_inv
        weight = 1.0 if (i == 0 or i == n_t) else 2.0
        total += weight * integrand

    total *= dt / 2
    return total


# =====================================================================
# PART 1: Test the heat kernel
# =====================================================================

def test_heat_kernel():
    """Test the H² heat kernel computation."""
    print("=" * 72)
    print("  PART 1: TESTING THE H² HEAT KERNEL")
    print("=" * 72)

    print(f"\n  K(d, t) for various d and t:\n")
    print(f"  {'d':>8s}", end="")
    for t in [0.1, 0.5, 1.0, 2.0, 5.0]:
        print(f"  {'t='+str(t):>12s}", end="")
    print()

    for d in [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 8.0]:
        print(f"  {d:8.2f}", end="")
        for t in [0.1, 0.5, 1.0, 2.0, 5.0]:
            K = heat_kernel_H2(d, t)
            print(f"  {K:12.6f}", end="")
        print()

    # Key property: K(d, t) → 0 exponentially fast for d >> sqrt(t)
    print(f"\n  Decay test: K(d, t=1) for increasing d:")
    for d in [0, 1, 2, 3, 5, 8, 10, 15, 20]:
        K = heat_kernel_H2(d, 1.0)
        print(f"    d={d:3d}: K = {K:.2e}")

    # The regularized Green's function
    print(f"\n  Regularized Green's function G_reg(d):")
    print(f"  (G_reg = ∫ [K(d,t) - 1/4π] dt from t=0.01 to t=20)\n")
    print(f"  {'d':>8s} {'G_reg(d)':>14s} {'Havelock S(d)':>14s} {'ratio':>10s}")

    for d in [0.5, 1.0, 1.5, 2.0, 3.0, 5.0]:
        G = greens_function_reg(d)
        S = -log(2 * sinh(d / 2))
        ratio = G / S if abs(S) > 1e-10 else 0
        print(f"  {d:8.2f} {G:14.6f} {S:14.6f} {ratio:10.4f}")


# =====================================================================
# PART 2: Build the Bolza heat kernel with lattice sum
# =====================================================================

def bolza_heat_kernel_matrix(orbit, t, n_shells=3):
    """Compute the Bolza heat kernel matrix K_{ij}(t) via lattice sum."""
    n = len(orbit)

    # Side-pairing translations
    R_disc = 0.810465
    mid_r = R_disc * cos(pi / 8)
    mid_hyp = 2 * atanh(mid_r)
    trans_dist = 2 * mid_hyp

    # Build translation vectors for n_shells shells
    translations = [(0, 0)]  # identity (for off-diagonal, direct term is handled separately)

    # Shell 1: nearest neighbors (8 translations)
    for k in range(4):
        angle = k * pi / 4
        translations.append((angle, trans_dist))
        translations.append((angle, -trans_dist))

    if n_shells >= 2:
        # Shell 2: next-nearest (double translations + diagonal)
        for k in range(4):
            angle = k * pi / 4
            translations.append((angle, 2 * trans_dist))
            translations.append((angle, -2 * trans_dist))
        # Diagonal translations
        for k in range(4):
            angle = (k + 0.5) * pi / 4
            translations.append((angle, trans_dist * sqrt(2)))
            translations.append((angle, -trans_dist * sqrt(2)))

    if n_shells >= 3:
        # Shell 3
        for k in range(4):
            angle = k * pi / 4
            translations.append((angle, 3 * trans_dist))
            translations.append((angle, -3 * trans_dist))
        for k in range(8):
            angle = k * pi / 4
            translations.append((angle + pi/8, trans_dist * 2))
            translations.append((angle + pi/8, -trans_dist * 2))

    K_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            total = 0.0
            for angle, dist in translations:
                if abs(dist) < 1e-10 and i == j:
                    continue  # skip identity for self-interaction
                if abs(dist) < 1e-10:
                    # Direct term
                    d = hyp_dist(orbit[i], orbit[j])
                else:
                    w_img = translate_disc(orbit[j], angle, dist)
                    d = hyp_dist(orbit[i], w_img)
                total += heat_kernel_H2(d, t)
            K_matrix[i][j] = total

    return K_matrix


# =====================================================================
# PART 3: The regularized interaction matrix
# =====================================================================

def regularized_matrix():
    """Build the regularized 16×16 interaction matrix via heat kernel."""
    print(f"\n{'='*72}")
    print("  PART 2: REGULARIZED INTERACTION MATRIX")
    print("=" * 72)

    elements = build_group()
    z0 = 0.15 + 0.08j
    orbit = make_orbit(z0, elements)
    n = len(orbit)
    print(f"\n  Orbit size: {n}")

    area_inv = 1.0 / (4 * pi)

    # Integrate K(t) - 1/Area over t
    # Use logarithmic spacing in t for better coverage of both small and large t
    t_values = np.concatenate([
        np.linspace(0.05, 0.5, 10),
        np.linspace(0.5, 2.0, 10),
        np.linspace(2.0, 10.0, 10),
        np.linspace(10.0, 30.0, 5),
    ])
    t_values = sorted(set(t_values))

    print(f"  Integrating heat kernel over {len(t_values)} t-values from {t_values[0]:.2f} to {t_values[-1]:.1f}")
    print(f"  Using 3 shells of lattice images")

    M_reg = np.zeros((n, n))

    for idx in range(len(t_values) - 1):
        t_lo = t_values[idx]
        t_hi = t_values[idx + 1]
        t_mid = (t_lo + t_hi) / 2
        dt = t_hi - t_lo

        K_mat = bolza_heat_kernel_matrix(orbit, t_mid, n_shells=2)

        # Subtract 1/Area and integrate
        for i in range(n):
            for j in range(n):
                M_reg[i][j] += (K_mat[i][j] - area_inv) * dt

        if idx % 10 == 0:
            # Progress: show the leading eigenvalue at this point
            ev_temp = sorted(np.linalg.eigvalsh(M_reg), reverse=True)
            print(f"    t = {t_mid:.2f}: leading eigenvalue = {ev_temp[0]:.6f}")

    # Final eigenvalues
    eigenvalues = sorted(np.linalg.eigvalsh(M_reg), reverse=True)

    print(f"\n  Eigenvalues of the regularized {n}×{n} matrix:")
    for i, ev in enumerate(eigenvalues):
        print(f"    λ_{i:2d} = {ev:14.10f}")

    # Degeneracy analysis
    print(f"\n  Degeneracy analysis (tolerance 10^-3):")
    groups = []
    used = set()
    for i in range(n):
        if i in used:
            continue
        group = [i]
        for j in range(i+1, n):
            if j not in used and abs(eigenvalues[i] - eigenvalues[j]) < 1e-3:
                group.append(j)
                used.add(j)
        used.add(i)
        groups.append((eigenvalues[group[0]], len(group)))

    for ev, mult in groups:
        tag = "*** 2D GL(2) ***" if mult == 2 else f"{mult}D"
        print(f"    {ev:14.8f}  mult = {mult}  {tag}")

    n_2d = sum(1 for _, m in groups if m == 2)
    print(f"\n  Total 2D irreps: {n_2d}")

    return M_reg, eigenvalues, groups


# =====================================================================
# PART 4: Base point independence test
# =====================================================================

def basepoint_test():
    """Test whether regularized eigenvalues are base-point independent."""
    print(f"\n{'='*72}")
    print("  PART 3: BASE POINT INDEPENDENCE TEST")
    print("=" * 72)

    elements = build_group()
    area_inv = 1.0 / (4 * pi)

    # Coarser t-grid for speed
    t_values = np.concatenate([
        np.linspace(0.1, 1.0, 5),
        np.linspace(1.0, 5.0, 5),
        np.linspace(5.0, 20.0, 5),
    ])

    test_points = [0.15 + 0.08j, 0.20 + 0.05j, 0.10 + 0.15j, 0.05 + 0.02j]

    print(f"\n  {'z_0':>16s} {'orbit':>6s}", end="")
    for i in range(3):
        print(f"  {'2D_'+str(i+1):>12s}", end="")
    print(f"  {'max 1D':>12s}")

    all_gl2 = []
    for z0 in test_points:
        orbit = make_orbit(z0, elements)
        n = len(orbit)

        M_reg = np.zeros((n, n))
        for idx in range(len(t_values) - 1):
            t_mid = (t_values[idx] + t_values[idx+1]) / 2
            dt = t_values[idx+1] - t_values[idx]
            K_mat = bolza_heat_kernel_matrix(orbit, t_mid, n_shells=2)
            for i in range(n):
                for j in range(n):
                    M_reg[i][j] += (K_mat[i][j] - area_inv) * dt

        ev = sorted(np.linalg.eigvalsh(M_reg), reverse=True)
        groups = []
        used = set()
        for i in range(n):
            if i in used:
                continue
            group = [i]
            for j in range(i+1, n):
                if j not in used and abs(ev[i] - ev[j]) < 5e-3:
                    group.append(j)
                    used.add(j)
            used.add(i)
            groups.append((ev[group[0]], len(group)))

        gl2 = sorted([e for e, m in groups if m == 2], reverse=True)[:3]
        max1d = max([e for e, m in groups if m == 1], default=0)
        all_gl2.append(gl2)

        z_str = f"{z0.real:.2f}+{z0.imag:.2f}i"
        print(f"  {z_str:>16s} {n:6d}", end="")
        for v in gl2:
            print(f"  {v:12.6f}", end="")
        print(f"  {max1d:12.6f}")

    # Statistics
    if all_gl2 and all(len(g) >= 3 for g in all_gl2):
        for i in range(3):
            vals = [g[i] for g in all_gl2]
            mean = np.mean(vals)
            std = np.std(vals)
            pct = 100 * std / abs(mean) if abs(mean) > 1e-10 else 0
            print(f"\n  2D_{i+1}: mean = {mean:.6f}, std = {std:.6f} ({pct:.1f}%)")


# =====================================================================
# MAIN
# =====================================================================

def main():
    print("=" * 72)
    print("  HEAT KERNEL REGULARIZED BOLZA VORTEX COMPUTATION")
    print("=" * 72)

    test_heat_kernel()
    M_reg, eigenvalues, groups = regularized_matrix()
    basepoint_test()

    print(f"\n{'='*72}")
    print("  RESULTS")
    print("=" * 72)

    n_2d = sum(1 for _, m in groups if m == 2)
    gl2_vals = [e for e, m in groups if m == 2]

    print(f"\n  2D irreducible representations: {n_2d}")
    if gl2_vals:
        max_ev = max(e for e, _ in groups)
        C = max_ev / 2.0
        print(f"  Normalization: C = {C:.6f}")
        print(f"\n  Normalized GL(2) Hecke eigenvalues:")
        for i, v in enumerate(sorted(gl2_vals, reverse=True)):
            a = v / C if C > 0 else 0
            print(f"    a_{i+1} = {a:.8f} (|a| = {abs(a):.6f})")


if __name__ == "__main__":
    main()
