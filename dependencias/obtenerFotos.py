import json
import pickle


f = open('players.json')

data = json.load(f)

obj = dict()

for i in data['league']['standard']:
    obj[i["firstName"] + " " + i["lastName"]] = i["personId"]

f.close()

fichero_datos = open(".\Ficheros\IdJugadores", "wb")
pickle.dump(obj, fichero_datos)
fichero_datos.close()