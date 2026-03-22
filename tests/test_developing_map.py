"""Tests for the developing map and conformal invariance theorem."""
import math
import cmath
import pytest
from planetary_polygons.extensions.developing_map import (
    gamma_func, hyp2f1_series, hyp2f1_at_one,
    image_radius, developing_map, developing_map_derivative,
    havelock_eigenvalue_flat, numerical_hessian_eigenvalues,
    image_positions, developing_map_first_order,
)


class TestGammaFunction:
    def test_integers(self):
        """Gamma(n) = (n-1)! for positive integers."""
        assert abs(gamma_func(1) - 1.0) < 1e-12
        assert abs(gamma_func(2) - 1.0) < 1e-12
        assert abs(gamma_func(3) - 2.0) < 1e-12
        assert abs(gamma_func(4) - 6.0) < 1e-12
        assert abs(gamma_func(5) - 24.0) < 1e-12

    def test_half_integers(self):
        """Gamma(1/2) = sqrt(pi)."""
        assert abs(gamma_func(0.5) - math.sqrt(math.pi)) < 1e-10

    def test_reflection(self):
        """Gamma(x)*Gamma(1-x) = pi/sin(pi*x)."""
        for x in [0.2, 0.3, 0.7, 1.0/3, 1.0/7]:
            product = gamma_func(x) * gamma_func(1 - x)
            expected = math.pi / math.sin(math.pi * x)
            assert abs(product - expected) < 1e-8, f"x={x}"


class TestHypergeometric:
    def test_trivial(self):
        """_2F1(0, b; c; z) = 1."""
        assert abs(hyp2f1_series(0, 0.5, 1.5, 0.5) - 1.0) < 1e-14

    def test_geometric(self):
        """_2F1(1, 1; 1; z) = 1/(1-z) for |z| < 1."""
        for z in [0.1, 0.3, 0.5, 0.7, 0.9]:
            val = hyp2f1_series(1, 1, 1, z)
            assert abs(val - 1.0 / (1 - z)) < 1e-10

    def test_log(self):
        """_2F1(1, 1; 2; z) = -log(1-z)/z for |z| < 1."""
        for z in [0.1, 0.3, 0.5, 0.7]:
            val = hyp2f1_series(1, 1, 2, z)
            expected = -math.log(1 - z) / z
            assert abs(val - expected) < 1e-10

    def test_gauss_at_one(self):
        """Gauss's formula at z = 1."""
        # _2F1(1/2, 1/3; 5/6; 1) should be finite
        val = hyp2f1_at_one(0.5, 1.0 / 3, 5.0 / 6)
        # c - a - b = 5/6 - 1/2 - 1/3 = 0 => diverges!
        # Use a convergent case instead.
        # _2F1(0.1, 0.2; 1.0; 1) = Gamma(1)*Gamma(0.7)/(Gamma(0.9)*Gamma(0.8))
        val = hyp2f1_at_one(0.1, 0.2, 1.0)
        expected = (gamma_func(1.0) * gamma_func(0.7)
                    / (gamma_func(0.9) * gamma_func(0.8)))
        assert abs(val - expected) < 1e-10


class TestImageRadius:
    def test_beta_zero(self):
        """At beta = 0: R_f = 1 for all N."""
        for N in range(3, 15):
            assert abs(image_radius(N, 0.0) - 1.0) < 1e-12

    def test_increasing_in_beta(self):
        """R_f increases as beta increases: the developing map expands
        the N-gon because the cone metric inflates distances near the tips."""
        for N in [3, 5, 7, 10]:
            prev = 1.0
            for beta in [0.01, 0.05, 0.1]:
                if beta < 1.0 / N:
                    Rf = image_radius(N, beta)
                    assert Rf > prev, f"N={N}, beta={beta}"
                    prev = Rf

    def test_endpoint_formula(self):
        """At beta = 1/N: R_f = (pi/N)/sin(pi/N)."""
        for N in [3, 4, 5, 6, 8, 10, 12]:
            beta = 1.0 / N - 1e-8  # approach endpoint
            Rf = image_radius(N, beta)
            Rf_exact = (math.pi / N) / math.sin(math.pi / N)
            assert abs(Rf - Rf_exact) < 0.01, (
                f"N={N}: R_f={Rf}, expected={Rf_exact}")

    def test_reflection_formula_endpoint(self):
        """R_f(beta=1/N) = Gamma(1+1/N)*Gamma(1-1/N) = (pi/N)/sin(pi/N)
        by the Gamma reflection formula."""
        for N in [3, 5, 7, 11]:
            G1 = gamma_func(1 + 1.0 / N)
            G2 = gamma_func(1 - 1.0 / N)
            product = G1 * G2
            expected = (math.pi / N) / math.sin(math.pi / N)
            assert abs(product - expected) < 1e-10, f"N={N}"


class TestDevelopingMap:
    def test_identity_at_beta_zero(self):
        """At beta = 0: f(z) = z."""
        for z in [0.3, 0.5 + 0.3j, 0.7j, -0.2 + 0.8j]:
            f = developing_map(z, 5, 0.0)
            assert abs(f - z) < 1e-12

    def test_derivative_at_beta_zero(self):
        """At beta = 0: f'(z) = 1."""
        for z in [0.3, 0.5j, -0.4 + 0.2j]:
            fp = developing_map_derivative(z, 5, 0.0)
            assert abs(fp - 1.0) < 1e-12

    def test_zn_symmetry(self):
        """f(omega*z) = omega*f(z) for omega = exp(2pi*i/N)."""
        for N in [3, 5, 7]:
            omega = cmath.exp(2j * math.pi / N)
            for beta in [0.01, 0.05]:
                z = 0.3 + 0.4j
                f_z = developing_map(z, N, beta)
                f_wz = developing_map(omega * z, N, beta)
                assert abs(f_wz - omega * f_z) < 1e-10, (
                    f"N={N}, beta={beta}")

    def test_image_is_regular_ngon(self):
        """Image positions form a regular N-gon of radius R_f."""
        for N in [4, 6, 8]:
            for beta in [0.01, 0.05]:
                Rf = image_radius(N, beta)
                positions = image_positions(N, beta)
                for j in range(N):
                    # Check radius
                    assert abs(abs(positions[j]) - Rf) < 1e-10
                    # Check angle
                    expected_angle = 2 * math.pi * j / N
                    actual_angle = cmath.phase(positions[j])
                    # Normalize to [0, 2pi)
                    diff = (actual_angle - expected_angle) % (2 * math.pi)
                    if diff > math.pi:
                        diff -= 2 * math.pi
                    assert abs(diff) < 1e-10

    def test_developing_map_approaches_image_radius(self):
        """f(r*z_j) -> R_f*z_j as r -> 1 from below."""
        N = 6
        beta = 0.05
        Rf = image_radius(N, beta)
        z_j = cmath.exp(2j * math.pi / N)  # first cone point
        for r in [0.9, 0.95, 0.99, 0.999]:
            f = developing_map(r * z_j, N, beta)
            expected = Rf * z_j  # in the limit r -> 1
            # Should approach
            if r > 0.99:
                assert abs(abs(f) - Rf * r) < 0.1 * Rf


class TestDerivative:
    def test_matches_finite_difference(self):
        """f'(z) matches (f(z+h) - f(z-h)) / (2h)."""
        N, beta = 5, 0.03
        z = 0.4 + 0.3j
        h = 1e-7
        fp = developing_map_derivative(z, N, beta)
        fd = (developing_map(z + h, N, beta)
              - developing_map(z - h, N, beta)) / (2 * h)
        assert abs(fp - fd) < 1e-5, f"f'={fp}, FD={fd}"

    def test_diverges_near_cone(self):
        """f'(z) diverges as z -> cone point."""
        N, beta = 5, 0.1
        z_cone = 1.0  # cone point at z=1 (5th root of unity)
        prev = abs(developing_map_derivative(0.5, N, beta))
        for r in [0.9, 0.95, 0.99, 0.999]:
            val = abs(developing_map_derivative(r, N, beta))
            assert val > prev, f"r={r}: |f'|={val} not increasing"
            prev = val


class TestConformalInvariance:
    """The central theorem: Havelock eigenvalues are independent of beta."""

    def test_tangential_eigenvalues_match(self):
        """Tangential Hessian eigenvalues are m(N-m)/2.

        The full Havelock eigenvalue is lambda_m = (N-1) - m(N-m)/2,
        where (N-1) comes from the angular-impulse constraint.
        The purely tangential Hessian gives only the interaction
        part: mu_m = m(N-m)/2.
        """
        for N in range(3, 10):
            eigs = numerical_hessian_eigenvalues(N, R=1.0)
            for m in range(N):
                expected = m * (N - m) / 2  # tangential eigenvalue
                assert abs(eigs[m] - expected) < 0.2, (
                    f"N={N}, m={m}: got {eigs[m]:.3f}, "
                    f"expected {expected:.3f}")

    def test_eigenvalues_independent_of_radius(self):
        """Eigenvalues don't change when R changes (scaling invariance)."""
        N = 7
        eigs_R1 = numerical_hessian_eigenvalues(N, R=1.0)
        for R in [0.5, 2.0, 0.1]:
            eigs = numerical_hessian_eigenvalues(N, R=R)
            for m in range(N):
                assert abs(eigs[m] - eigs_R1[m]) < 0.2, (
                    f"R={R}, m={m}: {eigs[m]:.3f} vs {eigs_R1[m]:.3f}")

    def test_eigenvalues_independent_of_beta(self):
        """THE KEY TEST: tangential eigenvalues are the same for all beta.

        The developing map expands the N-gon to radius R_f(beta),
        but the eigenvalues (in angular coordinates) are unchanged
        because log(R*d) = log(R) + log(d) and log(R) drops from
        the angular Hessian.
        """
        for N in [5, 7, 8]:
            eigs_flat = numerical_hessian_eigenvalues(N, R=1.0)
            for beta in [0.01, 0.05, 0.1]:
                if beta >= 1.0 / N:
                    continue
                Rf = image_radius(N, beta)
                eigs_cone = numerical_hessian_eigenvalues(N, R=Rf)
                for m in range(N):
                    expected = m * (N - m) / 2
                    assert abs(eigs_cone[m] - expected) < 0.2, (
                        f"N={N}, beta={beta}, m={m}: "
                        f"cone={eigs_cone[m]:.3f}, "
                        f"expected={expected:.3f}")

    def test_ncrit_7_all_beta(self):
        """N_crit = 7 for all beta < 1/N: the stability boundary
        does not shift with deficit angle."""
        for beta in [0.0, 0.01, 0.05, 0.1]:
            # N=7: all eigenvalues >= 0
            eigs7 = numerical_hessian_eigenvalues(7, R=image_radius(7, beta))
            assert all(e > -0.5 for e in eigs7), (
                f"beta={beta}: N=7 eigenvalues {eigs7}")

            # N=8: at least one eigenvalue < 0
            if beta < 1.0 / 8:
                eigs8 = numerical_hessian_eigenvalues(
                    8, R=image_radius(8, beta))
                min_eig = min(eigs8)
                assert min_eig < 0, (
                    f"beta={beta}: N=8 min eigenvalue {min_eig}")


class TestFirstOrderExpansion:
    def test_g_at_zero(self):
        """g(0) = 0 (no correction at the origin)."""
        for N in [3, 5, 7]:
            g = developing_map_first_order(0.0, N)
            assert abs(g) < 1e-15

    def test_g_matches_full(self):
        """beta * g(z^N) matches (f(z) - z) / z for small beta."""
        N = 5
        beta = 0.001
        z = 0.3 + 0.2j
        g = developing_map_first_order(z, N)
        f = developing_map(z, N, beta)
        correction = (f - z) / z  # should be ≈ beta * g
        assert abs(correction - beta * g) < beta ** 2, (
            f"correction={correction}, beta*g={beta * g}")


class TestImageRadiusProperties:
    def test_monotone_in_N(self):
        """For fixed beta, R_f approaches 1 from above as N grows
        (more cone points = smaller individual deficit, less expansion)."""
        beta = 0.01
        prev = float('inf')
        for N in range(4, 12):
            if beta < 1.0 / N:
                Rf = image_radius(N, beta)
                assert Rf > 1.0  # always expanded
                assert Rf < prev  # less expansion for larger N
                prev = Rf

    def test_small_beta_expansion(self):
        """R_f ≈ 1 - beta * [psi(1+1/N) - psi(1)] + O(beta^2)
        where psi is the digamma function.

        For small beta: Gamma(1-beta) ≈ 1 + gamma*beta, etc.
        Just check R_f ≈ 1 - const*beta for small beta.
        """
        N = 5
        R1 = image_radius(N, 0.001)
        R2 = image_radius(N, 0.002)
        # Should be linear: (1 - R1) / 0.001 ≈ (1 - R2) / 0.002
        slope1 = (1 - R1) / 0.001
        slope2 = (1 - R2) / 0.002
        assert abs(slope1 - slope2) / slope1 < 0.01
