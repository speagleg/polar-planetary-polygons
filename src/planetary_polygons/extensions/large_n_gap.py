"""
Large-N behavior of the mass gap: careful asymptotic analysis.

The WDW equation: [-hbar^2/(2c) d^2/drho^2 + V(rho)] Psi = E Psi

where c = 12*b(N) ~ N^2 and V(rho) = log(2sinh rho) + b(N) - f(m*)

For large N: f(m*) = N^2/8, b(N) ~ N^2/12 + N/12 - log2.
The shift: b - f = -N^2/24 + N/12 - log2 ~ -N^2/24.
So V(rho) ~ log(2sinh rho) - N^2/24.

The potential minimum is DEEP (V_min ~ -N^2/24) and the
kinetic coefficient is SMALL (hbar^2/(2c) ~ 1/(2N^2)).

The rescaled equation: define u = sqrt(c) * rho = N * rho
(the natural scale). Then:

[-1/2 d^2/du^2 + V(u/N)] Psi = E Psi

The rescaled potential: V(u/N) = log(2sinh(u/N)) + b(N) - f(m*)

For u/N << 1: V ~ log(2u/N) + b - f = log(u) - log(N/2) + b - f

So V ~ log(u) + [b - f - log(N/2)]
     ~ log(u) + [-N^2/24 - log(N/2)]

The DEPTH grows as N^2/24. The LOG SHAPE is u-independent.
The gap should be determined by the LOG potential alone
(since the depth just shifts all eigenvalues).
"""

import numpy as np
from math import pi, log, exp, sqrt, sinh, cosh, asinh


def b_exact(N):
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


def casimir(m, N):
    return m * (N - m) / 2.0


# =====================================================================
# PART 1: The rescaled equation
# =====================================================================

def rescaled_gap(N, n_grid=2000):
    """Solve the WDW equation in rescaled coordinates u = N*rho.

    The rescaled equation:
    [-1/(2N^2) d^2/drho^2 + V(rho)] Psi = E Psi

    In u = N*rho:
    [-1/2 d^2/du^2 + V(u/N)] Psi = E Psi

    The gap in the RESCALED equation is N^2-independent
    if V(u/N) depends on N only through an overall shift.
    """
    c = 12 * b_exact(N)
    f_crit = casimir(N // 2, N)
    b = b_exact(N)
    shift = b - f_crit  # the N-dependent shift

    # Solve in ORIGINAL coordinates (rho)
    rho_min = 0.005
    rho_max = 15
    drho = (rho_max - rho_min) / n_grid
    rho_grid = np.linspace(rho_min, rho_max, n_grid)

    V = np.array([log(2 * sinh(r)) + shift if r > 0.001 else -50
                  for r in rho_grid])

    hbar = 1.0
    T_coeff = hbar**2 / (2 * c * drho**2)
    H = np.diag(V) + T_coeff * (2 * np.eye(n_grid)
        - np.eye(n_grid, k=1) - np.eye(n_grid, k=-1))

    evals = np.linalg.eigvalsh(H)
    gap = evals[1] - evals[0]

    # Also solve the SHIFTED equation: remove the constant shift
    # V_shifted = log(2sinh rho) only (no b - f)
    V_pure = np.array([log(2 * sinh(r)) if r > 0.001 else -50
                       for r in rho_grid])

    H_pure = np.diag(V_pure) + T_coeff * (2 * np.eye(n_grid)
        - np.eye(n_grid, k=1) - np.eye(n_grid, k=-1))

    evals_pure = np.linalg.eigvalsh(H_pure)
    gap_pure = evals_pure[1] - evals_pure[0]

    return gap, gap_pure, shift, evals[:5], evals_pure[:5]


def compare_gaps():
    """Compare the full gap with the pure-potential gap."""
    print("=" * 72)
    print("  FULL GAP vs PURE POTENTIAL GAP")
    print("=" * 72)

    print(f"\n  {'N':>4s} {'c':>8s} {'shift':>10s} {'gap_full':>10s} "
          f"{'gap_pure':>10s} {'same?':>8s} {'E0_full':>10s} {'E0_pure':>10s}")

    for N in range(5, 25):
        c = 12 * b_exact(N)
        gap, gap_pure, shift, evals, evals_pure = rescaled_gap(N)

        same = abs(gap - gap_pure) < 0.001 * max(abs(gap), abs(gap_pure))

        print(f"  {N:4d} {c:8.1f} {shift:10.4f} {gap:10.6f} "
              f"{gap_pure:10.6f} {'YES' if same else 'no':>8s} "
              f"{evals[0]:10.4f} {evals_pure[0]:10.4f}")


# =====================================================================
# PART 2: The pure log(2sinh) gap at various c
# =====================================================================

def pure_potential_gap_vs_c():
    """The gap of V = log(2sinh rho) as a function of c ONLY."""
    print(f"\n{'='*72}")
    print("  PURE POTENTIAL GAP: V = log(2sinh rho), varying c")
    print("=" * 72)

    print(f"\n  {'c':>8s} {'gap':>10s} {'sqrt(2/3)':>10s} {'diff':>10s} "
          f"{'E_0':>10s} {'E_1':>10s}")

    n_grid = 3000
    rho_min = 0.002
    rho_max = 15

    gaps_data = []
    for c in [5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]:
        drho = (rho_max - rho_min) / n_grid
        rho_grid = np.linspace(rho_min, rho_max, n_grid)
        V = np.array([log(2 * sinh(r)) if r > 0.001 else log(0.002)
                      for r in rho_grid])

        T_coeff = 1.0 / (2 * c * drho**2)
        H = np.diag(V) + T_coeff * (2 * np.eye(n_grid)
            - np.eye(n_grid, k=1) - np.eye(n_grid, k=-1))

        evals = np.linalg.eigvalsh(H)
        gap = evals[1] - evals[0]
        gaps_data.append((c, gap))

        print(f"  {c:8.0f} {gap:10.6f} {sqrt(2/3):10.6f} "
              f"{gap - sqrt(2/3):+10.6f} {evals[0]:10.6f} {evals[1]:10.6f}")

    # Fit: gap(c) = a + b/c + d/c^2
    c_arr = np.array([g[0] for g in gaps_data])
    gap_arr = np.array([g[1] for g in gaps_data])

    A = np.column_stack([1/c_arr, 1/c_arr**2, np.ones(len(c_arr))])
    coeffs, _, _, _ = np.linalg.lstsq(A, gap_arr, rcond=None)

    print(f"\n  Fit: gap = {coeffs[2]:.8f} + {coeffs[0]:.4f}/c + {coeffs[1]:.2f}/c^2")
    print(f"  Asymptotic gap: {coeffs[2]:.8f}")
    print(f"  sqrt(2/3) = {sqrt(2/3):.8f}")
    print(f"  Diff = {coeffs[2] - sqrt(2/3):.8f}")


# =====================================================================
# PART 3: The WKB analysis of the gap
# =====================================================================

def wkb_gap_analysis():
    """WKB analysis of the mass gap for V = log(2sinh rho).

    The gap in WKB is determined by the quantization condition:
    integral_{rho_1}^{rho_2} sqrt(2c(E - V(rho))) drho = (n + 1/2) pi

    For the GROUND STATE (n=0): this gives E_0.
    For the FIRST EXCITED (n=1): this gives E_1.
    The gap: Delta_E = E_1 - E_0.

    At large c: the semiclassical limit. The turning points
    rho_1 and rho_2 satisfy V(rho_i) = E. Since V = log(2sinh rho),
    the turning points are:
    rho_1 = arcsinh(exp(E)/2) (inner turning point)... wait,
    V is monotonically increasing, so there's only ONE turning point
    for E > V_min.

    Actually: V(rho) = log(2sinh rho).
    V(0) = -inf (log singularity).
    V increases monotonically from -inf to +inf.
    So V = E has exactly ONE solution rho_E.

    For a potential with one turning point and a hard wall at rho = 0:
    The WKB condition becomes:
    integral_0^{rho_E} sqrt(2c(E - V)) drho = (n + 3/4) pi

    (The 3/4 comes from the hard wall at 0 and the turning point.)

    The gap: Delta = d E/d n at n = 0.
    dE/dn = pi / [integral_0^{rho_E} sqrt(c/(2(E-V))) drho]
    """
    print(f"\n{'='*72}")
    print("  WKB ANALYSIS OF THE GAP")
    print("=" * 72)

    # Numerical WKB: compute the action integral for various E
    print(f"\n  The WKB quantization condition:")
    print(f"  S(E) = integral sqrt(2c(E - V)) drho = (n + 3/4) pi\n")

    for c in [50, 100, 500, 1000]:
        print(f"  c = {c}:")
        print(f"  {'E':>8s} {'S(E)':>12s} {'S/pi':>10s} {'n+3/4':>10s}")

        E_values = np.linspace(-3, 3, 50)
        for E in E_values:
            # Numerical integration
            n_pts = 5000
            rho_pts = np.linspace(0.001, 15, n_pts)
            drho = rho_pts[1] - rho_pts[0]

            integrand = np.zeros(n_pts)
            for i, r in enumerate(rho_pts):
                V = log(2 * sinh(r))
                diff = E - V
                if diff > 0:
                    integrand[i] = sqrt(2 * c * diff)

            S = np.sum(integrand) * drho
            n_eff = S / pi - 0.75

            if abs(n_eff - round(n_eff)) < 0.1 and n_eff >= -0.5:
                print(f"  {E:8.4f} {S:12.4f} {S/pi:10.4f} "
                      f"{n_eff + 0.75:10.4f}  <-- n = {round(n_eff)}")

        # Extract gap from the WKB eigenvalues
        print()


# =====================================================================
# PART 4: The exact large-c limit
# =====================================================================

def large_c_exact():
    """Compute the gap in the exact large-c limit analytically.

    For c -> inf: the kinetic term vanishes and the spectrum
    becomes continuous. The gap goes to zero as 1/sqrt(c).

    Wait: that contradicts our numerical finding that the gap
    stays O(1) as N increases.

    The resolution: the potential ALSO depends on N (through the shift).
    As c = N^2 increases, the shift b - f ~ -N^2/24 makes the potential
    DEEPER. The deepening COUNTERACTS the vanishing kinetic term.

    The effective description: in the rescaled variable u = N*rho,
    the rescaled potential is:
    V(u/N) = log(2sinh(u/N)) + b(N) - f(m*)
           = log(2u/N) + u^2/(6N^2) + ... + b - f
           = log(u) - log(N/2) + u^2/(6N^2) + b(N) - f(m*)

    The terms -log(N/2) + b(N) - f(m*):
    b = N^2/12 + N/12 - log2 + log(N)/(N-1)
    f = N^2/8

    -log(N/2) + b - f = -log(N) + log(2) + N^2/12 + N/12 - log2 + logN/(N-1) - N^2/8
                       = -log(N) + N^2/12 - N^2/8 + N/12 + logN/(N-1)
                       = -N^2/24 - log(N) + N/12 + logN/(N-1)
                       ~ -N^2/24 for large N.

    So the rescaled potential:
    W(u) = log(u) + u^2/(6N^2) - N^2/24 + O(N)

    The eigenvalue equation in the rescaled frame:
    [-1/2 d^2/du^2 + W(u)] Psi = E Psi

    The energy E is RELATIVE to the potential minimum.
    The minimum of W is at u_min where W'(u_min) = 0:
    1/u + u/(3N^2) = 0 -> u_min^2 = -3N^2 (negative, no minimum for u > 0!)

    This means the rescaled potential is MONOTONICALLY DECREASING
    from the log singularity at u = 0 to... wait, that's wrong.

    W(u) = log(u) + u^2/(6N^2) + const.
    W'(u) = 1/u + u/(3N^2) > 0 for all u > 0.

    So W is MONOTONICALLY INCREASING for all u > 0.
    There is NO minimum! The potential goes from -inf at u = 0
    to +inf at u = inf.

    The bound states come from the HARD WALL at u = 0 (where V = -inf,
    repelling the wavefunction) and the confining potential at large u.
    """
    print(f"\n{'='*72}")
    print("  THE EXACT LARGE-c LIMIT")
    print("=" * 72)

    print(f"""
  The potential V(rho) = log(2sinh rho) is MONOTONICALLY INCREASING.
  There is no minimum. The bound states come from the balance between:
  - The LOG REPULSION at rho = 0 (pushes the wavefunction to the right)
  - The LINEAR CONFINEMENT at large rho (pushes it to the left)

  The WKB turning point for energy E:
  V(rho_E) = E -> 2sinh(rho_E) = exp(E) -> rho_E = arcsinh(exp(E)/2)

  The DENSITY OF STATES at energy E:
  g(E) = dN/dE = d/dE [S(E)/pi]

  where S(E) = integral_0^{{rho_E}} sqrt(2c(E - log(2sinh rho))) drho

  For E >> 1: rho_E ~ E, S ~ sqrt(c) * E^{{3/2}} / ...
  g(E) ~ sqrt(c) * sqrt(E)

  The gap: Delta = 1/g(E_0) ~ 1/(sqrt(c) * sqrt(E_0))

  For the ground state E_0 of log(2sinh):
  E_0 depends on c through the WKB quantization:
  S(E_0) = (3/4) pi -> integral ~ (3/4) pi / sqrt(c)

  This is a SMALL action, meaning E_0 is NEAR the bottom of the potential.
  For small rho: V ~ log(2rho) ~ log(rho) + log(2).
  The ground state in V = log(rho) with kinetic -1/(2c) d^2/drho^2:

  This is the 1D hydrogen problem in log coordinates!
  Let x = log(rho), then the Schrodinger equation becomes:
  -1/(2c) [e^{{-2x}} d^2/dx^2 - e^{{-2x}} d/dx] Psi + x Psi = (E - log2) Psi

  This doesn't simplify cleanly. Let me just compute numerically
  with high precision.
""")

    # High-precision computation with finer grid
    print(f"  High-precision gap computation:\n")
    print(f"  {'c':>8s} {'n_grid':>8s} {'gap':>12s} {'E_0':>10s} {'E_1':>10s}")

    for c, n_g in [(50, 4000), (100, 4000), (200, 4000),
                    (500, 5000), (1000, 5000), (2000, 6000)]:
        rho_min = 0.001
        rho_max = 12
        drho = (rho_max - rho_min) / n_g
        rho_grid = np.linspace(rho_min, rho_max, n_g)

        V = np.array([log(2 * sinh(r)) for r in rho_grid])

        T = 1.0 / (2 * c * drho**2)
        H = np.diag(V) + T * (2 * np.eye(n_g)
            - np.eye(n_g, k=1) - np.eye(n_g, k=-1))

        evals = np.linalg.eigvalsh(H)
        gap = evals[1] - evals[0]

        print(f"  {c:8.0f} {n_g:8d} {gap:12.8f} {evals[0]:10.6f} "
              f"{evals[1]:10.6f}")

    # Check the 1/c^{1/3} scaling
    print(f"\n  Testing gap = a * c^alpha:")
    c_vals = [50, 100, 200, 500, 1000, 2000]
    gap_vals = []
    for c in c_vals:
        n_g = 4000
        rho_min = 0.001
        rho_max = 12
        drho = (rho_max - rho_min) / n_g
        rho_grid = np.linspace(rho_min, rho_max, n_g)
        V = np.array([log(2 * sinh(r)) for r in rho_grid])
        T = 1.0 / (2 * c * drho**2)
        H = np.diag(V) + T * (2 * np.eye(n_g)
            - np.eye(n_g, k=1) - np.eye(n_g, k=-1))
        evals = np.linalg.eigvalsh(H)
        gap_vals.append(evals[1] - evals[0])

    log_c = np.log(c_vals)
    log_gap = np.log(gap_vals)
    A = np.column_stack([log_c, np.ones(len(log_c))])
    coeffs, _, _, _ = np.linalg.lstsq(A, log_gap, rcond=None)
    alpha = coeffs[0]
    a = exp(coeffs[1])

    print(f"  gap ~ {a:.6f} * c^{alpha:.6f}")
    print(f"  If alpha = -1/3: gap ~ c^(-1/3) -> 0 as c -> inf")
    print(f"  If alpha = 0: gap -> const as c -> inf")
    print(f"  Measured alpha = {alpha:.6f}")

    # The gap * c^{1/3}
    print(f"\n  {'c':>8s} {'gap':>12s} {'gap*c^(1/3)':>14s} "
          f"{'gap*c^(1/2)':>14s} {'gap*c':>14s}")

    for c, g in zip(c_vals, gap_vals):
        print(f"  {c:8.0f} {g:12.8f} {g * c**(1/3):14.6f} "
              f"{g * c**(1/2):14.6f} {g * c:14.4f}")


# =====================================================================
# MAIN
# =====================================================================

def main():
    print("=" * 72)
    print("  LARGE-N BEHAVIOR OF THE MASS GAP")
    print("=" * 72)

    compare_gaps()
    pure_potential_gap_vs_c()
    large_c_exact()

    print(f"\n{'='*72}")
    print("  CONCLUSION")
    print("=" * 72)


if __name__ == "__main__":
    main()
