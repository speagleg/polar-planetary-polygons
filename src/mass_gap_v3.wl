(* Mass Gap v3: Chebyshev spectral method only (trustworthy) *)
(* Push to large c to find the asymptotic limit *)

V[rho_] := Log[2 Sinh[rho]];

(* Chebyshev collocation on [rMin, rMax] *)
chebyshevGap[cVal_?NumericQ, nPts_Integer: 300, rMax_?NumericQ: 12.] := Module[
  {tj, rhoj, Dmat, D2mat, D2rho, interior, Vdiag, Hint, evals, ci, cj, rMin = 0.001},
  (* Chebyshev points *)
  tj = Table[N[Cos[Pi j/nPts], 20], {j, 0, nPts}];
  rhoj = rMin + (rMax - rMin) (1 + tj)/2;
  (* Differentiation matrix *)
  Dmat = Table[
    Which[
      i == j && i == 0, (2 nPts^2 + 1)/6.,
      i == j && i == nPts, -(2 nPts^2 + 1)/6.,
      i == j, -tj[[i+1]]/(2. (1 - tj[[i+1]]^2)),
      True,
        ci = If[i == 0 || i == nPts, 2., 1.];
        cj = If[j == 0 || j == nPts, 2., 1.];
        (-1.)^(i+j) ci / (cj (tj[[i+1]] - tj[[j+1]]))
    ],
    {i, 0, nPts}, {j, 0, nPts}
  ];
  D2mat = Dmat . Dmat;
  (* Scale derivatives to physical domain *)
  D2rho = (2./(rMax - rMin))^2 D2mat;
  (* Interior points (skip boundaries where u = 0) *)
  interior = Range[2, nPts];
  Vdiag = DiagonalMatrix[Table[N[Log[2 Sinh[rhoj[[i]]]], 20], {i, interior}]];
  Hint = -1./(2 cVal) D2rho[[interior, interior]] + Vdiag;
  evals = Sort[Eigenvalues[Hint]];
  (* Return first 4 eigenvalues *)
  evals[[1 ;; Min[4, Length[evals]]]]
];

(* Part 1: Gap vs c, extended to very large c *)
Print["CHEBYSHEV MASS GAP (300 points)"];
Print["================================"];
Print["c           E0            E1            gap           gap*c^(1/3)"];
gapData = {};
Do[
  ev = chebyshevGap[cVal, 300, 12.];
  gap = Re[ev[[2]] - ev[[1]]];
  AppendTo[gapData, {cVal, gap}];
  Print[PaddedForm[N[cVal], {8, 0}], "  ",
        PaddedForm[Re[ev[[1]]], {14, 8}], "  ",
        PaddedForm[Re[ev[[2]]], {14, 8}], "  ",
        PaddedForm[gap, {14, 10}], "  ",
        PaddedForm[gap cVal^(1/3), {12, 6}]],
  {cVal, {30., 50., 75., 100., 150., 200., 300., 500., 750.,
          1000., 1500., 2000., 3000., 5000., 10000., 20000.}}
];

(* Part 2: Extrapolate the asymptotic limit *)
Print["\nASYMPTOTIC EXTRAPOLATION"];
Print["========================"];
(* Fit gap = a + b/c^alpha for the last several points *)
(* Try alpha = 1/3 (Airy), 1/2, 2/3, 1 *)
Do[
  pts = Select[gapData, #[[1]] >= 500 &];
  fitData = {1/#[[1]]^alpha, #[[2]]} & /@ pts;
  fit = Fit[fitData, {1, x}, x];
  aInf = fit /. x -> 0;
  Print["alpha = ", PaddedForm[alpha, {4, 2}],
        "  gap(inf) = ", PaddedForm[aInf, {14, 10}],
        "  4/5 = ", PaddedForm[4./5, {14, 10}],
        "  diff = ", PaddedForm[aInf - 4./5, {12, 6}]],
  {alpha, {1/3., 1/2., 2/3., 1.}}
];

(* Part 3: Check specific exact candidates *)
Print["\nCANDIDATES vs gap at c = 10000"];
lastGap = gapData[[-1, 2]];
Print["Gap at largest c: ", InputForm[lastGap]];
cands = {
  {"4/5", 4./5},
  {"Sqrt[2/Pi]", Sqrt[2./Pi]},
  {"Pi/4", Pi/4.},
  {"Log[2Sinh[1]]", Log[2. Sinh[1.]]},
  {"Sqrt[2/3]", Sqrt[2./3]},
  {"Tanh[1]", Tanh[1.]},
  {"3/4", 3./4},
  {"1-1/Pi", 1. - 1./Pi},
  {"2-Sqrt[Pi]", 2. - Sqrt[Pi]},
  {"Sqrt[V'(1)^2-1]", Sqrt[Coth[1.]^2 - 1.]},
  {"Csch[1]", 1./Sinh[1.]},
  {"(Sqrt[5]-1)/2", (Sqrt[5.] - 1)/2},
  {"Log[Coth[1/2]]", Log[Coth[0.5]]},
  {"1/(2Sinh[1])", 1./(2 Sinh[1.])}
};
cands = SortBy[cands, Abs[#[[2]] - lastGap] &];
Do[
  Print[PaddedForm[c[[1]], {20, 0}], "  = ",
        PaddedForm[c[[2]], {14, 10}], "  diff = ",
        PaddedForm[c[[2]] - lastGap, {12, 8}]],
  {c, cands}
];

(* Part 4: Physical N values with Chebyshev *)
Print["\nPHYSICAL N VALUES (Chebyshev, 300 pts)"];
Do[
  cPhys = N[12 (nn (nn + 1)/12 - Log[2] + Log[nn]/(nn - 1))];
  ev = chebyshevGap[cPhys, 300, 12.];
  gap = Re[ev[[2]] - ev[[1]]];
  Print["N = ", PaddedForm[nn, {3, 0}],
        "  c = ", PaddedForm[cPhys, {10, 2}],
        "  gap = ", PaddedForm[gap, {14, 10}]],
  {nn, {6, 7, 8, 10, 12, 14, 16, 20, 30}}
];

Print["\nDONE"];
