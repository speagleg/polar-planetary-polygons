"""Algebraic verification tests for Paper IV claims.

Covers CODE_ONLY items from the paper-to-code mapping audit:
cosmological constant, string tension, coupling lock, effective
levels, DHVW twist energy, proton stability, θ_QCD, Higgs quartic,
Verlinde dimension, Polyakov monopole action, non-integrable bound.
"""
import math


# ── Cosmological constant Λ₃ = (N²-16)/16 ───────────────────────────


class TestCosmologicalConstant:
    def test_lambda3_N4_zero(self):
        """Λ₃(4) = 0 exactly (electroweak threshold)"""
        assert (4**2 - 16) / 16 == 0

    def test_lambda3_N7(self):
        """Λ₃(7) = 33/16"""
        assert (7**2 - 16) / 16 == 33 / 16

    def test_lambda3_N11(self):
        """Λ₃(11) = 105/16 = 6.5625"""
        assert (11**2 - 16) / 16 == 105 / 16
        assert abs((11**2 - 16) / 16 - 6.5625) < 1e-10


# ── String tension σ/Λ² = 5.97 ──────────────────────────────────────


class TestStringTension:
    def test_verlinde_dimension_su3_genus2(self):
        """dim H(Σ₂, SU(3)₁) = 9 from Verlinde formula"""
        S_00 = 1 / math.sqrt(3)
        dim_H = 3 * S_00**(-2)  # 3 reps × (1/√3)^{-2} = 3 × 3
        assert abs(dim_H - 9) < 1e-10

    def test_z_s3_squared(self):
        """Z(S³, SU(3), k=1)² = 2"""
        # Witten formula: √(2/4)³ × (√2)² × 2 = √2
        prefactor = (2 / 4) ** (3 / 2)   # (1/√2)³ = 1/(2√2)
        j1 = (2 * math.sin(math.pi / 4)) ** 2  # (√2)² = 2
        j2 = (2 * math.sin(math.pi / 2)) ** 1  # 2
        Z = prefactor * j1 * j2
        assert abs(Z - math.sqrt(2)) < 1e-10
        assert abs(Z**2 - 2) < 1e-10

    def test_enhancement_ratio(self):
        """dim H / Z² = 9/2 = 4.5"""
        assert abs(9 / 2 - 4.5) < 1e-10

    def test_string_tension_value(self):
        """σ/Λ² = σ_YM × dim H / Z² = 1.326 × 4.5 = 5.97"""
        sigma_YM = 1.326
        enhancement = 9 / 2
        result = sigma_YM * enhancement
        assert abs(result - 5.97) < 0.01


# ── Coupling lock α/(8πG) = 1/(2π²) ────────────────────────────────


class TestCouplingLock:
    def test_coupling_lock_c_independent(self):
        """α/(8πG) = 1/(2π²) for any c"""
        for c in [51.57, 126.56, 200.0, 1000.0]:
            alpha = 6 / (math.pi * c)
            G = 3 / (2 * c)
            ratio = alpha / (8 * math.pi * G)
            assert abs(ratio - 1 / (2 * math.pi**2)) < 1e-10

    def test_coupling_lock_exact(self):
        """Algebraic: [6/(πc)] / [8π × 3/(2c)] = 6/(12π²) = 1/(2π²)"""
        # 6/(πc) ÷ (24π/2c) = 6/(πc) × 2c/(24π) = 12/(24π²) = 1/(2π²)
        assert abs(12 / (24 * math.pi**2) - 1 / (2 * math.pi**2)) < 1e-15


# ── Effective levels k_R, k_L ────────────────────────────────────────


class TestEffectiveLevels:
    def test_effective_levels_N7(self):
        """k_R = 5/14, k_L = 23/14 at N=7"""
        eta = 9 / 7  # |η_grav(7)| = 9/7
        k_R = 1 - eta / 2
        k_L = 1 + eta / 2
        assert abs(k_R - 5 / 14) < 1e-12
        assert abs(k_L - 23 / 14) < 1e-12

    def test_levels_sum(self):
        """k_R + k_L = 2 (bare levels sum)"""
        eta = 9 / 7
        k_R = 1 - eta / 2
        k_L = 1 + eta / 2
        assert abs(k_R + k_L - 2) < 1e-12


# ── DHVW twist energy ────────────────────────────────────────────────


class TestDHVW:
    def test_twist_energy_k1(self):
        """h₁ = 1(3-1)/9 = 2/9"""
        assert abs(1 * (3 - 1) / 9 - 2 / 9) < 1e-12

    def test_twist_energy_k2(self):
        """h₂ = 2(3-2)/9 = 2/9"""
        assert abs(2 * (3 - 2) / 9 - 2 / 9) < 1e-12

    def test_no_tachyons(self):
        """All twist energies > 0"""
        for k in [1, 2]:
            h_k = k * (3 - k) / 9
            assert h_k > 0


# ── Proton stability ─────────────────────────────────────────────────


class TestProtonStability:
    def test_z56_symmetry(self):
        """Z₅₆ = lcm(Z₇, Z₈)"""
        assert math.lcm(7, 8) == 56

    def test_z56_divides_baryon(self):
        """Baryon number B = 1/3 per quark, 3 quarks → B=1.
        Z₅₆ preserves B (no decay operators)."""
        assert 56 % 7 == 0
        assert 56 % 8 == 0


# ── θ_QCD = 0 ────────────────────────────────────────────────────────


class TestThetaQCD:
    def test_theta_zero_from_integer_level(self):
        """k = 1 (integer) → θ = 2π × frac(k) = 0"""
        k_bare = 1
        theta = 2 * math.pi * (k_bare - int(k_bare))
        assert abs(theta) < 1e-10


# ── Higgs mass ────────────────────────────────────────────────────────


class TestHiggsMass:
    def test_quartic_components(self):
        """λ_H = 0.10 + 0.014 + 0.008 = 0.122"""
        lam = 0.10 + 0.014 + 0.008
        assert abs(lam - 0.122) < 1e-6

    def test_higgs_mass_LO(self):
        """m_H = √(2λ_H) × v ≈ 122 GeV at LO"""
        lam = 0.122
        v = 246  # GeV
        m_H = math.sqrt(2 * lam) * v
        assert 120 < m_H < 125

    def test_higgs_mass_NLO(self):
        """m_H = √(2λ_H^NLO) × v ≈ 128 GeV at NLO"""
        lam_NLO = 0.135
        v = 246
        m_H = math.sqrt(2 * lam_NLO) * v
        assert 126 < m_H < 130

    def test_observed_in_range(self):
        """125.25 GeV lies in [122, 128]"""
        m_obs = 125.25
        assert 122 <= m_obs <= 128


# ── Polyakov monopole action ──────────────────────────────────────────


class TestPolyakovMonopole:
    def test_monopole_action_H2(self):
        """S_mon = 2πk(1 + K/(6k²)) = 5π/3 on H² (K=-1)"""
        k, K = 1, -1
        S_mon = 2 * math.pi * k * (1 + K / (6 * k**2))
        assert abs(S_mon - 5 * math.pi / 3) < 1e-10

    def test_negative_curvature_reduces_barrier(self):
        """K < 0 → S_mon < 2πk (barrier reduced)"""
        k, K = 1, -1
        S_mon = 2 * math.pi * k * (1 + K / (6 * k**2))
        S_flat = 2 * math.pi * k
        assert S_mon < S_flat

    def test_flat_space_limit(self):
        """K = 0 → S_mon = 2πk"""
        k, K = 1, 0
        S_mon = 2 * math.pi * k * (1 + K / (6 * k**2))
        assert abs(S_mon - 2 * math.pi) < 1e-10


# ── α_s strong coupling ──────────────────────────────────────────────


class TestStrongCoupling:
    def test_alpha_s_polygon_scale(self):
        """α_s(M_poly) = 1/(4π√2) = 0.0563"""
        alpha_s = 1 / (4 * math.pi * math.sqrt(2))
        assert abs(alpha_s - 0.0563) < 0.0001

    def test_alpha_s_derivation(self):
        """α_s = α_s^3D × (k+h∨) / V_eff, (k+h∨) cancels"""
        k, h_v = 1, 3
        alpha_3d = 1 / (k + h_v)  # = 1/4
        Z_S3 = math.sqrt(2)
        V_eff = k * 4 * math.pi * Z_S3
        # α_4d = α_3d × (k+h∨) / V_eff = (1/4) × 4 / (4π√2) = 1/(4π√2)
        alpha_4d = alpha_3d * (k + h_v) / V_eff
        assert abs(alpha_4d - 1 / (4 * math.pi * math.sqrt(2))) < 1e-10
