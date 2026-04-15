(* Klein quartic forms via the CORRECT infinite product (Elkies 1998):

   f_a(tau) = q^{a/7} Prod_{n>=1} (1-q^{7n-a})^{-1} (1-q^{7n-(7-a)})^{-1} (1-q^n)^2

   BUT the simplest correct construction uses:
   f_a(tau) = q^{a(7-a)/14} Prod_{n>=0,n=a mod 7} (1-q^n) Prod_{n>=0,n=-a mod 7} (1-q^n)

   The key: the three coordinates of the Klein quartic are:
   x_a = q^{a/7} prod_{n>=1} (1-q^{7n-(7-a)})(1-q^{7n-a})
   for a = 1, 2, 3 (pair representatives)
   These satisfy x_1^3 x_2 + x_2^3 x_3 + x_3^3 x_1 = 0.
*)

NN = 7;
tau0 = N[(1 + I Sqrt[7])/2, 30];
q0 = N[Exp[2 Pi I tau0], 30];
Print["tau0 = ", tau0]
Print["|q| = ", Abs[q0]]

nterms = 300;

(* Construction 1: Direct infinite product *)
kleinProd[a_, tau_, nt_:300] := Module[{q, result},
  q = N[Exp[2 Pi I tau], 25];
  result = q^(a/NN);
  Do[
    result *= (1 - q^(NN n - (NN - a))) (1 - q^(NN n - a)),
    {n, 1, nt}
  ];
  result
]

Print["\n=== Construction 1: direct product ==="]
{x1, y1, z1} = {kleinProd[1, tau0], kleinProd[2, tau0], kleinProd[3, tau0]};
Print["x = ", x1, "  |x| = ", Abs[x1]]
Print["y = ", y1, "  |y| = ", Abs[y1]]
Print["z = ", z1, "  |z| = ", Abs[z1]]
kc1 = Abs[x1^3 y1 + y1^3 z1 + z1^3 x1];
Print["Klein check: ", kc1]

(* Construction 2: Try the RECIPROCAL *)
kleinRecip[a_, tau_, nt_:300] := Module[{q, result},
  q = N[Exp[2 Pi I tau], 25];
  result = q^(a/NN);
  Do[
    result /= (1 - q^(NN n - (NN - a))) (1 - q^(NN n - a)),
    {n, 1, nt}
  ];
  result
]

Print["\n=== Construction 2: reciprocal product ==="]
{x2, y2, z2} = {kleinRecip[1, tau0], kleinRecip[2, tau0], kleinRecip[3, tau0]};
Print["x = ", x2, "  |x| = ", Abs[x2]]
Print["y = ", y2, "  |y| = ", Abs[y2]]
Print["z = ", z2, "  |z| = ", Abs[z2]]
kc2 = Abs[x2^3 y2 + y2^3 z2 + z2^3 x2];
Print["Klein check: ", kc2]

(* Construction 3: with eta(tau)^2 normalization *)
kleinEta[a_, tau_, nt_:300] := Module[{q, etasq, prod},
  q = N[Exp[2 Pi I tau], 25];
  etasq = q^(1/12) Product[(1 - q^n)^2, {n, 1, nt}];
  prod = q^(a/NN);
  Do[
    prod *= (1 - q^(NN n - (NN - a))) (1 - q^(NN n - a)),
    {n, 1, nt}
  ];
  prod / etasq
]

Print["\n=== Construction 3: product / eta^2 ==="]
{x3, y3, z3} = {kleinEta[1, tau0], kleinEta[2, tau0], kleinEta[3, tau0]};
Print["x = ", x3, "  |x| = ", Abs[x3]]
Print["y = ", y3, "  |y| = ", Abs[y3]]
Print["z = ", z3, "  |z| = ", Abs[z3]]
kc3 = Abs[x3^3 y3 + y3^3 z3 + z3^3 x3];
Print["Klein check: ", kc3]

(* Construction 4: product * eta^2 *)
kleinEta2[a_, tau_, nt_:300] := Module[{q, etasq, prod},
  q = N[Exp[2 Pi I tau], 25];
  etasq = q^(1/12) Product[(1 - q^n)^2, {n, 1, nt}];
  prod = q^(a/NN);
  Do[
    prod *= (1 - q^(NN n - (NN - a))) (1 - q^(NN n - a)),
    {n, 1, nt}
  ];
  prod * etasq
]

Print["\n=== Construction 4: product * eta^2 ==="]
{x4, y4, z4} = {kleinEta2[1, tau0], kleinEta2[2, tau0], kleinEta2[3, tau0]};
Print["x = ", x4, "  |x| = ", Abs[x4]]
Print["y = ", y4, "  |y| = ", Abs[y4]]
Print["z = ", z4, "  |z| = ", Abs[z4]]
kc4 = Abs[x4^3 y4 + y4^3 z4 + z4^3 x4];
Print["Klein check: ", kc4]

(* Construction 5: leading power a(7-a)/14 instead of a/7 *)
kleinBern[a_, tau_, nt_:300] := Module[{q, lead, prod},
  q = N[Exp[2 Pi I tau], 25];
  lead = a (NN - a)/(2 NN); (* = Havelock Casimir / N *)
  prod = q^lead;
  Do[
    prod *= (1 - q^(NN n - (NN - a))) (1 - q^(NN n - a)),
    {n, 1, nt}
  ];
  prod
]

Print["\n=== Construction 5: leading power = a(7-a)/14 ==="]
{x5, y5, z5} = {kleinBern[1, tau0], kleinBern[2, tau0], kleinBern[3, tau0]};
Print["x = ", x5, "  |x| = ", Abs[x5]]
Print["y = ", y5, "  |y| = ", Abs[y5]]
Print["z = ", z5, "  |z| = ", Abs[z5]]
kc5 = Abs[x5^3 y5 + y5^3 z5 + z5^3 x5];
Print["Klein check: ", kc5]

(* ============================================================
   IDENTIFY THE WINNER: whichever has Klein check closest to 0
   ============================================================ *)
Print["\n=== SUMMARY OF KLEIN CHECKS ==="]
Print["Construction 1 (direct prod):    ", kc1]
Print["Construction 2 (reciprocal):     ", kc2]
Print["Construction 3 (prod/eta^2):     ", kc3]
Print["Construction 4 (prod*eta^2):     ", kc4]
Print["Construction 5 (Bernoulli lead): ", kc5]

best = First[Ordering[{kc1, kc2, kc3, kc4, kc5}]];
Print["\nBEST: Construction ", best]

(* Use the best construction for PMNS *)
{xB, yB, zB} = Switch[best,
  1, {x1, y1, z1},
  2, {x2, y2, z2},
  3, {x3, y3, z3},
  4, {x4, y4, z4},
  5, {x5, y5, z5}
];

Print["\n========================================"]
Print["PMNS FROM BEST KLEIN QUARTIC FORMS"]
Print["========================================"]

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
Mcl = N[xB IdentityMatrix[3] + yB P3 + zB P3.P3];
{evCl, UCl} = Eigensystem[N[ConjugateTranspose[Mcl].Mcl]];
UCl = Transpose[UCl[[Ordering[Re[evCl]]]]];

(* Symmetric Majorana neutrino *)
Mnu = N@{{2 xB, -zB, -yB}, {-zB, 2 yB, -xB}, {-yB, -xB, 2 zB}};
{evNu, UNu} = Eigensystem[N[Mnu]];
UNu = Transpose[UNu[[Ordering[Abs[evNu]]]]];

(* 4 PMNS constructions *)
Do[
  V = N[ConjugateTranspose[Ucl].Unu];
  a = ext[V];
  score = Total[Abs[a - target]];
  Print[label, ": t12=", a[[1]], " t23=", a[[2]], " t13=", a[[3]], " D=", score],
  {{label, Ucl, Unu}, {
    {"Circulant x Symmetric", UCl, UNu},
    {"F3 x Symmetric", F3, UNu},
    {"Circulant x Identity", UCl, IdentityMatrix[3]},
    {"F3 x Identity", F3, IdentityMatrix[3]}
  }}
]

Print["\nTarget: t12=33.4  t23=49.0  t13=8.5"]
Print["DONE"]
