#Librerias
import numpy as np
from dependencias import Estadistica
from dependencias import TratamientoDatos


def simularPartido(nombreEquipo, nombreEquipo2):
    TratamientoDatos.ajustarDatos(nombreEquipo[1])
    TratamientoDatos.ajustarDatos(nombreEquipo2[1])

    tiempo = 720
    cuarto = 1
    saque = 0
    while tiempo > 0 and cuarto != 4:
        if cuarto == 1 and tiempo == 720:
            #Equipo es un valor 0 o 1 según el equipo correspondiente, si necesitamos el nombre con valor 0 es equipo y con valor 1 es equipo2
            equipo = saltoInicial()
            # determinamos el equipo que saltara el siguiente cuarto
            if equipo:
                saque = 1
            else:
                saque = 0
        elif tiempo == 720:
            equipo = saque #se selecciona el equipo al que le toca sacar de inicio
        jugador = jugada(equipo)
        acierto = tiro(jugador)
        if not acierto:
            jugador = rebote(equipo)
        tiempo -= 10
        if tiempo <= 0:
            finCuarto()
            if cuarto == 4:
                finPartido()
            else:
                cuarto += 1
                tiempo = 720
                saque = "" #seleccionamos el equipo que sacara el proximo cuarto


def saltoInicial():
    # Simular salto inicial
    print("Salto Inicial")
    return "Equipo"


def jugada(equipo):
    # Simular jugada
    print("jugada")
    return "Jugador"


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
    #procesar datos cuarto
    print("Fin cuarto")


def finPartido():
    # Recopilar datos finales
    print("Final partido")


def elegirDistribucion(datos):
    resultados = Estadistica.comparar_distribuciones(
        x=np.array(datos),  # Se pasa la lista como un array NumPy
        familia='realall',
        # Se escribe la familia de distribuciones que queremos tener en cuenta: {'realall', 'realline', 'realplus', 'real0to1', 'discreta'}
        ordenar='bic',
        verbose=False
    )
    return resultados.values[0], resultados.values[0][5]


def aplicaDistribucionJugador(jugador):
    global distribucionesJugadores

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


def aplicaDistribucionEquipo(equipo):
    global distribucionesEquipos

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

