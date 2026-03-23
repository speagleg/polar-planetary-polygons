"""
Step D: Making the gauge field dynamical.

The U(1) connection A on S^1 with flux N/2 has been a FIXED background.
Promoting A to a dynamical field gives Kaluza-Klein electrodynamics
on the Seifert manifold.

The question: when A fluctuates, what happens to the KK spectrum,
the Casimir, and the three-layer decomposition?

The gauge field has two components:
1. A_phi: the flux (the zero mode of A on S^1) -> sets N/2
2. A_i: the H^2 components (the vector potential on the base)

The FLUX N/2 is QUANTIZED (by the Dirac condition). It cannot
fluctuate continuously — it can only change by integers.
So the flux is TOPOLOGICAL: N is fixed within each sector.

But A_i (the base components) CAN fluctuate. These fluctuations
are the KK GAUGE BOSONS: massless or massive vector fields on H^2.
"""

import numpy as np
from math import pi, sin, cos, log, exp, sqrt, sinh


def casimir(m, N):
    return m * (N - m) / 2.0


def b_exact(N):
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


# =====================================================================
# PART 1: The gauge field spectrum
# =====================================================================

def gauge_field_spectrum():
    """The KK spectrum of the gauge field on S^1."""
    print("=" * 72)
    print("  STEP D: THE DYNAMICAL GAUGE FIELD")
    print("=" * 72)

    print("""
  The U(1) gauge field A on S^1 decomposes into KK modes:
    A_mu(x, phi) = sum_n a_mu^{(n)}(x) e^{in phi}

  The ZERO MODE n = 0: a_mu^{(0)} is a massless vector on H^2.
  This is the 2D PHOTON — the gauge field inherited from 4D.

  The MASSIVE modes n != 0: a_mu^{(n)} has mass |n| from the S^1.
  These are the KK gauge bosons.

  But there's a SUBTLETY: the background flux N/2 modifies the
  gauge field KK decomposition. The covariant derivative on A is:

    D_phi A_mu = (d/dphi - i*N/2) A_mu  [in the adjoint representation]

  Wait: for a U(1) gauge field, the adjoint representation is trivial
  (the photon doesn't carry charge). So the flux does NOT affect
  the gauge field KK spectrum.

  The gauge field KK masses:
    M_n^{gauge} = |n|  (not shifted by N/2, unlike the charged scalar)

  The CHARGED SCALAR has M_m = |m - N/2| (shifted by the flux).
  The GAUGE FIELD has M_n = |n| (unshifted).

  This ASYMMETRY between matter and gauge KK spectra is physical:
  the matter "feels" the flux, the gauge field doesn't.
""")

    N = 8
    print(f"  N = {N}: KK spectra comparison\n")
    print(f"  {'mode':>6s} {'scalar M_m':>12s} {'gauge M_n':>12s} "
          f"{'scalar-gauge':>14s}")

    for m in range(N):
        M_scalar = abs(m - N/2)
        M_gauge = abs(m)  # unshifted for gauge
        diff = M_scalar - M_gauge
        print(f"  {m:6d} {M_scalar:12.4f} {M_gauge:12.4f} {diff:+14.4f}")


# =====================================================================
# PART 2: The Maxwell action on the Seifert manifold
# =====================================================================

def maxwell_action():
    """The Maxwell action for the dynamical gauge field."""
    print(f"\n{'='*72}")
    print("  THE MAXWELL ACTION ON THE SEIFERT MANIFOLD")
    print("=" * 72)

    print("""
  The 4D Maxwell action:

    S_Maxwell = -(1/4g^2) integral F_{mu nu} F^{mu nu} sqrt(-g) d^4x

  where F = dA is the field strength and g is the gauge coupling.

  On R x (H^2 x_N S^1):
    F has components F_{ti}, F_{t phi}, F_{ij}, F_{i phi}

  The BACKGROUND: A = (N/2) dphi -> F_background = (N/2) omega_{H^2}
  The FLUCTUATION: A -> A + delta_A

  The Maxwell equation for the fluctuation:
    d * F = J  (the source current from the charged scalar)

  The CURRENT from the KK scalar:
    J_mu = sum_m [psi_m^* D_mu psi_m - psi_m (D_mu psi_m)^*]
         = sum_m (2m - N) |psi_m|^2 * delta_{mu, phi} + gradient terms

  The phi-component of J is proportional to (2m - N):
  the MODE NUMBER relative to the flux center.

  The critical mode m = N/2 has J_phi = 0: it doesn't couple to the
  gauge field. This is because the critical mode has ZERO effective
  charge (it's at the flux center).

  The modes m != N/2 have NONZERO J_phi ~ (2m - N) |psi_m|^2:
  they source the gauge field fluctuations.
""")


# =====================================================================
# PART 3: The gauge coupling
# =====================================================================

def gauge_coupling():
    """Determine the gauge coupling from the framework."""
    print(f"\n{'='*72}")
    print("  THE GAUGE COUPLING")
    print("=" * 72)

    print("""
  In standard Kaluza-Klein: the 4D gauge coupling is determined by
  the radius of the compact dimension:

    1/g^2 = L_fiber / (16 pi G)

  where L_fiber = 2pi (the circumference of S^1) and G = 3/(2c).

  So: 1/g^2 = 2pi / (16 pi * 3/(2c)) = c/24 = N^2/24 + O(N)

  The gauge coupling: g^2 = 24/c = 24/N^2 + O(1/N^3)

  For N = 8: g^2 = 24/67.2 = 0.357, g = 0.597.
  For N = 7: g^2 = 24/51.6 = 0.465, g = 0.682.

  The FINE STRUCTURE CONSTANT:
    alpha_gauge = g^2/(4pi) = 6/(pi c) = 6/(pi N^2) + O(1/N^3)

  For N = 7: alpha = 6/(pi * 49) = 0.039 ~ 1/26.
  For N = 8: alpha = 6/(pi * 64) = 0.030 ~ 1/34.
  For N = 12: alpha = 6/(pi * 144) = 0.013 ~ 1/75.
""")

    print(f"  {'N':>4s} {'c':>8s} {'g^2=24/c':>10s} {'g':>8s} "
          f"{'alpha=g^2/4pi':>14s} {'1/alpha':>10s}")

    for N in range(5, 20):
        c = 12 * b_exact(N)
        g_sq = 24 / c
        g = sqrt(g_sq)
        alpha = g_sq / (4 * pi)
        inv_alpha = 1 / alpha

        print(f"  {N:4d} {c:8.1f} {g_sq:10.6f} {g:8.4f} "
              f"{alpha:14.6f} {inv_alpha:10.2f}")

    print(f"""
  The fine structure constant alpha = 6/(pi N^2) DECREASES with N.
  For N = 7 (the graviton threshold): alpha ~ 1/26.
  This is NOT the QED value 1/137, but it's the same ORDER OF MAGNITUDE.

  The RUNNING: alpha depends on N, which is a DISCRETE parameter.
  There is no continuous running — the coupling jumps between
  the discrete N sectors.

  The coupling HIERARCHY:
    N = 4: alpha = 0.093 ~ 1/11 (strong coupling)
    N = 7: alpha = 0.039 ~ 1/26 (moderate)
    N = 12: alpha = 0.013 ~ 1/75 (weak)
    N = 20: alpha = 0.005 ~ 1/211 (very weak)
""")


# =====================================================================
# PART 4: The gauge-matter coupling
# =====================================================================

def gauge_matter_coupling():
    """The coupling between the dynamical gauge field and the scalar."""
    print(f"\n{'='*72}")
    print("  THE GAUGE-MATTER COUPLING")
    print("=" * 72)

    print("""
  The covariant derivative of the scalar:
    D_mu Phi = (nabla_mu - i A_mu) Phi

  The gauge field fluctuation delta_A couples to the scalar through:
    L_coupling = delta_A_mu * J^mu
               = delta_A_i * J^i + delta_A_phi * J^phi

  The CURRENT at the N-gon (from the KK modes):
    J^phi = sum_m (2m - N) |psi_m|^2 / (2pi)  [the charge current]
    J^i = sum_m [psi_m^* nabla_i psi_m - c.c.] / (2pi)  [the gradient current]

  For the STATIC polygon (all psi_m at the N-gon equilibrium):
    J^phi = sum_m (2m - N) |epsilon_m|^2 / (2pi)

  At UNIT amplitude (|epsilon_m| = 1 for all m):
    J^phi = sum_{m=1}^{N-1} (2m - N) / (2pi) = 0 (by symmetry!)

  The total charge current VANISHES for the symmetric polygon.
  The gauge field is NOT sourced by the equilibrium configuration.

  HOWEVER: for ASYMMETRIC perturbations (|epsilon_m| != |epsilon_{N-m}|):
    J^phi != 0 and the gauge field IS sourced.
  The gauge field fluctuation is EXCITED by palindromic ASYMMETRY.
""")

    N = 8
    print(f"  N = {N}: Mode charges (2m - N) and their coupling\n")
    print(f"  {'m':>4s} {'charge 2m-N':>14s} {'|charge|':>10s} {'m paired with':>14s}")

    for m in range(1, N):
        charge = 2 * m - N
        partner = N - m
        print(f"  {m:4d} {charge:+14d} {abs(charge):10d} {partner:14d}")

    print(f"\n  Sum of charges: {sum(2*m - N for m in range(1, N))}")
    print(f"  The total charge is ZERO (charge neutrality of the polygon).")


# =====================================================================
# PART 5: The flux as a topological quantum number
# =====================================================================

def flux_topology():
    """The flux N/2 as a topological quantum number."""
    print(f"\n{'='*72}")
    print("  THE FLUX AS A TOPOLOGICAL QUANTUM NUMBER")
    print("=" * 72)

    print("""
  The magnetic flux Phi_B = N/2 is QUANTIZED:
  - Dirac condition: Phi_B = integer (for even N) or half-integer (odd N)
  - The flux CANNOT change continuously — it jumps by 1.
  - Changing N -> N+1 costs a FLUX QUANTUM.

  The ENERGY COST of changing the flux by 1:
    Delta_E_flux = E(N+1) - E(N) = b(N+1) - b(N) + ...

  Since b(N) ~ N^2/12: Delta_E ~ (2N+1)/12 ~ N/6.

  For N = 8: Delta_E_flux ~ 8/6 ~ 1.33 (in natural units).
  Compare with the mass gap sqrt(2/3) ~ 0.82.
  The flux change costs MORE than the mass gap.

  This means: flux changes are SUPPRESSED relative to mode excitations.
  The polygon prefers to excite vortex modes (energy gap sqrt(2/3))
  rather than change its polygon number N (energy gap N/6).

  The TOPOLOGICAL STABILITY of N:
  N is protected by the flux quantization.
  Changing N requires a topological transition (creating or
  annihilating a magnetic flux quantum), which is non-perturbative.
  This is why N is a SUPERSELECTION SECTOR in the quantum theory.
""")

    print(f"  The energy cost of changing N:\n")
    print(f"  {'N':>4s} {'b(N)':>10s} {'b(N+1)':>10s} {'Delta b':>10s} "
          f"{'N/6':>8s} {'Delta/gap':>10s}")

    for N in range(5, 15):
        b1 = b_exact(N)
        b2 = b_exact(N + 1)
        delta = b2 - b1
        n6 = N / 6
        gap = sqrt(2/3)
        ratio = delta / gap

        print(f"  {N:4d} {b1:10.4f} {b2:10.4f} {delta:10.4f} "
              f"{n6:8.4f} {ratio:10.4f}")


# =====================================================================
# PART 6: The full dynamical gauge theory
# =====================================================================

def full_gauge_theory():
    """The complete gauge theory on the Seifert manifold."""
    print(f"\n{'='*72}")
    print("  THE COMPLETE GAUGE THEORY")
    print("=" * 72)

    print("""
  The full 4D action with dynamical gauge field:

  S = S_gravity + S_Maxwell + S_matter + S_interaction

  S_gravity = (1/16pi G) integral R^{(4)} sqrt(-g) d^4x
  S_Maxwell = -(1/4g^2) integral F_{mu nu} F^{mu nu} sqrt(-g) d^4x
  S_matter = integral |D_mu Phi|^2 sqrt(-g) d^4x
  S_interaction = integral [lambda_4 |Phi|^4 + ...] sqrt(-g) d^4x

  The GAUGE COUPLING: g^2 = 24/c = 24/N^2
  The FINE STRUCTURE: alpha = 6/(pi N^2)

  The FIELD CONTENT:
  1. Gravity: the Seifert metric (non-dynamical in the static limit;
     dynamical through the WDW equation for rho)
  2. Gauge field: U(1) on S^1 with flux N/2 (topological sector)
     + fluctuations (the KK photon + massive gauge bosons)
  3. Scalar: charged scalar Phi with N KK modes
  4. Interactions: quartic, hexic, ... from the Magri hierarchy

  THE TOPOLOGICAL STRUCTURE:
  - N is a SUPERSELECTION SECTOR (protected by flux quantization)
  - Within each N sector: the gauge field fluctuates around A = (N/2)dphi
  - The scalar KK spectrum is SHIFTED by the flux: M_m = |m - N/2|
  - The gauge KK spectrum is UNSHIFTED: M_n = |n|
  - The critical scalar mode (m = N/2) is massless but NEUTRAL
  - The gauge field sees only the ASYMMETRIC perturbations

  THE GAUGE HIERARCHY:
  alpha = 6/(pi N^2) naturally gives a WEAK coupling for large N.
  The hierarchy between the gauge coupling (alpha ~ 1/N^2) and the
  gravitational coupling (G ~ 1/N^2) is:
    alpha / (8pi G) = 6/(pi N^2) / (8pi * 3/(2N^2)) = 6/(12pi^2) = 1/(2pi^2)

  This ratio is a UNIVERSAL CONSTANT: alpha/(8pi G) = 1/(2pi^2) ~ 0.05,
  independent of N!
""")

    print(f"  The universal ratio alpha/(8pi G):\n")
    print(f"  {'N':>4s} {'alpha':>10s} {'8pi G':>10s} {'ratio':>10s} "
          f"{'1/(2pi^2)':>10s}")

    for N in range(5, 16):
        c = 12 * b_exact(N)
        alpha = 6 / (pi * c / 12)  # alpha = 6/(pi N^2) approximately
        # More precisely: alpha = g^2/(4pi) = (24/c)/(4pi) = 6/(pi c)
        alpha_exact = 6 / (pi * c)
        G = 3 / (2 * c)
        eight_pi_G = 8 * pi * G
        ratio = alpha_exact / eight_pi_G
        target = 1 / (2 * pi**2)

        print(f"  {N:4d} {alpha_exact:10.6f} {eight_pi_G:10.6f} "
              f"{ratio:10.6f} {target:10.6f}")

    print(f"""
  The ratio alpha/(8pi G) = 1/(2pi^2) = {1/(2*pi**2):.8f} is EXACT
  (it follows algebraically from alpha = 6/(pi c) and G = 3/(2c)).

  This is the GAUGE-GRAVITY UNIFICATION ratio: the electromagnetic
  and gravitational couplings are locked together by the Kaluza-Klein
  geometry, with the universal ratio 1/(2pi^2).
""")


# =====================================================================
# MAIN
# =====================================================================

def main():
    print("=" * 72)
    print("  STEP D: THE DYNAMICAL GAUGE FIELD")
    print("  Kaluza-Klein electrodynamics on the Seifert manifold")
    print("=" * 72)

    gauge_field_spectrum()
    maxwell_action()
    gauge_coupling()
    gauge_matter_coupling()
    flux_topology()
    full_gauge_theory()

    print(f"\n{'='*72}")
    print("  SUMMARY")
    print("=" * 72)
    print(f"""
  The dynamical gauge field on the Seifert manifold gives:

  1. GAUGE COUPLING: alpha = 6/(pi c) = 6/(pi N^2) + O(1/N^3).
     Naturally weak for large N. At N = 7: alpha ~ 1/26.

  2. FLUX QUANTIZATION: N is a topological quantum number.
     Changing N costs energy ~N/6 (larger than the mass gap).
     N is a superselection sector.

  3. GAUGE-GRAVITY RATIO: alpha/(8pi G) = 1/(2pi^2) EXACTLY.
     This is a universal constant, independent of N.
     The gauge and gravitational couplings are LOCKED.

  4. CHARGE NEUTRALITY: the symmetric polygon has zero total
     charge current. The gauge field is sourced only by
     palindromic-ASYMMETRIC perturbations.

  5. The critical mode (m = N/2) is NEUTRAL: it doesn't couple
     to the gauge field. The graviton mode is uncharged.
""")


if __name__ == "__main__":
    main()
