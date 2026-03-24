(* Angular ZP v4: request 10 eigenvalues to capture deep ground state *)
Needs["NDSolve`FEM`"];

nn = 11; b = N[nn(nn+1)/12 - Log[2] + Log[nn]/(nn-1), 20];
c = 12. b; fCrit = 15.;
Print["c=", c];

(* Non-uniform mesh *)
rMin = 0.00001; rMax = 12.; nPts = 5000;
coords = Table[rMin + (rMax-rMin)(i/nPts)^2, {i, 0, nPts}];
mesh = ToElementMesh["Coordinates" -> Partition[coords, 1],
  "MeshElements" -> {LineElement[Table[{i,i+1}, {i, Length[coords]-1}]]}];

(* Request 10 eigenvalues to make sure we get the deep ones *)
{evals, efuncs} = NDEigensystem[
  {-1./(2. c) Derivative[2][u][x] + Log[2. Sinh[x]] u[x],
   DirichletCondition[u[x] == 0, True]},
  u[x], {x} \[Element] mesh, 10];

(* Sort by real part and print ALL *)
idx = Ordering[Re[evals]];
Print["ALL 10 eigenvalues (sorted):"];
Do[Print["  E", i, " = ", Re[evals[[idx[[i]]]]]], {i, 1, Min[10, Length[idx]]}];

e0 = Re[evals[[idx[[1]]]]]; e1 = Re[evals[[idx[[2]]]]];
gap = e1 - e0;
Print[];
Print["E0=", e0, " E1=", e1, " gap=", gap];

(* Use the DEEPEST eigenfunction as ground state *)
psi0 = efuncs[[idx[[1]]]];

(* Normalize *)
n2 = NIntegrate[psi0^2, {x, rMin, rMax}];
psi = psi0/Sqrt[n2];

(* Threshold *)
lam[r_] := Log[2 Sinh[r]] + b - fCrit;
rs = r /. FindRoot[lam[r] == 0, {r, 3.}];
Print["rho*=", rs];

(* Probability split *)
pB = NIntegrate[psi^2, {x, rMin, rs}];
pA = NIntegrate[psi^2, {x, rs, rMax}];
Print["P(below)=", pB, " P(above)=", pA];

(* Angular ZP *)
az = 0.5 NIntegrate[psi^2 Sqrt[Max[0, lam[x]]], {x, rs, rMax}, MaxRecursion->15];
Print["E_angular=", az];
Print[];

fm = gap + az;
Print["F_M = ", gap, " + ", az, " = ", fm];

(* Budget *)
fDE = b + nn/4.; fDM = 0.5 Sum[If[Abs[fCrit-m(nn-m)/2.]>0.01, Log[Abs[fCrit-m(nn-m)/2.]], 0], {m,1,nn-1}];
ft = fDE + fDM + fm;
Print["DE=", fDE/ft*100., "% DM=", fDM/ft*100., "% M=", fm/ft*100., "%"];

(* Best radion *)
bc=10.^10; bm=0.;
Do[fd=b+mr/2.; ft2=fd+fDM+fm;
  ch=((fd/ft2*100.-68.47)/0.73)^2+((fDM/ft2*100.-26.60)/0.73)^2+((fm/ft2*100.-4.93)/0.06)^2;
  If[ch<bc,bc=ch;bm=mr],{mr,4.,6.,0.001}];
fd2=b+bm/2.; ft2=fd2+fDM+fm;
Print["Best M_rad=", bm, " (shift=", bm-nn/2., ")"];
Print["DE=", fd2/ft2*100., "% DM=", fDM/ft2*100., "% M=", fm/ft2*100., "%"];
Print["sigma: DE=", Abs[fd2/ft2*100.-68.47]/0.73, " DM=", Abs[fDM/ft2*100.-26.60]/0.73, " M=", Abs[fm/ft2*100.-4.93]/0.06];
Print["DONE"];
