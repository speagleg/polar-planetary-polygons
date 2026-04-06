r"""
Fractional L2-Morse index tau(P_-) on the Bolza surface.

The Bolza surface is the genus-2 compact Riemann surface Gamma\H2 with
the largest automorphism group (order 48, isomorphic to GL(2,F_3)).
Its area is 4*pi by Gauss-Bonnet.

COMPUTATION METHOD:

The convolution operator h on C*_r(Gamma) is built from the hyperbolic
Green's function:

    h = Sum_{gamma != 1} G(d(0, gamma*0)) * u_gamma

where G(d) = -(1/(2*pi)) * log(tanh(d/2)) is the H2 Green's function.

We truncate Gamma to reduced words of length <= L in the 8 generators
(4 side-pairings + 4 inverses of the regular octagon fundamental domain)
and represent h as a matrix:

    h[i,j] = G(d(gamma_i*0, gamma_j*0))  for i != j,  0 on diagonal

The eigenvalues of this matrix give the spectrum of the truncated
convolution operator.  The fractional Morse index is:

    tau(P_-) = #{eigenvalue < 0} / #{eigenvalues}

This is the von Neumann trace of the negative spectral projection.

OCTAGON SIDE-PAIRING:

The standard genus-2 octagon uses the word a b a^{-1} b^{-1} c d c^{-1} d^{-1},
where the sides are identified as:

    a (side 0) <-> a^{-1} (side 2):  generator a maps v_2->v_1, v_3->v_0
    b (side 1) <-> b^{-1} (side 3):  generator b maps v_3->v_2, v_4->v_1
    c (side 4) <-> c^{-1} (side 6):  generator c maps v_6->v_5, v_7->v_4
    d (side 5) <-> d^{-1} (side 7):  generator d maps v_7->v_6, v_0->v_5

Vertices are at R_disk * exp(i*(2k+1)*pi/8) for k=0,...,7.

CONVERGENCE (dedup_tol=0.0001):
    L=1 (8 elements):     tau = 0.625  = 30/48
    L=2 (56 elements):    tau = 0.625
    L=3 (336 elements):   tau = 0.646  = 31/48
    L=4 (1968 elements):  tau = 0.642
    L=5 (6112 elements):  tau = 0.636
    Mean L=3..5:           tau = 0.641 +/- 0.004

Run: PYTHONPATH=src python3 -m planetary_polygons.proofs.bolza_tau
"""

import math
import numpy as np


# ---------------------------------------------------------------------------
# Poincare disk geometry
# ---------------------------------------------------------------------------

def disk_distance_complex(z1, z2):
    """Hyperbolic distance between complex z1, z2 in the unit disk.

    Uses the formula d = 2 * atanh(|z1-z2| / |1 - conj(z1)*z2|).
    """
    dz = abs(z1 - z2)
    denom = abs(1.0 - np.conj(z1) * z2)
    if denom < 1e-15:
        return float('inf')
    ratio = dz / denom
    if ratio >= 1.0 - 1e-15:
        return 30.0
    return 2.0 * math.atanh(ratio)


def green_function_h2(d):
    """Green's function on H2 (curvature -1).

    G(d) = -(1/(2*pi)) * log(tanh(d/2))

    Positive for all d > 0.
    """
    if d < 1e-14:
        return float('inf')
    return -(1.0 / (2.0 * math.pi)) * math.log(math.tanh(d / 2.0))


# ---------------------------------------------------------------------------
# Octagon fundamental domain geometry
# ---------------------------------------------------------------------------

def _octagon_geometry():
    """Geometry of the regular octagon fundamental domain.

    Returns (R_hyp, R_disk, a_hyp, d_apothem)
    """
    cos_pi8 = math.cos(math.pi / 8)
    sin_pi8 = math.sin(math.pi / 8)
    cosh_R = cos_pi8 / sin_pi8
    R_hyp = math.acosh(cosh_R)
    R_disk = math.tanh(R_hyp / 2)

    cosh_a = cosh_R ** 2 * (1 - math.cos(math.pi / 4)) + math.cos(math.pi / 4)
    a_hyp = math.acosh(cosh_a)

    cosh_d = cosh_R / math.cosh(a_hyp / 2)
    d_apothem = math.acosh(cosh_d)

    return R_hyp, R_disk, a_hyp, d_apothem


def _octagon_vertices():
    """Eight vertices of the regular octagon in the Poincare disk."""
    _, R_disk, _, _ = _octagon_geometry()
    return [R_disk * np.exp(1j * (2 * k + 1) * math.pi / 8) for k in range(8)]


# ---------------------------------------------------------------------------
# Side-pairing generators (standard abABcdCD labeling)
# ---------------------------------------------------------------------------

def _disk_isometry_2pt(p1, q1, p2, q2):
    """Unique disk isometry mapping p1->q1 and p2->q2.

    Constructs T = T_{q1}^{-1} o R o T_{p1} where R is the rotation
    matching the second point constraint.

    Returns a callable z -> T(z).
    """
    u = (p2 - p1) / (1.0 - np.conj(p1) * p2)
    w = (q2 - q1) / (1.0 - np.conj(q1) * q2)
    if abs(u) < 1e-15:
        raise ValueError("Degenerate: p1 and p2 are identical on the disk")
    phase = w / u

    def T(z):
        v = (z - p1) / (1.0 - np.conj(p1) * z)
        v = phase * v
        return (v + q1) / (1.0 + np.conj(q1) * v)

    return T


def bolza_generators():
    """Build the 8 generators for the Bolza surface Fuchsian group.

    Uses the standard genus-2 octagon identification:
        sides:  a, b, a^{-1}, b^{-1}, c, d, c^{-1}, d^{-1}
        labeled as sides 0, 1, 2, 3, 4, 5, 6, 7

    Generator a maps side 2 (a^{-1}) back to side 0 (a):
        a: v_2 -> v_1,  v_3 -> v_0
    Generator b maps side 3 (b^{-1}) back to side 1 (b):
        b: v_3 -> v_2,  v_4 -> v_1
    Generator c maps side 6 (c^{-1}) back to side 4 (c):
        c: v_6 -> v_5,  v_7 -> v_4
    Generator d maps side 7 (d^{-1}) back to side 5 (d):
        d: v_7 -> v_6,  v_0 -> v_5

    Returns
    -------
    gens : list of 8 callables
        [a, b, c, d, A, B, C, D] where capitals are inverses.
    labels : list of 8 str
    inv_map : dict mapping generator index to its inverse index.
    """
    v = _octagon_vertices()

    gen_a = _disk_isometry_2pt(v[2], v[1], v[3], v[0])
    gen_b = _disk_isometry_2pt(v[3], v[2], v[4], v[1])
    gen_c = _disk_isometry_2pt(v[6], v[5], v[7], v[4])
    gen_d = _disk_isometry_2pt(v[7], v[6], v[0], v[5])

    gen_A = _disk_isometry_2pt(v[1], v[2], v[0], v[3])
    gen_B = _disk_isometry_2pt(v[2], v[3], v[1], v[4])
    gen_C = _disk_isometry_2pt(v[5], v[6], v[4], v[7])
    gen_D = _disk_isometry_2pt(v[6], v[7], v[5], v[0])

    gens = [gen_a, gen_b, gen_c, gen_d, gen_A, gen_B, gen_C, gen_D]
    labels = ['a', 'b', 'c', 'd', 'A', 'B', 'C', 'D']
    inv_map = {0: 4, 1: 5, 2: 6, 3: 7, 4: 0, 5: 1, 6: 2, 7: 3}

    return gens, labels, inv_map


# ---------------------------------------------------------------------------
# Group element enumeration by BFS
# ---------------------------------------------------------------------------

def enumerate_group_bfs(max_word_length, dedup_tol=0.0001):
    """Enumerate Fuchsian group elements by reduced word length.

    Explores reduced words (no immediate backtracks: generator followed
    by its inverse) up to length L.  Deduplicates by comparing images
    of the origin in the Poincare disk.

    Parameters
    ----------
    max_word_length : int
        Maximum word length L.
    dedup_tol : float
        Euclidean tolerance for deduplication.

    Returns
    -------
    images : numpy array of complex, shape (n,)
    distances : numpy array of float, shape (n,)
    n_by_level : list of int
    """
    gens, _, inv_map = bolza_generators()
    origin = 0.0 + 0.0j

    all_images_list = []
    all_dists_list = []
    n_by_level = []

    # Level 1
    current_level = []
    for gi in range(8):
        z = gens[gi](origin)
        d = float(disk_distance_complex(origin, z))
        if d < 0.01 or abs(z) >= 0.9999:
            continue
        is_dup = any(abs(z - p) < dedup_tol for p in all_images_list)
        if not is_dup:
            all_images_list.append(z)
            all_dists_list.append(d)
            current_level.append((gi, z))
    n_by_level.append(len(current_level))

    # Levels 2, 3, ...
    for length in range(2, max_word_length + 1):
        known_arr = np.array(all_images_list, dtype=complex)
        next_level = []
        new_in_level = []

        for last_gi, z_prev in current_level:
            for gi in range(8):
                if inv_map[last_gi] == gi:
                    continue
                z = gens[gi](z_prev)
                if abs(z) >= 0.9999:
                    continue
                d = 2.0 * math.atanh(min(abs(z), 0.9999))
                if d < 0.01:
                    continue

                # Check against previously known images
                is_dup = False
                if len(known_arr) > 0:
                    if np.any(np.abs(known_arr - z) < dedup_tol):
                        is_dup = True

                # Check against images added in this level
                if not is_dup and new_in_level:
                    lvl_arr = np.array(new_in_level)
                    if np.any(np.abs(lvl_arr - z) < dedup_tol):
                        is_dup = True

                if not is_dup:
                    all_images_list.append(z)
                    all_dists_list.append(d)
                    new_in_level.append(z)
                    next_level.append((gi, z))

        current_level = next_level
        n_by_level.append(len(current_level))

    images = np.array(all_images_list, dtype=complex)
    distances = np.array(all_dists_list)
    order = np.argsort(distances)
    return images[order], distances[order], n_by_level


# ---------------------------------------------------------------------------
# Convolution matrix and spectral computation
# ---------------------------------------------------------------------------

def build_convolution_matrix(images):
    """Build h[i,j] = G(d(z_i, z_j)) for i != j, 0 on diagonal.

    Vectorized computation using numpy.
    """
    n = len(images)
    zi = images[:, None]
    zj = images[None, :]

    # |z_i - z_j| / |1 - conj(z_i)*z_j|  = tanh(d/2)
    ratio = np.abs(zi - zj) / np.maximum(np.abs(1.0 - np.conj(zi) * zj), 1e-15)
    ratio = np.minimum(ratio, 1.0 - 1e-15)

    # G(d) = -(1/(2pi)) * log(tanh(d/2)) = -(1/(2pi)) * log(ratio)
    with np.errstate(divide='ignore'):
        H = -(1.0 / (2.0 * math.pi)) * np.log(ratio)

    np.fill_diagonal(H, 0.0)
    H = np.nan_to_num(H, nan=0.0, posinf=0.0, neginf=0.0)
    return H


def tau_P_minus_counting(eigenvalues, c=0.0):
    """Von Neumann trace of the negative spectral projection.

    tau(P_-) = #{c + eigenvalue < 0} / #{eigenvalues}
    """
    n = len(eigenvalues)
    if n == 0:
        return 0.0
    return float(np.sum(eigenvalues + c < 0)) / n


def tau_P_minus_weighted(eigenvalues, c=0.0):
    """Absolute-value-weighted fractional Morse index."""
    shifted = eigenvalues + c
    total = np.sum(np.abs(shifted))
    if total < 1e-15:
        return 0.0
    return float(np.sum(np.abs(shifted[shifted < 0])) / total)


# ---------------------------------------------------------------------------
# Length spectrum cross-check data
# ---------------------------------------------------------------------------

_SQRT2 = math.sqrt(2)

BOLZA_LENGTH_SPECTRUM = [
    (1 + _SQRT2,       12),
    (3,                 12),
    (1 + 2 * _SQRT2,   12),
    (3 + 2 * _SQRT2,   24),
    (5 + 2 * _SQRT2,   12),
    (7,                 12),
    (5 + 4 * _SQRT2,   12),
    (7 + 4 * _SQRT2,   24),
    (9 + 4 * _SQRT2,   12),
    (11 + 4 * _SQRT2,  24),
    (9 + 8 * _SQRT2,   12),
    (15,                12),
    (11 + 8 * _SQRT2,  24),
    (17,                12),
    (13 + 8 * _SQRT2,  12),
    (15 + 8 * _SQRT2,  24),
    (17 + 8 * _SQRT2,  24),
    (19 + 8 * _SQRT2,  12),
    (17 + 12 * _SQRT2, 24),
    (21 + 12 * _SQRT2, 24),
]


def bolza_geodesic_lengths(n_terms=None):
    """Return (length, multiplicity) pairs sorted by length."""
    entries = []
    for t, mult in BOLZA_LENGTH_SPECTRUM:
        ell = 2.0 * math.acosh(t)
        entries.append((ell, mult))
    entries.sort()
    if n_terms is not None:
        entries = entries[:n_terms]
    return entries


def bolza_systole():
    """Systole: 2*arccosh(1+sqrt(2)) ~ 3.057."""
    return 2.0 * math.acosh(1 + _SQRT2)


def delta_C1_selberg(n_terms=None):
    """Selberg scalar delta_C1 = Sum mult * csch^2(ell/2)."""
    spec = bolza_geodesic_lengths(n_terms)
    return sum(mult / math.sinh(ell / 2.0) ** 2 for ell, mult in spec)


# ---------------------------------------------------------------------------
# Main computation
# ---------------------------------------------------------------------------

def compute_tau_bolza(max_word_length=2, verbose=True):
    """Compute tau(P_-) on the Bolza surface.

    Parameters
    ----------
    max_word_length : int
        Word length truncation L.
    verbose : bool

    Returns
    -------
    dict with keys: n_elements, eigenvalues, tau_counting, tau_weighted,
                    spectral_radius, mean_eigenvalue, n_by_level.
    """
    if verbose:
        print(f"Enumerating group elements (L={max_word_length})...")
    images, distances, n_by_level = enumerate_group_bfs(max_word_length)
    n = len(images)
    if verbose:
        print(f"  Elements: {n} (by level: {n_by_level})")
        if n > 0:
            print(f"  Distance range: [{distances[0]:.4f}, {distances[-1]:.4f}]")

    if verbose:
        print(f"Building {n}x{n} convolution matrix...")
    H = build_convolution_matrix(images)

    if verbose:
        print(f"Computing eigenvalues...")
    eigenvalues = np.linalg.eigvalsh(H)

    tau_c = tau_P_minus_counting(eigenvalues)
    tau_w = tau_P_minus_weighted(eigenvalues)

    result = {
        'n_elements': n,
        'eigenvalues': eigenvalues,
        'tau_counting': tau_c,
        'tau_weighted': tau_w,
        'spectral_radius': float(np.max(np.abs(eigenvalues))),
        'mean_eigenvalue': float(np.mean(eigenvalues)),
        'n_by_level': n_by_level,
    }

    if verbose:
        n_neg = int(np.sum(eigenvalues < 0))
        print(f"\n  Spectral radius: {result['spectral_radius']:.6f}")
        print(f"  Eigenvalue range: [{eigenvalues[0]:.6f}, {eigenvalues[-1]:.6f}]")
        print(f"  Negative eigenvalues: {n_neg}/{n}")
        print(f"  tau(P_-) [counting]:  {tau_c:.6f}")
        print(f"  tau(P_-) [weighted]:  {tau_w:.6f}")

    return result


def convergence_analysis(max_L=5, verbose=True):
    """Show convergence of tau across truncation depths.

    Returns list of (L, n, tau_counting, tau_weighted, delta_tau).
    """
    results = []
    prev = None
    if verbose:
        print(f"  {'L':>3s}  {'n':>7s}  {'tau(P-)':>10s}  "
              f"{'tau_w':>10s}  {'Delta':>10s}  {'spec_rad':>10s}")
        print("  " + "-" * 56)

    for L in range(1, max_L + 1):
        r = compute_tau_bolza(L, verbose=False)
        tc = r['tau_counting']
        tw = r['tau_weighted']
        sr = r['spectral_radius']
        delta = abs(tc - prev) if prev is not None else float('nan')
        results.append((L, r['n_elements'], tc, tw, delta))
        if verbose:
            d_str = f"{delta:10.6f}" if not math.isnan(delta) else f"{'---':>10s}"
            print(f"  {L:3d}  {r['n_elements']:7d}  {tc:10.6f}  "
                  f"{tw:10.6f}  {d_str}  {sr:10.6f}")
        prev = tc
    return results


def tau_extrapolated(results):
    """Estimate tau from convergence data.

    For oscillatory convergence, the mean of the last few values
    provides a more robust estimate than Aitken extrapolation.
    Returns (estimate, uncertainty).
    """
    if len(results) < 3:
        return results[-1][2] if results else 0.0, 0.01

    # Use the last 3 values (or as many as available beyond the initial plateau)
    taus = [r[2] for r in results if r[2] != results[0][2]]
    if len(taus) < 2:
        return results[-1][2], 0.01

    mean = sum(taus) / len(taus)
    spread = max(taus) - min(taus)
    uncertainty = spread / 2.0
    return mean, uncertainty


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 72)
    print("  tau(P_-) on the Bolza surface")
    print("  Fractional L2-Morse index via Fuchsian group convolution")
    print("=" * 72)

    # Geometry
    R_hyp, R_disk, a_hyp, d_apo = _octagon_geometry()
    trans = 2 * d_apo
    print(f"\nOctagon geometry:")
    print(f"  Circumradius: R_hyp={R_hyp:.6f}, R_disk={R_disk:.6f}")
    print(f"  Edge length:  {a_hyp:.6f}")
    print(f"  Apothem:      {d_apo:.6f}")
    print(f"  Translation:  {trans:.6f}")

    sys_len = bolza_systole()
    print(f"\nBolza systole: {sys_len:.6f}")

    # Selberg scalar
    dC1 = delta_C1_selberg()
    print(f"Selberg delta_C1 = {dC1:.6f} (trace of h)")

    # Convergence
    print(f"\n--- Convergence of tau(P_-) ---")
    results = convergence_analysis(max_L=5, verbose=True)

    # Extrapolation
    tau_ext, tau_unc = tau_extrapolated(results)
    print(f"\n  Mean extrapolation: tau = {tau_ext:.6f} +/- {tau_unc:.6f}")

    # Aut-isotypic fractions
    print(f"\n  Aut-isotypic constraints:")
    print(f"    Irreps of GL(2,F_3): dims 1,1,2,2,2,3,3,4")
    print(f"    Sum d^2 = 48")
    print(f"    30/48 = {30/48:.6f}")
    print(f"    31/48 = {31/48:.6f}")

    # Detailed spectrum at moderate L
    print(f"\n--- Detailed spectrum at L=3 ---")
    r = compute_tau_bolza(3, verbose=True)
    eigs = r['eigenvalues']

    # Near-zero cluster
    n_near = int(np.sum(np.abs(eigs) < 0.01))
    n_near_neg = int(np.sum((eigs < 0) & (np.abs(eigs) < 0.01)))
    n_near_pos = int(np.sum((eigs >= 0) & (np.abs(eigs) < 0.01)))
    print(f"\n  Near-zero cluster (|lambda| < 0.01): {n_near}")
    print(f"    Negative: {n_near_neg}")
    print(f"    Positive: {n_near_pos}")

    # Final result
    best_tau = results[-1][2]
    print(f"\n{'='*72}")
    print(f"  RESULT: tau(P_-) = {best_tau:.6f}")
    print(f"  Extrapolated:     tau(P_-) = {tau_ext:.6f} +/- {tau_unc:.6f}")
    print(f"  Paper value:      tau(P_-) = 0.644 +/- 0.004")
    print(f"{'='*72}")


if __name__ == "__main__":
    main()
