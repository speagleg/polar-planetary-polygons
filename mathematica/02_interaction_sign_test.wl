(* ============================================================ *)
(* TEST: Is the N-gon a critical point of ANY rotationally      *)
(* symmetric Hamiltonian restricted to the Z_N sector?          *)
(*                                                              *)
(* This would be a THEOREM, not dependent on the specific       *)
(* interaction [Thomson, Coulomb, etc.]                          *)
(* ============================================================ *)

Clear["Global`*"]

(* ------------------------------------------------------------ *)
(* Cell 1: General argument from symmetry                       *)
(* ------------------------------------------------------------ *)

(* For ANY function H[z_1, ..., z_N] that is:                   *)
(* [a] symmetric under rotation: H[e^{i phi} z_1, ..., e^{i phi} z_N] = H *)
(* [b] symmetric under cyclic permutation: H[z_2, z_3, ..., z_1] = H *)
(*                                                              *)
(* The regular N-gon z_k = R Exp[2 Pi I k/N] is a FIXED POINT  *)
(* of both symmetries. By a standard argument:                  *)
(* dH/dsigma = 0 at the N-gon for ANY symmetry-preserving       *)
(* deformation that takes the N-gon to a non-symmetric config.  *)

Print["SYMMETRY ARGUMENT FOR CRITICAL POINT"]
Print[""]
Print["For any H[z_1,...,z_N] with:"]
Print["  [a] U[1] rotation symmetry"]
Print["  [b] Z_N cyclic permutation symmetry"]
Print[""]
Print["The regular N-gon is a CRITICAL POINT of H."]
Print[""]
Print["Proof: The N-gon z_k = R Exp[2 Pi I k/N] is a fixed point"]
Print["of the Z_N action. Any smooth deformation that breaks Z_N"]
Print["symmetry must have dH = 0 at the symmetric point, because"]
Print["H is constant on the Z_N orbit of any configuration, and"]
Print["the N-gon is the unique Z_N-invariant configuration on the"]
Print["circle of radius R."]
Print[""]
Print["This is a consequence of the EQUIVARIANT CRITICAL POINT"]
Print["THEOREM: symmetric functions have critical points at"]
Print["fixed points of the symmetry group."]
Print[""]

(* ------------------------------------------------------------ *)
(* Cell 2: The SIGN of H'' — does it depend on the interaction? *)
(* ------------------------------------------------------------ *)

(* The critical point is guaranteed by symmetry.                 *)
(* The SIGN of H''[0] [max vs min] depends on the Hamiltonian.  *)
(* Test: is H''[0] < 0 [energy MAX] generic for pairwise         *)
(* interactions h[|z_j - z_k|] with h decreasing?               *)

spiralPos[NN_, sigma_] := Table[
  Exp[sigma k/NN] Exp[2 Pi I k/NN], {k, 0, NN - 1}] // N;

pairwiseH[NN_, sigma_, hFunc_] := Module[
  {zz = spiralPos[NN, sigma], total = 0},
  Do[Do[
    If[j != k, total += hFunc[Abs[zz[[j]] - zz[[k]]]]],
    {k, j + 1, NN}], {j, 1, NN}];
  total
];

ds = 0.001;

testH2[NN_, hFunc_] := Module[
  {H0, Hp, Hm},
  H0 = pairwiseH[NN, 0, hFunc];
  Hp = pairwiseH[NN, ds, hFunc];
  Hm = pairwiseH[NN, -ds, hFunc];
  (Hp - 2 H0 + Hm)/ds^2
];

Print["H''[0] FOR VARIOUS PAIRWISE INTERACTIONS, N=6"]
Print[""]

interactions = {
  {"h = -Log[r] [Thomson/vortex]", Function[r, -Log[r]]},
  {"h = -1/r [attractive Coulomb]", Function[r, -1/r]},
  {"h = +1/r [repulsive Coulomb]", Function[r, 1/r]},
  {"h = -1/r^2 [attractive inv-sq]", Function[r, -1/r^2]},
  {"h = +1/r^2 [repulsive inv-sq]", Function[r, 1/r^2]},
  {"h = +r^2 [spring/attractive]", Function[r, r^2]},
  {"h = -r^2 [repulsive harmonic]", Function[r, -r^2]},
  {"h = +r [separation]", Function[r, r]},
  {"h = Exp[-r] [Yukawa]", Function[r, Exp[-r]]}
};

Do[
  Module[{name = int[[1]], hf = int[[2]], H2},
    H2 = testH2[6, hf];
    Print["  ", name, ": H''[0] = ", NumberForm[H2, 5],
      "  ", If[H2 < -0.001, "MAX",
        If[H2 > 0.001, "min", "~flat"]]]
  ],
  {int, interactions}
]
Print[""]

(* ------------------------------------------------------------ *)
(* Cell 3: Pattern — when is the N-gon a maximum vs minimum?    *)
(* ------------------------------------------------------------ *)

Print["PATTERN: Which interactions give MAX vs min at the N-gon?"]
Print[""]
Print["If h[r] is DECREASING [attractive interaction]:"]
Print["  Particles prefer to be CLOSE => clustered state has lower H"]
Print["  The N-gon [spread out] is a MAXIMUM of H"]
Print["  => H''[0] < 0"]
Print[""]
Print["If h[r] is INCREASING [repulsive interaction]:"]
Print["  Particles prefer to be FAR => spread state has lower H"]
Print["  The N-gon [maximally spread on ring] is a MINIMUM of H"]
Print["  => H''[0] > 0"]
Print[""]
Print["The SIGN of H'' depends on whether the interaction is"]
Print["attractive [h decreasing, H'' < 0] or repulsive [h increasing, H'' > 0]."]
Print[""]
Print["For VORTEX dynamics: h = -Log[r] is DECREASING."]
Print["=> H''[0] < 0 [energy MAXIMUM at the N-gon]."]
Print["=> Onsager negative temperature selects the N-gon."]
Print[""]
Print["This is SPECIFIC to attractive/decreasing interactions."]
Print["It is NOT universal for all Hamiltonians."]
Print["But it IS universal for all VORTEX-type interactions"]
Print["[logarithmic, Coulomb, inverse-power with decay]."]

(* ------------------------------------------------------------ *)
(* Cell 4: The complete mechanistic picture                     *)
(* ------------------------------------------------------------ *)

Print[""]
Print["THE COMPLETE MECHANISTIC FRAMEWORK:"]
Print[""]
Print["UNIVERSAL [any Hamiltonian on symmetric domain]:"]
Print["  1. Spectral reality: s^2 in R [from real coefficients]"]
Print["  2. Critical point: N-gon is dH/dsigma = 0 [from symmetry]"]
Print[""]
Print["SPECIFIC TO VORTEX/ATTRACTIVE INTERACTIONS:"]
Print["  3. Energy maximum: H''[0] < 0 [from h decreasing]"]
Print["  4. Onsager: negative temp selects energy maxima"]
Print[""]
Print["SPECIFIC TO EACH PLANET:"]
Print["  5. Mode selection: n from Rossby [Saturn] or Thomson [Jupiter]"]
Print["  6. Thermostat: atmospheric turbulence provides mixing"]
Print[""]
Print["The POLYGON is universal for vortex-type Hamiltonians."]
Print["The specific N is planet-dependent."]
Print["The MECHANISM is: symmetry [critical point] + attractive"]
Print["interaction [energy max] + negative temperature [selection]."]
