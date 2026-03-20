"""
Topological protection of the Morse index μ(N).

The genuine content of the index theorem for vortex polygons is NOT
computing μ(N) (which is trivial eigenvalue counting), but proving
that μ(N) is ROBUST: it cannot change under continuous perturbations
that couple Fourier modes, as long as the boundary data is preserved.

Theorem (Topological protection):
    Let V(ξ) be any continuous family of symmetric (N-1)×(N-1) matrices
    on [0,1) with V(0) = 0 and V(ξ) → 0 as ξ → 1⁻.  Then

        SF(H_N + V, 0 → 1) = SF(H_N, 0 → 1) = μ(N),

    where H_N(ξ) = C₁(ξ)·I - F_N is the diagonal Havelock family.

Why this is non-trivial:
    For the diagonal family, each λ_m(ξ) is monotonically increasing
    (trivial spectral flow).  A mode-coupling perturbation V(ξ) can
    create avoided crossings, level repulsion, and non-monotonic
    eigenvalue trajectories.  But the NET spectral flow is unchanged.
    This is a consequence of the stability of the Fredholm index
    (Robbin-Salamon 1995).

Concrete demonstration:
    We construct explicit off-diagonal perturbations V(ξ) that couple
    modes m and m' (e.g., the negative mode m=3 with the positive
    mode m=2 for N=8).  We numerically track eigenvalue branches
    through avoided crossings and verify SF = μ(N) in every case.

Run: PYTHONPATH=src python3 -m planetary_polygons.proofs.topological_protection
"""
import numpy as np
from fractions import Fraction


def casimir(m, N):
    return Fraction(m * (N - m), 2)


def C1(xi):
    """C₁(ξ) = (N-1)(1+ξ²)/(1-ξ)² — but N-independent factor pulled out."""
    return (1 + xi**2) / (1 - xi)**2


def havelock_matrix(N, xi):
    """
    Diagonal Havelock family H_N(ξ) = C₁(ξ)·I - F_N.

    Returns (N-1)×(N-1) diagonal matrix with eigenvalues
    λ_m(ξ) = (N-1)·C₁(ξ) - m(N-m)/2.
    """
    c1 = (N - 1) * C1(xi)
    H = np.diag([c1 - float(casimir(m, N)) for m in range(1, N)])
    return H


def havelock_eigenvalue(m, N):
    """λ_m(0) = (N-1) - m(N-m)/2."""
    return (N - 1) - m * (N - m) / 2


def morse_index(N):
    """μ(N) = #{m : λ_m(0) < 0}."""
    return sum(1 for m in range(1, N) if havelock_eigenvalue(m, N) < 0)


# ============================================================
# Mode-coupling perturbations
# ============================================================

def coupling_perturbation(N, m1, m2, strength, xi):
    """
    Off-diagonal perturbation V(ξ) that couples modes m1 and m2.

    V(ξ) has V_{m1,m2} = V_{m2,m1} = strength · sin(πξ)
    (vanishes at ξ=0 and as ξ→1).

    This is the simplest perturbation that breaks diagonality
    while preserving the boundary conditions V(0) = 0.
    """
    V = np.zeros((N - 1, N - 1))
    i, j = m1 - 1, m2 - 1  # 0-indexed
    coupling = strength * np.sin(np.pi * xi)
    V[i, j] = coupling
    V[j, i] = coupling
    return V


def random_symmetric_perturbation(N, strength, xi, seed=42):
    """
    Random symmetric perturbation V(ξ) = strength·sin(πξ)·M
    where M is a fixed random symmetric matrix.

    Vanishes at ξ=0 and ξ=1 (envelope sin(πξ)).
    Couples ALL modes simultaneously.
    """
    rng = np.random.RandomState(seed)
    M = rng.randn(N - 1, N - 1)
    M = (M + M.T) / 2  # symmetrize
    M /= np.linalg.norm(M)  # normalize
    return strength * np.sin(np.pi * xi) * M


def bump_perturbation(N, m1, m2, strength, xi, center=0.5, width=0.1):
    """
    Localized off-diagonal perturbation: Gaussian bump centered at xi=center.

    V(ξ) couples modes m1 and m2 with a bump that vanishes at boundaries.
    """
    V = np.zeros((N - 1, N - 1))
    i, j = m1 - 1, m2 - 1
    envelope = strength * np.exp(-(xi - center)**2 / (2 * width**2))
    # Multiply by xi*(1-xi) to ensure vanishing at boundaries
    envelope *= xi * (1 - xi) * 4  # 4 for normalization
    V[i, j] = envelope
    V[j, i] = envelope
    return V


# ============================================================
# Spectral flow computation
# ============================================================

def compute_eigenvalue_branches(N, V_func, n_steps=2000, xi_max=0.999):
    """
    Track eigenvalue branches of H_N(ξ) + V(ξ) as ξ varies from 0 to xi_max.

    Returns:
        xi_values: array of shape (n_steps,)
        eigenvalues: array of shape (n_steps, N-1), sorted at each step
    """
    xi_values = np.linspace(0, xi_max, n_steps)
    eigenvalues = np.zeros((n_steps, N - 1))

    for i, xi in enumerate(xi_values):
        H = havelock_matrix(N, xi)
        if V_func is not None:
            V = V_func(N, xi)
            H = H + V
        eigs = np.linalg.eigvalsh(H)  # sorted ascending
        eigenvalues[i] = eigs

    return xi_values, eigenvalues


def compute_spectral_flow(eigenvalues, threshold=1e-10):
    """
    Count net zero crossings from the eigenvalue branch data.

    A crossing is counted when an eigenvalue changes sign between
    consecutive steps.  Positive crossing (- to +) counts +1,
    negative crossing (+ to -) counts -1.

    Returns (net_sf, crossings_detail).
    """
    n_steps, n_eigs = eigenvalues.shape
    net_sf = 0
    crossings = []

    for k in range(n_eigs):
        for i in range(n_steps - 1):
            e_curr = eigenvalues[i, k]
            e_next = eigenvalues[i + 1, k]
            if e_curr < -threshold and e_next > threshold:
                net_sf += 1
                crossings.append((i, k, '-to+'))
            elif e_curr > threshold and e_next < -threshold:
                net_sf -= 1
                crossings.append((i, k, '+to-'))

    return net_sf, crossings


def spectral_flow_from_boundary(N):
    """
    Compute SF from boundary data alone: SF = n₋(H(0)) - n₋(H(∞)).

    At ξ=0: n₋ = μ(N).
    At ξ→1: n₋ = 0 (all eigenvalues → +∞).
    Therefore SF = μ(N).

    This is the TRIVIAL computation (no index theory needed).
    """
    return morse_index(N)


# ============================================================
# Verification: topological protection under perturbations
# ============================================================

def verify_topological_protection(N, V_func, label="", n_steps=2000):
    """
    Verify that SF(H_N + V, 0→1) = μ(N) for a given perturbation V.

    Returns dict with verification results.
    """
    mu = morse_index(N)

    # Unperturbed (diagonal) spectral flow
    xi_diag, eigs_diag = compute_eigenvalue_branches(N, None, n_steps)
    sf_diag, _ = compute_spectral_flow(eigs_diag)

    # Perturbed spectral flow
    xi_pert, eigs_pert = compute_eigenvalue_branches(N, V_func, n_steps)
    sf_pert, crossings = compute_spectral_flow(eigs_pert)

    # Check boundary conditions
    eigs_at_0 = eigs_pert[0]
    eigs_at_end = eigs_pert[-1]
    n_neg_0 = np.sum(eigs_at_0 < -1e-10)
    n_neg_end = np.sum(eigs_at_end < -1e-10)

    return {
        'N': N,
        'mu': mu,
        'sf_diagonal': sf_diag,
        'sf_perturbed': sf_pert,
        'match': sf_pert == mu,
        'n_crossings': len(crossings),
        'n_neg_at_0': int(n_neg_0),
        'n_neg_at_end': int(n_neg_end),
        'boundary_preserved': n_neg_0 == mu and n_neg_end == 0,
        'label': label,
    }


def verify_suite(N_values=None):
    """
    Run the full verification suite: multiple perturbation types
    at multiple N values.

    Returns list of results.
    """
    if N_values is None:
        N_values = [6, 7, 8, 9, 10]

    results = []

    for N in N_values:
        mu = morse_index(N)

        # Test 1: No perturbation (baseline)
        r = verify_topological_protection(N, None, "diagonal (baseline)")
        results.append(r)

        # Test 2: Single mode coupling (bind mode with neighbor)
        m_bind = N // 2
        m_neighbor = max(1, m_bind - 1)
        if m_bind != m_neighbor:
            def V_single(N_, xi, m1=m_bind, m2=m_neighbor):
                return coupling_perturbation(N_, m1, m2, 5.0, xi)
            r = verify_topological_protection(
                N, V_single, f"couple m={m_bind},m={m_neighbor}, s=5")
            results.append(r)

        # Test 3: Strong random coupling
        def V_random(N_, xi):
            return random_symmetric_perturbation(N_, 10.0, xi)
        r = verify_topological_protection(
            N, V_random, "random symmetric, s=10")
        results.append(r)

        # Test 4: Very strong localized coupling
        if N >= 8:
            def V_bump(N_, xi, m1=3, m2=2):
                return bump_perturbation(N_, m1, m2, 50.0, xi)
            r = verify_topological_protection(
                N, V_bump, "bump m=3,2, s=50")
            results.append(r)

    return results


# ============================================================
# The proof: why this works
# ============================================================

def fredholm_stability_proof():
    """
    The analytical proof of topological protection.

    Returns a structured proof outline.
    """
    return {
        'theorem': (
            "Let V(ξ) be any continuous family of symmetric (N-1)×(N-1) "
            "matrices on [0,1) with V(0) = 0 and ||V(ξ)|| → 0 as ξ → 1⁻. "
            "Then SF(H_N + V, 0→1) = μ(N)."
        ),
        'proof_steps': [
            {
                'step': 1,
                'name': 'Fredholm property of D_N',
                'content': (
                    "D_N = d/dξ + H_N(ξ) on L²([0,1), R^{N-1}) with APS "
                    "boundary conditions. H_N(ξ) is self-adjoint with "
                    "eigenvalues → +∞ as ξ → 1⁻, so D_N is Fredholm "
                    "(Robbin-Salamon 1995, Theorem 4.1)."
                ),
            },
            {
                'step': 2,
                'name': 'Compact perturbation',
                'content': (
                    "V(ξ) → 0 as ξ → 1⁻ implies that V, viewed as a "
                    "multiplication operator on L²([0,1), R^{N-1}), is "
                    "D_N-compact: ||V·u||/||D_N·u|| → 0 for functions u "
                    "concentrated near ξ = 1. Hence D_N + V is also Fredholm."
                ),
            },
            {
                'step': 3,
                'name': 'Stability of Fredholm index',
                'content': (
                    "The map t ↦ ind(D_N + tV) is continuous (by openness "
                    "of Fredholm operators) and integer-valued, hence constant. "
                    "Therefore ind(D_N + V) = ind(D_N)."
                ),
            },
            {
                'step': 4,
                'name': 'Identification with spectral flow',
                'content': (
                    "By the Robbin-Salamon spectral flow theorem: "
                    "ind(D_N) = SF(H_N, 0→1) = μ(N) (diagonal computation). "
                    "ind(D_N + V) = SF(H_N + V, 0→1) (same theorem for "
                    "the perturbed operator). "
                    "Combining: SF(H_N + V, 0→1) = μ(N).  ∎"
                ),
            },
        ],
        'physical_content': (
            "The Morse index μ(N) is insensitive to mode coupling. "
            "A perturbation that couples Fourier modes (breaking the "
            "Z_N-diagonal structure of the Havelock family) can create "
            "avoided crossings and non-monotonic eigenvalue trajectories, "
            "but cannot change the net number of eigenvalues that cross "
            "zero. This topological protection is the genuine content of "
            "the index theorem in this setting."
        ),
        'what_this_does_NOT_prove': (
            "The theorem does NOT claim that individual eigenvalues are "
            "unchanged (they can move wildly), nor that stability of "
            "individual modes is preserved. It claims only that the NET "
            "spectral flow — the total count of instabilities created "
            "minus instabilities destroyed — is invariant."
        ),
    }


if __name__ == '__main__':
    print("=" * 70)
    print("Topological Protection of the Morse Index μ(N)")
    print("=" * 70)

    # Run verification suite
    results = verify_suite([7, 8, 9, 10])

    print(f"\n{'N':>3} {'μ':>3} {'SF(diag)':>8} {'SF(pert)':>8} "
          f"{'#cross':>6} {'match':>5}  {'perturbation'}")
    print("-" * 75)
    for r in results:
        check = "✓" if r['match'] else "✗"
        print(f"{r['N']:3d} {r['mu']:3d} {r['sf_diagonal']:8d} "
              f"{r['sf_perturbed']:8d} {r['n_crossings']:6d} "
              f"{check:>5}  {r['label']}")

    all_match = all(r['match'] for r in results)
    print(f"\nAll verified: {all_match}")

    # Show an example of non-trivial eigenvalue dynamics
    print("\n" + "=" * 70)
    print("Example: N=8 with strong mode coupling (m=3 ↔ m=2)")
    print("The negative mode m=3 couples to the positive mode m=2.")
    print("This creates an avoided crossing, but SF is unchanged.")
    print("=" * 70)

    N = 8

    def V_example(N_, xi):
        return coupling_perturbation(N_, 3, 2, 8.0, xi)

    xi, eigs_diag = compute_eigenvalue_branches(N, None, 500)
    _, eigs_pert = compute_eigenvalue_branches(N, V_example, 500)

    # Show eigenvalue trajectories at key points
    print(f"\n{'ξ':>6} ", end='')
    for m in range(1, N):
        print(f"{'λ_'+str(m):>8}", end='')
    print("  (perturbed)")
    for idx in [0, 50, 100, 150, 200, 300, 400, 499]:
        xi_val = xi[idx]
        print(f"{xi_val:6.3f} ", end='')
        for k in range(N - 1):
            print(f"{eigs_pert[idx, k]:8.3f}", end='')
        print()

    sf_diag, _ = compute_spectral_flow(eigs_diag)
    sf_pert, crossings = compute_spectral_flow(eigs_pert)
    print(f"\nSF(diagonal) = {sf_diag}")
    print(f"SF(perturbed) = {sf_pert}")
    print(f"μ(8) = {morse_index(8)}")
    print(f"Topologically protected: {sf_pert == morse_index(8)}")

    # Print the proof outline
    proof = fredholm_stability_proof()
    print("\n" + "=" * 70)
    print("PROOF OUTLINE")
    print("=" * 70)
    print(f"\nTheorem: {proof['theorem']}")
    for step in proof['proof_steps']:
        print(f"\nStep {step['step']} ({step['name']}):")
        print(f"  {step['content']}")
    print(f"\nPhysical content: {proof['physical_content']}")
    print(f"\nWhat this does NOT prove: {proof['what_this_does_NOT_prove']}")
