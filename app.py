from flask import Flask, render_template, request
from dependencias import Simulacion
import pickle
import json

app = Flask(__name__)

#Ruta base: página principal
@app.route('/', methods=['GET', 'POST'])
def index() :
    return render_template('index.html')


#Ruta para elegir equipos
@app.route('/elegir_equipos_futuro', methods=['GET', 'POST'])
def elegir_futuro() :    
    return render_template('elegir_equipos_futuro.html')


#Ruta para elegir parámetros a simular
@app.route('/resultados_futuro', methods=['GET', 'POST'])
def simular_futuro() :
    if request.method == 'POST':
        temporada = int(request.form['temporada'])
        equipo1 = request.form['equipo1'].split(",")
        equipo2 = request.form['equipo2'].split(",")
        #Solicitar datos del partido
        nuevosDatos, pbp = Simulacion.simularPartido(equipo1, equipo2)
        infile = open(".\Ficheros\IdJugadores", "rb")
        ids = pickle.load(infile)
        infile.close()
        vis = str(nuevosDatos['puntuacionVisitante'])
        loc = str(nuevosDatos['puntuacionLocal'])
        return render_template('resultados_futuro.html', datos=nuevosDatos, pbp=json.dumps(pbp), ids=json.dumps(ids), equipo1=equipo1, equipo2=equipo2, atributosJ = ['JUGADOR', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'RB', 'AST', 'STL', 'PTS'], atributosE = ['FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'RB', 'AST', 'STL', 'PF', 'PTS'], vis=vis, loc=loc)


if __name__ == '__main__' :
    app.run(debug=True)