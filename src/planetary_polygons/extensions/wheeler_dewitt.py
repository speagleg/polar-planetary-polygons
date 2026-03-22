"""
Wheeler-DeWitt equation for the vortex-gravity minisuperspace.

The single degree of freedom: rho (geodesic radius of the polygon).
The potential: V(rho) = lambda_{m*}(rho) = C_1(rho) - f(m*) + delta_{m*}
The mass: M = c = N^2 (the central charge = the Planck mass in 2D).

The WDW equation:
    [-hbar^2/(2M) * d^2/drho^2 + V(rho)] * Psi(rho) = 0

At the palindromic threshold rho*: V(rho*) = 0.
    - rho > rho*: V > 0, classically ALLOWED (exterior, oscillatory Psi)
    - rho < rho*: V < 0, classically FORBIDDEN (interior, evanescent Psi)

Near the threshold: V ~ alpha*(rho - rho*) where alpha = coth(rho*).
Solution: AIRY FUNCTION Psi ~ Ai(z) with z = (2M*alpha/hbar^2)^{1/3}(rho-rho*)

The three-layer decomposition IS the WDW potential decomposition:
    V(rho) = C_1(rho)    - f(m)     + delta_m
           = [cosmological] [matter]   [anomaly]
           = [gravity term] [QM term]  [1-loop correction]
"""

import numpy as np
from math import pi, sin, cos, log, sinh, cosh, tanh, sqrt, exp, gamma
try:
    from scipy.special import airy as scipy_airy
    from scipy.integrate import solve_ivp, quad
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False
    # Airy function approximation for Ai(z)
    def scipy_airy(z):
        """Minimal Airy function approximation."""
        if z > 2:
            # Asymptotic: Ai(z) ~ exp(-2/3 z^{3/2}) / (2*sqrt(pi)*z^{1/4})
            val = exp(-2/3 * z**1.5) / (2 * sqrt(pi) * z**0.25)
            return val, 0, 0, 0
        elif z < -2:
            # Oscillatory: Ai(z) ~ sin(2/3 |z|^{3/2} + pi/4) / (sqrt(pi)*|z|^{1/4})
            val = sin(2/3 * abs(z)**1.5 + pi/4) / (sqrt(pi) * abs(z)**0.25)
            return val, 0, 0, 0
        else:
            # Taylor series near z=0: Ai(0) = 1/(3^{2/3} Gamma(2/3))
            ai0 = 1 / (3**(2/3) * gamma(2/3))
            aip0 = -1 / (3**(1/3) * gamma(1/3))
            val = ai0 + aip0 * z + ai0 * z**3 / 6
            return val, aip0, 0, 0

    def quad(f, a, b, **kwargs):
        """Simple trapezoidal integration."""
        n = 1000
        x = np.linspace(a, b, n)
        y = np.array([f(xi) for xi in x])
        return np.trapz(y, x), 0


def casimir(m, N):
    return m * (N - m) / 2.0


def b_exact(N):
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


def C1(rho, N):
    """C_1(rho) = log(2sinh(rho)) + b(N)."""
    return log(2 * sinh(rho)) + b_exact(N)


def lambda_m(rho, m, N):
    """Havelock eigenvalue = the WDW potential for mode m."""
    return C1(rho, N) - casimir(m, N)  # ignoring delta_m at leading order


def find_threshold(N, m_crit=None):
    """Find rho* where lambda_{m*} = 0."""
    if m_crit is None:
        m_crit = N // 2
    f_crit = casimir(m_crit, N)
    b = b_exact(N)
    target = f_crit - b
    if target > 0:
        return np.arcsinh(exp(target) / 2)
    return 0.01


# =====================================================================
# PART 1: The WDW potential
# =====================================================================

def wdw_potential(rho, N, m_crit=None):
    """The Wheeler-DeWitt potential V(rho) = lambda_{m*}(rho).

    V > 0 for rho > rho* (exterior, classically allowed)
    V < 0 for rho < rho* (interior, classically forbidden)
    V = 0 at rho = rho* (the horizon / turning point)
    """
    if m_crit is None:
        m_crit = N // 2
    return lambda_m(rho, m_crit, N)


def plot_potential(N):
    """Display the WDW potential structure."""
    m_crit = N // 2
    rho_star = find_threshold(N, m_crit)
    f_crit = casimir(m_crit, N)

    print(f"\n  N = {N}, m* = {m_crit}, f* = {f_crit:.2f}, rho* = {rho_star:.4f}")
    print(f"  {'rho':>8s} {'V(rho)':>12s} {'region':>12s} {'WKB phase':>20s}")

    for rho in np.linspace(max(0.1, rho_star - 3), rho_star + 5, 20):
        V = wdw_potential(rho, N, m_crit)
        if V > 0.01:
            region = "exterior"
            phase = f"oscillatory (k={sqrt(V):.3f})"
        elif V < -0.01:
            region = "interior"
            phase = f"evanescent (kappa={sqrt(-V):.3f})"
        else:
            region = "HORIZON"
            phase = "Airy transition"
        print(f"  {rho:8.4f} {V:12.6f} {region:>12s} {phase:>20s}")


# =====================================================================
# PART 2: The Airy function solution near the threshold
# =====================================================================

def airy_solution(N, hbar=1.0, m_crit=None):
    """Solve the WDW equation near the palindromic threshold.

    Near rho*: V(rho) ~ alpha * (rho - rho*)
    where alpha = coth(rho*) ~ 1 for large rho*.

    The WDW equation: -hbar^2/(2M) Psi'' + alpha*(rho-rho*) Psi = 0

    Substitution: z = (2M*alpha/hbar^2)^{1/3} * (rho - rho*)
    gives: Psi''(z) = z * Psi(z)  [the Airy equation]

    Solution: Psi(z) = A * Ai(z) + B * Bi(z)

    Physical boundary condition:
    - Psi -> 0 as rho -> -infinity (deep interior: exponential decay)
    - This selects Ai(z) (the decaying Airy function)
    """
    if m_crit is None:
        m_crit = N // 2

    M = N**2  # the Planck mass = central charge
    rho_star = find_threshold(N, m_crit)
    alpha = 1.0 / tanh(rho_star) if rho_star > 0.01 else 100.0

    # The Airy scaling parameter
    a_scale = (2 * M * alpha / hbar**2)**(1.0/3)

    # The quantum smoothing width
    delta_rho = 1.0 / a_scale  # width of the Airy transition region

    print(f"\n  N = {N}, M = c = {M}, hbar = {hbar}")
    print(f"  rho* = {rho_star:.6f}, alpha = coth(rho*) = {alpha:.6f}")
    print(f"  Airy scale: a = (2M*alpha/hbar^2)^(1/3) = {a_scale:.6f}")
    print(f"  Quantum smoothing width: delta_rho = 1/a = {delta_rho:.6f}")
    print(f"  Classical threshold: sharp at rho = {rho_star:.6f}")
    print(f"  Quantum threshold: smeared over [{rho_star - delta_rho:.4f}, "
          f"{rho_star + delta_rho:.4f}]")

    # Evaluate the Airy function
    print(f"\n  {'rho':>8s} {'z':>10s} {'Ai(z)':>14s} {'|Psi|^2':>14s} "
          f"{'V(rho)':>12s}")

    rho_values = np.linspace(rho_star - 3*delta_rho, rho_star + 5*delta_rho, 20)
    for rho in rho_values:
        if rho <= 0.01:
            continue
        z = a_scale * (rho - rho_star)
        ai, aip, bi, bip = scipy_airy(z)
        psi_sq = ai**2  # |Psi|^2 for the Ai solution
        V = wdw_potential(rho, N, m_crit)

        print(f"  {rho:8.4f} {z:10.4f} {ai:14.8f} {psi_sq:14.8e} {V:12.6f}")

    return rho_star, alpha, a_scale, delta_rho


# =====================================================================
# PART 3: The WKB approximation
# =====================================================================

def wkb_phase(N, rho, m_crit=None, M=None):
    """WKB phase integral S(rho) = integral_{rho*}^{rho} sqrt(2M*V) drho'.

    For rho > rho* (exterior): S is real -> oscillatory Psi ~ sin(S/hbar)
    For rho < rho* (interior): S is imaginary -> evanescent Psi ~ exp(-|S|/hbar)
    """
    if m_crit is None:
        m_crit = N // 2
    if M is None:
        M = N**2

    rho_star = find_threshold(N, m_crit)

    if rho > rho_star:
        # Exterior: real phase
        def integrand(r):
            V = wdw_potential(r, N, m_crit)
            return sqrt(max(0, 2 * M * V))

        S, _ = quad(integrand, rho_star + 1e-6, rho)
        return S, "oscillatory"
    else:
        # Interior: imaginary phase (tunneling)
        def integrand(r):
            V = wdw_potential(r, N, m_crit)
            return sqrt(max(0, -2 * M * V))

        S, _ = quad(integrand, max(0.01, rho), rho_star - 1e-6)
        return S, "evanescent"


def wkb_analysis(N):
    """Full WKB analysis of the WDW equation."""
    m_crit = N // 2
    M = N**2
    rho_star = find_threshold(N, m_crit)

    print(f"\n  N = {N}, M = {M}, rho* = {rho_star:.4f}")

    # Exterior phases (oscillatory region)
    print(f"\n  EXTERIOR (rho > rho*): oscillatory WKB")
    print(f"  {'rho':>8s} {'V(rho)':>10s} {'S(rho)':>12s} {'k_local':>10s}")

    for delta in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
        rho = rho_star + delta
        V = wdw_potential(rho, N, m_crit)
        S, phase_type = wkb_phase(N, rho, m_crit, M)
        k_local = sqrt(2 * M * V) if V > 0 else 0
        print(f"  {rho:8.4f} {V:10.4f} {S:12.4f} {k_local:10.4f}")

    # Interior phases (tunneling region)
    print(f"\n  INTERIOR (rho < rho*): evanescent WKB (tunneling)")
    print(f"  {'rho':>8s} {'V(rho)':>10s} {'|S|(tunnel)':>12s} {'kappa':>10s}")

    for delta in [0.1, 0.5, 1.0, 2.0]:
        rho = max(0.01, rho_star - delta)
        V = wdw_potential(rho, N, m_crit)
        S, phase_type = wkb_phase(N, rho, m_crit, M)
        kappa = sqrt(-2 * M * V) if V < 0 else 0
        print(f"  {rho:8.4f} {V:10.4f} {S:12.4f} {kappa:10.4f}")


# =====================================================================
# PART 4: The tunneling amplitude
# =====================================================================

def tunneling_amplitude(N):
    """Compute the tunneling amplitude through the palindromic threshold.

    P_tunnel ~ exp(-2 * |S_tunnel| / hbar)

    where S_tunnel = integral_0^{rho*} sqrt(-2M*V) drho
    is the WKB action in the forbidden (interior) region.

    This should relate to the frozen determinant Z_frozen.
    """
    m_crit = N // 2
    M = N**2
    hbar = 1.0
    rho_star = find_threshold(N, m_crit)

    # Tunneling action from rho_min to rho*
    rho_min = max(0.1, rho_star - 10)

    def integrand(r):
        V = wdw_potential(r, N, m_crit)
        return sqrt(max(0, -2 * M * V))

    S_tunnel, _ = quad(integrand, rho_min, rho_star - 1e-6)

    P_tunnel = exp(-2 * S_tunnel / hbar) if S_tunnel < 500 else 0

    # Compare with the frozen determinant
    # Z_frozen = prod_{m != m*} |lambda_m(rho*)|^{-1/2}
    log_Z_frozen = 0
    for m in range(1, N):
        if m == m_crit:
            continue
        lam = lambda_m(rho_star, m, N)
        if abs(lam) > 1e-12:
            log_Z_frozen += -0.5 * log(abs(lam))

    return rho_star, S_tunnel, P_tunnel, log_Z_frozen


# =====================================================================
# PART 5: The identification M = c = N^2
# =====================================================================

def mass_identification():
    """Show that M = N^2 (the central charge) is the natural Planck mass.

    The quantum smoothing width delta_rho = (hbar^2/(2M*alpha))^{1/3}
    should scale as N^{-2/3} for M = N^2.

    At large N: alpha = coth(rho*) -> 1, so delta_rho ~ N^{-2/3}.

    This means the classical palindromic thresholds become SHARP
    in the large-N (= large-c) limit, consistent with the c -> infinity
    being the classical limit of the orbifold CFT.
    """
    print(f"\n  {'N':>4s} {'M=N^2':>8s} {'rho*':>10s} {'alpha':>10s} "
          f"{'delta_rho':>12s} {'N^(-2/3)':>10s} {'ratio':>10s}")

    for N in range(4, 21):
        M = N**2
        rho_star = find_threshold(N, N // 2)
        alpha = 1.0 / tanh(rho_star) if rho_star > 0.01 else 100.0
        delta_rho = (1.0 / (2 * M * alpha))**(1.0/3)
        n_23 = N**(-2.0/3)
        ratio = delta_rho / n_23

        print(f"  {N:4d} {M:8d} {rho_star:10.4f} {alpha:10.6f} "
              f"{delta_rho:12.6f} {n_23:10.6f} {ratio:10.6f}")


# =====================================================================
# PART 6: The bridge equation
# =====================================================================

def bridge_equation():
    """The complete QM-GR bridge through the WDW equation."""
    print("""
  ═══════════════════════════════════════════════════════════════
  THE QM-GR BRIDGE EQUATION
  ═══════════════════════════════════════════════════════════════

  The Wheeler-DeWitt equation for the vortex-gravity system:

      [-ℏ²/(2c) · d²/dρ² + λ_{m*}(ρ)] Ψ(ρ) = 0

  where:
    c = N² is the central charge (= Planck mass in 2D units)
    λ_{m*}(ρ) = C₁(ρ) - f(m*) + δ_{m*} is the Havelock eigenvalue

  Substituting the three-layer decomposition:

      [-ℏ²/(2c) · d²/dρ²  +  log(2sinh ρ) + b(N)  -  m(N-m)/2  +  δ_m] Ψ = 0
       \_________________/    \________________/    \__________/   \____/
        Quantum kinetic         GR: the H²          QM: twist      1-loop
        (gravity dyn.)          Green's function     field dim.     anomaly

  INTERPRETATION:
    - The kinetic term ℏ²/(2c) · Ψ'' is GRAVITY (the dynamics of ρ)
    - The potential log(2sinh ρ) is the CLASSICAL GRAVITATIONAL FIELD
    - The Casimir m(N-m)/2 is the QUANTUM MECHANICAL energy (matter)
    - The Weyl anomaly δ_m is the ONE-LOOP CORRECTION

  The equation UNIFIES QM and GR:
    GRAVITY provides the kinetic energy and the potential (through C₁)
    QM provides the matter content (through the Casimir and anomaly)
    The WDW constraint H = 0 binds them together

  THE CLASSICAL LIMIT (c → ∞):
    ℏ²/(2c) → 0, so the kinetic term vanishes.
    The equation reduces to: V(ρ) Ψ = 0
    → either Ψ = 0 (no universe) or V = 0 (classical threshold)
    The classical threshold λ_{m*}(ρ*) = 0 IS the Einstein equation
    for the vortex-gravity system.

  THE QUANTUM REGIME (finite c = N²):
    The Airy function smooths the classical threshold over a width
    δρ ~ (ℏ²/(2c))^{1/3} ~ N^{-2/3}
    → Quantum gravity effects at the horizon scale N^{-2/3}
    → The palindromic threshold becomes FUZZY

  THE SEMICLASSICAL (WKB) REGIME:
    Ψ ~ exp(±i S(ρ)/ℏ) where S = ∫ √(2c · V) dρ
    EXTERIOR (V > 0): S real → oscillatory → vortex oscillations
    INTERIOR (V < 0): S imaginary → evanescent → tunneling
    The connection at V = 0: Airy function → UNIVERSAL ν = 1/2

  THE SINH/COSH DISTINCTION:
    In the WKB approximation:
    Exterior: √V ~ √(log(2sinh ρ) + b - f) ← involves sinh
    Interior: √|V| ~ √(f - log(2sinh ρ) - b)
    At the horizon: V = 0, and the Airy function interpolates.

    The Lorentzian continuation ρ → ρ + iπ/2 maps:
    sinh(ρ) → i·cosh(ρ)  (exterior → interior)
    This IS the WKB connection formula through the turning point.

  THE FROZEN DETERMINANT:
    Z_frozen = ∏_{m≠m*} |λ_m(ρ*)|^{-1/2}

    In the WDW framework: this is the PREFACTOR of the WKB
    wavefunction at the turning point. The frozen modes provide
    the measure on the space of quantum states at the horizon.

  THE COMPLETE PARTITION FUNCTION:
    Z(ρ) = |Ψ(ρ)|² · Z_frozen(N)
         = |Ai((2c)^{1/3}(ρ-ρ*))|² · 2^{3(N-2)/4}/(N-3)!!

  This is the PROBABILITY of finding the polygon at geodesic
  radius ρ, given the quantum gravity wavefunction.
""")


# =====================================================================
# MAIN
# =====================================================================

def main():
    print("█" * 72)
    print("  WHEELER-DEWITT EQUATION FOR THE VORTEX-GRAVITY SYSTEM")
    print("  The dynamics of ρ from first principles")
    print("█" * 72)

    bridge_equation()

    # Part 1: The potential
    print(f"\n{'='*72}")
    print("  THE WDW POTENTIAL V(ρ) = λ_{m*}(ρ)")
    print("=" * 72)

    for N in [8, 12]:
        plot_potential(N)

    # Part 2: Airy solution
    print(f"\n{'='*72}")
    print("  AIRY FUNCTION NEAR THE THRESHOLD")
    print("=" * 72)

    for N in [8, 12]:
        airy_solution(N, hbar=1.0)

    # Part 3: WKB
    print(f"\n{'='*72}")
    print("  WKB APPROXIMATION")
    print("=" * 72)

    for N in [8, 12]:
        wkb_analysis(N)

    # Part 4: Tunneling
    print(f"\n{'='*72}")
    print("  TUNNELING AMPLITUDE")
    print("=" * 72)

    print(f"\n  {'N':>4s} {'rho*':>10s} {'S_tunnel':>12s} {'P_tunnel':>14s} "
          f"{'log Z_frozen':>14s} {'S/logZ':>10s}")

    for N in range(6, 18, 2):
        rho_star, S, P, logZ = tunneling_amplitude(N)
        ratio = S / abs(logZ) if abs(logZ) > 1e-10 else float('nan')
        print(f"  {N:4d} {rho_star:10.4f} {S:12.4f} {P:14.6e} "
              f"{logZ:14.6f} {ratio:10.4f}")

    # Part 5: Mass identification
    print(f"\n{'='*72}")
    print("  PLANCK MASS IDENTIFICATION: M = c = N²")
    print("=" * 72)

    mass_identification()

    # Summary
    print(f"\n{'='*72}")
    print("  THE UNIFIED PICTURE")
    print("=" * 72)

    print("""
  The Wheeler-DeWitt equation

      [-ℏ²/(2N²) d²/dρ² + log(2sinh ρ) + b(N) - m(N-m)/2 + δ_m] Ψ = 0

  UNIFIES the entire framework:

  ┌─────────────────────────────────────────────────────────────┐
  │  COMPONENT          │  ORIGIN      │  ROLE IN WDW          │
  ├─────────────────────┼──────────────┼───────────────────────┤
  │  ℏ²/(2N²) d²/dρ²   │  QG kinetic  │  Gravity dynamics     │
  │  log(2sinh ρ)       │  H² Green fn │  Classical potential   │
  │  b(N) = N²/12+...   │  Orbifold    │  Vacuum energy c/12   │
  │  m(N-m)/2           │  Casimir     │  Matter (twist field)  │
  │  δ_m                │  Weyl        │  1-loop anomaly        │
  ├─────────────────────┼──────────────┼───────────────────────┤
  │  Airy at threshold  │  QG horizon  │  Quantum smoothing     │
  │  WKB exterior       │  BTZ outside │  Vortex oscillations   │
  │  WKB interior       │  BTZ inside  │  Spatial growth/tunnel │
  │  sinh ↔ cosh        │  Kruskal     │  Exterior ↔ Interior   │
  │  Z_frozen           │  1-loop det  │  WKB prefactor         │
  │  ν = 1/2            │  Airy        │  Universal exponent    │
  └─────────────────────┴──────────────┴───────────────────────┘

  The classical limit c → ∞:  sharp threshold at ρ*
  The quantum correction:     Airy smoothing over δρ ~ N^{-2/3}
  The semiclassical regime:   WKB with sinh(exterior)/cosh(interior)
  The tunneling amplitude:    related to Z_frozen (the 1-loop det)
""")


if __name__ == "__main__":
    main()
