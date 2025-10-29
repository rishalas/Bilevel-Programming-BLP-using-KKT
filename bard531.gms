Variables
    x1,x2,y1,y2,y3                 "Decision variables"
    lambda1, lambda2, lambda3   "Lagrange multipliers"
    obj                  "Objective function value";

Positive Variables x1,x2, y1,y2,y3, u1,u2,u3, lambda1, lambda2, lambda3;

Equations
    objdef          "Objective definition"
    c1              "Constraint 1: "
    c2              "Constraint 2: "
    c3              "Constraint 3: "
    stationarity1    "Stationarity condition"
    stationarity2    "Stationarity condition"
    stationarity3    "Stationarity condition"
    comp1           "Complementary slackness 1"
    comp2           "Complementary slackness 2"
    comp3           "Complementary slackness 3";

* --- Objective ---
objdef.. obj =E= -8*x1- 4*x2 + 4*y1-40*y2-4*y3;

* --- Primal feasibility ---
c1.. -y1 + y2 + y3 =l= 1;
c2.. 2*x1 - y1 +2*y2 -0.5*y3 =l= 1;
c3.. 2*x2 + 2*y1 - y2 -0.5*y3=l= 1;


* --- Stationarity (dL/dy = 0) ---
stationarity1 .. 1 - lambda1 - lambda2 + 2*lambda3  =E= u1 ;
stationarity2 .. 1 + lambda1 + 2*lambda2 - lambda3  =E= u2;
stationarity3 .. 2 + lambda1 - 0.5*lambda2 - 0.5*lambda3  =E= u3;

* --- Complementary slackness ---
comp1.. lambda1*(-y1 + y2 + y3 - 1) =E= 0;
comp2.. lambda2*( 2*x1 - y1 +2*y2 -0.5*y3 - 1) =E= 0;
comp3.. lambda3*( 2*x2 + 2*y1 - y2 -0.5*y3 - 1) =E= 0;


* --- Model definition ---
Model KKTmodel /all/;

* --- Solve using BARON (for global optimum) ---
Option MINLP = baron;
Solve KKTmodel using minlp minimizing obj;

Display x1.l, x2.l,y1.l, y2.l, y3.l, lambda1.l, lambda2.l, lambda3.l, obj.l;
