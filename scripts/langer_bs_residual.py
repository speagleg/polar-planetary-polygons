"""
Langer residual via Bohr-Sommerfeld phase counting (scipy, fast).

Key insight: the PREVIOUS failure was in amplitude comparison (log(c)
transport contamination) and Prüfer phase tracking (accumulation over
O(sqrt(c)) cycles).  But ZERO COUNTING is robust at any precision:
just detect sign changes in psi.  The WKB phase integral is computed
via quadrature (no ODE accumulation error).

The BS residual is:
    alpha = Phi_WKB / pi  -  n_zeros

where alpha should be close to 1/4 (from the Maslov index at rho*).
Any deviation from 1/4 is the Langer correction.

Specifically:
    alpha = 1/4 + delta_Langer / pi

If the paper's claim holds: delta_Langer = -ln(2)/(2c),
so alpha - 1/4 = -ln(2)/(2 pi c).

Run: python3 scripts/langer_bs_residual.py
"""
from math import asinh, cosh, exp, log, pi, sinh, sqrt
import numpy as np
from scipy.integrate import solve_ivp, quad


# ================================================================
# Model
# ================================================================

def b_exact(N):
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)

def f_star(N):
    m = N // 2
    return m * (N - m) / 2

def c_N_val(N):
    return 12 * b_exact(N)

def V_BO(rho, N):
    return log(2 * sinh(rho)) + b_exact(N) - f_star(N)

def rho_star(N):
    return asinh(exp(f_star(N) - b_exact(N)) / 2)

def beta_0(N):
    return log(2) + b_exact(N) - f_star(N)


# ================================================================
# ODE solver: regular BC at rho = 0
# ================================================================

def solve_wdw(c, N, rho_end, rho_start=1e-6):
    """Solve psi'' = 2c V(rho) psi with regular BC at rho=0."""
    b0 = beta_0(N)
    psi0 = 1.0 + c * rho_start**2 * (b0 + log(rho_start) - 1.5)
    psip0 = 2.0 * c * rho_start * (b0 + log(rho_start) - 1.0)

    def ode(rho, y):
        return [y[1], 2 * c * V_BO(rho, N) * y[0]]

    # Let the adaptive solver choose steps.  DOP853 at rtol=1e-13
    # resolves the oscillatory solution without manual max_step tuning.
    sol = solve_ivp(ode, [rho_start, rho_end], [psi0, psip0],
                    method='DOP853', rtol=1e-13, atol=1e-15,
                    dense_output=True)
    return sol


def count_zeros(sol, rho_start, rho_end, n_per_cycle=30, c_val=None):
    """Count zero crossings of psi using dense output.

    Adaptive sampling: n_per_cycle points per estimated oscillation cycle.
    Falls back to 5000 points if c_val is not given.
    """
    if c_val is not None:
        # Rough estimate: max |V| ~ 10, so cycles ~ sqrt(2c*10)*L/(2pi)
        L = rho_end - rho_start
        n_cycles = sqrt(2 * c_val * 10) * L / (2 * pi)
        n_sample = max(2000, int(n_per_cycle * n_cycles))
    else:
        n_sample = 5000
    n_sample = min(n_sample, 100000)  # cap to avoid memory issues

    rhos = np.linspace(rho_start, rho_end, n_sample)
    psis = sol.sol(rhos)[0]
    signs = np.sign(psis)
    crossings = np.where(np.diff(signs) != 0)[0]
    return len(crossings)


# ================================================================
# WKB phase integral (via quadrature, no ODE accumulation)
# ================================================================

def wkb_phase(c, N, rho_start=1e-12, rho_end=None):
    """Compute Phi = int_{start}^{end} sqrt(2c|V|) drho."""
    if rho_end is None:
        rho_end = rho_star(N)

    def integrand(rho):
        v = V_BO(rho, N)
        if v >= 0:
            return 0.0
        return sqrt(2 * c * abs(v))

    # Split the integral to handle the log singularity at rho=0
    rho_mid = min(0.1, rho_end / 2)
    result1, err1 = quad(integrand, rho_start, rho_mid, limit=1000)
    result2, err2 = quad(integrand, rho_mid, rho_end, limit=1000)
    return result1 + result2


# ================================================================
# BS residual extraction
# ================================================================

def bs_residual(c, N, verbose=True):
    """Extract alpha = Phi/pi - n_zeros.

    The Maslov prediction is alpha = 1/4.
    Any deviation is the Langer correction.
    """
    rs = rho_star(N)
    rho_end = rs * 0.999  # stop just before turning point

    # Solve ODE
    sol = solve_wdw(c, N, rho_end)
    if not sol.success:
        return None

    # Count zeros
    n = count_zeros(sol, sol.t[0], sol.t[-1], c_val=c)

    # WKB phase integral (to the same endpoint)
    Phi = wkb_phase(c, N, rho_start=sol.t[0], rho_end=rho_end)

    alpha = Phi / pi - n

    if verbose:
        print(f"  c = {c:12.2f}: n_zeros = {n:4d}, Phi/pi = {Phi/pi:14.8f}, "
              f"alpha = {alpha:14.10f}, alpha-0.25 = {alpha-0.25:14.10f}")

    return alpha


def scan_N(N, multipliers=None, verbose=True):
    """Scan BS residual at several c values for given N."""
    if multipliers is None:
        multipliers = [1, 2, 4, 8, 16, 32, 64]

    c_base = c_N_val(N)
    rs = rho_star(N)
    b0 = beta_0(N)

    if verbose:
        print(f"\n{'='*78}")
        print(f"  N = {N},  c_base = {c_base:.4f},  rho* = {rs:.6f},  beta0 = {b0:.6f}")
        print(f"{'='*78}")
        print(f"  Maslov prediction: alpha = 0.25")
        print(f"  Paper claim: delta = -ln2/(2 pi c), so alpha - 0.25 = {-log(2)/(2*pi*c_base):.10f} at c_base")
        print()

    results = []
    for k in multipliers:
        c = c_base * k
        alpha = bs_residual(c, N, verbose=verbose)
        if alpha is not None:
            results.append((c, alpha))

    if verbose and len(results) >= 2:
        print(f"\n  --- Scaling analysis ---")
        print(f"  {'c':>12s}  {'alpha-0.25':>14s}  {'delta*c':>12s}  "
              f"{'delta*sqrt(c)':>14s}  {'delta*log(c)':>14s}")
        for c, alpha in results:
            d = alpha - 0.25
            print(f"  {c:12.2f}  {d:14.10f}  {d*c:12.6f}  "
                  f"{d*sqrt(c):14.8f}  {d*log(c):14.8f}")

        # Determine scaling: which product is most constant?
        deltas = [a - 0.25 for _, a in results]
        cs = [c for c, _ in results]

        prods_c = [d * c for d, c in zip(deltas, cs)]
        prods_sqrtc = [d * sqrt(c) for d, c in zip(deltas, cs)]
        prods_logc = [d * log(c) for d, c in zip(deltas, cs)]

        def variation(arr):
            if len(arr) < 2 or max(abs(x) for x in arr) < 1e-15:
                return float('inf')
            mean = sum(arr) / len(arr)
            return max(abs(x - mean) for x in arr) / abs(mean) if mean != 0 else float('inf')

        v_c = variation(prods_c)
        v_sqrt = variation(prods_sqrtc)
        v_log = variation(prods_logc)
        v_const = variation(deltas)

        print(f"\n  Relative variation of delta * f(c):")
        print(f"    delta (constant):    {v_const:.4f}")
        print(f"    delta * c:           {v_c:.4f}")
        print(f"    delta * sqrt(c):     {v_sqrt:.4f}")
        print(f"    delta * log(c):      {v_log:.4f}")

        best = min([(v_const, "O(1) — constant"),
                     (v_c, "O(1/c) — paper's claim"),
                     (v_sqrt, "O(1/sqrt(c))"),
                     (v_log, "O(1/log(c))")],
                    key=lambda x: x[0])
        print(f"  ==> Best fit: delta ~ {best[1]} (variation {best[0]:.4f})")

        if v_c < 0.1:
            D = sum(prods_c) / len(prods_c)
            print(f"\n  If 1/c: coefficient D = {D:.10f}")
            print(f"  Compare: -ln2/(2 pi) = {-log(2)/(2*pi):.10f}")
            print(f"  Compare: -ln2/2      = {-log(2)/2:.10f}")
            print(f"  Ratio D/(-ln2/(2pi)) = {D/(-log(2)/(2*pi)):.6f}")

    return results


# ================================================================
# Universal log-Airy equation
# ================================================================

def logairy_bs(a_val, rho_start=1e-8, verbose=True):
    """BS residual for psi'' = (a + log x) psi."""
    x0 = exp(-a_val)  # turning point
    x_end = x0 * 0.999

    b0 = a_val + log(rho_start)
    psi0 = 1.0 + rho_start**2 / 2 * (b0 - 1.5)
    psip0 = rho_start * (b0 - 1.0)

    def ode(x, y):
        return [y[1], (a_val + log(x)) * y[0]]

    sol = solve_ivp(ode, [rho_start, x_end], [psi0, psip0],
                    method='DOP853', rtol=1e-13, atol=1e-15,
                    dense_output=True)

    if not sol.success:
        if verbose:
            print(f"  a = {a_val}: ODE solver failed")
        return None

    # For log-Airy, estimate cycle count: |V| ~ |a|, wavelength ~ 2pi/sqrt|a|
    n_cycles_est = sqrt(abs(a_val)) * (x_end - rho_start) / (2 * pi)
    n_sample_la = max(2000, int(30 * n_cycles_est))
    n_sample_la = min(n_sample_la, 100000)
    rhos_la = np.linspace(sol.t[0], sol.t[-1], n_sample_la)
    psis_la = sol.sol(rhos_la)[0]
    signs_la = np.sign(psis_la)
    crossings_la = np.where(np.diff(signs_la) != 0)[0]
    n = len(crossings_la)

    def integrand(x):
        v = a_val + log(x)
        if v >= 0:
            return 0.0
        return sqrt(abs(v))

    x_mid = min(1.0, x_end / 2)
    Phi1, _ = quad(integrand, rho_start, x_mid, limit=1000)
    Phi2, _ = quad(integrand, x_mid, x_end, limit=1000)
    Phi = Phi1 + Phi2

    alpha = Phi / pi - n

    if verbose:
        print(f"  a = {a_val:8.2f}: x0 = {x0:10.2f}, n_zeros = {n:4d}, "
              f"Phi/pi = {Phi/pi:12.6f}, alpha = {alpha:12.8f}, "
              f"alpha-0.25 = {alpha-0.25:14.10f}")

    return alpha


# ================================================================
# Main
# ================================================================

if __name__ == "__main__":
    print("=" * 78)
    print("  LANGER RESIDUAL: Bohr-Sommerfeld zero-count extraction")
    print("  (scipy, fast, no amplitude contamination)")
    print("=" * 78)

    # ---- Full WDW equation at N = 7, 11 ----
    for N in [7, 11]:
        scan_N(N, multipliers=[1, 2, 4, 8, 16, 32, 64])

    # ---- Universal log-Airy equation ----
    print(f"\n{'='*78}")
    print("  UNIVERSAL LOG-AIRY:  psi'' = (a + log x) psi")
    print("  (No free parameters besides 'a')")
    print(f"{'='*78}")

    a_results = []
    for a in [-2, -3, -4, -5, -6, -7, -8, -10, -12, -15, -20]:
        alpha = logairy_bs(a)
        if alpha is not None:
            a_results.append((a, alpha))

    if a_results:
        print(f"\n  --- Log-Airy scaling ---")
        print(f"  {'a':>8s}  {'alpha-0.25':>14s}  {'d*|a|':>12s}  "
              f"{'d*|a|^{3/2}':>14s}  {'d*sqrt|a|':>12s}")
        for a, alpha in a_results:
            d = alpha - 0.25
            print(f"  {a:8.1f}  {d:14.10f}  {d*abs(a):12.6f}  "
                  f"{d*abs(a)**1.5:14.8f}  {d*sqrt(abs(a)):12.8f}")

    print("\nDone.")
