"""
Langer residual diagnostic: phase vs amplitude separation.

The paper claims delta_S^{Langer} = -ln2/(2c) is an AMPLITUDE correction
(correction to ln|psi|, i.e., the WKB action's real part), NOT a phase
correction.

This script separates the two:
  1. PHASE: BS residual alpha = Phi/pi - n_zeros  (should be ~0.25 from Maslov)
  2. AMPLITUDE: Prüfer envelope R vs WKB |V|^{-1/4} normalization
  3. COMBINED: Both at several c values to determine scaling

Run: python3 scripts/langer_diagnostic.py
"""
from math import asinh, cosh, exp, log, pi, sinh, sqrt, atan2
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
# ODE solver
# ================================================================

def solve_wdw(c, N, rho_end, rho_start=1e-6):
    b0 = beta_0(N)
    psi0 = 1.0 + c * rho_start**2 * (b0 + log(rho_start) - 1.5)
    psip0 = 2.0 * c * rho_start * (b0 + log(rho_start) - 1.0)

    def ode(rho, y):
        return [y[1], 2 * c * V_BO(rho, N) * y[0]]

    sol = solve_ivp(ode, [rho_start, rho_end], [psi0, psip0],
                    method='DOP853', rtol=1e-13, atol=1e-15,
                    dense_output=True)
    return sol

# ================================================================
# WKB phase integral
# ================================================================

def wkb_phase(c, N, rho_start=1e-12, rho_end=None):
    if rho_end is None:
        rho_end = rho_star(N)

    def integrand(rho):
        v = V_BO(rho, N)
        if v >= 0:
            return 0.0
        return sqrt(2 * c * abs(v))

    result, _ = quad(integrand, rho_start, rho_end, limit=1000)
    return result

# ================================================================
# Phase diagnostic: BS residual
# ================================================================

def phase_diagnostic(c, N, rho_start=1e-6, verbose=True):
    """Extract the BS phase residual."""
    rs = rho_star(N)
    rho_end = rs * 0.999

    sol = solve_wdw(c, N, rho_end, rho_start)
    if not sol.success:
        return None, None

    # Count zeros using the solver's own output points (already adaptive)
    psis = sol.y[0]
    signs = np.sign(psis)
    n_zeros_coarse = np.sum(np.diff(signs) != 0)

    # Also use dense output for finer count
    n_pts = max(5000, int(50 * sqrt(c)))
    rhos = np.linspace(rho_start, rho_end, n_pts)
    psis_dense = sol.sol(rhos)[0]
    signs_dense = np.sign(psis_dense)
    n_zeros = np.sum(np.diff(signs_dense) != 0)

    # WKB phase
    Phi = wkb_phase(c, N, rho_start, rho_end)
    alpha = Phi / pi - n_zeros

    if verbose:
        print(f"  c={c:10.2f}: n_zeros={n_zeros:4d} (check:{n_zeros_coarse:4d}), "
              f"Phi/pi={Phi/pi:12.6f}, alpha={alpha:12.8f}")

    return alpha, n_zeros

# ================================================================
# Amplitude diagnostic: Prüfer envelope
# ================================================================

def amplitude_diagnostic(c, N, rho_obs, rho_start=1e-6, verbose=True):
    """Extract the Prüfer envelope at rho_obs and compare with WKB.

    The Prüfer envelope R is defined by:
      R^2 = psi^2 + (psi' / p)^2   where p = sqrt(2c|V|)

    In WKB: R = A |V|^{-1/4} where A is the normalization constant.
    So the "normalized envelope" E = R * |V|^{1/4} should be approximately
    constant (= A) across the classical region.

    We compare E at rho_obs with E at a reference point.
    """
    rs = rho_star(N)
    rho_end = rs * 0.95  # stay well inside classical region

    sol = solve_wdw(c, N, rho_end, rho_start)
    if not sol.success:
        return None

    # Evaluate psi and psi' at rho_obs
    y = sol.sol(rho_obs)
    psi, psip = y[0], y[1]
    V = V_BO(rho_obs, N)

    if V >= 0:
        return None

    p = sqrt(2 * c * abs(V))
    R = sqrt(psi**2 + (psip / p)**2)
    E = R * abs(V)**0.25  # normalized envelope

    # Also evaluate at a reference point (rho* / 2)
    rho_ref = rs / 2
    y_ref = sol.sol(rho_ref)
    psi_ref, psip_ref = y_ref[0], y_ref[1]
    V_ref = V_BO(rho_ref, N)
    p_ref = sqrt(2 * c * abs(V_ref))
    R_ref = sqrt(psi_ref**2 + (psip_ref / p_ref)**2)
    E_ref = R_ref * abs(V_ref)**0.25

    if verbose:
        print(f"  c={c:10.2f}: E(obs)={E:14.10f}, E(ref)={E_ref:14.10f}, "
              f"ratio={E/E_ref:14.10f}, ln(ratio)={log(E/E_ref):14.10f}")

    return E, E_ref, log(E/E_ref)

# ================================================================
# Envelope scan: measure E at several rho values
# ================================================================

def envelope_scan(c, N, rho_start=1e-6, n_points=200, verbose=True):
    """Measure the Prüfer envelope E(rho) across the classical region."""
    rs = rho_star(N)
    rho_end = rs * 0.90

    sol = solve_wdw(c, N, rho_end, rho_start)
    if not sol.success:
        return None

    rhos = np.linspace(rs * 0.05, rho_end, n_points)
    Es = []
    for rho in rhos:
        y = sol.sol(rho)
        psi, psip = float(y[0]), float(y[1])
        V = V_BO(rho, N)
        if V >= 0:
            Es.append(None)
            continue
        p = sqrt(2 * c * abs(V))
        R = sqrt(psi**2 + (psip / p)**2)
        E = R * abs(V)**0.25
        Es.append(E)

    # Filter Nones
    valid = [(r, e) for r, e in zip(rhos, Es) if e is not None]
    rhos_v = np.array([r for r, e in valid])
    Es_v = np.array([e for r, e in valid])

    # Fit E(rho) = A + B * rho + C * rho^2 to check constancy
    if len(valid) > 3:
        mat = np.column_stack([np.ones(len(rhos_v)), rhos_v, rhos_v**2])
        fit, _, _, _ = np.linalg.lstsq(mat, Es_v, rcond=None)
        A, B, C = fit
        E_mean = np.mean(Es_v)
        E_std = np.std(Es_v)
        rel_var = E_std / E_mean if E_mean != 0 else float('inf')

        if verbose:
            print(f"  c={c:10.2f}: E_mean={E_mean:14.10f}, E_std={E_std:.6e}, "
                  f"rel_var={rel_var:.6e}")
            print(f"            fit: E = {A:.10f} + {B:.6e}*rho + {C:.6e}*rho^2")

        return E_mean, E_std, rel_var

    return None

# ================================================================
# Main
# ================================================================

if __name__ == "__main__":
    print("=" * 78)
    print("  LANGER RESIDUAL DIAGNOSTIC")
    print("  Separating PHASE (BS residual) from AMPLITUDE (Prüfer envelope)")
    print("=" * 78)

    for N in [7, 11]:
        c_base = c_N_val(N)
        rs = rho_star(N)
        b0 = beta_0(N)

        print(f"\n{'='*78}")
        print(f"  N = {N}")
        print(f"  c_base = {c_base:.4f}, rho* = {rs:.6f}, beta0 = {b0:.6f}")
        print(f"  Paper claim: delta_S = -ln2/(2c), so at c_base: {-log(2)/(2*c_base):.10f}")
        print(f"{'='*78}")

        # --- PHASE ---
        print(f"\n  --- PHASE: BS residual alpha = Phi/pi - n_zeros ---")
        print(f"  (Should be ~0.25 from Maslov if WKB is exact)")
        alphas = []
        for k in [1, 2, 4, 8, 16, 32]:
            c = c_base * k
            alpha, n_zeros = phase_diagnostic(c, N)
            if alpha is not None:
                alphas.append((c, alpha))

        if alphas:
            print(f"\n  Scaling of alpha:")
            print(f"  {'c':>12s}  {'alpha':>14s}  {'alpha-0.25':>14s}")
            for c, alpha in alphas:
                print(f"  {c:12.2f}  {alpha:14.10f}  {alpha-0.25:14.10f}")

        # --- AMPLITUDE ---
        print(f"\n  --- AMPLITUDE: Prüfer envelope constancy ---")
        print(f"  (E = R |V|^(1/4) should be constant if WKB amplitude is exact)")
        for k in [1, 2, 4, 8, 16]:
            c = c_base * k
            result = envelope_scan(c, N)

        # --- AMPLITUDE at fixed observation point ---
        print(f"\n  --- AMPLITUDE: E(rho_obs) vs c ---")
        print(f"  (If Langer correction is 1/c, then E should have a 1/c piece)")
        rho_obs = rs * 0.4  # deep in classical region
        E_data = []
        for k in [1, 2, 4, 8, 16, 32]:
            c = c_base * k
            result = amplitude_diagnostic(c, N, rho_obs)
            if result is not None:
                E, E_ref, ln_ratio = result
                E_data.append((c, E, E_ref, ln_ratio))

        if E_data:
            print(f"\n  Scaling of ln(E(obs)/E(ref)) at rho_obs={rho_obs:.4f}:")
            print(f"  {'c':>12s}  {'ln(ratio)':>14s}  {'ratio*c':>12s}  "
                  f"{'ratio*sqrt(c)':>14s}  {'ratio*log(c)':>14s}")
            for c, E, E_ref, lr in E_data:
                print(f"  {c:12.2f}  {lr:14.10f}  {lr*c:12.6f}  "
                      f"{lr*sqrt(c):14.8f}  {lr*log(c):14.8f}")

    print("\n" + "=" * 78)
    print("  UNIVERSAL LOG-AIRY: psi'' = (a + log x) psi")
    print("=" * 78)

    for a in [-3, -5, -8, -12, -16, -20]:
        x0 = exp(-a)
        x_end = x0 * 0.999
        x_start = 1e-8

        b0 = a + log(x_start)
        psi0 = 1.0 + x_start**2 / 2 * (b0 - 1.5)
        psip0 = x_start * (b0 - 1.0)

        def ode(x, y, a_val=a):
            return [y[1], (a_val + log(x)) * y[0]]

        sol = solve_ivp(ode, [x_start, x_end], [psi0, psip0],
                        method='DOP853', rtol=1e-13, atol=1e-15,
                        dense_output=True)

        if not sol.success:
            print(f"  a={a}: FAILED")
            continue

        # Count zeros
        n_pts = max(5000, int(50 * sqrt(abs(a)) * x0))
        n_pts = min(n_pts, 200000)
        xs = np.linspace(x_start, x_end, n_pts)
        psis = sol.sol(xs)[0]
        signs = np.sign(psis)
        n_zeros = np.sum(np.diff(signs) != 0)

        # WKB phase
        def integrand(x, a_val=a):
            v = a_val + log(x)
            if v >= 0:
                return 0.0
            return sqrt(abs(v))

        Phi, _ = quad(integrand, x_start, x_end, limit=1000)
        alpha = Phi / pi - n_zeros

        print(f"  a={a:5.0f}: n_zeros={n_zeros:4d}, Phi/pi={Phi/pi:10.4f}, "
              f"alpha={alpha:12.8f}, alpha-0.25={alpha-0.25:14.10f}")

    print("\nDone.")
