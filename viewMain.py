import os
from flask import Flask, request, redirect
from neo4j import GraphDatabase
from web import index
import DataExchange

#Conexion a la base de datos
url = "bolt://localhost:7687"
driver = GraphDatabase.driver(url, auth=("neo4j", "12345678"))
session = driver.session()
user_id = None

#Inicializar web
app = Flask(__name__)
template_dir = os.path.abspath('web/templates')
app.template_folder = template_dir

@app.route('/')
def main():
    return index.main()

@app.route('/idErroneo')
def idErroneo():
    return index.idErroneo()

@app.route('/amigosciudad', methods=['GET', 'POST'])
def amigosCiudad():
    user_id = request.form.get('user_id')
    app.config['user_id'] = user_id
    if DataExchange.comprobarId(user_id, session):
        amigos = DataExchange.obtenerAmigos(user_id, session)
        ciudades = DataExchange.obtenerCiudades(session)
        return index.amigosCiudad(amigos, ciudades, user_id)
    else:
        return redirect('/idErroneo')

@app.route('/amigosciudad/resultados', methods=['POST'])
def resultados():
    amigosSeleccionados = request.form.getlist('elegirAmigos')
    ciudadSelecionada = request.form.getlist('elegirCiudad')
    restaurantes = DataExchange.obtenerRestaurantes(amigosSeleccionados, app.config['user_id'], ciudadSelecionada, session)
    # Usa user_id como sea necesario en el procesamiento de resultados
    return index.resultados(restaurantes, user_id)

if __name__ == "__main__":
    app.run(debug= True, port=5001)


session.close()
