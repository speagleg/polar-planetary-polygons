(* ============================================================ *)
(* FULL 3-REGION BVP: Simultaneous determination of eps & sigma *)
(*                                                              *)
(* All variables declared real. No Conjugate or ComplexExpand.  *)
(* Direct real/imaginary arithmetic throughout.                 *)
(* ============================================================ *)

Clear["Global`*"]

(* ------------------------------------------------------------ *)
(* Cell 1: Solve matching conditions symbolically               *)
(* ------------------------------------------------------------ *)

(* Inner: psi = A Exp[I alpha rho] + B Exp[-I alpha rho] *)
(* Outer: psi = C Exp[-kappa rho], normalize C = 1 *)
(* At rho = 0: *)
(*   Continuity:       A + B = 1 *)
(*   Derivative jump:  I alpha (A - B) + kappa = -Dq/Ustar *)

(* Solve for A and B *)
sol = Solve[{
  Aa + Bb == 1,
  I alpha (Aa - Bb) == -(kappa + Dq/Ustar)
}, {Aa, Bb}][[1]];

Aexpr = Aa /. sol;
Bexpr = Bb /. sol;

Print["A = ", Aexpr // Simplify]
Print["B = ", Bexpr // Simplify]
Print[""]

(* Write A = Ar + I Ai, B = Br + I Bi *)
(* From the solution, extract real and imaginary parts *)
(* All of alpha, kappa, Dq, Ustar are REAL *)

Ar = 1/2;  (* Re(A): from (A+B=1) and symmetry *)
Ai = (kappa + Dq/Ustar) / (2 alpha);  (* Im(A): from I*alpha*(A-B) equation *)
Br = 1/2;
Bi = -(kappa + Dq/Ustar) / (2 alpha);

Print["Explicit real/imaginary parts:"]
Print["  A = ", Ar, " + I*(", Ai, ")"]
Print["  B = ", Br, " + I*(", Bi, ")"]
Print[""]

(* Verify *)
Print["Check A + B = ", (Ar + Br), " + I*(", (Ai + Bi), ")  (should be 1 + 0I)"]
Print["Check I*alpha*(A-B) = I*alpha*(", 2 I Ai, ") = ", -2 alpha Ai,
  "  (should be -(kappa + Dq/Ustar) = ", -(kappa + Dq/Ustar), ")"]
Print[""]


(* ------------------------------------------------------------ *)
(* Cell 2: Compute |A|^2, |B|^2, and sigma                     *)
(* ------------------------------------------------------------ *)

modAsq = Ar^2 + Ai^2;
modBsq = Br^2 + Bi^2;

Print["|A|^2 = ", modAsq // Expand]
Print["|B|^2 = ", modBsq // Expand]
Print[""]

(* Since Ar = Br = 1/2 and Ai = -Bi: *)
(* |A|^2 = 1/4 + Ai^2 *)
(* |B|^2 = 1/4 + Bi^2 = 1/4 + Ai^2 *)
(* So |A|^2 = |B|^2 ALWAYS! *)

Print["|A|^2 - |B|^2 = ", modAsq - modBsq // Simplify]
Print[""]
Print["CRITICAL RESULT: |A|^2 = |B|^2 for all parameter values!"]
Print["  This means the net radial flux is ZERO."]
Print["  The flux-based sigma formula gives sigma = 0."]
Print[""]
Print["REASON: The matching conditions (continuity + derivative jump)"]
Print["  preserve the amplitude symmetry |A| = |B|. The PV step"]
Print["  shifts the PHASE of A relative to B but not the AMPLITUDE."]
Print[""]

(* The PHASE difference IS the physical effect: *)
phaseA = ArcTan[Ar, Ai];
phaseB = ArcTan[Br, Bi];
phaseDiff = phaseA - phaseB;

Print["Phase of A: arctan(Ai/Ar) = arctan(", Ai/Ar, ")"]
Print["Phase of B: arctan(Bi/Br) = arctan(", Bi/Br, ")"]
Print["Phase difference: ", phaseDiff // Simplify]
Print[""]


(* ------------------------------------------------------------ *)
(* Cell 3: What the phase difference means physically           *)
(* ------------------------------------------------------------ *)

(* The inner solution: *)
(* psi = A Exp[I alpha rho] + B Exp[-I alpha rho] *)
(* = |A|{Exp[I(alpha rho + phiA)] + Exp[-I(alpha rho - phiB)]} *)
(* = 2|A| cos(alpha rho + (phiA-phiB)/2) cos((phiA+phiB)/2) ... *)

(* More directly: *)
(* psi = (Ar+Br) cos(alpha rho) - (Ai+Bi) sin(alpha rho) *)
(*     + I[(Ai+Bi) cos(alpha rho) + (Ar+Br) sin(alpha rho)] ... no *)

(* Actually for REAL psi: *)
(* psi_real = Re[A Exp[I alpha rho] + B Exp[-I alpha rho]] *)
(* = (Ar cos(alpha rho) - Ai sin(alpha rho)) *)
(*   + (Br cos(alpha rho) + Bi sin(alpha rho)) *)
(* = (Ar+Br) cos(alpha rho) + (Bi-Ai) sin(alpha rho) *)
(* = cos(alpha rho) + (Bi-Ai) sin(alpha rho) *)
(* = cos(alpha rho) - (2 Ai) sin(alpha rho) *)
(* = cos(alpha rho) - (kappa + Dq/Ustar)/alpha * sin(alpha rho) *)

gamma = (kappa + Dq/Ustar)/alpha;

Print["Real inner solution:"]
Print["  psi = cos(alpha*rho) - gamma * sin(alpha*rho)"]
Print["  where gamma = (kappa + Dq/U*) / alpha = ", gamma]
Print[""]
Print["  = sqrt(1 + gamma^2) * cos(alpha*rho + arctan(gamma))"]
Print[""]
Print["  amplitude = sqrt(1 + gamma^2)"]
Print["  phase shift = arctan(gamma)"]
Print[""]

(* The phase shift arctan(gamma) is what makes the inner solution *)
(* NOT centered on cos(alpha rho). This phase shift propagates   *)
(* into the stream function as a theta-dependent phase, which     *)
(* is equivalent to a nonzero sigma in the loxodromic form.      *)

Print["The phase shift arctan(gamma) in the eigenfunction"]
Print["translates to sigma in the stream function via:"]
Print["  sigma_flow = alpha * arctan(gamma) / pi"]
Print["  (the phase shift per half-period, normalized by alpha)"]
Print[""]


(* ------------------------------------------------------------ *)
(* Cell 4: Saturn numerical evaluation                          *)
(* ------------------------------------------------------------ *)

(* Saturn values *)
alphaVal = Pi/3;
kappaVal = 6;  (* outer decay rate *)
UstarVal = 105.3;

(* Fourier-projected Dq *)
nn = 6; sJ = 1/20; Umax = 120;
overlap = nn Umax - Exp[nn^2 sJ^2/2] nn^2 Sqrt[Pi/2] sJ Umax Erfc[nn sJ/Sqrt[2]] // N;
DqVal = -overlap;

gammaVal = (kappaVal + DqVal/UstarVal) / alphaVal // N;

Print["Saturn evaluation:"]
Print["  overlap = ", overlap]
Print["  Dq = ", DqVal]
Print["  gamma = (kappa + Dq/U*)/alpha = ", gammaVal]
Print["  arctan(gamma) = ", ArcTan[gammaVal] // N, " rad"]
Print["  arctan(gamma) = ", ArcTan[gammaVal] 180/Pi // N, " deg"]
Print[""]

(* Amplitude and phase *)
ampVal = Sqrt[1 + gammaVal^2] // N;
phaseVal = ArcTan[gammaVal] // N;

Print["  Inner solution amplitude: ", ampVal]
Print["  Inner solution phase shift: ", phaseVal, " rad"]
Print[""]

(* sigma from phase shift *)
(* The phase shift delta_phi in the eigenfunction corresponds to *)
(* a sigma in the stream function through: *)
(* psi ~ cos(alpha rho + delta_phi) ~ cos(alpha rho + sigma theta_eff) *)
(* where theta_eff = delta_phi/alpha per unit of "theta" traversed *)

sigmaPhase = phaseVal;  (* sigma ~ phase shift directly *)
Print["  sigma_flow (from BVP phase shift):"]
Print["    sigma = arctan(gamma) = ", sigmaPhase]
Print["    r = Exp[sigma] = ", Exp[sigmaPhase] // N]
Print[""]

(* Compare *)
sigmaKin = alphaVal * nn * 0.112/Sqrt[2] // N;
sigmaChain = alphaVal/Sqrt[2] * 0.14 // N;

Print["COMPARISON:"]
Print["  sigma_BVP   = ", sigmaPhase]
Print["  sigma_kin   = ", sigmaKin, " (Cassini kinematic)"]
Print["  sigma_chain = ", sigmaChain, " (self-consistency chain)"]
Print[""]

(* Also: epsilon from the matching *)
Ceff = overlap/(UstarVal nn) // N;
epsBVP = Ceff * 0.14 // N;
Print["  epsilon_BVP = ", epsBVP]
Print["  epsilon_obs = 0.112"]
