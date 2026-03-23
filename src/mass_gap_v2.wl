(* Mass Gap v2: Adaptive mesh that refines near rho=0 *)
(* The ground state lives at rho ~ (2c)^{-1/3}, so we need *)
(* fine mesh there and can be coarser at large rho *)

V[rho_] := Log[2 Sinh[rho]];

(* Version using shooting method / parametric NDSolve for better accuracy *)
solveWDW[cVal_?NumericQ, nStates_Integer: 3] := Module[
  {evals, efuncs, rMax, rMin, cellSize},
  (* Adaptive: finer mesh for larger c *)
  rMin = 0.001;
  rMax = Min[15, 5 + 2 Log[cVal]];
  cellSize = Min[0.005, 0.5/(cVal^(1/3))]; (* resolves the wavefunction *)
  {evals, efuncs} = NDEigensystem[
    {-1/(2 cVal) u''[x] + Log[2 Sinh[x]] u[x],
     DirichletCondition[u[x] == 0, True]},
    u[x], {x, rMin, rMax}, nStates,
    Method -> {"PDEDiscretization" -> {"FiniteElement",
      "MeshOptions" -> {"MaxCellMeasure" -> cellSize}}}
  ];
  Sort[evals]
];

(* Part 1: Gap vs c with adaptive mesh *)
Print["MASS GAP vs c (adaptive mesh)"];
Print["=============================="];
Do[
  ev = solveWDW[cVal, 4];
  gap01 = ev[[2]] - ev[[1]];
  gap12 = ev[[3]] - ev[[2]];
  Print["c = ", PaddedForm[N[cVal], {8, 1}],
        "  E0 = ", PaddedForm[ev[[1]], {12, 6}],
        "  E1 = ", PaddedForm[ev[[2]], {12, 6}],
        "  gap01 = ", PaddedForm[gap01, {12, 8}],
        "  gap12 = ", PaddedForm[gap12, {12, 8}],
        "  ratio12/01 = ", PaddedForm[gap12/gap01, {8, 4}]],
  {cVal, {20., 40., 60., 80., 100., 150., 200., 300., 500., 1000.}}
];

(* Part 2: Physical N values *)
Print["\nGAP AT PHYSICAL N VALUES (adaptive mesh)"];
Print["========================================="];
Do[
  cPhys = N[12 (nn (nn + 1)/12 - Log[2] + Log[nn]/(nn - 1))];
  ev = solveWDW[cPhys, 4];
  gap = ev[[2]] - ev[[1]];
  Print["N = ", PaddedForm[nn, {3, 0}],
        "  c = ", PaddedForm[cPhys, {10, 2}],
        "  cellSize = ", PaddedForm[N[0.5/cPhys^(1/3)], {8, 4}],
        "  gap = ", PaddedForm[gap, {12, 8}],
        "  E0 = ", PaddedForm[ev[[1]], {12, 6}],
        "  E1 = ", PaddedForm[ev[[2]], {12, 6}]],
  {nn, {6, 7, 8, 10, 12, 14, 16, 20}}
];

(* Part 3: Convergence test - same c, decreasing cell size *)
Print["\nCONVERGENCE TEST at c = 100"];
Print["==========================="];
Do[
  {evals, efuncs} = NDEigensystem[
    {-1/(2*100.) u''[x] + Log[2 Sinh[x]] u[x],
     DirichletCondition[u[x] == 0, True]},
    u[x], {x, 0.001, 12}, 3,
    Method -> {"PDEDiscretization" -> {"FiniteElement",
      "MeshOptions" -> {"MaxCellMeasure" -> cs}}}
  ];
  ev = Sort[evals];
  Print["cellSize = ", PaddedForm[cs, {8, 5}],
        "  E0 = ", PaddedForm[ev[[1]], {14, 8}],
        "  E1 = ", PaddedForm[ev[[2]], {14, 8}],
        "  gap = ", PaddedForm[ev[[2]] - ev[[1]], {14, 10}]],
  {cs, {0.05, 0.02, 0.01, 0.005, 0.002, 0.001}}
];

(* Part 4: Alternative - use DEigensystem with explicit operator *)
Print["\nALTERNATIVE: Spectral method (Chebyshev collocation)"];
Print["==================================================="];
(* Map rho in [0, L] to t in [-1, 1] via rho = L(1+t)/2 *)
(* This gives better resolution near rho = 0 *)
Do[
  nPts = 200;
  rhoMax = 10.;
  (* Chebyshev points *)
  tj = Table[Cos[Pi j/nPts], {j, 0, nPts}];
  rhoj = rhoMax (1 + tj)/2;
  (* Differentiation matrix *)
  Dmat = Table[
    If[i == j,
      If[i == 0, (2 nPts^2 + 1)/6,
       If[i == nPts, -(2 nPts^2 + 1)/6,
        -tj[[i+1]]/(2 (1 - tj[[i+1]]^2))]],
      (-1)^(i+j) / ((tj[[i+1]] - tj[[j+1]]) *
        If[i == 0 || i == nPts, 2, 1] *
        If[j == 0 || j == nPts, 1/2, 1])
    ],
    {i, 0, nPts}, {j, 0, nPts}
  ];
  D2mat = Dmat . Dmat;
  (* Scale to [0, rhoMax]: d/drho = (2/rhoMax) d/dt *)
  D2rho = (2/rhoMax)^2 D2mat;
  (* Hamiltonian at interior points *)
  interior = Range[2, nPts]; (* skip boundary points *)
  Vdiag = DiagonalMatrix[Table[Log[2 Sinh[rhoj[[i]]]], {i, interior}]];
  Hint = -1/(2 cVal) D2rho[[interior, interior]] + Vdiag;
  evals = Sort[Eigenvalues[N[Hint]]];
  gap = evals[[2]] - evals[[1]];
  Print["c = ", PaddedForm[N[cVal], {8, 1}],
        "  gap(Chebyshev) = ", PaddedForm[gap, {14, 10}]],
  {cVal, {50., 100., 200., 500., 1000.}}
];

Print["\nDONE"];
