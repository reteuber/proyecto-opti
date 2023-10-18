from gurobipy import GRB, Model, quicksum
from random import randint

# defininir los conjuntos

Bencinero = range(6150) # I ✅
Electrico = range(10000) # J ✅
Anos = range(15) # T ✅

# definir los parámetros

emisiones_carga = [42.408, 36.936, 35.568, 35.568, 34.2, 31.464, 30.096,
25.992, 21.888, 20.52, 20.52, 19.152, 17.784, 16.416, 13.68] # ✅

transacciones = [352.6, 357.0075, 359.21125, 360.313125, 362.2965,
362.516875, 365.8225, 370.23, 372.43375, 374.6375, 376.84125, 379.045, 
380.89615, 381.24875, 395.573125] # ✅


Cprod = {j: 8282.27 for j in Electrico} # ✅
Cope_j = {j: 222.74 for j in Electrico} # ✅
Cope_i = {i: 4968.13 if i <= 2150 else 1044.44 for i in Bencinero} # ✅
Ccar = {j: 222.74 for j in Electrico} # ✅
Cben = {i: 1183.91 if i <= 2150 else 1043.19 for i in Bencinero} # ✅
Cmante = {j: 415.77 for j in Electrico} # ✅
Cmantb = {i: 2142.7 if i <= 2150 else 376.5 for i in Bencinero} # ✅
D = {t: transacciones[t] for t in Anos} # ✅
Emax = {t: randint(1,10) for t in Anos} # ⚠️ pendiente
Eprod = {j: 42 for j in Electrico} # ✅
Ecar = {t: emisiones_carga[t] for t in Anos}
Erb = {i: 131.54 if i <= 2150 else 157 for i in Bencinero} # ✅
Pme = {j: 81 for j in Electrico} # ✅
Pmb = {i: 99 if i <= 2150 else 81 for i in Bencinero} # ✅
P = 4000000 # pendiente, revisar la plata por km y pasajero ⚠️
Pref = 0.823 # ✅
V_j = {j: 15 for j in Electrico} # ✅
V_i = {i: 10 for i in Bencinero} # ✅
Vinicio_i = {i: randint(1, 5) if i <= 2150 else randint(4, 8) for i in Bencinero} # ✅
print(Vinicio_i[1])
Vinicio_j = {j: randint(1, 3) if j <= 750 else 0 for j in Electrico} # ✅
M = 4 # ⚠️ CAMBIAR VALOR
# Parametros auxiliares
# revisar
CEprod = {j: Eprod[j] * Pref for j in Electrico} # ✅
CEcar = {t: Pref * Ecar[t] for t in Anos} # ✅
CErb = {i: Erb[i] * Pref for i in Bencinero} # ✅
Ctot = {j: Cprod[j] + CEprod[j] for j in Electrico} # ✅
Ctu_j = {(j,t): Ccar[j] + Cope_j[j] + CEcar[t] + Cmante[j] for j in Electrico for t in Anos} # ✅
Ctu_i = {i: Cben[i] + CErb[i] + Cope_i[i] + Cmantb[i] for i in Bencinero} # ✅



# crear el modelo vacío (model = Model())

model = Model() # ✅

# definir las variables

x = model.addVars(Bencinero, Anos, vtype = GRB.BINARY, name="x_it") # ✅
y = model.addVars(Electrico, Anos, vtype = GRB.BINARY, name="y_jt") # ✅
z = model.addVars(Bencinero, Anos, vtype = GRB.BINARY, name="z_it") # ✅
w = model.addVars(Electrico, Anos, vtype = GRB.BINARY, name="w_jt") # ✅

# variables auxiliares
# sumatoria: quicksum(lo que está adentro de la sumatoria for i in Lo que sea)
a = model.addVars(Bencinero, vtype= GRB.INTEGER, name = "a_i") # revisar ⚠️
model.addConstrs((a[i] == quicksum(z[i, t] * t for t in Anos) for i in Bencinero), name="def_a") # revisar ⚠️

# llamar al update (model.update())
model.update() # ✅

# definir las restricciones

#1)
model.addConstrs(((quicksum(x[i,t]*Pmb[i] for i in Bencinero)+ 
                   (quicksum(y[j,t]*Pme[j] for j in Electrico))<= D[t]*M) for t in Anos) , name = "R1") # R1 demanda anual de pasajeros de buses ✅

#2)
#model.addConstrs(((quicksum(x[i,t]*(Cben[i]+Cope_i[i]+Cmantb[i]) for i in Bencinero) # revisar ⚠️
 #                  + (quicksum(y[j,t]*(Ccar[j]+Cope_j[j]+Cmante) for j in Electrico
  #                  + (quicksum(w[j,t]*Cprod[j]) for j in Electrico))) <= P) for t in Anos), name = "R2") # R2 Los costos totales no pueden sobrepasar el presupuesto anual. ✅

model.addConstrs(((quicksum(x[i, t] * (Cben[i] + Cope_i[i] + Cmantb[i]) for i in Bencinero) #REVISAR, CORREGI CON CHATGPT PERO NOSE SI SIGNIFICARA LO MISMO
     + quicksum(y[j, t] * (Ccar[j] + Cope_j[j] + Cmante[j]) for j in Electrico)
     + quicksum(w[j, t] * Cprod[j] for j in Electrico)) <= P for t in Anos), name="R2") # R2 Los costos totales no pueden sobrepasar el presupuesto anual. ✅

#3)
#model.addConstrs(((quicksum(w[j,t]*Eprod[j] for j in Electrico) + (quicksum(y[j,t]*Ecar[t]) # revisar ⚠️
 #               for j in Electrico)+(quicksum(x[i,t]*Erb[i]) for i in Bencinero) 
  #              <= Emax[t]) for t in Anos), name = "R3") #R3 La contaminación anual generada no sobrepasa la máxima permitida ✅

model.addConstrs((quicksum(w[j, t] * Eprod[j] for j in Electrico) +
     quicksum(y[j, t] * Ecar[t] for j in Electrico) +
     quicksum(x[i, t] * Erb[i] for i in Bencinero) <= Emax[t]
     for t in Anos), name="R3")  #R3 La contaminación anual generada no sobrepasa la máxima permitida ✅

#4)
model.addConstrs(((x[i,t] == x[i,t-1]-z[i,t-1]) for i in Bencinero for t in range(2, len(Anos))), name = "R4") # R4 Flujo de cada bus bencinero i en el período t ✅

#5)
model.addConstrs(((y[j,t] == y[j, t-1]+w[j,t]) for j in Electrico for t in range(2, len(Anos))), name = "R5") #R5 Flujo de cada bus eléctrico j en el período t ✅

#6)
model.addConstrs((w[j,t] <= y[j,t]for j in Electrico for t in Anos), name = "R6") # R6 Activación de la variable Wj,t en base a Yj,t ✅

#7)
#model.addConstrs((((quicksum(w[j,t]) for t in Anos)<=1) for j in Electrico), name = "R7") # R7 Cada bus eléctrico j sólo se puede implementar 1 vez ✅ # revisar ⚠️

model.addConstrs((
    (quicksum(w[j, t] for t in Anos) <= 1) for j in Electrico),
    name="R7") # R7 Cada bus eléctrico j sólo se puede implementar 1 vez ✅ # revisar ⚠️

#8)
model.addConstrs(((z[i,t]<=x[i,t]) for i in Bencinero for t in Anos), name = "R8") # R8 Activación de la variable Zi,t en base a Xi,t ✅

#9)
#model.addConstrs((((quicksum(z[i,t]) for t in Anos)<=1) for i in Bencinero), name = "R9") # R9 Cada bus bencinero i solo puede estar en su ultimo periodo de funcionamiento una vez ✅ # revisar ⚠️

model.addConstrs((
    (quicksum(z[i, t] for t in Anos) <= 1) for i in Bencinero),
    name="R9")  # R9 Cada bus bencinero i solo puede estar en su ultimo periodo de funcionamiento una vez ✅ # revisar ⚠️

#10)
model.addConstrs(((quicksum(y[j,t] for t in Anos))<=(V_j[j] - Vinicio_j[j]) for j in Bencinero), name = "R10") # R10 Funcionamiento en base a la vida  útil de los buses eléctricos ✅

#11)
#model.addConstr((a[i] <= V_i[i] - Vinicio_i[i] for i in Bencinero), name= "R11") #R11 Funcionamiento en base a la vida útil de los buses bencineros ✅ ⚠️ NO FUNCIONA

# hacer el setObjective (GRB.MINIMIZE)

objetivo = (quicksum(x[i,t] * Ctu_i[i] for i in Bencinero for t in Anos) + quicksum(y[j,t] * Ctu_j[j][t] for j in Electrico for t in Anos) + quicksum(w[j,t] * Ctot[j] for j in Electrico for t in Anos)) # ✅ # revisar ⚠️ NO FUNCIONA

#objetivo = (quicksum(quicksum(x[i,t] * Ctu_i[i] for i in Bencinero) for t in Anos) + quicksum(quicksum(y[j,t] * Ctu_j[j][t] for j in Electrico) for t in Anos) + quicksum(quicksum(w[j,t] * Ctot[j] for j in Electrico) for t in Anos)) # ✅ # revisar ⚠️ NO FUNCIONA


model.setObjective(objetivo, GRB.MNIMIZE) # ✅
model.optimize() # ✅


# printear soluciones

print(model.ObjVal)