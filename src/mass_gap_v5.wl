(* Mass Gap v5: Fix the left boundary and mesh resolution *)
(* The issue: ground state lives at rho ~ c^{-1/3} and the *)
(* boundary rMin = 0.002 was too far from 0 for large c. *)
(* Also: use logarithmic mesh spacing near rho = 0. *)

V[rho_] := Log[2 Sinh[rho]];

(* Strategy: map to a new coordinate that concentrates points near 0 *)
(* Use the substitution rho = rMax * (t/tMax)^2 where t in [0, tMax] *)
(* This gives quadratically fine spacing near rho = 0. *)

(* Or simpler: just use a very small rMin and let Mathematica handle it *)
solveGap[cVal_?NumericQ, nStates_Integer: 4] := Module[
  {evals, efuncs, rMin, rMax, cs},
  (* rMin must be << c^{-1/3} to not cut off the wavefunction *)
  rMin = Min[0.0001, 0.01/cVal^(1/3)];
  rMax = 12.;
  (* Cell size: resolve the wavefunction width ~ c^{-1/3} *)
  cs = Max[0.0003, Min[0.002, 0.2/cVal^(1/3)]];
  {evals, efuncs} = NDEigensystem[
    {-1./(2. cVal) Derivative[2][u][x] + Log[2. Sinh[x]] u[x],
     DirichletCondition[u[x] == 0, True]},
    u[x], {x, rMin, rMax}, nStates,
    Method -> {"PDEDiscretization" -> {"FiniteElement",
      "MeshOptions" -> {"MaxCellMeasure" -> cs}}}
  ];
  Sort[Re[evals]]
];

(* Part 1: Convergence test at c = 200 (where the drop happened) *)
Print["CONVERGENCE TEST at c = 200, varying rMin"];
Print["============================================="];
Do[
  {evals, efuncs} = NDEigensystem[
    {-1./400. Derivative[2][u][x] + Log[2. Sinh[x]] u[x],
     DirichletCondition[u[x] == 0, True]},
    u[x], {x, rMin, 12.}, 4,
    Method -> {"PDEDiscretization" -> {"FiniteElement",
      "MeshOptions" -> {"MaxCellMeasure" -> 0.001}}}
  ];
  ev = Sort[Re[evals]];
  Print["rMin = ", PaddedForm[rMin, {10, 6}],
        "  E0 = ", PaddedForm[ev[[1]], {14, 8}],
        "  E1 = ", PaddedForm[ev[[2]], {14, 8}],
        "  gap = ", PaddedForm[ev[[2]] - ev[[1]], {14, 10}]],
  {rMin, {0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001, 0.0005, 0.0001}}
];

(* Part 2: Convergence at c = 500 *)
Print["\nCONVERGENCE TEST at c = 500, varying rMin"];
Do[
  {evals, efuncs} = NDEigensystem[
    {-1./1000. Derivative[2][u][x] + Log[2. Sinh[x]] u[x],
     DirichletCondition[u[x] == 0, True]},
    u[x], {x, rMin, 12.}, 4,
    Method -> {"PDEDiscretization" -> {"FiniteElement",
      "MeshOptions" -> {"MaxCellMeasure" -> 0.0005}}}
  ];
  ev = Sort[Re[evals]];
  Print["rMin = ", PaddedForm[rMin, {10, 6}],
        "  E0 = ", PaddedForm[ev[[1]], {14, 8}],
        "  E1 = ", PaddedForm[ev[[2]], {14, 8}],
        "  gap = ", PaddedForm[ev[[2]] - ev[[1]], {14, 10}]],
  {rMin, {0.05, 0.02, 0.01, 0.005, 0.002, 0.001, 0.0005, 0.0001, 0.00005}}
];

(* Part 3: Gap vs c with corrected rMin *)
Print["\nMASS GAP vs c (corrected rMin)"];
Print["==============================="];
Do[
  ev = solveGap[cVal, 4];
  gap = ev[[2]] - ev[[1]];
  Print["c = ", PaddedForm[N[cVal], {8, 1}],
        "  E0 = ", PaddedForm[ev[[1]], {14, 8}],
        "  E1 = ", PaddedForm[ev[[2]], {14, 8}],
        "  gap = ", PaddedForm[gap, {14, 10}]],
  {cVal, {50., 100., 200., 300., 500., 750., 1000.}}
];

Print["\nDONE"];
