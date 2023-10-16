from gurobipy import GRB, Model, quicksum
from random import randint

# defininir los conjuntos

Bencinero = range() # I Completar
Electrico = range() # J Completar
Años = range() # T Completar

# definir los parámetros

Cprod = {j: randint() for j in Electrico}
Cch = 10 # Completar
Ccar = {j: randint() for j in Electrico}
Cben = {i: randint() for i in Bencinero}
D = {t: randint() for t in Años}
Emax = {t: randint() for t in Años}
Eprod = {j: randint() for j in Electrico}
Erb = {i: randint() for i in Bencinero}
Pme = {j: randint() for j in Electrico}
Pmb = {i: randint() for i in Bencinero}
P = {t: randint() for t in Años}
Pref = 10 # Completar
V_j = {j: randint() for j in Electrico}
V_i = {i: randint() for i in Bencinero}
Vinicio_i = {i: randint() for i in Bencinero}
Vinicio_j = {j: randint() for j in Electrico}

# Parametros auxiliares

CEprod = {j: Eprod[j] * Pref for j in Electrico}
CErb = {i: Erb[i] * Pref for i in Bencinero}
Ctot = {j: Cprod[j] + CEprod[j] for j in Electrico}
Ctu_j = {j: Ccar[j] + Cch for j in Electrico}
Ctu_i = {i: Cben[i] + CErb[i] + Cch for i in Bencinero}

# crear el modelo vacío (model = Model())

model = Model()

# definir las variables

x = model.addVars(Bencinero, Años, vtype = GRB.BINARY, name="x_it")
y = model.addVars(Electrico, Años, vtype = GRB.BINARY, name="y_jt")
z = model.addVars(Bencinero, Años, vtype = GRB.BINARY, name="z_it")
w = model.addVars(Electrico, Años, vtype = GRB.BINARY, name="w_jt")


# llamar al update (model.update())

model.update()

# definir las restricciones

# hacer el setObjective (GRB.MINIMIZE)

# model.optimize()

# printear soluciones