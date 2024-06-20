from flask import Flask, jsonify, request
from neo4j import GraphDatabase
import DataExchange

#Conexion a la base de datos
url = "bolt://localhost:7687"
driver = GraphDatabase.driver(url, auth=("neo4j", "12345678"))
session = driver.session()

app = Flask (__name__)

# Ruta base
@app.route('/')
def getUser():
    return ""

# Recoje el id de la url mostrando la lista de amigos
@app.route("/<user_id>/amigos")
def getAmigos(user_id):
    # Comprobamos que el usuario introducido es correcto
    if DataExchange.comprobarId(user_id,session):
        amigos = DataExchange.obtenerAmigos(user_id, session)
        amigosData = []
        for amigo in amigos:
            amigosData.append({'user_id': amigo[0], 'name': amigo[1]})
        amigosFinal = jsonify(amigosData)
    else:
        # TODO MANEJAR QUE EL USUARIO NO SEA CORRECTO
        None
    return amigosFinal

# Muestra la lista de ciudades elegibles
@app.route("/<user_id>/<path:amigos>/ciudad")
def getCiudad(user_id, amigos):
    # listaAmigos = amigos.split("-")
    listaCiudades = []
    ciudades = DataExchange.obtenerCiudades(user_id, session)
    for c in ciudades:
        listaCiudades.append({'Ciudad':c})
    ciudadesFinal = jsonify(listaCiudades)
    return ciudadesFinal

# Muestra los restaurantes resultado
@app.route("/<user_id>/<path:amigos>/<ciudad>/resultados")
def mostrarResultados(user_id, amigos, ciudad):
    listaResultados = []
    listaAmigos = amigos.split("-")
    resultados = DataExchange.obtenerRestaurantes(listaAmigos, user_id, ciudad, session)
    for r in resultados:
        listaResultados.append({'Nombre':r[0] ,'Stars': r[1], 'Direccion': r[2]})
    resultadosFinal = jsonify(listaResultados)
    return resultadosFinal

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port=5002) 

session.close()