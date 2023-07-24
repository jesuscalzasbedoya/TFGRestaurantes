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

#ciudades = obtenerCiudades()

#Funciones

def obtenerAmigos(user_id, session):
    user = Usuario(user_id, session)
    amigos = []
    if(len(user.friends) > 0):
        for amigo in user.friends:
            a = (amigo.get("user_id"), amigo.get("name"))
            amigos.append(a)
    return amigos        

#No comprueba que no se haya introducido ya el amigo, pero con la interfaz lo arreglaré
"""
def SeleccionarAmigos(user):
    amigosSeleccionados = []
    print("Selecciona a los amigos: ")
    nombres = nombreAmigos()
    if(len(user.friends) > 0):
        todosAmigos = False
        print ("Introduce el Nº del amigo que quieres añadir(Fin = Ya): ")
        while(todosAmigos == False):
            amigoSeleccionado = input()
            if(amigoSeleccionado != "Ya"):
                amigoSeleccionado = int(amigoSeleccionado)
                if(amigoSeleccionado<=len(nombres)):
                    amigosSeleccionados.append(user.friends[amigoSeleccionado-1].get("user_id"))
            else:
                todosAmigos = True
    amigosSeleccionados.append(user.user_id)
    return amigosSeleccionados
"""
"""
def SeleccionarCiudad():
    repetir = True
    while(repetir):
        print("Elige la ciudad en la que quieras que esté el restaurante: ")
        print (ciudades)
        ciudad = input()
        if (ciudades.count(ciudad)>0):
            repetir = False
        else:
            print("La ciudad introducida es erronea")
    return ciudad

def repetirRecomendacion():
    valida = False
    while(valida == False):
        print("Recomendar de nuevo S/N")
        respuesta = input()
        if(respuesta == 'S'): 
            elegir = True
            valida = True
        elif (respuesta == 'N'):
            elegir = False
            valida = True
    return elegir
"""
def sanearRestaurantes(listaPred, session):
    listaRest = []
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
            tupla = (Restaurante(i[0], session), prediccion/apariciones)
            listaRest.append(tupla)
    return listaRest


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

"""
idCorrecto = False
while(idCorrecto == False):
    print("Introduce tu userId: ")
    idUsuario = input()                                            #####################################
    #idUsuario = 'u1'
    #print(idUsuario)
    user = Usuario(idUsuario, session)
    if(user.existeUsuario() == False):
        print("El id introducido es erroneo")
    else:
        idCorrecto = True
"""

#Elegir amigos
"""
elegir = True
while (elegir == True):   
    #Selecciona los amigos a los que hacer la recomendación
    seleccionados=[]
    while(len(seleccionados)==0 and len(user.friends)>0):
        seleccionados = SeleccionarAmigos()                        #####################################
        #seleccionados = ["1", "Ya"]
    #Seleccionar el estado
    ciudad = ""
    while (len(ciudad)==0): 
        ciudad = SeleccionarCiudad()                                      #####################################
        #ciudad = "Zionsville"
        #print(ciudad)

    print("Amigos seleccionados: ")
    for s in seleccionados:
        print(" - ", s)
    print("Ciudad seleccionada:", ciudad)
    print(seleccionados)
"""

def generarRecomendacion(seleccionados, session):
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

    listaRestaurantes = sanearRestaurantes(listaPredicciones)

    eliminarGrupo(grupo)
    return listaRestaurantes
#elegir = False
#elegir = repetirRecomendacion()                            #####################################
    

