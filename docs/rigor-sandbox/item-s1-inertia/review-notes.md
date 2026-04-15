# S1: Proposition 17 (prop:inertia) — Proof Repair

## Bug
Line 2913 of paper-2-physics/main.tex claims:
  ‖δω‖_{H⁻¹} ≥ (c_P/ε)‖δω‖_{L²}
This is backwards: H⁻¹ is weaker than L², so the inequality should be ≤ not ≥.

## Consequence
- The coercivity lower bound on λ_min(H_ss) is wrong
- The derived ε₀(N) = (λ_min d_min⁶)^{1/4} has wrong scaling
- The Schur complement bound O(ε⁶/d_min⁶) is wrong

## Correct approach
1. H_ss > 0 follows directly: H⁻¹ inner product is positive on mean-zero perturbations
2. Schur complement: In(H) = In(H_ss) + In(S), S = H_cc - H_cs H_ss⁻¹ H_cs^T
3. Bound ‖H_cs H_ss⁻¹ H_cs^T‖ via regularity of coupling (not via λ_min(H_ss))
4. Key: H_cs^T v is smooth (quadrupole), so ⟨H_cs^T v, H_ss⁻¹ H_cs^T v⟩ = 4π² ‖∇(H_cs^T v)‖² < ∞

## Oracle results (numerical_check.py, scaling_analysis.py)
- H_ss > 0 confirmed for all N, all ε
- λ_min(H_ss) ~ ε² (exact: ε^2.00)
- coupling_m ~ ε^{m+1} (m=2: ε^2.95, m=3: ε^3.90, m=4: ε^4.94)
- Schur contribution from mode m ~ ε^{2m} (leading m=2: ε^3.90)
- Total ‖correction‖ ~ ε^{3.99} → O(ε⁴/d⁶), NOT O(ε⁶/d⁶)
- δ(N) values UNCHANGED (determined by O(ε²) blob correction, not Schur)

## Status
- [x] Numerical oracle
- [x] Algebraic derivation
- [ ] Review gate (≥ 9.0)
- [ ] Integration
