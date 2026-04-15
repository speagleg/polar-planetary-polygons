(* Fast version: forces numeric evaluation throughout *)

NN = 7;
tau0 = N[(1 + I Sqrt[7])/2, 30];

(* Klein quartic forms via built-in DedekindEta *)
kf[a_, tau_] := N[DedekindEta[(tau + a)/NN] DedekindEta[(tau + (NN - a))/NN] / DedekindEta[tau]^2, 20]

Print["Computing Klein quartic forms..."]
{x, y, z} = {kf[1, tau0], kf[2, tau0], kf[3, tau0]};
Print["x = ", x, "  |x| = ", Abs[x]]
Print["y = ", y, "  |y| = ", Abs[y]]
Print["z = ", z, "  |z| = ", Abs[z]]
Print["Klein check: ", Abs[x^3 y + y^3 z + z^3 x]]

(* Matrices - all forced numeric *)
P3 = N@{{0,0,1},{1,0,0},{0,1,0}};
omega3 = N[Exp[2 Pi I/3]];
F3 = N@Table[omega3^((a-1)(b-1)), {a,3}, {b,3}]/Sqrt[3.0];

(* Charged lepton: circulant *)
Mcl = N[x IdentityMatrix[3] + y P3 + z P3.P3];
Print["\nMcl built, diagonalizing..."]
{evCl, UCl} = Eigensystem[N[ConjugateTranspose[Mcl].Mcl]];
UCl = Transpose[UCl[[Ordering[Re[evCl]]]]];
Print["Charged lepton eigenvalues: ", Sqrt[Sort[Re[evCl]]]]

(* Neutrino: symmetric CG of PSL(2,7) *)
Mnu = N@{{2x, -z, -y}, {-z, 2y, -x}, {-y, -x, 2z}};
Print["Mnu built, diagonalizing..."]
{evNu, UNu} = Eigensystem[N[Mnu]];
UNu = Transpose[UNu[[Ordering[Abs[evNu]]]]];
Print["Neutrino eigenvalues: ", Sort[Abs[evNu]]]

(* Extract PMNS angles *)
ext[V_] := Module[{s13, c13, s12, s23},
  s13 = Min[Abs[V[[1,3]]], 0.999];
  c13 = Sqrt[1 - s13^2];
  s12 = If[c13 > 10^-10, Min[Abs[V[[1,2]]]/c13, 0.999], 0];
  s23 = If[c13 > 10^-10, Min[Abs[V[[2,3]]]/c13, 0.999], 0];
  {ArcSin[s12]*180/Pi, ArcSin[s23]*180/Pi, ArcSin[s13]*180/Pi}
]

(* === THREE PMNS CONSTRUCTIONS === *)
Print["\n========================================"]
Print["PMNS RESULTS"]
Print["========================================"]
Print["Target: theta12=33.4  theta23=49.0  theta13=8.5\n"]

(* 1. Circulant x Symmetric *)
V1 = N[ConjugateTranspose[UCl].UNu];
a1 = ext[V1];
Print["1. U_cl(circulant) x U_nu(symmetric):"]
Print["   t12=", a1[[1]], "  t23=", a1[[2]], "  t13=", a1[[3]]]
Print["   Delta=", Total[Abs[a1 - {33.4, 49.0, 8.5}]]]

(* 2. F3 x Symmetric *)
V2 = N[ConjugateTranspose[F3].UNu];
a2 = ext[V2];
Print["\n2. F3^dag x U_nu(symmetric):"]
Print["   t12=", a2[[1]], "  t23=", a2[[2]], "  t13=", a2[[3]]]
Print["   Delta=", Total[Abs[a2 - {33.4, 49.0, 8.5}]]]

(* 3. Fricke x Symmetric *)
QR = {1, 2, 4};
Sgen = N@Table[2 I Sin[2. Pi QR[[a]] QR[[b]]/NN]/Sqrt[7.0], {a,3}, {b,3}];
V3 = N[ConjugateTranspose[Sgen].UNu];
a3 = ext[V3];
Print["\n3. S_Fricke^dag x U_nu(symmetric):"]
Print["   t12=", a3[[1]], "  t23=", a3[[2]], "  t13=", a3[[3]]]
Print["   Delta=", Total[Abs[a3 - {33.4, 49.0, 8.5}]]]

(* 4. Circulant x Diagonal *)
MnuDiag = N@DiagonalMatrix[{x, y, z}];
{evD, UD} = Eigensystem[N[MnuDiag]];
UD = Transpose[UD[[Ordering[Abs[evD]]]]];
V4 = N[ConjugateTranspose[UCl].UD];
a4 = ext[V4];
Print["\n4. U_cl(circulant) x U_nu(diagonal):"]
Print["   t12=", a4[[1]], "  t23=", a4[[2]], "  t13=", a4[[3]]]
Print["   Delta=", Total[Abs[a4 - {33.4, 49.0, 8.5}]]]

(* 5. Try with seesaw: M_nu = Mcl . diag(1/M_R) . Mcl^T *)
Do[
  MR = N@DiagonalMatrix[mr];
  Mss = N[Mcl.Inverse[MR].Transpose[Mcl]];
  {evS, US} = Eigensystem[N[ConjugateTranspose[Mss].Mss]];
  US = Transpose[US[[Ordering[Re[evS]]]]];
  V5 = N[ConjugateTranspose[UCl].US];
  a5 = ext[V5];
  score = Total[Abs[a5 - {33.4, 49.0, 8.5}]];
  If[score < 40,
    Print["\n5. Seesaw MR=", mrlabel, ": t12=", a5[[1]], " t23=", a5[[2]], " t13=", a5[[3]], " D=", score]
  ],
  {mrlabel, mr} , {
    {"flat", {1., 1., 1.}},
    {"lambda", {3., 1., 0.01}},
    {"inv", {0.01, 1., 3.}},
    {"steep", {10., 1., 0.001}}
  }
]

Print["\n========================================"]
Print["DONE"]
Print["========================================"]
