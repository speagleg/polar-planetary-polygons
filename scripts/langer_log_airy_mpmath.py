"""
High-precision extraction of the Langer residual using mpmath.

The log-Airy equation: psi'' = (a + log(x)) psi
Regular BC: psi(0) = 1, psi'(0) = 0.

Strategy: solve the ODE at 50-digit precision using mpmath's Taylor
series ODE solver (odefun). Extract the Prufer phase in the classical
region, compare with WKB, and isolate the 1/|a| correction.

Also: solve the FULL WDW equation -psi''/(2c) + V(rho) psi = 0 at
high precision and extract the 1/c Langer coefficient directly.

Requires: mpmath (pip install mpmath)
Run: python3 scripts/langer_log_airy_mpmath.py

Cross-reference: spiral-hexagon/src/spiral_hexagon/gap_b_olver_constant.py
uses the same mpmath framework for Olver remainder bounds.
"""
import sys
try:
    import mpmath as mp
except ImportError:
    print("mpmath not installed. Run: pip install mpmath")
    sys.exit(1)

mp.mp.dps = 50  # 50 decimal digits

# ================================================================
# Part 1: The universal log-Airy equation psi'' = (a + log x) psi
# ================================================================

def V_logairy(x, a):
    return a + mp.log(x)

def solve_logairy_taylor(a_val, x_start=None, x_end=None, n_steps=10000):
    """Solve psi'' = (a + log x) psi using mpmath's odefun (Taylor series).

    Returns (x_values, psi_values, psip_values).
    """
    a = mp.mpf(a_val)
    x0_tp = mp.exp(-a)  # turning point

    if x_start is None:
        x_start = mp.power(10, -8)
    if x_end is None:
        x_end = x0_tp * mp.mpf('0.9')

    # Series seed at x_start
    b0 = a + mp.log(x_start)
    psi0 = 1 + x_start**2 / 2 * (b0 - mp.mpf('3')/2)
    psip0 = x_start * (b0 - 1)

    # ODE system: y0 = psi, y1 = psi'
    def f(x, y):
        return [y[1], (a + mp.log(x)) * y[0]]

    # Use mpmath's odefun with Taylor method
    solver = mp.odefun(f, mp.mpf(x_start), [psi0, psip0], tol=mp.power(10, -45))

    dx = (x_end - x_start) / n_steps
    xs = [x_start + i * dx for i in range(n_steps + 1)]
    results = []
    for x in xs:
        y = solver(x)
        results.append((x, y[0], y[1]))

    return results

def count_zeros_precise(results):
    """Count zero crossings in the solution."""
    n = 0
    for i in range(1, len(results)):
        if results[i-1][1] * results[i][1] < 0:
            n += 1
    return n

def wkb_phase_logairy(a_val, x_from, x_to):
    """WKB phase integral for the log-Airy equation."""
    a = mp.mpf(a_val)
    def integrand(x):
        v = a + mp.log(x)
        return mp.sqrt(mp.fabs(v)) if v < 0 else mp.mpf(0)
    return mp.quad(integrand, [x_from, x_to])

# ================================================================
# Part 2: Full WDW equation -psi''/(2c) + V(rho) psi = 0
# ================================================================

def b_exact(N):
    N = mp.mpf(N)
    return N*(N+1)/12 - mp.log(2) + mp.log(N)/(N-1)

def f_star(N):
    m = N // 2
    return mp.mpf(m * (N - m)) / 2

def V_WDW(rho, N):
    return mp.log(2 * mp.sinh(rho)) + b_exact(N) - f_star(N)

def rho_star(N):
    return mp.asinh(mp.exp(f_star(N) - b_exact(N)) / 2)

def solve_wdw_mpmath(c_val, N, rho_start=None, rho_end=None, n_steps=5000):
    """Solve -psi''/(2c) + V(rho) psi = 0 at arbitrary precision."""
    c = mp.mpf(c_val)
    if rho_start is None:
        rho_start = mp.power(10, -8)
    if rho_end is None:
        rho_end = rho_star(N) * mp.mpf('0.5')

    beta0 = mp.log(2) + b_exact(N) - f_star(N)
    psi0 = 1 + c * rho_start**2 * (beta0 + mp.log(rho_start) - mp.mpf('3')/2)
    psip0 = 2 * c * rho_start * (beta0 + mp.log(rho_start) - 1)

    def f(rho, y):
        return [y[1], 2 * c * V_WDW(rho, N) * y[0]]

    solver = mp.odefun(f, rho_start, [psi0, psip0], tol=mp.power(10, -45))

    dx = (rho_end - rho_start) / n_steps
    xs = [rho_start + i * dx for i in range(n_steps + 1)]
    results = []
    for x in xs:
        y = solver(x)
        results.append((x, y[0], y[1]))

    return results

# ================================================================
# Part 3: Extract the 1/c coefficient
# ================================================================

def extract_langer_coefficient(N, multipliers=None):
    """Extract the 1/c Langer coefficient by solving at multiple c values
    and using Richardson extrapolation.

    Returns the coefficient D in: residual = A + B/sqrt(c) + D/c + ...
    """
    if multipliers is None:
        multipliers = [1, 2, 4, 8, 16, 32]

    c_base = float(12 * b_exact(N))
    rho_match = float(rho_star(N)) / 2

    print(f"\nN = {N}, c_base = {c_base:.4f}, rho_match = {rho_match:.4f}")
    print(f"beta0 = {float(b_exact(N) + mp.log(2) - f_star(N)):.6f}")
    print(f"Predicted: -Log[2]/2 = {float(-mp.log(2)/2):.10f}")
    print()

    data = []
    for k in multipliers:
        c = c_base * k
        results = solve_wdw_mpmath(c, N, rho_end=mp.mpf(rho_match))

        psi_m = results[-1][1]
        V_m = V_WDW(mp.mpf(rho_match), N)

        exact_log = float(mp.log(mp.fabs(psi_m)))
        wkb_log = float(-mp.mpf('0.25') * mp.log(mp.fabs(V_m)))
        residual = exact_log - wkb_log

        data.append((c, residual))
        print(f"  c = {c:10.2f} ({k:3d}x): ln|psi| = {exact_log:20.14f}, "
              f"WKB = {wkb_log:14.10f}, resid = {residual:16.12f}")

    # Richardson: fit resid = A + D/c using last two points
    if len(data) >= 2:
        c1, r1 = data[-2]
        c2, r2 = data[-1]
        # r = A + D/c => r1 c1 = A c1 + D, r2 c2 = A c2 + D
        # D = (r1 c1 - r2 c2) / (1 - c2/c1) ... no
        # D = (r1 c1 c2 - r2 c1 c2) / (c2 - c1) = c1 c2 (r1-r2)/(c2-c1)
        D = c1 * c2 * (r1 - r2) / (c2 - c1)
        A = r1 - D / c1
        print(f"\n  Richardson (last 2): A = {A:.10f}, D = {D:.10f}")
        print(f"  Compare: -Log[2]/2 = {float(-mp.log(2)/2):.10f}")
        print(f"  Ratio D/(-Log[2]/2) = {D / float(-mp.log(2)/2):.10f}")

    # Better: use ALL points with least-squares fit to A + B/sqrt(c) + D/c
    if len(data) >= 3:
        import numpy as np
        cs = np.array([d[0] for d in data])
        rs = np.array([d[1] for d in data])
        mat = np.column_stack([np.ones(len(cs)), 1/np.sqrt(cs), 1/cs])
        fit, _, _, _ = np.linalg.lstsq(mat, rs, rcond=None)
        A, B, D = fit
        print(f"\n  Least-squares (A + B/sqrt(c) + D/c):")
        print(f"    A = {A:.12f}")
        print(f"    B = {B:.12f}")
        print(f"    D = {D:.12f}")
        print(f"    -Log[2]/2 = {float(-mp.log(2)/2):.12f}")
        print(f"    Ratio D/(-Log[2]/2) = {D/float(-mp.log(2)/2):.12f}")

    return data

# ================================================================
# Main
# ================================================================

if __name__ == "__main__":
    print("=" * 72)
    print("  LANGER RESIDUAL: HIGH-PRECISION EXTRACTION (mpmath, 50 digits)")
    print("=" * 72)

    print("\n" + "=" * 72)
    print("  PART 1: Universal log-Airy equation psi'' = (a + log x) psi")
    print("=" * 72)

    for a in [-3, -5, -8]:
        a_val = mp.mpf(a)
        x0 = mp.exp(-a_val)
        x_end = x0 * mp.mpf('0.9')

        print(f"\na = {a}: x0 = {float(x0):.2f}")

        results = solve_logairy_taylor(a_val, n_steps=min(5000, int(float(x0) * 10)))
        n_zeros = count_zeros_precise(results)
        phi = float(wkb_phase_logairy(a_val, mp.power(10, -8), x_end))

        delta_n = n_zeros - phi / float(mp.pi)
        print(f"  n_zeros = {n_zeros}, Phi/pi = {phi/float(mp.pi):.6f}, "
              f"delta = {delta_n:.8f}")

    print("\n" + "=" * 72)
    print("  PART 2: Full WDW equation at N = 7, 11")
    print("=" * 72)

    for N in [7, 11]:
        data = extract_langer_coefficient(N, multipliers=[1, 2, 4, 8, 16, 32])

    print("\nDone.")
