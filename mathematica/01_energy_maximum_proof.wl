(* ============================================================ *)
(* PROVE: H''[0] < 0 for all N >= 3                            *)
(*                                                              *)
(* H[sigma] = -Sum_{j<k} Log|z_j[sigma] - z_k[sigma]|         *)
(* z_k[sigma] = R Exp[sigma k/N] Exp[2 Pi I k/N]              *)
(*                                                              *)
(* Goal: compute H''[0] analytically as a function of N         *)
(* and show it is negative for all N >= 3.                      *)
(* ============================================================ *)

Clear["Global`*"]

(* ------------------------------------------------------------ *)
(* Cell 1: H[sigma] symbolically for general N                  *)
(* ------------------------------------------------------------ *)

(* z_k = R Exp[sigma k/NN] Exp[2 Pi I k/NN]                    *)
(* |z_j - z_k|^2 = R^2 |Exp[sigma j/NN] Exp[2Pi I j/NN]       *)
(*                       - Exp[sigma k/NN] Exp[2Pi I k/NN]|^2  *)
(*                                                              *)
(* Factor out Exp[sigma j/NN]:                                  *)
(* = R^2 Exp[2 sigma j/NN] |1 - Exp[sigma[k-j]/NN] Exp[2Pi I [k-j]/NN]|^2 *)
(*                                                              *)
(* Let m = k - j, then for the ring:                            *)
(* |z_j - z_k|^2 = R^2 Exp[2 sigma j/NN] *                    *)
(*   |1 - Exp[sigma m/NN] Exp[2 Pi I m/NN]|^2                  *)

(* H = -Sum_{j<k} Log|z_j - z_k|                               *)
(*   = -(1/2) Sum_{j<k} Log|z_j - z_k|^2                       *)

(* At sigma = 0: z_k = R Exp[2 Pi I k/NN]                      *)
(* |z_j - z_k|^2 = R^2 |1 - Exp[2 Pi I m/NN]|^2               *)
(*               = R^2 * 4 Sin[Pi m/NN]^2                       *)

Print["STEP 1: H at sigma = 0"]
Print["  |z_j - z_k|^2 = 4 R^2 Sin[Pi m/N]^2, m = k-j"]
Print["  H[0] = -Sum_{m=1}^{N-1} [N-m]/2 * Log[2 R Sin[Pi m/N]]"]
Print[""]

(* ------------------------------------------------------------ *)
(* Cell 2: Compute d^2/dsigma^2 of Log|z_j - z_k|^2 at sigma=0 *)
(* ------------------------------------------------------------ *)

(* |z_j - z_k|^2 with the loxodromic deformation:               *)
(* Let u = sigma/NN, phi_m = 2 Pi m/NN                          *)
(* z_j - z_k = R Exp[u j] Exp[I phi_j] [1 - Exp[u m] Exp[I phi_m]] *)
(*                                                              *)
(* |z_j - z_k|^2 = R^2 Exp[2 u j] *                            *)
(*   [1 - Exp[u m] Cos[phi_m]]^2 + [Exp[u m] Sin[phi_m]]^2     *)
(* = R^2 Exp[2 u j] * [1 - 2 Exp[u m] Cos[phi_m] + Exp[2 u m]] *)

(* Define F[u,m] = Log[1 - 2 Exp[u m] Cos[phi_m] + Exp[2 u m]] *)
(* where phi_m = 2 Pi m / NN and u = sigma/NN                   *)

(* H[sigma] = -(1/2) Sum_{j<k} Log|z_j-z_k|^2                  *)
(*          = -(1/2) Sum_{j<k} [2 u j + Log R^2 + F[u,m]]      *)

(* The F term depends only on m = k-j.                          *)
(* The 2 u j term sums over all pairs.                          *)

(* We need d^2H/dsigma^2 at sigma=0.                            *)
(* Since u = sigma/NN, d/dsigma = [1/NN] d/du                   *)
(* d^2/dsigma^2 = [1/NN^2] d^2/du^2                             *)

(* Focus on F[u,m]: *)
phim[m_, NN_] := 2 Pi m/NN;

Fexpr[u_, m_, NN_] := Log[1 - 2 Exp[u m] Cos[phim[m, NN]] + Exp[2 u m]];

(* d^2F/du^2 at u = 0 *)
d2Fdu2[m_, NN_] := D[Fexpr[u, m, NN], {u, 2}] /. u -> 0 // FullSimplify;

Print["STEP 2: d^2F/du^2 at u=0 for each m"]
Print[""]

(* Compute for small N to see the pattern *)
Do[
  Print["N=", nn, ":"];
  Do[
    Module[{val = d2Fdu2[m, nn]},
      Print["  m=", m, ": d^2F/du^2 = ", val // Simplify]
    ],
    {m, 1, nn - 1}
  ];
  Print[""],
  {nn, {3, 4, 5, 6}}
]

(* ------------------------------------------------------------ *)
(* Cell 3: Sum over all pairs to get H''[0]                     *)
(* ------------------------------------------------------------ *)

(* H''[0] = -(1/2) * [1/NN^2] * Sum of pair contributions      *)
(* Each pair [j,k] with m=k-j contributes:                      *)
(*   d^2/du^2 [2 u j + F[u,m]] = 0 + d^2F/du^2[m]             *)
(* Wait: d^2[2uj]/du^2 = 0 since 2uj is linear in u.           *)
(*                                                              *)
(* Actually d[2uj]/du = 2j, d^2/du^2 = 0. Correct.             *)
(*                                                              *)
(* Number of pairs with separation m: [N-m] for m=1,...,N-1     *)
(* H''[0] = -[1/[2 NN^2]] Sum_{m=1}^{N-1} [NN-m] d^2F/du^2[m] *)

Hpp[NN_] := Module[{total = 0},
  Do[
    total += (NN - m) d2Fdu2[m, NN],
    {m, 1, NN - 1}
  ];
  -total / (2 NN^2)
];

Print["STEP 3: H''[0] for each N"]
Print[""]
Do[
  Module[{val = Hpp[nn] // FullSimplify},
    Print["N=", nn, ": H''[0] = ", val // N, "  negative? ", val < 0]
  ],
  {nn, 3, 12}
]
Print[""]

(* ------------------------------------------------------------ *)
(* Cell 4: Look for a closed form                               *)
(* ------------------------------------------------------------ *)

Print["STEP 4: Look for pattern in H''[0]"]
Print[""]
Do[
  Module[{val = Hpp[nn] // FullSimplify},
    Print["N=", nn, ": H''[0] = ", val // N,
      ",  H''[0] * N^2 = ", val nn^2 // N]
  ],
  {nn, 3, 9}
]
Print[""]
Print["If H''[0] * N^2 has a recognizable pattern,"]
Print["we can prove H''[0] < 0 for all N >= 3."]
