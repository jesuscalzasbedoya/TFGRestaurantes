from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)



@app.route("/")
def home():
    data = {
        'titulo': 'Recomendación de Restaurantes'
    }
    return render_template('index.html', data=data) 

@app.route('/contacto/<nombre>/<int:edad>')
def contacto(nombre, edad):
    data = {
        'titulo': 'Contacto',
        'nombre':  nombre,
        'edad': edad
    }
    return render_template('contacto.html', data=data)

@app.route('/amigosciudad')
def amigosCiudad():
    data = {
        'titulo': 'Recomendación de Restaurantes',
        'amigos': 'Elegir amigos',
        'ciudad': 'Elegir ciudad'
    }
    return render_template('AmigosCiudad.html', data=data)

@app.route('/amigosciudad/resultados')
def resultados():
    data ={
        'titulo': 'Recomendación de Restaurantes',
        'nombre': 'Nombre',
        'direccion': 'Dirección',
        'valoracion': 'Valoración'
    }
    return render_template('MostrarResultados.html', data = data)

def query_string():
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    return "ok"

def pagina_no_encontrada(error):
    return redirect(url_for('home'))

"""
@app.route("/result",methods = ['POST', "GET"])
def result():
    output = request.form.to_dict()
    user_id = output["user_id"]

    return render_template('index.html', user_id=user_id)
"""

if __name__ == "__main__":
    app.add_url_rule('/query_string', view_func=query_string)
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug= True, port=5001)
