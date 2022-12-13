import os.path

from basketball_reference_scraper.seasons import get_schedule
from basketball_reference_scraper.box_scores import get_box_scores
from basketball_reference_scraper.teams import get_roster
import pickle
import csv
import Estadistica
import numpy as np
import simpy

equipos = {
    "Atlanta Hawks": "ATL",
    "Boston Celtics": "BOS",
    "Brooklyn Nets": "BRK",
    "Charlotte Hornets": "CHO",
    "Chicago Bulls": "CHI",
    "Cleveland Cavaliers": "CLE",
    "Los Angeles Clippers": "LAC",
    "Dallas Mavericks": "DAL",
    "Denver Nuggets": "DEN",
    "Detroit Pistons": "DET",
    "Golden State Warriors": "GSW",
    "Houston Rockets": "HOU",
    "Indiana Pacers": "IND",
    "Los Angeles Lakers": "LAL",
    "Memphis Grizzlies": "MEM",
    "Miami Heat": "MIA",
    "Milwaukee Bucks": "MIL",
    "Minnesota Timberwolves": "MIN",
    "New York Knicks": "NYK",
    "New Orleans Pelicans": "NOP",
    "Oklahoma City Thunder": "OKC",
    "Orlando Magic": "ORL",
    "Philadelphia 76ers": "PHI",
    "Phoenix Suns": "PHO",
    "Portland Trail Blazers": "POR",
    "Sacramento Kings": "SAC",
    "San Antonio Spurs": "SAS",
    "Toronto Raptors": "TOR",
    "Utah Jazz": "UTA",
    "Washington Wizzards": "WAS"
}


def estadisticasPartidosEquipo(equipo, temporada):
    temporadaEquipo = {}
    if not os.path.isfile("datos.txt"):
        partidos = get_schedule(temporada, False)
        estadisticasEquipo = []
        estadisticasJugadores = {}
        rosterEquipo = get_roster(equipo[0],temporada)
        for jugador in rosterEquipo.values:
            estadisticasJugadores[jugador[1]] = []
        for partido in partidos.values:
            # Partidos donde el equipo es local
            if partido[1] == equipo[1]:
                # Obtenemos los datos del partido
                estadisticas = get_box_scores(str(partido[0])[:-9], equipo[0], equipos[partido[3]])

                # Diccionario de jugadores
                for jugador in estadisticas[equipo[0]].values:
                    if estadisticasJugadores.keys().__contains__(jugador[0]):
                        estadisticasJugadores[jugador[0]].append(jugador[1:])
                    elif jugador[0] == "Team Totals":
                        estadisticasEquipo.append(jugador[1:])

            # Partidos donde el equipo es visitante
            elif partido[3] == equipo[1]:
                estadisticas = get_box_scores(str(partido[0])[:-9], equipos[partido[1]], equipo[0])
                for jugador in estadisticas[equipo[0]].values:
                    if estadisticasJugadores.keys().__contains__(jugador[0]):
                        estadisticasJugadores[jugador[0]].append(jugador[1:])
                    elif jugador[0] == "Team Totals":
                        estadisticasEquipo.append(jugador[1:])

        temporadaEquipo["equipo"] = estadisticasEquipo
        temporadaEquipo["jugadores"] = estadisticasJugadores
        fichero_datos = open("datos", "wb")
        pickle.dump(temporadaEquipo, fichero_datos)
        fichero_datos.close()
    else:
        infile = open("datos", "rb")
        temporadaEquipo = pickle.load(infile)
        infile.close()
    print(temporadaEquipo)


def leerCSVJugadores():
    datosJugador = {}
    with open('players.csv', newline='') as File:
        next(File)
        reader = csv.reader(File)
        for row in reader:
            if row[3] != "2019":
                break
            datos = {}
            datos["ID"] = row[2]
            datos["Equipo"] = row[1]
            datos["Estadisticas"] = {"Minutos": [], "Puntos": [], "Asistencias": [], "Rebotes": [], "Robos": [], "Tiros": [],
                                     "PorcentajeAciertos": [], "Triples": [], "PorcentajeTriples": []}
            datosJugador[row[0]] = datos
        fichero_datos = open("Jugadores", "wb")
        pickle.dump(datosJugador, fichero_datos)
        fichero_datos.close()


def leerCSVEquipos():
    global equipos
    datosEquipo = {}
    with open('teams.csv', newline='') as File:
        next(File)
        reader = csv.reader(File)
        for row in reader:
            datos = {}
            datos["Abreviatura"] = row[4]
            datos["NombreCompleto"] = list(equipos.keys())[list(equipos.values()).index(row[4])]
            datos["Estadio"] = row[8]
            datos["Estadisticas"] = {"Robos": [], "Faltas": [], "Rebotes": [], "TiempoPosesion" : []}
            datosEquipo[row[1]] = datos
        fichero_datos = open("Equipos", "wb")
        pickle.dump(datosEquipo, fichero_datos)
        fichero_datos.close()


def leerPartidos():
    leerCSVEquipos()
    infile = open("Equipos", "rb")
    equipo = pickle.load(infile)
    infile.close()
    with open('games.csv', newline='') as File:
        next(File)
        reader = csv.reader(File)
        for row in reader:
            equipo[row[3]]["Estadisticas"]["Rebotes"].append(int(float(row[12])))
            equipo[row[4]]["Estadisticas"]["Rebotes"].append(int(float(row[19])))
        fichero_datos = open("Equipos", "wb")
        pickle.dump(equipo, fichero_datos)
        fichero_datos.close()
    leerEstadisticasIndividualesEquipo()
    cambioClaves()


def leerPartidosJugadores():
    leerCSVJugadores()
    infile = open("Jugadores", "rb")
    jugadores = pickle.load(infile)
    infile.close()
    partidos = []
    with open('games_details.csv', newline='') as File:
        next(File)
        reader = csv.reader(File)
        for row in reader:
            partidos.append(row[0])
    with open('games_details.csv', newline='') as File:
        next(File)
        reader = csv.reader(File)
        for row in reader:
            if partidos.__contains__(row[0]) and list(jugadores.keys()).__contains__(row[5]):
                if row[9] != "":
                    jugadores[row[5]]["Estadisticas"]["Minutos"].append(row[9])
                if row[27] != "":
                    jugadores[row[5]]["Estadisticas"]["Puntos"].append(int(float(row[27])))
                if row[21] != "":
                    jugadores[row[5]]["Estadisticas"]["Rebotes"].append(int(float(row[21])))
                if row[22] != "":
                    jugadores[row[5]]["Estadisticas"]["Asistencias"].append(int(float(row[22])))
                if row[23] != "":
                    jugadores[row[5]]["Estadisticas"]["Robos"].append(int(float(row[23])))
                if row[11] != "":
                    jugadores[row[5]]["Estadisticas"]["Tiros"].append(int(float(row[11])))
                if row[12] != "":
                    jugadores[row[5]]["Estadisticas"]["PorcentajeAciertos"].append(float(row[12]))
                if row[14] != "":
                    jugadores[row[5]]["Estadisticas"]["Triples"].append(int(float(row[14])))
                if row[15] != "":
                    jugadores[row[5]]["Estadisticas"]["PorcentajeTriples"].append(float(row[15]))
        fichero_datos = open("Jugadores", "wb")
        pickle.dump(jugadores, fichero_datos)
        fichero_datos.close()


def cambioClaves():
    infile = open("Equipos", "rb")
    equipos = pickle.load(infile)
    infile.close()
    nuevoEquipos = {}
    for equipo in equipos:
        datos = {}
        datos["Abreviatura"] = equipos[equipo]["Abreviatura"]
        datos["ID"] = equipo
        datos["Estadio"] = equipos[equipo]["Estadio"]
        datos["Estadisticas"] = equipos[equipo]["Estadisticas"]
        nuevoEquipos[equipos[equipo]["NombreCompleto"]] = datos
    print(nuevoEquipos)
    fichero_datos = open("Equipos", "wb")
    pickle.dump(nuevoEquipos, fichero_datos)
    fichero_datos.close()


def leerEstadisticasIndividualesEquipo():
    infile = open("Equipos","rb")
    equipos = pickle.load(infile)
    infile.close()
    with open('games_details.csv', newline='') as File:
        next(File)
        reader = csv.reader(File)
        equipo = ""
        robos = 0
        faltas = 0
        for row in reader:
            if row[1] != equipo and equipo != "":
                equipos[equipo]["Estadisticas"]["Robos"].append(robos)
                equipos[equipo]["Estadisticas"]["Faltas"].append(faltas)
                robos = 0
                faltas = 0
            equipo = row[1]
            if row[23] != "":
                robos += int(float(row[23]))
            if row[26] != "":
                faltas += int(float(row[26]))
    fichero_datos = open("Equipos", "wb")
    pickle.dump(equipos, fichero_datos)
    fichero_datos.close()


def imprimirCSVJugadores():
    infile = open("Jugadores", "rb")
    jugadores = pickle.load(infile)
    infile.close()
    print(jugadores)


def imprimirCSVEquipo():
    infile = open("Equipos", "rb")
    jugadores = pickle.load(infile)
    infile.close()
    print(jugadores)


def ajustarDatos(nombre):
    infile = open("Equipos", "rb")
    jugadores = pickle.load(infile)
    infile.close()
    distribucion = {}
    #Datos jugadores
    for estadistica in jugadores[nombre]["Estadisticas"]:
        distribucion[estadistica] = []
        distribucion[estadistica].append(elegirDistribucion(jugadores[nombre]["Estadisticas"][estadistica]))
        distribucion[estadistica].append(jugadores[nombre]["Estadisticas"][estadistica])
    print(distribucion)


def elegirDistribucion(datos):
    resultados = Estadistica.comparar_distribuciones(
        x=np.array(list(datos)),  # Se pasa la lista como un array NumPy
        familia='realall',
        # Se escribe la familia de distribuciones que queremos tener en cuenta: {'realall', 'realline', 'realplus', 'real0to1', 'discreta'}
        ordenar='bic',
        verbose=False
    )
    return resultados.values[0][0]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    imprimirCSVJugadores()