from neo4j import GraphDatabase
from Usuario import Usuario
from UsuarioAux import UsuarioAux
#Conexion a la base de datos

url = "bolt://localhost:7687"
driver = GraphDatabase.driver(url, auth=("neo4j", "12345678"))
session = driver.session()


userId = 'Q3Y0AjsTpuJuQ-TWZOlVzg'
reviewId = 'Sv_CnnR0FEnzXE4Xnm_RuA'
restauranteId = 'MTSW4McQd7CbVtyjqoe9mw'

"""
palabra = "abcdefghijklmnñopq"
palabras = []


while(fin == False):
    aux = palabra[:2]
    palabras.append(aux)
    if(len(palabra)-3 >= 2):
        palabra = palabra[3:]
    else:
        fin = True
for i in palabras:
    print(i)


amigos = []
fin = False
query = "MATCH (u:Usuario{user_id:'" + userId + "'}) RETURN u.friends"
resultado = session.run(query)
if (resultado.peek() is None):
    pass
else:
    usuarios = ""
    for i in resultado:
        i = str(i)
        i = i[19:-2]
        print(i)
        usuarios += i
    
    print(len(usuarios))

    while(fin == False):
        aux = usuarios[:22]
        amigos.append(aux)
        if(len(usuarios)-24 >= 22):
            usuarios = usuarios[24:]
        else:
            fin = True
    for w in amigos:
        print (w)
    print(len(amigos))
"""
"""

lista = [0, 1, 2, 3, 4, 5, 6, 7, 8]
i = 0
n = 2
for x in lista:
    if (i == 2):
        lista.pop (6)
    print(lista[i])
    i+=1

"""

"""
query = "MATCH (u:Usuario{user_id:'" + userId + "'}) RETURN u.name"
result = session.run(query)
if (result.peek() is None):
    name = None
else:
    for i in result:
        i = str(i)
        name = i[16:-2]
    print(name)


lista = []
query = "MATCH (r:Restaurante) RETURN r.city"
ciudades = session.run(query)
for i in ciudades:
    x = str(i)
    x = x[16:-2]
    if(lista.count(x) == 0):
        lista.append(x)

lista.sort()

print("Longitud: ", len(lista), " --> ", lista)
"""

x = UsuarioAux("yAslAaF6zzqgfV5xwye3jQ", session)
print (x.listaReviews)
session.close()
