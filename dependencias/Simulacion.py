# Librerias
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

    TratamientoDatos.cargaDatosGeneral()
    distribucionesEquipos[nombreEquipo[1]] = TratamientoDatos.ajustarDatos(nombreEquipo[1], tiempoParaTiro, 24)
    distribucionesEquipos[nombreEquipo2[1]] = TratamientoDatos.ajustarDatos(nombreEquipo2[1], tiempoParaTiro, 24)
    distribucionesJugadores = TratamientoDatos.ajustarDatosJugadores(nombreEquipo[1],nombreEquipo2[1])
    inicializarEquipos(nombreEquipo[1], nombreEquipo2[1])
    inicializarJugadores(nombreEquipo[1], nombreEquipo2[1])
    tiempo = 720
    cuarto = 1
    saque = 0
    maximo = 24
    while tiempo > 0 and cuarto != 4:

        if cuarto == 1 and tiempo == 720:

            # Equipo es un valor 0 o 1 según el equipo correspondiente, si necesitamos el nombre con valor 0 es equipo y con valor 1 es equipo2
            equipo = saltoInicial()
            equipoOrden.append(nombreEquipo[1])
            equipoOrden.append(nombreEquipo2[1])
            # determinamos el equipo que saltara el siguiente cuarto
            saque = (equipo + equipo) % 2

        elif tiempo == 720:

            equipo = saque  # se selecciona el equipo al que le toca sacar de inicio
            saque = (saque + saque) % 2

        # Se reduce el tiempo de posesión del reloj
        if tiempo > 24:
            tiempoUsado = tiempoPosesion(equipoOrden[equipo], maximo)
        else:
            tiempoUsado = tiempoPosesion(equipoOrden[equipo], tiempo)

        if tiempoUsado == -1:
            tiempo = -1
        else:
            tiempo -= tiempoUsado

        if tiempo >= 0:
            # Desarrollo de la jugada
            jugador, jugadorAsiste, roboRealizado, faltaRealizada = jugada(equipo)
            if roboRealizado:
                maximo = 24
                equipo = (equipo + equipo) % 2
            else:
                if faltaRealizada and tiempoUsado > 10:
                    maximo = 14
                elif faltaRealizada and tiempoUsado < 10:
                    maximo = maximo - tiempoUsado
                else:
                    # Desarrollo del tiro
                    acierto = tiro(jugador,jugadorAsiste,equipoOrden[equipo])

                    # Si se falla el tiro se juega el rebote
                    if not acierto:
                        reboteCogido = rebote(equipoOrden[equipo], equipoOrden[(equipo + equipo) % 2])
                        if reboteCogido:
                            maximo = 14
                            # juega el mismo equipo el balón
                        else:
                            maximo = 24
                            equipo = (equipo + equipo) % 2
                            # empieza una nueva posesión del rival

        # Si fin de cuarto se sacan los datos del mismo
        if tiempo <= 0:
            finCuarto()
            # Si fin del último cuarto se sacan los datos del partido
            if cuarto == 4:
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
    if robo(equipoOrden[(equipo + equipo)  % 2]):
        return "","",True,False
    else:
        if falta(equipoOrden[equipo]):
            return "","",False,True
        else:
            jugador,jugadorAsiste = asistencia(equipo)
    return jugador,jugadorAsiste,False,False


def robo(equipo):
    global estadisticasJugadores; global estadisticasEquipos

    valor = aplicaDistribucionEquipo(equipo, "Robo")
    resultado = random.random()
    if resultado < valor:
        for jugador in estadisticasEquipos[equipo]["Jugadores"]:
            valor = aplicaDistribucionJugador(jugador, "Robos")
            if valor > maximo:
                maximo = valor
                elegido = jugador
        estadisticasJugadores[equipo][elegido]["EstadisticasPartido"]["Robos"] += 1
        return True
    return False


def falta(equipo):
    global estadisticasEquipos

    valor = aplicaDistribucionEquipo(equipo, "Falta")
    resultado = random.random()
    if resultado < valor:
        estadisticasEquipos[equipo]["Estadisticas"]["Faltas"] += 1
        return True
    return False


def asistencia(equipo):
    global estadisticasEquipos
    # Decidir quien hace la asistencia, se genera un valor para cada jugador el mas alto asiste
    maximo = 0
    elegido = ""
    elegidoTiro = ""
    for jugador in estadisticasEquipos[equipo]["Jugadores"]:
        valor = aplicaDistribucionJugador(jugador,"Asistencia")
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
                valor = aplicaDistribucionJugador(jugador,"ProbabilidadTiro")
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
    elif tiempo >= 24:
        return round(aplicaDistribucionEquipo(equipo, "TiempoPosesion"))


def tiro(jugador, jugadorAsistencia, equipo):
    global estadisticasJugadores; global estadisticasEquipos

    # Decidir si el tiro es de dos o de tres
    valor = aplicaDistribucionJugador(jugador,"PorcentajeTriples")
    resultado = random.random()
    if valor > resultado:
        tiro = 3
        estadisticasJugadores[equipo][jugador]["EstadisticasPartido"]["Tiros"] += 1
        estadisticasJugadores[equipo][jugador]["EstadisticasPartido"]["Triples"] += 1
        valor = aplicaDistribucionJugador(jugador, "PorcentajeAciertoTriples")
    else:
        tiro = 2
        estadisticasJugadores[equipo][jugador]["EstadisticasPartido"]["Tiros"] += 1
        # Simular tiro
        valor = aplicaDistribucionJugador(jugador,"PorcentajeAciertos")
    resultado = random.random()

    if resultado > valor:
        return False

    # Sumar estadistica al jugador
    if jugador != jugadorAsistencia:
        estadisticasJugadores[equipo][jugadorAsistencia]["EstadisticasPartido"]["Asistencia"] += 1
    estadisticasJugadores[equipo][jugador]["EstadisticasPartido"]["TirosAnotados"] += 1
    estadisticasJugadores[equipo][jugador]["EstadisticasPartido"]["Puntos"] += tiro
    estadisticasEquipos[equipo]["Estadisticas"]["Puntos"] += tiro
    if tiro == 3:
        estadisticasJugadores[equipo][jugador]["EstadisticasPartido"]["TriplesAnotado"] += 1

    return True


def rebote(equipoPosesion, equipoDefiende):
    global estadisticasEquipos; global estadisticasJugadores
    # Simular rebote
    valor = aplicaDistribucionEquipo(equipoPosesion,"Rebote")
    valor2 = aplicaDistribucionEquipo(equipoDefiende,"Rebote")
    if valor2 < valor:
        # decidir el jugador que suma la estadistica
        estadisticasEquipos[equipoPosesion]["Estadisticas"]["Rebotes"] += 1
        for jugador in estadisticasEquipos[equipoPosesion]["Jugadores"]:
            valor = aplicaDistribucionJugador(jugador, "Robos")
            if valor > maximo:
                maximo = valor
                elegido = jugador
        estadisticasJugadores[equipoPosesion][elegido]["Estadisticas"]["Rebotes"] += 1
        return True

    estadisticasEquipos[equipoDefiende]["Estadisticas"]["Rebotes"] += 1
    for jugador in estadisticasEquipos[equipoDefiende]["Jugadores"]:
        valor = aplicaDistribucionJugador(jugador, "Robos")
        if valor > maximo:
            maximo = valor
            elegido = jugador
    # decidir el jugador que suma la estadistica
    estadisticasJugadores[equipoDefiende][elegido]["Estadisticas"]["Rebotes"] += 1
    return False


def finCuarto():
    # procesar datos cuarto
    print("Fin cuarto")


def finPartido():
    # Recopilar datos finales
    print("Final partido")


def aplicaDistribucionJugador(jugador, estadistica):
    global distribucionesJugadores

    if distribucionesJugadores[jugador][estadistica]["nombre"] == "norm":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        val = norm.rvs(loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "gumbel_r":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        val = gumbel_r.rvs(loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "gumbel_l":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        val = gumbel_l.rvs(loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "logistic":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        val = logistic.rvs(loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "dgamma":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        a = distribucionesJugadores[jugador][estadistica]["parametros"]["a"]
        val = dgamma.rvs(a,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == 'hypsecant':
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        val = hypsecant.rvs(loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "dweybull":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        c = distribucionesJugadores[jugador][estadistica]["parametros"]["c"]
        val = weibull_max.rvs(c, loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "genextreme":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        c = distribucionesJugadores[jugador][estadistica]["parametros"]["c"]
        val = genextreme.rvs(c,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "skewnorm":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        a = distribucionesJugadores[jugador][estadistica]["parametros"]["a"]
        val = skewnorm.rvs(a,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "genlogistic":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        c = distribucionesJugadores[jugador][estadistica]["parametros"]["c"]
        val = genlogistic.rvs(c, loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "pearson3":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        skew = distribucionesJugadores[jugador][estadistica]["parametros"]["skew"]
        val = pearson3.rvs(skew,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "laplace":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        val = laplace.rvs(loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "powernorm":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        c = distribucionesJugadores[jugador][estadistica]["parametros"]["c"]
        val = powernorm.rvs(c, loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "exponnorm":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        val = exponnorm.rvs(loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "norminvgauss":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        a = distribucionesJugadores[jugador][estadistica]["parametros"]["a"]
        b = distribucionesJugadores[jugador][estadistica]["parametros"]["b"]
        val = norminvgauss.rvs(a,b,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "johnsonsu":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        a = distribucionesJugadores[jugador][estadistica]["parametros"]["a"]
        b = distribucionesJugadores[jugador][estadistica]["parametros"]["b"]
        val = johnsonsu.rvs(a,b,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "cauchy":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        val = cauchy.rvs(loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "tukeylambda":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        lam = distribucionesJugadores[jugador][estadistica]["parametros"]["lam"]
        val = tukeylambda.rvs(lam,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "genhyperbolic":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        p = distribucionesJugadores[jugador][estadistica]["parametros"]["p"]
        a = distribucionesJugadores[jugador][estadistica]["parametros"]["a"]
        b = distribucionesJugadores[jugador][estadistica]["parametros"]["b"]
        val = genhyperbolic.rvs(p,a,b,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "kappa4":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        h = distribucionesJugadores[jugador][estadistica]["parametros"]["h"]
        k = distribucionesJugadores[jugador][estadistica]["parametros"]["k"]
        val = kappa4.rvs(h,k,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "laplace_asymmetric":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        kappa = distribucionesJugadores[jugador][estadistica]["parametros"]["kappa"]
        val = laplace_asymmetric.rvs(kappa,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "moyal":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        val = moyal.rvs(loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "t":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        df = distribucionesJugadores[jugador][estadistica]["parametros"]["df"]
        val = t.rvs(df,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "gennorm":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        beta = distribucionesJugadores[jugador][estadistica]["parametros"]["beta"]
        val = gennorm.rvs(beta,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "loggamma":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        c = distribucionesJugadores[jugador][estadistica]["parametros"]["c"]
        val = loggamma.rvs(c, loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "nct":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        df = distribucionesJugadores[jugador][estadistica]["parametros"]["df"]
        nc = distribucionesJugadores[jugador][estadistica]["parametros"]["nc"]
        val = nct.rvs(df,nc,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "crystalball":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        beta = distribucionesJugadores[jugador][estadistica]["parametros"]["beta"]
        m = distribucionesJugadores[jugador][estadistica]["parametros"]["m"]
        val = crystalball.rvs(beta,m,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "truncnorm":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        a = distribucionesJugadores[jugador][estadistica]["parametros"]["a"]
        b = distribucionesJugadores[jugador][estadistica]["parametros"]["b"]
        val = truncnorm.rvs(a,b,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "skewcauchy":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        a = distribucionesJugadores[jugador][estadistica]["parametros"]["a"]
        val = skewcauchy.rvs(a, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "weibull_min":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        c = distribucionesJugadores[jugador][estadistica]["parametros"]["p"]
        a = distribucionesJugadores[jugador][estadistica]["parametros"]["a"]
        b = distribucionesJugadores[jugador][estadistica]["parametros"]["b"]
        val = weibull_min.rvs(c,a,b,loc, scale, size=1)

    elif distribucionesJugadores[jugador][estadistica]["nombre"] == "reciprocal":
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        a = distribucionesJugadores[jugador][estadistica]["parametros"]["a"]
        b = distribucionesJugadores[jugador][estadistica]["parametros"]["b"]
        val = reciprocal.rvs(a,b,loc, scale, size=1)

    else:
        loc = distribucionesJugadores[jugador][estadistica]["parametros"]["loc"]
        scale = distribucionesJugadores[jugador][estadistica]["parametros"]["scale"]
        val = norm.rvs(loc, scale, size=1)

    return val


def aplicaDistribucionEquipo(equipo, estadistica):
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
        val = skewcauchy.rvs(a, scale, size=1)

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
        max = distribucionesEquipos[equipo][estadistica]["max"]
        media = distribucionesEquipos[equipo][estadistica]["media"]
        print(min)
        print(max)
        print(media)
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

    estadisticasEquipos[nombreLocal] = { "Puntos": 0, "Rebotes": 0, "Faltas": 0, "Jugadores": [] }
    estadisticasEquipos[nombreVisitante] = { "Puntos": 0, "Rebotes": 0, "Faltas": 0, "Jugadores": [] }
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
    for jugador in jugadores:
        if jugadores[jugador]["Equipo"] == nombreLocal:
            estadisticasJugadores[nombreLocal][jugador] = \
                {"Estadisticas" : { jugadores[jugador]["Estadisticas"] },
                 "EstadisticasPartido" :
                     { "Puntos": 0, "Asistencias": 0, "Rebotes": 0, "Robos": 0, "Tiros Anotados": 0, "Tiros": 0, "Triples Anotados": 0, "Triples": 0 }
                }