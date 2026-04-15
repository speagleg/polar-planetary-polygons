(* ================================================================ *)
(* Langer residual: three clean experiments                          *)
(* Run: wolframscript -file scripts/langer_chi_equation.wl           *)
(* ================================================================ *)

wp = 30;

(* --- Model --- *)
bExact[nn_Integer] := nn(nn+1)/12 - Log[2] + Log[nn]/(nn-1);
fStar[nn_Integer]  := Module[{m = Floor[nn/2]}, m(nn-m)/2];
cBase[nn_Integer]  := 12 bExact[nn];
rhoStar[nn_Integer]:= ArcSinh[Exp[fStar[nn] - bExact[nn]]/2];
beta0[nn_Integer]  := Log[2] + bExact[nn] - fStar[nn];
VV[rho_, nn_Integer] := Log[2 Sinh[rho]] + bExact[nn] - fStar[nn];

(* chi potential *)
UU[t_, c_, nn_Integer] := 1/4 + 2 c Exp[-2 t] VV[Exp[-t], nn];

sep[] := Print[StringJoin[Table["=", 72]]];

(* ================================================================ *)
(* PART A: Eigenvalue alpha_n                                        *)
(* Find c_n where psi(rho*)=0, compute alpha_n = Phi(c_n)/pi - n.   *)
(* ================================================================ *)

psiEnd[cVal_?NumericQ, nn_Integer] := Module[
  {rs, b0, r0, p0, pp0, soln},
  rs = N[rhoStar[nn], wp];
  b0 = N[beta0[nn], wp];
  r0 = N[10^-6, wp];
  p0  = 1 + N[cVal, wp] r0^2 (b0 + Log[r0] - 3/2);
  pp0 = 2 N[cVal, wp] r0 (b0 + Log[r0] - 1);
  soln = NDSolve[
    {yy''[r] == 2 N[cVal, wp] VV[r, nn] yy[r],
     yy[r0] == p0, yy'[r0] == pp0},
    yy, {r, r0, rs},
    WorkingPrecision -> wp, MaxSteps -> 10^7,
    AccuracyGoal -> wp - 5, PrecisionGoal -> wp - 5];
  (yy /. First[soln])[rs]
];

wkbPhi[cVal_?NumericQ, nn_Integer] := NIntegrate[
  Sqrt[2 cVal Abs[VV[r, nn]]],
  {r, 10^-12, rhoStar[nn]},
  WorkingPrecision -> wp, MaxRecursion -> 100];

sep[];
Print["  PART A: Eigenvalue alpha_n = Phi(c_n)/pi - n"];
sep[];

Do[
  Module[{nn = nVal, cb, eigs, c1, c2, p1, p2, ce,
          phi, ne, al, ad, cs, ds, mat, fit, mat2, fit2},

  cb = N[cBase[nn], wp];
  Print[""];
  Print["N = ", nn, "  c_base = ", N[cb, 6],
        "  rho* = ", N[rhoStar[nn], 6]];

  (* Coarse scan *)
  eigs = {};
  Do[
    c1 = cb k / 10; c2 = cb (k + 1) / 10;
    p1 = psiEnd[N[c1, wp], nn];
    p2 = psiEnd[N[c2, wp], nn];
    If[p1 p2 < 0,
      ce = c /. FindRoot[psiEnd[c, nn] == 0,
        {c, N[(c1 + c2)/2, wp], N[c1, wp], N[c2, wp]},
        WorkingPrecision -> wp];
      AppendTo[eigs, ce]],
    {k, 5, 500}];

  Print["  Found ", Length[eigs], " eigenvalues"];
  Print["    n       c_n          Phi/pi       alpha      alpha-1/4"];

  ad = {};
  Do[
    phi = wkbPhi[eigs[[i]], nn];
    ne = Round[phi/Pi - 1/4];
    al = phi/Pi - ne;
    AppendTo[ad, {eigs[[i]], ne, al}];
    If[Mod[i, 5] == 1 || i <= 5 || i == Length[eigs],
      Print["    ", PaddedForm[ne, {4, 0}], "  ",
        N[eigs[[i]], 10], "  ", N[phi/Pi, 10], "  ",
        N[al, 10], "  ", N[al - 1/4, 10]]],
    {i, Length[eigs]}];

  If[Length[ad] >= 3,
    cs = N[ad[[All, 1]], wp];
    ds = N[ad[[All, 3]] - 1/4, wp];
    (* Fit delta = B/sqrt(c) + D/c *)
    mat = Table[{1/Sqrt[ci], 1/ci}, {ci, cs}];
    fit = LeastSquares[mat, ds];
    Print[""];
    Print["  Fit: alpha - 1/4 = ", N[fit[[1]], 10],
          "/Sqrt[c] + ", N[fit[[2]], 10], "/c"];
    (* Extrapolate alpha_inf *)
    mat2 = Table[{1, 1/Sqrt[ci], 1/ci}, {ci, cs}];
    fit2 = LeastSquares[mat2, N[ad[[All, 3]], wp]];
    Print["  alpha_inf = ", N[fit2[[1]], 12],
          "  (delta = ", N[fit2[[1]] - 1/4, 12], ")"];
    Print["  Compare: 2/5 = 0.4,  1/4 + 3/(2 Pi^2) = ",
          N[1/4 + 3/(2 Pi^2), 12]]];

  ],  (* end Module *)
  {nVal, {7, 11}}
];


(* ================================================================ *)
(* PART B: chi equation Prufer envelope                              *)
(* Solve chi''=U(t) chi from large t inward, extract E_chi.          *)
(* ================================================================ *)

Print[""];
sep[];
Print["  PART B: chi equation Prufer envelope"];
sep[];

Do[
  Module[{nn = nVal, cb, c, tTurn, tObs, tStart,
          chi0val, chip0val, soln, fF, cv, cpv, uv,
          pp, RR, Echi, En, data, cs, es, mat, fit},

  cb = N[cBase[nn], wp];
  Print[""];
  Print["N = ", nn];
  data = {};

  Do[
    c = N[cb mult, wp];

    tTurn = t /. FindRoot[UU[t, c, nn] == 0, {t, 3},
      WorkingPrecision -> wp];
    tObs  = N[tTurn/2, wp];
    tStart = N[tTurn + 15, wp];

    chi0val  = N[Exp[tStart/2], wp];
    chip0val = N[Exp[tStart/2]/2, wp];

    soln = NDSolve[
      {ff''[t] == UU[t, c, nn] ff[t],
       ff[tStart] == chi0val, ff'[tStart] == chip0val},
      ff, {t, -1, tStart},
      WorkingPrecision -> wp, MaxSteps -> 10^7,
      AccuracyGoal -> wp - 5, PrecisionGoal -> wp - 5];

    fF = ff /. First[soln];
    cv  = fF[tObs];
    cpv = fF'[tObs];
    uv  = UU[tObs, c, nn];

    If[uv < 0,
      pp = Sqrt[Abs[uv]];
      RR = Sqrt[cv^2 + (cpv/pp)^2];
      Echi = RR Abs[uv]^(1/4);
      En = Echi / Sqrt[2];
      AppendTo[data, {c, En}];
      Print["  c = ", N[c, 8], " (", mult, "x): E/sqrt2 = ", N[En, 15]],
      (* else *)
      Print["  c = ", N[c, 8], " (", mult, "x): U>0 at t_obs"]],
    {mult, {1, 2, 4, 8, 16, 32, 64, 128}}];

  If[Length[data] >= 3,
    cs = N[data[[All, 1]], wp];
    es = N[data[[All, 2]], wp];
    mat = Table[{1, 1/Sqrt[ci], 1/ci}, {ci, cs}];
    fit = LeastSquares[mat, es];
    Print[""];
    Print["  Fit: E/sqrt2 = ", N[fit[[1]], 12],
          " + ", N[fit[[2]], 10], "/sqrt(c) + ",
          N[fit[[3]], 10], "/c"];
    Print["  1/c coeff = ", N[fit[[3]], 10],
          "   -ln2/2 = ", N[-Log[2]/2, 10]]];

  ],  (* end Module *)
  {nVal, {7, 11}}
];


(* ================================================================ *)
(* PART C: Universal log-Airy eigenvalues                            *)
(* psi'' = (a + Log x) psi. Tests whether alpha_inf is universal.    *)
(* ================================================================ *)

Print[""];
sep[];
Print["  PART C: Universal log-Airy eigenvalues"];
sep[];

psiLA[aVal_?NumericQ] := Module[{x0, xs, b0, p0, pp0, soln},
  x0 = N[Exp[-aVal], wp];
  xs = N[10^-8, wp];
  b0 = N[aVal, wp] + Log[xs];
  p0  = 1 + xs^2/2 (b0 - 3/2);
  pp0 = xs (b0 - 1);
  soln = NDSolve[
    {yy''[x] == (N[aVal, wp] + Log[x]) yy[x],
     yy[xs] == p0, yy'[xs] == pp0},
    yy, {x, xs, x0},
    WorkingPrecision -> wp, MaxSteps -> 10^7,
    AccuracyGoal -> wp - 5, PrecisionGoal -> wp - 5];
  (yy /. First[soln])[x0]
];

wkbPhiLA[aVal_?NumericQ] := NIntegrate[
  Sqrt[Abs[aVal + Log[x]]],
  {x, 10^-12, Exp[-aVal]},
  WorkingPrecision -> wp, MaxRecursion -> 100];

Module[{eigsLA = {}, a1, a2, p1, p2, ae,
        phi, ne, al, adLA, aas, als, mat, fit},

  (* Scan a from -2 to -30 in steps of 0.2 *)
  Do[
    a1 = N[-2 - (k - 1) * 2/10, wp];
    a2 = N[-2 - k * 2/10, wp];
    Quiet[
      p1 = psiLA[a1];
      p2 = psiLA[a2];
      If[NumericQ[p1] && NumericQ[p2] && p1 p2 < 0,
        ae = a /. FindRoot[psiLA[a] == 0,
          {a, (a1 + a2)/2, a1, a2},
          WorkingPrecision -> wp];
        AppendTo[eigsLA, ae]]],
    {k, 1, 140}];

  Print["  Found ", Length[eigsLA], " log-Airy eigenvalues"];
  Print[""];
  Print["    n      a_n         |a|      Phi/pi       alpha      alpha-1/4"];

  adLA = {};
  Do[
    phi = wkbPhiLA[eigsLA[[i]]];
    ne = Round[phi/Pi - 0.40];
    al = phi/Pi - ne;
    AppendTo[adLA, {eigsLA[[i]], ne, al}];
    Print["    ", PaddedForm[ne, {4, 0}], "  ",
      N[eigsLA[[i]], 8], "  ", N[Abs[eigsLA[[i]]], 6], "  ",
      N[phi/Pi, 10], "  ", N[al, 10], "  ", N[al - 1/4, 10]],
    {i, Length[eigsLA]}];

  If[Length[adLA] >= 3,
    aas = N[Abs[adLA[[All, 1]]], wp];
    als = N[adLA[[All, 3]], wp];
    mat = Table[{1, 1/Sqrt[ai], 1/ai}, {ai, aas}];
    fit = LeastSquares[mat, als];
    Print[""];
    Print["  alpha_inf (log-Airy) = ", N[fit[[1]], 12],
          "  (delta = ", N[fit[[1]] - 1/4, 12], ")"];
    Print["  WDW N=7 result:      alpha_inf ~ 0.403"];
    If[Abs[fit[[1]] - 0.403] < 0.02,
      Print["  Universal? YES"],
      Print["  Universal? DIFFERENT"]]];
];

Print[""];
Print["Done."];
