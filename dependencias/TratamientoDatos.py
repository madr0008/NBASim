import pickle
import csv
from dependencias import Estadistica
import numpy as np


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


def cargaDatosGeneral():
    leerPartidos()
    leerPartidosJugadores()
    cambioClaves()


def leerCSVJugadores():
    infile = open("Equipos", "rb")
    equipo = pickle.load(infile)
    infile.close()
    datosJugador = {}
    with open('players.csv', newline='') as File:
        next(File)
        reader = csv.reader(File)
        for row in reader:
            if row[3] != "2019":
                break
            datos = {}
            datos["ID"] = row[2]
            datos["Equipo"] = equipo[row[1]]["NombreCompleto"]
            datos["Estadisticas"] = {"Minutos": [], "Puntos": [], "Asistencias": [], "Rebotes": [], "Robos": [], "Tiros": [], "ProbabilidadTiro": [],
                                     "PorcentajeAciertos": [], "Triples": [],"PorcentajeTriples": [] , "PorcentajeAciertoTriples": []}
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
            datos["Estadisticas"] = {"Tiros": [], "Robos": [],"PorcentajeRobos": [], "Faltas": [],"PorcentajeFaltas": [], "Rebotes": [], "PorcentajeRebote": [], "TiempoPosesion" : []}
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
            equipo[row[3]]["Estadisticas"]["PorcentajeRebote"].append(int(float(row[12])) / (int(float(row[12])) + int(float(row[19]))))
            equipo[row[4]]["Estadisticas"]["PorcentajeRebote"].append(int(float(row[19])) / (int(float(row[12])) + int(float(row[19]))))
            equipo[row[3]]["Estadisticas"]["Asistencias"].append(int(float(row[11])))
            equipo[row[4]]["Estadisticas"]["Asistencias"].append(int(float(row[18])))
        fichero_datos = open("Equipos", "wb")
        pickle.dump(equipo, fichero_datos)
        fichero_datos.close()
    leerEstadisticasIndividualesEquipo()


def leerPartidosJugadores():
    leerCSVJugadores()
    infile = open("Jugadores", "rb")
    jugadores = pickle.load(infile)
    infile.close()

    infile = open("Equipos", "rb")
    equipos = pickle.load(infile)
    infile.close()
    partidos = []
    iterador = {}
    for equipo in equipos:
        iterador[equipo] = 0
    with open('games.csv', newline='') as File:
        next(File)
        reader = csv.reader(File)
        for row in reader:
            partidos.append(row[1])
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
                    jugadores[row[5]]["Estadisticas"]["Rebotes"].append(int(float(row[21])) / equipos[jugadores[row[5]]["Equipo"]]["Estadisticas"]["Rebotes"][iterador[jugadores[row[5]]["Equipo"]]])
                if row[22] != "":
                    jugadores[row[5]]["Estadisticas"]["Asistencias"].append(int(float(row[22])) / equipos[jugadores[row[5]]["Equipo"]]["Estadisticas"]["Asistencias"][iterador[jugadores[row[5]]["Equipo"]]])
                if row[23] != "":
                    jugadores[row[5]]["Estadisticas"]["Robos"].append(int(float(row[23])) / equipos[jugadores[row[5]]["Equipo"]]["Estadisticas"]["Robos"][iterador[jugadores[row[5]]["Equipo"]]])
                if row[11] != "":
                    jugadores[row[5]]["Estadisticas"]["Tiros"].append(int(float(row[11])))
                    jugadores[row[5]]["Estadisticas"]["ProbabilidadTiro"].append(int(float(row[11])) / equipos[jugadores[row[5]]["Equipo"]]["Estadisticas"]["Tiros"][iterador[jugadores[row[5]]["Equipo"]]])
                if row[12] != "":
                    jugadores[row[5]]["Estadisticas"]["PorcentajeAciertos"].append(float(row[12]))
                if row[14] != "":
                    jugadores[row[5]]["Estadisticas"]["Triples"].append(int(float(row[14])))
                    jugadores[row[5]]["Estadisticas"]["PorcentajeTriples"].append(int(float(row[14])) / int(float(row[11])))
                if row[15] != "":
                    jugadores[row[5]]["Estadisticas"]["PorcentajeAciertoTriples"].append(float(row[15]))
            iterador[jugadores[row[5]]["Equipo"]] += 1
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
    # Adición tiempo de posesion
    with open('Datos_posesiones.csv', newline='') as File:
        next(File)
        next(File)
        reader = csv.reader(File)
        for row in reader:
            nuevoEquipos[list(equipos.keys())[list(equipos.values()).index(row[1])]]["Estadisticas"]["TiempoPosesion"] = row[2]
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
        equipo2 = ""
        robos = 0
        faltas = 0
        tiros = 0
        iterador = 0
        for row in reader:
            if row[1] != equipo2 and equipo2 != "":
                equipos[equipo2]["Estadisticas"]["Robos"].append(robos)
                equipos[equipo2]["Estadisticas"]["Faltas"].append(faltas)
                equipos[equipo2]["Estadisticas"]["Tiros"].append(tiros)
                if robos == 0:
                    equipos[equipo2]["Estadisticas"]["PorcentajeRobos"].append(robos)
                else:
                    equipos[equipo2]["Estadisticas"]["PorcentajeRobos"].append(robos / (robos + equipos[equipo]["Estadisticas"]["Robos"][len(equipos[equipo]["Estadisticas"]["Robos"]) - 1]))
                equipos[equipo2]["Estadisticas"]["porcentajeFaltas"].append(faltas / (faltas + equipos[equipo]["Estadisticas"]["Faltas"][len(equipos[equipo]["Estadisticas"]["Faltas"]) - 1]))
                if  equipos[equipo]["Estadisticas"]["Robos"][len(equipos[equipo]["Estadisticas"]["Robos"]) - 1] != 0:
                    equipos[equipo]["Estadisticas"]["PorcentajeRobos"][len(equipos[equipo]["Estadisticas"]["Robos"]) - 1].append(
                        equipos[equipo]["Estadisticas"]["Robos"][len(equipos[equipo]["Estadisticas"]["Robos"]) - 1] / (robos + equipos[equipo]["Estadisticas"]["Robos"][len(equipos[equipo]["Estadisticas"]["Robos"]) - 1]))
                equipos[equipo]["Estadisticas"]["PorcentajeFaltas"][len(equipos[equipo]["Estadisticas"]["Faltas"]) - 1].append(
                    equipos[equipo]["Estadisticas"]["Faltas"][len(equipos[equipo]["Estadisticas"]["Faltas"]) - 1] / (robos + equipos[equipo]["Estadisticas"]["Faltas"][len(equipos[equipo]["Estadisticas"]["Faltas"]) - 1]))
                robos = 0
                faltas = 0
                tiros = 0
                equipo = ""
                equipo2 = ""
                iterador = 0
            elif row[1] != equipo and equipo != "" and equipo2 == "":
                equipo2 = row[1]
                equipos[equipo]["Estadisticas"]["Robos"].append(robos)
                equipos[equipo]["Estadisticas"]["Faltas"].append(faltas)
                equipos[equipo]["Estadisticas"]["Tiros"].append(tiros)
                robos = 0
                faltas = 0
                tiros = 0
            if iterador == 0:
                equipo = row[1]
                iterador += 1
            if row[23] != "":
                robos += int(float(row[23]))
            if row[26] != "":
                faltas += int(float(row[26]))
            if row[11] != "":
                tiros += int(float(row[11]))
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
    archivo = ""
    if nombre in equipos.keys :
        archivo = "Equipos"
    infile = open(archivo, "rb")
    objeto = pickle.load(infile)
    infile.close()
    distribucion = {}
    #Datos jugadores
    for estadistica in objeto[nombre]["Estadisticas"]:
        distribucion[estadistica] = []
        distribucion[estadistica].append(elegirDistribucion(objeto[nombre]["Estadisticas"][estadistica])[0])
        distribucion[estadistica].append(elegirDistribucion(objeto[nombre]["Estadisticas"][estadistica])[1])
        distribucion[estadistica].append(objeto[nombre]["Estadisticas"][estadistica])
    return distribucion


def ajustarDatosJugadores(equipoLocal,equipoVisitante):
    infile = open("Jugadores", "rb")
    objetos = pickle.load(infile)
    infile.close()
    distribucion = {}
    for objeto in objetos:
        if objetos[objeto]["Equipo"] == equipoLocal or objetos[objeto]["Equipo"] == equipoVisitante:
            distribucion[objeto] = {}
            for estadistica in objetos[objeto]["Estadisticas"]:
                distribucion[objeto][estadistica] = []
                distribucion[objeto][estadistica].append(elegirDistribucion(objetos[objeto]["Estadisticas"][estadistica])[0])
                distribucion[objeto][estadistica].append(elegirDistribucion(objetos[objeto]["Estadisticas"][estadistica])[1])
                distribucion[objeto][estadistica].append(objetos[objeto]["Estadisticas"][estadistica])
    return distribucion


def elegirDistribucion(datos):
    resultados = Estadistica.comparar_distribuciones(
        x=np.array(list(datos)),  # Se pasa la lista como un array NumPy
        familia='realall',
        # Se escribe la familia de distribuciones que queremos tener en cuenta: {'realall', 'realline', 'realplus', 'real0to1', 'discreta'}
        ordenar='bic',
        verbose=False
    )
    return resultados.values[0][0], resultados.values[0][5]
