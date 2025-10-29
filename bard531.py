# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 11:36:09 2025

@author: sinergi
"""

from pyomo.environ import *
#from pyomo.mpec import Complementarity, complements

#from pyomo.environ import ConcreteModel, Var, Objective, Constraint, SolverFactory, minimize, value
#from pyomo.mpec import Complementarity, complements


# Reformulate as single-level using KKT conditions
M = ConcreteModel()

# Variables
M.x1 = Var(bounds=(0,None))
M.y1 = Var(bounds=(0,None))
M.x2 = Var(bounds=(0,None))
M.y2 = Var(bounds=(0,None))
M.y3 = Var(bounds=(0,None))
# Dual variables for lower level constraints
M.lambda1 = Var(bounds=(0,None))
M.lambda2 = Var(bounds=(0,None)) 
M.lambda3 = Var(bounds=(0,None))
M.u1 = Var(bounds=(0,None))
M.u2 = Var(bounds=(0,None))
M.u3 = Var(bounds=(0,None))
# Upper level objective
M.obj = Objective(expr= - 8*M.x1 - 4 * M.x2 + 4* M.y1 - 40 * M.y2- 4* M.y3, sense=minimize)

# Lower level constraints (primal feasibility)
M.c1 = Constraint(expr= - M.y1 +  M.y2 + M.y3 <= 1)  # x + y >= 3
M.c2 = Constraint(expr= 2*M.x1 - M.y1 + 2 * M.y2- 0.5* M.y3 <= 1)  # 2x - y >= 0
M.c3 = Constraint(expr= 2*M.x2 + 2*M.y1 - M.y2- 0.5* M.y3 <= 1)  # 2x + y <= 12


# Stationarity condition for lower level
M.stationarity1 = Constraint(expr=1 - M.lambda1 - M.lambda2 + 2*M.lambda3 == M.u1)
M.stationarity2 = Constraint(expr=1 + M.lambda1 - 2*M.lambda2 - M.lambda3  == M.u2)
M.stationarity3 = Constraint(expr=2 + M.lambda1 - 0.5*M.lambda2 - 0.5* M.lambda3  == M.u3)

# Complementary slackness conditions
M.comp1 = Constraint(expr=M.lambda1 * (- M.y1 +  M.y2 + M.y3 - 1) == 0)
M.comp2 = Constraint(expr=M.lambda2 * (2*M.x1 - M.y1 + 2 * M.y2- 0.5* M.y3 - 1) == 0)
M.comp3 = Constraint(expr=M.lambda3 * ( 2*M.x2 + 2*M.y1 - M.y2- 0.5* M.y3 - 1) == 0)


# Solve
#solver = SolverFactory('scip')
#results = solver.solve(M, tee=True)
import os
os.environ['NEOS_EMAIL'] = 'rishalas@yahoo.com'
opt = SolverManagerFactory('neos')
results = SolverFactory("scip").solve(M, tee=True).write()

print("\nSOLUTION:")
print(f"x1 = {M.x1.value:.4f}")
print(f"x2 = {M.x2.value:.4f}")
print(f"y1 = {M.y1.value:.4f}")
print(f"y2 = {M.y2.value:.4f}")
print(f"y3 = {M.y3.value:.4f}")
print(f"Objective = {M.obj.expr():.4f}")