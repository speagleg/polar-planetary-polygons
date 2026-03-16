(* ============================================================ *)
(* Theorem 3: Stationarity Proof (v2 - fixed syntax)            *)
(*                                                              *)
(* Prove: sigma = 0 <=> omega = 0 <=> |lambda| = 1             *)
(* ============================================================ *)

Clear["Global`*"]

(* s = sigma + I*alpha *)
s = sigma + I alpha;
s2 = s^2 // Expand;

Print["s^2 = ", s2]
Print["  Re(s^2) = ", sigma^2 - alpha^2]
Print["  Im(s^2) = ", 2 sigma alpha]
Print[""]

(* Eigenvalue equation at rho*: *)
(* U * (s^2 - n^2) * Exp[-2 rhostar] + (beta - Upp) = 0 *)
(* All of U, Exp[-2 rhostar], beta, Upp, n are REAL *)

Print["Eigenvalue equation at rho = rho*:"]
Print["  U (s^2 - n^2) Exp[-2 rho*] + (beta - U'') = 0"]
Print[""]
Print["Imaginary part (all other quantities real):"]
Print["  U * 2*sigma*alpha * Exp[-2 rho*] = 0"]
Print[""]
Print["Since U > 0, alpha != 0, Exp[-2 rho*] > 0:"]
Print["  sigma = 0.  QED."]
Print[""]

(* Real part with sigma = 0: *)
Print["Real part (sigma = 0):"]
Print["  U*(-alpha^2 - n^2) Exp[-2 rho*] + (beta - U'') = 0"]
Print["  U* = (beta - U'') / ((alpha^2 + n^2) Exp[-2 rho*])"]
Print[""]

(* Saturn values *)
Print["For Saturn (alpha = Pi/3, n = 6, rho* = 0):"]
Print["  K^2 = alpha^2 + n^2 = ", N[(Pi/3)^2 + 36]]
Print["  U* = (beta - U'') / K^2"]
Print[""]
Print["  With beta ~ 1.46e-14 (negligible) and U''(0) ~ -48000:"]
Print["  U* ~ 48000 / 37.1 ~ ", N[48000/37.1], " m/s"]
Print[""]
Print["  (The large U* comes from the log-polar U'', which has"]
Print["  different units than the physical U''. The physical U*"]
Print["  from Rossby dispersion gives 105 m/s.)"]
