(* Mass gap: CORRECT approach using NDEigensystem in ORIGINAL coordinates *)
(* with VERY fine mesh concentrated near rho=0. *)
(*  *)
(* The issue with all previous attempts:  *)
(* - Original FEM (v4): converged at c=67 (gap=0.809) but NOT at c>100 *)
(* - Regularized (spectral): WRONG transformation (missed e^{2t} weight) *)
(* - Shooting: WRONG boundary condition (oscillatory regime at rho=0) *)
(*  *)
(* The CORRECT approach: use the original FEM with a NON-UNIFORM mesh *)
(* that has fine spacing near rho=0 and coarse spacing far away. *)
(* Mathematica's ToElementMesh allows explicit mesh specification. *)

Needs["NDSolve`FEM`"];

V[rho_] := Log[2 Sinh[rho]];

(* Build a non-uniform mesh concentrated near rho=0 *)
buildMesh[rhoMin_, rhoMax_, nPts_] := Module[
  {coords, elements, mesh},
  (* Use geometric spacing: denser near rhoMin *)
  coords = Table[
    rhoMin + (rhoMax - rhoMin) (i/nPts)^2,  (* quadratic concentration *)
    {i, 0, nPts}
  ];
  (* Convert to ToElementMesh format *)
  mesh = ToElementMesh[
    "Coordinates" -> Partition[coords, 1],
    "MeshElements" -> {LineElement[
      Table[{i, i + 1}, {i, Length[coords] - 1}]
    ]}
  ];
  mesh
];

solveWithMesh[cVal_?NumericQ, rhoMin_: 0.0001, rhoMax_: 12., nPts_: 5000] := Module[
  {mesh, evals, efuncs},
  mesh = buildMesh[rhoMin, rhoMax, nPts];
  {evals, efuncs} = NDEigensystem[
    {-1./(2. cVal) Derivative[2][u][x] + Log[2. Sinh[x]] u[x],
     DirichletCondition[u[x] == 0, True]},
    u[x], {x} \[Element] mesh, 5
  ];
  Sort[Re[evals]]
];

(* Part 1: Validate at c = 67 (N=8) where FEM gave 0.809 *)
Print["VALIDATION at c = 67 (N=8)"];
Print["=============================="];
c8 = 12. (8.*9./12. - Log[2.] + Log[8.]/7.);
Print["c = ", c8];
Print[];

(* Test convergence in nPts *)
Do[
  ev = solveWithMesh[c8, 0.0001, 12., nPts];
  gap = ev[[2]] - ev[[1]];
  Print["nPts = ", PaddedForm[nPts, {6,0}],
        "  E0 = ", PaddedForm[ev[[1]], {14,8}],
        "  E1 = ", PaddedForm[ev[[2]], {14,8}],
        "  gap = ", PaddedForm[gap, {14,10}]],
  {nPts, {500, 1000, 2000, 5000, 10000}}
];

(* Test convergence in rhoMin *)
Print[];
Print["Convergence in rhoMin (nPts = 5000):"];
Do[
  ev = solveWithMesh[c8, rMin, 12., 5000];
  gap = ev[[2]] - ev[[1]];
  Print["rMin = ", PaddedForm[rMin, {12,8}],
        "  E0 = ", PaddedForm[ev[[1]], {14,8}],
        "  gap = ", PaddedForm[gap, {14,10}]],
  {rMin, {0.01, 0.001, 0.0001, 0.00001, 0.000001}}
];

(* Part 2: The target — c = 127 (N=11) *)
Print[];
Print["TARGET at c = 127 (N=11)"];
Print["==========================="];
c11 = 12. (11.*12./12. - Log[2.] + Log[11.]/10.);
Print["c = ", c11];
Print[];

Do[
  ev = solveWithMesh[c11, rMin, 12., 5000];
  gap = ev[[2]] - ev[[1]];
  Print["rMin = ", PaddedForm[rMin, {12,8}],
        "  E0 = ", PaddedForm[ev[[1]], {14,8}],
        "  E1 = ", PaddedForm[ev[[2]], {14,8}],
        "  gap = ", PaddedForm[gap, {14,10}]],
  {rMin, {0.01, 0.001, 0.0001, 0.00001, 0.000001}}
];

(* Part 3: All physical N values with best settings *)
Print[];
Print["ALL PHYSICAL N VALUES (rMin=10^-5, nPts=5000)"];
Print["================================================="];
Do[
  cPhys = N[12. (nn*(nn+1.)/12. - Log[2.] + Log[N[nn]]/(nn-1.))];
  ev = solveWithMesh[cPhys, 0.00001, 12., 5000];
  If[Length[ev] >= 2,
    gap = ev[[2]] - ev[[1]];
    Print["N = ", PaddedForm[nn, {3,0}],
          "  c = ", PaddedForm[cPhys, {10,2}],
          "  E0 = ", PaddedForm[ev[[1]], {12,6}],
          "  E1 = ", PaddedForm[ev[[2]], {12,6}],
          "  gap = ", PaddedForm[gap, {12,8}]],
    Print["N = ", nn, " FAILED"]
  ],
  {nn, {6, 7, 8, 9, 10, 11, 12, 14, 16, 20}}
];

Print[];
Print["DONE"];
