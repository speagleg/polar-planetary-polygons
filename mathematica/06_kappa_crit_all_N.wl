(* ============================================================ *)
(* PROVE: kappa_crit for N=3 and N=5 analytically               *)
(*                                                              *)
(* N=4: already proven, kappa_crit = -1/2 from char poly        *)
(* N=6: already proven, kappa_crit = -1/4 from char poly        *)
(* N=3: 6x6 Jacobian, should be tractable symbolically          *)
(* N=5: 10x10 Jacobian, use numerical positions + symbolic k0   *)
(* ============================================================ *)

Clear["Global`*"]

(* ------------------------------------------------------------ *)
(* Cell 1: N=3 — full symbolic computation                      *)
(* ------------------------------------------------------------ *)

Print["N = 3: SYMBOLIC CHARACTERISTIC POLYNOMIAL"]
Print[""]

NN = 3;
zz = Table[Exp[2 Pi I k/NN] // N, {k, 0, NN - 1}];
x0 = Re /@ zz;
y0 = Im /@ zz;
kappa = 1;

(* Co-rotating frame angular velocity *)
Omega = kappa (NN - 1)/(4 Pi) + k0/(2 Pi);

(* Build 2N x 2N analytic Jacobian *)
JJ = Table[0, {2 NN}, {2 NN}];

Do[
  Do[
    If[j != k,
      Module[{dx, dy, r2, r4, CC,
              dvxdx, dvxdy, dvydx, dvydy},
        dx = x0[[k + 1]] - x0[[j + 1]];
        dy = y0[[k + 1]] - y0[[j + 1]];
        r2 = dx^2 + dy^2;
        r4 = r2^2;
        CC = kappa/(2 Pi);
        dvxdx = CC 2 dx dy/r4;
        dvxdy = CC (dy^2 - dx^2)/r4;
        dvydx = CC (dy^2 - dx^2)/r4;
        dvydy = -CC 2 dx dy/r4;
        JJ[[k + 1, j + 1]] += dvxdx;
        JJ[[k + 1, j + 1 + NN]] += dvxdy;
        JJ[[k + 1 + NN, j + 1]] += dvydx;
        JJ[[k + 1 + NN, j + 1 + NN]] += dvydy;
        JJ[[k + 1, k + 1]] -= dvxdx;
        JJ[[k + 1, k + 1 + NN]] -= dvxdy;
        JJ[[k + 1 + NN, k + 1]] -= dvydx;
        JJ[[k + 1 + NN, k + 1 + NN]] -= dvydy;
      ]
    ],
    {j, 0, NN - 1}
  ];
  (* Central vortex *)
  Module[{xk, yk, rk2, rk4, Cc},
    xk = x0[[k + 1]]; yk = y0[[k + 1]];
    rk2 = xk^2 + yk^2; rk4 = rk2^2;
    Cc = k0/(2 Pi);
    JJ[[k + 1, k + 1]] += -Cc 2 xk yk/rk4;
    JJ[[k + 1, k + 1 + NN]] += Cc (xk^2 - yk^2)/rk4;
    JJ[[k + 1 + NN, k + 1]] += Cc (xk^2 - yk^2)/rk4;
    JJ[[k + 1 + NN, k + 1 + NN]] += Cc 2 xk yk/rk4;
  ];
  JJ[[k + 1, k + 1 + NN]] += Omega;
  JJ[[k + 1 + NN, k + 1]] -= Omega;,
  {k, 0, NN - 1}
];

(* Characteristic polynomial *)
charPoly3 = Det[JJ - lam IdentityMatrix[2 NN]] // Simplify;
Print["Char poly N=3: ", charPoly3]
Print[""]

(* Find where lambda = 0 is an eigenvalue *)
charAt0 = charPoly3 /. lam -> 0 // Simplify;
Print["charPoly at lambda=0: ", charAt0]
Print[""]

(* Factor and find kappa_crit *)
Print["Solving for k0 where instability begins:"]
(* The char poly should factor; find the quadratic in lam^2 that gives instability *)

(* Eigenvalues at k0 = -1/2 *)
JJhalf = JJ /. k0 -> -1/2;
eigsHalf = Eigenvalues[JJhalf] // Chop;
Print["Eigenvalues at k0 = -1/2: ", Sort[eigsHalf, Abs[Re[#1]] > Abs[Re[#2]] &]]
Print[""]

(* Eigenvalues at k0 = -0.4 *)
JJ4 = JJ /. k0 -> -4/10;
eigs4 = Eigenvalues[JJ4] // Chop;
maxRe4 = Max[Abs[Re /@ eigs4]];
Print["Max |Re[eig]| at k0 = -0.4: ", maxRe4]

(* Eigenvalues at k0 = -0.6 *)
JJ6 = JJ /. k0 -> -6/10;
eigs6 = Eigenvalues[JJ6] // Chop;
maxRe6 = Max[Abs[Re /@ eigs6]];
Print["Max |Re[eig]| at k0 = -0.6: ", maxRe6]
Print[""]

Print["If max|Re| is ~0 at k0=-0.5 and >0 at k0=-0.6: kappa_crit = -1/2"]
Print[""]


(* ------------------------------------------------------------ *)
(* Cell 2: N=5 — numerical positions, symbolic k0               *)
(* ------------------------------------------------------------ *)

Print[""]
Print["N = 5: CHARACTERISTIC POLYNOMIAL"]
Print[""]

Clear[JJ, NN, Omega, zz, x0, y0]

NN = 5;
zz = Table[Exp[2 Pi I k/NN] // N, {k, 0, NN - 1}];
x0 = Re /@ zz;
y0 = Im /@ zz;
kappa = 1;
Omega = kappa (NN - 1)/(4 Pi) + k0/(2 Pi);

JJ = Table[0, {2 NN}, {2 NN}];

Do[
  Do[
    If[j != k,
      Module[{dx, dy, r2, r4, CC,
              dvxdx, dvxdy, dvydx, dvydy},
        dx = x0[[k + 1]] - x0[[j + 1]];
        dy = y0[[k + 1]] - y0[[j + 1]];
        r2 = dx^2 + dy^2;
        r4 = r2^2;
        CC = kappa/(2 Pi);
        dvxdx = CC 2 dx dy/r4;
        dvxdy = CC (dy^2 - dx^2)/r4;
        dvydx = CC (dy^2 - dx^2)/r4;
        dvydy = -CC 2 dx dy/r4;
        JJ[[k + 1, j + 1]] += dvxdx;
        JJ[[k + 1, j + 1 + NN]] += dvxdy;
        JJ[[k + 1 + NN, j + 1]] += dvydx;
        JJ[[k + 1 + NN, j + 1 + NN]] += dvydy;
        JJ[[k + 1, k + 1]] -= dvxdx;
        JJ[[k + 1, k + 1 + NN]] -= dvxdy;
        JJ[[k + 1 + NN, k + 1]] -= dvydx;
        JJ[[k + 1 + NN, k + 1 + NN]] -= dvydy;
      ]
    ],
    {j, 0, NN - 1}
  ];
  Module[{xk, yk, rk2, rk4, Cc},
    xk = x0[[k + 1]]; yk = y0[[k + 1]];
    rk2 = xk^2 + yk^2; rk4 = rk2^2;
    Cc = k0/(2 Pi);
    JJ[[k + 1, k + 1]] += -Cc 2 xk yk/rk4;
    JJ[[k + 1, k + 1 + NN]] += Cc (xk^2 - yk^2)/rk4;
    JJ[[k + 1 + NN, k + 1]] += Cc (xk^2 - yk^2)/rk4;
    JJ[[k + 1 + NN, k + 1 + NN]] += Cc 2 xk yk/rk4;
  ];
  JJ[[k + 1, k + 1 + NN]] += Omega;
  JJ[[k + 1 + NN, k + 1]] -= Omega;,
  {k, 0, NN - 1}
];

(* For N=5, the char poly may be too large to display *)
(* Instead, compute eigenvalues at specific k0 values *)

Print["Eigenvalue scan for N=5:"]
Do[
  Module[{JJk, eigs, maxRe},
    JJk = JJ /. k0 -> kval;
    eigs = Eigenvalues[JJk] // Chop;
    maxRe = Max[Abs[Re /@ eigs]];
    Print["  k0 = ", kval, ": max|Re[eig]| = ", maxRe]
  ],
  {kval, {0, -0.2, -0.4, -0.49, -0.50, -0.51, -0.6, -1.0}}
]

Print[""]
Print["If transition occurs at k0 = -0.50: kappa_crit = -1/2 for N=5"]

(* Try to get the char poly *)
Print[""]
Print["Attempting characteristic polynomial for N=5..."]
charPoly5 = Det[JJ - lam IdentityMatrix[2 NN]] // Chop // Simplify;
Print["Done. Factoring..."]
Print["charPoly at lambda=0: ", charPoly5 /. lam -> 0 // Chop]
