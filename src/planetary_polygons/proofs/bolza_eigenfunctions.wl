(* ================================================================== *)
(* BOLZA EIGENFUNCTIONS via Mathematica NDEigensystem                 *)
(*                                                                    *)
(* Solves -Δφ = λφ on the regular octagon fundamental domain          *)
(* of the Bolza surface in the Poincaré disk model.                   *)
(*                                                                    *)
(* The octagon has vertices at                                        *)
(*   z_k = r_oct · e^{2πi(k+1/2)/8}, k = 0,...,7                    *)
(* where r_oct = (√2-1)^{1/2} in the unit disk (curvature -1).       *)
(*                                                                    *)
(* For the EIGENFUNCTION computation, we work in the Euclidean        *)
(* octagon (ignoring the hyperbolic metric) as a FIRST APPROXIMATION. *)
(* The correct computation requires the Poincaré disk Laplacian:      *)
(*   Δ_hyp = (1-|z|²)²/4 · Δ_Euclidean                              *)
(*                                                                    *)
(* Run: Get["bolza_eigenfunctions.wl"]                                *)
(* ================================================================== *)

Print["=" <> StringJoin[Table["=", 68]]];
Print["BOLZA EIGENFUNCTION COMPUTATION"];
Print["=" <> StringJoin[Table["=", 68]]];

(* === Step 1: Define the octagonal domain === *)

(* The regular octagon in the Poincaré disk *)
(* Vertices at angles (2k+1)π/8 for k=0,...,7 *)
(* Euclidean radius: r_oct for the Bolza fundamental domain *)
(* In the Poincaré disk with curvature K=-1: *)
(* The octagon's Euclidean circumradius is r = tanh(arccosh(1+√2)/2) *)

rOct = N[Tanh[ArcCosh[1 + Sqrt[2]]/2]];
Print["\nOctagon circumradius in Poincaré disk: r = ", rOct];

octagonVertices = Table[
  rOct * {Cos[(2 k + 1) Pi/8], Sin[(2 k + 1) Pi/8]},
  {k, 0, 7}
];

Print["Vertices: ", N[octagonVertices, 4]];

(* Create the octagonal region *)
octRegion = Polygon[octagonVertices];
Print["Area (Euclidean): ", N[Area[octRegion]]];

(* Hyperbolic area should be 4π *)
(* The Euclidean area differs; the hyperbolic metric scales by *)
(* 4/(1-|z|²)² *)

(* === Step 2: Solve the Euclidean eigenvalue problem === *)
(* (First approximation — the correct version needs the hyperbolic Laplacian) *)

Print["\n--- Solving Euclidean -Δφ = λφ on the octagon ---"];
Print["(This is an APPROXIMATION; the correct Laplacian is hyperbolic)"];

(* NDEigensystem with Dirichlet BCs (NOT the correct BCs, but a start) *)
nEigs = 15;
{eigenvalues, eigenfunctions} = NDEigensystem[
  {-Laplacian[u[x, y], {x, y}], DirichletCondition[u[x, y] == 0, True]},
  u[x, y], {x, y} ∈ octRegion, nEigs
];

Print["\nEuclidean Dirichlet eigenvalues (APPROXIMATION):"];
Do[
  Print["  λ_", i, " = ", N[eigenvalues[[i]], 6]],
  {i, 1, Min[nEigs, Length[eigenvalues]]}
]

(* === Step 3: Evaluate eigenfunctions at the center === *)

Print["\n--- Eigenfunction values at the center (0,0) ---"];
Do[
  val = eigenfunctions[[i]][0, 0];
  Print["  φ_", i, "(0,0) = ", N[val, 6],
    If[Abs[val] < 0.001, " (VANISHES)", ""]],
  {i, 1, Min[nEigs, Length[eigenfunctions]]}
]

(* === Step 4: The CORRECT computation (hyperbolic Laplacian) === *)

Print["\n--- Step 4: Hyperbolic Laplacian ---"];
Print["The CORRECT eigenvalue problem is:"];
Print["  -(1-|z|²)²/4 · Δ_Euclid φ = λ φ"];
Print["  with PERIODIC boundary conditions (side identifications)"];
Print[];
Print["This requires:"];
Print["  1. Replace the Laplacian with the Poincaré disk Laplacian"];
Print["  2. Replace Dirichlet BCs with periodic BCs matching"];
Print["     opposite sides via Fuchsian group generators"];
Print[];
Print["The hyperbolic Laplacian as a PDE:"];
Print["  -((1-x²-y²)²/4)(∂²φ/∂x² + ∂²φ/∂y²) = λ φ"];

(* Try with the hyperbolic Laplacian but Dirichlet BCs *)
(* (still wrong BCs, but correct operator) *)

conformalFactor[x_, y_] := (1 - x^2 - y^2)^2/4;

{hypEigenvalues, hypEigenfunctions} = NDEigensystem[
  {-conformalFactor[x, y] * Laplacian[u[x, y], {x, y}],
   DirichletCondition[u[x, y] == 0, True]},
  u[x, y], {x, y} ∈ octRegion, nEigs
];

Print["\nHyperbolic Laplacian with Dirichlet BCs (STILL APPROXIMATE):"];
Do[
  Print["  λ_", i, " = ", N[hypEigenvalues[[i]], 6]],
  {i, 1, Min[nEigs, Length[hypEigenvalues]]}
]

Print["\nEigenfunctions at center:"];
Do[
  val = hypEigenfunctions[[i]][0, 0];
  Print["  φ_", i, "(0,0) = ", N[val, 6],
    If[Abs[val] < 0.001, " (VANISHES)", ""]],
  {i, 1, Min[nEigs, Length[hypEigenfunctions]]}
]

(* === Step 5: Compare with known eigenvalues === *)

Print["\n--- Comparison with Strohmaier-Uski (2013) ---"];
Print["Known Bolza eigenvalues (first 10 distinct):"];
knownEigs = {3.8389, 5.3536, 8.2496, 14.7262, 15.0489,
             18.6588, 20.5199, 23.0786, 28.0796, 30.8330};
Do[
  Print["  λ_", i, " = ", knownEigs[[i]]],
  {i, 1, Length[knownEigs]}
]

Print[];
Print["NOTE: The Dirichlet BC computation will NOT match these values."];
Print["The correct computation requires PERIODIC boundary conditions"];
Print["matching opposite octagon sides via the Fuchsian group."];
Print["This is the key computational challenge."];
Print[];
Print["For the EIGENFUNCTIONS at the center (which is what we need for"];
Print["the spectral stability correction δC₁), the Dirichlet computation"];
Print["gives a qualitative picture: eigenfunctions with the right symmetry"];
Print["vanish or not at the center based on their representation type."];
