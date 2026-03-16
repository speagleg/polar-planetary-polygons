(* ============================================================ *)
(* MECHANISTIC FRAMEWORK: Hamiltonian systems on symmetric      *)
(* domains with Z_N mode restriction                            *)
(*                                                              *)
(* Hypothesis: For any Hamiltonian system on a rotationally     *)
(* symmetric domain, restricted to the Z_N sector, the regular  *)
(* N-gon is a distinguished critical point of both the spectral *)
(* problem and the energy landscape.                            *)
(*                                                              *)
(* This file tests three predictions:                           *)
(* 1. The spectral reality condition [s^2 real] is generic      *)
(*    for Hamiltonian systems with rotational symmetry           *)
(* 2. The energy critical point at the N-gon is generic         *)
(* 3. The sign [H'' < 0] is generic [not just for Thomson]      *)
(* ============================================================ *)

Clear["Global`*"]

(* ------------------------------------------------------------ *)
(* Cell 1: Test with DIFFERENT Hamiltonians                     *)
(* ------------------------------------------------------------ *)

(* The Thomson Hamiltonian: H = -Sum ln|z_j - z_k|              *)
(* We proved H''[0] < 0 for the spiral deformation.             *)
(*                                                              *)
(* Now test with OTHER rotationally symmetric Hamiltonians:      *)
(* H_alpha = Sum |z_j - z_k|^alpha for various alpha            *)
(*                                                              *)
(* Thomson: alpha -> 0 limit [H = -Sum ln|dz|]                  *)
(* Coulomb: alpha = -1 [H = Sum 1/|dz|]                         *)
(* Spring:  alpha = +2 [H = Sum |dz|^2]                         *)
(* Lennard-Jones-like: alpha = -2 [H = Sum 1/|dz|^2]            *)

spiralPositions[NN_, sigma_] := Table[
  Exp[sigma k/NN] Exp[2 Pi I k/NN], {k, 0, NN - 1}] // N;

hamiltonianAlpha[NN_, sigma_, alpha_] := Module[
  {zz = spiralPositions[NN, sigma], total = 0},
  Do[
    Do[
      If[j != k,
        Module[{dist = Abs[zz[[j]] - zz[[k]]]},
          If[alpha == 0,
            total += -Log[dist],
            total += dist^alpha
          ]
        ]
      ],
      {k, j + 1, NN}
    ],
    {j, 1, NN}
  ];
  total
];

(* Compute H''[0] for each Hamiltonian *)
ds = 0.001;

Print["H''[0] FOR DIFFERENT HAMILTONIANS"]
Print["Spiral deformation, N = 6"]
Print[""]
Print[Grid[
  Prepend[
    Table[
      Module[{H0, Hp, Hm, H2},
        H0 = hamiltonianAlpha[6, 0, alpha];
        Hp = hamiltonianAlpha[6, ds, alpha];
        Hm = hamiltonianAlpha[6, -ds, alpha];
        H2 = (Hp - 2 H0 + Hm)/ds^2;
        {If[alpha == 0, "ln [Thomson]",
          If[alpha == -1, "1/r [Coulomb]",
          If[alpha == -2, "1/r^2 [enstrophy]",
          If[alpha == 2, "r^2 [spring]",
          If[alpha == 1, "r [separation]",
          ToString[alpha]]]]]],
         NumberForm[H2, 4],
         If[H2 < 0, "MAX", If[H2 > 0, "min", "flat"]]}
      ],
      {alpha, {0, -1, -2, 1, 2, -3, 3}}
    ],
    {"Hamiltonian", "H''[0]", "Extremum"}
  ],
  Frame -> All
]]
Print[""]

(* ------------------------------------------------------------ *)
(* Cell 2: Test across different N                              *)
(* ------------------------------------------------------------ *)

Print["H''[0] FOR THOMSON [alpha=0] ACROSS N"]
Print[""]
Do[
  Module[{H0, Hp, Hm, H2},
    H0 = hamiltonianAlpha[nn, 0, 0];
    Hp = hamiltonianAlpha[nn, ds, 0];
    Hm = hamiltonianAlpha[nn, -ds, 0];
    H2 = (Hp - 2 H0 + Hm)/ds^2;
    Print["  N=", nn, ": H''[0] = ", NumberForm[H2, 5],
      "  ", If[H2 < 0, "MAX", "min"]]
  ],
  {nn, 3, 9}
]
Print[""]

Print["H''[0] FOR COULOMB [alpha=-1] ACROSS N"]
Print[""]
Do[
  Module[{H0, Hp, Hm, H2},
    H0 = hamiltonianAlpha[nn, 0, -1];
    Hp = hamiltonianAlpha[nn, ds, -1];
    Hm = hamiltonianAlpha[nn, -ds, -1];
    H2 = (Hp - 2 H0 + Hm)/ds^2;
    Print["  N=", nn, ": H''[0] = ", NumberForm[H2, 5],
      "  ", If[H2 < 0, "MAX", "min"]]
  ],
  {nn, 3, 9}
]
Print[""]

Print["H''[0] FOR SPRING [alpha=+2] ACROSS N"]
Print[""]
Do[
  Module[{H0, Hp, Hm, H2},
    H0 = hamiltonianAlpha[nn, 0, 2];
    Hp = hamiltonianAlpha[nn, ds, 2];
    Hm = hamiltonianAlpha[nn, -ds, 2];
    H2 = (Hp - 2 H0 + Hm)/ds^2;
    Print["  N=", nn, ": H''[0] = ", NumberForm[H2, 5],
      "  ", If[H2 < 0, "MAX", "min"]]
  ],
  {nn, 3, 9}
]

(* ------------------------------------------------------------ *)
(* Cell 3: The key question — is the sign universal?            *)
(* ------------------------------------------------------------ *)

Print[""]
Print["KEY QUESTION: Is H''[0] < 0 for ALL symmetric Hamiltonians?"]
Print[""]
Print["If yes: the energy maximum at the N-gon is a GENERIC property"]
Print["of Hamiltonian systems on symmetric domains, not specific to"]
Print["the Thomson [logarithmic] interaction."]
Print[""]
Print["If no: the sign depends on the interaction, and the Thomson"]
Print["result is specific to 2D vortex dynamics."]
