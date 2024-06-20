from neo4j import GraphDatabase
from Algoritmos import Algoritmo
from Usuario import Usuario
from Grupo import Grupo
from Restaurante import Restaurante

#Funciones
def obtenerCiudades(user_id, session):
    lista = []
    query = ("MATCH (u:Usuario{user_id:'" + user_id + "'})-[:FRIEND]->(a:Usuario) WITH COLLECT(u) + COLLECT(a) AS grupo MATCH (g)-[:Reviews]->(:Restaurante)<-[:Reviews]-(u:Usuario)-[:Reviews]-(r:Restaurante) WHERE g IN grupo RETURN DISTINCT r.city as Ciudad")
    result = session.run(query)
    while result.peek():
        record = result.__next__()
        node = record["Ciudad"]
        lista.append(node)
    return lista

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
    # Se comprueba que no se repita el mismo restaurante
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
            # Se añade a la lista resultante el restaurante junto a la media de todas las predicciones
            tupla = (Restaurante(i[0], session), round(prediccion / apariciones, 2))
            listaRest.append(tupla)
    # Se seleccionan únicamente los restaurantes que se encuentran en la ciudad indicada
    for i in listaRest:
        if i[0].ciudad == ciudad[0] or i[0].ciudad == ciudad:
            tupla = (i[0].name, i[1], i[0].direccion)
            listaFinal.append(tupla)
    # Devolver los 5 restaurantes con predicción más alta
    listaFinal.sort(key=lambda x: x[1], reverse=True)  
    return listaFinal[:5]

def eliminarGrupo(grupo, session):
    query = "MATCH (g:Grupo{grupo_id: '" + grupo.grupo_id + "'})-[r]->() DELETE r, g"
    session.run(query)

#Programa
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