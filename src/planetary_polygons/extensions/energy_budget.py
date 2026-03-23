"""
Energy budget at the palindromic threshold: vacuum, frozen, and matter.

At the threshold rho*(N), the energy decomposes into:
1. VACUUM energy: from the mode-averaged C_1 (the cosmological constant)
2. FROZEN energy: from the non-critical modes (dark matter candidate)
3. CRITICAL mode: lambda_{m*} = 0 (the horizon, zero energy)
4. BARYONIC: the self-energy of the vortices (the physical matter)

The question: does the ratio frozen/vacuum match any known fraction?
"""

import numpy as np
from math import pi, sin, cos, log, exp, sqrt, sinh


def casimir(m, N):
    return m * (N - m) / 2.0


def b_exact(N):
    return N * (N + 1) / 12 - log(2) + log(N) / (N - 1)


def havelock_eigenvalue(m, N, rho):
    lam = 0.0
    for p in range(1, N):
        two_sinh = 2 * sinh(rho) * abs(sin(pi * p / N))
        lam += -log(two_sinh) * cos(2 * pi * p * m / N)
    return lam


def find_threshold(N, m_crit=None):
    if m_crit is None:
        m_crit = N // 2
    f_crit = casimir(m_crit, N)
    b = b_exact(N)
    target = f_crit - b
    if target > 0:
        return np.arcsinh(exp(target) / 2)
    return 0.01


def energy_budget_at_threshold(N):
    """Compute the full energy budget at the palindromic threshold.

    At rho = rho*(N):
    - lambda_{m*} = 0 (the critical mode)
    - lambda_m = C_1 - f(m) + delta_m for m != m* (frozen modes)

    The energy budget:
    E_total = sum_m lambda_m = (N-1)*C_1 - sum f(m) + sum delta_m
            = (N-1)*C_1 - N(N^2-1)/12 + 0  [traceless delta]

    The VACUUM contribution: C_1 per mode, summed over N-1 modes
    E_vacuum = (N-1) * C_1

    The CASIMIR (matter) contribution: -sum f(m)
    E_casimir = -N(N^2-1)/12

    The WEYL (anomaly) contribution: sum delta_m = 0 (traceless)

    The individual frozen mode energies:
    lambda_m = f(m*) - f(m) + (delta_m - delta_{m*})
    """
    m_crit = N // 2
    rho_star = find_threshold(N, m_crit)
    f_crit = casimir(m_crit, N)

    # Compute all eigenvalues at the threshold
    eigenvalues = []
    casimirs_list = []
    for m in range(1, N):
        lam = havelock_eigenvalue(m, N, rho_star)
        eigenvalues.append(lam)
        casimirs_list.append(casimir(m, N))

    eigenvalues = np.array(eigenvalues)
    casimirs_arr = np.array(casimirs_list)

    # C_1 at the threshold
    C1 = np.mean(eigenvalues + casimirs_arr)

    # The three-layer decomposition at threshold
    deltas = eigenvalues - C1 + casimirs_arr

    # Energy components
    E_total = np.sum(eigenvalues)
    E_vacuum_per_mode = C1  # this is what each mode "sees" as the background
    E_vacuum_total = (N - 1) * C1
    E_casimir_total = -np.sum(casimirs_arr)
    E_weyl_total = np.sum(deltas)  # should be ~0 (traceless)

    # The frozen mode energies (excluding the critical mode)
    frozen_eigenvalues = []
    frozen_casimir_gaps = []
    frozen_weyl_corrections = []

    delta_crit = deltas[m_crit - 1]

    for m in range(1, N):
        if m == m_crit:
            continue
        lam = eigenvalues[m - 1]
        cas_gap = f_crit - casimir(m, N)
        weyl_corr = deltas[m - 1] - delta_crit

        frozen_eigenvalues.append(lam)
        frozen_casimir_gaps.append(cas_gap)
        frozen_weyl_corrections.append(weyl_corr)

    E_frozen = sum(frozen_eigenvalues)
    E_frozen_casimir = sum(frozen_casimir_gaps)
    E_frozen_weyl = sum(frozen_weyl_corrections)

    return {
        'N': N,
        'rho_star': rho_star,
        'C1': C1,
        'f_crit': f_crit,
        'E_total': E_total,
        'E_vacuum': E_vacuum_total,
        'E_casimir': E_casimir_total,
        'E_weyl': E_weyl_total,
        'E_frozen': E_frozen,
        'E_frozen_casimir': E_frozen_casimir,
        'E_frozen_weyl': E_frozen_weyl,
        'eigenvalues': eigenvalues,
        'deltas': deltas,
        'frozen_evals': frozen_eigenvalues,
        'frozen_gaps': frozen_casimir_gaps,
    }


def main():
    print("=" * 72)
    print("  ENERGY BUDGET AT THE PALINDROMIC THRESHOLD")
    print("=" * 72)

    # Part 1: The full budget for each N
    print(f"\n{'='*72}")
    print("  PART 1: Energy decomposition at the threshold")
    print("=" * 72)

    print(f"\n  {'N':>4s} {'C₁':>8s} {'E_total':>10s} {'E_vacuum':>10s} "
          f"{'E_Casimir':>10s} {'E_frozen':>10s} {'E_weyl':>10s}")

    for N in range(5, 18):
        b = energy_budget_at_threshold(N)
        print(f"  {N:4d} {b['C1']:8.3f} {b['E_total']:10.3f} "
              f"{b['E_vacuum']:10.3f} {b['E_casimir']:10.3f} "
              f"{b['E_frozen']:10.3f} {b['E_weyl']:10.2e}")

    # Part 2: The fractions
    print(f"\n{'='*72}")
    print("  PART 2: Energy fractions at the threshold")
    print("=" * 72)

    print(f"\n  At the threshold, the critical mode has E = 0.")
    print(f"  The frozen modes carry ALL the energy.")
    print(f"  How does this decompose into Casimir vs Weyl?")

    print(f"\n  {'N':>4s} {'E_frozen':>10s} {'E_Cas_gap':>10s} "
          f"{'E_Weyl':>10s} {'%Casimir':>10s} {'%Weyl':>10s}")

    for N in range(5, 18):
        b = energy_budget_at_threshold(N)

        E_fr = b['E_frozen']
        E_cg = b['E_frozen_casimir']
        E_wl = b['E_frozen_weyl']

        pct_cas = E_cg / E_fr * 100 if abs(E_fr) > 1e-10 else 0
        pct_wl = E_wl / E_fr * 100 if abs(E_fr) > 1e-10 else 0

        print(f"  {N:4d} {E_fr:10.4f} {E_cg:10.4f} "
              f"{E_wl:10.4f} {pct_cas:10.2f} {pct_wl:10.2f}")

    # Part 3: Ratios to vacuum energy
    print(f"\n{'='*72}")
    print("  PART 3: Ratios relative to vacuum energy b(N)")
    print("=" * 72)

    print(f"\n  b(N) = N(N+1)/12 - log2 + logN/(N-1)  [the vacuum energy]")
    print(f"\n  {'N':>4s} {'b(N)':>10s} {'E_frozen':>10s} "
          f"{'E_fr/b':>10s} {'f_crit':>10s} {'Σ gaps':>10s} "
          f"{'gaps/b':>10s}")

    for N in range(5, 18):
        b_N = b_exact(N)
        budget = energy_budget_at_threshold(N)
        E_fr = budget['E_frozen']
        f_crit = budget['f_crit']
        sum_gaps = budget['E_frozen_casimir']

        print(f"  {N:4d} {b_N:10.4f} {E_fr:10.4f} "
              f"{E_fr / b_N:10.4f} {f_crit:10.4f} {sum_gaps:10.4f} "
              f"{sum_gaps / b_N:10.4f}")

    # Part 4: The Casimir gap sum (analytical)
    print(f"\n{'='*72}")
    print("  PART 4: Analytical Casimir gap sum")
    print("=" * 72)

    print(f"""
  For even N at the critical mode m* = N/2:
  The Casimir gap: f(m*) - f(m) = (N-2m)²/8

  Sum of all frozen gaps:
  Σ_{{m≠m*}} (N-2m)²/8 = (2/8) Σ_{{k=1}}^{{N/2-1}} (2k)² [by palindromic sym, doubled]
                        = (1/4) · 2 · Σ_{{k=1}}^{{N/2-1}} (2k)²
                        = Σ_{{k=1}}^{{N/2-1}} k²
                        = (N/2-1)(N/2)(N-1)/6

  For large N: ~ N³/48
""")

    print(f"  {'N':>4s} {'Σ gaps (num)':>14s} {'(N/2-1)(N/2)(N-1)/6':>22s} "
          f"{'match':>8s} {'ratio to b':>10s}")

    for N in range(6, 20, 2):
        budget = energy_budget_at_threshold(N)
        sum_gaps_num = budget['E_frozen_casimir']

        # Analytical formula
        sum_gaps_ana = (N/2 - 1) * (N/2) * (N - 1) / 6
        b_N = b_exact(N)

        match = abs(sum_gaps_num - sum_gaps_ana) < 0.01 * abs(sum_gaps_ana)

        print(f"  {N:4d} {sum_gaps_num:14.4f} {sum_gaps_ana:22.4f} "
              f"{'YES' if match else 'no':>8s} {sum_gaps_num / b_N:10.4f}")

    # Part 5: The critical ratio
    print(f"\n{'='*72}")
    print("  PART 5: The frozen/vacuum ratio and its N-dependence")
    print("=" * 72)

    print(f"""
  The ratio R(N) = E_frozen / E_vacuum = Σ gaps / b(N)

  Σ gaps ~ N³/48 (for large N)
  b(N) ~ N²/12

  So R(N) ~ (N³/48) / (N²/12) = N/4 (grows linearly!)

  The ratio is NOT a fixed number — it depends on N.
  There is no single N that gives R = 0.40 (the dark matter ratio).

  But the ratio of INDIVIDUAL components might be more meaningful:
""")

    print(f"  {'N':>4s} {'R=E_fr/b':>10s} {'N/4':>8s} "
          f"{'E_fr/(N-1)':>12s} {'b/(N-1)':>10s} {'per-mode R':>12s}")

    for N in range(5, 20):
        budget = energy_budget_at_threshold(N)
        b_N = b_exact(N)
        E_fr = budget['E_frozen']
        R = E_fr / b_N
        per_mode_fr = E_fr / (N - 2)  # N-2 frozen modes
        per_mode_b = b_N  # b is already per-mode-averaged

        print(f"  {N:4d} {R:10.4f} {N/4:8.4f} "
              f"{per_mode_fr:12.4f} {per_mode_b:10.4f} "
              f"{per_mode_fr / per_mode_b:12.6f}")

    # Part 6: Different decomposition
    print(f"\n{'='*72}")
    print("  PART 6: Alternative decomposition")
    print("=" * 72)

    print(f"""
  Instead of frozen/vacuum, consider the THREE-COMPONENT split:

  E_total = E_critical + E_frozen + E_baryonic
  where:
    E_critical = lambda_{{m*}} = 0 at threshold (the "dark energy" = Λ)
    E_frozen = Σ_{{m≠m*}} lambda_m (the "dark matter")
    E_baryonic = the vortex self-energy (the "visible matter")

  The vortex self-energy:
  E_self = N * h(0) = N * (-log(2*sinh(0))) = N * infinity (divergent!)
  Regularized: E_self ~ N * log(1/a) where a is the vortex core size.

  The RATIO that matters physically:
  Ω_Λ = 0 at threshold (Λ = 0 by construction)
  Ω_frozen / Ω_baryonic = E_frozen / E_self

  At the threshold:
  E_frozen = Σ gaps ~ N³/48
  E_self ~ N * log(1/a)

  Ratio: Ω_frozen/Ω_baryonic ~ N²/(48 log(1/a))

  For this to equal the observed 27/5 ≈ 5.4:
  N²/(48 * log(1/a)) = 5.4
  log(1/a) = N²/259

  For N = 7: log(1/a) = 49/259 ≈ 0.19, so a ≈ 0.83
  For N = 8: log(1/a) = 64/259 ≈ 0.25, so a ≈ 0.78
""")

    # The ε-dependent split
    print(f"  The full energy budget at the threshold for N = 8:\n")
    N = 8
    budget = energy_budget_at_threshold(N)

    print(f"  Component        | Energy     | Fraction (of frozen)")
    print(f"  -----------------+------------+---------------------")

    for i, m in enumerate(range(1, N)):
        if m == N // 2:
            label = f"  m={m} (CRITICAL)"
            energy = budget['eigenvalues'][m-1]
        else:
            label = f"  m={m} (frozen)"
            energy = budget['eigenvalues'][m-1]
        frac = energy / budget['E_frozen'] if abs(budget['E_frozen']) > 1e-10 else 0
        gap = budget['frozen_gaps'][i] if i < len(budget['frozen_gaps']) else 0
        print(f"  {label:16s}  | {energy:10.4f} | {frac:10.4f}  gap={(N-2*m)**2/8:.2f}")

    print(f"\n  Total frozen: {budget['E_frozen']:.4f}")
    print(f"  C₁ at threshold: {budget['C1']:.4f}")
    print(f"  f(m*) = {budget['f_crit']:.4f}")

    # Part 7: What actually sets the ratio
    print(f"\n{'='*72}")
    print("  PART 7: What the ratio actually depends on")
    print("=" * 72)

    print(f"""
  The frozen/vacuum ratio R(N) = [Σ (N-2m)²/8] / b(N)

  For even N:
    Σ gaps = (N/2-1)(N/2)(N-1)/6  [exact]
    b(N) = N(N+1)/12 - log2 + logN/(N-1)  [exact]

  The ratio:
    R(N) = (N/2-1)(N/2)(N-1)/6  /  [N(N+1)/12 - log2 + logN/(N-1)]
         ~ [N³/48] / [N²/12]  for large N
         = N/4

  The ratio grows LINEARLY with N. This means:
    - For N = 3 (triangle): R = 0 (no frozen modes, anomaly-free)
    - For N = 4 (square): R ~ 1
    - For N = 8 (octagon): R ~ 2
    - For N = 20: R ~ 5

  NO value of N gives R = 0.40 (the observed dark matter fraction).

  HOWEVER: if the relevant ratio is not frozen/vacuum but
  frozen/TOTAL where TOTAL includes the baryonic self-energy,
  then the ratio depends on the UV cutoff a (vortex core size).

  The ONE free parameter in the theory — the vortex core size a —
  could in principle be tuned to match the observed ratio.
  But that's fine-tuning, not a prediction.

  CONCLUSION: The framework gives a STRUCTURAL explanation for
  "dark-matter-like" energy (frozen modes at the threshold) but
  NOT a quantitative prediction for its fraction of the total
  energy budget. The ratio depends on N (the polygon type) and
  a (the UV cutoff), neither of which is fixed by the framework.
""")


if __name__ == "__main__":
    main()
