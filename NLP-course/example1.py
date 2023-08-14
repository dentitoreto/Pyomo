# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AJJRXkf1oUTVqK0zQXVRBfQwzQl8Cypn
"""

!pip install pyomo
!wget -N -q "https://matematica.unipv.it/gualandi/solvers/ipopt-linux64.zip"
!unzip -o -q ipopt-linux64
import pyomo.environ as pyo
from pyomo.opt import SolverFactory

model = pyo.ConcreteModel()

model.x1 = pyo.Var(domain = pyo.NonNegativeReals)
x1 = model.x1
model.x2 = pyo.Var(domain = pyo.NonNegativeReals)
x2 = model.x2

def objective_rule(model):
  return x1*x2 - 180
model.obj = pyo.Objective(rule = objective_rule, sense = pyo.maximize)

def con1(model):
  return 0.5*(x1 - x2) <= -4
model.co1 = pyo.Constraint(rule = con1)

def con2(model):
  return 2*(x1+x2) <= 194
model.co2 = pyo.Constraint(rule = con2)

solver = SolverFactory('ipopt', executable = '/content/ipopt')
results = solver.solve(model)
print(results)
print('Objective function', model.obj())
print('Variables: \tx1 =', x1(),'\n\t\tx2 =',x2())
