"""
Born-Oppenheimer structure: the vortex-gravity quantum system.

SLOW variable: rho (the geodesic radius = gravitational d.o.f.)
FAST variables: epsilon_m (the Fourier modes = matter d.o.f.)

The FAST Schrodinger equation (at fixed rho):
    i d epsilon_m / dt = lambda_m(rho) epsilon_m

where lambda_m(rho) = C_1(rho) - f(m,N) + delta_m is the Havelock eigenvalue.

This is a COLLECTION OF HARMONIC OSCILLATORS with rho-dependent frequencies.
The quantum vortex Hamiltonian:
    H_fast = sum_m lambda_m(rho) * a_m^dag a_m

where a_m, a_m^dag are creation/annihilation operators for mode m.

The FAST energy levels (at fixed rho):
    E_fast(n_1,...,n_{N-1}; rho) = sum_m lambda_m(rho) * (n_m + 1/2)

The SLOW Schrodinger equation (the WDW equation):
    [-hbar^2/(2M) d^2/drho^2 + E_fast(n; rho)] Psi(rho) = E_total Psi(rho)

where M = c = N^2 and E_fast acts as the POTENTIAL for rho.

The WDW constraint: E_total = 0.

This is the Born-Oppenheimer approximation for quantum gravity:
- The vortex modes are the "electrons" (fast)
- The geodesic radius is the "nucleus" (slow)
- The Born-Oppenheimer potential is the total vortex energy
"""

import numpy as np
from math import pi, sin, cos, log, exp, sqrt, sinh, cosh


def casimir(m, N):
    return m * (N - m) / 2.0


def b_exact(N):
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


def lambda_m(rho, m, N):
    """Havelock eigenvalue at rho for mode m."""
    lam = 0.0
    for p in range(1, N):
        two_sinh = 2 * sinh(rho) * abs(sin(pi * p / N))
        lam += -log(two_sinh) * cos(2 * pi * p * m / N)
    return lam


def C1(rho, N):
    return log(2 * sinh(rho)) + b_exact(N)


# =====================================================================
# PART 1: The fast Schrodinger equation
# =====================================================================

def fast_schrodinger():
    """The quantum vortex system at fixed rho."""
    print("=" * 72)
    print("  THE FAST SCHRODINGER EQUATION")
    print("  Quantum vortex modes at fixed gravitational background")
    print("=" * 72)

    print("""
  The Hamiltonian for the vortex modes (at fixed rho):

    H_fast = sum_m lambda_m(rho) * (a_m^dag a_m + 1/2)

  This is a set of INDEPENDENT harmonic oscillators with
  rho-DEPENDENT frequencies lambda_m(rho).

  Energy levels: E(n_1,...,n_{N-1}; rho) = sum_m lambda_m(rho) (n_m + 1/2)

  The GROUND STATE (all n_m = 0):
    E_0(rho) = (1/2) sum_m lambda_m(rho) = the ZERO-POINT ENERGY

  The FIRST EXCITED STATE (n_{m*} = 1, all others 0):
    E_1(rho) = E_0(rho) + lambda_{m*}(rho) = ground state + one quantum

  The excitation energy: Delta E = lambda_{m*}(rho).
  This DEPENDS ON rho (the gravitational background).
""")

    N = 8
    print(f"  N = {N}: Vortex energy levels vs rho\n")
    print(f"  {'rho':>8s} {'E_0(zpe)':>12s} {'lambda_1':>10s} "
          f"{'lambda_4':>10s} {'E_0+lam4':>12s} {'all lam>0?':>10s}")

    for rho in np.linspace(0.5, 8, 16):
        eigenvalues = [lambda_m(rho, m, N) for m in range(1, N)]
        zpe = sum(eigenvalues) / 2
        lam1 = eigenvalues[0]
        lam4 = eigenvalues[3]  # critical mode
        all_positive = all(l > 0 for l in eigenvalues)

        print(f"  {rho:8.4f} {zpe:12.4f} {lam1:10.4f} "
              f"{lam4:10.4f} {zpe + lam4:12.4f} "
              f"{'yes' if all_positive else 'NO':>10s}")


# =====================================================================
# PART 2: The Born-Oppenheimer potential
# =====================================================================

def bo_potential():
    """The Born-Oppenheimer potential for the slow variable rho."""
    print(f"\n{'='*72}")
    print("  THE BORN-OPPENHEIMER POTENTIAL")
    print("=" * 72)

    print("""
  The BO potential V_BO(rho) = E_fast(n; rho) is the total
  vortex energy at the given occupation numbers {n_m}.

  For the GROUND STATE (all n_m = 0):
    V_BO^{(0)}(rho) = (1/2) sum_m lambda_m(rho)
                     = (1/2) [(N-1)*C_1(rho) - sum f(m)]
                     = (1/2) [(N-1)*C_1 - N(N^2-1)/12]

  This is a MONOTONICALLY INCREASING function of rho
  (since C_1 ~ rho for large rho).

  For the FIRST EXCITED STATE in the critical mode:
    V_BO^{(1)}(rho) = V_BO^{(0)} + lambda_{m*}(rho)

  The DIFFERENCE: lambda_{m*}(rho) = C_1(rho) - f(m*) + delta_{m*}
  This is the WDW potential we've been studying!
""")

    N = 8
    print(f"  N = {N}: The three BO potentials\n")
    print(f"  {'rho':>8s} {'V_ground':>12s} {'V_excited':>12s} "
          f"{'gap=lam_m*':>12s} {'V_2nd':>12s}")

    sum_f = sum(casimir(m, N) for m in range(1, N))
    m_crit = N // 2

    for rho in np.linspace(0.5, 10, 20):
        c1 = C1(rho, N)
        V_ground = 0.5 * ((N-1) * c1 - sum_f)

        lam_crit = lambda_m(rho, m_crit, N)
        V_excited = V_ground + lam_crit

        lam_next = lambda_m(rho, m_crit - 1, N)
        V_2nd = V_ground + lam_crit + lam_next

        print(f"  {rho:8.4f} {V_ground:12.4f} {V_excited:12.4f} "
              f"{lam_crit:12.4f} {V_2nd:12.4f}")


# =====================================================================
# PART 3: The adiabatic connection
# =====================================================================

def adiabatic_connection():
    """The Berry phase from the adiabatic evolution."""
    print(f"\n{'='*72}")
    print("  THE ADIABATIC CONNECTION (BERRY PHASE)")
    print("=" * 72)

    print("""
  As rho changes slowly, the vortex modes adjust adiabatically.
  The BERRY PHASE from this adjustment:

    gamma_m = -Im integral d rho <psi_m| d/d rho |psi_m>

  For harmonic oscillators with rho-dependent frequency:
    |psi_m> = (lambda_m)^{1/4} exp(-lambda_m epsilon_m^2 / 2) / sqrt(...)

  The Berry connection:
    A_m = <psi_m| d/d rho |psi_m> = (1/4) d(log lambda_m)/d rho

  The Berry phase over a closed path in rho:
    gamma_m = (1/4) oint d(log lambda_m) = 0 (for a closed path)

  So the BERRY PHASE IS ZERO for a closed path in rho.
  BUT: if rho passes through a LEVEL CROSSING (lambda_m = 0),
  the Berry phase picks up a pi/2 contribution.

  At the palindromic threshold (lambda_{m*} = 0):
    The Berry phase jumps by pi/2.
    This is the GEOMETRIC PHASE of the polygon-BTZ transition.
""")

    N = 8
    m_crit = N // 2

    print(f"  N = {N}: Berry connection A(rho) = (1/4) d log(lambda)/d rho\n")
    print(f"  {'rho':>8s} {'lambda_m*':>12s} {'d_lam/d_rho':>12s} "
          f"{'A = dlam/(4lam)':>16s}")

    eps = 0.001
    for rho in np.linspace(0.5, 8, 16):
        lam = lambda_m(rho, m_crit, N)
        lam_plus = lambda_m(rho + eps, m_crit, N)
        dlam = (lam_plus - lam) / eps

        if abs(lam) > 0.01:
            A = dlam / (4 * lam)
        else:
            A = float('inf')

        print(f"  {rho:8.4f} {lam:12.6f} {dlam:12.6f} "
              f"{A:16.6f}")


# =====================================================================
# PART 4: The non-adiabatic corrections
# =====================================================================

def non_adiabatic():
    """Non-adiabatic corrections: when the BO approximation fails."""
    print(f"\n{'='*72}")
    print("  NON-ADIABATIC CORRECTIONS")
    print("=" * 72)

    print("""
  The BO approximation fails when:
    hbar * |d lambda/d rho| / lambda^2 ~ 1

  i.e., when the rate of change of the frequency is comparable
  to the frequency squared (the adiabatic condition).

  d lambda_m / d rho = d C_1/d rho = coth(rho)
  lambda_m ~ C_1 - f(m)

  The non-adiabatic parameter:
    eta_m(rho) = |coth(rho)| / lambda_m(rho)^2

  When eta ~ 1: the vortex mode CANNOT follow the gravitational
  background adiabatically. Mode mixing and transitions occur.

  At the palindromic threshold (lambda -> 0): eta -> infinity.
  The BO approximation ALWAYS fails at the threshold.
  This is ANOTHER way to see that the palindromic transition
  is a fundamentally quantum (non-adiabatic) event.
""")

    N = 8
    m_crit = N // 2

    print(f"  N = {N}: Non-adiabatic parameter eta(rho)\n")
    print(f"  {'rho':>8s} {'lambda':>10s} {'coth':>10s} "
          f"{'eta':>12s} {'regime':>14s}")

    for rho in np.linspace(0.5, 8, 20):
        lam = lambda_m(rho, m_crit, N)
        coth = cosh(rho) / sinh(rho)
        eta = abs(coth) / lam**2 if abs(lam) > 0.01 else float('inf')

        if eta < 0.1:
            regime = "ADIABATIC"
        elif eta < 1:
            regime = "marginal"
        elif eta < 10:
            regime = "non-adiabatic"
        else:
            regime = "BREAKDOWN"

        print(f"  {rho:8.4f} {lam:10.4f} {coth:10.4f} "
              f"{eta:12.4f} {regime:>14s}")


# =====================================================================
# PART 5: The full Born-Oppenheimer Schrodinger system
# =====================================================================

def full_bo_system():
    """The complete two-level quantum system."""
    print(f"\n{'='*72}")
    print("  THE FULL BORN-OPPENHEIMER SYSTEM")
    print("=" * 72)

    print("""
  LEVEL 1 (FAST): The vortex Schrodinger equation

    i hbar d/dt |Psi_fast> = H_fast(rho) |Psi_fast>

    H_fast = sum_m lambda_m(rho) * a_m^dag a_m

    Spectrum: E_n(rho) = sum_m lambda_m(rho) * (n_m + 1/2)
    Eigenstates: |n_1, ..., n_{N-1}; rho>

    This is QUANTUM MECHANICS of the vortex modes.
    The gravitational field rho enters as an EXTERNAL PARAMETER.

  LEVEL 2 (SLOW): The gravitational Schrodinger equation

    [-hbar^2/(2c) d^2/drho^2 + E_n(rho)] chi(rho) = E_total chi(rho)

    The BO potential E_n(rho) is the vortex energy at occupation n.
    The mass M = c = N^2 is the central charge.
    The constraint E_total = 0 (the WDW equation).

    This is QUANTUM GRAVITY for the spatial geometry.
    The vortex energy acts as the MATTER SOURCE.

  THE COUPLED SYSTEM:

    |Psi_total> = sum_n chi_n(rho) |n; rho>

    The full Schrodinger equation:
    [H_gravity + H_fast + H_coupling] |Psi_total> = 0

    where H_coupling contains the non-adiabatic terms:
    H_coupling = -(hbar^2/2c) [2 <n|d/drho|n'> d/drho + <n|d^2/drho^2|n'>]
""")


# =====================================================================
# PART 6: The energy levels as quantum numbers
# =====================================================================

def quantum_numbers():
    """The complete set of quantum numbers for the vortex-gravity system."""
    print(f"\n{'='*72}")
    print("  THE QUANTUM NUMBERS")
    print("=" * 72)

    print("""
  The full quantum state is specified by:

  1. N (the polygon number): an INTEGER >= 3.
     This determines the NUMBER of modes and the Casimir spectrum.
     N is NOT a quantum number — it's a SUPERSELECTION SECTOR.

  2. {n_m} (the vortex occupation numbers): n_m = 0, 1, 2, ...
     for each mode m = 1, ..., N-1.
     These are the "matter" quantum numbers.

  3. k (the gravitational quantum number): k = 0, 1, 2, ...
     This labels the eigenstate of the slow (rho) equation.
     The ground state k = 0 has the wavefunction concentrated
     near rho_eq. Excited states k > 0 have nodes in rho.

  The total state: |N; n_1,...,n_{N-1}; k>

  The total energy:
    E_total = E_fast({n_m}; rho_k) + E_gravity(k)
            = sum_m lambda_m(rho_k) * (n_m + 1/2) + E_k^{grav}

  The WDW CONSTRAINT: E_total = 0.
  This FIXES one quantum number in terms of the others.

  For example: given N and {n_m}, the gravitational quantum number k
  is determined by E_total = 0:
    E_k^{grav} = -E_fast({n_m}; rho_k)

  Or: given N and k, the allowed occupation numbers {n_m} are
  constrained by E_total = 0.
""")

    N = 8
    m_crit = N // 2
    c = 12 * b_exact(N)

    print(f"  N = {N}: Energy levels in the ground BO potential\n")
    print(f"  The ground BO potential: V_0(rho) = (1/2) sum lambda_m(rho)")
    print(f"  The WDW equation: [-1/(2c) d^2/drho^2 + V_0(rho)] chi = 0\n")

    # Solve the slow equation with V = (1/2) sum lambda_m
    n_grid = 3000
    rho_min = 0.01
    rho_max = 15
    drho = (rho_max - rho_min) / n_grid
    rho_grid = np.linspace(rho_min, rho_max, n_grid)

    sum_f = sum(casimir(m, N) for m in range(1, N))

    V_ground = np.array([
        0.5 * ((N-1) * C1(r, N) - sum_f) if r > 0.001 else -50
        for r in rho_grid
    ])

    # Also the first excited BO potential
    V_excited = np.array([
        V_ground[i] + lambda_m(r, m_crit, N) if r > 0.001 else -50
        for i, r in enumerate(rho_grid)
    ])

    T_coeff = 1.0 / (2 * c * drho**2)

    # Ground BO surface
    H0 = np.diag(V_ground) + T_coeff * (2 * np.eye(n_grid)
        - np.eye(n_grid, k=1) - np.eye(n_grid, k=-1))
    evals_0 = np.linalg.eigvalsh(H0)[:5]

    # Excited BO surface
    H1 = np.diag(V_excited) + T_coeff * (2 * np.eye(n_grid)
        - np.eye(n_grid, k=1) - np.eye(n_grid, k=-1))
    evals_1 = np.linalg.eigvalsh(H1)[:5]

    print(f"  Ground BO surface (all n_m = 0):")
    print(f"  {'k':>4s} {'E_k^grav':>12s}")
    for k in range(5):
        print(f"  {k:4d} {evals_0[k]:12.6f}")

    print(f"\n  Excited BO surface (n_m* = 1):")
    print(f"  {'k':>4s} {'E_k^grav':>12s} {'gap to ground':>14s}")
    for k in range(5):
        gap = evals_1[k] - evals_0[k]
        print(f"  {k:4d} {evals_1[k]:12.6f} {gap:14.6f}")

    # The BO gap: difference between ground and excited surfaces
    print(f"\n  The BO gap at each rho:")
    print(f"  {'rho':>8s} {'V_ground':>12s} {'V_excited':>12s} "
          f"{'gap=lam_m*':>12s}")

    for rho in [0.5, 1.0, 2.0, 3.0, 5.0]:
        vg = 0.5 * ((N-1) * C1(rho, N) - sum_f)
        ve = vg + lambda_m(rho, m_crit, N)
        gap = ve - vg
        print(f"  {rho:8.4f} {vg:12.4f} {ve:12.4f} {gap:12.4f}")


# =====================================================================
# PART 7: The molecular analogy
# =====================================================================

def molecular_analogy():
    """The analogy between the vortex-gravity system and molecules."""
    print(f"\n{'='*72}")
    print("  THE MOLECULAR ANALOGY")
    print("=" * 72)

    print("""
  The Born-Oppenheimer structure maps EXACTLY onto molecular physics:

  MOLECULE                    |  VORTEX-GRAVITY SYSTEM
  ============================|================================
  Nuclei (slow, heavy)        |  rho (the geometry, mass c = N^2)
  Electrons (fast, light)     |  epsilon_m (the vortex modes)
  Nuclear position R          |  Geodesic radius rho
  Electronic Hamiltonian H(R) |  Havelock Hamiltonian H(rho)
  Electronic energy E_n(R)    |  Vortex energy sum lambda_m(rho)
  BO surface E_n(R)           |  The BO potential V_n(rho)
  Vibrational states          |  Gravitational quantum number k
  Rotational states           |  The Z_N symmetry quantum number m
  Bond breaking (R -> inf)    |  Polygon-BTZ transition (rho -> rho*)
  Ionization energy           |  The mass gap sqrt(2/3)
  Berry phase                 |  Geometric phase at the threshold
  Conical intersection        |  Palindromic eigenvalue crossing

  The CONICAL INTERSECTION analogy:
  At the palindromic threshold, the critical eigenvalue lambda_{m*} = 0.
  This is where two BO surfaces TOUCH (the ground and excited).
  In molecular physics, this is a "conical intersection" where
  the BO approximation fails and non-adiabatic transitions occur.

  The TUNNELING analogy:
  The molecule can tunnel through a potential barrier (e.g., NH3).
  The polygon can tunnel through the palindromic threshold (BO barrier).
  We showed: the tunneling probability is 10^{-16} at N = 7.
  This is like a molecule with an extremely high barrier.

  The KEY DIFFERENCE:
  In molecules: the nuclear mass M is physical (proton mass ~1836 m_e).
  In our system: the "nuclear mass" M = c = N^2 is the CENTRAL CHARGE.
  The Born-Oppenheimer parameter: m_e/M = 1/c = 1/N^2.
  For N = 7: m_e/M = 1/49 ~ 0.02 (comparable to hydrogen!).
  For N = 3: m_e/M = 1/9 ~ 0.11 (like a muonic atom).
""")

    print(f"  The BO parameter 1/c = 1/N^2 for each N:\n")
    print(f"  {'N':>4s} {'c':>8s} {'1/c':>10s} {'molecular analog':>25s}")

    analogs = {
        3: "muonic hydrogen (1/9)",
        4: "positronium (1/16)",
        5: "helium (1/25)",
        6: "lithium (1/36)",
        7: "hydrogen (1/49)",
        8: "deuterium (1/64)",
        10: "neon-like (1/100)",
        12: "magnesium-like (1/144)",
    }

    for N in range(3, 16):
        c = 12 * b_exact(N)
        analog = analogs.get(N, "")
        print(f"  {N:4d} {c:8.1f} {1/c:10.6f} {analog:>25s}")

    print(f"""
  N = 7 (the graviton threshold) has 1/c ~ 0.02, which is
  close to the electron-proton mass ratio in hydrogen (1/1836 ~ 0.0005).

  The BO approximation works BETTER for larger N (smaller 1/c).
  For N <= 5: 1/c > 0.04 and the BO corrections are significant.
  For N >= 10: 1/c < 0.01 and the BO approximation is excellent.

  This is consistent with our earlier finding:
  - N <= 7: semiclassical (sigma/rho_eq < 0.5)
  - N > 7: quantum (sigma/rho_eq > 0.5)
  The BO parameter 1/c = 1/N^2 controls BOTH transitions.
""")


# =====================================================================
# MAIN
# =====================================================================

def main():
    print("=" * 72)
    print("  THE BORN-OPPENHEIMER STRUCTURE")
    print("  Vortex (fast) + Gravity (slow) = Quantum Polygon")
    print("=" * 72)

    fast_schrodinger()
    bo_potential()
    adiabatic_connection()
    non_adiabatic()
    full_bo_system()
    quantum_numbers()
    molecular_analogy()

    print(f"\n{'='*72}")
    print("  SUMMARY")
    print("=" * 72)
    print("""
  The quantum polygon system has a Born-Oppenheimer structure:

  1. FAST (vortex modes): Schrodinger equation at fixed rho.
     H_fast = sum lambda_m(rho) a_m^dag a_m
     Spectrum: harmonic oscillator with rho-dependent frequencies.

  2. SLOW (geometry): WDW equation with vortex energy as potential.
     [-hbar^2/(2c) d^2/drho^2 + E_fast(rho)] chi = 0
     Mass M = c = N^2 (the central charge).

  3. COUPLING: Non-adiabatic terms from the Berry connection.
     The Berry phase is zero for closed paths but jumps by pi/2
     at the palindromic threshold (the "conical intersection").

  4. QUANTUM NUMBERS: |N; n_1,...,n_{N-1}; k>
     N = polygon sector (superselection)
     {n_m} = vortex occupation numbers (matter)
     k = gravitational quantum number (geometry)
     The WDW constraint fixes one in terms of the others.

  5. The BO parameter 1/c = 1/N^2 controls the quality of the
     approximation: good for N > 7, breaks down for N <= 5.

  THE MOLECULAR ANALOGY is exact:
  rho = nuclear coordinate, epsilon_m = electronic d.o.f.,
  lambda_m(rho) = electronic energy surface, c = nuclear mass.
  The palindromic threshold IS a conical intersection.
  The mass gap sqrt(2/3) IS the ionization energy.
""")


if __name__ == "__main__":
    main()
