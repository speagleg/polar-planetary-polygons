(* ================================================================== *)
(* LANGER RESIDUAL FOR THE LOG-AIRY EQUATION                          *)
(* ================================================================== *)
(*                                                                      *)
(* Equation: -psi''/(2c) + V(rho) psi = 0                             *)
(*   V(rho) = Log[2 Sinh[rho]] + b(N) - f(m*, N)                      *)
(*                                                                      *)
(* Near rho = 0:  V ~ beta0 + Log[rho],  beta0 = Log[2] + b - f       *)
(*                                                                      *)
(* GOAL: Extract the 1/c coefficient of the tunneling log-amplitude    *)
(* and verify whether it equals -Log[2]/2 (the claimed Langer residual *)
(* from the "2" in "2 Sinh rho").                                       *)
(*                                                                      *)
(* METHOD: Solve the ODE at arbitrary precision using NDSolve with     *)
(* WorkingPrecision -> 50, at several c values, and extract the 1/c    *)
(* coefficient by Richardson extrapolation.                             *)
(*                                                                      *)
(* Run: wolframscript -file scripts/langer_log_airy.wl                 *)
(* ================================================================== *)

Print["=" <> StringJoin[Table["=", 70]]];
Print["  LANGER RESIDUAL: HIGH-PRECISION NUMERICAL EXTRACTION"];
Print["=" <> StringJoin[Table["=", 70]]];

(* ---- Model parameters ---- *)
bExact[NN_] := NN (NN + 1)/12 - Log[2] + Log[NN]/(NN - 1);
fStar[NN_] := Floor[NN/2] (NN - Floor[NN/2])/2;
cN[NN_] := 12 bExact[NN];
rhoStar[NN_] := ArcSinh[Exp[fStar[NN] - bExact[NN]]/2];
beta0[NN_] := Log[2] + bExact[NN] - fStar[NN];

VBO[rho_, NN_] := Log[2 Sinh[rho]] + bExact[NN] - fStar[NN];

(* ---- High-precision ODE solver ---- *)
(* Solve from rho_start to rho_match in the CLASSICAL region *)
(* using the regular solution series seed at rho_start *)

wp = 50;  (* working precision *)

solvePsi[cVal_?NumericQ, NN_Integer, rhoStart_:10^-8,
         rhoEnd_:Automatic] := Module[
  {b0, psi0, psip0, rEnd, sol},

  b0 = N[beta0[NN], wp];

  (* Series seed: psi = 1 + c rho^2 (beta0 + Log[rho] - 3/2) *)
  psi0 = 1 + N[cVal, wp] * rhoStart^2 * (b0 + Log[rhoStart] - 3/2);
  psip0 = 2 N[cVal, wp] * rhoStart * (b0 + Log[rhoStart] - 1);

  rEnd = If[rhoEnd === Automatic, N[rhoStar[NN] * 9/10, wp], N[rhoEnd, wp]];

  sol = NDSolve[
    {psi''[rho] == 2 N[cVal, wp] * VBO[rho, NN] * psi[rho],
     psi[N[rhoStart, wp]] == psi0,
     psi'[N[rhoStart, wp]] == psip0},
    psi, {rho, N[rhoStart, wp], rEnd},
    WorkingPrecision -> wp,
    MaxSteps -> 10^7,
    AccuracyGoal -> wp - 5,
    PrecisionGoal -> wp - 5
  ];

  sol
];

(* ---- WKB phase integral ---- *)
phiWKB[cVal_?NumericQ, NN_Integer, rhoFrom_:10^-8,
       rhoTo_:Automatic] := Module[
  {rEnd},
  rEnd = If[rhoTo === Automatic, N[rhoStar[NN] * 9/10, wp], N[rhoTo, wp]];
  NIntegrate[
    Sqrt[2 cVal * Abs[VBO[rho, NN]]],
    {rho, rhoFrom, rEnd},
    WorkingPrecision -> wp,
    MaxRecursion -> 50
  ]
];

(* ================================================================== *)
(* APPROACH 1: Scaled Prufer angle                                     *)
(*                                                                      *)
(* theta' = Sqrt[|V|] + V'/(4V) Sin[2 theta]                          *)
(*                                                                      *)
(* Integrate theta alongside the ODE, extract delta = theta - Phi_WKB  *)
(* ================================================================== *)

Print["\n--- APPROACH 1: Scaled Prufer phase extraction ---\n"];

solvePrufer[cVal_?NumericQ, NN_Integer] := Module[
  {b0, rhoS, rEnd, psi0, psip0, V0, p0, R0, th0, sol, thEnd, phi},

  rhoS = N[10^-8, wp];
  rEnd = N[rhoStar[NN] * 9/10, wp];
  b0 = N[beta0[NN], wp];

  psi0 = 1 + N[cVal, wp] * rhoS^2 * (b0 + Log[rhoS] - 3/2);
  psip0 = 2 N[cVal, wp] * rhoS * (b0 + Log[rhoS] - 1);
  V0 = N[VBO[rhoS, NN], wp];
  p0 = Sqrt[Abs[V0]];
  R0 = Sqrt[psi0^2 + (psip0/p0)^2];
  th0 = ArcTan[psip0/(p0 R0), psi0/R0];

  sol = NDSolve[
    {y1'[r] == y2[r],
     y2'[r] == 2 N[cVal, wp] VBO[r, NN] y1[r],
     th'[r] == Sqrt[Abs[VBO[r, NN]]] +
               (Cosh[r]/(Sinh[r] * 4 VBO[r, NN])) * Sin[2 th[r]],
     y1[rhoS] == psi0,
     y2[rhoS] == psip0,
     th[rhoS] == th0},
    {y1, y2, th}, {r, rhoS, rEnd},
    WorkingPrecision -> wp,
    MaxSteps -> 10^7,
    AccuracyGoal -> wp - 5,
    PrecisionGoal -> wp - 5
  ];

  thEnd = (th /. First[sol])[rEnd];
  phi = phiWKB[cVal, NN, 10^-8, rEnd];

  {thEnd - th0, phi, thEnd - th0 - phi}
];

(* ================================================================== *)
(* APPROACH 2: Direct amplitude comparison                             *)
(*                                                                      *)
(* At a matching point rho_m in the classical region:                   *)
(*   ln|psi_exact| vs -(1/4) ln|V| + (WKB corrections)                *)
(*                                                                      *)
(* The 1/c part of the difference is the Langer residual.              *)
(* ================================================================== *)

Print["--- APPROACH 2: Amplitude comparison at matching point ---\n"];

(* Solve at several c values and extract 1/c coefficient *)
Do[
  NN = n;
  cBase = N[cN[NN], wp];
  rMatch = N[rhoStar[NN] / 2, wp];

  Print[StringForm["N = ``, c_N = ``, rho* = ``, rho_match = ``",
    NN, N[cBase, 10], N[rhoStar[NN], 8], N[rMatch, 8]]];
  Print[StringForm["  beta0 = ``, predicted residual = -Log[2]/(2c) = ``",
    N[beta0[NN], 10], N[-Log[2]/(2 cBase), 10]]];

  (* Solve at multiples of c_N *)
  multipliers = {1, 2, 4, 8, 16, 32, 64, 128};
  data = {};

  Do[
    c = cBase * k;
    sol = solvePsi[c, NN, 10^-8, rMatch];
    psiVal = (psi /. First[sol])[rMatch];

    (* WKB prediction at matching point *)
    Vm = VBO[rMatch, NN];
    wkbLogAmp = -1/4 Log[Abs[Vm]];
    exactLogAmp = Log[Abs[psiVal]];

    residual = exactLogAmp - wkbLogAmp;
    AppendTo[data, {c, residual}];

    Print[StringForm["  c = `` (``x): ln|psi| = ``, WKB = ``, resid = ``",
      N[c, 8], k, N[exactLogAmp, 15], N[wkbLogAmp, 15], N[residual, 15]]];
    ,
    {k, multipliers}
  ];

  (* Richardson extrapolation: fit residual = A + B/Sqrt[c] + D/c + E/c^{3/2} *)
  (* Using the last 4 data points (largest c, best 1/c isolation) *)
  Print["\n  --- Richardson extrapolation ---"];
  lastData = data[[-4 ;;]];

  (* Fit: residual = a0 + a1/Sqrt[c] + a2/c *)
  mat = Table[{1, 1/Sqrt[d[[1]]], 1/d[[1]]}, {d, lastData}];
  rhs = lastData[[All, 2]];

  (* Least-squares if overdetermined, exact if 3 points *)
  If[Length[lastData] >= 3,
    fit = LeastSquares[mat[[1;;3]], rhs[[1;;3]]];
    Print[StringForm["  Fit: resid = `` + ``/Sqrt[c] + ``/c",
      N[fit[[1]], 12], N[fit[[2]], 12], N[fit[[3]], 12]]];
    Print[StringForm["  1/c coefficient D = ``", N[fit[[3]], 12]]];
    Print[StringForm["  Predicted: -Log[2]/2 = ``", N[-Log[2]/2, 12]]];
    Print[StringForm["  Ratio D/(-Log[2]/2) = ``", N[fit[[3]]/(-Log[2]/2), 12]]];
  ];

  (* Also: pairwise extraction D = (r1*c1 - r2*c2) * c1*c2/(c1-c2)^2 ... *)
  (* Simpler: D_est = residual * c for each point *)
  Print["\n  D estimates from residual * c:"];
  Do[
    {c, r} = d;
    Print[StringForm["    c = ``: D = r*c = ``", N[c, 6], N[r * c, 12]]];
    ,
    {d, data}
  ];

  Print["\n"];
  ,
  {n, {7, 11}}
];

(* ================================================================== *)
(* APPROACH 3: Universal log-Airy equation                             *)
(*                                                                      *)
(* psi'' = (a + Log[x]) psi                                            *)
(*                                                                      *)
(* Solve at several a values (large negative), extract the tunneling   *)
(* action correction. The parameter a = beta0 - (1/2) Log[2c].        *)
(* ================================================================== *)

Print["--- APPROACH 3: Universal log-Airy equation ---\n"];
Print["Equation: psi'' = (a + Log[x]) psi, regular BC psi(0)=1, psi'(0)=0\n"];

Do[
  aVal = N[a, wp];
  x0 = Exp[-aVal];  (* turning point *)
  xEnd = x0 * 9/10;
  xStart = N[10^-10, wp];

  psi0 = 1 + xStart^2/2 * (aVal + Log[xStart] - 3/2);
  psip0 = xStart * (aVal + Log[xStart] - 1);

  sol = NDSolve[
    {psi''[x] == (aVal + Log[x]) psi[x],
     psi[xStart] == psi0,
     psi'[xStart] == psip0},
    psi, {x, xStart, xEnd},
    WorkingPrecision -> wp,
    MaxSteps -> 10^7,
    AccuracyGoal -> wp - 5,
    PrecisionGoal -> wp - 5
  ];

  (* Count zeros *)
  psiFunc = psi /. First[sol];
  zeros = {};
  Quiet[
    zeros = x /. FindRoot[psiFunc[x] == 0,
      {x, #}] & /@ Range[N[xStart + x0/1000, wp], xEnd, x0/500];
    zeros = DeleteDuplicates[Sort[Select[Re /@ zeros,
      xStart < # < xEnd &]], Abs[#1 - #2] < x0/10000 &];
  ];
  nZeros = Length[zeros];

  (* WKB phase *)
  phiWKBval = NIntegrate[Sqrt[Abs[aVal + Log[x]]],
    {x, xStart, xEnd},
    WorkingPrecision -> wp, MaxRecursion -> 50];

  nWKB = phiWKBval / Pi;
  deltaN = nZeros - nWKB;

  Print[StringForm["a = ``: x0 = ``, n_zeros = ``, Phi/Pi = ``, delta_n = ``",
    a, N[x0, 6], nZeros, N[nWKB, 10], N[deltaN, 10]]];
  ,
  {a, {-2, -3, -4, -5, -6, -7, -8}}
];

(* ================================================================== *)
(* APPROACH 4: Direct eigenvalue of the log-Airy ODE at high prec.    *)
(*                                                                      *)
(* The most reliable numerical approach: solve psi'' = (a+log x) psi  *)
(* with SHOOTING from both ends, matching at an interior point.        *)
(* The eigenvalue condition determines the allowed a values.           *)
(*                                                                      *)
(* For OUR problem: we don't need eigenvalues. We need the SCATTERING *)
(* phase shift delta(a). This is the phase of psi at the turning point *)
(* relative to the WKB prediction.                                     *)
(*                                                                      *)
(* At x = x0 * alpha (alpha < 1, near turning point):                 *)
(*   psi ~ Ai(-xi) where xi = (2/3 int sqrt|V| dx)^{2/3}             *)
(*   The phase of psi determines delta.                                *)
(* ================================================================== *)

Print["\n--- APPROACH 4: Phase at turning point via Airy matching ---\n"];

Do[
  aVal = N[a, wp];
  x0 = Exp[-aVal];
  xNear = x0 * 95/100;  (* 95% of turning point *)
  xStart = N[10^-10, wp];

  psi0 = 1 + xStart^2/2 * (aVal + Log[xStart] - 3/2);
  psip0 = xStart * (aVal + Log[xStart] - 1);

  sol = NDSolve[
    {psi''[x] == (aVal + Log[x]) psi[x],
     psi[xStart] == psi0,
     psi'[xStart] == psip0},
    psi, {x, xStart, xNear},
    WorkingPrecision -> wp,
    MaxSteps -> 10^7,
    AccuracyGoal -> wp - 5,
    PrecisionGoal -> wp - 5
  ];

  psiAtNear = (psi /. First[sol])[xNear];
  psipAtNear = (psi' /. First[sol])[xNear];

  VNear = aVal + Log[xNear];
  pNear = Sqrt[Abs[VNear]];

  (* WKB phase from 0 to xNear *)
  phiTo = NIntegrate[Sqrt[Abs[aVal + Log[x]]], {x, xStart, xNear},
    WorkingPrecision -> wp, MaxRecursion -> 50];

  (* From WKB: psi ~ |V|^{-1/4} sin(phi + delta) *)
  (* psi'/psi ~ pNear * cos(phi+delta)/sin(phi+delta) = pNear * Cot[phi+delta] *)
  (* So: phi + delta = ArcTan[pNear * psi / psip] (roughly) *)

  (* More precisely accounting for the V' prefactor correction: *)
  (* psi' = |V|^{-1/4} [p cos(phi+d) + V'/(4V) sin(phi+d)] *)
  (* psi = |V|^{-1/4} sin(phi+d) *)
  (* psi'/psi = p Cot[phi+d] + V'/(4V) *)
  Vp = 1/xNear;
  correctedRatio = psipAtNear/psiAtNear - Vp/(4 VNear);
  phiPlusDelta = ArcTan[pNear / correctedRatio];

  (* Unwrap: add n*Pi for the number of zero crossings *)
  (* Count sign changes for approximate zero count *)
  xSample = Table[x, {x, N[xStart, wp], xNear, (xNear - xStart)/10000}];
  psiSample = (psi /. First[sol]) /@ xSample;
  nCross = Count[Differences[Sign[psiSample]], _?(# != 0 &)];

  totalPhase = nCross * Pi + phiPlusDelta;
  delta = totalPhase - phiTo;

  Print[StringForm[
    "a = ``: phi_WKB = ``, n_cross = ``, total = ``, delta = ``",
    a, N[phiTo, 10], nCross, N[totalPhase, 10], N[delta, 10]]];
  ,
  {a, {-2, -3, -4, -5, -6, -7, -8}}
];

Print["\nExpected: delta -> Pi/2 + O(1/|a|) as a -> -inf"];
Print["The O(1/|a|) correction is the Langer residual."];
Print["In original WDW units: 1/|a| ~ 2/Log[2c] ~ (very slow decay)"];
Print["The claim -Log[2]/(2c) corresponds to a FASTER decay ~ e^{2a}."];
Print["\nDone."];
