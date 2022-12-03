from flask import Flask, render_template, request
from jinja2.utils import markupsafe
from dependencias import Partido
from dependencias import Equipo

app = Flask(__name__)


#VARIABLES GLOBALES
datos = list()

#Ruta base: página principal
@app.route('/', methods=['GET', 'POST'])
def index() :
    return render_template('index.html')


#Ruta para elegir equipos
@app.route('/elegir_equipos', methods=['GET', 'POST'])
def simular() :    
    return render_template('elegir_equipos.html')


#Ruta para elegir partido
@app.route('/elegir_partido', methods=['GET', 'POST'])
def elegir_partido() :

    if request.method == 'POST':
        temporada = int(request.form['temporada'])
        equipo1 = request.form['equipo1'].split(",")
        equipo2 = request.form['equipo2'].split(",")
        #Solicitar partidos
        partidos = []
        partidos = Partido.obtenerPartidos(temporada, equipo1, equipo2)
        return render_template('elegir_partido.html', partidos=partidos, equipo1=equipo1, equipo2=equipo2, temporada=temporada)
    

#Ruta para elegir parámetros a simular
@app.route('/simular_partido', methods=['GET', 'POST'])
def simular_partido() :
    global datos
    if request.method == 'POST':
        temporada = int(request.form['temporada'])
        fechaPartido = request.form['partido']
        equipo1 = request.form['equipo1'].split(",")
        equipo2 = request.form['equipo2'].split(",")
        #Solicitar datos del partido
        datos = Partido.obtenerDatosPartido(equipo1, equipo2, fechaPartido, temporada)
        return render_template('simular_partido.html', datos=datos, atributos = ['JUGADOR', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', '+/-'])


#Ruta para mostrar resultados
@app.route('/resultados', methods=['GET', 'POST'])
def resultados() :
    global datos
    if request.method == 'POST':
        nCondiciones = int(request.form['nCondiciones'])
        condiciones = []
        for i in range(nCondiciones) :
            condiciones.append(dict())
            condiciones[i]["tipo"] = request.form['accion' + str(i + 1)]
            condiciones[i]["actor"] = request.form['actor' + str(i + 1)]
            if condiciones[i]["tipo"] == "equipo" :
                condiciones[i]["accion"] = request.form['accionequipo' + str(i + 1)]
            else :
               condiciones[i]["accion"] = request.form['accionjugador' + str(i + 1)] 
            condiciones[i]["valor"] = request.form['num' + str(i + 1)]
            if "tirado" in condiciones[i]["accion"] :
                condiciones[i]["tipotiro"] = request.form['tipotiro' + str(i + 1)]
        #resultados = simularPartido(datos, condiciones)
        return render_template('resultados.html')


if __name__ == '__main__' :
    app.run(debug=True)