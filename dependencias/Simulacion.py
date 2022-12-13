#Librerias
import Equipo
import numpy as np
import Estadistica
import TratamientoDatos
import csv

#Librerias para graficos
import matplotlib.pyplot as plt
from matplotlib import style


def simularPartido(datos, nombreEquipo, nombreEquipo2):
    TratamientoDatos.ajustarDatos(datos, nombreEquipo[0], nombreEquipo2[0])
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

    if distribucionesJugadores[jugador] == "normal":
        print("normal")
    elif distribucionesJugadores[jugador] == "normal":
        print("normal")
    elif distribucionesJugadores[jugador] == "normal":
        print("normal")
    elif distribucionesJugadores[jugador] == "normal":
        print("normal")
    elif distribucionesJugadores[jugador] == "normal":
        print("normal")
    elif distribucionesJugadores[jugador] == "normal":
        print("normal")
    elif distribucionesJugadores[jugador] == "normal":
        print("normal")
    elif distribucionesJugadores[jugador] == "normal":
        print("normal")


def aplicaDistribucionEquipo(equipo):
    global distribucionesEquipos

    if distribucionesEquipos[equipo] == "normal":
        print("normal")
    elif distribucionesEquipos[equipo] == "normal":
        print("normal")
    elif distribucionesEquipos[equipo] == "normal":
        print("normal")
    elif distribucionesEquipos[equipo] == "normal":
        print("normal")
    elif distribucionesEquipos[equipo] == "normal":
        print("normal")
    elif distribucionesEquipos[equipo] == "normal":
        print("normal")
    elif distribucionesEquipos[equipo] == "normal":
        print("normal")
    elif distribucionesEquipos[equipo] == "normal":
        print("normal")

