from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def main():
    data = {
        'titulo': 'Recomendación de Restaurantes'
    }
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        return render_template('indexIdErroneo.html', resultado=user_id, data=data)
    return render_template('index.html', data=data)

@app.route('/idErroneo', methods=['GET', 'POST'])
def idErroneo():
    data = {
        'titulo': 'Recomendación de Restaurantes'
    }
    return render_template('indexIdErroneo.html', data=data)

@app.route('/amigosciudad', methods=['GET'])
def amigosCiudad(amigos, ciudades):
    data = {
        'titulo': 'Recomendación de Restaurantes',
        'amigos': amigos,
        'ciudades': ciudades
    }
    return render_template('AmigosCiudad.html', data=data)

@app.route('/amigosciudad/resultados')
def resultados():
    data ={
        'titulo': 'Recomendación de Restaurantes',
        'nombre': 'Nombre',
        'direccion': 'Dirección',
        'valoracion': 'Valoración',
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
