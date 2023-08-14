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

model.i = pyo.Set(initialize = ['V_oil','oil1','oil_0.4'])
model.j = pyo.Set(initialize = model.i)

model.LU = pyo.Param(model.i, initialize = {'V_oil':0.75,'oil1':1,'oil_0.4':1})
model.SP = pyo.Param(model.i, initialize = {'V_oil':4.45,'oil1':3.03,'oil_0.4':3.03})
model.OC = pyo.Param(model.i, initialize = {'V_oil':3.45,'oil1':2.7,'oil_0.4':2.8})
model.PC = pyo.Param(model.i, initialize = {'V_oil':0.75,'oil1':0.15,'oil_0.4':0.15})
model.SC = pyo.Param(model.i, initialize = {'V_oil':0.02,'oil1':0.02,'oil_0.4':0.02})
model.Y =  pyo.Param(model.i, initialize = {'V_oil':0.08,'oil1':0.04,'oil_0.4':0.04})
model.RA = pyo.Param(model.i, initialize = {'V_oil':350000,'oil1':750000,'oil_0.4':750000})
model.MK = pyo.Param(model.i, initialize = {'V_oil':175000,'oil1':900000,'oil_0.4':750000})
model.PS = pyo.Param(model.i, initialize = {'V_oil':35000,'oil1':100000,'oil_0.4':100000})

model.x = pyo.Var(model.i,domain = pyo.NonNegativeReals)
x = model.x

def objective_rule(model,i):
  return sum(x[i] * model.LU[i] * (model.SP[i] - (x[i] * model.LU[i]/(100*model.RA[i]))) for i in model.i)- sum(x[i] * model.LU[i] * model.OC[i] for i in model.i) - sum(x[i] * model.PC[i] for i in model.i) - sum(x[i] * model.LU[i] * model.SC[i] * (1 + model.Y[i] * (x[i] * model.LU[i] / sum(x[j] * model.LU[j] for j in model.j))) for i in model.i)
model.obj = pyo.Objective(rule = objective_rule, sense = pyo.maximize)

model.obj = pyo.Objective(rule = objective_rule, sense = pyo.maximize)

def con1(model,i):
  return sum(x[i] / model.PS[i] for i in model.i) <= 20
model.con1 = pyo.Constraint(rule = con1)


def con2(model):
  return x['V_oil'] / model.LU['V_oil']  >= model.MK['V_oil']
model.con2 = pyo.Constraint(rule = con2)

def con3(model):
  return x['oil1'] / model.LU['oil1']  >= model.MK['oil1']
model.con3 = pyo.Constraint(rule = con3)

def con4(model):
  return x['oil_0.4'] / model.LU['oil_0.4']  >= model.MK['oil_0.4']
model.con4 = pyo.Constraint(rule = con4)



solver = SolverFactory('ipopt', executable = '/content/ipopt')
results = solver.solve(model)
print(results)
print('objective function', model.obj())
for i in model.i:
  print('units of', i, 'produced is', x[i]())

