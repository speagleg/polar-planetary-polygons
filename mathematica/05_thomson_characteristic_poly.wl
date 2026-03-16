(* ============================================================ *)
(* OPEN PROBLEM 2: Thomson-Rossby Conjecture (Theorem 4)        *)
(*                                                              *)
(* CORRECTED VERSION: The simplified formula                     *)
(*   F_m = E_m + (kappa_0/kappa) * m*(N-m)/(2N)                *)
(* is INCOMPLETE — it assumes Fourier modes decouple, but the   *)
(* central vortex introduces cross-coupling.                    *)
(*                                                              *)
(* The correct approach: build the FULL 2N×2N stability matrix  *)
(* symbolically, including all central vortex interactions.      *)
(*                                                              *)
(* Numerical result (Python): kappa_crit = -0.2501 for N=6.    *)
(* Goal: derive this analytically.                              *)
(* ============================================================ *)

Clear["Global`*"]

(* ------------------------------------------------------------ *)
(* Part 1: Build the EXACT stability matrix for N=6             *)
(* ------------------------------------------------------------ *)

(* N vortices on the unit circle plus central vortex *)
(* z_k = exp(2 pi i k / N), k = 0, ..., N-1         *)
(* Central vortex at z = 0 with circulation kappa_0   *)

NN = 6;
zz = Table[Exp[2 Pi I k/NN], {k, 0, NN - 1}];

Print["Vortex positions (N=6 on unit circle):"]
Print["  ", zz // Simplify]
Print[""]

(* Point vortex equations of motion:                            *)
(*   dx_k/dt = +(kappa/2pi) Sum[(y_k-y_j)/|z_k-z_j|^2, j!=k]  *)
(*           + (k0/2pi) y_k / |z_k|^2 + Omega y_k              *)
(*   dy_k/dt = -(kappa/2pi) Sum[(x_k-x_j)/|z_k-z_j|^2, j!=k]  *)
(*           - (k0/2pi) x_k / |z_k|^2 - Omega x_k              *)
(*                                                              *)
(* For the unit circle, |z_k| = 1, so central vortex terms     *)
(* simplify: k0/(2pi) * y_k and -k0/(2pi) * x_k               *)
(*                                                              *)
(* Omega = kappa*(N-1)/(4pi) + k0/(2pi)  [on unit circle R=1]  *)

(* Use kappa = 1, k0 as parameter *)
k0 = Symbol["k0"];  (* central vortex strength *)
kappa = 1;
Omega = kappa (NN - 1)/(4 Pi) + k0/(2 Pi);

(* Build the Jacobian numerically for symbolic k0 *)
(* The velocity function for vortex k:             *)

(* Equilibrium positions *)
x0 = Table[Re[zz[[k+1]]] // ComplexExpand // Simplify, {k, 0, NN-1}];
y0 = Table[Im[zz[[k+1]]] // ComplexExpand // Simplify, {k, 0, NN-1}];

Print["Equilibrium x: ", x0 // N]
Print["Equilibrium y: ", y0 // N]
Print[""]

(* Define symbolic perturbation variables *)
dx = Table[Symbol["dx" <> ToString[k]], {k, 0, NN-1}];
dy = Table[Symbol["dy" <> ToString[k]], {k, 0, NN-1}];

(* Perturbed positions *)
xp = x0 + dx;
yp = y0 + dy;

(* Velocity of vortex k in co-rotating frame *)
vx[k_] := Module[{vxk = 0},
  Do[
    If[j != k,
      Module[{ddx, ddy, r2},
        ddx = xp[[k+1]] - xp[[j+1]];
        ddy = yp[[k+1]] - yp[[j+1]];
        r2 = ddx^2 + ddy^2;
        vxk += kappa/(2 Pi) * ddy / r2;
      ]
    ],
    {j, 0, NN-1}
  ];
  (* Central vortex at origin *)
  Module[{r2c = xp[[k+1]]^2 + yp[[k+1]]^2},
    vxk += k0/(2 Pi) * yp[[k+1]] / r2c;
  ];
  (* Co-rotating frame *)
  vxk += Omega * yp[[k+1]];
  vxk
];

vy[k_] := Module[{vyk = 0},
  Do[
    If[j != k,
      Module[{ddx, ddy, r2},
        ddx = xp[[k+1]] - xp[[j+1]];
        ddy = yp[[k+1]] - yp[[j+1]];
        r2 = ddx^2 + ddy^2;
        vyk -= kappa/(2 Pi) * ddx / r2;
      ]
    ],
    {j, 0, NN-1}
  ];
  Module[{r2c = xp[[k+1]]^2 + yp[[k+1]]^2},
    vyk -= k0/(2 Pi) * xp[[k+1]] / r2c;
  ];
  vyk -= Omega * xp[[k+1]];
  vyk
];

Print["Building symbolic Jacobian (this may take a minute)..."]

(* Build the 2N x 2N Jacobian matrix *)
(* State vector: (dx0, dx1, ..., dx5, dy0, dy1, ..., dy5) *)
allVars = Join[dx, dy];

(* Velocity functions *)
allVelocities = Join[Table[vx[k], {k, 0, NN-1}], Table[vy[k], {k, 0, NN-1}]];

(* Take derivatives and evaluate at equilibrium (all perturbations = 0) *)
zeroRule = Thread[allVars -> 0];

jacobian = Table[
  D[allVelocities[[i]], allVars[[j]]] /. zeroRule // Simplify,
  {i, 1, 2 NN}, {j, 1, 2 NN}
];

Print["Jacobian computed. Size: ", Dimensions[jacobian]]
Print[""]

(* ------------------------------------------------------------ *)
(* Part 2: Find the characteristic polynomial                   *)
(* ------------------------------------------------------------ *)

Print["Computing characteristic polynomial..."]

lambda = Symbol["lambda"];
charPoly = Det[jacobian - lambda IdentityMatrix[2 NN]] // Simplify;

Print["Characteristic polynomial (in lambda):"]
Print["  ", charPoly]
Print[""]

(* Factor and find eigenvalues *)
eigenvalueEquations = Solve[charPoly == 0, lambda];
Print["Number of eigenvalue solutions: ", Length[eigenvalueEquations]]
Print[""]

(* ------------------------------------------------------------ *)
(* Part 3: Find critical k0 where real eigenvalue appears       *)
(* ------------------------------------------------------------ *)

Print["Finding critical k0..."]
Print[""]

(* The critical point is where an eigenvalue pair transitions *)
(* from purely imaginary to having a real component.          *)
(* This occurs when two imaginary eigenvalues collide.        *)
(* At the collision: lambda = i*omega (double root).          *)
(* Condition: charPoly = 0 AND d(charPoly)/d(lambda) = 0     *)

(* Alternatively: substitute lambda = i*omega into charPoly  *)
(* and find where it has a double root.                       *)

(* Numerical check first: *)
Print["Numerical eigenvalues at k0 = -1/4:"]
jacNum = jacobian /. k0 -> -1/4 // N;
eigsNum = Eigenvalues[jacNum];
Print["  ", Sort[eigsNum, Abs[Im[#1]] > Abs[Im[#2]] &]]
Print[""]

Print["Numerical eigenvalues at k0 = -0.30:"]
jacNum2 = jacobian /. k0 -> -0.30 // N;
eigsNum2 = Eigenvalues[jacNum2];
Print["  ", Sort[eigsNum2, Abs[Re[#1]] > Abs[Re[#2]] &]]
Print[""]

(* Try to solve for critical k0 symbolically *)
Print["Attempting symbolic solution for critical k0..."]
Print["(This may take several minutes for N=6)"]
Print[""]

(* For computational tractability, try the characteristic polynomial *)
(* evaluated at lambda = 0 (which would give a zero eigenvalue *)
(* at the marginal point) *)
charPolyAt0 = charPoly /. lambda -> 0 // Simplify;
Print["charPoly(0) = ", charPolyAt0]
Print[""]

(* Critical k0 from charPoly(0) = 0: *)
criticalK0 = Solve[charPolyAt0 == 0, k0];
Print["k0 values where lambda=0 is an eigenvalue:"]
Print["  ", criticalK0 // N]
Print[""]
Print["Compare with Python numerical: k_crit = -0.2501"]
