(* Mass Gap v4: Clean NDEigensystem with VERIFIED convergence *)
(* The v1 FEM was correct for small c but lost states at large c *)
(* The v3 Chebyshev had a matrix construction bug *)
(* This version: FEM with very fine mesh + convergence check *)

V[rho_] := Log[2 Sinh[rho]];

(* Solve using NDEigensystem with VERY fine mesh *)
solveGap[cVal_?NumericQ, nStates_Integer: 4] := Module[
  {evals, efuncs, rMin = 0.002, rMax, cs},
  rMax = 12.;
  (* Cell size: must resolve (2c)^{-1/3} *)
  cs = Max[0.0005, Min[0.003, 0.3/cVal^(1/3)]];
  {evals, efuncs} = NDEigensystem[
    {-1./(2. cVal) Derivative[2][u][x] + Log[2. Sinh[x]] u[x],
     DirichletCondition[u[x] == 0, True]},
    u[x], {x, rMin, rMax}, nStates,
    Method -> {"PDEDiscretization" -> {"FiniteElement",
      "MeshOptions" -> {"MaxCellMeasure" -> cs}}}
  ];
  Sort[Re[evals]]
];

(* Part 1: Convergence test at c = 100 *)
Print["CONVERGENCE TEST at c = 100"];
Print["============================"];
Do[
  {evals, efuncs} = NDEigensystem[
    {-1./200. Derivative[2][u][x] + Log[2. Sinh[x]] u[x],
     DirichletCondition[u[x] == 0, True]},
    u[x], {x, 0.002, 12.}, 4,
    Method -> {"PDEDiscretization" -> {"FiniteElement",
      "MeshOptions" -> {"MaxCellMeasure" -> cs}}}
  ];
  ev = Sort[Re[evals]];
  Print["cs = ", PaddedForm[cs, {8, 5}],
        "  nElem ~ ", PaddedForm[Round[12./cs], {6, 0}],
        "  E0 = ", PaddedForm[ev[[1]], {14, 8}],
        "  E1 = ", PaddedForm[ev[[2]], {14, 8}],
        "  gap = ", PaddedForm[ev[[2]] - ev[[1]], {14, 10}]],
  {cs, {0.01, 0.005, 0.003, 0.002, 0.001, 0.0005}}
];

(* Part 2: Gap vs c with fine mesh *)
Print["\nMASS GAP vs c (fine mesh, verified)"];
Print["===================================="];
gapData = {};
Do[
  ev = solveGap[cVal, 4];
  gap = ev[[2]] - ev[[1]];
  gap12 = ev[[3]] - ev[[2]];
  AppendTo[gapData, {cVal, gap}];
  Print["c = ", PaddedForm[N[cVal], {8, 1}],
        "  E0 = ", PaddedForm[ev[[1]], {14, 8}],
        "  E1 = ", PaddedForm[ev[[2]], {14, 8}],
        "  E2 = ", PaddedForm[ev[[3]], {14, 8}],
        "  gap01 = ", PaddedForm[gap, {12, 8}],
        "  gap12 = ", PaddedForm[gap12, {12, 8}]],
  {cVal, {20., 50., 100., 200., 500., 1000., 2000., 5000.}}
];

(* Part 3: Physical N values *)
Print["\nPHYSICAL N VALUES"];
Print["=================="];
Do[
  cPhys = N[12. (nn (nn + 1.)/12. - Log[2.] + Log[N[nn]]/(nn - 1.))];
  ev = solveGap[cPhys, 4];
  gap = ev[[2]] - ev[[1]];
  Print["N = ", PaddedForm[nn, {3, 0}],
        "  c = ", PaddedForm[cPhys, {10, 2}],
        "  gap = ", PaddedForm[gap, {14, 10}],
        "  E0 = ", PaddedForm[ev[[1]], {12, 6}],
        "  E1 = ", PaddedForm[ev[[2]], {12, 6}]],
  {nn, {6, 7, 8, 10, 12, 14, 16, 20}}
];

(* Part 4: If gap converges, check candidates *)
Print["\nASYMPTOTIC ANALYSIS"];
Print["==================="];
If[Length[gapData] >= 4,
  lastGaps = gapData[[-4 ;;]];
  Print["Last 4 gaps: ", lastGaps[[All, 2]]];
  (* Richardson extrapolation assuming gap = a + b/c^{1/3} *)
  g1 = lastGaps[[-2, 2]]; c1 = lastGaps[[-2, 1]];
  g2 = lastGaps[[-1, 2]]; c2 = lastGaps[[-1, 1]];
  (* gap = a + b * c^{-1/3} *)
  (* g1 = a + b * c1^{-1/3}, g2 = a + b * c2^{-1/3} *)
  b = (g1 - g2) / (c1^(-1/3) - c2^(-1/3));
  a = g1 - b * c1^(-1/3);
  Print["Richardson (alpha=1/3): gap(inf) = ", InputForm[a]];
  Print["  4/5 = 0.8, sqrt(2/3) = ", InputForm[N[Sqrt[2/3]]]];
  Print["  diff from 4/5: ", InputForm[a - 0.8]];
];

Print["\nDONE"];
