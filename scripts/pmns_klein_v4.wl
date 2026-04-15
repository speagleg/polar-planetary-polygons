(* v4: Fixed Mathematica syntax. Run in same session with x5,y5,z5 defined *)

xB = x5; yB = y5; zB = z5;

P3 = N@{{0,0,1},{1,0,0},{0,1,0}};
F3 = N@Table[Exp[2. Pi I (a-1)(b-1)/3], {a,3}, {b,3}]/Sqrt[3.0];

ext[V_] := Module[{s13, c13, s12, s23},
  s13 = Min[Abs[V[[1,3]]], 0.999];
  c13 = Sqrt[1 - s13^2];
  s12 = If[c13 > 10^-10, Min[Abs[V[[1,2]]]/c13, 0.999], 0];
  s23 = If[c13 > 10^-10, Min[Abs[V[[2,3]]]/c13, 0.999], 0];
  {ArcSin[s12]*180/Pi, ArcSin[s23]*180/Pi, ArcSin[s13]*180/Pi}
]

target = {33.4, 49.0, 8.5};

(* Charged lepton: circulant *)
Mcl = N[xB IdentityMatrix[3] + yB P3 + zB (P3.P3)];
{evCl, vCl} = Eigensystem[N[ConjugateTranspose[Mcl].Mcl]];
uCl = Transpose[vCl[[Ordering[Re[evCl]]]]];

(* Helper: compute PMNS score for given Mnu and U_cl *)
tryPMNS[Mnu_, Ucl_] := Module[{evN, vN, uN, V, angles},
  {evN, vN} = Eigensystem[N[(Mnu + Transpose[Mnu])/2]];
  uN = Transpose[vN[[Ordering[Abs[evN]]]]];
  V = N[ConjugateTranspose[Ucl].uN];
  angles = ext[V];
  {angles, Total[Abs[angles - target]]}
]

(* === SCAN: a*diag + b*offdiag, both CL bases === *)
Print["=== Scanning a*diag(x,y,z) + b*offdiag ==="]
bestAll = {999, {}};
Do[
  Mnu = N[aa DiagonalMatrix[{xB, yB, zB}] + bb {{0,zB,yB},{zB,0,xB},{yB,xB,0}}];

  (* Try circulant CL *)
  {ang1, sc1} = tryPMNS[Mnu, uCl];
  If[sc1 < bestAll[[1]], bestAll = {sc1, {"Circ", aa, bb, ang1}}];
  If[sc1 < 20, Print["a=",aa," b=",bb," Circ: ",ang1," D=",sc1]];

  (* Try F3 CL *)
  {ang2, sc2} = tryPMNS[Mnu, F3];
  If[sc2 < bestAll[[1]], bestAll = {sc2, {"F3", aa, bb, ang2}}];
  If[sc2 < 20, Print["a=",aa," b=",bb," F3: ",ang2," D=",sc2]],

  {aa, -5, 5, 0.2}, {bb, -5, 5, 0.2}
];
Print["\nBest from grid: D=", bestAll[[1]], " params=", bestAll[[2]]]

(* === CG TEXTURES === *)
Print["\n=== CG textures ==="]
texList = {
  N@{{2xB,-zB,-yB},{-zB,2yB,-xB},{-yB,-xB,2zB}},
  N@{{2zB,-yB,-xB},{-yB,2xB,-zB},{-xB,-zB,2yB}},
  N@{{2yB,-xB,-zB},{-xB,2zB,-yB},{-zB,-yB,2xB}},
  N@{{xB,zB,yB},{zB,yB,xB},{yB,xB,zB}},
  N@{{xB,-zB,-yB},{-zB,yB,-xB},{-yB,-xB,zB}},
  N@{{0,zB,yB},{zB,0,xB},{yB,xB,0}},
  N@{{xB,yB,zB},{yB,zB,xB},{zB,xB,yB}}
};
texNames = {"Std 2x,-z,-y","Flip 2z,-y,-x","Rot 2y,-x,-z",
            "Diag+off1","Diag+off2","Pure off","Anti-cyc"};

Do[
  Mnu = texList[[i]];
  {ang1, sc1} = tryPMNS[Mnu, uCl];
  {ang2, sc2} = tryPMNS[Mnu, F3];
  Print[texNames[[i]], " Circ: ", ang1, " D=", sc1];
  Print[texNames[[i]], " F3:   ", ang2, " D=", sc2],
  {i, Length[texList]}
]

(* === FINE OPTIMIZATION === *)
Print["\n=== Fine optimization ==="]

(* Use FindMinimum with explicit numerical evaluation *)
scoreFunc[aa_?NumericQ, bb_?NumericQ, which_] := Module[
  {Mnu, evN, vN, uN, V, angles, Ucl},
  Ucl = If[which == 1, uCl, F3];
  Mnu = N[aa DiagonalMatrix[{xB,yB,zB}] + bb {{0,zB,yB},{zB,0,xB},{yB,xB,0}}];
  Mnu = (Mnu + Transpose[Mnu])/2;
  {evN, vN} = Eigensystem[N[Mnu]];
  uN = Transpose[vN[[Ordering[Abs[evN]]]]];
  V = N[ConjugateTranspose[Ucl].uN];
  angles = ext[V];
  Total[(angles - target)^2]
]

(* Grid of starting points for FindMinimum *)
Print["Optimizing (circulant CL)..."]
bestOpt = {10^6, 0, 0};
Do[
  Quiet[
    res = FindMinimum[scoreFunc[aa, bb, 1], {{aa, a0}, {bb, b0}}];
    If[res[[1]] < bestOpt[[1]],
      bestOpt = {res[[1]], aa /. res[[2]], bb /. res[[2]]}
    ]
  ],
  {a0, {-2, -1, 0, 1, 2}}, {b0, {-2, -1, 0, 1, 2}}
];
Print["  Best: a=", bestOpt[[2]], " b=", bestOpt[[3]], " score^2=", bestOpt[[1]]]
{angOpt, scOpt} = tryPMNS[
  N[bestOpt[[2]] DiagonalMatrix[{xB,yB,zB}] + bestOpt[[3]] {{0,zB,yB},{zB,0,xB},{yB,xB,0}}],
  uCl];
Print["  t12=", angOpt[[1]], " t23=", angOpt[[2]], " t13=", angOpt[[3]], " D=", scOpt]

Print["\nOptimizing (F3 CL)..."]
bestOpt2 = {10^6, 0, 0};
Do[
  Quiet[
    res = FindMinimum[scoreFunc[aa, bb, 2], {{aa, a0}, {bb, b0}}];
    If[res[[1]] < bestOpt2[[1]],
      bestOpt2 = {res[[1]], aa /. res[[2]], bb /. res[[2]]}
    ]
  ],
  {a0, {-2, -1, 0, 1, 2}}, {b0, {-2, -1, 0, 1, 2}}
];
Print["  Best: a=", bestOpt2[[2]], " b=", bestOpt2[[3]], " score^2=", bestOpt2[[1]]]
{angOpt2, scOpt2} = tryPMNS[
  N[bestOpt2[[2]] DiagonalMatrix[{xB,yB,zB}] + bestOpt2[[3]] {{0,zB,yB},{zB,0,xB},{yB,xB,0}}],
  F3];
Print["  t12=", angOpt2[[1]], " t23=", angOpt2[[2]], " t13=", angOpt2[[3]], " D=", scOpt2]

Print["\nTarget: t12=33.4  t23=49.0  t13=8.5"]
Print["DONE"]
