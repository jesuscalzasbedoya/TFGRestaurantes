''' 
------------LEAVE ONE OUT CROSS VALIDATION (LOO-VC)------------
'''
import json
from neo4j import GraphDatabase
from Algoritmos import Algoritmo
from Usuario import Usuario
from Grupo import Grupo
from Restaurante import Restaurante

# Conexión BBDD
url = "bolt://localhost:7687"
driver = GraphDatabase.driver(url, auth=("neo4j", "12345678"))
session = driver.session()

algoritmo = Algoritmo(session)
usuariosRandom = []
usuariosUsados = 0
iteraciones = 0
restaurantesComprobados = 0
estrellasBorradas = 0.0
restaurantesCorrectos = 0
porcentajeTotal = 0.0
archivoResultados = 'resultados.json'

def obtenerUsuariosRandom():
    usuarios = []
    query = "MATCH (u:Usuario)-[:FRIEND]->(u2:Usuario), (u)-[:Reviews]->(r:Restaurante) RETURN DISTINCT u.user_id as user_id LIMIT 1000"
    result = session.run(query)
    while result.peek():
        record = result.__next__()
        user_id = record["user_id"]
        usuarios.append(user_id)
    return usuarios

def crearGrupo(user):
    listaGrupo = []
    amigos = user.friends
    for a in amigos:
        listaGrupo.append(a.get("user_id"))
    listaGrupo.append(user.user_id)
    grupo = Grupo(listaGrupo, session)
    return grupo

def eliminarResenia(grupo, r):
    parameters = {
        'grupo_id': grupo.grupo_id,
        'business_id': r,
    }
    query = """MATCH (:Grupo {grupo_id: $grupo_id})
               -[rev:GReviews]->(:Restaurante {business_id: $business_id}) 
               RETURN rev.stars as stars"""
    result = session.run(query,parameters)
    while result.peek():
        record = result.__next__()
        global estrellasBorradas
        estrellasBorradas = record["stars"]
    query = "MATCH (g:Grupo{grupo_id:'" + grupo.grupo_id + "'})-[gr:GReviews]->(r:Restaurante{business_id:'" + r + "'}) DELETE gr"
    session.run(query)

def aniadirResenia(grupo, r):
    parameters = {
        'grupo_id': grupo.grupo_id,
        'business_id': r,
        'estrellasBorradas': estrellasBorradas
    }
    query = """MATCH (g:Grupo {grupo_id: $grupo_id})
        MATCH (r:Restaurante {business_id: $business_id})
        CREATE (g)-[:GReviews {stars: $estrellasBorradas}]->(r)"""
    session.run(query, parameters)

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
        if i[0].ciudad == ciudad[0] or i[0].ciudad == ciudad:
            tupla = (i[0].restaurante_id, i[1])
            listaFinal.append(tupla)
    listaFinal.sort(key=lambda x: x[1], reverse=True)  
    return listaFinal[:5]

def eliminarGrupo(grupo, session):
    query = "MATCH (g:Grupo{grupo_id: '" + grupo.grupo_id + "'})-[r]->() DELETE r, g"
    session.run(query)

########################
######## INICIO ########
########################

usuariosRandom  = obtenerUsuariosRandom()
with open(archivoResultados, 'w') as json_file:
    while iteraciones < 30:
        user = Usuario(usuariosRandom[usuariosUsados], session)
        usuariosUsados += 1
        grupo = crearGrupo(user)
        listaRestaurantes = []

        #Obtener usuarios afines
        usuariosAfines = []
        usuariosAfines = algoritmo.usuariosAfines(grupo)

        #Obtener similitud de los usuarios afines
        similitudes = []
        for i in usuariosAfines:
            similitudes.append(algoritmo.similitud(grupo, i))

        #Aquí se queda con los 10 usuarios más afines
        similitudes = sorted(similitudes, key=lambda tupla: tupla[1])
        similitudes = similitudes[:10]

        #Obtener restaurantes reseñados
        restGrupo = grupo.obtenerRestaurantes()
        
        for r in restGrupo:
            eliminarResenia(grupo, r[0])
            listaPredicciones = []
            listaRestaurantes = []
            encontrado = False
            j=0
            for i in similitudes:
                listaPredicciones += algoritmo.prediccion(grupo, i)
            listaRestaurantes = sanearRestaurantes(listaPredicciones, r[1], session)
            while (encontrado == False) and (j<len(listaRestaurantes)):
                if (r[0] == listaRestaurantes[j][0]):
                    encontrado = True
                    restaurantesCorrectos += 1
                j += 1
                #print("Grupo: " + grupo.grupo_id + " | Restaurante: " + r[0] + " | Aparece: " + str(encontrado))
            aniadirResenia(grupo, r[0])
            restaurantesComprobados += 1
            if (restaurantesComprobados >= 50):
                porcentaje = round((restaurantesCorrectos/restaurantesComprobados)*100, 2)
                porcentajeTotal += porcentaje
                iteracion = {"Iteracion": str(iteraciones),"Apariciones": str(restaurantesCorrectos) + "/" + str(restaurantesComprobados), "Porcentaje de acierto": str(porcentaje) + "%"}
                json.dump(iteracion, json_file, indent=4)
                json_file.write("\n")
                print(iteracion)
                iteraciones += 1
                restaurantesComprobados = 0 
                restaurantesCorrectos = 0
            if (iteraciones == 30):
                break
        eliminarGrupo(grupo, session)

    final = {"Porcentaje total de acierto": str(porcentajeTotal/30) + "%"}
    json.dump(final, json_file)
    json_file.write("\n")      
print(final)

#("Apariciones en la iteración " + str(iteraciones) + ": " + str(restaurantesCorrectos) + "/" + str(restaurantesComprobados) + " | Porcentaje de acierto= " + str(porcentaje) + "%")