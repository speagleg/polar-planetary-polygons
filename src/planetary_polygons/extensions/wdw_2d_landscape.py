"""
2D Wheeler-DeWitt landscape: finding the minimum of V(rho, K).

V(rho, K) = lambda_{m*}(rho, K) = G_K(rho) + b_eff(N,K) - f(m*)

The potential must be analyzed for:
1. Minima (where the wavefunction concentrates)
2. Saddle points (transition states)
3. Normalizability (does V -> inf in all directions?)

Key insight: V depends on the PRODUCT kappa*rho = sqrt(|K|)*rho.
Define xi = sqrt(|K|) * rho (the dimensionless curvature-radius product).
Then the potential is a function of xi and the SIGN of K.

For K < 0: V(xi) = log(2*sinh(xi)) + b - f  [grows as xi for large xi]
For K > 0: V(xi) = log(2*sin(xi)) + b - f   [oscillates, bounded]

The CONFINING behavior comes from K < 0 only.
For K > 0, V is NOT confining (it oscillates).

The question: does the 2D potential V(rho, K) have a minimum in
the K < 0 half-plane?
"""

import numpy as np
from math import pi, sin, cos, log, exp, sqrt, sinh, cosh, asin, asinh


def casimir(m, N):
    return m * (N - m) / 2.0


def havelock_eigenvalue_K(m, N, rho, K):
    """Havelock eigenvalue at curvature K."""
    lam = 0.0
    for p in range(1, N):
        sin_angle = abs(sin(pi * p / N))
        if K < -1e-10:
            kappa = sqrt(-K)
            sinh_half_d = sinh(kappa * rho) * sin_angle
            if sinh_half_d > 1e-15:
                h = -log(2 * sinh_half_d)
            else:
                h = 30
        elif K > 1e-10:
            kappa = sqrt(K)
            sin_half_d = sin(kappa * rho) * sin_angle
            if 0 < sin_half_d <= 1:
                h = -log(2 * sin_half_d)
            elif sin_half_d > 1:
                h = -log(2.0)  # cap
            else:
                h = 30
        else:
            d = 2 * rho * sin_angle
            h = -log(d) if d > 1e-15 else 30
        lam += h * cos(2 * pi * p * m / N)
    return lam


def V_potential(rho, K, N, m_crit=None):
    """The WDW potential V(rho, K) for the critical mode."""
    if m_crit is None:
        m_crit = N // 2
    return havelock_eigenvalue_K(m_crit, N, rho, K)


def scan_potential_2d(N):
    """Scan V(rho, K) on a 2D grid and find structure."""
    m_crit = N // 2
    f_crit = casimir(m_crit, N)

    # Grid
    rho_vals = np.linspace(0.3, 6.0, 40)
    K_vals = np.linspace(-4.0, -0.01, 40)

    V_grid = np.zeros((len(K_vals), len(rho_vals)))

    for i, K in enumerate(K_vals):
        for j, rho in enumerate(rho_vals):
            V_grid[i, j] = V_potential(rho, K, N, m_crit)

    # Find the minimum
    min_idx = np.unravel_index(np.argmin(np.abs(V_grid)), V_grid.shape)
    K_min = K_vals[min_idx[0]]
    rho_min = rho_vals[min_idx[1]]
    V_min = V_grid[min_idx]

    # The zero contour (the threshold surface)
    zero_crossings = []
    for i, K in enumerate(K_vals):
        for j in range(len(rho_vals) - 1):
            if V_grid[i, j] * V_grid[i, j+1] < 0:
                # Linear interpolation
                rho_zero = rho_vals[j] - V_grid[i,j] * (rho_vals[j+1] - rho_vals[j]) / (V_grid[i,j+1] - V_grid[i,j])
                zero_crossings.append((K, rho_zero))

    return V_grid, K_vals, rho_vals, K_min, rho_min, V_min, zero_crossings


def analyze_xi_variable(N):
    """Analyze in the natural variable xi = sqrt(|K|) * rho.

    For K < 0: V depends on rho and K only through xi = sqrt(|K|)*rho
    PLUS the normalization factor from the kernel.

    Specifically:
    2*sinh(d_p/2) = 2*sinh(kappa*rho)*sin(pi*p/N)
                  = 2*sinh(xi)*sin(pi*p/N)  where xi = kappa*rho

    and h(d_p) = -log(2*sinh(xi)*sin(pi*p/N)) + log(kappa)... NO:
    d_p = 2*arcsinh(sinh(kappa*rho)*sin(pi*p/N)) / kappa
    h(d_p) = -log(2*sinh(d_p/2))

    For d_p on H^2 with curvature K = -kappa^2:
    cosh(kappa*d_p) = 1 + 2*sinh^2(kappa*rho)*sin^2(pi*p/N)

    Actually: the Havelock eigenvalue at curvature K = -kappa^2 is:
    lambda_m = sum_p [-log(2*sinh(d_p/2))] * cos(2*pi*p*m/N)

    where 2*sinh(kappa*d_p/2) = 2*sinh(kappa*rho)*|sin(pi*p/N)|

    So: h(d_p) = -log(2*sinh(kappa*d_p/2)/kappa)
              = -log(2*sinh(kappa*rho)*|sin(pi*p/N)|/kappa)
              = -log(2*sinh(xi)*|sin(pi*p/N)|) + log(kappa)

    Wait, h(d) = -log(2*sinh(d/2)) where d is the geodesic distance
    in the metric ds^2_K = K^{-1} * ds^2_{H^2,K=-1}.

    Actually, for curvature K = -1/a^2 (so a = 1/kappa):
    The geodesic distance formula gives:
    2*sinh(d/(2a)) = 2*sinh(rho/a)*|sin(pi*p/N)|

    And the Green's function: h(d) = -log(2*sinh(d/(2a)))... no.

    The Green's function on H^2 of curvature K = -1/a^2 is:
    G(d) = -(1/(2*pi)) * log(2*sinh(d/(2a))) + const
    But for point vortices, h(d) = -log(2*sinh(d/(2a))) (without the 2*pi).

    Hmm, let me just check: does V depend on xi = kappa*rho alone?
    """
    m_crit = N // 2

    print(f"\n  Testing: does V depend on xi = sqrt(|K|)*rho alone?")
    print(f"  N = {N}, m* = {m_crit}")
    print(f"\n  {'xi':>8s} {'K=-0.5,rho':>12s} {'V(-0.5)':>10s} "
          f"{'K=-1,rho':>12s} {'V(-1)':>10s} "
          f"{'K=-2,rho':>12s} {'V(-2)':>10s} {'same?':>8s}")

    for xi in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]:
        results = []
        for K in [-0.5, -1.0, -2.0]:
            kappa = sqrt(-K)
            rho = xi / kappa
            V = V_potential(rho, K, N, m_crit)
            results.append((K, rho, V))

        V_spread = max(r[2] for r in results) - min(r[2] for r in results)
        same = "YES" if V_spread < 0.01 else f"no({V_spread:.3f})"

        print(f"  {xi:8.4f} {results[0][1]:12.4f} {results[0][2]:10.4f} "
              f"{results[1][1]:12.4f} {results[1][2]:10.4f} "
              f"{results[2][1]:12.4f} {results[2][2]:10.4f} {same:>8s}")


def find_V_minimum_along_threshold(N):
    """Along the threshold curve V=0, find the minimum of |dV/drho|.

    Where the potential is FLATTEST along the threshold, the
    wavefunction spreads the most. This is the natural "attractor."
    """
    m_crit = N // 2

    print(f"\n  N = {N}: slope |dV/drho| along the threshold curve")
    print(f"  {'K':>8s} {'rho*':>10s} {'dV/drho':>12s} {'d2V/drho2':>12s}")

    for K in np.linspace(-3, -0.1, 20):
        kappa = sqrt(-K)
        # Find threshold
        rho_lo, rho_hi = 0.1, 50.0
        for _ in range(100):
            rho_mid = (rho_lo + rho_hi) / 2
            V = V_potential(rho_mid, K, N, m_crit)
            if V > 0:
                rho_lo = rho_mid
            else:
                rho_hi = rho_mid
        rho_star = (rho_lo + rho_hi) / 2

        # Slope at threshold
        eps = 0.001
        V_plus = V_potential(rho_star + eps, K, N, m_crit)
        V_minus = V_potential(rho_star - eps, K, N, m_crit)
        dV = (V_plus - V_minus) / (2 * eps)

        V_pp = (V_plus - 2 * V_potential(rho_star, K, N, m_crit) + V_minus) / eps**2

        print(f"  {K:8.4f} {rho_star:10.4f} {dV:12.6f} {V_pp:12.6f}")


def total_energy_landscape(N_max=10):
    """The TOTAL potential including all modes, not just the critical one.

    V_total(rho, K) = sum_m lambda_m(rho, K)
                    = (N-1)*C_1(rho, K) - sum f(m) + sum delta_m

    Since sum delta = 0 (traceless):
    V_total = (N-1)*C_1 - N(N^2-1)/12

    C_1 depends on (rho, K) through the Green's function.
    """
    print(f"\n  Total potential V_total = sum_m lambda_m:")
    print(f"  {'K':>8s} {'rho':>8s}", end="")
    for N in [6, 8, 10]:
        print(f"  V_tot({N})", end="")
    print()

    for K in [-2.0, -1.0, -0.5, -0.1, 0.0, 0.1, 0.3]:
        for rho in [0.5, 1.0, 2.0, 3.0]:
            if K > 0 and rho > pi / (2 * sqrt(K)) * 0.9:
                continue
            print(f"  {K:8.4f} {rho:8.4f}", end="")
            for N in [6, 8, 10]:
                V_tot = sum(havelock_eigenvalue_K(m, N, rho, K)
                           for m in range(1, N))
                print(f"  {V_tot:9.3f}", end="")
            print()


def wdw_ground_state_1d(N, K_fixed):
    """Solve the 1D WDW equation at fixed K to find the ground state energy.

    [-hbar^2/(2c) d^2/drho^2 + V(rho)] Psi = E Psi

    The ground state energy E_0(K) as a function of K tells us
    whether there's a preferred K.
    """
    m_crit = N // 2
    c = N**2

    # Discretize the 1D Schrodinger equation
    rho_min, rho_max = 0.3, 15.0
    n_grid = 500
    drho = (rho_max - rho_min) / n_grid
    rho_grid = np.linspace(rho_min, rho_max, n_grid)

    # Build the Hamiltonian matrix (tridiagonal)
    V_diag = np.array([V_potential(rho, K_fixed, N, m_crit) for rho in rho_grid])

    # Kinetic energy: -hbar^2/(2c) * d^2/drho^2
    # Discretized: T_{ij} = (hbar^2/(2c*drho^2)) * (2*delta_{ij} - delta_{i,j+1} - delta_{i,j-1})
    hbar = 1.0
    T_coeff = hbar**2 / (2 * c * drho**2)

    # The eigenvalue problem: (T + V) psi = E psi
    # For the GROUND STATE, use the variational method or direct diag

    # Build the full Hamiltonian
    H = np.diag(V_diag) + T_coeff * (2 * np.eye(n_grid)
        - np.eye(n_grid, k=1) - np.eye(n_grid, k=-1))

    # Find the lowest few eigenvalues
    eigenvalues = np.linalg.eigvalsh(H)
    E_0 = eigenvalues[0]
    E_1 = eigenvalues[1] if len(eigenvalues) > 1 else None

    return E_0, E_1, eigenvalues[:5]


def ground_state_vs_K(N):
    """Compute the ground state energy E_0(K) as a function of K."""
    print(f"\n  Ground state energy E_0(K) for N = {N}:")
    print(f"  {'K':>8s} {'E_0':>12s} {'E_1':>12s} {'gap':>10s}")

    E0_vals = []
    K_vals = np.linspace(-3, -0.1, 20)

    for K in K_vals:
        try:
            E0, E1, evals = wdw_ground_state_1d(N, K)
            gap = E1 - E0 if E1 is not None else 0
            E0_vals.append((K, E0))
            print(f"  {K:8.4f} {E0:12.6f} {E1:12.6f} {gap:10.6f}")
        except Exception as e:
            print(f"  {K:8.4f} ERROR: {e}")

    if E0_vals:
        # Find the minimum E_0
        min_entry = min(E0_vals, key=lambda x: x[1])
        print(f"\n  Minimum E_0 at K = {min_entry[0]:.4f} with E_0 = {min_entry[1]:.6f}")

        # Does E_0(K) have a minimum at FINITE K?
        K_arr = [e[0] for e in E0_vals]
        E_arr = [e[1] for e in E0_vals]

        # Check monotonicity
        diffs = [E_arr[i+1] - E_arr[i] for i in range(len(E_arr)-1)]
        all_decreasing = all(d <= 0 for d in diffs)
        all_increasing = all(d >= 0 for d in diffs)

        if all_decreasing:
            print(f"  E_0(K) is MONOTONICALLY DECREASING (no finite minimum)")
        elif all_increasing:
            print(f"  E_0(K) is MONOTONICALLY INCREASING")
        else:
            # Find the turning point
            for i in range(len(diffs)-1):
                if diffs[i] * diffs[i+1] < 0:
                    K_turn = K_arr[i+1]
                    print(f"  E_0(K) has a TURNING POINT near K = {K_turn:.4f}")
                    break

    return E0_vals


def main():
    print("=" * 72)
    print("  2D WHEELER-DEWITT LANDSCAPE")
    print("  Finding structure in V(rho, K)")
    print("=" * 72)

    N = 8

    # Part 1: Does V depend on xi = sqrt(|K|)*rho alone?
    print(f"\n{'='*72}")
    print("  TEST: Does V depend on xi = sqrt(|K|)*rho alone?")
    print("=" * 72)
    analyze_xi_variable(N)

    # Part 2: 2D potential scan
    print(f"\n{'='*72}")
    print("  2D POTENTIAL SCAN")
    print("=" * 72)
    V_grid, K_vals, rho_vals, K_min, rho_min, V_min, zeros = scan_potential_2d(N)

    print(f"\n  N = {N}: V(rho, K) closest to zero at K={K_min:.2f}, rho={rho_min:.2f}")
    print(f"  V_min = {V_min:.6f}")
    print(f"  Number of zero-crossing points: {len(zeros)}")
    if zeros:
        print(f"  Zero contour (threshold curve):")
        for K, rho in zeros[::max(1, len(zeros)//10)]:
            print(f"    K = {K:.4f}, rho* = {rho:.4f}")

    # Part 3: Slope along threshold
    print(f"\n{'='*72}")
    print("  SLOPE ALONG THE THRESHOLD CURVE")
    print("=" * 72)
    find_V_minimum_along_threshold(N)

    # Part 4: Total energy
    print(f"\n{'='*72}")
    print("  TOTAL POTENTIAL (sum over all modes)")
    print("=" * 72)
    total_energy_landscape()

    # Part 5: Ground state vs K
    print(f"\n{'='*72}")
    print("  GROUND STATE ENERGY E_0(K)")
    print("  Does the WDW equation select a preferred K?")
    print("=" * 72)

    for N in [6, 8]:
        E0_data = ground_state_vs_K(N)

    print(f"\n{'='*72}")
    print("  CONCLUSIONS")
    print("=" * 72)


if __name__ == "__main__":
    main()
