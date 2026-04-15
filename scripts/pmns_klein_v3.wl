(* v3: Explore ALL PSL(2,7) Majorana textures with the correct Klein quartic forms *)
(* Run in same session where x5, y5, z5 are defined *)

xB = x5; yB = y5; zB = z5;
Print["Klein forms: |x|=", Abs[xB], " |y|=", Abs[yB], " |z|=", Abs[zB]]

P3 = N@{{0,0,1},{1,0,0},{0,1,0}};
omega3 = N[Exp[2 Pi I/3]];
F3 = N@Table[omega3^((a-1)(b-1)), {a,3}, {b,3}]/Sqrt[3.0];

ext[V_] := Module[{s13, c13, s12, s23},
  s13 = Min[Abs[V[[1,3]]], 0.999];
  c13 = Sqrt[1 - s13^2];
  s12 = If[c13 > 10^-10, Min[Abs[V[[1,2]]]/c13, 0.999], 0];
  s23 = If[c13 > 10^-10, Min[Abs[V[[2,3]]]/c13, 0.999], 0];
  {ArcSin[s12]*180/Pi, ArcSin[s23]*180/Pi, ArcSin[s13]*180/Pi}
]

target = {33.4, 49.0, 8.5};

(* Circulant charged lepton *)
Mcl = N[xB IdentityMatrix[3] + yB P3 + zB (P3.P3)];
{evCl, vCl} = Eigensystem[N[ConjugateTranspose[Mcl].Mcl]];
uCl = Transpose[vCl[[Ordering[Re[evCl]]]]];

(* ============================================================
   SECTION 1: All possible 3x3 symmetric matrices from (x,y,z)

   For PSL(2,7), the symmetric square Sym^2(3) = 3 + 3'
   (NOT 6 as I said before — for PSL(2,7) with 3 being faithful,
   Sym^2(3) decomposes into 3 + 3')

   So there are TWO independent symmetric matrix constructions:
   one from the 3 channel and one from the 3' channel.
   ============================================================ *)

Print["\n=== SECTION 1: Systematic Majorana textures ==="]

(* The most general symmetric 3x3 matrix built from (x,y,z)
   respecting the cyclic Z_3 subgroup has the form:
   M = a*[[x,0,0],[0,y,0],[0,0,z]] + b*[[0,z,y],[z,0,x],[y,x,0]]
   where a and b are free coefficients.

   The diagonal part uses (x,y,z) directly.
   The off-diagonal part uses the CYCLIC COMPLEMENT:
   M_12 = z, M_13 = y, M_23 = x (shifted by one step)
*)

(* Scan over (a, b) parameter space *)
Print["Scanning a*diag(x,y,z) + b*offdiag(z,y;x) ..."]
bestScore = 999;
bestParams = {};

Do[
  Mnu = N[aa*DiagonalMatrix[{xB, yB, zB}] +
          bb*{{0, zB, yB}, {zB, 0, xB}, {yB, xB, 0}}];
  (* Symmetrize *)
  Mnu = (Mnu + Transpose[Mnu])/2;
  {evN, vN} = Eigensystem[N[Mnu]];
  uN = Transpose[vN[[Ordering[Abs[evN]]]]];

  (* Try both charged lepton bases *)
  Do[
    V = N[ConjugateTranspose[ucl].uN];
    angles = ext[V];
    score = Total[Abs[angles - target]];
    If[score < bestScore,
      bestScore = score;
      bestParams = {aa, bb, clabel, angles}
    ];
    If[score < 20,
      Print["  a=", aa, " b=", bb, " cl=", clabel,
            ": t12=", angles[[1]], " t23=", angles[[2]],
            " t13=", angles[[3]], " D=", score]
    ],
    {{clabel, ucl}, {{"Circ", uCl}, {"F3", F3}}}
  ],
  {aa, -3, 3, 0.25},
  {bb, -3, 3, 0.25}
];

Print["\nBest: a=", bestParams[[1]], " b=", bestParams[[2]],
      " cl=", bestParams[[3]]]
Print["  t12=", bestParams[[4,1]], " t23=", bestParams[[4,2]],
      " t13=", bestParams[[4,3]], " D=", bestScore]

(* ============================================================
   SECTION 2: The OTHER PSL(2,7) CG decomposition

   The standard CG: [[2x,-z,-y],[-z,2y,-x],[-y,-x,2z]]
   The alternative: [[x+y, z, z], [z, y+z, x], [z, x, x+z]]
   And cyclic variants...
   ============================================================ *)

Print["\n=== SECTION 2: Alternative PSL(2,7) CG textures ==="]

textures = {
  {"Standard: 2x,-z,-y", N@{{2xB, -zB, -yB}, {-zB, 2yB, -xB}, {-yB, -xB, 2zB}}},
  {"Flipped: 2z,-y,-x", N@{{2zB, -yB, -xB}, {-yB, 2xB, -zB}, {-xB, -zB, 2yB}}},
  {"Rotated: 2y,-x,-z", N@{{2yB, -xB, -zB}, {-xB, 2zB, -yB}, {-zB, -yB, 2xB}}},
  {"Diag+offdiag1", N@{{xB, zB, yB}, {zB, yB, xB}, {yB, xB, zB}}},
  {"Diag+offdiag2", N@{{xB, -zB, -yB}, {-zB, yB, -xB}, {-yB, -xB, zB}}},
  {"Pure offdiag", N@{{0, zB, yB}, {zB, 0, xB}, {yB, xB, 0}}},
  {"Anti-cyclic", N@{{xB, yB, zB}, {yB, zB, xB}, {zB, xB, yB}}},
  {"x^2 outer", N@Outer[Times, {xB,yB,zB}, {xB,yB,zB}]},
  {"Democratic+diag", N@({{1,1,1},{1,1,1},{1,1,1}}*xB/3 + DiagonalMatrix[{0, yB-xB/3, zB-xB/3}])},
  {"Seesaw-like", N@({{xB^2,xB yB,xB zB},{xB yB,yB^2,yB zB},{xB zB,yB zB,zB^2}}/xB)}
};

Do[
  {label, Mnu} = tex;
  Mnu = N[(Mnu + Transpose[Mnu])/2]; (* ensure symmetric *)
  {evN, vN} = Eigensystem[N[Mnu]];
  uN = Transpose[vN[[Ordering[Abs[evN]]]]];

  Do[
    V = N[ConjugateTranspose[ucl].uN];
    angles = ext[V];
    score = Total[Abs[angles - target]];
    If[score < 30,
      Print[label, " + ", clabel, ": t12=", angles[[1]],
            " t23=", angles[[2]], " t13=", angles[[3]], " D=", score]
    ],
    {{clabel, ucl}, {{"Circ", uCl}, {"F3", F3}}}
  ],
  {tex, textures}
]

(* ============================================================
   SECTION 3: Seesaw M_nu = Y . diag(1/MR) . Y^T
   with Y = circulant(x,y,z) and various M_R
   ============================================================ *)

Print["\n=== SECTION 3: Seesaw with circulant Dirac Yukawa ==="]

Yd = N[xB IdentityMatrix[3] + yB P3 + zB (P3.P3)];
bestSS = 999;

Do[
  MRinv = N@DiagonalMatrix[1.0/mr];
  Mss = N[Yd.MRinv.Transpose[Yd]];
  Mss = N[(Mss + Transpose[Mss])/2];
  {evS, vS} = Eigensystem[N[Mss]];
  uS = Transpose[vS[[Ordering[Abs[evS]]]]];

  Do[
    V = N[ConjugateTranspose[ucl].uS];
    angles = ext[V];
    score = Total[Abs[angles - target]];
    If[score < 30,
      Print["MR=", mrlabel, " + ", clabel, ": t12=", angles[[1]],
            " t23=", angles[[2]], " t13=", angles[[3]], " D=", score]
    ];
    If[score < bestSS, bestSS = score; bestSSparams = {mrlabel, clabel, angles}],
    {{clabel, ucl}, {{"Circ", uCl}, {"F3", F3}}}
  ],
  {{mrlabel, mr}, {
    {"flat", {1., 1., 1.}},
    {"1:2:4", {1., 2., 4.}},
    {"1:3:6", {1., 3., 6.}},
    {"1:5:25", {1., 5., 25.}},
    {"1:7:49", {1., 7., 49.}},
    {"3:1:0.01", {3., 1., 0.01}},
    {"0.01:1:3", {0.01, 1., 3.}},
    {"6:2:0.1", {6., 2., 0.1}},
    {"0.1:1:10", {0.1, 1., 10.}},
    {"49:7:1", {49., 7., 1.}},
    {"exp", {Exp[3.], Exp[1.], Exp[0.]}},
    {"inv_exp", {Exp[0.], Exp[1.], Exp[3.]}}
  }}
]

Print["\nBest seesaw: ", bestSSparams, " D=", bestSS]

(* ============================================================
   SECTION 4: OPTIMIZE a,b in M = a*diag + b*offdiag
   ============================================================ *)

Print["\n=== SECTION 4: Fine optimization of (a,b) ==="]

pmnsScore[{aa_, bb_}, ucl_] := Module[{Mnu, evN, vN, uN, V, angles},
  Mnu = N[aa*DiagonalMatrix[{xB, yB, zB}] +
          bb*{{0, zB, yB}, {zB, 0, xB}, {yB, xB, 0}}];
  Mnu = (Mnu + Transpose[Mnu])/2;
  {evN, vN} = Eigensystem[N[Mnu]];
  uN = Transpose[vN[[Ordering[Abs[evN]]]]];
  V = N[ConjugateTranspose[ucl].uN];
  angles = ext[V];
  Total[(angles - target)^2]
]

(* Optimize for circulant CL *)
Print["Optimizing with circulant charged leptons..."]
result1 = NMinimize[pmnsScore[{aa, bb}, uCl], {aa, bb}];
Print["  Min score^2 = ", result1[[1]]]
{aaOpt, bbOpt} = {aa, bb} /. result1[[2]];
Print["  a = ", aaOpt, ", b = ", bbOpt]

Mnu = N[aaOpt*DiagonalMatrix[{xB, yB, zB}] +
        bbOpt*{{0, zB, yB}, {zB, 0, xB}, {yB, xB, 0}}];
Mnu = (Mnu + Transpose[Mnu])/2;
{evN, vN} = Eigensystem[N[Mnu]];
uN = Transpose[vN[[Ordering[Abs[evN]]]]];
V = N[ConjugateTranspose[uCl].uN];
aOpt = ext[V];
Print["  t12=", aOpt[[1]], " t23=", aOpt[[2]], " t13=", aOpt[[3]],
      " D=", Total[Abs[aOpt - target]]]

(* Optimize for F3 CL *)
Print["\nOptimizing with F3 charged leptons..."]
result2 = NMinimize[pmnsScore[{aa, bb}, F3], {aa, bb}];
Print["  Min score^2 = ", result2[[1]]]
{aaOpt2, bbOpt2} = {aa, bb} /. result2[[2]];
Print["  a = ", aaOpt2, ", b = ", bbOpt2]

Mnu2 = N[aaOpt2*DiagonalMatrix[{xB, yB, zB}] +
         bbOpt2*{{0, zB, yB}, {zB, 0, xB}, {yB, xB, 0}}];
Mnu2 = (Mnu2 + Transpose[Mnu2])/2;
{evN2, vN2} = Eigensystem[N[Mnu2]];
uN2 = Transpose[vN2[[Ordering[Abs[evN2]]]]];
V2 = N[ConjugateTranspose[F3].uN2];
aOpt2 = ext[V2];
Print["  t12=", aOpt2[[1]], " t23=", aOpt2[[2]], " t13=", aOpt2[[3]],
      " D=", Total[Abs[aOpt2 - target]]]

Print["\n========================================"]
Print["DONE — check which construction gets Delta < 15"]
Print["========================================"]
