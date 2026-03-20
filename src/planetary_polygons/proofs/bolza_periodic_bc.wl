(* ================================================================== *)
(* BOLZA EIGENFUNCTIONS WITH PERIODIC BOUNDARY CONDITIONS             *)
(*                                                                    *)
(* The Bolza surface fundamental domain: regular octagon in the       *)
(* Poincaré disk with opposite sides identified by hyperbolic         *)
(* isometries (Fuchsian group generators).                            *)
(*                                                                    *)
(* Side pairings: side k ↔ side k+4 (opposite) for k=0,1,2,3.       *)
(* Each pairing is a hyperbolic translation along the perpendicular   *)
(* bisector of the two identified sides.                              *)
(*                                                                    *)
(* Method: Solve the GENERALIZED eigenvalue problem with the          *)
(* hyperbolic metric, using PeriodicBoundaryCondition to enforce      *)
(* the side identifications.                                          *)
(* ================================================================== *)

Print["=" <> StringJoin[Table["=", 68]]];
Print["BOLZA PERIODIC BC EIGENFUNCTION COMPUTATION"];
Print["=" <> StringJoin[Table["=", 68]]];

(* === The octagonal fundamental domain === *)

rOct = N[Tanh[ArcCosh[1 + Sqrt[2]]/2], 20];
vertices = Table[
  rOct * {Cos[(2 k + 1) Pi/8], Sin[(2 k + 1) Pi/8]},
  {k, 0, 7}
];

Print["\nOctagon circumradius: r = ", N[rOct, 8]];

octRegion = Polygon[vertices];

(* === Side-pairing Möbius transformations === *)
(* For the standard Bolza octagon: opposite sides are identified. *)
(* Side k (from vertex k to vertex k+1) is paired with           *)
(* side k+4 (from vertex k+4 to vertex k+5).                     *)
(*                                                                *)
(* The identification map for side 0↔4 is a hyperbolic translation*)
(* that maps the midpoint of side 0 to the midpoint of side 4.   *)
(* In Möbius form: w = (az+b)/(cz+d) with ad-bc=1.              *)
(*                                                                *)
(* For the regular octagon in the Poincaré disk:                  *)
(* The side-pairing maps are rotations by π followed by           *)
(* translations. For simplicity, use the AFFINE APPROXIMATION    *)
(* (valid near the center where the metric is nearly Euclidean).  *)

(* Midpoints of each side *)
midpoints = Table[
  (vertices[[Mod[k, 8] + 1]] + vertices[[Mod[k + 1, 8] + 1]])/2,
  {k, 0, 7}
];

Print["\nSide midpoints:"];
Do[Print["  Side ", k, ": ", N[midpoints[[k + 1]], 4]], {k, 0, 7}]

(* The pairing maps: side k → side k+4 *)
(* For periodic BCs: φ(point on side k) = φ(corresponding point on side k+4) *)
(* The corresponding point is obtained by the affine map that sends *)
(* side k to side k+4, preserving the parameterization. *)

(* For the regular octagon with 8-fold symmetry: *)
(* The map from side k to side k+4 is: rotation by π + translation *)
(* In the Poincaré disk: this is a Möbius transformation. *)

(* The SIMPLEST approach: use the fact that opposite sides differ *)
(* by a translation vector (in the AFFINE approximation). *)
(* Translation vectors: midpoint(side k+4) - midpoint(side k) *)

translationVectors = Table[
  midpoints[[Mod[k + 4, 8] + 1]] - midpoints[[k + 1]],
  {k, 0, 3}
];

Print["\nTranslation vectors (affine approximation):"];
Do[Print["  Side ", k, " → Side ", k + 4, ": ",
  N[translationVectors[[k + 1]], 4]], {k, 0, 3}]

(* === Set up the eigenvalue problem with periodic BCs === *)

Print["\n--- Setting up periodic BC eigenvalue problem ---"];

(* The hyperbolic Laplacian *)
confFactor[x_, y_] := (1 - x^2 - y^2)^2/4;

(* Define the PDE: -Δ_hyp φ = λ · (4/(1-|z|²)²) · φ *)
(* In weak form: ∫ ∇φ·∇ψ dA_hyp = λ ∫ φψ dA_hyp *)
(* where dA_hyp = 4/(1-|z|²)² dA_Eucl *)

(* Mathematica's NDEigensystem with PeriodicBoundaryCondition: *)
(* PeriodicBoundaryCondition[u[x,y], pred1, tfun] *)
(* where pred1 selects one boundary, tfun maps it to the paired boundary *)

(* For side 0 → side 4: *)
(* Side 0 goes from vertex 0 to vertex 1 *)
(* Side 4 goes from vertex 4 to vertex 5 *)
(* The map: affine translation by translationVectors[[1]] *)

(* Build the periodic BCs *)
(* Side boundaries as predicates *)

sidePred[k_] := Module[{v1, v2, nx, ny},
  v1 = vertices[[Mod[k, 8] + 1]];
  v2 = vertices[[Mod[k + 1, 8] + 1]];
  (* Normal vector pointing outward *)
  {nx, ny} = {v2[[2]] - v1[[2]], v1[[1]] - v2[[1]]};
  {nx, ny} = {nx, ny}/Norm[{nx, ny}];
  (* The side is where the dot product with normal equals the distance *)
  Function[{x, y},
    Abs[(x - v1[[1]]) nx + (y - v1[[2]]) ny] < 0.001 &&
    Min[v1[[1]], v2[[1]]] - 0.01 <= x <= Max[v1[[1]], v2[[1]]] + 0.01 &&
    Min[v1[[2]], v2[[2]]] - 0.01 <= y <= Max[v1[[2]], v2[[2]]] + 0.01
  ]
]

(* Try the computation with periodic BCs *)
(* Note: PeriodicBoundaryCondition needs an AffineTransform *)

nEigs = 10;

Print["\nAttempting NDEigensystem with periodic BCs..."];
Print["(This may take a while or fail if the mesh doesn't align with the BCs)"];

result = Quiet@Check[
  NDEigensystem[
    {-confFactor[x, y] * Laplacian[u[x, y], {x, y}],
     PeriodicBoundaryCondition[u[x, y],
       x == vertices[[1, 1]] && vertices[[1, 2]] <= y <= vertices[[2, 2]],
       Function[{x, y}, {x, y} + translationVectors[[1]]]
     ],
     PeriodicBoundaryCondition[u[x, y],
       y == vertices[[2, 2]] && vertices[[3, 1]] <= x <= vertices[[2, 1]],
       Function[{x, y}, {x, y} + translationVectors[[2]]]
     ],
     PeriodicBoundaryCondition[u[x, y],
       x == vertices[[4, 1]] && vertices[[5, 2]] <= y <= vertices[[4, 2]],
       Function[{x, y}, {x, y} + translationVectors[[3]]]
     ],
     PeriodicBoundaryCondition[u[x, y],
       y == vertices[[6, 2]] && vertices[[6, 1]] <= x <= vertices[[7, 1]],
       Function[{x, y}, {x, y} + translationVectors[[4]]]
     ]
    },
    u[x, y], {x, y} \[Element] octRegion, nEigs
  ],
  $Failed
];

If[result === $Failed,
  Print["\nPeriodic BC approach failed (boundary predicates may not match mesh)."];
  Print["Falling back to: use Dirichlet eigenfunctions + symmetry analysis."];
  Print[];
  Print["ALTERNATIVE: Use the theoretical shortcut."];
  Print["Since we KNOW which eigenvalues have trivial rep (mult-1 from"];
  Print["Strohmaier-Uski), we can estimate δC₁ without the eigenfunctions:"];
  Print[];
  Print["  For trivial-rep eigenfunctions: |φ_n(center)|² ≈ 1/Area = 1/(4π)"];
  Print["  (by equidistribution for the unique Aut-fixed point)"];
  Print[];

  (* Compute δC₁ estimate using the theoretical shortcut *)
  area = 4 Pi;
  (* Multiplicity-1 eigenvalues from Strohmaier-Uski = trivial rep *)
  trivialRepEigs = {23.0786, 32.6736};  (* first two mult-1 values *)

  Print["  Trivial-rep eigenvalues (mult-1 from Strohmaier-Uski):"];
  Print["    λ = ", trivialRepEigs];
  Print[];
  Print["  Estimated |φ_n(0)|² = 1/Area = ", N[1/area, 6]];
  Print[];

  (* The Hessian factor H_n for the m-th Fourier mode: *)
  (* H_n ≈ λ_n × (N-1) × (geometric factor) *)
  (* For a rough estimate: H_n ~ λ_n (the eigenvalue itself, *)
  (* since the Hessian of φ_n scales with λ_n) *)

  Print["  Rough estimate: H_n ~ λ_n (Hessian scales with eigenvalue)"];
  Print["  Then: A_n/λ_n ~ |φ_n(0)|² × H_n/λ_n ~ 1/(4π) × 1 = ", N[1/(4 Pi), 6]];
  Print[];
  Print["  δC₁ ≈ Σ (1/4π) = ", N[Length[trivialRepEigs]/(4 Pi), 6],
    " (from ", Length[trivialRepEigs], " terms)"];
  Print[];
  Print["  Compare to the binding eigenvalue at N=12: λ_bind = 0.778"];
  Print["  δC₁/λ_bind ≈ ", N[Length[trivialRepEigs]/(4 Pi * 0.778), 4]];
  Print[];
  Print["  If δC₁ > 0: N_crit increases (Bolza MORE stable than H²)"];
  Print["  If δC₁ < 0: N_crit decreases (Bolza LESS stable)"];
  Print["  The SIGN requires the actual Hessian computation."];
  ,
  (* Success! Extract eigenvalues and eigenfunctions *)
  {periodicEigs, periodicFuncs} = result;
  Print["\nPeriodic BC eigenvalues:"];
  Do[Print["  λ_", i, " = ", N[periodicEigs[[i]], 6]], {i, 1, nEigs}];
  Print["\nEigenfunctions at center:"];
  Do[
    val = periodicFuncs[[i]] /. {x -> 0, y -> 0};
    Print["  φ_", i, "(0,0) = ", N[val, 6],
      If[Abs[val] < 0.01, " (vanishes)", " *** NONZERO ***"]],
    {i, 1, nEigs}
  ]
]
