r"""Critical polygon number N_crit as a function of conformal dimension Δ.

Generalizes the flat-plane constrained Hessian analysis (core/hessian.py)
from the logarithmic interaction V = -log|x-y| to the power-law family
V = |x-y|^{-2Δ}.

For Δ = 0 (logarithmic):  N_crit = 7  (Havelock 1931)
For Δ > 0 (power-law):    N_crit(Δ) to be determined

The stability of the N-ring at radius R on the flat plane is determined
by the constrained Hessian on the surface {L = NR², P = 0}, where L is
angular impulse and P is linear impulse.

KEY QUESTION: Are the critical Δ values Δ*(N) (where N_crit drops below N)
algebraic or transcendental?
"""

import math
import numpy as np
from numpy.linalg import eigvalsh, svd, norm


# ============================================================
# Energy for general Δ
# ============================================================

def power_law_energy(pos, N, Delta):
    """E = Σ_{j<k} V(|z_j - z_k|) for the N-ring.

    V(r) = -log(r) for Δ = 0
    V(r) = r^{-2Δ}  for Δ > 0
    """
    x, y = pos[:N], pos[N:]
    E = 0.0
    for j in range(N):
        for k in range(j + 1, N):
            dx = x[j] - x[k]
            dy = y[j] - y[k]
            r2 = dx ** 2 + dy ** 2
            if r2 < 1e-30:
                return float('inf')
            if abs(Delta) < 1e-10:
                E -= 0.5 * math.log(r2)  # -log|z| = -½ log(r²)
            else:
                E += r2 ** (-Delta)  # r^{-2Δ} = (r²)^{-Δ}
    return E


def ngon_positions(N, R=1.0):
    """Regular N-gon on circle of radius R."""
    theta = 2 * np.pi * np.arange(N) / N
    return np.concatenate([R * np.cos(theta), R * np.sin(theta)])


# ============================================================
# Numerical derivatives
# ============================================================

def numerical_hessian(f, pos, eps=1e-5):
    """Central-difference Hessian via 4-point stencil."""
    n = len(pos)
    H = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            p_pp = pos.copy(); p_pp[i] += eps; p_pp[j] += eps
            p_pm = pos.copy(); p_pm[i] += eps; p_pm[j] -= eps
            p_mp = pos.copy(); p_mp[i] -= eps; p_mp[j] += eps
            p_mm = pos.copy(); p_mm[i] -= eps; p_mm[j] -= eps
            val = (f(p_pp) - f(p_pm) - f(p_mp) + f(p_mm)) / (4 * eps ** 2)
            H[i, j] = val
            H[j, i] = val
    return H


def numerical_gradient(f, pos, eps=1e-7):
    """Central-difference gradient."""
    n = len(pos)
    grad = np.zeros(n)
    for i in range(n):
        p_plus = pos.copy(); p_plus[i] += eps
        p_minus = pos.copy(); p_minus[i] -= eps
        grad[i] = (f(p_plus) - f(p_minus)) / (2 * eps)
    return grad


# ============================================================
# Constrained Hessian for general Δ
# ============================================================

def constrained_hessian_delta(N, Delta, R=1.0):
    """Constrained Hessian analysis for V = |x-y|^{-2Δ} on the N-ring.

    Returns dict with:
        constrained_evals: eigenvalues on the constraint surface
        is_stable: True if all constrained evals >= 0
        mu_L: Lagrange multiplier for angular impulse
        min_eval: minimum constrained eigenvalue
    """
    pos = ngon_positions(N, R)
    dim = 2 * N

    def energy(p):
        return power_law_energy(p, N, Delta)

    # Gradient
    grad_H = numerical_gradient(energy, pos)

    # Constraint gradients: L = Σ|z_k|², Px = Σx_k, Py = Σy_k
    grad_L = 2 * pos
    grad_Px = np.concatenate([np.ones(N), np.zeros(N)])
    grad_Py = np.concatenate([np.zeros(N), np.ones(N)])
    G = np.column_stack([grad_L, grad_Px, grad_Py])

    # Lagrange multipliers
    mu, _, _, _ = np.linalg.lstsq(G, grad_H, rcond=None)
    mu_L = mu[0]
    residual = norm(grad_H - G @ mu)

    # Full Hessian
    H_full = numerical_hessian(energy, pos)

    # Lagrangian Hessian: ∇²H - 2μ_L · I  (since ∇²L = 2I, ∇²P = 0)
    H_lagr = H_full - 2 * mu_L * np.eye(dim)

    # Tangent space of constraint surface
    U, S_vals, Vt = svd(G.T)
    rank = np.sum(S_vals > 1e-10)
    null_basis = Vt[rank:].T

    # Restricted Hessian
    H_restricted = null_basis.T @ H_lagr @ null_basis
    constrained_evals = eigvalsh(H_restricted)

    tol = 1e-4
    n_neg = int(np.sum(constrained_evals < -tol))
    min_eval = float(constrained_evals[0])

    return {
        'N': N,
        'Delta': Delta,
        'R': R,
        'mu_L': float(mu_L),
        'lagrange_residual': float(residual),
        'constrained_evals': constrained_evals,
        'min_eval': min_eval,
        'n_neg': n_neg,
        'is_stable': (n_neg == 0),
    }


# ============================================================
# N_crit(Δ) — the main result
# ============================================================

def ncrit_at_delta(Delta, N_max=12, R=1.0):
    """Find N_crit(Δ) — largest stable N on the flat plane.

    Uses the constrained Hessian on {L=const, P=0}.
    """
    for N_test in range(N_max, 2, -1):
        result = constrained_hessian_delta(N_test, Delta, R)
        if result['is_stable']:
            return N_test
    return 2


def stability_margin(N, Delta, R=1.0):
    """The minimum non-trivial constrained eigenvalue (stability margin).

    Skips eigenvalues near zero (rotation zero modes).
    Positive = stable, negative = unstable.
    """
    result = constrained_hessian_delta(N, Delta, R)
    evals = result['constrained_evals']
    # Separate genuinely negative from zero modes
    # Zero modes are from rotation symmetry (should be exactly 0 or 1 zero mode)
    negative = evals[evals < -1e-4]
    if len(negative) > 0:
        return float(negative[0])  # Most negative
    # No negative eigenvalues: return the smallest positive (skip zeros)
    positive = evals[evals > 1e-4]
    if len(positive) > 0:
        return float(positive[0])  # Smallest positive
    return 0.0  # All zeros (degenerate)


def find_critical_delta(N, Delta_lo=0.0, Delta_hi=20.0, tol=1e-10,
                        max_iter=80, R=1.0):
    """Find Δ*(N) where the N-ring transitions from stable to unstable.

    Uses bisection on the minimum constrained eigenvalue.
    Returns Δ*(N) or None if no transition in [Delta_lo, Delta_hi].
    """
    margin_lo = stability_margin(N, Delta_lo, R)
    margin_hi = stability_margin(N, Delta_hi, R)

    if margin_lo < 0 and margin_hi < 0:
        return None  # Unstable throughout
    if margin_lo >= 0 and margin_hi >= 0:
        return None  # Stable throughout

    for _ in range(max_iter):
        Delta_mid = (Delta_lo + Delta_hi) / 2
        margin_mid = stability_margin(N, Delta_mid, R)

        if abs(Delta_hi - Delta_lo) < tol:
            return Delta_mid

        if (margin_lo >= 0) == (margin_mid >= 0):
            Delta_lo = Delta_mid
            margin_lo = margin_mid
        else:
            Delta_hi = Delta_mid

    return (Delta_lo + Delta_hi) / 2


# ============================================================
# Generalized Casimir (analytical, for comparison)
# ============================================================

def weight_tilde(p, N, Delta):
    """w̃(p, Δ) = sin^{-2Δ-2}(πp/N) · [1 + 2Δ cos²(πp/N)]"""
    u = math.pi * p / N
    sin_u = math.sin(u)
    cos_u = math.cos(u)
    if abs(sin_u) < 1e-30:
        return float('inf')
    return sin_u ** (-2 * Delta - 2) * (1 + 2 * Delta * cos_u ** 2)


def generalized_casimir(m, N, Delta):
    """h(m, N, Δ) = Σ_{p=1}^{N-1} w̃(p,Δ)(1 - cos(2πmp/N))"""
    return sum(weight_tilde(p, N, Delta) * (1 - math.cos(2*math.pi*m*p/N))
               for p in range(1, N))


def casimir_ratio(m, N, Delta):
    """h(m,N,Δ) / h(1,N,Δ)"""
    h1 = generalized_casimir(1, N, Delta)
    return generalized_casimir(m, N, Delta) / h1 if abs(h1) > 1e-30 else float('inf')


# ============================================================
# PSLQ algebraicity analysis
# ============================================================

def analyze_critical_delta(N, Delta_star, tol=1e-6):
    """Test whether Δ*(N) is algebraic using PSLQ.

    For each degree d = 1, ..., 6, check if [1, Δ*, Δ*², ..., Δ*^d]
    has an integer relation with small coefficients.
    """
    if Delta_star is None:
        return {'N': N, 'Delta_star': None, 'status': 'no_transition'}

    import mpmath
    mpmath.mp.dps = 50
    D = mpmath.mpf(Delta_star)

    # PSLQ for degrees 1..6
    pslq_results = {}
    for deg in range(1, 7):
        vec = [D ** k for k in range(deg + 1)]
        try:
            rel = mpmath.pslq(vec, maxcoeff=10000, tol=mpmath.mpf(10) ** (-15))
            if rel is not None:
                pslq_results[deg] = [int(c) for c in rel]
        except Exception:
            pass

    # Quick rational test
    best_rational = None
    for q in range(1, 100):
        p = round(float(D) * q)
        if p > 0 and abs(D - mpmath.mpf(p) / q) < tol:
            if best_rational is None or q < best_rational[1]:
                best_rational = (p, q)

    return {
        'N': N,
        'Delta_star': float(Delta_star),
        'pslq': pslq_results,
        'best_rational': best_rational,
    }


# ============================================================
# Master computations
# ============================================================

def ncrit_delta_scan(Delta_values=None, N_max=12):
    """N_crit(Δ) for a range of Δ."""
    if Delta_values is None:
        Delta_values = [0, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0]
    return [(D, ncrit_at_delta(D, N_max)) for D in Delta_values]


def critical_delta_table(N_range=None):
    """Find Δ*(N) for each N in range."""
    if N_range is None:
        N_range = range(3, 13)

    results = []
    for N in N_range:
        margin_0 = stability_margin(N, 0.0)
        stable_0 = margin_0 >= -1e-4

        if not stable_0:
            # N ≥ 8: unstable at Δ=0. Does it become stable at some Δ>0?
            # Check if margin becomes positive
            found = False
            for D_test in [0.5, 1.0, 2.0, 5.0, 10.0, 20.0]:
                m = stability_margin(N, D_test)
                if m >= 0:
                    # Find the transition
                    Delta_star = find_critical_delta(N, 0.0, D_test)
                    results.append({
                        'N': N, 'stable_at_0': False,
                        'restabilizes': True, 'Delta_star': Delta_star,
                        'margin_0': float(margin_0),
                    })
                    found = True
                    break
            if not found:
                results.append({
                    'N': N, 'stable_at_0': False,
                    'restabilizes': False, 'Delta_star': None,
                    'margin_0': float(margin_0),
                })
        else:
            # N ≤ 7: stable at Δ=0. Does it lose stability at some Δ>0?
            found = False
            for D_test in [1.0, 5.0, 20.0, 100.0]:
                m = stability_margin(N, D_test)
                if m < 0:
                    Delta_star = find_critical_delta(N, 0.0, D_test)
                    results.append({
                        'N': N, 'stable_at_0': True,
                        'loses_stability': True, 'Delta_star': Delta_star,
                        'margin_0': float(margin_0),
                    })
                    found = True
                    break
            if not found:
                results.append({
                    'N': N, 'stable_at_0': True,
                    'loses_stability': False, 'Delta_star': None,
                    'margin_0': float(margin_0),
                })

    return results


if __name__ == '__main__':
    print("=" * 60)
    print("N_crit(Δ) — flat-plane constrained Hessian")
    print("=" * 60)

    # Quick scan
    print("\n--- N_crit(Δ) scan ---")
    for D, nc in ncrit_delta_scan():
        print(f"  Δ = {D:5.1f}  →  N_crit = {nc}")

    # Critical Δ for each N
    print("\n--- Δ*(N) table ---")
    for row in critical_delta_table():
        N = row['N']
        if row.get('stable_at_0'):
            if row.get('loses_stability'):
                print(f"  N={N:2d}: stable at Δ=0 (margin={row['margin_0']:.4f}), "
                      f"loses stability at Δ*={row['Delta_star']:.8f}")
            else:
                print(f"  N={N:2d}: stable at Δ=0 (margin={row['margin_0']:.4f}), "
                      f"STABLE for all Δ tested")
        else:
            if row.get('restabilizes'):
                print(f"  N={N:2d}: UNSTABLE at Δ=0 (margin={row['margin_0']:.4f}), "
                      f"restabilizes at Δ*={row['Delta_star']:.8f}")
            else:
                print(f"  N={N:2d}: UNSTABLE at Δ=0 (margin={row['margin_0']:.4f}), "
                      f"remains unstable")
