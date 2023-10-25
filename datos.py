emisiones_carga = [42.408, 36.936, 35.568, 35.568, 34.2, 31.464, 30.096,
25.992, 21.888, 20.52, 20.52, 19.152, 17.784, 16.416, 13.68] # ✅

transacciones = [352.6, 357.0075, 359.21125, 360.313125, 362.2965,
362.516875, 365.8225, 370.23, 372.43375, 374.6375, 376.84125, 379.045, 
380.89615, 381.24875, 395.573125] # ✅

parametros = {
    "Cprod": 8282.27,
    "Cope_j": 222.74,
    "Cope_i": 1044.44,
    "Ccar": 222.74,
    "Cben": 1183.91,
    "Cben2": 1043.19,
    "Cmante": 415.77,
    "Cmantb": 214.27,
    "Cmantb2": 376.5, 
    "Emax": 2000000, 
    "Eprod": 42, 
    "Erb": 131.54, 
    "Erb2": 157,
    "Pme": 81, 
    "Pmb": 99, 
    "Pmb2": 81, 
    "P_t": 9000000, 
    "P_t2": 4000000, 
    "Pref": 0.823, 
    "V_j": 15, 
    "V_i": 10,
    "Vinicio_j": 0, 
    "Pas": 0.017 * 365, 
    "Plata_km": 0.014, 
    "M": 1.7
    }

def int_comp(valor, n):
    nuevo_valor = valor * (1.0416) ** n
    return nuevo_valor

