"""
Refined heat kernel computation: resolve the 7-fold cluster and test base point independence.

IMPROVEMENTS:
1. Log-spaced t-grid near t=0 (captures short-range structure)
2. More lattice shells for convergence
3. Multiple base points to test invariance
4. Finer degeneracy tolerance to resolve the cluster at -0.2817
5. Use Strohmaier-Uski λ₁ = 3.839 for normalization context
"""

import numpy as np
from math import pi, sin, cos, log, sqrt, exp, atan2, cosh, sinh, acosh, tanh, atanh
from scipy.integrate import quad


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
        elements.append(('ref', omega**k))
        elements.append(('rot_neg', omega**k))
        elements.append(('ref_neg', omega**k))
    return elements


def make_orbit(z0):
    elements = build_group()
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
    """Heat kernel on H² — optimized."""
    if t < 1e-15:
        return 0.0
    if d < 1e-10:
        return exp(-t/4) / (4 * pi * t)
    if d*d / (4*t) > 80:
        return 0.0  # exponentially small

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


# =====================================================================
# Build the translation set for the lattice sum
# =====================================================================

def build_translations(n_shells):
    """Build Γ-image translations for the lattice sum."""
    R_disc = 0.810465
    mid_r = R_disc * cos(pi / 8)
    mid_hyp = 2 * atanh(mid_r)
    L = 2 * mid_hyp  # fundamental translation distance

    trans = []
    # Shell 1: 8 nearest
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

    if n_shells >= 3:
        for k in range(4):
            a = k * pi / 4
            trans.append((a, 3*L))
            trans.append((a, -3*L))
        for k in range(8):
            a = k * pi / 4
            trans.append((a + pi/8, 2*L))
            trans.append((a + pi/8, -2*L))

    return trans


# =====================================================================
# Compute the regularized matrix for one base point
# =====================================================================

def compute_regularized(z0, n_shells=2, verbose=False):
    """Compute the regularized interaction matrix via heat kernel."""
    orbit = make_orbit(z0)
    n = len(orbit)
    trans = build_translations(n_shells)
    area_inv = 1.0 / (4 * pi)

    # Log-spaced t-grid near 0, then linear for larger t
    t_grid = np.concatenate([
        np.logspace(-2, -0.5, 15),  # 0.01 to 0.316
        np.linspace(0.4, 2.0, 12),
        np.linspace(2.5, 8.0, 8),
        np.linspace(10, 30, 5),
    ])
    t_grid = sorted(set(t_grid))

    M = np.zeros((n, n))

    for idx in range(len(t_grid) - 1):
        t_lo = t_grid[idx]
        t_hi = t_grid[idx + 1]
        t_mid = (t_lo + t_hi) / 2
        dt = t_hi - t_lo

        # Build K matrix at this t
        K = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                total = 0.0
                # Direct term (j != i)
                if i != j:
                    d = hyp_dist(orbit[i], orbit[j])
                    total += heat_kernel_H2(d, t_mid)
                # Lattice images
                for angle, dist in trans:
                    if abs(dist) < 1e-10:
                        continue
                    w = translate_disc(orbit[j], angle, dist)
                    d = hyp_dist(orbit[i], w)
                    total += heat_kernel_H2(d, t_mid)
                K[i][j] = total

        for i in range(n):
            for j in range(n):
                M[i][j] += (K[i][j] - area_inv) * dt

    ev = sorted(np.linalg.eigvalsh(M), reverse=True)
    return n, ev, M


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
# MAIN COMPUTATION
# =====================================================================

def main():
    print("=" * 72)
    print("  REFINED BOLZA HEAT KERNEL COMPUTATION")
    print("=" * 72)

    # ---- Part 1: Main computation at reference point ----
    print(f"\n  PART 1: Reference computation at z0 = 0.15 + 0.08i\n")

    z0 = 0.15 + 0.08j
    n, ev, M = compute_regularized(z0, n_shells=2, verbose=True)

    print(f"  Orbit size: {n}")
    print(f"\n  Eigenvalues:")
    for i, e in enumerate(ev):
        print(f"    λ_{i:2d} = {e:16.12f}")

    # Multi-resolution degeneracy
    for tol_exp in [2, 3, 4, 5]:
        tol = 10**(-tol_exp)
        groups = degeneracy_groups(ev, tol)
        n2d = sum(1 for _, m in groups if m == 2)
        print(f"\n  Degeneracy at tol = 10^-{tol_exp}: {len(groups)} groups, {n2d} × 2D")
        for e, m in groups:
            tag = " *** GL(2) ***" if m == 2 else ""
            print(f"    {e:16.10f}  mult = {m}{tag}")

    # ---- Part 2: Base point independence ----
    print(f"\n{'='*72}")
    print(f"  PART 2: BASE POINT INDEPENDENCE")
    print(f"{'='*72}\n")

    test_pts = [
        0.15 + 0.08j,
        0.20 + 0.05j,
        0.10 + 0.15j,
        0.05 + 0.02j,
    ]

    print(f"  {'z0':>16s} {'n':>4s}", end="")
    for i in range(4):
        print(f"  {'λ_'+str(i):>14s}", end="")
    print()

    all_ev = []
    for z0 in test_pts:
        n, ev, _ = compute_regularized(z0, n_shells=2)
        all_ev.append(ev)
        z_str = f"{z0.real:.2f}+{z0.imag:.2f}i"
        print(f"  {z_str:>16s} {n:4d}", end="")
        for e in ev[:4]:
            print(f"  {e:14.8f}", end="")
        print()

    # Statistics on leading eigenvalues
    if all_ev:
        print(f"\n  Stability of leading eigenvalues across base points:")
        for i in range(min(4, min(len(e) for e in all_ev))):
            vals = [e[i] for e in all_ev]
            mn, sd = np.mean(vals), np.std(vals)
            pct = 100*sd/abs(mn) if abs(mn) > 1e-10 else 999
            print(f"    λ_{i}: mean = {mn:12.8f}, std = {sd:10.2e}, variation = {pct:.1f}%")

    # ---- Part 3: Convergence with shells ----
    print(f"\n{'='*72}")
    print(f"  PART 3: CONVERGENCE WITH LATTICE SHELLS")
    print(f"{'='*72}\n")

    z0 = 0.15 + 0.08j
    print(f"  {'shells':>8s}", end="")
    for i in range(4):
        print(f"  {'λ_'+str(i):>14s}", end="")
    print()

    for ns in [1, 2, 3]:
        n, ev, _ = compute_regularized(z0, n_shells=ns)
        print(f"  {ns:8d}", end="")
        for e in ev[:4]:
            print(f"  {e:14.8f}", end="")
        print()

    # ---- Summary ----
    print(f"\n{'='*72}")
    print(f"  SUMMARY")
    print(f"{'='*72}")

    # Use the best computation
    n, ev, _ = compute_regularized(0.15 + 0.08j, n_shells=2)
    groups = degeneracy_groups(ev, 1e-3)
    gl2 = [(e, m) for e, m in groups if m == 2]

    print(f"\n  GL(2) eigenvalues (2-fold degenerate):")
    for e, m in gl2:
        print(f"    {e:14.10f}")

    # Spectral interpretation
    print(f"\n  Spectral interpretation:")
    print(f"  Bolza spectral gap: λ₁ = 3.839 (Strohmaier-Uski)")
    print(f"  Expected G_reg scale: 1/λ₁ = {1/3.839:.6f}")
    print(f"  Our leading GL(2) eigenvalue: {gl2[0][0]:.6f}" if gl2 else "  No GL(2) found")

    if gl2:
        ratio = gl2[0][0] / (1/3.839)
        print(f"  Ratio (GL2 / 1/λ₁): {ratio:.6f}")
        print(f"  This ratio = |φ₁(z₀)|² averaged over the orbit")


if __name__ == "__main__":
    main()
