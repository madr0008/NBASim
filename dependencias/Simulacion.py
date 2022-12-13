# Librerias
from dependencias import TratamientoDatos
from scipy.stats import *


estadisticasJugadores = {"Equipo" :
                             {"Nombre":
                                { "Equipo" : "", "ID" : 0, "Estadisticas" :
                                    { "Puntos": 0, "Asistencias": 0, "Rebotes": 0, "Robos": 0, "Tiros Anotados": 0, "Tiros": 0, "Triples Anotados": 0, "Triples": 0 } }}}

estadisticasEquipos = {"Nombre" :
                           { "Puntos": 0, "Rebotes": 0, "Faltas": 0 }}


def simularPartido(nombreEquipo, nombreEquipo2):

    distribucionesEquipos = TratamientoDatos.ajustarDatos("Equipos")
    distribucionesJugadores = TratamientoDatos.ajustarDatos("Jugadores")
    inicializarEquipos(nombreEquipo[1],nombreEquipo2[1])
    inicializarJugadores(nombreEquipo[1],nombreEquipo2[1])
    tiempo = 720
    cuarto = 1
    saque = 0
    maximo = 24
    falta = False
    tiempoUsado = 0
    while tiempo > 0 and cuarto != 4:
        if cuarto == 1 and tiempo == 720:

            # Equipo es un valor 0 o 1 según el equipo correspondiente, si necesitamos el nombre con valor 0 es equipo y con valor 1 es equipo2
            equipo = saltoInicial()
            # determinamos el equipo que saltara el siguiente cuarto
            saque = (equipo + equipo) % 2

        elif tiempo == 720:

            equipo = saque  # se selecciona el equipo al que le toca sacar de inicio
            saque = (saque + saque) % 2

        # Se reduce el tiempo de posesión del reloj
        tiempoUsado = tiempoPosesion(equipo)
        tiempo -= tiempoUsado

        # Desarrollo de la jugada
        jugador, falta = jugada(equipo)

        if falta and tiempoUsado > 10:
            maximo = 14
        elif falta and tiempoUsado < 10:
            maximo = maximo - tiempoUsado
        else:
            # Desarrollo del tiro
            acierto = tiro(jugador)

            # Si se falla el tiro se juega el rebote
            if not acierto:
                jugador = rebote(equipo)
                if jugador in equipo:
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
    # Simular salto inicial
    print("Salto Inicial")
    return "Equipo"


def jugada(equipo):
    # Simular jugada
    print("jugada")
    return "Jugador"


def tiempoPosesion(equipo):
    return 1


def tiro(jugador):
    # Simular tiro
    aplicaDistribucionJugador(jugador)
    print("tiro")
    return True


def rebote(equipo):
    # Simular rebote
    print("rebote")
    return "Rebote"


def finCuarto():
    # procesar datos cuarto
    print("Fin cuarto")


def finPartido():
    # Recopilar datos finales
    print("Final partido")


def aplicaDistribucionJugador(jugador, distribucionesJugadores):

    if distribucionesJugadores[jugador]["nombre"] == "norm":
        print("normal")
    elif distribucionesJugadores[jugador]["nombre"] == "gumbel_r":
        print("normal")
    elif distribucionesJugadores[jugador]["nombre"] == "gumbel_l":
        print("normal")
    elif distribucionesJugadores[jugador]["nombre"] == "logistic":
        print("normal")
    elif distribucionesJugadores[jugador]["nombre"] == "dgamma":
        print("normal")
    elif distribucionesJugadores[jugador]["nombre"] == "hypsecant":
        print("normal")
    elif distribucionesJugadores[jugador]["nombre"] == "dweybull":
        print("normal")
    elif distribucionesJugadores[jugador]["nombre"] == "genextreme":
        print("normal")
    elif distribucionesJugadores[jugador]["nombre"] == "skewnorm":
        print("normal")
    elif distribucionesJugadores[jugador]["nombre"] == "genlogistic":
        print("normal")
    elif distribucionesJugadores[jugador]["nombre"] == "pearson3":
        print("normal")
    elif distribucionesJugadores[jugador]["nombre"] == "laplace":
        print("normal")
    elif distribucionesJugadores[jugador]["nombre"] == "powernorm":
        print("normal")
    elif distribucionesJugadores[jugador]["nombre"] == "exponnorm":
        print("normal")
    elif distribucionesJugadores[jugador]["nombre"] == "normingvgauss":
        print("normal")
    elif distribucionesJugadores[jugador]["nombre"] == "johnsonsu":
        print("normal")
    elif distribucionesJugadores[jugador]["nombre"] == "kauchi":
        print("normal")
    elif distribucionesJugadores[jugador]["nombre"] == "tukeylambda":
        print("normal")
    elif distribucionesJugadores[jugador]["nombre"] == "genhyperbolic":
        print("normal")
    elif distribucionesJugadores[jugador]["nombre"] == "kappa4":
        print("normal")
    elif distribucionesJugadores[jugador]["nombre"] == "laplace_asymmetric":
        print("normal")
    elif distribucionesJugadores[jugador]["nombre"] == "moyal":
        print("normal")
    elif distribucionesJugadores[jugador]["nombre"] == "t":
        print("normal")
    elif distribucionesJugadores[jugador]["nombre"] == "gennorm":
        print("normal")
    elif distribucionesJugadores[jugador]["nombre"] == "loggamma":
        print("normal")
    elif distribucionesJugadores[jugador]["nombre"] == "nct":
        print("normal")
    elif distribucionesJugadores[jugador]["nombre"] == "crystalball":
        print("normal")
    elif distribucionesJugadores[jugador]["nombre"] == "truncnorm":
        print("normal")
    elif distribucionesJugadores[jugador]["nombre"] == "skewcauchy":
        print("normal")
    elif distribucionesJugadores[jugador]["nombre"] == "truncweibull_min":
        print("normal")


def aplicaDistribucionEquipo(equipo, distribucionesEquipos):

    if distribucionesEquipos[equipo] == "normal":
        print("normal")
    elif distribucionesEquipos[equipo] == "gumbel_r":
        print("normal")
    elif distribucionesEquipos[equipo] == "gumbel_l":
        print("normal")
    elif distribucionesEquipos[equipo] == "logistic":
        print("normal")
    elif distribucionesEquipos[equipo] == "dgamma":
        print("normal")
    elif distribucionesEquipos[equipo] == "hypsecant":
        print("normal")
    elif distribucionesEquipos[equipo] == "dweybull":
        print("normal")
    elif distribucionesEquipos[equipo] == "genextreme":
        print("normal")
    elif distribucionesEquipos[equipo] == "skewnorm":
        print("normal")
    elif distribucionesEquipos[equipo] == "genlogistic":
        print("normal")
    elif distribucionesEquipos[equipo] == "pearson3":
        print("normal")
    elif distribucionesEquipos[equipo] == "laplace":
        print("normal")
    elif distribucionesEquipos[equipo] == "powernorm":
        print("normal")
    elif distribucionesEquipos[equipo] == "exponnorm":
        print("normal")
    elif distribucionesEquipos[equipo] == "normingvgauss":
        print("normal")
    elif distribucionesEquipos[equipo] == "johnsonsu":
        print("normal")
    elif distribucionesEquipos[equipo] == "kauchi":
        print("normal")
    elif distribucionesEquipos[equipo] == "tukeylambda":
        print("normal")
    elif distribucionesEquipos[equipo] == "genhyperbolic":
        print("normal")
    elif distribucionesEquipos[equipo] == "kappa4":
        print("normal")
    elif distribucionesEquipos[equipo]["nombre"] == "laplace_asymmetric":
        print("normal")
    elif distribucionesEquipos[equipo]["nombre"] == "moyal":
        print("normal")
    elif distribucionesEquipos[equipo]["nombre"] == "t":
        print("normal")
    elif distribucionesEquipos[equipo]["nombre"] == "gennorm":
        print("normal")
    elif distribucionesEquipos[equipo]["nombre"] == "loggamma":
        print("normal")
    elif distribucionesEquipos[equipo]["nombre"] == "nct":
        print("normal")
    elif distribucionesEquipos[equipo]["nombre"] == "crystalball":
        print("normal")
    elif distribucionesEquipos[equipo]["nombre"] == "truncnorm":
        print("normal")
    elif distribucionesEquipos[equipo]["nombre"] == "skewcauchy":
        print("normal")
    elif distribucionesEquipos[equipo]["nombre"] == "truncweibull_min":
        print("normal")


def inicializarEquipos(nombreLocal, nombreVisitante):
    return 1


def inicializarJugadores(nombreLocal, nombreVisitante):
    return 1