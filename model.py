from gurobipy import GRB, Model, quicksum
from random import randint, random
import csv
import random
from datos import transacciones, emisiones_carga, parametros, int_comp

# Como usamos randint entre 1 y 5, y entre 4 y 8, podríamos poner 4 o 5 nomas
random.seed(5)

# Defininir los conjuntos
Bencinero = range(1, 6151) # I ✅
Electrico = range(1, 10001) # J ✅
Anos = range(1, 16) # T ✅

# Definir los parámetros
Cprod = parametros["Cprod"] # ✅ 
Cope_j = parametros["Cope_j"] # ✅  
Cope_i = {i: parametros["Cope_i"] for i in Bencinero} # ✅ 
Ccar = {t: int_comp(parametros["Ccar"], t) for t in Anos} # ✅ 
Cben = {(i, t): int_comp(parametros["Cben"], t) if i <= 2150 else int_comp(parametros["Cben2"], t) for i in Bencinero for t in Anos} # ✅ 
Cmante = parametros["Cmante"] # ✅ 
Cmantb = {i: parametros["Cmantb"] if i <= 2150 else parametros["Cmantb2"] for i in Bencinero} # ✅ 
D = {t: transacciones[t - 1] * 1000000 / 365 for t in Anos} # ✅ 
Emax = {t: parametros["Emax"] for t in Anos} # ✅
Eprod = parametros["Eprod"] # ✅ 
Ecar = {t: emisiones_carga[t - 1] for t in Anos}
Erb = {i: parametros["Erb"] if i <= 2150 else parametros["Erb2"] for i in Bencinero} # ✅ 
Pme = parametros["Pme"] # ✅ 
Pmb = {i: parametros["Pmb"] if i <= 2150 else parametros["Pmb2"] for i in Bencinero} # ✅ 
P_t = {t: parametros["P_t"] if t == 1 else parametros["P_t2"] for t in Anos} # ✅
Pref = parametros["Pref"] # ✅
V_j = parametros["V_j"]  # ✅ 
V_i = parametros["V_i"] # ✅ 
Vinicio_i = {i: randint(1, 5) if i <= 2150 else randint(4, 8) for i in Bencinero} # ✅ 
Vinicio_j = parametros["Vinicio_j"] # ✅
Pas = parametros["Pas"] # ✅
Plata_km = parametros["Plata_km"] # ✅
M = parametros["M"] # ✅

# Parametros auxiliares
CEprod = Eprod * Pref # ✅ 
CEcar = {t: Pref * Ecar[t] for t in Anos} # ✅ 
CErb = {i: Erb[i] * Pref for i in Bencinero} # ✅ 
Ctot = Cprod + CEprod # ✅ 
Ctu_t = {t: Ccar[t] + Cope_j + CEcar[t] + Cmante for t in Anos} # ✅ 
Ctu_i = {(i,t): Cben[i,t] + CErb[i] + Cope_i[i] + Cmantb[i] for i in Bencinero for t in Anos} # ✅ 

# Crear el modelo vacío (model = Model())
model = Model() # ✅

# Definir las variables
x = model.addVars(Bencinero, Anos, vtype = GRB.BINARY, name="x_it") # ✅
y = model.addVars(Electrico, Anos, vtype = GRB.BINARY, name="y_jt") # ✅
z = model.addVars(Bencinero, Anos, vtype = GRB.BINARY, name="z_it") # ✅
w = model.addVars(Electrico, Anos, vtype = GRB.BINARY, name="w_jt") # ✅
I = model.addVars(Anos, vtype = GRB.CONTINUOUS, name = "I_t") # ✅

# Variables auxiliares
a = model.addVars(Bencinero, vtype= GRB.INTEGER, name = "a_i") # ✅
model.addConstrs((a[i] == quicksum(z[i, t] * t for t in Anos) for i in Bencinero), name="def_a") # ✅
g = model.addVars(Anos, vtype = GRB.CONTINUOUS, name = "G_t") # ✅ 
model.addConstrs((g[t] == quicksum(y[j,t] * (Cope_j + Ccar[t] + Cmante) for j in Electrico)
    + quicksum(x[i,t] * (Cope_i[i] + Cben[i,t] + Cmantb[i]) for i in Bencinero)
    + quicksum(w[j,t] * Cprod for j in Electrico) for t in Anos), name = "def_g") # ✅ 

# Llamar al update (model.update())
model.update() # ✅

# Definir las restricciones
#R1) demanda anual de pasajeros de buses ✅
model.addConstrs((((quicksum(x[i,t]*Pmb[i] for i in Bencinero)+ 
                   quicksum(y[j,t]*Pme for j in Electrico)) * M >= D[t]) for t in Anos) , name = "R1") 

#R2) Los costos totales no pueden sobrepasar el presupuesto anual. ✅
model.addConstrs((I[t] >= 0 for t in Anos), name="R2") 

#R3) La contaminación anual generada no sobrepasa la máxima permitida ✅
model.addConstrs((quicksum(w[j, t] * Eprod for j in Electrico) +
     quicksum(y[j, t] * Ecar[t] for j in Electrico) +
     quicksum(x[i, t] * Erb[i] for i in Bencinero) <= Emax[t]
     for t in Anos), name="R3")  

#R4) Flujo de cada bus bencinero i en el período t ✅
model.addConstrs(((x[i,t] == x[i,t-1]-z[i,t-1]) for i in Bencinero for t in range(2, 16)), name = "R4") 

#R5) Flujo de cada bus eléctrico j en el período t ✅
model.addConstrs(((y[j,t] == y[j, t-1] + w[j,t]) for j in Electrico for t in range(2, 16)), name = "R5") 

#R6) Activación de la variable Wj,t en base a Yj,t ✅
model.addConstrs((w[j,1] == y[j,1]for j in Electrico), name = "R6")

#R7) Cada bus eléctrico j sólo se puede implementar 1 vez ✅
model.addConstrs(((quicksum(w[j, t] for t in Anos) <= 1) for j in Electrico), name="R7")  

#R8) Cada bus bencinero i solo puede estar en su ultimo periodo de funcionamiento una vez ✅
model.addConstrs((
    (quicksum(z[i, t] for t in Anos) == x[i,1]) for i in Bencinero), name="R8")

#R9) Funcionamiento en base a la vida  útil de los buses eléctricos ✅
model.addConstrs(((quicksum(y[j,t] for t in Anos)) <= V_j for j in Electrico), name = "R9")

#R10) Funcionamiento en base a la vida útil de los buses bencineros ✅
model.addConstrs((a[i] <= V_i - Vinicio_i[i] for i in Bencinero), name= "R10") 

#R11) Inventario de dinero en el periodo 1 ✅
model.addConstr(I[1] == P_t[1] - g[1] + D[1] * Pas + quicksum(y[j,1] * Plata_km * 90000 for j in Electrico)
    + quicksum(x[i,1] * Plata_km * 90000 * 0.93 for i in Bencinero), name = "R11") 

#R12) Inventario de dinero en el periodo t ∈ {2,...,T} ✅
model.addConstrs((I[t] == I[t - 1] + P_t[t] - g[t] + D[t] * Pas
    + quicksum(y[j,t] * Plata_km * 90000 * 0.93 for j in Electrico) 
    + quicksum(x[i,t] * Plata_km * 90000 * 0.93 for i in Bencinero) for t in Anos if t >= 2), name = "R12")

# Definir el objetivo
objetivo = (quicksum(x[i,t] * Ctu_i[i, t] for i in Bencinero for t in Anos) 
    + quicksum(y[j,t] * Ctu_t[t] for j in Electrico for t in Anos)
    + quicksum(w[j,t] * Ctot for j in Electrico for t in Anos)) # ✅

# Settear el objetivo
model.setObjective(objetivo, GRB.MINIMIZE) # ✅
model.Params.MIPGap = 0.02
# Optimizar
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


# generar CSV

datos_csv = []

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
            
    inventario = I[ano].x

    datos_csv.append([ano, bencineros, electricos, producidos, ultimo, inventario])

with open('datos_tabla.csv', 'w', newline='') as archivo_csv:
    columnas = ['Año', 'Bencineros', 'Electricos', 'Buses Producidos', 'Bencineros último año', 'Inventario']
    escritor_csv = csv.writer(archivo_csv)

    escritor_csv.writerow(columnas)
    escritor_csv.writerows(datos_csv)
