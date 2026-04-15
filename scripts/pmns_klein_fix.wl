(* Quick fix: compute PMNS from Construction 5 (already computed) *)
(* xB, yB, zB should already be x5, y5, z5 from the previous run *)

xB = x5; yB = y5; zB = z5;
Print["Using Construction 5 (Bernoulli lead, Klein check = 6e-8)"]
Print["|x| = ", Abs[xB], "  |y| = ", Abs[yB], "  |z| = ", Abs[zB]]

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

(* Circulant charged lepton *)
Mcl = N[xB IdentityMatrix[3] + yB P3 + zB (P3.P3)];
{evCl, vCl} = Eigensystem[N[ConjugateTranspose[Mcl].Mcl]];
uCl = Transpose[vCl[[Ordering[Re[evCl]]]]];
Print["\nCharged lepton masses: ", Sqrt[Sort[Re[evCl]]]]

(* Symmetric Majorana neutrino (PSL(2,7) CG) *)
Mnu = N@{{2 xB, -zB, -yB}, {-zB, 2 yB, -xB}, {-yB, -xB, 2 zB}};
{evNu, vNu} = Eigensystem[N[Mnu]];
uNu = Transpose[vNu[[Ordering[Abs[evNu]]]]];
Print["Neutrino eigenvalues: ", Sort[Abs[evNu]]]

target = {33.4, 49.0, 8.5};

(* 1. Circulant x Symmetric *)
V1 = N[ConjugateTranspose[uCl].uNu];
a1 = ext[V1];
Print["\n1. Circulant x Symmetric: t12=", a1[[1]], " t23=", a1[[2]], " t13=", a1[[3]], " D=", Total[Abs[a1-target]]]

(* 2. F3 x Symmetric *)
V2 = N[ConjugateTranspose[F3].uNu];
a2 = ext[V2];
Print["2. F3 x Symmetric:        t12=", a2[[1]], " t23=", a2[[2]], " t13=", a2[[3]], " D=", Total[Abs[a2-target]]]

(* 3. Circulant x Identity (= pure charged lepton mixing) *)
V3 = N[ConjugateTranspose[uCl]];
a3 = ext[V3];
Print["3. Circulant x I:          t12=", a3[[1]], " t23=", a3[[2]], " t13=", a3[[3]], " D=", Total[Abs[a3-target]]]

(* 4. F3 x Identity (= pure TBM) *)
V4 = N[ConjugateTranspose[F3]];
a4 = ext[V4];
Print["4. F3 x I (TBM):           t12=", a4[[1]], " t23=", a4[[2]], " t13=", a4[[3]], " D=", Total[Abs[a4-target]]]

(* 5. Fricke S-matrix *)
QR = {1, 2, 4};
Sgen = N@Table[2 I Sin[2. Pi QR[[a]] QR[[b]]/7]/Sqrt[7.0], {a,3}, {b,3}];
V5 = N[ConjugateTranspose[Sgen].uNu];
a5 = ext[V5];
Print["5. Fricke x Symmetric:     t12=", a5[[1]], " t23=", a5[[2]], " t13=", a5[[3]], " D=", Total[Abs[a5-target]]]

Print["\nTarget: t12=33.4  t23=49.0  t13=8.5"]
