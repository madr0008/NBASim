# Librerias
import math
import pickle
from dependencias import TratamientoDatos
from scipy.stats import *
import random
import numpy as np

distribucionesEquipos = {}
distribucionesJugadores = {}


estadisticasJugadores = {}
estadisticasEquipos = {}

equipoOrden = []

tiempoParaTiro = 2

def simularPartido(nombreEquipo, nombreEquipo2):
    global distribucionesEquipos; global distribucionesJugadores; global equipoOrden; global tiempoParaTiro
    print("Empieza")
    TratamientoDatos.cargaDatosGeneral()
    print("Paso 1")
    # distribucionesEquipos[nombreEquipo[1]] = TratamientoDatos.ajustarDatos(nombreEquipo[1], tiempoParaTiro, 24)
    # distribucionesEquipos[nombreEquipo2[1]] = TratamientoDatos.ajustarDatos(nombreEquipo2[1], tiempoParaTiro, 24)
    # fichero_datos = open(".\Ficheros\DistribucionesEquipos", "wb")
    # pickle.dump(distribucionesEquipos, fichero_datos)
    # fichero_datos.close()
    infile = open(".\Ficheros\DistribucionesEquipos", "rb")
    distribucionesEquipos = pickle.load(infile)
    infile.close()

    print("Paso 2")
    # distribucionesJugadores = TratamientoDatos.ajustarDatosJugadores(nombreEquipo[1], nombreEquipo2[1])
    # fichero_datos = open(".\Ficheros\DistribucionesJugadores", "wb")
    # pickle.dump(distribucionesJugadores, fichero_datos)
    # fichero_datos.close()
    infile = open(".\Ficheros\DistribucionesJugadores", "rb")
    distribucionesJugadores = pickle.load(infile)
    infile.close()

    print("Paso 3")
    inicializarEquipos(nombreEquipo[1], nombreEquipo2[1])
    inicializarJugadores(nombreEquipo[1], nombreEquipo2[1])
    tiempo = 720
    cuarto = 1
    saque = 0
    maximo = 24
    while tiempo > 0 or cuarto != 4:

        print("\n\n" + str(tiempo) + " segundos del cuarto " + str(cuarto))

        if cuarto == 1 and tiempo == 720:

            # Equipo es un valor 0 o 1 según el equipo correspondiente, si necesitamos el nombre con valor 0 es equipo y con valor 1 es equipo2
            equipo = saltoInicial()
            equipoOrden.append(nombreEquipo[1])
            equipoOrden.append(nombreEquipo2[1])
            # determinamos el equipo que saltara el siguiente cuarto
            saque = (equipo + 1) % 2
            print("Saca el equipo " + equipoOrden[equipo])

        elif tiempo == 720:

            equipo = saque  # se selecciona el equipo al que le toca sacar de inicio
            saque = (saque + saque) % 2
            print("Saca " + equipoOrden[equipo])

        # Se reduce el tiempo de posesión del reloj
        if tiempo > 24:
            tiempoUsado = tiempoPosesion(equipoOrden[equipo], maximo)
        else:
            tiempoUsado = tiempoPosesion(equipoOrden[equipo], tiempo)

        if tiempoUsado == -1:
            tiempo = -1
            print("No hay tiempo para mas!")
        else:
            tiempo -= tiempoUsado

        if tiempo >= 0:

            print("La jugada dura " + str(tiempoUsado) + " segundos")

            # Desarrollo de la jugada
            jugador, jugadorAsiste, roboRealizado, faltaRealizada = jugada(equipo)
            if roboRealizado:
                maximo = 24
                equipo = (equipo + 1) % 2
                print("Roba " + equipoOrden[equipo])
            else:
                if faltaRealizada and maximo - tiempoUsado < 14:
                    maximo = 14
                    print("Falta de " + equipoOrden[(equipo + 1) % 2] + ". Quedan " + str(maximo) + " segundos")
                elif faltaRealizada and maximo - tiempoUsado > 10:
                    maximo = maximo - tiempoUsado
                    print("Falta de " + equipoOrden[(equipo + 1) % 2] + ". Quedan " + str(maximo) + " segundos")
                else:
                    # Desarrollo del tiro
                    acierto = tiro(jugador,jugadorAsiste,equipoOrden[equipo])

                    # Si se falla el tiro se juega el rebote
                    if not acierto:
                        reboteCogido = rebote(equipoOrden[equipo], equipoOrden[(equipo + 1) % 2])
                        if reboteCogido:
                            maximo = 14
                            print("Fallo de " + jugador + ". Rebote para " + equipoOrden[equipo])
                            # juega el mismo equipo el balón
                        else:
                            maximo = 24
                            equipo = (equipo + 1) % 2
                            print("Fallo de " + jugador + ". Rebote para " + equipoOrden[equipo])
                            # empieza una nueva posesión del rival
                    else:
                        if jugador != jugadorAsiste:
                            print("Canasta de " + jugador + " con asistencia de " + jugadorAsiste)
                        else:
                            print("Canasta de " + jugador + " con una gran jugada individual")
                        print(equipoOrden[0] + " " + str(estadisticasEquipos[equipoOrden[0]]["Puntos"]) + " - " + str(estadisticasEquipos[equipoOrden[0]]["Puntos"]) + " " + equipoOrden[1])
        # Si fin de cuarto se sacan los datos del mismo
        if tiempo <= 0:
            finCuarto()
            print("Se acaba el cuarto " + str(cuarto))
            # Si fin del último cuarto se sacan los datos del partido
            if cuarto == 4:
                print("Se acaba el partido")
                finPartido()
            # Sino se empieza un nuevo cuarto
            else:
                cuarto += 1
                tiempo = 720


def saltoInicial():
    # Simular salto inicial probabilidad 50% ambos equipos
    return random.randint(0, 1)


def jugada(equipo):
    global equipoOrden
    # Simular jugada
    if robo(equipoOrden[(equipo + 1)  % 2]):
        return "","",True,False
    else:
        if falta(equipoOrden[equipo]):
            return "","",False,True
        else:
            jugador,jugadorAsiste = asistencia(equipoOrden[equipo])
    return jugador,jugadorAsiste,False,False


def robo(equipo):
    global estadisticasJugadores; global estadisticasEquipos

    valor = aplicaDistribucionEquipo(equipo, "PorcentajeRobos")[0]
    resultado = random.random()
    maximo = 0
    if resultado < valor:
        for jugador in estadisticasEquipos[equipo]["Jugadores"]:
            valor = aplicaDistribucionJugador(jugador, "Robos")[0]
            if valor > maximo:
                maximo = valor
                elegido = jugador
        estadisticasJugadores[equipo][elegido]["EstadisticasPartido"]["Robos"] += 1
        estadisticasEquipos[equipo]["Robos"] += 1
        return True
    return False


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
    for jugador in estadisticasEquipos[equipo]["Jugadores"]:
        valor = aplicaDistribucionJugador(jugador,"Asistencias")[0]
        if valor > maximo:
            maximo = valor
            elegido = jugador
    resultado = random.random()

    # Se realiza la asistencia
    if resultado < maximo:
        # Decidir el jugador que realizara el tiro
        maximo = 0
        for jugador in estadisticasEquipos[equipo]["Jugadores"]:
            if jugador != elegido:
                valor = aplicaDistribucionJugador(jugador,"ProbabilidadTiro")[0]
                if valor > maximo:
                    maximo = valor
                    elegidoTiro = jugador
    # No se realiza asistencia tira el jugador que tiene la bola
    else:
        elegidoTiro = elegido
    return elegidoTiro,elegido


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
        valor = aplicaDistribucionJugador(jugador, "PorcentajeAciertoTriples")[0]
    else:
        tiro = 2
        estadisticasJugadores[equipo][jugador]["EstadisticasPartido"]["Tiros"] += 1
        # Simular tiro
        valor = aplicaDistribucionJugador(jugador,"PorcentajeAciertos")[0]
    resultado = random.random()

    if resultado > valor:
        return False

    # Sumar estadistica al jugador
    if jugador != jugadorAsistencia:
        estadisticasJugadores[equipo][jugadorAsistencia]["EstadisticasPartido"]["Asistencias"] += 1
    estadisticasJugadores[equipo][jugador]["EstadisticasPartido"]["TirosAnotados"] += 1
    estadisticasJugadores[equipo][jugador]["EstadisticasPartido"]["Puntos"] += tiro
    estadisticasEquipos[equipo]["Puntos"] += tiro
    if tiro == 3:
        estadisticasJugadores[equipo][jugador]["EstadisticasPartido"]["TriplesAnotados"] += 1

    return True


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
        for jugador in estadisticasEquipos[equipoPosesion]["Jugadores"]:
            valor = aplicaDistribucionJugador(jugador, "Rebotes")[0]
            if valor > maximo:
                maximo = valor
                elegido = jugador
        estadisticasJugadores[equipoPosesion][elegido]["EstadisticasPartido"]["Rebotes"] += 1
        return True

    estadisticasEquipos[equipoDefiende]["Rebotes"] += 1
    maximo = 0
    for jugador in estadisticasEquipos[equipoDefiende]["Jugadores"]:
        valor = aplicaDistribucionJugador(jugador, "Rebotes")[0]
        if valor > maximo:
            maximo = valor
            elegido = jugador
    # decidir el jugador que suma la estadistica
    estadisticasJugadores[equipoDefiende][elegido]["EstadisticasPartido"]["Rebotes"] += 1
    return False


def finCuarto():
    # procesar datos cuarto
    print("Fin cuarto")


def finPartido():
    global estadisticasEquipos; global estadisticasJugadores
    # Recopilar datos finales
    for equipo in estadisticasEquipos:
        print(equipo)
        print("\t" + str(estadisticasEquipos[equipo]["Puntos"]) + " puntos")
        print("\t" + str(estadisticasEquipos[equipo]["Rebotes"]) + " rebotes")
        print("\t" + str(estadisticasEquipos[equipo]["Faltas"]) + " faltas")
        print("\t" + str(estadisticasEquipos[equipo]["Robos"]) + " robos")
    for equipo in estadisticasJugadores:
        print(equipo)
        for jugador in estadisticasJugadores[equipo]:
            print("\t" + jugador)
            print("\t" + "\t" + str(estadisticasJugadores[equipo][jugador]["EstadisticasPartido"]["Puntos"]) + " puntos")
            print("\t" + "\t" + str(estadisticasJugadores[equipo][jugador]["EstadisticasPartido"]["Robos"]) + " robos")
            print("\t" + "\t" + str(estadisticasJugadores[equipo][jugador]["EstadisticasPartido"]["Tiros"]) + " tiros")
            print("\t" + "\t" + str(estadisticasJugadores[equipo][jugador]["EstadisticasPartido"]["TirosAnotados"]) + " tiros anotados")


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

    estadisticasEquipos[nombreLocal] = { "Puntos": 0, "Rebotes": 0, "Faltas": 0, "Robos": 0, "Jugadores": [] }
    estadisticasEquipos[nombreVisitante] = { "Puntos": 0, "Rebotes": 0, "Faltas": 0, "Robos": 0, "Jugadores": [] }
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
                     { "Puntos": 0, "Asistencias": 0, "Rebotes": 0, "Robos": 0, "TirosAnotados": 0, "Tiros": 0, "TriplesAnotados": 0, "Triples": 0 }
                }
        elif jugadores[jugador]["Equipo"] == nombreVisitante:
            estadisticasJugadores[nombreVisitante][jugador] = \
                {"Estadisticas" : jugadores[jugador]["Estadisticas"],
                 "EstadisticasPartido" :
                     { "Puntos": 0, "Asistencias": 0, "Rebotes": 0, "Robos": 0, "TirosAnotados": 0, "Tiros": 0, "TriplesAnotados": 0, "Triples": 0 }
                }