from gurobipy import GRB, Model, quicksum
from random import randint

# defininir los conjuntos

Bencinero = range(1, 6151) # I ✅
Electrico = range(1, 10001) # J ✅
Anos = range(1, 16) # T ✅

# definir los parámetros

emisiones_carga = [42.408, 36.936, 35.568, 35.568, 34.2, 31.464, 30.096,
25.992, 21.888, 20.52, 20.52, 19.152, 17.784, 16.416, 13.68] # ✅

transacciones = [352.6, 357.0075, 359.21125, 360.313125, 362.2965,
362.516875, 365.8225, 370.23, 372.43375, 374.6375, 376.84125, 379.045, 
380.89615, 381.24875, 395.573125] # ✅

def int_comp(valor, n):
    nuevo_valor = valor * (1.0416) ** n
    return nuevo_valor



Cprod = 8282.27 # ✅ 
Cope_j = 222.74 # ✅ 
# Cope_i = {i: 496.813 if i <= 2150 else 1044.44 for i in Bencinero} # ✅ 
Cope_i = {i: 1044.44 for i in Bencinero} # ✅ 
Ccar = {t: int_comp(222.74, t) for t in Anos} # ✅ 
Cben = {(i, t): int_comp(1183.91, t) if i <= 2150 else int_comp(1043.19, t) for i in Bencinero for t in Anos} # ✅ 
Cmante = 415.77 # ✅ 
Cmantb = {i: 214.27 if i <= 2150 else 376.5 for i in Bencinero} # ✅ 
D = {t: transacciones[t - 1] * 1000000 / 365 for t in Anos} # ✅ 
Emax = {t: 1000000 for t in Anos} # ⚠️ pendiente
Eprod = 42 # ✅ 
Ecar = {t: emisiones_carga[t - 1] for t in Anos}
Erb = {i: 131.54 if i <= 2150 else 157 for i in Bencinero} # ✅ 
Pme = 81 # ✅ 
Pmb = {i: 99 if i <= 2150 else 81 for i in Bencinero} # ✅ 
P_t = {t: 4000000 for t in Anos} # pendiente, revisar la plata por km y pasajero ⚠️
Pref = 0.823 # ✅
V_j = 15  # ✅ 
V_i = 10 # ✅ 
Vinicio_i = {i: randint(1, 5) if i <= 2150 else randint(4, 8) for i in Bencinero} # ✅ 
# Vinicio_j = {j: randint(1, 3) if j <= 750 else 0 for j in Electrico} # ✅🛫🟨 
Vinicio_j = 0 # ✅🛫
Pas = 0.017 * 365
Plata_km = 0.014
M = 2 # ⚠️ CAMBIAR VALOR 7 ES!! 

# Parametros auxiliares
CEprod = Eprod * Pref # ✅ 
CEcar = {t: Pref * Ecar[t] for t in Anos} # ✅ 
CErb = {i: Erb[i] * Pref for i in Bencinero} # ✅ 
Ctot = Cprod + CEprod # ✅ 
Ctu_t = {t: Ccar[t] + Cope_j + CEcar[t] + Cmante for t in Anos} # ✅ 
Ctu_i = {(i,t): Cben[i,t] + CErb[i] + Cope_i[i] + Cmantb[i] for i in Bencinero for t in Anos} # ✅ 
Cna_i = {(i,t): Cope_i[i] + Cben[i,t] + Cmantb[i] for i in Bencinero for t in Anos} # ✅ 
Cna_j = {t: Cope_j + Ccar[t] + Cmante for t in Anos}

# crear el modelo vacío (model = Model())

model = Model() # ✅

# definir las variables

x = model.addVars(Bencinero, Anos, vtype = GRB.BINARY, name="x_it") # ✅
y = model.addVars(Electrico, Anos, vtype = GRB.BINARY, name="y_jt") # ✅
z = model.addVars(Bencinero, Anos, vtype = GRB.BINARY, name="z_it") # ✅
w = model.addVars(Electrico, Anos, vtype = GRB.BINARY, name="w_jt") # ✅
I = model.addVars(Anos, vtype = GRB.CONTINUOUS, name = "I_t") # ✅

# variables auxiliares
# sumatoria: quicksum(lo que está adentro de la sumatoria for i in Lo que sea)
a = model.addVars(Bencinero, vtype= GRB.INTEGER, name = "a_i") # ✅
model.addConstrs((a[i] == quicksum(z[i, t] * t for t in Anos) for i in Bencinero), name="def_a") # ✅
g = model.addVars(Anos, vtype = GRB.CONTINUOUS, name = "G_t")
model.addConstrs((g[t] == quicksum(y[j,t] * Cna_j[t] for j in Electrico) + quicksum(x[i,t] * Cna_i[i, t] for i in Bencinero) + quicksum(w[j,t] * Cprod for j in Electrico) for t in Anos), name = "def_g")
# llamar al update (model.update())
model.update() # ✅

# definir las restricciones

#1)
model.addConstrs((((quicksum(x[i,t]*Pmb[i] for i in Bencinero)+ 
                   quicksum(y[j,t]*Pme for j in Electrico)) * M >= D[t]) for t in Anos) , name = "R1") # R1 demanda anual de pasajeros de buses ✅

#2)
model.addConstrs((I[t] >= 0 for t in Anos), name="R2") # R2 Los costos totales no pueden sobrepasar el presupuesto anual. ✅

#3)
model.addConstrs((quicksum(w[j, t] * Eprod for j in Electrico) +
     quicksum(y[j, t] * Ecar[t] for j in Electrico) +
     quicksum(x[i, t] * Erb[i] for i in Bencinero) <= Emax[t]
     for t in Anos), name="R3")  #R3 La contaminación anual generada no sobrepasa la máxima permitida ✅

#4)
model.addConstrs(((x[i,t] == x[i,t-1]-z[i,t-1]) for i in Bencinero for t in range(2, 16)), name = "R4") # R4 Flujo de cada bus bencinero i en el período t ✅

#5)
model.addConstrs(((y[j,t] == y[j, t-1] + w[j,t]) for j in Electrico for t in range(2, 16)), name = "R5") #R5 Flujo de cada bus eléctrico j en el período t ✅

#6)
model.addConstrs((w[j,1] == y[j,1]for j in Electrico), name = "R6") # R6 Activación de la variable Wj,t en base a Yj,t ✅

#7)
model.addConstrs(((quicksum(w[j, t] for t in Anos) <= 1) for j in Electrico),
    name="R7") # R7 Cada bus eléctrico j sólo se puede implementar 1 vez ✅

#8)
#model.addConstrs(((z[i,t] <= x[i,t]) for i in Bencinero for t in Anos), name = "R8") # R8 Activación de la variable Zi,t en base a Xi,t ✅

#9)
model.addConstrs((
    (quicksum(z[i, t] for t in Anos) == x[i,1]) for i in Bencinero),
    name="R9")  # R9 Cada bus bencinero i solo puede estar en su ultimo periodo de funcionamiento una vez ✅ 

#10)
model.addConstrs(((quicksum(y[j,t] for t in Anos)) <= V_j for j in Electrico), name = "R10") # R10 Funcionamiento en base a la vida  útil de los buses eléctricos ✅

#11)
model.addConstrs((a[i] <= V_i - Vinicio_i[i] for i in Bencinero), name= "R11") #R11 Funcionamiento en base a la vida útil de los buses bencineros ✅

# #12)
# model.addConstr(I[1] == P_t[1] - quicksum(y[j,1] * Cna_j[1] for j in Electrico) - quicksum(x[i,1] * Cna_i[i, 1] for i in Bencinero) - quicksum(y[j,1] * Plata_km * 90000 for j in Electrico) + quicksum(x[i,1] * Plata_km * 90000 for i in Bencinero), name = "R12") # ✅ 

# #13)
# model.addConstrs((I[t] == I[t - 1] + P_t[t] - quicksum(y[j,t] * Cna_j[t] for j in Electrico) - quicksum(x[i,t] * Cna_i[i, t] for i in Bencinero) + D[t - 1] * Pas + quicksum(y[j,t] * Plata_km * 90000 for j in Electrico) + quicksum(x[i,t] * Plata_km * 90000 for i in Bencinero) for t in Anos if t >= 2), name = "R13") # ✅ 
#12)+ D[1] * Pas + quicksum(y[j,1] * Plata_km * 90000 for j in Electrico) + quicksum(x[i,1] * Plata_km * 90000 for i in Bencinero)
model.addConstr(I[1] == P_t[1] - g[1] + D[1] * Pas + quicksum(y[j,1] * Plata_km * 90000 for j in Electrico) + quicksum(x[i,1] * Plata_km * 90000 for i in Bencinero), name = "R12") # ✅ 

#13) + D[t] * Pas + quicksum(y[j,t] * Plata_km * 90000 for j in Electrico) + quicksum(x[i,t] * Plata_km * 90000 for i in Bencinero)
model.addConstrs((I[t] == I[t - 1] + P_t[t] - g[t] + D[t] * Pas + quicksum(y[j,t] * Plata_km * 90000 for j in Electrico) + quicksum(x[i,t] * Plata_km * 90000 for i in Bencinero) for t in Anos if t >= 2), name = "R13") # ✅ 

#model.addConstrs(x[i,1] == 1 for i in Bencinero)
#14)
#model.addConstrs((quicksum(x[i,t] for i in Bencinero) >= 150 for t in Anos if t == 1), name = "R14")

objetivo = (quicksum(x[i,t] * Ctu_i[i, t] for i in Bencinero for t in Anos) + quicksum(y[j,t] * Ctu_t[t] for j in Electrico for t in Anos) + quicksum(w[j,t] * Ctot for j in Electrico for t in Anos)) # ✅


model.setObjective(objetivo, GRB.MINIMIZE) # ✅

model.Params.MIPGap = 0.02

model.optimize() # ✅


# printear soluciones
# Chamullo
lista_bencineros = []
lista_electricos = []
xr = []
lista_implementados = []
print(f" es xd {model.ObjVal}")
for ano in Anos:
    agregar_elec = []
    agregarw = []
    for bencina in Bencinero:
        if x[bencina, ano].x != 0:
            lista_bencineros.append([bencina, ano])
        
    for electrico in Electrico:
        if y[electrico, ano].x != 0:
            agregar_elec.append([electrico, ano])
            xr.append(f"{electrico}, {ano}")

    lista_electricos.append(agregar_elec)
    for l in Electrico:
        if w[l, ano].x != 0:
            agregarw.append([l, ano])
            lista_implementados.append([l, ano])

for ano in Anos:
    bencineros = 0
    ultimo = 0
    for bencina in Bencinero:
        if x[bencina, ano].x == 1:
            bencineros += 1
        if z[bencina, ano].x == 1:
            ultimo += 1
    electricos = 0
    producidos = 0
    for electrico in Electrico:
        if y[electrico, ano].x == 1:
            electricos += 1
        if w[electrico, ano].x == 1:
            producidos += 1
    print(f'[AÑO {ano}] bencineros: {bencineros} electricos: {electricos}')
    print(f'PRODUCIDOS: {producidos}')
    print(f'BENCINEROS EN ÚLTIMO AÑO: {ultimo}')
    print(f'INVENTARIO: {I[ano].x}')

# print(len(xr))
# print(len(lista_bencineros))
# print("pov")
# print(lista_bencineros)
# print("pov")
# print(lista_electricos[0])
# print("pov")
# print(len(lista_implementados))
