"""Tests for Lichnerowicz-Havelock equivalence and Hamiltonian constraint."""

import math
import pytest
import numpy as np
from planetary_polygons.extensions.lichnerowicz_havelock import (
    weyl_tensor_dimension, lichnerowicz_modes_2plus1,
    lichnerowicz_vs_havelock_3plus1,
    hamiltonian_constraint_check, adm_energy_from_stability,
    casimir_ratio, focusing_theorem_verification,
    raychaudhuri_analogy_table, dimensional_comparison,
    full_verification, casimir, b_exact,
)


class TestWeylTensor:
    def test_vanishes_2plus1(self):
        """Weyl tensor has 0 components in d=2,3."""
        assert weyl_tensor_dimension(2) == 0
        assert weyl_tensor_dimension(3) == 0

    def test_nonzero_4D(self):
        """Weyl tensor has 10 components in d=4."""
        assert weyl_tensor_dimension(4) == 10

    def test_grows(self):
        """Components grow with dimension."""
        for d in range(4, 8):
            assert weyl_tensor_dimension(d + 1) > weyl_tensor_dimension(d)


class TestLichnerowicz2plus1:
    def test_identical_to_havelock(self):
        """In 2+1D, Lichnerowicz eigenvalues = Havelock eigenvalues."""
        for N in [6, 8, 10]:
            result = lichnerowicz_modes_2plus1(N, xi=0.1)
            assert result['are_identical'] is True
            assert result['weyl_components'] == 0

    def test_eigenvalue_values(self):
        """Check specific eigenvalue values."""
        N, xi = 8, 0.1
        result = lichnerowicz_modes_2plus1(N, xi)
        C1 = (N - 1) * (1 + xi**2) / (1 - xi)**2
        for m in range(1, N):
            expected = C1 - m * (N - m) / 2
            assert result['havelock_eigenvalues'][m] == pytest.approx(expected)

    def test_stability_N7(self):
        """N=7 at xi=0: marginal (λ_3 = 0)."""
        result = lichnerowicz_modes_2plus1(7, xi=0.0)
        assert result['havelock_eigenvalues'][3] == pytest.approx(0.0)


class TestLichnerowicz3plus1:
    def test_has_tensor_modes(self):
        """3+1D has tensor modes from Weyl curvature."""
        result = lichnerowicz_vs_havelock_3plus1(8, theta0=0.5, Delta=1.0)
        assert result['has_tensor_modes'] is True
        assert result['weyl_components'] == 10
        assert result['exact_decomposition'] is False


class TestHamiltonianConstraint:
    def test_threshold_is_constraint(self):
        """At ρ*, V ≈ 0 (the Hamiltonian constraint)."""
        N = 8
        f_star = casimir(N // 2, N)
        b = b_exact(N)
        target = f_star - b
        rho_star = np.arcsinh(math.exp(target) / 2)
        result = hamiltonian_constraint_check(N, rho_star)
        assert abs(result['V']) < 0.01  # near zero at threshold

    def test_above_threshold_allowed(self):
        """Above ρ*: V > 0 (classically allowed)."""
        N = 8
        f_star = casimir(N // 2, N)
        b = b_exact(N)
        rho_star = np.arcsinh(math.exp(f_star - b) / 2)
        result = hamiltonian_constraint_check(N, rho_star + 2)
        assert result['V'] > 0

    def test_below_threshold_forbidden(self):
        """Below ρ*: V < 0 (classically forbidden / trapped)."""
        N = 10
        f_star = casimir(N // 2, N)
        b = b_exact(N)
        rho_star = np.arcsinh(math.exp(f_star - b) / 2)
        result = hamiltonian_constraint_check(N, max(0.1, rho_star - 2))
        assert result['V'] < 0


class TestADMEnergy:
    def test_positive_energy(self):
        """Above threshold: positive ADM energy (stable polygon)."""
        N = 8
        f_star = casimir(N // 2, N)
        b = b_exact(N)
        rho_star = np.arcsinh(math.exp(f_star - b) / 2)
        E, interp = adm_energy_from_stability(N, rho_star + 2)
        assert E > 0
        assert interp == "positive_energy_stable"

    def test_negative_energy(self):
        """Below threshold: negative ADM energy (trapped)."""
        N = 10
        E, interp = adm_energy_from_stability(N, 0.5)
        assert E < 0
        assert interp == "negative_energy_trapped"


class TestFocusingTheorem:
    def test_monotonicity(self):
        """R(Δ) is strictly increasing for all N ≥ 4."""
        for N in [4, 6, 8, 10, 12]:
            result = focusing_theorem_verification(N)
            assert result['is_monotone'] is True

    def test_limits(self):
        """R(0) = m*(N-m*)/(N-1), R(∞) → [sin(πm*/N)/sin(π/N)]²."""
        N = 8
        m = N // 2
        result = focusing_theorem_verification(N, Delta_values=np.linspace(0, 10, 100))
        R_0 = result['R_at_0']
        R_inf = result['R_at_inf']

        expected_R0 = m * (N - m) / (N - 1)
        expected_Rinf = (math.sin(math.pi * m / N) / math.sin(math.pi / N))**2

        assert R_0 == pytest.approx(expected_R0, rel=0.01)
        assert R_inf == pytest.approx(expected_Rinf, rel=0.05)

    def test_dR_positive(self):
        """dR/dΔ > 0 everywhere (the focusing condition)."""
        N = 8
        result = focusing_theorem_verification(N)
        for Delta, R, dR in result['dR_dDelta']:
            assert dR > 0, f"Focusing violated at Δ={Delta}: dR/dΔ={dR}"


class TestAnalogy:
    def test_table_complete(self):
        table = raychaudhuri_analogy_table()
        assert len(table) == 7
        concepts = [row[0] for row in table]
        assert "Focusing equation" in concepts
        assert "Positive energy theorem" in concepts


class TestDimensionalComparison:
    def test_structure(self):
        comp = dimensional_comparison()
        assert 'theorem_1_lichnerowicz' in comp
        assert 'theorem_2_hamiltonian' in comp
        assert 'theorem_3_focusing' in comp
        assert 'EXACT' in comp['theorem_1_lichnerowicz']['2+1D']
        assert 'APPROXIMATE' in comp['theorem_1_lichnerowicz']['3+1D']


class TestFullVerification:
    def test_runs(self):
        result = full_verification(N=8)
        assert result['theorem_1']['are_identical'] is True
        assert result['theorem_3']['is_monotone'] is True
        # Theorem 2: at threshold V ≈ 0
        assert abs(result['theorem_2']['at_threshold']['V']) < 0.1
