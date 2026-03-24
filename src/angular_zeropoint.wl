(* Angular zero-point energy of the critical pair at N=11 *)
(* *)
(* The critical pair (m=5, m=6) has TWO degrees of freedom: *)
(* 1. Radial (ρ): the WDW mass gap ΔE = 0.815 *)
(* 2. Angular (θ within the pair): zero-point energy to compute *)
(* *)
(* The angular frequency at geodesic radius ρ: *)
(*   ω_ang(ρ) = √(λ_{m*}(ρ)) = √(C₁(ρ) - f(m*)) *)
(* where C₁(ρ) = Log[2 Sinh[ρ]] + b(N) and f(m*) = 15. *)
(* *)
(* The angular zero-point energy: *)
(*   E_ang = <ψ₀| (1/2)ω_ang(ρ) |ψ₀> *)
(*         = (1/2) ∫ |ψ₀(ρ)|² √(Max[0, C₁(ρ)-f]) dρ *)
(* where ψ₀ is the WDW ground state wavefunction. *)

Needs["NDSolve`FEM`"];

V[rho_] := Log[2 Sinh[rho]];
bN[n_] := n (n + 1)/12 - Log[2] + Log[n]/(n - 1);

nn = 11;
b = N[bN[nn], 20];
c = 12. b;
fCrit = nn/2 (nn - nn/2)/2;  (* = 15 for N=11 *)

Print["ANGULAR ZERO-POINT ENERGY AT N=11"];
Print["====================================="];
Print["b(11) = ", b];
Print["c = ", c];
Print["f(m*) = ", fCrit];
Print[];

(* Build the non-uniform mesh (same as mass_gap_correct.wl) *)
buildMesh[rhoMin_, rhoMax_, nPts_] := Module[
  {coords, mesh},
  coords = Table[
    rhoMin + (rhoMax - rhoMin) (i/nPts)^2,
    {i, 0, nPts}
  ];
  ToElementMesh[
    "Coordinates" -> Partition[coords, 1],
    "MeshElements" -> {LineElement[
      Table[{i, i + 1}, {i, Length[coords] - 1}]
    ]}
  ]
];

(* Step 1: Get the ground state wavefunction *)
Print["Step 1: Computing WDW ground state wavefunction"];
rhoMin = 0.00001;
rhoMax = 12.;
nPts = 5000;
mesh = buildMesh[rhoMin, rhoMax, nPts];

{evals, efuncs} = NDEigensystem[
  {-1./(2. c) Derivative[2][u][x] + V[x] u[x],
   DirichletCondition[u[x] == 0, True]},
  u[x], {x} \[Element] mesh, 3
];

idx = Ordering[Re[evals]];
e0 = Re[evals[[idx[[1]]]]];
e1 = Re[evals[[idx[[2]]]]];
psi0 = efuncs[[idx[[1]]]];

Print["E0 = ", e0];
Print["E1 = ", e1];
Print["Gap = ", e1 - e0];
Print[];

(* Step 2: Normalize the ground state *)
Print["Step 2: Normalizing ground state"];
norm2 = NIntegrate[psi0^2, {x, rhoMin, rhoMax}];
psi0norm = psi0 / Sqrt[norm2];
Print["Norm check: ", NIntegrate[psi0norm^2, {x, rhoMin, rhoMax}]];
Print[];

(* Step 3: Compute the angular frequency function *)
(* ω(ρ) = √(Max[0, C₁(ρ) - f*]) where C₁ = V(ρ) + b(N) *)
(* But this is just √(Max[0, λ_{m*}(ρ)]) *)
(* λ_{m*} = V(ρ) + b - f* = Log[2Sinh[ρ]] + b - 15 *)

lambda[rho_] := V[rho] + b - fCrit;
omegaAng[rho_] := Sqrt[Max[0, lambda[rho]]];

(* The threshold: where λ = 0 *)
rhoStar = FindRoot[lambda[rho] == 0, {rho, 3.}][[1, 2]];
Print["Step 3: Angular frequency"];
Print["Threshold rho* = ", rhoStar];
Print["λ(rho*-1) = ", lambda[rhoStar - 1.]];
Print["λ(rho*) = ", lambda[rhoStar]];
Print["λ(rho*+1) = ", lambda[rhoStar + 1.]];
Print[];

(* Step 4: Compute the angular zero-point energy *)
(* E_ang = (1/2) ∫ |ψ₀|² ω_ang(ρ) dρ *)
(* = (1/2) ∫ |ψ₀|² √(Max[0, λ(ρ)]) dρ *)

Print["Step 4: Angular zero-point energy"];
Print[];

(* The integral has two regions: *)
(* ρ < ρ*: λ < 0, ω = 0 (classically forbidden, no angular ZP) *)
(* ρ > ρ*: λ > 0, ω = √λ (classically allowed, angular ZP contributes) *)

(* Probability below threshold *)
probBelow = NIntegrate[psi0norm^2, {x, rhoMin, rhoStar}];
probAbove = NIntegrate[psi0norm^2, {x, rhoStar, rhoMax}];
Print["P(ρ < ρ*) = ", probBelow, " (classically forbidden)"];
Print["P(ρ > ρ*) = ", probAbove, " (classically allowed)"];
Print[];

(* The angular ZP integral (only over ρ > ρ*) *)
angularZP = 0.5 NIntegrate[
  psi0norm^2 Sqrt[Max[0, lambda[x]]],
  {x, rhoStar, rhoMax},
  MaxRecursion -> 20, AccuracyGoal -> 8
];

Print["Angular zero-point energy:"];
Print["  E_ang = (1/2)<√λ> = ", angularZP];
Print[];

(* Step 5: The total matter free energy *)
gap = e1 - e0;
totalMatter = gap + angularZP;

Print["Step 5: Total matter free energy"];
Print["  ΔE (radial) = ", gap];
Print["  E_ang (angular) = ", angularZP];
Print["  F_M (total) = ", totalMatter];
Print[];

(* Step 6: The cosmological budget *)
Print["Step 6: Cosmological budget"];
FDE = b + nn/4.;  (* vacuum + radion *)
FDM = 0.5 Sum[
  If[Abs[fCrit - m (nn - m)/2] > 0.01,
    Log[Abs[fCrit - m (nn - m)/2.]], 0],
  {m, 1, nn - 1}
];
FM = totalMatter;
FTotal = FDE + FDM + FM;

Print["  F_DE = ", FDE, " (", FDE/FTotal 100., "%)"];
Print["  F_DM = ", FDM, " (", FDM/FTotal 100., "%)"];
Print["  F_M  = ", FM, " (", FM/FTotal 100., "%)"];
Print[];
Print["  Planck: DE=68.47%, DM=26.60%, M=4.93%"];
Print[];

(* Step 7: With corrected radion mass *)
Print["Step 7: Scanning radion mass for best fit"];
bestChi2 = 10^10;
bestMrad = 0;
Do[
  FDEtrial = b + mrad/2.;
  FTtrial = FDEtrial + FDM + FM;
  dePct = FDEtrial/FTtrial 100.;
  dmPct = FDM/FTtrial 100.;
  mPct = FM/FTtrial 100.;
  chi2 = ((dePct - 68.47)/0.73)^2 + ((dmPct - 26.60)/0.73)^2 + ((mPct - 4.93)/0.06)^2;
  If[chi2 < bestChi2, bestChi2 = chi2; bestMrad = mrad],
  {mrad, 4., 6., 0.001}
];

FDEbest = b + bestMrad/2.;
FTbest = FDEbest + FDM + FM;
Print["  Best radion mass: M_rad = ", bestMrad];
Print["  δM from N/2: ", bestMrad - nn/2., " (", (bestMrad - nn/2.)/(nn/2.) 100., "%)"];
Print[];
Print["  DE = ", FDEbest/FTbest 100., "% (Planck: 68.47%)"];
Print["  DM = ", FDM/FTbest 100., "% (Planck: 26.60%)"];
Print["  M  = ", FM/FTbest 100., "% (Planck: 4.93%)"];
Print[];
Print["  chi² = ", bestChi2];
Print["  σ_DE = ", Abs[FDEbest/FTbest 100. - 68.47]/0.73];
Print["  σ_DM = ", Abs[FDM/FTbest 100. - 26.60]/0.73];
Print["  σ_M  = ", Abs[FM/FTbest 100. - 4.93]/0.06];

Print[];
Print["DONE"];
