from basketball_reference_scraper.box_scores import get_box_scores
from basketball_reference_scraper.seasons import get_schedule, get_standings
from basketball_reference_scraper.shot_charts import get_shot_chart
from dependencias import Equipo
from pandas import DataFrame as df


def obtenerPartidos(temporada, equipo1, equipo2):
    calendario = get_schedule(temporada,False)
    partidos = []
    for partido in calendario.values:
        datos = {}
        if (partido[1] == equipo1[1] or partido[1] == equipo2[1]) and (partido[3] == equipo1[1] or partido[3] == equipo2[1]):
            datos["visitante"] = []
            if partido[1] == equipo1[1] :
                datos["visitante"].append(equipo1[0])
            else :
                datos["visitante"].append(equipo2[0])
            datos["visitante"].append(partido[1])
            datos["puntuacionVisitante"] = partido[2]
            datos["local"] = []
            if partido[3] == equipo1[1] :
                datos["local"].append(equipo1[0])
            else :
                datos["local"].append(equipo2[0])
            datos["local"].append(partido[3])
            datos["puntuacionLocal"] = partido[4]
            datos["estadio"] = Equipo.obtenerEstadio(partido[3], temporada)
            datos["fecha"] = str(partido[0])[:-9]
            partidos.append(datos)
    return partidos


def obtenerDatosPartido(equipo1, equipo2, fecha, temporada):
    partido = dict()
    datosPlantillaLocal = {}
    datosPlantillaVisitante = {}
    datosEquipoLocal = []
    datosEquipoVisitante = []
    estadisticas = get_box_scores(fecha,equipo1[0],equipo2[0])
    for jugador in estadisticas[equipo1[0]].values:
        datosPlantillaLocal[jugador[0]] = jugador[1:]
    datosEquipoLocal = datosPlantillaLocal['Team Totals']
    datosPlantillaLocal.pop('Team Totals')
    for jugador in estadisticas[equipo2[0]].values:
        datosPlantillaVisitante[jugador[0]] = jugador[1:]
    datosEquipoVisitante = datosPlantillaVisitante['Team Totals']
    datosPlantillaVisitante.pop('Team Totals')
    partido['local'] = equipo1
    partido['visitante'] = equipo2
    partido['fecha'] = fecha
    partido['estadisticasLocal'] = datosEquipoLocal
    partido['estadisticasVisitante'] = datosEquipoVisitante
    partido['jugadoresLocal'] = datosPlantillaLocal
    partido['jugadoresVisitante'] = datosPlantillaVisitante
    
    return partido