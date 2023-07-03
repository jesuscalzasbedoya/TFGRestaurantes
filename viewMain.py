import os
from flask import Flask, render_template, request
from web import index
import mainCodigo
app = Flask(__name__)
template_dir = os.path.abspath('web/templates')
app.template_folder = template_dir

def obtenerAmigos ():
    amigos = []
    amigo = ("2", "u2")
    amigos.append(amigo)
    amigo = ("3", "u3")
    amigos.append(amigo)
    amigo = ("4", "u4")
    amigos.append(amigo)
    return amigos

def obtenerCiudades():
    ciudades = []
    ciudades.append("Madrid")
    ciudades.append("Ferrol")
    return ciudades


@app.route('/')
def main():
    return index.main()

@app.route('/amigosciudad', methods=['POST'])
def amigosCiudad():
    texto = request.form.get('user_id')  # Obtener el valor del campo de texto del formulario
    amigos = obtenerAmigos()
    ciudades = obtenerCiudades()
    return index.amigosCiudad(amigos, ciudades)

@app.route('/amigosciudad/resultados', methods=['POST'])
def resultados():
    amigosSeleccionados = request.form.getlist('elegirAmigos')
    ciudadSelecionada = request.form.getlist('elegirCiudad')
    return index.resultados()


if __name__ == "__main__":
    app.run(debug= True, port=5001)
