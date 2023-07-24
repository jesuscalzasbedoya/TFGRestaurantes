import os
from flask import Flask, request, redirect
from neo4j import GraphDatabase
from web import index
import mainCodigo

#Conexion a la base de datos
url = "bolt://localhost:7687"
driver = GraphDatabase.driver(url, auth=("neo4j", "12345678"))
session = driver.session()
user_id = None

#Inicializar web
app = Flask(__name__)
template_dir = os.path.abspath('web/templates')
app.template_folder = template_dir

def obtenerAmigos (user_id):
    amigos = mainCodigo.obtenerAmigos(user_id, session)
    return amigos

def obtenerCiudades():
    ciudades = mainCodigo.obtenerCiudades(session)
    return ciudades

@app.route('/')
def main():
    return index.main()

"""
@app.route('/comprobarUserId')
def comprobarUserId():
    user_id = request.form.get('user_id')  # Obtener el valor del campo de texto del formulario
    ruta = '/'
    if (mainCodigo.comprobarId(user_id)):
        ruta = ''
"""


##############################
#####Mirar que esté bien######
##############################

@app.route('/amigosciudad', methods=['POST'])
def amigosCiudad():
    user_id = request.form.get('user_id')
    if mainCodigo.comprobarId(user_id, session):
        amigos = obtenerAmigos(user_id)
        ciudades = obtenerCiudades()
        return index.amigosCiudad(amigos, ciudades)
    else:
        return redirect('/')

@app.route('/amigosciudad/resultados', methods=['POST'])
def resultados():
    amigosSeleccionados = request.form.getlist('elegirAmigos')
    ciudadSelecionada = request.form.getlist('elegirCiudad')
    return index.resultados()


if __name__ == "__main__":
    app.run(debug= True, port=5001)


session.close()
