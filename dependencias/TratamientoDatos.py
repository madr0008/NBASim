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

posesiones = 0


def cargaDatosGeneral():
    leerPartidos()
    leerPartidosJugadores()
    cambioClaves()


def leerCSVJugadores():
    infile = open(".\Ficheros\Equipos", "rb")
    equipo = pickle.load(infile)
    infile.close()
    datosJugador = {}
    with open('.\Ficheros\players.csv', newline='') as File:
        next(File)
        reader = csv.reader(File)
        for row in reader:
            if row[3] != "2019":
                break
            datos = {}
            datos["ID"] = row[2]
            datos["Equipo"] = equipo[row[1]]["NombreCompleto"]
            datos["Estadisticas"] = {"Asistencias": [], "Rebotes": [], "Robos": [],"ProbabilidadTiro": [],
                                     "PorcentajeAciertos": [],"PorcentajeTriples": [] , "PorcentajeAciertoTriples": []}
            datosJugador[row[0]] = datos
        fichero_datos = open(".\Ficheros\Jugadores", "wb")
        pickle.dump(datosJugador, fichero_datos)
        fichero_datos.close()


def leerCSVEquipos():
    global equipos
    tiemposPosesion = {}
    # Adición tiempo de posesion
    with open('.\Ficheros\Datos_posesiones.csv', newline='') as File:
        next(File)
        next(File)
        reader = csv.reader(File)
        for row in reader:
            tiemposPosesion[row[1]] = float(row[2])
    datosEquipo = {}
    with open('.\Ficheros\equipos.csv', newline='') as File:
        next(File)
        reader = csv.reader(File)
        for row in reader:
            datos = {}
            datos["Abreviatura"] = row[4]
            datos["NombreCompleto"] = list(equipos.keys())[list(equipos.values()).index(row[4])]
            datos["Estadio"] = row[8]
            datos["Estadisticas"] = {"Tiros": [], "Robos": [],"PorcentajeRobos": [], "Faltas": [],"PorcentajeFaltas": [], "Rebotes": [], "PorcentajeRebote": [],"Asistencias": [], "TiempoPosesion" : tiemposPosesion[row[4]]}
            datosEquipo[row[1]] = datos
    fichero_datos = open(".\Ficheros\Equipos", "wb")
    pickle.dump(datosEquipo, fichero_datos)
    fichero_datos.close()


def leerPartidos():
    leerCSVEquipos()
    infile = open(".\Ficheros\Equipos", "rb")
    equipo = pickle.load(infile)
    infile.close()
    with open('.\Ficheros\games.csv', newline='') as File:
        next(File)
        reader = csv.reader(File)
        for row in reader:
            equipo[row[3]]["Estadisticas"]["Rebotes"].append(int(float(row[12])))
            equipo[row[4]]["Estadisticas"]["Rebotes"].append(int(float(row[19])))
            equipo[row[3]]["Estadisticas"]["PorcentajeRebote"].append(int(float(row[12])) / (int(float(row[12])) + int(float(row[19]))))
            equipo[row[4]]["Estadisticas"]["PorcentajeRebote"].append(int(float(row[19])) / (int(float(row[12])) + int(float(row[19]))))
            equipo[row[3]]["Estadisticas"]["Asistencias"].append(int(float(row[11])))
            equipo[row[4]]["Estadisticas"]["Asistencias"].append(int(float(row[18])))
    fichero_datos = open(".\Ficheros\Equipos", "wb")
    pickle.dump(equipo, fichero_datos)
    fichero_datos.close()
    leerEstadisticasIndividualesEquipo()


def leerPartidosJugadores():
    global equipos

    leerCSVJugadores()
    infile = open(".\Ficheros\Jugadores", "rb")
    jugadores = pickle.load(infile)
    infile.close()

    infile = open(".\Ficheros\Equipos", "rb")
    equiposDatos = pickle.load(infile)
    infile.close()
    partidos = []
    iterador = dict()
    for equipo in equiposDatos.keys():
        iterador[equiposDatos[equipo]["NombreCompleto"]] = dict()
        iterador[equiposDatos[equipo]["NombreCompleto"]]["ID"] = equipo
        iterador[equiposDatos[equipo]["NombreCompleto"]]["Numero"] = 0
    with open('.\Ficheros\games.csv', newline='') as File:
        next(File)
        reader = csv.reader(File)
        for row in reader:
            partidos.append(row[1])
    with open('.\Ficheros\games_details.csv', newline='') as File:
        next(File)
        reader = csv.reader(File)
        equipoPartido = ""
        for row in reader:
            eq = list(equipos.keys())[list(equipos.values()).index(row[2])]
            if (row[0] in partidos) and (row[5] in list(jugadores.keys())) and (jugadores[row[5]]["Equipo"] == eq) :
                if eq != equipoPartido and equipoPartido != "":
                    iterador[equipoPartido]["Numero"] += 1
                equipoPartido = eq
                if row[21] != "":
                    jugadores[row[5]]["Estadisticas"]["Rebotes"].append(int(float(row[21])) / equiposDatos[iterador[jugadores[row[5]]["Equipo"]]["ID"]]["Estadisticas"]["Rebotes"][iterador[jugadores[row[5]]["Equipo"]]["Numero"]])
                if row[22] != "":
                    jugadores[row[5]]["Estadisticas"]["Asistencias"].append(int(float(row[22])) / equiposDatos[iterador[jugadores[row[5]]["Equipo"]]["ID"]]["Estadisticas"]["Asistencias"][iterador[jugadores[row[5]]["Equipo"]]["Numero"]])
                if row[23] != "":
                    try :
                        jugadores[row[5]]["Estadisticas"]["Robos"].append(int(float(row[23])) / equiposDatos[iterador[jugadores[row[5]]["Equipo"]]["ID"]]["Estadisticas"]["Robos"][iterador[jugadores[row[5]]["Equipo"]]["Numero"]])
                    except :
                        jugadores[row[5]]["Estadisticas"]["Robos"].append(0)
                if row[11] != "":
                    try :
                        jugadores[row[5]]["Estadisticas"]["ProbabilidadTiro"].append(int(float(row[11])) / equiposDatos[iterador[jugadores[row[5]]["Equipo"]]["ID"]]["Estadisticas"]["Tiros"][iterador[jugadores[row[5]]["Equipo"]]["Numero"]])
                    except :
                        pass
                if row[12] != "":
                    valor = row[12].replace(",",".")
                    jugadores[row[5]]["Estadisticas"]["PorcentajeAciertos"].append(float(valor))
                if row[14] != "":
                    try :
                        jugadores[row[5]]["Estadisticas"]["PorcentajeTriples"].append(int(float(row[14])) / int(float(row[11])))
                    except :
                        jugadores[row[5]]["Estadisticas"]["PorcentajeTriples"].append(0)
                if row[15] != "":
                    valor = row[12].replace(",", ".")
                    jugadores[row[5]]["Estadisticas"]["PorcentajeAciertoTriples"].append(float(valor))
        fichero_datos = open(".\Ficheros\Jugadores", "wb")
        pickle.dump(jugadores, fichero_datos)
        fichero_datos.close()


def cambioClaves():
    global equipos

    infile = open(".\Ficheros\Equipos", "rb")
    equiposDatos = pickle.load(infile)
    infile.close()
    nuevoEquipos = {}
    for equipo in equiposDatos.keys():
        datos = {}
        datos["Abreviatura"] = equiposDatos[equipo]["Abreviatura"]
        datos["ID"] = equiposDatos
        datos["Estadio"] = equiposDatos[equipo]["Estadio"]
        datos["Estadisticas"] = equiposDatos[equipo]["Estadisticas"]
        nuevoEquipos[equiposDatos[equipo]["NombreCompleto"]] = datos
    fichero_datos = open(".\Ficheros\Equipos", "wb")
    pickle.dump(nuevoEquipos, fichero_datos)
    fichero_datos.close()


def leerEstadisticasIndividualesEquipo():
    infile = open(".\Ficheros\Equipos","rb")
    equiposDatos = pickle.load(infile)
    infile.close()
    with open('.\Ficheros\games_details.csv', newline='') as File:
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
                equiposDatos[equipo2]["Estadisticas"]["Robos"].append(robos)
                equiposDatos[equipo2]["Estadisticas"]["Faltas"].append(faltas)
                equiposDatos[equipo2]["Estadisticas"]["Tiros"].append(tiros)
                if robos == 0:
                    equiposDatos[equipo2]["Estadisticas"]["PorcentajeRobos"].append(robos)
                else:
                    equiposDatos[equipo2]["Estadisticas"]["PorcentajeRobos"].append(robos / (robos + equiposDatos[equipo]["Estadisticas"]["Robos"][len(equiposDatos[equipo]["Estadisticas"]["Robos"]) - 1]))
                equiposDatos[equipo2]["Estadisticas"]["PorcentajeFaltas"].append(faltas / (faltas + equiposDatos[equipo]["Estadisticas"]["Faltas"][len(equiposDatos[equipo]["Estadisticas"]["Faltas"]) - 1]))
                if  equiposDatos[equipo]["Estadisticas"]["Robos"][len(equiposDatos[equipo]["Estadisticas"]["Robos"]) - 1] != 0:
                    equiposDatos[equipo]["Estadisticas"]["PorcentajeRobos"].append(equiposDatos[equipo]["Estadisticas"]["Robos"][len(equiposDatos[equipo]["Estadisticas"]["Robos"]) - 1] / (robos + equiposDatos[equipo]["Estadisticas"]["Robos"][len(equiposDatos[equipo]["Estadisticas"]["Robos"]) - 1]))
                equiposDatos[equipo]["Estadisticas"]["PorcentajeFaltas"].append(equiposDatos[equipo]["Estadisticas"]["Faltas"][len(equiposDatos[equipo]["Estadisticas"]["Faltas"]) - 1] / (robos + equiposDatos[equipo]["Estadisticas"]["Faltas"][len(equiposDatos[equipo]["Estadisticas"]["Faltas"]) - 1]))
                robos = 0
                faltas = 0
                tiros = 0
                equipo = ""
                equipo2 = ""
                iterador = 0
            elif row[1] != equipo and equipo != "" and equipo2 == "":
                equipo2 = row[1]
                equiposDatos[equipo]["Estadisticas"]["Robos"].append(robos)
                equiposDatos[equipo]["Estadisticas"]["Faltas"].append(faltas)
                equiposDatos[equipo]["Estadisticas"]["Tiros"].append(tiros)
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
    fichero_datos = open(".\Ficheros\Equipos", "wb")
    pickle.dump(equiposDatos, fichero_datos)
    fichero_datos.close()


def imprimirCSVJugadores():
    infile = open(".\Ficheros\Jugadores", "rb")
    jugadores = pickle.load(infile)
    infile.close()
    print(jugadores)


def imprimirCSVEquipo():
    infile = open(".\Ficheros\Equipos", "rb")
    jugadores = pickle.load(infile)
    infile.close()
    print(jugadores)


def ajustarDatos(nombre, min, max):
    archivo = ""
    if nombre in equipos.keys() :
        archivo = ".\Ficheros\Equipos"
    infile = open(archivo, "rb")
    objeto = pickle.load(infile)
    infile.close()
    distribucion = dict()
    for estadistica in objeto[nombre]["Estadisticas"]:
        if estadistica != "TiempoPosesion" :
            distribucion[estadistica] = dict() #Deberia ser un dict, creo
            n, p = elegirDistribucion(objeto[nombre]["Estadisticas"][estadistica])
            distribucion[estadistica]['nombre'] = n
            distribucion[estadistica]['parametros'] = p
        else :
            distribucion[estadistica] = dict()
            distribucion[estadistica]['nombre'] = "triangular"
            distribucion[estadistica]['min'] = min
            distribucion[estadistica]['max'] = max
            distribucion[estadistica]['media'] = objeto[nombre]["Estadisticas"][estadistica]
            
    return distribucion


def ajustarDatosJugadores(equipoLocal, equipoVisitante):
    infile = open(".\Ficheros\Jugadores", "rb")
    objetos = pickle.load(infile)
    infile.close()
    distribucion = dict()
    for objeto in objetos.keys():
        if objetos[objeto]["Equipo"] == equipoLocal or objetos[objeto]["Equipo"] == equipoVisitante:
            distribucion[objeto] = dict()
            for estadistica in objetos[objeto]["Estadisticas"]:
                distribucion[objeto][estadistica] = dict()
                n, p = elegirDistribucion(objetos[objeto]["Estadisticas"][estadistica])
                distribucion[objeto][estadistica]['nombre'] = n
                distribucion[objeto][estadistica]['parametros'] = p
    return distribucion


def elegirDistribucion(datos):
    # print(np.array(list(datos)))
    resultados = Estadistica.comparar_distribuciones(
        x=np.array(list(datos)),  # Se pasa la lista como un array NumPy
        familia='realall',
        # Se escribe la familia de distribuciones que queremos tener en cuenta: {'realall', 'realline', 'realplus', 'real0to1', 'discreta'}
        ordenar='bic',
        verbose=False
    )
    return resultados.values[0][0], resultados.values[0][5]
