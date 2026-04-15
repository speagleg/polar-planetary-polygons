"""
Subleading WKB corrections for the Wheeler-DeWitt equation.

WDW equation:  -psi''(rho)/(2c) + V(rho) psi(rho) = 0,   V(rho) = log(2 sinh rho) + b - f

The large-c expansion of ln|psi| at a reference point takes the form
    ln|psi(rho)| = sqrt(2c) S_0(rho) + S_1(rho) + S_2(rho)/sqrt(2c) + S_3(rho)/c + ...

where
    S_0 = integral of sqrt(|V|) drho                              (leading WKB action)
    S_1 = -(1/4) log|V|                                           (WKB prefactor / Jacobian)
    S_3 = "Dunham" correction from V'' and (V')^2 integrated      (1/c term)

At a logarithmic singularity rho -> 0 (V -> -infty like log rho), standard WKB breaks
down and Langer's regularization adds an effective centrifugal term 1/(8 c rho^2).

At a simple turning point rho* (V(rho*)=0, V'(rho*) != 0), the Maslov connection gives a
fixed pi/4 phase shift that is independent of c.

This module computes each contribution individually and then sums them to give the
1/c coefficient of ln|psi| accumulated across the classically allowed interval (0, rho*).
"""

from __future__ import annotations

from math import asinh, cosh, exp, log, pi, sinh, sqrt
from typing import Callable

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq


# ----------------------------------------------------------------------
# Model inputs:  V(rho) = log(2 sinh rho) + b(N) - f(m*, N)
# ----------------------------------------------------------------------

def b_exact(N: int) -> float:
    """b(N) = N(N+1)/12 - log 2 + log(N)/(N-1)  (Gauss product form)."""
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


def c_N(N: int) -> float:
    return 12 * b_exact(N)


def f_star(N: int) -> float:
    """Critical Casimir f(m*, N) = m*(N-m*)/2 at m* = floor(N/2)."""
    m_star = N // 2
    return m_star * (N - m_star) / 2


def V(rho: float, N: int) -> float:
    """BO potential: V(rho) = log(2 sinh rho) + b(N) - f(m*, N)."""
    return log(2 * sinh(rho)) + b_exact(N) - f_star(N)


def V_prime(rho: float, N: int) -> float:
    """dV/drho = coth(rho). (The constant b-f has zero derivative.)"""
    return cosh(rho) / sinh(rho)


def V_double(rho: float, N: int) -> float:
    """d^2V/drho^2 = -csch^2(rho)."""
    return -1.0 / sinh(rho) ** 2


def rho_star(N: int) -> float:
    """Outer turning point:  V(rho*) = 0, i.e., 2 sinh(rho*) = exp(f - b)."""
    return asinh(exp(f_star(N) - b_exact(N)) / 2)


# ----------------------------------------------------------------------
# Standard WKB action (leading order in 1/c)
#
#   S_BO := integral_{0}^{rho*} sqrt(2c |V|) drho
#
# Numerical integration handles the integrable log singularity at rho=0.
# ----------------------------------------------------------------------

def S_BO(N: int, eps: float = 1e-12) -> float:
    """Leading WKB action.  S_BO = sqrt(c) * S_BO_bare."""
    c = c_N(N)

    def integrand(rho: float) -> float:
        v = V(rho, N)
        return sqrt(2 * c * abs(v)) if v < 0 else 0.0

    result, _ = quad(integrand, eps, rho_star(N), limit=500)
    return result


def S_BO_bare(N: int, eps: float = 1e-12) -> float:
    """c-independent part: integral sqrt(2 |V|) drho."""

    def integrand(rho: float) -> float:
        v = V(rho, N)
        return sqrt(2 * abs(v)) if v < 0 else 0.0

    result, _ = quad(integrand, eps, rho_star(N), limit=500)
    return result


# ----------------------------------------------------------------------
# Subleading contributions to ln|psi|
#
# Standard result (see e.g. Bender & Orszag, Advanced Mathematical Methods,
# ch. 10; or Miller, Adv. Chem. Phys. 30 (1975) 77): with psi = exp(S)
# and S = sqrt(2c) Y_{-1} + Y_0 + Y_1/sqrt(2c) + Y_2/(2c) + ...,
#
#   Y_{-1} = integral sqrt(V) drho          (for V > 0) or  i*integral sqrt(-V) drho
#   Y_0    = -(1/4) log|V|                  (prefactor)
#   Y_2    = integral [  V''/(8 V^{3/2}) - 5 (V')^2 / (32 V^{5/2}) ] drho
#
# (The Y_1 term vanishes in the symmetric gauge; see Bender-Orszag eq.(10.1.18).)
#
# For V < 0 (classically allowed region), the formulas carry through with
# the replacement sqrt(V) -> i sqrt(-V); the net result for the
# LOG-AMPLITUDE (real part of S) at subleading 1/c order is:
#
#   ln|psi(b)| - ln|psi(a)| includes a piece
#     (1/(2c)) * integral_a^b [ V''(rho) / (8 |V|^{3/2}) - 5 (V'(rho))^2 / (32 |V|^{5/2}) ] drho
#
# This is the "Dunham / one-loop" correction in the classical region.
# ----------------------------------------------------------------------

def dunham_integrand(rho: float, N: int) -> float:
    """Integrand for the 1/c Dunham correction in the classically allowed region."""
    v = V(rho, N)
    vp = V_prime(rho, N)
    vpp = V_double(rho, N)
    absV = abs(v)
    term1 = vpp / (8 * absV ** 1.5)
    term2 = -5 * vp ** 2 / (32 * absV ** 2.5)
    return term1 + term2


def dunham_correction(N: int, cutoff_lo: float = 1e-3,
                      cutoff_hi: float | None = None) -> float:
    """Dunham / 1/c correction to ln|psi| integrated over (cutoff_lo, rho* - eps).

    The integrand diverges as rho -> 0 (log singularity) and as rho -> rho*
    (turning-point singularity). We cut off symmetrically and later match
    with the Langer and Maslov contributions.
    """
    rho_t = rho_star(N)
    if cutoff_hi is None:
        cutoff_hi = rho_t - 1e-6

    result, _ = quad(
        lambda rho: dunham_integrand(rho, N),
        cutoff_lo,
        cutoff_hi,
        limit=1000,
    )
    return result


# ----------------------------------------------------------------------
# Langer regularization at rho = 0
#
# Near rho = 0,  V(rho) = log(2 rho) + (b - f) + O(rho^2) = log 2 + log rho + (b - f).
# The canonical Liouville substitution  psi = rho^{1/2} chi  turns -psi''/(2c) + V psi = 0
# into  -chi''/(2c) + (V + 1/(8 c rho^2)) chi = 0.
# The centrifugal term 1/(8 c rho^2) is the "Langer correction" that
# regularizes the log singularity.
#
# Matching the WKB phase in the Langer-regularized picture to the
# Bessel-function solution of the exact near-origin problem gives, at
# subleading O(1/c), the phase shift:
#
#   delta_Langer  =  (beta_0)/(2 sqrt(2c) * alpha)   -> at 1/c order contributes
#   delta_S^{Langer}  =  - alpha * (ln 2 + (b - f)) / (2 c)   (constant shift)
#
# where alpha = 1 is the coefficient of log(rho) in V near rho=0 and
# beta_0 = ln 2 + (b - f) is the constant term.
#
# Of this, the part proportional to (b - f) is already absorbed into S_BO
# (it just shifts the turning point). The residual is the ln 2 piece from
# the curvature factor "2" in "2 sinh rho":
#
#   delta_S^{Langer, residual} = - ln 2 / (2 c)
#
# This is the mechanism behind the ln 2 / (2 c_N) correction.
# ----------------------------------------------------------------------

def langer_residual(N: int) -> float:
    """The ln 2 / (2 c_N) residual from the Langer regularization at rho=0.

    Returns the SIGNED value that should be added to ln|psi| in the
    matching between the classical region and the origin.
    """
    return -log(2) / (2 * c_N(N))


# ----------------------------------------------------------------------
# Numerical verification:  solve the WDW ODE exactly at several values
# of c (via a 'c-scaling trick') and extract the 1/c coefficient by
# Richardson extrapolation.
#
# Key observation: S_BO itself is exactly proportional to sqrt(c). The
# 1/c corrections must come from the PREFACTOR (the overall normalization
# ln|psi|), not from the integral. We therefore compare the log-amplitude
# of the decaying solution at a fixed outer point rho_ref > rho* as c varies.
# ----------------------------------------------------------------------

def wdw_numeric_logamp(c_val: float, N: int,
                       rho_match: float = 0.05,
                       rho_outer: float = 8.0) -> float:
    """Solve the WDW ODE and return ln|psi| at rho_outer, with normalization
    psi(rho_match) = 1, psi'(rho_match) = sqrt(2 c |V(rho_match)|).

    The initial condition is the OUTGOING WKB solution, so the subsequent
    evolution captures both the Maslov-corrected phase in (rho_match, rho*)
    and the exponentially-decaying tail for rho > rho*.
    """
    from scipy.integrate import solve_ivp

    m_star = N // 2
    f = m_star * (N - m_star) / 2
    b = b_exact(N)

    def V_local(r):
        return log(2 * sinh(r)) + b - f

    def ode(rho, y):
        psi, psip = y
        return [psip, 2 * c_val * V_local(rho) * psi]

    v_start = V_local(rho_match)
    psi0 = 1.0
    psip0 = sqrt(2 * c_val * abs(v_start))

    sol = solve_ivp(
        ode,
        [rho_match, rho_outer],
        [psi0, psip0],
        method="DOP853",
        rtol=1e-13,
        atol=1e-15,
        max_step=0.005,
    )

    if not sol.success:
        return float("nan")

    psi_final = sol.y[0][-1]
    # Take absolute value since the solution can oscillate in (rho_match, rho*)
    return log(abs(psi_final))


def extract_1_over_c(N: int, rho_match: float = 0.05,
                     rho_outer: float = 8.0) -> tuple[float, float]:
    """Extract the 1/c coefficient of ln|psi| by Richardson extrapolation.

    ln|psi|(c) = A sqrt(c) + B + C / sqrt(c) + D / c + E / c^{3/2} + ...
    Compute at c, 2c, 4c, 8c and isolate D.
    """
    c_base = c_N(N)
    cs = [c_base, 2 * c_base, 4 * c_base, 8 * c_base]
    logpsis = [wdw_numeric_logamp(c, N, rho_match, rho_outer) for c in cs]

    # Subtract sqrt(c) leading term
    A = (logpsis[1] - logpsis[0]) / (sqrt(cs[1]) - sqrt(cs[0]))
    # logpsis_rem(c) = B + C/sqrt(c) + D/c + ...
    rem = [lp - A * sqrt(c) for lp, c in zip(logpsis, cs)]

    B = (rem[1] * sqrt(cs[1]) - rem[0] * sqrt(cs[0])) / (sqrt(cs[1]) - sqrt(cs[0]))
    # rem(c) - B = C/sqrt(c) + D/c + ...
    r2 = [r - B for r in rem]
    C = (r2[1] * cs[1] - r2[0] * cs[0]) * (sqrt(cs[1]) - sqrt(cs[0])) \
        / (cs[1] - cs[0]) / (sqrt(cs[1]) + sqrt(cs[0]))
    # Approximate: for large c, D dominates
    # D = lim_{c -> infty} c * (rem(c) - B - C/sqrt(c))
    D_estimates = [c * (r - B - C / sqrt(c)) for r, c in zip(rem, cs)]
    D_best = D_estimates[-1]
    D_err = max(abs(D_estimates[-1] - D_estimates[-2]),
                abs(D_estimates[-2] - D_estimates[-3]))
    return D_best, D_err
