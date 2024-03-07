from neo4j import GraphDatabase
from Algoritmos import Algoritmo
from Usuario import Usuario
from Grupo import Grupo
from Restaurante import Restaurante

#Conexion a la base de datos

def obtenerCiudades(session):
    lista = []
    query = ("MATCH (r:Restaurante) RETURN DISTINCT(r.city) as ciudad ORDER BY r.city ASC")
    result = session.run(query)
    while result.peek():
        record = result.__next__()
        node = record["ciudad"]
        lista.append(node)
    return lista

#Funciones
def obtenerAmigos(user_id, session):
    user = Usuario(user_id, session)
    amigos = []
    if(len(user.friends) > 0):
        for amigo in user.friends:
            a = (amigo.get("user_id"), amigo.get("name"))
            amigos.append(a)
    return amigos        

def sanearRestaurantes(listaPred, ciudad, session):
    listaRest = []
    listaFinal = []
    for i in listaPred:
        apariciones = 0
        prediccion = 0
        registrado = False
        for j in listaRest:
            if (j[0].restaurante_id == i[0]):
                registrado = True
                break
        if (registrado == False):
            for k in listaPred:
                if (i[0] == k[0]):
                    apariciones += 1
                    prediccion += k[1]
            tupla = (Restaurante(i[0], session), round(prediccion / apariciones, 2))
            listaRest.append(tupla)
    for i in listaRest:
        if i[0].ciudad == ciudad[0]:
            tupla = (i[0].name, i[0].direccion, i[1])
            listaFinal.append(tupla)
    listaFinal.sort(key=lambda x: x[2], reverse=True)  
    return listaFinal[:5]


def eliminarGrupo(grupo, session):
    query = "MATCH (g:Grupo{grupo_id: '" + grupo.grupo_id + "'})-[r]->() DELETE r, g"
    session.run(query)

#Programa
#Introducir el id
def comprobarId(idUsuario, session):
    idCorrecto = False
    user = Usuario(idUsuario, session)
    if(user.existeUsuario() == True):
        idCorrecto = True
    return idCorrecto

def generarRecomendacion(seleccionados, ciudad, session):
    grupo = Grupo(seleccionados, session)
    algoritmo = Algoritmo(session)

    #######################
    ####USUARIOS AFINES####
    #######################
    usuariosAfines = []
    usuariosAfines = algoritmo.usuariosAfines(grupo)
    
    #######################
    #######SIMILITUD#######
    #######################

    similitudes = []

    for i in usuariosAfines:
        similitudes.append(algoritmo.similitud(grupo, i))

    similitudes = sorted(similitudes, key=lambda tupla: tupla[1])
    similitudes = similitudes[:10]

    ########################
    #######PREDICCION#######
    ########################

    listaPredicciones = []
    listaRestaurantes = []

    for i in similitudes:
        listaPredicciones += algoritmo.prediccion(grupo, i)
    
    #####ObtenerCiudad#####
    listaRestaurantes = sanearRestaurantes(listaPredicciones, ciudad, session)

    eliminarGrupo(grupo, session)

    return listaRestaurantes