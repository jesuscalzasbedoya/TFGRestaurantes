from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def main():
    data = {
        'titulo': 'GROUP EAT'
    }
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        return render_template('indexIdErroneo.html', resultado=user_id, data=data)
    return render_template('index.html', data=data)

@app.route('/idErroneo', methods=['GET', 'POST'])
def idErroneo():
    data = {
        'titulo': 'GROUP EAT'
    }
    return render_template('indexIdErroneo.html', data=data)

@app.route('/amigosciudad', methods=['GET'])
def amigosCiudad(amigos, ciudades, user_id):
    data = {
        'titulo': 'GROUP EAT',
        'amigos': amigos,
        'ciudades': ciudades
    }
    return render_template('AmigosCiudad.html', data=data, user_id=user_id)

@app.route('/amigosciudad/resultados')
def resultados(restaurantes, user_id):
    data ={
        'titulo': 'GROUP EAT',
        'nombre': 'Nombre',
        'direccion': 'Dirección',
        'valoracion': 'Valoración',
        'restaurantes': restaurantes,
        'user_id': user_id
    }
    return render_template('MostrarResultados.html', data = data)

def query_string():
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    return "ok"

def pagina_no_encontrada(error):
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.add_url_rule('/query_string', view_func=query_string)
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug= True, port=5001)
