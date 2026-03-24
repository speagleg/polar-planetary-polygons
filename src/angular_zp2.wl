(* Angular zero-point energy at N=11 — clean version *)
V[rho_] := Log[2 Sinh[rho]];
nn = 11; b = N[nn (nn + 1)/12 - Log[2] + Log[nn]/(nn - 1), 20];
c = 12. b; fCrit = 15.;
Print["c = ", c, ", b = ", b];

(* Ground state via FEM *)
{evals, efuncs} = NDEigensystem[
  {-1./(2. c) Derivative[2][u][x] + Log[2. Sinh[x]] u[x],
   DirichletCondition[u[x] == 0, True]},
  u[x], {x, 0.00001, 12.}, 3,
  Method -> {"PDEDiscretization" -> {"FiniteElement",
    "MeshOptions" -> {"MaxCellMeasure" -> 0.001}}}];
idx = Ordering[Re[evals]];
e0 = Re[evals[[idx[[1]]]]]; e1 = Re[evals[[idx[[2]]]]];
psi0 = efuncs[[idx[[1]]]];
Print["E0=", e0, " E1=", e1, " gap=", e1-e0];

(* Normalize *)
n2 = NIntegrate[psi0^2, {x, 0.00001, 12.}];
psi = psi0/Sqrt[n2];

(* Threshold *)
lam[r_] := Log[2 Sinh[r]] + b - fCrit;
rs = r /. FindRoot[lam[r] == 0, {r, 3.}];
Print["rho* = ", rs];

(* Probability split *)
pB = NIntegrate[psi^2, {x, 0.00001, rs}];
pA = NIntegrate[psi^2, {x, rs, 12.}];
Print["P(below)=", pB, " P(above)=", pA];

(* Angular ZP = (1/2) int |psi|^2 sqrt(lambda) for rho>rho* *)
az = 0.5 NIntegrate[psi^2 Sqrt[Max[0, lam[x]]], {x, rs, 12.}, MaxRecursion->15];
Print["E_angular = ", az];

(* Total matter *)
gap = e1 - e0; fm = gap + az;
Print["gap=", gap, " angular=", az, " total F_M=", fm];

(* Budget with radion N/4 *)
fDE = b + nn/4.; fDM = 0.5 Sum[If[Abs[fCrit-m(nn-m)/2.]>0.01, Log[Abs[fCrit-m(nn-m)/2.]], 0], {m,1,nn-1}];
ft = fDE + fDM + fm;
Print["DE=", fDE/ft*100., "% DM=", fDM/ft*100., "% M=", fm/ft*100., "%"];

(* Best radion *)
bc = 10.^10; bm = 0.;
Do[fd=b+mr/2.; ft2=fd+fDM+fm;
  ch=((fd/ft2*100.-68.47)/0.73)^2+((fDM/ft2*100.-26.60)/0.73)^2+((fm/ft2*100.-4.93)/0.06)^2;
  If[ch<bc,bc=ch;bm=mr],{mr,4.,6.,0.001}];
fd2=b+bm/2.; ft2=fd2+fDM+fm;
Print["Best M_rad=", bm, " shift=", bm-nn/2.];
Print["DE=", fd2/ft2*100., "% DM=", fDM/ft2*100., "% M=", fm/ft2*100., "%"];
Print["sigma: DE=", Abs[fd2/ft2*100.-68.47]/0.73, " DM=", Abs[fDM/ft2*100.-26.60]/0.73, " M=", Abs[fm/ft2*100.-4.93]/0.06];
Print["DONE"];
