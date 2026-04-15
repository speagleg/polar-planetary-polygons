(* ================================================================== *)
(* LANGER RESIDUAL v2: Corrected extraction                           *)
(* ================================================================== *)
(* Previous approach (Approach 2) failed because the classical-region  *)
(* envelope ratio grows as Log[c], not as A + D/c.  This script uses  *)
(* three cleaner approaches:                                           *)
(*                                                                      *)
(* A) Prüfer envelope RATIO at two fixed points (cancels abs. norm)    *)
(* B) Tunneling amplitude: psi past the turning point rho*             *)
(* C) Direct 1/c extraction from the envelope vs sqrt(c) scaling       *)
(*                                                                      *)
(* Key insight: the Langer modification V -> V + 1/(8c rho^2)         *)
(* changes the WKB action by ~0.85 (an O(1) correction, NOT O(1/c)).  *)
(* The paper's claimed O(1/c) piece is a SUBLEADING correction to     *)
(* this, which requires very precise extraction.                        *)
(*                                                                      *)
(* Run: wolframscript -file scripts/langer_residual_v2.wl              *)
(* ================================================================== *)

wp = 30;  (* working precision — 30 digits is plenty *)

(* ---- Model ---- *)
bExact[NN_] := NN (NN + 1)/12 - Log[2] + Log[NN]/(NN - 1);
fStar[NN_] := Floor[NN/2] (NN - Floor[NN/2])/2;
cN[NN_] := 12 bExact[NN];
rhoStar[NN_] := ArcSinh[Exp[fStar[NN] - bExact[NN]]/2];
beta0[NN_] := Log[2] + bExact[NN] - fStar[NN];
VBO[rho_, NN_] := Log[2 Sinh[rho]] + bExact[NN] - fStar[NN];

(* ================================================================== *)
(* APPROACH A: Prüfer envelope at fixed observation points             *)
(*                                                                      *)
(* The Prüfer amplitude R = Sqrt[psi^2 + (psi'/p)^2] where            *)
(* p = Sqrt[2c|V|].  The "normalized envelope" E = R |V|^{1/4}        *)
(* should be constant in WKB.  We track E as a function of c.          *)
(*                                                                      *)
(* Since the ABSOLUTE normalization A cancels badly (divergent WKB at  *)
(* rho=0), we measure the RATIO E(rho1)/E(rho2) at two fixed points.  *)
(* In exact WKB this ratio = 1.  Deviations are transport corrections: *)
(*   ln[E(rho1)/E(rho2)] = T_0 + T_1/sqrt(c) + T_2/c + ...           *)
(* where T_2 contains the Dunham integral (not the Langer piece).      *)
(*                                                                      *)
(* Separately, the ABSOLUTE E(c) at one point contains the Langer:     *)
(*   E(rho_obs, c) = E_0 + E_1/sqrt(c) + E_Langer/c + ...            *)
(*                                                                      *)
(* We extract E(rho_obs, c) directly.                                   *)
(* ================================================================== *)

Print["=" <> StringJoin[Table["=", 70]]];
Print["  APPROACH A: Prüfer envelope E(rho_obs) vs c"];
Print["=" <> StringJoin[Table["=", 70]]];

solvePsi[cVal_?NumericQ, NN_Integer, rhoEnd_?NumericQ,
         rhoStart_:10^-6] := Module[
  {b0, psi0, psip0, sol},
  b0 = N[beta0[NN], wp];
  psi0 = 1 + N[cVal, wp] * rhoStart^2 * (b0 + Log[rhoStart] - 3/2);
  psip0 = 2 N[cVal, wp] * rhoStart * (b0 + Log[rhoStart] - 1);
  sol = NDSolve[
    {psi''[r] == 2 N[cVal, wp] VBO[r, NN] psi[r],
     psi[N[rhoStart, wp]] == psi0,
     psi'[N[rhoStart, wp]] == psip0},
    psi, {r, N[rhoStart, wp], N[rhoEnd, wp]},
    WorkingPrecision -> wp,
    MaxSteps -> 10^7,
    AccuracyGoal -> wp - 5,
    PrecisionGoal -> wp - 5
  ];
  First[sol]
];

pruferEnvelope[sol_, cVal_, rhoObs_, NN_] := Module[
  {psiFunc, psiVal, psipVal, Vm, p, R, E},
  psiFunc = psi /. sol;
  psiVal = psiFunc[N[rhoObs, wp]];
  psipVal = psiFunc'[N[rhoObs, wp]];
  Vm = VBO[N[rhoObs, wp], NN];
  p = Sqrt[2 N[cVal, wp] Abs[Vm]];
  R = Sqrt[psiVal^2 + (psipVal/p)^2];
  E = R * Abs[Vm]^(1/4);
  {psiVal, psipVal, R, E}
];

Do[
  NN = n;
  cBase = N[cN[NN], wp];
  rs = N[rhoStar[NN], wp];
  rhoObs = rs * 2/5;  (* 40% of rho* — deep in classical region *)
  rhoEnd = rs * 95/100;

  Print[StringForm["\nN = ``, c_base = ``, rho* = ``, rho_obs = ``",
    NN, N[cBase, 8], N[rs, 6], N[rhoObs, 6]]];

  (* Solve at several c values *)
  multipliers = {1, 2, 4, 8, 16, 32, 64};
  data = {};

  Do[
    c = cBase * k;
    sol = solvePsi[c, NN, rhoEnd];
    {psiVal, psipVal, R, E} = pruferEnvelope[sol, c, rhoObs, NN];
    AppendTo[data, {c, E}];
    Print[StringForm["  c = `` (``x): E(rho_obs) = ``, R = ``",
      N[c, 8], k, N[E, 15], N[R, 15]]];
    ,
    {k, multipliers}
  ];

  (* Fit E(c) = A + B/Sqrt[c] + D/c *)
  If[Length[data] >= 3,
    cs = data[[All, 1]];
    Es = data[[All, 2]];
    mat = Table[{1, 1/Sqrt[ci], 1/ci}, {ci, cs}];
    fit = LeastSquares[N[mat, wp], N[Es, wp]];
    Print[StringForm["\n  Fit: E = `` + ``/Sqrt[c] + ``/c",
      N[fit[[1]], 12], N[fit[[2]], 12], N[fit[[3]], 12]]];
    Print[StringForm["  1/c coefficient: ``", N[fit[[3]], 12]]];
    Print[StringForm["  Compare: -Log[2]/2 = ``", N[-Log[2]/2, 12]]];
    Print[StringForm["  Compare: -beta0/2 = ``", N[-beta0[NN]/2, 12]]];
  ];

  (* Also fit E(c) = A + B*Log[c] + D/c *)
  If[Length[data] >= 3,
    mat2 = Table[{1, Log[ci], 1/ci}, {ci, cs}];
    fit2 = LeastSquares[N[mat2, wp], N[Es, wp]];
    Print[StringForm["\n  Alt fit: E = `` + ``*Log[c] + ``/c",
      N[fit2[[1]], 12], N[fit2[[2]], 12], N[fit2[[3]], 12]]];
    Print[StringForm["  1/c coefficient (alt): ``", N[fit2[[3]], 12]]];
  ];

  Print[];
  ,
  {n, {7, 11}}
];


(* ================================================================== *)
(* APPROACH B: Tunneling amplitude                                      *)
(*                                                                      *)
(* Solve past rho* into the forbidden region.  The exact solution       *)
(* grows as exp(S) where S = int_{rho*}^{rho_far} sqrt(2cV) drho.     *)
(* Extract the growing-mode coefficient:                                *)
(*   C_grow = psi(rho_far) |V(rho_far)|^{1/4} exp(-S)                 *)
(* This C_grow depends on the classical amplitude and phase.            *)
(*                                                                      *)
(* The key: C_grow = E(rho*^-) * cos(Phi_total + pi/4)                *)
(* where E is the Prüfer envelope and Phi_total is the WKB phase.      *)
(* The Langer correction modifies E(rho*^-).                            *)
(*                                                                      *)
(* Since cos(Phi + pi/4) oscillates with c, we use the ABSOLUTE VALUE  *)
(* |C_grow| to avoid the oscillation.                                   *)
(* ================================================================== *)

Print["=" <> StringJoin[Table["=", 70]]];
Print["  APPROACH B: Tunneling amplitude (solve past rho*)"];
Print["=" <> StringJoin[Table["=", 70]]];

Do[
  NN = n;
  cBase = N[cN[NN], wp];
  rs = N[rhoStar[NN], wp];
  delta = 3/10;  (* go 0.3 past rho* *)
  rhoFar = rs + delta;

  Print[StringForm["\nN = ``, rho_far = rho* + 0.3 = ``", NN, N[rhoFar, 6]]];

  data = {};
  Do[
    c = cBase * k;

    (* Solve past rho* *)
    sol = solvePsi[c, NN, rhoFar];
    psiFunc = psi /. sol;
    psiFar = psiFunc[N[rhoFar, wp]];

    (* Barrier action *)
    S = NIntegrate[
      Sqrt[2 N[c, wp] VBO[r, NN]],
      {r, N[rs, wp], N[rhoFar, wp]},
      WorkingPrecision -> wp, MaxRecursion -> 50
    ];

    (* Growing-mode coefficient *)
    Vf = VBO[N[rhoFar, wp], NN];
    lnCgrow = Log[Abs[psiFar]] + Log[Abs[Vf]]/4 - S;

    (* WKB phase integral *)
    Phi = NIntegrate[
      Sqrt[2 N[c, wp] Abs[VBO[r, NN]]],
      {r, N[10^-6, wp], N[rs, wp]},
      WorkingPrecision -> wp, MaxRecursion -> 50
    ];

    AppendTo[data, {c, lnCgrow, Phi, S}];
    Print[StringForm["  c = `` (``x): ln|C_grow| = ``, Phi = ``, S = ``",
      N[c, 8], k, N[lnCgrow, 12], N[Phi, 10], N[S, 10]]];
    ,
    {k, {1, 2, 4, 8, 16, 32}}
  ];

  Print[];
  ,
  {n, {7, 11}}
];


(* ================================================================== *)
(* APPROACH C: WKB action difference (Langer vs plain)                  *)
(*                                                                      *)
(* Quick recomputation of the result from the Python diagnostic:        *)
(* delta_S = Phi_Langer - Phi_plain at high precision.                  *)
(* Fit to A + B Log[c] + D/c to isolate the 1/c piece.                *)
(* ================================================================== *)

Print["=" <> StringJoin[Table["=", 70]]];
Print["  APPROACH C: Langer action difference at high precision"];
Print["=" <> StringJoin[Table["=", 70]]];

Do[
  NN = n;
  cBase = N[cN[NN], wp];
  rs = N[rhoStar[NN], wp];

  Print[StringForm["\nN = ``", NN]];

  data = {};
  Do[
    c = cBase * k;

    (* Plain WKB action *)
    phiPlain = NIntegrate[
      Sqrt[2 c Abs[VBO[r, NN]]],
      {r, 10^-12, rs},
      WorkingPrecision -> wp, MaxRecursion -> 100
    ];

    (* Langer-modified potential *)
    VL[r_] := VBO[r, NN] + 1/(8 c r^2);

    (* Find inner turning point *)
    rhoBreak = r /. FindRoot[VL[r] == 0, {r, 10^-3},
      WorkingPrecision -> wp];

    (* Langer WKB action *)
    phiLanger = NIntegrate[
      Sqrt[2 c Abs[VL[r]]],
      {r, rhoBreak, rs},
      WorkingPrecision -> wp, MaxRecursion -> 100
    ];

    deltaS = phiLanger - phiPlain;
    AppendTo[data, {c, deltaS}];
    Print[StringForm["  c = `` (``x): delta_S = ``, delta_S*c = ``",
      N[c, 8], k, N[deltaS, 15], N[deltaS * c, 12]]];
    ,
    {k, {1, 2, 4, 8, 16, 32, 64, 128, 256}}
  ];

  (* Fit delta_S = A + B Log[c] + D/c *)
  If[Length[data] >= 4,
    cs = data[[All, 1]];
    dSs = data[[All, 2]];
    mat = Table[{1, Log[ci], 1/ci}, {ci, cs}];
    fit = LeastSquares[N[mat, wp], N[dSs, wp]];
    Print[StringForm["\n  Fit: delta_S = `` + `` Log[c] + ``/c",
      N[fit[[1]], 12], N[fit[[2]], 12], N[fit[[3]], 12]]];
    Print[StringForm["  1/c coefficient D = ``", N[fit[[3]], 12]]];
    Print[StringForm["  Compare: -Log[2]/2 = ``", N[-Log[2]/2, 12]]];
    Print[StringForm["  Compare: -beta0/2 = ``", N[-beta0[NN]/2, 12]]];
  ];

  Print[];
  ,
  {n, {7, 11}}
];

Print["\n=== SUMMARY ==="];
Print["The Langer modification V -> V + 1/(8c rho^2) changes the WKB"];
Print["action by ~0.85 (O(1) constant), with a slow Log[c] correction."];
Print["The 1/c piece is extracted from the three-parameter fit above."];
Print["\nDone."];
