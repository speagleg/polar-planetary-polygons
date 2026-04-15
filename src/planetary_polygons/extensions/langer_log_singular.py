"""
Rigorous Langer-type connection formula for potentials with logarithmic singularities.

The WDW equation:
    -ψ''(ρ)/(2c) + V(ρ) ψ(ρ) = 0,   V(ρ) = log(2 sinh ρ) + (b - f)

has a logarithmic singularity at ρ = 0:
    V(ρ) = log(2ρ) + (b-f) + O(ρ²) = β₀ + log ρ + O(ρ²),   β₀ := log 2 + (b-f).

Near ρ = 0, the equation becomes (to leading order):
    -ψ''/(2c) + (log ρ + β₀) ψ = 0.

This has solutions that are NOT standard Bessel or Airy — they involve the equation
    -χ''/(2c) + (log ρ + β₀) χ = 0
which is related to Whittaker / Coulomb wave functions on the exponentiated variable.

STRATEGY for the Langer residual:
  1. Transform ρ = e^{-t} (t ∈ (0, ∞) as ρ ∈ (1, 0) decreasing).
  2. Equation becomes ψ'' + ψ' (dropping lower-order) with exponential damping.
  3. Compute the exact regular solution near ρ = 0.
  4. Match to the WKB expansion in the interior, extract the phase shift.

This file implements the numerical verification step-by-step.
"""
from __future__ import annotations

from math import cosh, exp, log, pi, sinh, sqrt
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq


# ----------------------------------------------------------------------
# Exact ODE solver with proper boundary conditions at ρ = 0
# ----------------------------------------------------------------------

def V_BO(rho: float, N: int) -> float:
    """Born-Oppenheimer potential: V(ρ) = log(2 sinh ρ) + b(N) - f(m*, N)."""
    b = N * (N + 1) / 12 - log(2) + log(N) / (N - 1)
    m_star = N // 2
    f_star = m_star * (N - m_star) / 2
    return log(2 * sinh(rho)) + b - f_star


def V_asymptotic_near_zero(rho: float, N: int) -> float:
    """Asymptotic form near ρ = 0: V ≈ log(2ρ) + (b - f) = β₀ + log ρ."""
    b = N * (N + 1) / 12 - log(2) + log(N) / (N - 1)
    m_star = N // 2
    f_star = m_star * (N - m_star) / 2
    beta_0 = log(2) + b - f_star
    return beta_0 + log(rho)


def regular_solution_series(rho: float, c: float, N: int, order: int = 4) -> tuple:
    """Return (ψ, ψ') for the regular solution ψ(ρ = 0) = 1, ψ'(0) finite.

    Near ρ = 0 with V = β₀ + log ρ:
        -ψ''/(2c) + (β₀ + log ρ) ψ = 0

    Substitute u = -log ρ (so ρ = e^{-u}, u large):
        ψ'_ρ = -e^u ψ_u;  ψ''_ρ = e^{2u}(ψ_uu + ψ_u)
        -e^{2u}(ψ_uu + ψ_u)/(2c) + (β₀ - u) ψ = 0
        ψ_uu + ψ_u + 2c e^{-2u}(u - β₀) ψ = 0

    At leading order (large u, small ρ): ψ_uu + ψ_u ≈ 0 → ψ(u) = A + B e^{-u}.
    In ρ variable: ψ(ρ) ≈ A + B ρ.

    Higher orders: ψ = A + B ρ + 2c ρ² × (next coefficient) + ...

    We compute the REGULAR solution where A = 1, B = 0 (symmetric initial).
    """
    b = N * (N + 1) / 12 - log(2) + log(N) / (N - 1)
    m_star = N // 2
    f_star = m_star * (N - m_star) / 2
    beta_0 = log(2) + b - f_star

    # Regular solution: ψ(0) = 1, ψ'(0) = 0 as starting seed
    # Corrections at O(ρ²): from the equation
    # -ψ''/(2c) + (β₀ + log ρ) ψ = 0 near ρ=0 with ψ ≈ 1:
    # ψ'' ≈ 2c(β₀ + log ρ)    (integrable singularity)
    # Need to integrate this: ψ'(ρ) = ∫₀^ρ 2c(β₀ + log ρ') dρ' = 2c [β₀ ρ + ρ(log ρ - 1)]
    # ψ(ρ) = 1 + 2c ∫₀^ρ [β₀ ρ' + ρ'(log ρ' - 1)] dρ'
    #      = 1 + 2c [β₀ ρ²/2 + (ρ² log ρ)/2 - ρ²/4 - ρ²/2]
    #      = 1 + c ρ² [β₀ + log ρ - 3/2]
    if rho <= 0:
        return (1.0, 0.0)
    psi = 1.0 + c * rho**2 * (beta_0 + log(rho) - 1.5)
    psi_prime = 2 * c * rho * (beta_0 + log(rho) - 1.0)
    return (psi, psi_prime)


def solve_WDW_from_zero(c: float, N: int, rho_end: float = 3.0, rho_start: float = 1e-4) -> dict:
    """Solve WDW ODE from rho_start to rho_end using the regular solution as seed."""
    psi0, psip0 = regular_solution_series(rho_start, c, N)

    def ode(rho, y):
        psi, psip = y
        V = V_BO(rho, N)
        return [psip, 2 * c * V * psi]

    sol = solve_ivp(ode, [rho_start, rho_end], [psi0, psip0],
                    method="DOP853", rtol=1e-13, atol=1e-15, max_step=0.001)
    return {"sol": sol, "psi": sol.y[0], "psip": sol.y[1], "rho": sol.t}


def WKB_phase_integral(c: float, N: int, rho_from: float, rho_to: float) -> float:
    """Compute the WKB phase integral ∫ sqrt(2c |V|) dρ from rho_from to rho_to."""
    def integrand(rho):
        V = V_BO(rho, N)
        return sqrt(2 * c * abs(V))
    result, _ = quad(integrand, rho_from, rho_to, limit=500)
    return result


def extract_langer_residual(c: float, N: int, rho_start: float = 1e-4, rho_match: float = 0.5) -> float:
    """Extract the Langer phase residual by matching numerical ODE to WKB at rho_match.

    The WKB log-amplitude at ρ_match should equal the integrated phase
    sqrt(2c) × ∫₀^{rho_match} sqrt(|V|) dρ, plus a subleading correction from
    the Langer regularization at ρ=0.

    The residual is:
        δS = log|ψ_exact(ρ_match)| - [ WKB leading amplitude at ρ_match ]
    """
    result = solve_WDW_from_zero(c, N, rho_end=rho_match + 0.01, rho_start=rho_start)
    sol = result["sol"]

    # Find ψ at ρ_match
    idx = np.argmin(np.abs(sol.t - rho_match))
    psi_match = sol.y[0][idx]
    rho_actual = sol.t[idx]

    # WKB leading log-amplitude at ρ_match:
    # In classical region (V < 0), ψ ≈ |V|^{-1/4} cos(phase).
    # Log-amplitude = -(1/4) log|V(rho_match)| (relative to phase=0 starting)
    V_match = V_BO(rho_actual, N)
    if V_match >= 0:
        return None  # Outside classical region

    wkb_log_amplitude = -0.25 * log(abs(V_match))
    exact_log_amplitude = log(abs(psi_match))

    residual = exact_log_amplitude - wkb_log_amplitude
    return residual


if __name__ == "__main__":
    print("=" * 72)
    print("Langer residual extraction at different c values (N = 11)")
    print("=" * 72)

    N = 11
    from src.planetary_polygons.extensions.cft_central_charge import b_N
    c_N_val = 12 * b_N(N)
    print(f"c_N = 12 b(N) = {c_N_val:.4f}")
    print(f"Predicted Langer residual: -ln 2/(2c_N) = {-log(2)/(2*c_N_val):.6f}\n")

    # Test at several c values
    for c in [c_N_val, 2*c_N_val, 4*c_N_val, 8*c_N_val]:
        residual = extract_langer_residual(c, N, rho_start=1e-5, rho_match=0.5)
        predicted = -log(2) / (2 * c)
        print(f"c = {c:.2f}: numerical residual = {residual:.6f}, predicted = {predicted:.6f}")

    # Extract 1/c coefficient by fitting residual(c) = D / c + ...
    print("\n=== 1/c coefficient extraction ===")
    cs = [c_N_val * k for k in [1, 2, 4, 8]]
    residuals = [extract_langer_residual(c, N, rho_start=1e-5, rho_match=0.5) for c in cs]

    # Fit residual(c) = A + D/c
    A_coef = np.array([[1, 1/c] for c in cs])
    coefs, *_ = np.linalg.lstsq(A_coef, residuals, rcond=None)
    A, D = coefs
    print(f"Fit: residual(c) = {A:.6f} + {D:.6f}/c")
    print(f"Compare: predicted 1/c coefficient = -ln 2 / 2 = {-log(2)/2:.6f}")
    print(f"Ratio: D / (-ln 2/2) = {D / (-log(2)/2):.4f}")
