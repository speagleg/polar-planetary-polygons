(* ============================================================
   PMNS Mixing from Level-7 Modular Forms on the Klein Quartic
   ============================================================

   The Klein quartic x^3 y + y^3 z + z^3 x = 0 is the modular
   curve X(7) with Aut = PSL(2,7). Its three holomorphic
   differentials span S_2(Gamma(7)), the 3D space of weight-2
   cusp forms at level 7.

   We evaluate these at the CM point tau_0 = (1 + I Sqrt[7])/2
   (discriminant D = -7, class number 1) and construct the
   PMNS mixing matrix from the modular Yukawa couplings.

   Reference: Elkies, "The Klein Quartic in Number Theory" (1998)
   ============================================================ *)

(* --- Constants --- *)
NN = 7;
tau0 = (1 + I Sqrt[7])/2;
q0 = Exp[2 Pi I tau0];
Print["tau_0 = ", tau0, "  |q| = ", Abs[q0] // N]

(* ============================================================
   SECTION 1: Construct the cusp forms of Gamma(7)
   ============================================================ *)

(* Dedekind eta function *)
eta[tau_, nterms_:500] := Module[{q = Exp[2 Pi I tau]},
  q^(1/24) Product[1 - q^n, {n, 1, nterms}]
]

(* The three cusp forms of Gamma(7) via eta quotients.
   From Schoeneberg (1939) and Elkies (1998):

   f_a(tau) = eta(tau)^2 * Product over (n = a mod 7) and (n = -a mod 7)

   More precisely, the Klein quartic coordinates are:
   x_a(tau) = q^(a(7-a)/14) * Prod_{n>=1} (1-q^n)^{c_a(n)}
   where c_a(n) = 2 if n = 0 mod 7,
                  -1 if n = +/-a mod 7,
                  0 otherwise

   Equivalently using generalized eta products:
*)

(* Generalized eta product for pair mode a in {1,2,3} *)
kleinForm[a_, tau_, nterms_:300] := Module[
  {q = Exp[2 Pi I tau], result, n, nmod},
  (* Leading q-power: a*(7-a)/(2*7) = Havelock Casimir / N *)
  result = q^(a (NN - a)/(2 NN));
  Do[
    nmod = Mod[n, NN];
    Which[
      nmod == a || nmod == NN - a,
        result *= (1 - q^n),
      nmod == 0,
        result *= (1 - q^n)^2,
      True,
        (* no contribution *)
        Null
    ],
    {n, 1, nterms}
  ];
  (* Divide by eta(tau)^2 to get weight 2/7 form *)
  result /= (eta[tau, nterms])^2;
  result
]

(* Evaluate at CM point *)
Print["\n=== Klein quartic forms at tau_0 ==="]
{x1, x2, x3} = Table[kleinForm[a, tau0] // N, {a, {1, 2, 3}}];
Print["f_1(tau_0) = ", x1]
Print["f_2(tau_0) = ", x2]
Print["f_3(tau_0) = ", x3]
Print["|f_1| = ", Abs[x1], "  |f_2| = ", Abs[x2], "  |f_3| = ", Abs[x3]]

(* Check Klein quartic equation *)
kleinCheck = x1^3 x2 + x2^3 x3 + x3^3 x1;
Print["\nx^3 y + y^3 z + z^3 x = ", kleinCheck, " (should be 0)"]

(* ============================================================
   SECTION 2: Alternative construction using Mathematica's
   built-in modular form capabilities (v13+)
   ============================================================ *)

(* If Mathematica version >= 13, we can use: *)
(* DedekindEta is built-in *)

Print["\n=== Using built-in DedekindEta ==="]
etaBuiltin[tau_] := DedekindEta[tau]

(* The three Klein quartic coordinates via the standard construction:

   x_a(tau) = (eta(tau/7 + a/7) * eta(tau/7 + (7-a)/7)) / eta(tau)^2

   adjusted for the correct modular weight. *)

kleinBuiltin[a_, tau_] := Module[{},
  (DedekindEta[(tau + a)/7] DedekindEta[(tau + (NN - a))/7]) /
   DedekindEta[tau]^2
]

{xb1, xb2, xb3} = Table[kleinBuiltin[a, tau0] // N, {a, {1, 2, 3}}];
Print["f_1 = ", xb1]
Print["f_2 = ", xb2]
Print["f_3 = ", xb3]
Print["|f_1| = ", Abs[xb1], "  |f_2| = ", Abs[xb2], "  |f_3| = ", Abs[xb3]]

kleinCheck2 = xb1^3 xb2 + xb2^3 xb3 + xb3^3 xb1;
Print["Klein check: ", Abs[kleinCheck2]]

(* ============================================================
   SECTION 3: Try ALL standard eta quotient constructions
   ============================================================ *)

Print["\n=== Systematic eta quotient search ==="]

(* The most general level-7 eta quotient of weight 2:
   f = eta(tau)^a * eta(7*tau)^b with a+b=4 (weight 2 condition)
   and appropriate vanishing at cusps *)

(* Standard basis for S_2(Gamma_0(7)): EMPTY (dim = 0)
   But for Gamma_1(7) or Gamma(7), the space is larger. *)

(* For Gamma(7): use the MODULAR UNITS
   u_a(tau) = eta((tau+a)/7) / eta(tau)  for a = 0,...,6
   These satisfy the modular unit relations. *)

(* The Klein quartic parametrization (Elkies):
   X = -u_1 u_6, Y = -u_2 u_5, Z = -u_3 u_4
   where u_a = q^{B_2(a/7)/2} Prod_{n>=1} (1-q^{7n+a})(1-q^{7n-a})/(1-q^n)^2
*)

kleinElkies[a_, tau_, nterms_:500] := Module[
  {q = Exp[2 Pi I tau], b2, result, n},
  b2 = (a/NN)^2 - (a/NN) + 1/6;
  result = q^(b2/2);
  Do[
    result *= (1 - q^(NN n + a)) (1 - q^(NN n + (NN - a))) / (1 - q^n)^2,
    {n, 1, nterms}
  ];
  (* Also the n=0 terms for the first factors *)
  result *= (1 - q^a) (1 - q^(NN - a));
  result
]

Print["\n=== Elkies construction: X = -u_1*u_6, etc. ==="]
Do[
  ua = kleinElkies[a, tau0];
  Print["u_", a, "(tau_0) = ", ua, "  |u_", a, "| = ", Abs[ua]],
  {a, 1, 3}
]

(* The Klein quartic coordinates: X_m = -u_m * u_{7-m} *)
X1e = -kleinElkies[1, tau0] kleinElkies[6, tau0];
X2e = -kleinElkies[2, tau0] kleinElkies[5, tau0];
X3e = -kleinElkies[3, tau0] kleinElkies[4, tau0];

Print["\nX_1 = ", X1e, "  |X_1| = ", Abs[X1e]]
Print["X_2 = ", X2e, "  |X_2| = ", Abs[X2e]]
Print["X_3 = ", X3e, "  |X_3| = ", Abs[X3e]]

kleinCheck3 = X1e^3 X2e + X2e^3 X3e + X3e^3 X1e;
Print["\nKlein check: |x^3y + y^3z + z^3x| = ", Abs[kleinCheck3]]

(* ============================================================
   SECTION 4: Build PMNS from the modular form values
   ============================================================ *)

Print["\n=== PMNS construction ==="]

(* Use whichever (X1, X2, X3) satisfies the Klein quartic best *)
(* Try the Elkies construction first *)
{XX, YY, ZZ} = {X1e, X2e, X3e};

(* PSL(2,7) 3D irrep generators *)
omega7 = Exp[2 Pi I/7];
QR = {1, 2, 4};

(* T generator (order 7): diagonal *)
Tgen = DiagonalMatrix[omega7^# & /@ QR];

(* S generator (Fricke involution): *)
Sgen = Table[
  2 I Sin[2 Pi QR[[a]] QR[[b]]/NN] / Sqrt[NN],
  {a, 3}, {b, 3}
];

(* F_3 = DFT on Z_3 (TBM base) *)
omega3 = Exp[2 Pi I/3];
F3 = Table[omega3^((a-1)(b-1)), {a, 3}, {b, 3}] / Sqrt[3];

(* Majorana mass matrix: symmetric product 3 x 3 -> 6 *)
(* Standard CG for PSL(2,7): M_nu = [[2x,-z,-y],[-z,2y,-x],[-y,-x,2z]] *)
Mnu = {{2 XX, -ZZ, -YY}, {-ZZ, 2 YY, -XX}, {-YY, -XX, 2 ZZ}};

(* Also try the circulant: M_cl = x I + y P + z P^2 *)
P3mat = {{0, 0, 1}, {1, 0, 0}, {0, 1, 0}};
Mcl = XX IdentityMatrix[3] + YY P3mat + ZZ P3mat.P3mat;

(* Diagonalize both *)
{evCl, UCl} = Eigensystem[ConjugateTranspose[Mcl].Mcl];
UCl = Transpose[UCl[[Ordering[Re[evCl]]]]];

{evNu, UNu} = Eigensystem[Mnu];
UNu = Transpose[UNu[[Ordering[Abs[evNu]]]]];

(* PMNS candidates *)
extractAngles[V_] := Module[{s13, c13, s12, s23},
  s13 = Min[Abs[V[[1, 3]]], 0.999];
  c13 = Sqrt[1 - s13^2];
  s12 = If[c13 > 10^-10, Min[Abs[V[[1, 2]]]/c13, 0.999], 0];
  s23 = If[c13 > 10^-10, Min[Abs[V[[2, 3]]]/c13, 0.999], 0];
  {ArcSin[s12] 180/Pi, ArcSin[s23] 180/Pi, ArcSin[s13] 180/Pi}
]

(* Try multiple PMNS constructions *)
Print["\n--- PMNS = U_cl^dag x U_nu (circulant x symmetric) ---"]
VPMNS1 = ConjugateTranspose[UCl].UNu;
angles1 = extractAngles[VPMNS1 // N];
Print["theta_12 = ", angles1[[1]], "  theta_23 = ", angles1[[2]], "  theta_13 = ", angles1[[3]]]
Print["Delta = ", Abs[angles1[[1]] - 33.4] + Abs[angles1[[2]] - 49.0] + Abs[angles1[[3]] - 8.5]]

Print["\n--- PMNS = F3^dag x U_nu ---"]
VPMNS2 = ConjugateTranspose[F3].UNu;
angles2 = extractAngles[VPMNS2 // N];
Print["theta_12 = ", angles2[[1]], "  theta_23 = ", angles2[[2]], "  theta_13 = ", angles2[[3]]]

Print["\n--- PMNS = S^dag x U_nu (Fricke x symmetric) ---"]
VPMNS3 = ConjugateTranspose[Sgen].UNu;
angles3 = extractAngles[VPMNS3 // N];
Print["theta_12 = ", angles3[[1]], "  theta_23 = ", angles3[[2]], "  theta_13 = ", angles3[[3]]]

(* ============================================================
   SECTION 5: Scan over modular parameter tau
   ============================================================ *)

Print["\n=== Scan: vary tau near CM point ==="]
Print["Looking for tau that gives Z_7 PMNS fractions:"]
Print["  sin^2(theta_23) = 4/7, sin^2(2 theta_12) = 6/7, sin^2(theta_13) = 1/48"]

target = {33.90, 49.11, 8.30};

(* Define PMNS as function of tau *)
pmnsAngles[tau_] := Module[
  {q, x, y, z, Mcl2, Mnu2, evC, UC, evN, UN, V},

  (* Evaluate Klein quartic forms *)
  x = kleinBuiltin[1, tau];
  y = kleinBuiltin[2, tau];
  z = kleinBuiltin[3, tau];

  (* Charged lepton: circulant *)
  Mcl2 = x IdentityMatrix[3] + y P3mat + z P3mat.P3mat;
  {evC, UC} = Eigensystem[ConjugateTranspose[Mcl2].Mcl2];
  UC = Transpose[UC[[Ordering[Re[evC]]]]];

  (* Neutrino: symmetric product *)
  Mnu2 = {{2 x, -z, -y}, {-z, 2 y, -x}, {-y, -x, 2 z}};
  {evN, UN} = Eigensystem[Mnu2];
  UN = Transpose[UN[[Ordering[Abs[evN]]]]];

  V = ConjugateTranspose[UC].UN;
  extractAngles[V // N]
]

(* Scan along the imaginary axis near tau_0 *)
Print["\nScan: tau = 1/2 + i*t for t near Sqrt[7]/2"]
Do[
  tau = 1/2 + I t;
  angles = Quiet[pmnsAngles[tau]];
  score = Total[Abs[angles - target]];
  If[score < 30,
    Print["  t = ", t // N, ": theta_12 = ", angles[[1]] // N,
          "  theta_23 = ", angles[[2]] // N, "  theta_13 = ", angles[[3]] // N,
          "  Delta = ", score // N]
  ],
  {t, 0.5, 3.0, 0.1}
]

(* ============================================================
   SECTION 6: The SU(2)_5 cross-sector approach
   ============================================================ *)

Print["\n=== SU(2)_5 cross-sector S-matrix ==="]
(* Full 6x6 S-matrix *)
Sfull = Table[
  Sqrt[2/NN] Sin[Pi (2 j + 1)(2 l + 1)/NN],
  {j, {0, 1/2, 1, 3/2, 2, 5/2}},
  {l, {0, 1/2, 1, 3/2, 2, 5/2}}
];

(* Cross-sector: rows = integer {0,1,2}, cols = half-integer {1/2,3/2,5/2} *)
Scross = Sfull[[{1, 3, 5}, {2, 4, 6}]];
Print["S_cross = "]
Print[MatrixForm[Scross // N]]

(* Normalize rows *)
Snorm = Table[Scross[[i]]/Norm[Scross[[i]]], {i, 3}];
Print["\nNormalized: "]
Print[MatrixForm[Snorm // N]]

(* Extract PMNS angles for all permutations *)
Print["\nBest permutations:"]
bestScore = 999;
Do[
  Uperm = Snorm[[rp, cp]] // N;
  angles = extractAngles[Uperm];
  score = Total[Abs[angles - target]];
  If[score < 25,
    Print["  r=", rp, " c=", cp, ": theta_12=", angles[[1]],
          " theta_23=", angles[[2]], " theta_13=", angles[[3]], " Delta=", score];
    If[score < bestScore, bestScore = score]
  ],
  {rp, Permutations[{1, 2, 3}]},
  {cp, Permutations[{1, 2, 3}]}
]

(* ============================================================
   SECTION 7: Direct check of Z_7 fraction formulas
   ============================================================ *)

Print["\n=== Z_7 PMNS predictions ==="]
Print["sin^2(2 theta_12) = (N-1)/N = ", (NN-1)/NN, " -> theta_12 = ",
      ArcSin[Sqrt[(1 - 1/Sqrt[NN])/2]] 180/Pi // N, " deg"]
Print["sin^2(theta_23)   = (N+1)/(2N) = ", (NN+1)/(2 NN), " -> theta_23 = ",
      ArcSin[Sqrt[(NN+1)/(2 NN)]] 180/Pi // N, " deg"]
Print["sin^2(theta_13)   = 1/(N^2-1) = ", 1/(NN^2-1), " -> theta_13 = ",
      ArcSin[Sqrt[1/(NN^2-1)]] 180/Pi // N, " deg"]

Print["\nPDG 2024: theta_12 = 33.41 +/- 0.79"]
Print["PDG 2024: theta_23 = 49.0  +/- 1.3"]
Print["PDG 2024: theta_13 = 8.54  +/- 0.15"]

Print["\n=== DONE ==="]
Print["Run this in Mathematica 13+ for DedekindEta support."]
Print["Key outputs to check:"]
Print["  1. Do the Klein quartic forms satisfy x^3 y + y^3 z + z^3 x = 0?"]
Print["  2. What PMNS angles emerge from circulant x symmetric texture?"]
Print["  3. Does scanning tau find a value matching the Z_7 fractions?"]
