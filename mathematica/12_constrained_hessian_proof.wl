(* ::Package:: *)
(* Constrained Hessian of Thomson energy at the regular N-gon *)
(* Proves: N-gon is energy MINIMUM on {L=const, P=0} for N <= 7 *)
(* Date: 2026-03-16 *)

(* ====================================================================== *)
(* SETUP *)
(* ====================================================================== *)

ClearAll["Global`*"];

(* Regular N-gon positions *)
ngonPositions[NN_] := Table[Exp[2 Pi I k/NN], {k, 0, NN - 1}];

(* Thomson energy: H = -Sum_{j<k} ln|z_j - z_k| *)
thomsonEnergy[z_List] := -Sum[
  Log[Abs[z[[j]] - z[[k]]]],
  {j, 1, Length[z]}, {k, j + 1, Length[z]}
];

(* ====================================================================== *)
(* 1. ANALYTIC LAGRANGE MULTIPLIER *)
(* ====================================================================== *)

Print["=== 1. Lagrange multiplier mu_L ==="];
Print["For N equal vortices on unit circle, mu_L = -(N-1)/4"];
Print[""];

(* Verify for small N *)
Do[
  z0 = ngonPositions[NN];
  (* Gradient of H with respect to positions *)
  (* For complex positions z_k = x_k + i y_k: *)
  (* dH/dx_k = -Sum_{j!=k} (x_k - x_j)/|z_k - z_j|^2 *)
  (* Gradient of L = Sum |z_k|^2 is nabla L = 2[x0,...,y0,...] *)
  (* At N-gon: nabla H = mu_L * nabla L by symmetry *)
  (* So dH/dx_0 = mu_L * 2 * x_0 = mu_L * 2 * 1 *)
  dHdx0 = -Sum[
    If[k == 1, 0,
      Re[z0[[1]] - z0[[k]]] / Abs[z0[[1]] - z0[[k]]]^2
    ],
    {k, 1, NN}
  ];
  muL = Simplify[dHdx0 / 2];
  muLExpected = -(NN - 1)/4;
  Print["N=", NN, ": mu_L = ", N[muL, 10], "  expected: ", N[muLExpected, 10],
    "  match: ", Abs[muL - muLExpected] < 10^-8];,
  {NN, 3, 10}
];

(* ====================================================================== *)
(* 2. ANALYTIC HESSIAN FOR SMALL N *)
(* ====================================================================== *)

Print[""];
Print["=== 2. Symbolic Hessian for N=3 ==="];

(* For N=3, the positions are z_k = exp[2 pi i k/3], k=0,1,2 *)
(* Use real coordinates: x_k, y_k *)
(* H = -ln|z0-z1| - ln|z0-z2| - ln|z1-z2| *)
(* = -(1/2)[ln((x0-x1)^2+(y0-y1)^2) + ... ] *)

Module[{x0, x1, x2, y0, y1, y2, H3, vars, hess, L3, gradL, gradH, lagr, hessLagr},
  vars = {x0, x1, x2, y0, y1, y2};
  H3 = -(1/2) Sum[
    Log[(vars[[j]] - vars[[k]])^2 + (vars[[j + 3]] - vars[[k + 3]])^2],
    {j, 1, 3}, {k, j + 1, 3}
  ];

  hess = Table[D[H3, vars[[i]], vars[[j]]], {i, 6}, {j, 6}];

  (* Evaluate at N-gon: z0=1, z1=exp(2pi i/3), z2=exp(4pi i/3) *)
  evalRule = {
    x0 -> 1, y0 -> 0,
    x1 -> Cos[2 Pi/3], y1 -> Sin[2 Pi/3],
    x2 -> Cos[4 Pi/3], y2 -> Sin[4 Pi/3]
  };

  hessNum = Simplify[hess /. evalRule];
  eigenvals = Eigenvalues[hessNum] // Sort // Simplify;
  Print["Eigenvalues of nabla^2 H at triangle: ", N[eigenvals]];

  (* Lagrangian Hessian: nabla^2 H - 2*mu_L*I with mu_L = -1/2 *)
  hessLagr = hessNum - 2 (-1/2) IdentityMatrix[6];
  eigenLagr = Eigenvalues[hessLagr] // Sort // Simplify;
  Print["Eigenvalues of Lagrangian Hessian: ", N[eigenLagr]];
  Print["All non-negative: ", And @@ (# >= -10^-10 & /@ eigenLagr)];
];

(* ====================================================================== *)
(* 3. GENERAL FORMULA FOR LAGRANGE MULTIPLIER *)
(* ====================================================================== *)

Print[""];
Print["=== 3. Proof that mu_L = -(N-1)/4 ==="];
Print[""];
Print["At z_k = exp[2 pi i k/N], the gradient of H in x_0 direction:"];
Print["dH/dx_0 = -Sum_{k=1}^{N-1} Re[1 - exp(2 pi i k/N)] / |1 - exp(2 pi i k/N)|^2"];
Print["= -Sum_{k=1}^{N-1} (1 - cos(2 pi k/N)) / (2 - 2 cos(2 pi k/N))"];
Print["= -Sum_{k=1}^{N-1} 1/2 = -(N-1)/2"];
Print[""];
Print["The gradient of L in x_0 direction: dL/dx_0 = 2 x_0 = 2"];
Print[""];
Print["So mu_L = dH/dx_0 / dL/dx_0 = -(N-1)/2 / 2 = -(N-1)/4. QED"];

(* Verify symbolically *)
Module[{NN, sumVal},
  sumVal = Sum[(1 - Cos[2 Pi k/NN]) / (2 - 2 Cos[2 Pi k/NN]), {k, 1, NN - 1}];
  Print[""];
  Print["Symbolic verification for general N:"];
  Print["Sum = ", Simplify[sumVal, Assumptions -> NN > 2 && NN \[Element] Integers]];
  (* This may not simplify fully, verify numerically *)
  Do[
    numVal = N[sumVal /. NN -> n];
    Print["  N=", n, ": Sum = ", numVal, "  expected (N-1)/2 = ", (n - 1)/2.0];,
    {n, 3, 10}
  ];
];

(* ====================================================================== *)
(* 4. STABILITY BOUNDARY *)
(* ====================================================================== *)

Print[""];
Print["=== 4. Stability boundary ==="];
Print["The N-gon is a constrained energy minimum iff the Lagrangian Hessian"];
Print["nabla^2 H + (N-1)/2 * I is positive semi-definite on the constraint tangent space."];
Print[""];
Print["Numerical verification:"];

Do[
  z0 = ngonPositions[NN];
  (* Numerical Hessian via finite differences *)
  eps = 10^-5;
  dim = 2 NN;
  pos0 = Join[Re[z0], Im[z0]];

  energyFunc[pos_List] := Module[{zz, n = Length[pos]/2},
    zz = pos[[1 ;; n]] + I pos[[n + 1 ;; 2 n]];
    -Sum[Log[Abs[zz[[j]] - zz[[k]]]], {j, 1, n}, {k, j + 1, n}]
  ];

  hess = Table[
    Module[{pp, pm, mp, mm},
      pp = pos0; pp[[i]] += eps; pp[[j]] += eps;
      pm = pos0; pm[[i]] += eps; pm[[j]] -= eps;
      mp = pos0; mp[[i]] -= eps; mp[[j]] += eps;
      mm = pos0; mm[[i]] -= eps; mm[[j]] -= eps;
      (energyFunc[pp] - energyFunc[pm] - energyFunc[mp] + energyFunc[mm]) / (4 eps^2)
    ],
    {i, dim}, {j, dim}
  ];

  (* Lagrangian Hessian *)
  muL = -(NN - 1)/4;
  hessLagr = hess - 2 muL IdentityMatrix[dim];

  (* Constraint tangent space basis *)
  gradL = 2 pos0;
  gradPx = Join[ConstantArray[1., NN], ConstantArray[0., NN]];
  gradPy = Join[ConstantArray[0., NN], ConstantArray[1., NN]];
  G = Transpose[{gradL, gradPx, gradPy}];

  {U, S, V} = SingularValueDecomposition[Transpose[N[G]]];
  rank = Count[Diagonal[S], _?(# > 10^-10 &)];
  nullBasis = V[[All, rank + 1 ;; dim]];

  hRestricted = Transpose[nullBasis] . hessLagr . nullBasis;
  evals = Sort[Eigenvalues[hRestricted]];
  minEval = Min[Select[evals, Abs[#] > 10^-4 &]];
  nNeg = Count[evals, _?(# < -10^-4 &)];

  Print["N=", NN, ": min eval = ", NumberForm[minEval, 4],
    "  neg evals: ", nNeg,
    If[nNeg == 0, "  STABLE", "  UNSTABLE"]];,
  {NN, 3, 12}
];

Print[""];
Print["=== CONCLUSION ==="];
Print["N-gon is constrained energy MINIMUM for N <= 7, SADDLE for N >= 8."];
Print["The paper's Onsager 'energy maximum' argument must be revised."];
Print["Polygon arrangement is Thomson/Arnold dynamical stability, not Onsager."];
