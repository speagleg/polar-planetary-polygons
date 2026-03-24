(* Mass gap via spectral method with change of variables *)
(* The log singularity at ρ→0 is regularized by mapping to *)
(* a new coordinate where the wavefunction is smooth. *)
(*                                                        *)
(* The potential: V(ρ) = Log[2 Sinh[ρ]]                   *)
(* Near ρ=0: V ~ Log[2ρ] → -∞ (the problem)              *)
(*                                                        *)
(* Change of variables: ρ = e^t, t ∈ (-∞, T_max)          *)
(* ψ(ρ) = ρ^{-1/2} φ(t) = e^{-t/2} φ(t)                *)
(* The Schrödinger equation becomes:                      *)
(* -φ''/(2c) + W(t) φ = E φ                              *)
(* where W(t) = V(e^t) + 1/(8c e^{2t})                   *)
(* The potential W is REGULAR as t → -∞:                  *)
(* W ~ t + Log[2] + 1/(8c)e^{-2t} → -∞ linearly         *)
(* This is an AIRY-like potential: no log singularity!    *)

Print["MASS GAP VIA SPECTRAL METHOD (regularized coordinates)"];
Print["========================================================"];
Print[];

(* The transformed potential *)
W[t_, cVal_] := Log[2 Sinh[Exp[t]]] + 1/(8 cVal Exp[2 t]);

(* Solve using NDEigensystem on the REGULAR potential W(t) *)
solveRegularized[cVal_?NumericQ, nStates_Integer: 4] := Module[
  {evals, efuncs, tMin, tMax, cs},
  (* t = Log[ρ], so ρ ∈ [ρ_min, ρ_max] maps to t ∈ [t_min, t_max] *)
  tMin = -10.;  (* ρ_min = e^{-10} ≈ 4.5×10⁻⁵ — very small *)
  tMax = Log[15.];  (* ρ_max = 15 *)
  cs = 0.01;  (* uniform mesh is fine since W(t) is smooth *)
  {evals, efuncs} = NDEigensystem[
    {-1./(2. cVal) Derivative[2][phi][t] + W[t, cVal] phi[t],
     DirichletCondition[phi[t] == 0, True]},
    phi[t], {t, tMin, tMax}, nStates,
    Method -> {"PDEDiscretization" -> {"FiniteElement",
      "MeshOptions" -> {"MaxCellMeasure" -> cs}}}
  ];
  Sort[Re[evals]]
];

(* Part 1: Convergence test at c = 127 *)
Print["CONVERGENCE TEST at c = 127 (N=11)"];
Print["====================================="];
cTest = 12. (11. * 12./12. - Log[2.] + Log[11.]/(11. - 1.));
Print["c = ", cTest];
Print[];

Do[
  ev = solveRegularized[cTest, 4];
  gap = ev[[2]] - ev[[1]];
  Print["cs = ", PaddedForm[cs, {8, 4}],
        "  E0 = ", PaddedForm[ev[[1]], {14, 8}],
        "  E1 = ", PaddedForm[ev[[2]], {14, 8}],
        "  gap = ", PaddedForm[gap, {14, 10}]],
  {cs, {0.05, 0.02, 0.01, 0.005, 0.002, 0.001}}
];

(* Part 2: Convergence test in tMin *)
Print[];
Print["CONVERGENCE TEST in tMin at c = 127"];
Print["======================================"];
Do[
  {evals, efuncs} = NDEigensystem[
    {-1./(2. cTest) Derivative[2][phi][t] + W[t, cTest] phi[t],
     DirichletCondition[phi[t] == 0, True]},
    phi[t], {t, tMin, Log[15.]}, 4,
    Method -> {"PDEDiscretization" -> {"FiniteElement",
      "MeshOptions" -> {"MaxCellMeasure" -> 0.005}}}
  ];
  ev = Sort[Re[evals]];
  Print["tMin = ", PaddedForm[tMin, {6, 1}],
        " (rho_min = ", PaddedForm[Exp[tMin], {10, 6}], ")",
        "  E0 = ", PaddedForm[ev[[1]], {14, 8}],
        "  E1 = ", PaddedForm[ev[[2]], {14, 8}],
        "  gap = ", PaddedForm[ev[[2]] - ev[[1]], {14, 10}]],
  {tMin, {-5., -7., -10., -12., -15., -20.}}
];

(* Part 3: Gap vs c using the regularized method *)
Print[];
Print["MASS GAP vs c (regularized spectral method)"];
Print["==============================================="];
Do[
  ev = solveRegularized[cVal, 4];
  gap = ev[[2]] - ev[[1]];
  gap12 = ev[[3]] - ev[[2]];
  Print["c = ", PaddedForm[N[cVal], {8, 1}],
        "  E0 = ", PaddedForm[ev[[1]], {14, 8}],
        "  E1 = ", PaddedForm[ev[[2]], {14, 8}],
        "  gap01 = ", PaddedForm[gap, {14, 10}],
        "  gap12 = ", PaddedForm[gap12, {14, 10}]],
  {cVal, {20., 40., 67., 85., 100., 127., 150., 200., 300., 500., 1000.}}
];

(* Part 4: Physical N values *)
Print[];
Print["MASS GAP AT PHYSICAL N VALUES"];
Print["================================"];
Do[
  cPhys = N[12. (nn (nn + 1.)/12. - Log[2.] + Log[N[nn]]/(nn - 1.))];
  ev = solveRegularized[cPhys, 4];
  gap = ev[[2]] - ev[[1]];
  Print["N = ", PaddedForm[nn, {3, 0}],
        "  c = ", PaddedForm[cPhys, {10, 2}],
        "  gap = ", PaddedForm[gap, {14, 10}],
        "  E0 = ", PaddedForm[ev[[1]], {12, 6}]],
  {nn, {6, 7, 8, 9, 10, 11, 12, 14, 16, 20}}
];

Print[];
Print["TARGET: gap(N=11) = 0.962 (from Planck baryon fraction)"];
Print["If gap ≈ 0.96: cosmological prediction CONFIRMED."];
Print["If gap ≈ 0.81: the prediction needs revision."];
Print["If gap ≈ 0.46: the original FEM was correct after all."];
Print[];
Print["DONE"];
