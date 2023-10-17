from gurobipy import GRB, Model, quicksum
from random import randint

# defininir los conjuntos

Bencinero = range(6150) # I 
Electrico = range(10000) # J 
Anos = range(15) # T

# definir los parámetros

emisiones_carga = [42.408, 36.936, 35.568, 35.568, 34.2, 31.464, 30.096,
25.992, 21.888, 20.52, 20.52, 19.152, 17.784, 16.416, 13.68]

transacciones = [352.6, 357.0075, 359.21125, 360.313125, 362.2965,
362.516875, 365.8225, 370.23, 372.43375, 374.6375, 376.84125, 379.045, 
380.89615, 381.24875, 395.573125]


Cprod = {j: 8282.27 for j in Electrico} # ✅
Cope_j = {j: 222.74 for j in Electrico} # ✅
Cope_i = {i: 4968.13 if i <= 2150 else 1044.44 for i in Bencinero} # ✅
Ccar = {j: 222.74 for j in Electrico} # ✅
Cben = {i: 1183.91 if i <= 2150 else 1043.19 for i in Bencinero} # ✅
Cmante = {j: 415.77 for j in Electrico} # ✅
Cmantb = {i: 2142.7 if i <= 2150 else 376.5 for i in Bencinero} # ✅
D = {t: transacciones[t] for t in Anos} # ✅
Emax = {t: randint() for t in Anos} # pendiente
Eprod = {j: 42 for j in Electrico} # ✅
Ecar = {t: emisiones_carga[t] for t in Anos}
Erb = {i: 131.54 if i <= 2150 else 157 for i in Bencinero} # ✅
Pme = {j: 81 for j in Electrico} # ✅
Pmb = {i: 99 if i <= 2150 else 81 for i in Bencinero}
P = {t: randint() for t in Anos} # pendiente
Pref = 0.823 # ✅
V_j = {j: 15 for j in Electrico} # ✅
V_i = {i: 10 for i in Bencinero} # ✅
Vinicio_i = {i: randint(1, 5) if i <= 2150 else randint(4, 8) for i in Bencinero} # ✅
Vinicio_j = {j: randint(1, 3) if j <= 750 else 0 for j in Electrico} # ✅

# Parametros auxiliares
# revisar
CEprod = {j: Eprod[j] * Pref for j in Electrico} # ✅
CEcar = {t: Pref * Ecar[t] for t in Anos} # ✅
CErb = {i: Erb[i] * Pref for i in Bencinero} # ✅
Ctot = {j: Cprod[j] + CEprod[j] for j in Electrico} # ✅
Ctu_j = {(j,t): Ccar[j] + Cope_j[j] + CEcar[t] + Cmante[j] for j in Electrico for t in Anos} # ✅
Ctu_i = {i: Cben[i] + CErb[i] + Cope_i[i] + Cmantb[i] for i in Bencinero} # ✅

# crear el modelo vacío (model = Model())

model = Model()

# definir las variables

x = model.addVars(Bencinero, Anos, vtype = GRB.BINARY, name="x_it")
y = model.addVars(Electrico, Anos, vtype = GRB.BINARY, name="y_jt")
z = model.addVars(Bencinero, Anos, vtype = GRB.BINARY, name="z_it")
w = model.addVars(Electrico, Anos, vtype = GRB.BINARY, name="w_jt")


# llamar al update (model.update())
model.update()

# definir las restricciones

# hacer el setObjective (GRB.MINIMIZE)

# model.optimize()

# printear soluciones