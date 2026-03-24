(* Mass gap via SHOOTING METHOD — the most robust 1D approach *)
(* No coordinate transformation, no FEM boundary issues. *)
(* Directly integrates -ψ''/(2c) + V(ρ)ψ = Eψ from both *)
(* ends and matches at a midpoint. *)

V[rho_] := Log[2 Sinh[rho]];

(* For a given energy E and mass c, integrate from left and right *)
(* and find the mismatch in the logarithmic derivative at the match point *)
shootingMismatch[energy_?NumericQ, cVal_?NumericQ, rhoMatch_: 1.0] := Module[
  {solL, solR, rhoMin = 0.0001, rhoMax = 12., psiL, psiR, dpsiL, dpsiR},

  (* Left integration: from rhoMin outward *)
  (* BC: ψ(rhoMin) = rhoMin (linear behavior near 0) *)
  solL = NDSolve[
    {-1/(2 cVal) psi''[rho] + V[rho] psi[rho] == energy psi[rho],
     psi[rhoMin] == rhoMin, psi'[rhoMin] == 1},
    psi, {rho, rhoMin, rhoMatch + 0.01},
    MaxSteps -> 100000, AccuracyGoal -> 12, PrecisionGoal -> 12
  ];

  (* Right integration: from rhoMax inward *)
  (* BC: ψ(rhoMax) ≈ 0, ψ'(rhoMax) = -1 (decaying) *)
  solR = NDSolve[
    {-1/(2 cVal) psi''[rho] + V[rho] psi[rho] == energy psi[rho],
     psi[rhoMax] == 10.^-10, psi'[rhoMax] == -10.^-10},
    psi, {rho, rhoMax, rhoMatch - 0.01},
    MaxSteps -> 100000, AccuracyGoal -> 12, PrecisionGoal -> 12
  ];

  (* Logarithmic derivatives at the match point *)
  psiL = (psi /. solL[[1]])[rhoMatch];
  dpsiL = (psi' /. solL[[1]])[rhoMatch];
  psiR = (psi /. solR[[1]])[rhoMatch];
  dpsiR = (psi' /. solR[[1]])[rhoMatch];

  (* Mismatch = difference of log derivatives *)
  If[Abs[psiL] > 10^-15 && Abs[psiR] > 10^-15,
    dpsiL/psiL - dpsiR/psiR,
    10^10  (* no valid solution *)
  ]
];

(* Find eigenvalues by scanning for sign changes of the mismatch *)
findEigenvalues[cVal_?NumericQ, nEvals_: 4, eMin_: -5., eMax_: 5.] := Module[
  {energies, rhoM, mismatches, signChanges, refinedEvals, i},

  (* Choose match point: near the classical turning point *)
  rhoM = 1.0;

  (* Scan energy range *)
  energies = Table[e, {e, eMin, eMax, (eMax - eMin)/200.}];
  mismatches = Table[
    Quiet[Check[shootingMismatch[e, cVal, rhoM], 10^10]],
    {e, energies}
  ];

  (* Find sign changes *)
  signChanges = {};
  Do[
    If[mismatches[[i]] mismatches[[i + 1]] < 0 &&
       Abs[mismatches[[i]]] < 10^5 && Abs[mismatches[[i + 1]]] < 10^5,
      AppendTo[signChanges, {energies[[i]], energies[[i + 1]]}]
    ],
    {i, Length[mismatches] - 1}
  ];

  (* Refine each eigenvalue by bisection *)
  refinedEvals = {};
  Do[
    {eLo, eHi} = sc;
    Do[
      eMid = (eLo + eHi)/2;
      mLo = Quiet[Check[shootingMismatch[eLo, cVal, rhoM], 10^10]];
      mMid = Quiet[Check[shootingMismatch[eMid, cVal, rhoM], 10^10]];
      If[mLo mMid < 0, eHi = eMid, eLo = eMid],
      {50}  (* 50 bisection steps = ~15 digit precision *)
    ];
    AppendTo[refinedEvals, (eLo + eHi)/2],
    {sc, Take[signChanges, Min[nEvals, Length[signChanges]]]}
  ];

  Sort[refinedEvals]
];

(* Part 1: Test at c = 67 (N=8) where we know the answer *)
Print["SHOOTING METHOD: MASS GAP COMPUTATION"];
Print["========================================"];
Print[];

Print["TEST at c = 67 (N=8): expected gap ≈ 0.809"];
c8 = 12. (8. * 9./12. - Log[2.] + Log[8.]/7.);
Print["c = ", c8];
evals8 = findEigenvalues[c8, 3, -2., 2.];
Print["Eigenvalues: ", evals8];
If[Length[evals8] >= 2,
  Print["Gap = ", evals8[[2]] - evals8[[1]]];
  Print["Expected: 0.809"];
];
Print[];

(* Part 2: The target — c = 127 (N=11) *)
Print["TARGET at c = 127 (N=11): predicted gap = 0.962"];
c11 = 12. (11. * 12./12. - Log[2.] + Log[11.]/10.);
Print["c = ", c11];
evals11 = findEigenvalues[c11, 3, -2., 2.];
Print["Eigenvalues: ", evals11];
If[Length[evals11] >= 2,
  Print["Gap = ", evals11[[2]] - evals11[[1]]];
  Print["Cosmological prediction: 0.962"];
];
Print[];

(* Part 3: Scan all physical N values *)
Print["MASS GAP AT ALL PHYSICAL N VALUES"];
Print["===================================="];
Do[
  cPhys = N[12. (nn (nn + 1.)/12. - Log[2.] + Log[N[nn]]/(nn - 1.))];
  evals = findEigenvalues[cPhys, 3, -3., 3.];
  If[Length[evals] >= 2,
    gap = evals[[2]] - evals[[1]];
    Print["N = ", PaddedForm[nn, {3, 0}],
          "  c = ", PaddedForm[cPhys, {10, 2}],
          "  E0 = ", PaddedForm[evals[[1]], {12, 6}],
          "  E1 = ", PaddedForm[evals[[2]], {12, 6}],
          "  gap = ", PaddedForm[gap, {12, 8}]],
    Print["N = ", nn, "  c = ", cPhys, "  FAILED (no eigenvalues found)"]
  ],
  {nn, {6, 7, 8, 9, 10, 11, 12, 14, 16, 20}}
];

Print[];
Print["DONE"];
