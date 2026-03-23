(* Mass gap at N=11 (c = 126.56): high-precision verification *)
(* PREDICTION: ΔE = 0.962 (from cosmological baryon fraction) *)
(* CURRENT FEM: ΔE ≈ 0.81 (possibly underestimated by boundary) *)

V[rho_] := Log[2 Sinh[rho]];
c = 12. (11. * 12./12. - Log[2.] + Log[11.]/(11. - 1.));
Print["c = ", c];
Print["Predicted gap: 0.962"];
Print[];

(* Convergence test: vary rMin at c = 127 *)
Print["CONVERGENCE TEST: varying rMin at c = ", Round[c]];
Print["=============================================="];
Do[
  {evals, efuncs} = NDEigensystem[
    {-1./(2. c) Derivative[2][u][x] + Log[2. Sinh[x]] u[x],
     DirichletCondition[u[x] == 0, True]},
    u[x], {x, rMin, 12.}, 3,
    Method -> {"PDEDiscretization" -> {"FiniteElement",
      "MeshOptions" -> {"MaxCellMeasure" -> 0.0005}}}
  ];
  ev = Sort[Re[evals]];
  Print["rMin = ", PaddedForm[rMin, {12, 8}],
        "  E0 = ", PaddedForm[ev[[1]], {14, 8}],
        "  E1 = ", PaddedForm[ev[[2]], {14, 8}],
        "  gap = ", PaddedForm[ev[[2]] - ev[[1]], {14, 10}]],
  {rMin, {0.01, 0.005, 0.002, 0.001, 0.0005, 0.0002, 0.0001, 0.00005, 0.00002, 0.00001}}
];

Print[];
Print["If gap converges to ~0.96: the cosmological prediction is CONFIRMED."];
Print["If gap stays at ~0.81: the boundary error hypothesis is RULED OUT."];
Print["DONE"];
