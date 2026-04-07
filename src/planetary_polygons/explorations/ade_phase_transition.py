r"""
EXPLORATION: ADE phase transition in vortex configurations.

HYPOTHESIS: As the curvature parameter varies from K>0 (S²) to K<0 (H²),
the lowest-energy vortex configuration transitions from Platonic (E-type
McKay: E_6/E_7/E_8) to polygon (A-type McKay: SU(N)).

This would unify the polygon framework (Papers I-VI) with the Platonic
framework discovered in this session, via a curvature phase transition
that simultaneously:
  (a) changes the symmetry group from non-abelian to cyclic
  (b) breaks the gauge group from E-type to A-type (= SM)

TEST: Compare the vortex energy of:
  - Regular N-gon ring at optimized latitude on S²
  - Platonic solid with N vertices on S²
for N=6 (hexagon vs octahedron) and N=12 (12-gon vs icosahedron).
"""

import numpy as np
from math import pi, sin, cos, acos, log, sqrt, tan


# =====================================================================
# Energy on S²: H = -Σ_{j<k} ln sin(d_{jk}/2)
# =====================================================================

def s2_energy(verts):
    """Vortex energy H = -Σ_{j<k} ln sin(d/2) on S²."""
    N = len(verts)
    H = 0.0
    for j in range(N):
        for k in range(j + 1, N):
            dot = np.clip(np.dot(verts[j], verts[k]), -1, 1)
            d = acos(dot)
            s = sin(d / 2)
            if s > 1e-15:
                H -= log(s)
    return H


def polygon_ring(N, theta0):
    """N equally-spaced vertices on a ring at colatitude theta0 on S²."""
    verts = []
    for k in range(N):
        phi = 2 * pi * k / N
        verts.append([
            sin(theta0) * cos(phi),
            sin(theta0) * sin(phi),
            cos(theta0),
        ])
    return np.array(verts)


def polygon_energy(N, theta0):
    """Energy of N-gon ring at colatitude theta0."""
    return s2_energy(polygon_ring(N, theta0))


# =====================================================================
# Optimal polygon latitude
# =====================================================================

def optimal_polygon_theta(N, n_points=200):
    """Find the colatitude that minimizes the polygon ring energy.

    Uses a grid search (no scipy needed).
    """
    thetas = np.linspace(0.05, pi - 0.05, n_points)
    energies = [polygon_energy(N, t) for t in thetas]
    best_idx = np.argmin(energies)

    # Refine with finer grid around the minimum
    t_lo = thetas[max(0, best_idx - 2)]
    t_hi = thetas[min(len(thetas) - 1, best_idx + 2)]
    thetas_fine = np.linspace(t_lo, t_hi, 100)
    energies_fine = [polygon_energy(N, t) for t in thetas_fine]
    best_fine = np.argmin(energies_fine)

    return thetas_fine[best_fine], energies_fine[best_fine]


# =====================================================================
# Platonic solid configurations
# =====================================================================

def platonic_vertices(name):
    """Get Platonic solid vertices on S²."""
    from planetary_polygons.explorations.platonic_vortices import (
        tetrahedron_vertices, octahedron_vertices, cube_vertices,
        icosahedron_vertices, dodecahedron_vertices,
    )
    return {
        'tetrahedron': tetrahedron_vertices,
        'octahedron': octahedron_vertices,
        'cube': cube_vertices,
        'icosahedron': icosahedron_vertices,
        'dodecahedron': dodecahedron_vertices,
    }[name]()


def platonic_energy(name):
    """Energy of the Platonic solid on S²."""
    return s2_energy(platonic_vertices(name))


# =====================================================================
# Hessian stability (finite-difference, correct for S²)
# =====================================================================

def s2_hessian_fd(verts, eps=1e-5):
    """Finite-difference Hessian of S² vortex energy."""
    N = len(verts)
    bases = []
    for k in range(N):
        p = verts[k]
        if abs(p[0]) < 0.9:
            v = np.array([1, 0, 0.])
        else:
            v = np.array([0, 1, 0.])
        e1 = v - np.dot(v, p) * p
        e1 /= np.linalg.norm(e1)
        e2 = np.cross(p, e1)
        e2 /= np.linalg.norm(e2)
        bases.append((e1, e2))

    def perturb(verts, k, a, delta):
        v = verts.copy()
        v[k] = v[k] + delta * bases[k][a]
        v[k] /= np.linalg.norm(v[k])
        return v

    dim = 2 * N
    H = np.zeros((dim, dim))
    for i in range(dim):
        ki, ai = i // 2, i % 2
        for j in range(i, dim):
            kj, aj = j // 2, j % 2
            vpp = perturb(perturb(verts, ki, ai, eps), kj, aj, eps)
            vpm = perturb(perturb(verts, ki, ai, eps), kj, aj, -eps)
            vmp = perturb(perturb(verts, ki, ai, -eps), kj, aj, eps)
            vmm = perturb(perturb(verts, ki, ai, -eps), kj, aj, -eps)
            H[i, j] = (s2_energy(vpp) - s2_energy(vpm) -
                        s2_energy(vmp) + s2_energy(vmm)) / (4 * eps ** 2)
            H[j, i] = H[i, j]
    return np.sort(np.linalg.eigvalsh(H))


def min_positive_eigenvalue(evals, tol=0.01):
    """Smallest positive eigenvalue (stability measure)."""
    pos = [e for e in evals if e > tol]
    return min(pos) if pos else 0.0


def n_negative(evals, tol=0.01):
    """Number of negative eigenvalues."""
    return sum(1 for e in evals if e < -tol)


# =====================================================================
# Energy comparison: polygon ring vs Platonic solid
# =====================================================================

def energy_comparison(N, platonic_name, n_thetas=50):
    """Compare polygon ring energy vs Platonic solid energy on S².

    Returns a dict with the comparison data for plotting/analysis.
    """
    # Platonic energy (fixed)
    E_platonic = platonic_energy(platonic_name)

    # Polygon energy as a function of colatitude
    thetas = np.linspace(0.1, pi - 0.1, n_thetas)
    E_polygon = [polygon_energy(N, t) for t in thetas]

    # Optimal polygon
    theta_opt, E_opt = optimal_polygon_theta(N)

    # Find crossover points (where E_polygon = E_platonic)
    crossovers = []
    for i in range(len(thetas) - 1):
        if (E_polygon[i] - E_platonic) * (E_polygon[i + 1] - E_platonic) < 0:
            # Linear interpolation for the crossover theta
            f1 = E_polygon[i] - E_platonic
            f2 = E_polygon[i + 1] - E_platonic
            t_cross = thetas[i] - f1 * (thetas[i + 1] - thetas[i]) / (f2 - f1)
            crossovers.append(t_cross)

    return {
        'N': N,
        'platonic_name': platonic_name,
        'E_platonic': E_platonic,
        'thetas': thetas,
        'E_polygon': E_polygon,
        'theta_opt': theta_opt,
        'E_polygon_opt': E_opt,
        'crossover_thetas': crossovers,
        'platonic_wins': E_platonic < E_opt,
        'energy_gap': E_platonic - E_opt,
    }


# =====================================================================
# Full phase transition analysis
# =====================================================================

def phase_transition_analysis():
    """Run the full ADE phase transition analysis."""
    results = {}

    cases = [
        (4, 'tetrahedron', 'A_4', 'E_6'),
        (6, 'octahedron', 'S_4', 'E_7'),
        (8, 'cube', 'S_4', 'E_7'),
        (12, 'icosahedron', 'A_5', 'E_8'),
        (20, 'dodecahedron', 'A_5', 'E_8'),
    ]

    for N, pname, G, mckay in cases:
        comp = energy_comparison(N, pname)

        # Stability analysis for the Platonic solid
        verts_p = platonic_vertices(pname)
        evals_p = s2_hessian_fd(verts_p)
        n_neg_p = n_negative(evals_p)

        # Stability for optimal polygon
        verts_poly = polygon_ring(N, comp['theta_opt'])
        evals_poly = s2_hessian_fd(verts_poly)
        n_neg_poly = n_negative(evals_poly)

        results[pname] = {
            **comp,
            'G': G,
            'mckay': mckay,
            'platonic_stable': n_neg_p == 0,
            'polygon_stable': n_neg_poly == 0,
            'platonic_morse_index': n_neg_p,
            'polygon_morse_index': n_neg_poly,
        }

    return results


if __name__ == '__main__':
    print("=" * 72)
    print("ADE PHASE TRANSITION: Polygon (A-type) vs Platonic (E-type)")
    print("=" * 72)
    print()

    results = phase_transition_analysis()

    print(f"{'Solid':<14s} {'N':>3s} {'G':>5s} {'McKay':>5s} "
          f"{'E_plat':>9s} {'E_poly':>9s} {'Gap':>8s} "
          f"{'Winner':>10s} {'P_stab':>6s} {'R_stab':>6s}")
    print("-" * 85)

    for name in ['tetrahedron', 'octahedron', 'cube', 'icosahedron', 'dodecahedron']:
        r = results[name]
        winner = r['platonic_name'] if r['platonic_wins'] else f"{r['N']}-gon"
        p_stab = "Y" if r['platonic_stable'] else "N"
        r_stab = "Y" if r['polygon_stable'] else "N"
        print(f"{name:<14s} {r['N']:3d} {r['G']:>5s} {r['mckay']:>5s} "
              f"{r['E_platonic']:9.4f} {r['E_polygon_opt']:9.4f} "
              f"{r['energy_gap']:+8.4f} "
              f"{winner:>10s} {p_stab:>6s} {r_stab:>6s}")

    print()
    print("Gap > 0: Platonic has higher energy (polygon wins)")
    print("Gap < 0: Platonic has lower energy (Platonic wins)")
    print()

    # Detailed analysis for the key cases
    for name in ['octahedron', 'icosahedron']:
        r = results[name]
        print(f"\n--- {name} (N={r['N']}) vs {r['N']}-gon ---")
        print(f"  Platonic energy: {r['E_platonic']:.6f}")
        print(f"  Polygon optimal: θ={np.degrees(r['theta_opt']):.1f}°, E={r['E_polygon_opt']:.6f}")
        print(f"  Energy gap: {r['energy_gap']:+.6f}")
        if r['platonic_wins']:
            print(f"  → PLATONIC WINS (lower energy)")
        else:
            print(f"  → POLYGON WINS (lower energy)")
        if r['crossover_thetas']:
            for t in r['crossover_thetas']:
                print(f"  Crossover at θ = {np.degrees(t):.1f}°")
        print(f"  Platonic stable: {r['platonic_stable']} (index {r['platonic_morse_index']})")
        print(f"  Polygon stable: {r['polygon_stable']} (index {r['polygon_morse_index']})")
