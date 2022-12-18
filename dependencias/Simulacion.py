# Librerias
import math
import pickle
from dependencias import TratamientoDatos
from scipy.stats import *
import random
import numpy as np

distribucionesEquipos = {}
distribucionesJugadores = {}
diccionarioSolucion = {}

estadisticasJugadores = {}
estadisticasEquipos = {}

equipoOrden = []

tiempoParaTiro = 2

contadorProrroga = 0

def simularPartido(nombreEquipo, nombreEquipo2):
    global distribucionesEquipos; global distribucionesJugadores; global equipoOrden; global tiempoParaTiro; global diccionarioSolucion; global estadisticasJugadores; global estadisticasEquipos; global contadorProrroga

    distribucionesEquipos = {}
    distribucionesJugadores = {}
    diccionarioSolucion = {}

    estadisticasJugadores = {}
    estadisticasEquipos = {}

    equipoOrden = []

    contadorProrroga = 0
    
    TratamientoDatos.cargaDatosGeneral()
    infile = open(".\Ficheros\DistribucionesEquipos", "rb")
    distribucionesEquipos = pickle.load(infile)
    infile.close()
    infile = open(".\Ficheros\DistribucionesJugadores", "rb")
    distribucionesJugadores = pickle.load(infile)
    infile.close()

    
    inicializarEquipos(nombreEquipo[1], nombreEquipo2[1])
    inicializarJugadores(nombreEquipo[1], nombreEquipo2[1])

    pbp = {'equipo':[], 'jugador':[], 'accion':[], 'cuarto':[], 'tiempo':[], 'resultado':[]}
    tiempo = 720
    cuarto = 1
    saque = 0
    maximo = 24
    prorroga = False
    
    while tiempo > 0 or cuarto != 4 or prorroga:

        if cuarto == 1 and tiempo == 720:

            # Equipo es un valor 0 o 1 según el equipo correspondiente, si necesitamos el nombre con valor 0 es equipo y con valor 1 es equipo2
            equipo = saltoInicial()
            equipoOrden.append(nombreEquipo[1])
            equipoOrden.append(nombreEquipo2[1])
            # determinamos el equipo que saltara el siguiente cuarto
            saque = (equipo + 1) % 2
            
            pbp['equipo'].append(equipoOrden[equipo])
            pbp['jugador'].append("-")
            pbp['accion'].append("ganaSalto")
            if not prorroga :
                pbp['cuarto'].append(cuarto)
            else :
                pbp['cuarto'].append("OT" + contadorProrroga)
            pbp['tiempo'].append(tiempo)
            pbp['resultado'].append("-")

        elif tiempo == 720:

            equipo = saque  # se selecciona el equipo al que le toca sacar de inicio
            saque = (saque + saque) % 2
            
            pbp['equipo'].append(equipoOrden[equipo])
            pbp['jugador'].append("-")
            pbp['accion'].append("saca")
            if not prorroga :
                pbp['cuarto'].append(cuarto)
            else :
                pbp['cuarto'].append("OT" + contadorProrroga)
            pbp['tiempo'].append(tiempo)
            pbp['resultado'].append("-")

        # Se reduce el tiempo de posesión del reloj
        if tiempo > 24:
            tiempoUsado = tiempoPosesion(equipoOrden[equipo], maximo)
        elif tiempo > 14 and maximo == 14:
            tiempoUsado = tiempoPosesion(equipoOrden[equipo], maximo)
        else:
            tiempoUsado = tiempoPosesion(equipoOrden[equipo], tiempo)

        if tiempoUsado == -1:
            tiempo = -1
            
        else:
            tiempo -= tiempoUsado

        if tiempo > 0:

            # Desarrollo de la jugada
            jugador, jugadorAsiste, roboRealizado, faltaRealizada, robador = jugada(equipo)
            if roboRealizado:
                maximo = 24
                equipo = (equipo + 1) % 2
                
                pbp['equipo'].append(equipoOrden[equipo])
                pbp['jugador'].append(robador)
                pbp['accion'].append("roba")
                if not prorroga :
                    pbp['cuarto'].append(cuarto)
                else :
                    pbp['cuarto'].append("OT" + contadorProrroga)
                pbp['tiempo'].append(tiempo)
                pbp['resultado'].append("-")
            else:
                if faltaRealizada and maximo - tiempoUsado < 14:
                    maximo = 14
                    
                    pbp['equipo'].append(equipoOrden[equipo])
                    pbp['jugador'].append("-")
                    pbp['accion'].append("falta")
                    if not prorroga :
                        pbp['cuarto'].append(cuarto)
                    else :
                        pbp['cuarto'].append("OT" + contadorProrroga)
                    pbp['tiempo'].append(tiempo)
                    pbp['resultado'].append("-")
                elif faltaRealizada and maximo - tiempoUsado > 10:
                    maximo = maximo - tiempoUsado
                    
                    pbp['equipo'].append(equipoOrden[equipo])
                    pbp['jugador'].append("-")
                    pbp['accion'].append("falta")
                    if not prorroga :
                        pbp['cuarto'].append(cuarto)
                    else :
                        pbp['cuarto'].append("OT" + contadorProrroga)
                    pbp['tiempo'].append(tiempo)
                    pbp['resultado'].append("-")
                else:
                    # Desarrollo del tiro
                    acierto, tipo = tiro(jugador,jugadorAsiste,equipoOrden[equipo])

                    # Si se falla el tiro se juega el rebote
                    if not acierto:
                        reboteCogido, reboteador = rebote(equipoOrden[equipo], equipoOrden[(equipo + 1) % 2])
                        
                        if reboteCogido:
                            maximo = 14
                            
                            pbp['equipo'].append(equipoOrden[equipo])
                            pbp['jugador'].append(jugador)
                            pbp['accion'].append("tiro_" + str(tipo) + "_ofensivo_" + reboteador)
                            if not prorroga :
                                pbp['cuarto'].append(cuarto)
                            else :
                                pbp['cuarto'].append("OT" + contadorProrroga)
                            pbp['tiempo'].append(tiempo)
                            pbp['resultado'].append("-")
                            # juega el mismo equipo el balón
                        else:
                            maximo = 24
                            equipo = (equipo + 1) % 2
                            
                            pbp['equipo'].append(equipoOrden[equipo])
                            pbp['jugador'].append(jugador)
                            pbp['accion'].append("tiro_" + str(tipo) + "_defensivo_" + reboteador)
                            if not prorroga :
                                pbp['cuarto'].append(cuarto)
                            else :
                                pbp['cuarto'].append("OT" + contadorProrroga)
                            pbp['tiempo'].append(tiempo)
                            pbp['resultado'].append("-")
                            # empieza una nueva posesión del rival
                        
                    else:
                        pbp['equipo'].append(equipoOrden[equipo])
                        pbp['jugador'].append(jugador)
                        pbp['accion'].append("tiro_" + str(tipo) + "_acertado_" + str(jugadorAsiste))
                        if not prorroga :
                            pbp['cuarto'].append(cuarto)
                        else :
                            pbp['cuarto'].append("OT" + contadorProrroga)
                        pbp['tiempo'].append(tiempo)
                        pbp['resultado'].append(str(estadisticasEquipos[equipoOrden[0]]["Puntos"]) + " - " + str(estadisticasEquipos[equipoOrden[1]]["Puntos"]))
                        equipo = (equipo + 1) % 2
        # Si fin de cuarto se sacan los datos del mismo
        else :
            # Si fin del último cuarto se sacan los datos del partido
            if cuarto == 4 or prorroga:
                prorroga = finPartido()
                if prorroga:
                    tiempo = 300
            # Sino se empieza un nuevo cuarto
            else:
                cuarto += 1
                tiempo = 720

    return diccionarioSolucion, pbp


def saltoInicial():
    # Simular salto inicial probabilidad 50% ambos equipos
    return random.randint(0, 1)


def jugada(equipo):
    global equipoOrden
    # Simular jugada
    r, robador = robo(equipoOrden[(equipo + 1)  % 2])
    if r:
        return "","",True,False, robador
    else:
        if falta(equipoOrden[equipo]):
            return "","",False,True, robador
        else:
            jugador,jugadorAsiste = asistencia(equipoOrden[equipo])
    return jugador,jugadorAsiste,False,False, robador


def robo(equipo):
    global estadisticasJugadores; global estadisticasEquipos

    valor = aplicaDistribucionEquipo(equipo, "PorcentajeRobos")[0]
    resultado = random.random()
    maximo = 0
    elegido = ""
    if resultado < valor:
        for jugador in estadisticasEquipos[equipo]["Jugadores"]:
            valor = aplicaDistribucionJugador(jugador, "Robos")[0]
            if valor > maximo:
                maximo = valor
                elegido = jugador
        estadisticasJugadores[equipo][elegido]["EstadisticasPartido"]["Robos"] += 1
        estadisticasEquipos[equipo]["Robos"] += 1
        return True, elegido
    return False, elegido


def falta(equipo):
    global estadisticasEquipos

    valor = aplicaDistribucionEquipo(equipo, "PorcentajeFaltas")[0]
    resultado = random.random()
    if resultado < valor:
        estadisticasEquipos[equipo]["Faltas"] += 1
        return True
    return False


def asistencia(equipo):
    global estadisticasEquipos
    # Decidir quien hace la asistencia, se genera un valor para cada jugador el mas alto asiste
    maximo = 0
    elegido = ""
    elegidoTiro = ""
    valores = {}
    for jugador in estadisticasEquipos[equipo]["Jugadores"]:
        valor = aplicaDistribucionJugador(jugador,"Asistencias")[0]
        if valor > 0:
            valores[jugador] = [maximo, (maximo + valor)]
            maximo += valor
    resultado = random.uniform(0, maximo)
    for jugador in valores:
        if (resultado >= valores[jugador][0]) and (resultado <= valores[jugador][1]) :
            elegido = jugador
    maximo = aplicaDistribucionJugador(elegido, "Asistencias")[0]
    resultado = random.random()

    # Se realiza la asistencia
    if resultado < maximo:
        hayAsistencia = True
    else :
        hayAsistencia = False

    # Decidir el jugador que realizara el tiro
    maximo = 0
    valores = {}
    for jugador in estadisticasEquipos[equipo]["Jugadores"]:
        if jugador != elegido or not hayAsistencia:
            valor = aplicaDistribucionJugador(jugador, "ProbabilidadTiro")[0]
            if valor > 0:
                valores[jugador] = []
                valores[jugador].append(maximo)
                maximo += valor
                valores[jugador].append(maximo)
    resultado = random.uniform(0, maximo)
    for jugador in valores:
        if (resultado >= valores[jugador][0]) and (resultado <= valores[jugador][1]) :
            elegidoTiro = jugador
        
    # No se realiza asistencia tira el jugador que tiene la bola
    if not hayAsistencia:
        elegido = elegidoTiro

    return elegidoTiro, elegido


def tiempoPosesion(equipo, tiempo):
    
    global tiempoParaTiro

    if tiempo <= tiempoParaTiro:
        return -1

    # sino devolvemos un dato generado por una función de distribución triangular
    if tiempo > 24:
        valor = aplicaDistribucionEquipo(equipo, "TiempoPosesion", 24)
    valor = aplicaDistribucionEquipo(equipo, "TiempoPosesion", tiempo)
    return round(valor[0])


def tiro(jugador, jugadorAsistencia, equipo):
    global estadisticasJugadores; global estadisticasEquipos

    # Decidir si el tiro es de dos o de tres
    valor = aplicaDistribucionJugador(jugador,"PorcentajeTriples")[0]
    resultado = random.random()
    if valor > resultado:
        tiro = 3
        estadisticasJugadores[equipo][jugador]["EstadisticasPartido"]["Tiros"] += 1
        estadisticasJugadores[equipo][jugador]["EstadisticasPartido"]["Triples"] += 1
        estadisticasEquipos[equipo]["Tiros"] += 1
        estadisticasEquipos[equipo]["Triples"] += 1
        valor = aplicaDistribucionJugador(jugador, "PorcentajeAciertoTriples")[0]
    else:
        tiro = 2
        estadisticasJugadores[equipo][jugador]["EstadisticasPartido"]["Tiros"] += 1
        estadisticasEquipos[equipo]["Tiros"] += 1
        # Simular tiro
        valor = aplicaDistribucionJugador(jugador,"PorcentajeAciertos")[0]
    resultado = random.random()

    if resultado > valor:
        return False, tiro

    # Sumar estadistica al jugador
    if jugador != jugadorAsistencia:
        estadisticasJugadores[equipo][jugadorAsistencia]["EstadisticasPartido"]["Asistencias"] += 1
        estadisticasEquipos[equipo]["Asistencias"] += 1
    estadisticasJugadores[equipo][jugador]["EstadisticasPartido"]["TirosAnotados"] += 1
    estadisticasJugadores[equipo][jugador]["EstadisticasPartido"]["Puntos"] += tiro
    estadisticasEquipos[equipo]["Puntos"] += tiro
    estadisticasEquipos[equipo]["TirosAnotados"] += 1
    if tiro == 3:
        estadisticasJugadores[equipo][jugador]["EstadisticasPartido"]["TriplesAnotados"] += 1
        estadisticasEquipos[equipo]["TriplesAnotados"] += 1

    return True, tiro


def rebote(equipoPosesion, equipoDefiende):
    global estadisticasEquipos; global estadisticasJugadores
    # Simular rebote
    elegido = ""
    valor = aplicaDistribucionEquipo(equipoPosesion,"PorcentajeRebote")[0]
    valor2 = aplicaDistribucionEquipo(equipoDefiende,"PorcentajeRebote")[0]
    if valor2 < valor:
        # decidir el jugador que suma la estadistica
        estadisticasEquipos[equipoPosesion]["Rebotes"] += 1
        maximo = 0
        valores ={}
        for jugador in estadisticasEquipos[equipoPosesion]["Jugadores"]:
            valor = aplicaDistribucionJugador(jugador, "Asistencias")[0]
            if valor > 0:
                valores[jugador] = [maximo, (maximo + valor)]
                maximo += valor
        resultado = random.uniform(0, maximo)
        for jugador in valores:
            if (resultado >= valores[jugador][0]) and (resultado <= valores[jugador][1]):
                elegido = jugador
        estadisticasJugadores[equipoPosesion][elegido]["EstadisticasPartido"]["Rebotes"] += 1
        return True, elegido

    estadisticasEquipos[equipoDefiende]["Rebotes"] += 1
    maximo = 0
    valores = {}
    for jugador in estadisticasEquipos[equipoDefiende]["Jugadores"]:
        valor = aplicaDistribucionJugador(jugador, "Asistencias")[0]
        if valor > 0:
            valores[jugador] = [maximo, (maximo + valor)]
            maximo += valor
    resultado = random.uniform(0, maximo)
    for jugador in valores:
        if (resultado >= valores[jugador][0]) and (resultado <= valores[jugador][1]):
            elegido = jugador
    # decidir el jugador que suma la estadistica
    estadisticasJugadores[equipoDefiende][elegido]["EstadisticasPartido"]["Rebotes"] += 1
    return False, elegido


def finPartido():
    global estadisticasEquipos; global estadisticasJugadores; global equipoOrden; global diccionarioSolucion; global contadorProrroga
    # Recopilar datos finales
    if estadisticasEquipos[equipoOrden[0]]["Puntos"] == estadisticasEquipos[equipoOrden[1]]["Puntos"]:
        contadorProrroga += 1
        return True
    else:
        diccionarioSolucion = {}
        diccionarioSolucion["visitante"] = equipoOrden[0]
        diccionarioSolucion["local"] = equipoOrden[1]
        diccionarioSolucion["puntuacionVisitante"] = estadisticasEquipos[equipoOrden[0]]["Puntos"]
        diccionarioSolucion["puntuacionLocal"] = estadisticasEquipos[equipoOrden[1]]["Puntos"]

        diccionarioSolucion["estadisticasVisitante"] = {}
        for estadistica in estadisticasEquipos[equipoOrden[0]]:
            if estadistica != "Jugadores":
                diccionarioSolucion["estadisticasVisitante"][estadistica] = estadisticasEquipos[equipoOrden[0]][estadistica]
        diccionarioSolucion["estadisticasVisitante"]["PCT_TirosAnotados"] = ("{0:.2f}".format(float(diccionarioSolucion["estadisticasVisitante"]["TirosAnotados"] / diccionarioSolucion["estadisticasVisitante"]["Tiros"])))
        diccionarioSolucion["estadisticasVisitante"]["PCT_TriplesAnotados"] = ("{0:.2f}".format(float(diccionarioSolucion["estadisticasVisitante"]["TriplesAnotados"] / diccionarioSolucion["estadisticasVisitante"]["Triples"])))

        diccionarioSolucion["estadisticasLocal"] = {}
        for estadistica in estadisticasEquipos[equipoOrden[1]]:
            if estadistica != "Jugadores":
                diccionarioSolucion["estadisticasLocal"][estadistica] = estadisticasEquipos[equipoOrden[1]][estadistica]
        diccionarioSolucion["estadisticasLocal"]["PCT_TirosAnotados"] = ("{0:.2f}".format(float(diccionarioSolucion["estadisticasLocal"]["TirosAnotados"] / diccionarioSolucion["estadisticasLocal"]["Tiros"])))
        diccionarioSolucion["estadisticasLocal"]["PCT_TriplesAnotados"] = ("{0:.2f}".format(float(diccionarioSolucion["estadisticasLocal"]["TriplesAnotados"] / diccionarioSolucion["estadisticasLocal"]["Triples"])))

        diccionarioSolucion["jugadoresVisitante"] = {}
        for jugador in estadisticasEquipos[equipoOrden[0]]["Jugadores"]:
            diccionarioSolucion["jugadoresVisitante"][jugador] = estadisticasJugadores[equipoOrden[0]][jugador]["EstadisticasPartido"]
            if diccionarioSolucion["jugadoresVisitante"][jugador]["Tiros"] != 0:
                diccionarioSolucion["jugadoresVisitante"][jugador]["PCT_TirosAnotados"] = ("{0:.2f}".format(float(diccionarioSolucion["jugadoresVisitante"][jugador]["TirosAnotados"] / diccionarioSolucion["jugadoresVisitante"][jugador]["Tiros"])))
            if diccionarioSolucion["jugadoresVisitante"][jugador]["Triples"] != 0:
                diccionarioSolucion["jugadoresVisitante"][jugador]["PCT_TriplesAnotados"] = ("{0:.2f}".format(float(diccionarioSolucion["jugadoresVisitante"][jugador]["TriplesAnotados"] / diccionarioSolucion["jugadoresVisitante"][jugador]["Triples"])))

        diccionarioSolucion["jugadoresLocal"] = {}
        for jugador in estadisticasEquipos[equipoOrden[1]]["Jugadores"]:
            diccionarioSolucion["jugadoresLocal"][jugador] = estadisticasJugadores[equipoOrden[1]][jugador]["EstadisticasPartido"]
            if diccionarioSolucion["jugadoresLocal"][jugador]["Tiros"] != 0:
                diccionarioSolucion["jugadoresLocal"][jugador]["PCT_TirosAnotados"] = ("{0:.2f}".format(float( diccionarioSolucion["jugadoresLocal"][jugador]["TirosAnotados"] / diccionarioSolucion["jugadoresLocal"][jugador]["Tiros"])))
            if diccionarioSolucion["jugadoresLocal"][jugador]["Triples"] != 0:
                diccionarioSolucion["jugadoresLocal"][jugador]["PCT_TriplesAnotados"] = ("{0:.2f}".format(float(diccionarioSolucion["jugadoresLocal"][jugador]["TriplesAnotados"] /diccionarioSolucion["jugadoresLocal"][jugador]["Triples"])))

        return False

def aplicaDistribucionJugador(jugador, estadistica):
    global distribucionesJugadores
    val = [-1]
    if distribucionesJugadores[jugador][estadistica]["nombre"] == "norm":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        if not math.isnan(loc) or not math.isnan(scale):
            val = norm.rvs(loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "gumbel_r":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        if not math.isnan(loc) or not math.isnan(scale):
            val = gumbel_r.rvs(loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "gumbel_l":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        if not math.isnan(loc) or not math.isnan(scale):
            val = gumbel_l.rvs(loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "logistic":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        if not math.isnan(loc) or not math.isnan(scale):
            val = logistic.rvs(loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "dgamma":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        a = distribucionesJugadores[jugador][estadistica]["parametros"]["a"]
        if not math.isnan(loc) or not math.isnan(scale) or not math.isnan(a):
            val = dgamma.rvs(a,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == 'hypsecant':
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        if not math.isnan(loc) or not math.isnan(scale):
            val = hypsecant.rvs(loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "dweybull":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        c = distribucionesJugadores[jugador][estadistica]["parametros"]["c"]
        if not math.isnan(loc) or not math.isnan(scale) or not math.isnan(c):
            val = weibull_max.rvs(c, loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "genextreme":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        c = distribucionesJugadores[jugador][estadistica]["parametros"]["c"]
        if not math.isnan(loc) or not math.isnan(scale) or not math.isnan(c):
            val = genextreme.rvs(c,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "skewnorm":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        a = distribucionesJugadores[jugador][estadistica]["parametros"]["a"]
        if not math.isnan(loc) or not math.isnan(scale) or not math.isnan(a):
            val = skewnorm.rvs(a,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "genlogistic":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        c = distribucionesJugadores[jugador][estadistica]["parametros"]["c"]
        if not math.isnan(loc) or not math.isnan(scale) or not math.isnan(c):
            val = genlogistic.rvs(c, loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "pearson3":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        skew = distribucionesJugadores[jugador][estadistica]["parametros"]["skew"]
        if not math.isnan(loc) or not math.isnan(scale) or not math.isnan(skew):
            val = pearson3.rvs(skew,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "laplace":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        if not math.isnan(loc) or not math.isnan(scale):
            val = laplace.rvs(loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "powernorm":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        c = distribucionesJugadores[jugador][estadistica]["parametros"]["c"]
        if not math.isnan(loc) or not math.isnan(scale) or not math.isnan(c):
            val = powernorm.rvs(c, loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "exponnorm":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        if not math.isnan(loc) or not math.isnan(scale):
            val = exponnorm.rvs(loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "norminvgauss":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        a = distribucionesJugadores[jugador][estadistica]["parametros"]["a"]
        b = distribucionesJugadores[jugador][estadistica]["parametros"]["b"]
        if not math.isnan(loc) or not math.isnan(scale) or not math.isnan(a) or not math.isnan(b):
            val = norminvgauss.rvs(a,b,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "johnsonsu":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        a = distribucionesJugadores[jugador][estadistica]["parametros"]["a"]
        b = distribucionesJugadores[jugador][estadistica]["parametros"]["b"]
        if not math.isnan(loc) or not math.isnan(scale) or not math.isnan(a) or not math.isnan(b):
            val = johnsonsu.rvs(a,b,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "cauchy":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        if not math.isnan(loc) or not math.isnan(scale):
            val = cauchy.rvs(loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "tukeylambda":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        lam = distribucionesJugadores[jugador][estadistica]["parametros"]["lam"]
        if not math.isnan(loc) or not math.isnan(scale) or not math.isnan(lam):
            val = tukeylambda.rvs(lam,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "genhyperbolic":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        p = distribucionesJugadores[jugador][estadistica]["parametros"]["p"]
        a = distribucionesJugadores[jugador][estadistica]["parametros"]["a"]
        b = distribucionesJugadores[jugador][estadistica]["parametros"]["b"]
        if not math.isnan(loc) or not math.isnan(scale) or not math.isnan(p) or not math.isnan(a) or not math.isnan(b):
            val = genhyperbolic.rvs(p,a,b,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "kappa4":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        h = distribucionesJugadores[jugador][estadistica]["parametros"]["h"]
        k = distribucionesJugadores[jugador][estadistica]["parametros"]["k"]
        if not math.isnan(loc) or not math.isnan(scale) or not math.isnan(h) or not math.isnan(k):
            val = kappa4.rvs(h,k,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "laplace_asymmetric":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        kappa = distribucionesJugadores[jugador][estadistica]["parametros"]["kappa"]
        if not math.isnan(loc) or not math.isnan(scale) or not math.isnan(kappa):
            val = laplace_asymmetric.rvs(kappa,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "moyal":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        if not math.isnan(loc) or not math.isnan(scale):
            val = moyal.rvs(loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "t":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        df = distribucionesJugadores[jugador][estadistica]["parametros"]["df"]
        if not math.isnan(loc) or not math.isnan(scale) or not math.isnan(df):
            val = t.rvs(df,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "gennorm":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        beta = distribucionesJugadores[jugador][estadistica]["parametros"]["beta"]
        if not math.isnan(loc) or not math.isnan(scale) or not math.isnan(beta):
            val = gennorm.rvs(beta,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "loggamma":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        c = distribucionesJugadores[jugador][estadistica]["parametros"]["c"]
        if not math.isnan(loc) or not math.isnan(scale) or not math.isnan(c):
            val = loggamma.rvs(c, loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "nct":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        df = distribucionesJugadores[jugador][estadistica]["parametros"]["df"]
        nc = distribucionesJugadores[jugador][estadistica]["parametros"]["nc"]
        if not math.isnan(loc) or not math.isnan(scale) or not math.isnan(df) or not math.isnan(nc):
            val = nct.rvs(df,nc,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "crystalball":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        beta = distribucionesJugadores[jugador][estadistica]["parametros"]["beta"]
        m = distribucionesJugadores[jugador][estadistica]["parametros"]["m"]
        if not math.isnan(loc) or not math.isnan(scale) or not math.isnan(beta) or not math.isnan(m):
            val = crystalball.rvs(beta,m,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "truncnorm":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        a = distribucionesJugadores[jugador][estadistica]["parametros"]["a"]
        b = distribucionesJugadores[jugador][estadistica]["parametros"]["b"]
        if not math.isnan(loc) or not math.isnan(scale) or not math.isnan(a) or not math.isnan(b):
            val = truncnorm.rvs(a,b,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "skewcauchy":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        a = distribucionesJugadores[jugador][estadistica]["parametros"]["a"]
        if not math.isnan(loc) or not math.isnan(scale) or not math.isnan(a):
            val = skewcauchy.rvs(a, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "weibull_min":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        c = distribucionesJugadores[jugador][estadistica]["parametros"]["p"]
        a = distribucionesJugadores[jugador][estadistica]["parametros"]["a"]
        b = distribucionesJugadores[jugador][estadistica]["parametros"]["b"]
        if not math.isnan(loc) or not math.isnan(scale) or not math.isnan(c) or not math.isnan(a) or not math.isnan(b):
            val = weibull_min.rvs(c,a,b,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "reciprocal":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        a = distribucionesJugadores[jugador][estadistica]["parametros"]["a"]
        b = distribucionesJugadores[jugador][estadistica]["parametros"]["b"]
        if not math.isnan(loc) or not math.isnan(scale) or not math.isnan(b) or not math.isnan(a):
            val = reciprocal.rvs(a,b,loc, scale, size=1)

    else:
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        if not math.isnan(loc) or not math.isnan(scale):
            val = norm.rvs(loc, scale, size=1)

    return val


def aplicaDistribucionEquipo(equipo, estadistica, tiempo=0 ):
    global distribucionesEquipos

    if distribucionesEquipos[equipo][estadistica]["nombre"] == "norm":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        val = norm.rvs(loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "gumbel_r":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        val = gumbel_r.rvs(loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "gumbel_l":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        val = gumbel_l.rvs(loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "logistic":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        val = logistic.rvs(loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "dgamma":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        a = distribucionesEquipos[equipo][estadistica]["parametros"]["a"]
        val = dgamma.rvs(a, loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "hypsecant":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        val = hypsecant.rvs(loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "dweybull":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        c = distribucionesEquipos[equipo][estadistica]["parametros"]["c"]
        val = weibull_max.rvs(c, loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "genextreme":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        c = distribucionesEquipos[equipo][estadistica]["parametros"]["c"]
        val = genextreme.rvs(c, loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "skewnorm":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        a = distribucionesEquipos[equipo][estadistica]["parametros"]["a"]
        val = skewnorm.rvs(a, loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "genlogistic":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        c = distribucionesEquipos[equipo][estadistica]["parametros"]["c"]
        val = genlogistic.rvs(c, loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "pearson3":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        skew = distribucionesEquipos[equipo][estadistica]["parametros"]["skew"]
        val = pearson3.rvs(skew, loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "laplace":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        val = laplace.rvs(loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "powernorm":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        c = distribucionesEquipos[equipo][estadistica]["parametros"]["c"]
        val = powernorm.rvs(c, loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "exponnorm":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        val = exponnorm.rvs(loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "norminvgauss":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        a = distribucionesEquipos[equipo][estadistica]["parametros"]["a"]
        b = distribucionesEquipos[equipo][estadistica]["parametros"]["b"]
        val = norminvgauss.rvs(a, b, loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "johnsonsu":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        a = distribucionesEquipos[equipo][estadistica]["parametros"]["a"]
        b = distribucionesEquipos[equipo][estadistica]["parametros"]["b"]
        val = johnsonsu.rvs(a, b, loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "cauchy":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        val = cauchy.rvs(loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "tukeylambda":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        lam = distribucionesEquipos[equipo][estadistica]["parametros"]["lam"]
        val = tukeylambda.rvs(lam, loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "genhyperbolic":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        p = distribucionesEquipos[equipo][estadistica]["parametros"]["p"]
        a = distribucionesEquipos[equipo][estadistica]["parametros"]["a"]
        b = distribucionesEquipos[equipo][estadistica]["parametros"]["b"]
        val = genhyperbolic.rvs(p, a, b, loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "kappa4":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        h = distribucionesEquipos[equipo][estadistica]["parametros"]["h"]
        k = distribucionesEquipos[equipo][estadistica]["parametros"]["k"]
        val = kappa4.rvs(h, k, loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "laplace_asymmetric":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        kappa = distribucionesEquipos[equipo][estadistica]["parametros"]["kappa"]
        val = laplace_asymmetric.rvs(kappa, loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "moyal":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        val = moyal.rvs(loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "t":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        df = distribucionesEquipos[equipo][estadistica]["parametros"]["df"]
        val = t.rvs(df, loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "gennorm":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        beta = distribucionesEquipos[equipo][estadistica]["parametros"]["beta"]
        val = gennorm.rvs(beta, loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "loggamma":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        c = distribucionesEquipos[equipo][estadistica]["parametros"]["c"]
        val = loggamma.rvs(c, loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "nct":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        df = distribucionesEquipos[equipo][estadistica]["parametros"]["df"]
        nc = distribucionesEquipos[equipo][estadistica]["parametros"]["nc"]
        val = nct.rvs(df, nc, loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "crystalball":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        beta = distribucionesEquipos[equipo][estadistica]["parametros"]["beta"]
        m = distribucionesEquipos[equipo][estadistica]["parametros"]["m"]
        val = crystalball.rvs(beta, m, loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "truncnorm":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        a = distribucionesEquipos[equipo][estadistica]["parametros"]["a"]
        b = distribucionesEquipos[equipo][estadistica]["parametros"]["b"]
        val = truncnorm.rvs(a, b, loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "skewcauchy":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        a = distribucionesEquipos[equipo][estadistica]["parametros"]["a"]
        val = skewcauchy.rvs(a,loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "weibull_min":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        c = distribucionesEquipos[equipo][estadistica]["parametros"]["p"]
        a = distribucionesEquipos[equipo][estadistica]["parametros"]["a"]
        b = distribucionesEquipos[equipo][estadistica]["parametros"]["b"]
        val = weibull_min.rvs(c, a, b, loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "reciprocal":
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        a = distribucionesEquipos[equipo][estadistica]["parametros"]["a"]
        b = distribucionesEquipos[equipo][estadistica]["parametros"]["b"]
        val = reciprocal.rvs(a, b, loc, scale, size=1)

    elif distribucionesEquipos[equipo][estadistica]["nombre"] == "triangular":
        min = distribucionesEquipos[equipo][estadistica]["min"]
        max = tiempo
        media = distribucionesEquipos[equipo][estadistica]["media"]
        if max < media:
            media = (max + min) / 2
        val = np.random.triangular(min, media, max, 1)

    else:
        loc = distribucionesEquipos[equipo][estadistica]["parametros"]["loc"]
        scale = distribucionesEquipos[equipo][estadistica]["parametros"]["scale"]
        val = norm.rvs(loc, scale, size=1)
    
    return val


def inicializarEquipos(nombreLocal, nombreVisitante):
    global estadisticasEquipos
    infile = open(".\Ficheros\Jugadores", "rb")
    jugadores = pickle.load(infile)
    infile.close()
    estadisticasEquipos[nombreLocal] = { "TirosAnotados": 0, "Tiros": 0, "PCT_TirosAnotados": 0.0, "TriplesAnotados": 0, "Triples": 0,
                                         "PCT_TriplesAnotados": 0.0, "Rebotes": 0,"Asistencias": 0, "Robos": 0, "Faltas": 0, "Puntos":0, "Jugadores": [] }
    estadisticasEquipos[nombreVisitante] = { "TirosAnotados": 0, "Tiros": 0, "PCT_TirosAnotados": 0.0, "TriplesAnotados": 0, "Triples": 0,
                                         "PCT_TriplesAnotados": 0.0, "Rebotes": 0,"Asistencias": 0, "Robos": 0, "Faltas": 0, "Puntos":0, "Jugadores": [] }
    for jugador in jugadores:
        if jugadores[jugador]["Equipo"] == nombreLocal:
            estadisticasEquipos[nombreLocal]["Jugadores"].append(jugador)
        elif jugadores[jugador]["Equipo"] == nombreVisitante:
            estadisticasEquipos[nombreVisitante]["Jugadores"].append(jugador)


def inicializarJugadores(nombreLocal, nombreVisitante):
    global estadisticasJugadores

    infile = open(".\Ficheros\Jugadores", "rb")
    jugadores = pickle.load(infile)
    infile.close()
    estadisticasJugadores[nombreLocal] = {}
    estadisticasJugadores[nombreVisitante] = {}
    for jugador in jugadores:
        if jugadores[jugador]["Equipo"] == nombreLocal:
            estadisticasJugadores[nombreLocal][jugador] = \
                {"Estadisticas" : jugadores[jugador]["Estadisticas"],
                 "EstadisticasPartido" :
                     { "TirosAnotados": 0, "Tiros": 0, "PCT_TirosAnotados": 0.0, "TriplesAnotados": 0, "Triples": 0,
                                         "PCT_TriplesAnotados": 0.0, "Rebotes": 0,"Asistencias": 0, "Robos": 0, "Puntos":0}
                }
        elif jugadores[jugador]["Equipo"] == nombreVisitante:
            estadisticasJugadores[nombreVisitante][jugador] = \
                {"Estadisticas" : jugadores[jugador]["Estadisticas"],
                 "EstadisticasPartido" :
                     { "TirosAnotados": 0, "Tiros": 0, "PCT_TirosAnotados": 0.0, "TriplesAnotados": 0, "Triples": 0,
                                         "PCT_TriplesAnotados": 0.0, "Rebotes": 0,"Asistencias": 0, "Robos": 0, "Puntos":0}
                }