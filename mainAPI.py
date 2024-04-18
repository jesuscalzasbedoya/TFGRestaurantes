from flask import Flask, jsonify, request
from neo4j import GraphDatabase
import DataExchange

#Conexion a la base de datos
url = "bolt://localhost:7687"
driver = GraphDatabase.driver(url, auth=("neo4j", "12345678"))
session = driver.session()
user_id = None

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
        amigos = jsonify(DataExchange.obtenerAmigos(user_id, session))
    else:
        # DEBO MANEJAR QUE EL USUARIO NO SEA CORRECTO
        None
    return amigos

# Muestra la lista de ciudades elegibles
@app.route("/<user_id>/<path:amigos>/ciudad")
def getCiudad(user_id, amigos):
    # listaAmigos = amigos.split("-")
    return DataExchange.obtenerCiudades(session)

# Muestra los restaurantes resultado
@app.route("/<user_id>/<path:amigos>/<ciudad>/resultados")
def mostrarResultados(user_id, amigos, ciudad):
    listaAmigos = amigos.split("-")
    return DataExchange.obtenerRestaurantes(amigos, user_id, ciudad, session)

if __name__=="__main__":
    app.run(debug=True, port=5002) 