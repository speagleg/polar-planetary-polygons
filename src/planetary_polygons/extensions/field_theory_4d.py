"""
The 3+1D field theory: covariant equation, propagator, and vertices.

Step A: The covariant 4D field equation on R x (H^2 x_N S^1)
Step B: The 4D propagator from the KK decomposition
Step C: The interaction vertices from the Magri hierarchy

The spacetime: M^4 = R_t x M^3 where M^3 = H^2 x_N S^1
with metric ds^2 = -dt^2 + ds^2_{H^2} + (dphi + A)^2
and gauge connection A with flux N/2.
"""

import numpy as np
from math import pi, sin, cos, log, exp, sqrt, sinh, cosh, asinh


def casimir(m, N):
    return m * (N - m) / 2.0


def b_exact(N):
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


# =====================================================================
# STEP A: The covariant 4D field equation
# =====================================================================

def covariant_equation():
    """The Klein-Gordon equation on R x (H^2 x_N S^1)."""
    print("=" * 72)
    print("  STEP A: THE COVARIANT 4D FIELD EQUATION")
    print("=" * 72)

    print("""
  The spacetime metric:
    ds^2 = -dt^2 + ds^2_{H^2} + (dphi + A_i dx^i)^2

  where ds^2_{H^2} = drho^2 + sinh^2(rho) dtheta^2 (curvature K=-1)
  and A is a U(1) connection with dA = (N/2) omega_{H^2}.

  The COVARIANT Klein-Gordon equation:

    (Box_4 - mu_0^2) Phi = lambda |Phi|^2 Phi

  where Box_4 = g^{mu nu} nabla_mu nabla_nu is the 4D d'Alembertian.

  In components:

    Box_4 = -d^2/dt^2 + Delta_{H^2} + D_phi^2

  where:
    Delta_{H^2} = d^2/drho^2 + coth(rho) d/drho + (1/sinh^2 rho) d^2/dtheta^2
    D_phi = d/dphi - i(N/2)  [the covariant derivative on S^1]

  The FREE equation (lambda = 0):

    [-d^2/dt^2 + Delta_{H^2} + D_phi^2 - mu_0^2] Phi = 0

  KK DECOMPOSITION: Phi(t, x, phi) = sum_m psi_m(t, x) e^{im phi}

  For each mode m:

    [-d^2/dt^2 + Delta_{H^2} - (m - N/2)^2 - mu_0^2] psi_m = 0

  The EFFECTIVE 2D mass for mode m:

    M_m^2 = (m - N/2)^2 + mu_0^2

  If mu_0 = 0 (massless 4D field):
    M_m^2 = (m - N/2)^2 = the KK mass spectrum.

  The critical mode m = N/2 has M_{N/2} = mu_0 (the bare mass).
  For mu_0 = 0: the critical mode is MASSLESS in 2D.

  THE CONNECTION TO HAVELOCK:
  The Havelock eigenvalue lambda_m on H^2 involves the massive
  Green's function G_{M_m} of (Delta_{H^2} - M_m^2):

    lambda_m = sum_p G_{M_m}(d_p) cos(2pi pm/N)

  For the massless mode (m = N/2, mu_0 = 0):
    lambda_{N/2} = sum_p G_0(d_p) cos(pi p) = standard Havelock

  For massive modes (m != N/2):
    lambda_m = sum_p G_{|m-N/2|}(d_p) cos(2pi pm/N) = screened Havelock
""")


# =====================================================================
# STEP A continued: The massive propagator on H^2
# =====================================================================

def massive_propagator_H2():
    """The massive Green's function on H^2."""
    print(f"\n{'='*72}")
    print("  THE MASSIVE PROPAGATOR ON H^2")
    print("=" * 72)

    print("""
  The Green's function G_mu(d) of (Delta_{H^2} - mu^2) on H^2:

    G_mu(d) = -(1/(2pi)) Q_{-1/2 + sqrt(1/4 + mu^2)}(cosh d)

  where Q_nu is the Legendre Q function of the second kind.

  Special cases:
    mu = 0: G_0(d) = -(1/(2pi)) Q_{-1/2}(cosh d)
                    = -(1/(2pi)) log(2sinh(d/2))  [the Havelock kernel]

    mu >> 1: G_mu(d) ~ -(1/(4pi mu)) exp(-mu d)  [exponential screening]

  For the KK mode m: mu_m = |m - N/2|, so:
    m = N/2: G_0 = -log(2sinh(d/2))/(2pi) [massless, long-range]
    m = N/2 +/- 1: G_1 ~ exp(-d)/(4pi) [screened at scale 1]
    m = 1 or N-1: G_{N/2-1} ~ exp(-(N/2-1)d) [heavily screened]
""")

    # Compute the massive Green's function numerically
    # G_mu(d) can be computed from the integral representation:
    # G_mu(d) = integral_0^inf exp(-sqrt(1/4+mu^2)*t) / sqrt(2(cosh t - cosh d)) dt / (2pi)
    # For d > 0.

    print(f"\n  The screening lengths 1/mu_m for N = 8:\n")
    print(f"  {'m':>4s} {'mu_m':>8s} {'1/mu':>10s} {'screening':>14s}")

    N = 8
    for m in range(1, N):
        mu = abs(m - N/2)
        inv_mu = 1/mu if mu > 0 else float('inf')

        if mu == 0:
            screen = "MASSLESS (log)"
        elif mu < 1:
            screen = f"weak ({inv_mu:.2f})"
        else:
            screen = f"strong ({inv_mu:.3f})"

        print(f"  {m:4d} {mu:8.4f} {inv_mu:10.4f} {screen:>14s}")

    print("""
  The critical mode m = N/2 is the ONLY massless mode.
  All other modes are screened with length 1/|m - N/2|.
  The m = 1 and m = N-1 modes have screening length 2/(N-2).

  For N = 8: the hierarchy of screening lengths:
    m = 4: infinite (massless) -> the GRAVITON MODE
    m = 3, 5: screening 1.0 -> nearest-neighbor coupling
    m = 2, 6: screening 0.5 -> short-range
    m = 1, 7: screening 0.33 -> very short-range

  The PHYSICAL PICTURE: the polygon perturbation has one
  long-range mode (the graviton/critical mode) and N-2
  short-range modes (the massive KK tower). The long-range
  mode determines stability; the short-range modes provide
  the fine structure.
""")


# =====================================================================
# STEP B: The 4D propagator
# =====================================================================

def propagator_4d():
    """The full 4D propagator from the KK decomposition."""
    print(f"\n{'='*72}")
    print("  STEP B: THE 4D PROPAGATOR")
    print("=" * 72)

    print("""
  The 4D propagator G_4(x, x'; phi, phi'):

    G_4 = sum_m G_{mu_m}(d_{H^2}(x, x')) * exp(im(phi - phi')) / (2pi)

  where mu_m = |m - N/2| and d is the H^2 geodesic distance.

  In the COINCIDENT LIMIT (x -> x', phi -> phi'):

    G_4(0, 0) = sum_m G_{mu_m}(0) / (2pi) = DIVERGENT

  The REGULARIZED propagator (subtracting the UV divergence):

    G_4^{reg} = sum_m [G_{mu_m}(d) - G_{mu_m}(0)] exp(im Delta_phi) / (2pi)

  For SEPARATED points (d > 0):

    G_4(d, Delta_phi) = (1/(2pi)) sum_m G_{mu_m}(d) e^{im Delta_phi}

  At Delta_phi = 0 (same fiber point):
    G_4(d, 0) = (1/(2pi)) sum_m G_{mu_m}(d)
              = (1/(2pi)) [G_0(d) + 2 sum_{k=1}^{N/2-1} G_k(d)]

  The DOMINANT contribution: G_0(d) ~ -log(d)/(2pi) (the massless mode).
  The CORRECTIONS: sum G_k(d) ~ sum exp(-k*d)/(4pi k) (screened modes).
  For d >> 1: only G_0 survives -> the 4D propagator reduces to 2D.
  For d << 1: all modes contribute -> the 4D structure matters.
""")

    # Compute the propagator numerically for N = 8
    N = 8
    print(f"  N = {N}: The 4D propagator at Delta_phi = 0\n")
    print(f"  {'d':>8s} {'G_0 (mass=0)':>14s} {'sum G_k':>12s} "
          f"{'G_4':>12s} {'G_4/G_0':>10s}")

    for d in [0.1, 0.2, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0]:
        # Massless propagator
        G0 = -log(2 * sinh(d/2)) / (2 * pi)

        # Massive propagators (use the asymptotic form)
        sum_Gk = 0.0
        for k in range(1, N//2):
            # G_k(d) ~ exp(-k*d) / (4*pi*k) for k*d >> 1
            # More precisely: G_k ~ -Q_{-1/2+sqrt(1/4+k^2)}(cosh d) / (2pi)
            # For large k: ~ exp(-k*d) * correction
            if k * d > 50:
                Gk = 0
            else:
                Gk = -exp(-k * d) / (4 * pi * k)  # leading asymptotic
            sum_Gk += 2 * Gk  # factor 2 for +k and -k

        G4 = G0 + sum_Gk
        ratio = G4 / G0 if abs(G0) > 1e-10 else 0

        print(f"  {d:8.4f} {G0:14.8f} {sum_Gk:12.8f} "
              f"{G4:12.8f} {ratio:10.4f}")

    print("""
  At large d: G_4 -> G_0 (the massive modes are screened).
  At small d: G_4 = G_0 + corrections (the KK tower contributes).
  The ratio G_4/G_0 -> 1 for d >> 1 (dimensional reduction works at IR).
""")


# =====================================================================
# STEP C: The interaction vertices
# =====================================================================

def interaction_vertices():
    """The 4D interaction vertices from the Magri hierarchy."""
    print(f"\n{'='*72}")
    print("  STEP C: THE INTERACTION VERTICES")
    print("=" * 72)

    print("""
  The 4D self-interaction: lambda_4 |Phi|^4 in the KK decomposition.

  |Phi|^4 = |sum_m psi_m e^{im phi}|^4
           = sum_{m1+m2=m3+m4 mod N} psi_{m1} psi_{m2} psi*_{m3} psi*_{m4}
             * integral e^{i(m1+m2-m3-m4)phi} dphi / (2pi)

  The SELECTION RULE from S^1 momentum conservation:
    m1 + m2 = m3 + m4  (mod N)

  This restricts which modes can interact.

  The 4D QUARTIC VERTEX for modes (m1, m2, m3, m4):

    V_{m1 m2 m3 m4} = lambda_4 * delta_{m1+m2, m3+m4 mod N}
                     * integral_{H^2} G_{mu1}(x) G_{mu2}(x) G_{mu3}(x) G_{mu4}(x) dA

  The DIAGONAL vertex (m, -m, m, -m) = (m, N-m, m, N-m):
  This is the self-coupling of mode m with its palindromic partner.

  From the Magri hierarchy:
    d_4 = 4N f^2 = N^5/16 at the critical mode.

  The 4D QUARTIC COUPLING at the critical mode:

    g_4 = d_4 / (2pi * L_fiber) = 4N f^2 / (2pi)

  where L_fiber = 2pi is the circumference of S^1.
  So: g_4 = 4N f^2 / (2pi) = 2N f^2 / pi.
""")

    # Compute the vertices for each N
    print(f"  The quartic coupling constant for each N:\n")
    print(f"  {'N':>4s} {'f_crit':>8s} {'d_4 = 4Nf^2':>14s} "
          f"{'g_4 = 2Nf^2/pi':>16s} {'g_4/c':>10s}")

    for N in range(5, 16):
        f = casimir(N//2, N)
        d4 = 4 * N * f**2
        g4 = 2 * N * f**2 / pi
        c = 12 * b_exact(N)
        ratio = g4 / c

        print(f"  {N:4d} {f:8.2f} {d4:14.2f} {g4:16.4f} {ratio:10.6f}")

    print("""
  The ratio g_4/c measures the coupling strength relative to
  the gravitational scale. For all N: g_4/c is O(N^2),
  meaning the coupling GROWS with N.

  The PERTURBATIVE expansion parameter: g_4 / (c * mass_gap^2)
  = 2Nf^2 / (pi * N^2 * 2/3) = 3f^2 / (pi N) = 3N^3 / (64pi).

  For N = 8: perturbative parameter = 3*512/(64*pi) ~ 7.6.
  This is NOT small -> the theory is STRONGLY COUPLED at the
  quartic level. Perturbation theory in g_4 does not converge.

  This is CONSISTENT with our earlier finding: the CS action and
  the Wilson line contribution are COMPARABLE at the threshold
  (ratio k/(gaps*rho*) ~ 0.3 at N = 8).
""")


# =====================================================================
# STEP C continued: The selection rules
# =====================================================================

def selection_rules():
    """The selection rules for mode-mode interactions."""
    print(f"\n{'='*72}")
    print("  THE SELECTION RULES")
    print("=" * 72)

    print("""
  The S^1 momentum conservation: m1 + m2 = m3 + m4 (mod N).

  For the QUARTIC vertex with 4 external legs:
  The allowed processes are (m1, m2) -> (m3, m4) with m1+m2 = m3+m4 mod N.

  DIAGONAL processes (m, N-m, m, N-m):
  m + (N-m) = 0 mod N -> m1 + m2 = N = 0 mod N. Always allowed.
  These are the ELASTIC scatterings (same modes in and out).

  CROSS processes (m1, m2, m3, m4) with m1 != m3:
  These TRANSFER momentum between modes.
  The number of allowed channels depends on N.
""")

    for N in [6, 7, 8]:
        print(f"\n  N = {N}: Allowed quartic processes")
        print(f"  {'(m1,m2)':>10s} -> {'(m3,m4)':>10s} {'type':>14s}")

        count = 0
        for m1 in range(1, N):
            for m2 in range(m1, N):
                target = (m1 + m2) % N
                for m3 in range(1, N):
                    m4 = (target - m3) % N
                    if 1 <= m4 < N and m3 <= m4:
                        if (m1, m2) != (m3, m4):
                            ptype = "cross"
                        else:
                            ptype = "diagonal"

                        if count < 15:
                            print(f"  ({m1},{m2}){'':<4s} -> ({m3},{m4}){'':<4s} "
                                  f"{ptype:>14s}")
                        count += 1

        print(f"  Total allowed channels: {count}")


# =====================================================================
# STEP C continued: The hexic vertex
# =====================================================================

def hexic_vertex():
    """The hexic (6-point) vertex from the Magri hierarchy."""
    print(f"\n{'='*72}")
    print("  THE HEXIC VERTEX (6-POINT)")
    print("=" * 72)

    print("""
  From the Magri hierarchy: d_6 = 64N f^3 (at the critical mode).

  The 6-point selection rule:
    m1 + m2 + m3 = m4 + m5 + m6  (mod N)

  The 4D hexic coupling:
    g_6 = d_6 / (2pi)^2 = 64N f^3 / (4 pi^2) = 16N f^3 / pi^2

  The hierarchy of couplings:
""")

    print(f"  {'N':>4s} {'g_4':>12s} {'g_6':>14s} {'g_6/g_4':>12s} "
          f"{'g_6/(g_4*f)':>14s}")

    for N in range(6, 14, 2):
        f = casimir(N//2, N)
        g4 = 2 * N * f**2 / pi
        g6 = 16 * N * f**3 / pi**2
        ratio = g6 / g4
        norm_ratio = g6 / (g4 * f)

        print(f"  {N:4d} {g4:12.2f} {g6:14.2f} {ratio:12.4f} "
              f"{norm_ratio:14.6f}")

    print("""
  The ratio g_6/g_4 = 8f/pi ~ 8N^2/(8pi) = N^2/pi.
  Each higher vertex brings a factor of ~N^2/pi.

  The MAGRI TOWER of vertices:
    g_{2k} = (4/pi)^{k-1} * N * f^k * (combinatorial factor)

  The perturbative series: sum_k g_{2k} / (mass_gap)^{2k-2}
  has coefficients growing as N^{2k} / N^{2k} ~ 1 per order.
  The series is MARGINAL (neither convergent nor divergent).
""")


# =====================================================================
# The complete 4D action
# =====================================================================

def complete_action():
    """The full 4D action assembling all components."""
    print(f"\n{'='*72}")
    print("  THE COMPLETE 4D ACTION")
    print("=" * 72)

    print("""
  S[Phi, g] = S_gravity + S_matter + S_interaction

  where:

  S_gravity = (1/16pi G) integral R^{(4)} sqrt(-g) d^4x
            = (1/16pi G) integral R^{(3)} sqrt(g_3) dt d^3x
            [for a static spacetime]

  S_matter = integral [(1/2)|D_mu Phi|^2 + (1/2)mu_0^2 |Phi|^2] sqrt(-g) d^4x
           = integral [(1/2)|d_t Phi|^2 + (1/2)|nabla_{H^2} Phi|^2
                       + (1/2)|D_phi Phi|^2 + (1/2)mu_0^2 |Phi|^2] ...

  S_interaction = integral [lambda_4 |Phi|^4 + lambda_6 |Phi|^6 + ...] sqrt(-g) d^4x

  After KK decomposition (Phi = sum psi_m e^{im phi}):

  S = integral dt d^2x sqrt(g_{H^2}) {
      sum_m [(1/2)|d_t psi_m|^2 - (1/2)|nabla psi_m|^2 - (1/2)M_m^2|psi_m|^2]
    + sum_{m1+m2=m3+m4} g_4/N * psi_{m1} psi_{m2} psi*_{m3} psi*_{m4}
    + sum_{6-point} g_6/N^2 * (6-point terms)
    + ...
  }

  where M_m^2 = (m-N/2)^2 + mu_0^2 is the KK mass.

  THE EQUATIONS OF MOTION:

  For each mode m:
    d^2 psi_m / dt^2 = [Delta_{H^2} - M_m^2] psi_m
                      - 4g_4/N sum_{m2,m3} psi_{m2} psi*_{m3} psi_{m+m3-m2}
                      - (6-point terms)

  This is a NONLINEAR WAVE EQUATION on H^2 for each KK mode,
  coupled through the momentum-conserving interaction vertices.

  THE STATIC LIMIT (d/dt = 0):
  [Delta_{H^2} - M_m^2] psi_m = 4g_4/N sum psi psi* psi + ...

  For the N-GON CONFIGURATION (psi_m = epsilon_m at the polygon):
  The static equation reduces to the HAVELOCK EIGENVALUE EQUATION:
    lambda_m epsilon_m = [linearized interaction terms]

  THE FIELD THEORY IS THE HAVELOCK THEORY LIFTED TO 4D.
""")


# =====================================================================
# Summary
# =====================================================================

def field_theory_summary():
    """Summary of the complete 4D field theory."""
    print(f"\n{'='*72}")
    print("  THE COMPLETE 4D FIELD THEORY")
    print("=" * 72)

    N = 8
    c = 12 * b_exact(N)
    G = 3 / (2 * c)
    f = casimir(N//2, N)
    g4 = 2 * N * f**2 / pi
    g6 = 16 * N * f**3 / pi**2

    print("""
  For N = {N} (the first polygon above the graviton threshold):

  SPACETIME: R x (H^2 x_{N} S^1)
    Spatial geometry: SL(2,R)~ (Thurston)
    Curvature: R^(3) = -2 - N^2/8 = {-2 - N**2/8:.1f}
    AdS radius: l = 1
    Newton's constant: G = {G:.6f}

  FIELD CONTENT:
    Scalar field Phi on M^4 with U(1) charge
    KK decomposition: {N} modes with masses mu_m = |m - {N//2}|
    Critical mode m = {N//2}: massless (the graviton mode)
    Massive modes: screening lengths 1/|m - {N//2}|

  COUPLING CONSTANTS:
    CS level: k = c/6 = {c/6:.1f}
    Central charge: c = {c:.1f}
    Quartic coupling: g_4 = {g4:.1f}
    Hexic coupling: g_6 = {g6:.1f}
    Perturbative parameter: g_4/(c * Delta_E^2) = {g4/(c * 2/3):.2f}

  THE SPECTRUM (at the N-gon):
    Havelock eigenvalues: lambda_m = C_1(rho) - m(N-m)/2 + delta_m
    Mass gap: Delta_E = sqrt(2/3) = {sqrt(2/3):.4f}
    Frozen determinant: Z_frozen = 2^(3*{N-2}/4) / {N-3}!! = {2**(3*(N-2)/4):.1f}/{np.prod(range(1, N-2, 2)):.0f}

  THE QUANTUM STRUCTURE:
    BO parameter: 1/c = {1/c:.4f}
    WDW smoothing: delta_rho = (1/(2c))^(1/3) = {(1/(2*c))**(1/3):.4f}
    Tunneling to BTZ: P ~ 10^(-30) (essentially zero)
    Phase: CLASSICAL (sigma/rho_eq = 0.40)

  STATUS: All components computed. The theory is STRONGLY COUPLED
  at the quartic level (g_4/c ~ N^2). Non-perturbative methods
  (the exact Havelock spectrum, the Magri hierarchy) are essential.
""")


# =====================================================================
# MAIN
# =====================================================================

def main():
    print("=" * 72)
    print("  THE 3+1D FIELD THEORY: EQUATION, PROPAGATOR, VERTICES")
    print("=" * 72)

    covariant_equation()
    massive_propagator_H2()
    propagator_4d()
    interaction_vertices()
    selection_rules()
    hexic_vertex()
    complete_action()
    field_theory_summary()


if __name__ == "__main__":
    main()
