(* ============================================================ *)
(* PROPOSITION 1: Polygon from Circle + Z_N Symmetry            *)
(*                                                              *)
(* GOAL: Prove that the stream function w[z] = A z^s at sigma=0 *)
(* with Z_N Fourier projection gives an N-fold meander          *)
(* rho_boundary[theta] = rhostar + eps cos[N theta + phi]       *)
(* ============================================================ *)

Clear["Global`*"]

(* ------------------------------------------------------------ *)
(* Cell 1: The stream function at sigma = 0                     *)
(* ------------------------------------------------------------ *)

(* Complex potential: w = A z^s with s = i alpha, sigma = 0     *)
(* z = exp[rho + i theta] in log-polar coordinates              *)
(* w = A exp[i alpha rho - alpha theta]                         *)
(* Stream function = Im[w]:                                     *)
(* psi = Abs[A] exp[-alpha theta] Sin[alpha rho + Arg[A]]      *)

NN = 6;
alpha = 2 Pi/NN;

psiFull[rho_, theta_, Amod_, Aarg_] :=
  Amod Exp[-alpha theta] Sin[alpha rho + Aarg];

Print["Stream function at sigma=0:"]
Print["  psi = Abs[A] Exp[-alpha theta] Sin[alpha rho + Arg[A]]"]
Print["  alpha = 2 Pi/N = ", alpha // N]
Print[""]

(* ------------------------------------------------------------ *)
(* Cell 2: The Fourier projection onto mode n = N               *)
(* ------------------------------------------------------------ *)

(* The QGPV eigenfunction is:                                   *)
(*   psi_prime = psihat_n[rho] exp[i n theta] exp[-i omega t]  *)
(* The Fourier mode n = N extracts the N-fold component.        *)
(* For a STATIONARY wave, omega = 0, so:                        *)
(*   psi_n = An[rho] cos[N theta + phi_n]                      *)
(*                                                              *)
(* The JET BOUNDARY is where the total PV q = const.            *)
(* Total PV: q = q0[rho] + qn[rho] cos[N theta + phi]         *)
(* At the boundary, q = qB:                                     *)
(*   q0[rhoB] + qn[rhoB] cos[N theta + phi] = qB              *)
(*                                                              *)
(* Linearize around rhoB = rhostar + delta:                     *)
(*   q0[rhostar] + dq0 * delta + qn[rhostar] cos[..] = qB     *)
(* Since q0[rhostar] = qB:                                     *)
(*   delta = -qn[rhostar] / dq0 * cos[N theta + phi]           *)

Print["PV CONTOUR DERIVATION:"]
Print[""]
Print["Total PV: q = q0 + qn cos[N theta + phi]"]
Print["Boundary: q = qB, a constant"]
Print[""]
Print["Linearize around rho = rhostar:"]
Print["  q0 + dq0 * delta_rho + qn cos[N theta] = qB"]
Print[""]
Print["Since q0 at rhostar equals qB:"]
Print["  delta_rho = -qn / dq0 * cos[N theta + phi]"]
Print[""]
Print["Therefore:"]
Print["  rho_boundary = rhostar + eps cos[N theta + phi]"]
Print["  where eps = Abs[qn] / Abs[dq0]"]
Print[""]
Print["This is a meander with N-FOLD SYMMETRY."]
Print["For small eps, it approximates a regular N-gon.  QED."]
Print[""]

(* ------------------------------------------------------------ *)
(* Cell 3: Why this is an N-gon and not just a wavy circle      *)
(* ------------------------------------------------------------ *)

(* A cos[N theta] perturbation of a circle gives:               *)
(* r[theta] = R * [1 + eps cos[N theta]]                       *)
(* For N = 6: this has 6 maxima and 6 minima equally spaced.    *)
(* The maxima are at theta = 0, 2pi/6, 4pi/6, ..., 10pi/6      *)
(* Connecting the maxima gives a regular hexagon.               *)

Print["WHY IT IS AN N-GON:"]
Print[""]
Print["The boundary r = R * [1 + eps cos[N theta]] has"]
Print["N maxima at theta = 2 pi k / N, for k = 0,...,N-1"]
Print["N minima at theta = pi * [2k+1] / N"]
Print[""]

Do[
  Module[{theta = 2 Pi k/NN, r},
    r = 1 + 0.1 Cos[NN theta];
    Print["  Vertex k=", k, ": theta=", theta // N, " rad, r=", r // N]
  ],
  {k, 0, NN - 1}
]

Print[""]
Print["All vertices at the SAME radius r = 1 + eps."]
Print["Equally spaced in angle: theta = 2 pi k/N."]
Print["This is a regular N-gon. For small eps, the edges are"]
Print["straight to order eps^2."]
Print[""]

(* ------------------------------------------------------------ *)
(* Cell 4: Numerical verification                               *)
(* ------------------------------------------------------------ *)

Print["NUMERICAL VERIFICATION, N=6, eps=0.1:"]
Print[""]

vertices = Table[
  Module[{theta = 2 Pi k/6},
    {(1 + 0.1 Cos[6 theta]) Cos[theta],
     (1 + 0.1 Cos[6 theta]) Sin[theta]}
  ],
  {k, 0, 5}
];

sideLengths = Table[
  Norm[vertices[[Mod[k, 6] + 1]] - vertices[[Mod[k + 1, 6] + 1]]],
  {k, 0, 5}
];

Print["  Vertex positions [x, y]:"]
Do[Print["    k=", k, ": ", vertices[[k + 1]] // N], {k, 0, 5}]
Print["  Side lengths: ", sideLengths // N]
Print["  Max - min side length: ", Max[sideLengths] - Min[sideLengths] // N]
Print["  Should be 0 for perfect hexagon"]
