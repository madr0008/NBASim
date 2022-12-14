# Librerias
from dependencias import TratamientoDatos
from scipy.stats import *
import random

distribucionesEquipos = {}
distribucionesJugadores = {}


estadisticasJugadores = {"Equipo" :
                             {"Nombre":
                                {"Estadisticas" :
                                    { },
                                 "EstadisticasPartido" :
                                     { "Puntos": 0, "Asistencias": 0, "Rebotes": 0, "Robos": 0, "Tiros Anotados": 0, "Tiros": 0, "Triples Anotados": 0, "Triples": 0 }
                                 }}}

estadisticasEquipos = {}

equipoOrden = []

def simularPartido(nombreEquipo, nombreEquipo2):
    global distribucionesEquipos; global distribucionesJugadores; global equipoOrden

    distribucionesEquipos[nombreEquipo[1]] = TratamientoDatos.ajustarDatos(nombreEquipo[1])
    distribucionesEquipos[nombreEquipo2[1]] = TratamientoDatos.ajustarDatos(nombreEquipo2[1])
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
            equipoOrden = [nombreEquipo[1],nombreEquipo2[2]]
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
                if faltaRealiza and tiempoUsado > 10:
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
    valor = aplicaDistribucionEquipo(equipo, "Robo")
    resultado = random.random()
    if resultado < valor:
        #decidir el jugador que suma la estadistica
        return True
    return False


def falta(equipo):
    valor = aplicaDistribucionEquipo(equipo, "Falta")
    resultado = random.random()
    if resultado < valor:
        #decidir el jugador que suma la estadistica
        return True
    return False


def asistencia(equipo):
    # Decidir quien hace la asistencia, se genera un valor para cada jugador el mas alto asiste
    maximo = 0
    elegido = ""
    elegidoTiro = ""
    for jugador in equipo:
        valor = aplicaDistribucionJugador(jugador,"Asistencia")
        if valor > maximo:
            maximo = valor
            elegido = jugador
    resultado = random.random()

    # Se realiza la asistencia
    if resultado < maximo:
        # Decidir el jugador que realizara el tiro
        maximo = 0
        for jugador in equipo:
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
    if tiempo <= 2:
        return -1

    # sino devolvemos la normal con maximo el tiempo restante
    elif tiempo >= 24:
        return 1


def tiro(jugador, jugadorAsistencia, equipo):
    global estadisticasJugadores
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
        estadisticasJugadores[equipo][jugadorAsiste]["EstadisticasPartido"]["Asistencia"] += 1
    estadisticasJugadores[equipo][jugador]["EstadisticasPartido"]["TirosAnotados"] += 1
    estadisticasJugadores[equipo][jugador]["EstadisticasPartido"]["Puntos"] += tiro
    if tiro == 3:
        estadisticasJugadores[equipo][jugador]["EstadisticasPartido"]["TriplesAnotado"] += 1

    return True


def rebote(equipoPosesion, equipoDefiende):
    # Simular rebote
    valor = aplicaDistribucionEquipo(equipoPosesion,"Rebote")
    valor2 = aplicaDistribucionEquipo(equipoDefiende,"Rebote")
    if valor2 < valor:
        # decidir el jugador que suma la estadistica
        return True

    # decidir el jugador que suma la estadistica
    return False


def finCuarto():
    # procesar datos cuarto
    print("Fin cuarto")


def finPartido():
    # Recopilar datos finales
    print("Final partido")


def aplicaDistribucionJugador(jugador, estadistica):
    global distribucionesJugadores

    if distribucionesJugadores[jugador]["nombre"] == "norm":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        val = norm.rvs(loc, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == "gumbel_r":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        val = gumbel_r.rvs(loc, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == "gumbel_l":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        val = gumbel_l.rvs(loc, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == "logistic":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        val = logistic.rvs(loc, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == "dgamma":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        a = distribucionesJugadores[jugador][estadistica][1]["a"]
        val = dgamma.rvs(a,loc, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == 'hypsecant':
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        val = hypsecant.rvs(loc, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == "dweybull":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        c = distribucionesJugadores[jugador][estadistica][1]["c"]
        val = weibull_max.rvs(c, loc, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == "genextreme":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        c = distribucionesJugadores[jugador][estadistica][1]["c"]
        val = genextreme.rvs(c,loc, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == "skewnorm":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        a = distribucionesJugadores[jugador][estadistica][1]["a"]
        val = skewnorm.rvs(a,loc, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == "genlogistic":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        c = distribucionesJugadores[jugador][estadistica][1]["c"]
        val = genlogistic.rvs(c, loc, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == "pearson3":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        skew = distribucionesJugadores[jugador][estadistica][1]["skew"]
        val = pearson3.rvs(skew,loc, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == "laplace":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        val = laplace.rvs(loc, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == "powernorm":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        c = distribucionesJugadores[jugador][estadistica][1]["c"]
        val = powernorm.rvs(c, loc, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == "exponnorm":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        val = exponnorm.rvs(loc, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == "norminvgauss":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        a = distribucionesJugadores[jugador][estadistica][1]["a"]
        b = distribucionesJugadores[jugador][estadistica][1]["b"]
        val = norminvgauss.rvs(a,b,loc, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == "johnsonsu":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        a = distribucionesJugadores[jugador][estadistica][1]["a"]
        b = distribucionesJugadores[jugador][estadistica][1]["b"]
        val = johnsonsu.rvs(a,b,loc, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == "cauchy":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        val = cauchy.rvs(loc, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == "tukeylambda":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        lam = distribucionesJugadores[jugador][estadistica][1]["lam"]
        val = tukeylambda.rvs(lam,loc, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == "genhyperbolic":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        p = distribucionesJugadores[jugador][estadistica][1]["p"]
        a = distribucionesJugadores[jugador][estadistica][1]["a"]
        b = distribucionesJugadores[jugador][estadistica][1]["b"]
        val = genhyperbolic.rvs(p,a,b,loc, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == "kappa4":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        h = distribucionesJugadores[jugador][estadistica][1]["h"]
        k = distribucionesJugadores[jugador][estadistica][1]["k"]
        val = kappa4.rvs(h,k,loc, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == "laplace_asymmetric":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        kappa = distribucionesJugadores[jugador][estadistica][1]["kappa"]
        val = laplace_asymmetric.rvs(kappa,loc, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == "moyal":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        val = moyal.rvs(loc, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == "t":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        df = distribucionesJugadores[jugador][estadistica][1]["df"]
        val = t.rvs(df,loc, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == "gennorm":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        beta = distribucionesJugadores[jugador][estadistica][1]["beta"]
        val = gennorm.rvs(beta,loc, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == "loggamma":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        c = distribucionesJugadores[jugador][estadistica][1]["c"]
        val = loggamma.rvs(c, loc, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == "nct":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        df = distribucionesJugadores[jugador][estadistica][1]["df"]
        nc = distribucionesJugadores[jugador][estadistica][1]["nc"]
        val = nct.rvs(df,nc,loc, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == "crystalball":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        beta = distribucionesJugadores[jugador][estadistica][1]["beta"]
        m = distribucionesJugadores[jugador][estadistica][1]["m"]
        val = crystalball.rvs(beta,m,loc, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == "truncnorm":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        a = distribucionesJugadores[jugador][estadistica][1]["a"]
        b = distribucionesJugadores[jugador][estadistica][1]["b"]
        val = truncnorm.rvs(a,b,loc, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == "skewcauchy":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        a = distribucionesJugadores[jugador][estadistica][1]["a"]
        val = skewcauchy.rvs(a, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == "truncweibull_min":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        c = distribucionesJugadores[jugador][estadistica][1]["p"]
        a = distribucionesJugadores[jugador][estadistica][1]["a"]
        b = distribucionesJugadores[jugador][estadistica][1]["b"]
        val = truncweibull_min.rvs(c,a,b,loc, scale, size=1)

    elif distribucionesJugadores[jugador]["nombre"] == "reciprocal":
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        a = distribucionesJugadores[jugador][estadistica][1]["a"]
        b = distribucionesJugadores[jugador][estadistica][1]["b"]
        val = reciprocal.rvs(a,b,loc, scale, size=1)

    else:
        loc = distribucionesJugadores[jugador][estadistica][1]["loc"]
        scale = distribucionesJugadores[jugador][estadistica][1]["scale"]
        val = norm.rvs(loc, scale, size=1)
    return val


def aplicaDistribucionEquipo(equipo, estadistica):
    global distribucionesEquipos

    if distribucionesEquipos[equipo]["nombre"] == "norm":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        val = norm.rvs(loc, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "gumbel_r":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        val = gumbel_r.rvs(loc, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "gumbel_l":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        val = gumbel_l.rvs(loc, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "logistic":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        val = logistic.rvs(loc, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "dgamma":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        a = distribucionesEquipos[equipo][estadistica][1]["a"]
        val = dgamma.rvs(a, loc, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "hypsecant":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        val = hypsecant.rvs(loc, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "dweybull":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        c = distribucionesEquipos[equipo][estadistica][1]["c"]
        val = weibull_max.rvs(c, loc, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "genextreme":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        c = distribucionesEquipos[equipo][estadistica][1]["c"]
        val = genextreme.rvs(c, loc, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "skewnorm":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        a = distribucionesEquipos[equipo][estadistica][1]["a"]
        val = skewnorm.rvs(a, loc, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "genlogistic":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        c = distribucionesEquipos[equipo][estadistica][1]["c"]
        val = genlogistic.rvs(c, loc, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "pearson3":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        skew = distribucionesEquipos[equipo][estadistica][1]["skew"]
        val = pearson3.rvs(skew, loc, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "laplace":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        val = laplace.rvs(loc, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "powernorm":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        c = distribucionesEquipos[equipo][estadistica][1]["c"]
        val = powernorm.rvs(c, loc, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "exponnorm":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        val = exponnorm.rvs(loc, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "norminvgauss":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        a = distribucionesEquipos[equipo][estadistica][1]["a"]
        b = distribucionesEquipos[equipo][estadistica][1]["b"]
        val = norminvgauss.rvs(a, b, loc, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "johnsonsu":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        a = distribucionesEquipos[equipo][estadistica][1]["a"]
        b = distribucionesEquipos[equipo][estadistica][1]["b"]
        val = johnsonsu.rvs(a, b, loc, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "cauchy":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        val = cauchy.rvs(loc, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "tukeylambda":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        lam = distribucionesEquipos[equipo][estadistica][1]["lam"]
        val = tukeylambda.rvs(lam, loc, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "genhyperbolic":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        p = distribucionesEquipos[equipo][estadistica][1]["p"]
        a = distribucionesEquipos[equipo][estadistica][1]["a"]
        b = distribucionesEquipos[equipo][estadistica][1]["b"]
        val = genhyperbolic.rvs(p, a, b, loc, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "kappa4":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        h = distribucionesEquipos[equipo][estadistica][1]["h"]
        k = distribucionesEquipos[equipo][estadistica][1]["k"]
        val = kappa4.rvs(h, k, loc, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "laplace_asymmetric":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        kappa = distribucionesEquipos[equipo][estadistica][1]["kappa"]
        val = laplace_asymmetric.rvs(kappa, loc, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "moyal":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        val = moyal.rvs(loc, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "t":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        df = distribucionesEquipos[equipo][estadistica][1]["df"]
        val = t.rvs(df, loc, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "gennorm":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        beta = distribucionesEquipos[equipo][estadistica][1]["beta"]
        val = gennorm.rvs(beta, loc, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "loggamma":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        c = distribucionesEquipos[equipo][estadistica][1]["c"]
        val = loggamma.rvs(c, loc, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "nct":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        df = distribucionesEquipos[equipo][estadistica][1]["df"]
        nc = distribucionesEquipos[equipo][estadistica][1]["nc"]
        val = nct.rvs(df, nc, loc, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "crystalball":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        beta = distribucionesEquipos[equipo][estadistica][1]["beta"]
        m = distribucionesEquipos[equipo][estadistica][1]["m"]
        val = crystalball.rvs(beta, m, loc, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "truncnorm":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        a = distribucionesEquipos[equipo][estadistica][1]["a"]
        b = distribucionesEquipos[equipo][estadistica][1]["b"]
        val = truncnorm.rvs(a, b, loc, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "skewcauchy":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        a = distribucionesEquipos[equipo][estadistica][1]["a"]
        val = skewcauchy.rvs(a, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "truncweibull_min":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        c = distribucionesEquipos[equipo][estadistica][1]["p"]
        a = distribucionesEquipos[equipo][estadistica][1]["a"]
        b = distribucionesEquipos[equipo][estadistica][1]["b"]
        val = truncweibull_min.rvs(c, a, b, loc, scale, size=1)

    elif distribucionesEquipos[equipo]["nombre"] == "reciprocal":
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        a = distribucionesEquipos[equipo][estadistica][1]["a"]
        b = distribucionesEquipos[equipo][estadistica][1]["b"]
        val = reciprocal.rvs(a, b, loc, scale, size=1)

    else:
        loc = distribucionesEquipos[equipo][estadistica][1]["loc"]
        scale = distribucionesEquipos[equipo][estadistica][1]["scale"]
        val = norm.rvs(loc, scale, size=1)
    return val


def inicializarEquipos(nombreLocal, nombreVisitante):
    global estadisticasEquipos

    estadisticasEquipos[nombreLocal] = { "Puntos": 0, "Rebotes": 0, "Faltas": 0,  }
    estadisticasEquipos[nombreVisitante] = { "Puntos": 0, "Rebotes": 0, "Faltas": 0 }


def inicializarJugadores(nombreLocal, nombreVisitante):
    global estadisticasJugadores

    infile = open("Jugadores", "rb")
    jugadores = pickle.load(infile)
    infile.close()
    for jugador in jugadores:
        if jugadores[jugador]["Equipo"] == nombreLocal:
            estadisticasJugadores[nombreLocal][jugador] = \
                {"Estadisticas" : { jugadores[jugador]["Estadisticas"] },
                 "EstadisticasPartido" :
                     { "Puntos": 0, "Asistencias": 0, "Rebotes": 0, "Robos": 0, "Tiros Anotados": 0, "Tiros": 0, "Triples Anotados": 0, "Triples": 0 }
                }