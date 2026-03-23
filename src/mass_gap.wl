(* Mass Gap of the WDW Equation: V(rho) = Log[2 Sinh[rho]] *)
(* Solve: -1/(2c) psi''[rho] + V[rho] psi[rho] == E psi[rho] *)

V[rho_] := Log[2 Sinh[rho]];

(* Use NDEigensystem with explicit numeric c *)
solveWDW[cVal_?NumericQ, nStates_Integer: 3] := Module[
  {evals, efuncs, rMax = 15},
  {evals, efuncs} = NDEigensystem[
    {-1/(2 cVal) u''[x] + Log[2 Sinh[x]] u[x],
     DirichletCondition[u[x] == 0, True]},
    u[x], {x, 0.005, rMax}, nStates,
    Method -> {"PDEDiscretization" -> {"FiniteElement",
      "MeshOptions" -> {"MaxCellMeasure" -> 0.008}}}
  ];
  Sort[evals]
];

(* Part 1: Gap vs c *)
Print["MASS GAP vs c"];
Print["============="];
gapList = {};
Do[
  ev = solveWDW[cVal, 3];
  gap = ev[[2]] - ev[[1]];
  AppendTo[gapList, {cVal, gap}];
  Print["c = ", PaddedForm[N[cVal], {8, 1}],
        "  E0 = ", PaddedForm[ev[[1]], {12, 6}],
        "  E1 = ", PaddedForm[ev[[2]], {12, 6}],
        "  gap = ", PaddedForm[gap, {12, 8}]],
  {cVal, {20., 40., 60., 80., 100., 150., 200., 300., 400., 500., 700., 1000., 2000., 5000.}}
];

(* Part 2: Find minimum gap *)
Print["\nFINDING MINIMUM GAP"];
gapFn[cVal_?NumericQ] := Module[{ev},
  ev = solveWDW[cVal, 2];
  ev[[2]] - ev[[1]]
];

result = FindMinimum[gapFn[cc], {cc, 250, 100, 600}];
gMin = result[[1]];
cAtMin = cc /. result[[2]];
Print["Minimum gap = ", InputForm[gMin]];
Print["at c = ", InputForm[cAtMin]];

(* Part 3: Candidates *)
Print["\nCANDIDATE EXACT VALUES (sorted by closeness to min gap)"];
cands = {
  {"Sqrt[2/3]", Sqrt[2/3]},
  {"Tanh[1]", Tanh[1]},
  {"Sqrt[Log[2]]", Sqrt[Log[2]]},
  {"Log[2]+1/8", Log[2] + 1/8},
  {"4/5", 4/5},
  {"1-1/(2E)", 1 - 1/(2 E)},
  {"2Tanh[1/2]", 2 Tanh[1/2]},
  {"Coth[1]-Csch[1]", Coth[1] - Csch[1]},
  {"Sqrt[2/Pi]", Sqrt[2/Pi]},
  {"Log[2Sinh[1]]", Log[2 Sinh[1]]},
  {"1/Cosh[1]", Sech[1]},
  {"V[1]=Log[2Sinh[1]]", Log[2 Sinh[1]]},
  {"Sqrt[V[1]]", Sqrt[Log[2 Sinh[1]]]},
  {"Pi/4", Pi/4},
  {"2/Pi+1/2", 2/Pi + 1/2}
};
cands = SortBy[cands, Abs[N[#[[2]]] - gMin] &];
Do[
  Print[PaddedForm[c[[1]], {25, 0}], "  = ",
        PaddedForm[N[c[[2]], 12], {14, 10}], "  diff = ",
        PaddedForm[N[c[[2]] - gMin, 8], {12, 6}]],
  {c, cands}
];

(* Part 4: Physical c values *)
Print["\nGAP AT PHYSICAL N VALUES"];
Do[
  cPhys = N[12 (nn (nn + 1)/12 - Log[2] + Log[nn]/(nn - 1))];
  ev = solveWDW[cPhys, 3];
  gap = ev[[2]] - ev[[1]];
  Print["N = ", PaddedForm[nn, {3, 0}],
        "  c = ", PaddedForm[cPhys, {10, 2}],
        "  gap = ", PaddedForm[gap, {12, 8}]],
  {nn, {6, 7, 8, 10, 12, 14, 16, 20}}
];

(* Part 5: Transcendental tests at the minimum *)
Print["\nTRANSCENDENTAL TESTS at g = ", InputForm[gMin]];
g = gMin;
Print["V(g) = ", InputForm[N[V[g], 15]]];
Print["V'(g) = Coth(g) = ", InputForm[N[Coth[g], 15]]];
Print["g^2 = ", InputForm[N[g^2, 15]]];
Print["V(g)/g = ", InputForm[N[V[g]/g, 15]]];
Print["g Coth(g) = ", InputForm[N[g Coth[g], 15]]];
Print["g Coth(g) - 1 = ", InputForm[N[g Coth[g] - 1, 15]]];
Print["2V(g) - g^2 = ", InputForm[N[2 V[g] - g^2, 15]]];
Print["V(g) - g^2/2 = ", InputForm[N[V[g] - g^2/2, 15]]];
Print["Exp(g) = ", InputForm[N[Exp[g], 15]]];
Print["2Sinh(g) = ", InputForm[N[2 Sinh[g], 15]]];

Print["\nDONE"];
