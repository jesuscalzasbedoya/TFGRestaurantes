import math

from Restaurante import Restaurante

class Algoritmo:

    def __init__(self, session):
        self.session = session

    def similitud(self, grupo, usuario):
        arriba = 0
        abajo1 = 0
        abajo2 = 0

        query = "MATCH (g:Grupo{grupo_id: '" + grupo.grupo_id + "'})-[grev:GReviews]->(gr:Restaurante) MATCH (u:Usuario{user_id: '" + usuario[0] + "'})-[urev:Reviews]->(ur:Restaurante) WHERE ur.business_id = gr.business_id RETURN grev.stars as vGrupo, urev.stars as vUsuario"
        reviews = []
        result = self.session.run(query)
        while result.peek():
            record = result.__next__()
            vGrupo = record["vGrupo"]
            vUsuario = record["vUsuario"]
            tupla = (vGrupo, vUsuario)
            reviews.append(tupla)

        for r in reviews:
            a = r[0] - grupo.valoracionMedia
            b = r[1] - usuario[1]    #Si las estrellas y la valoración media es la misma, se divide entre 0
            if(a == 0):
                a = 0.01
            if(b == 0):
                b = 0.01
            arriba += a*b

            abajo1 += pow(a,2)
            abajo2 += pow(b,2)
        
        abajo1 = math.sqrt(abajo1)*math.sqrt(abajo2)

        return usuario, arriba/abajo1

    def prediccion(self, grupo, usuario): #Usuario (usuario[0][0] = id, usuario[0][1] = media y usuario[1] = similitud
        query = "MATCH (g:Grupo{grupo_id : '" + grupo.grupo_id + "'})-[:GReviews]->(ra:Restaurante) MATCH (g:Grupo{grupo_id : '" + grupo.grupo_id + "'})-[:GDescartados]->(rd:Restaurante) WITH COLLECT(ra.business_id) AS rAceptados, COLLECT(rd.business_id) AS rDescartados  MATCH (c:Usuario{user_id: '" + usuario[0][0] + "'})-[rev:Reviews]->(r:Restaurante) WHERE NOT r.business_id IN rAceptados AND NOT r.business_id IN rDescartados RETURN r.business_id as restauranteId, rev.stars as stars"
        lista = []
        result = self.session.run(query)
        while result.peek():
            record = result.__next__()
            restaurante_id = record["restauranteId"]
            valoracion = record["stars"]
            valoracion -= usuario[0][1]
            p = (usuario[1] * valoracion) + grupo.valoracionMedia
            tupla = (restaurante_id, p)
            lista.append(tupla)
        #Cuidado, porque puede ser que necesite crear nuevos valores porque de error
        lista = sorted(lista, key=lambda x: x[1], reverse=True)
        lista = lista[:5]
        return lista

    def usuariosAfines(self,grupo):
        lista = []
        query = "OPTIONAL MATCH (g:Grupo{grupo_id: '" + grupo.grupo_id + "'})-[:GReviews]->(r:Restaurante) OPTIONAL MATCH (gr:Grupo{grupo_id: '" + grupo.grupo_id + "'})-[:GDescartados]->(rd:Restaurante) WITH collect(r.business_id) AS aceptados, collect(rd.business_id) AS descartados MATCH (r1:Restaurante)<-[:Reviews]-(u)-[:Reviews]->(r2:Restaurante) WHERE r1.business_id IN aceptados AND (NOT r2.business_id IN aceptados AND NOT r2.business_id IN descartados) WITH u.user_id AS uid, count(DISTINCT r2) AS rDif, aceptados, descartados MATCH (u:Usuario)-[:Reviews]->(r:Restaurante) WHERE u.user_id IN uid AND (r.business_id IN aceptados OR r.business_id IN descartados) WITH u.user_id AS userId, count(DISTINCT r) AS rComun, rDif MATCH (u:Usuario)-[rev:Reviews]->(r:Restaurante) WHERE u.user_id IN userId WITH u.user_id AS uid, avg(rev.stars) AS media, rComun, rDif ORDER BY rComun DESC, rDif DESC LIMIT 20 RETURN uid, media"
        result = self.session.run(query)
        while result.peek():
            record = result.__next__()
            user_id = record["uid"]
            media = float(record["media"])
            tupla = (user_id, media)
            lista.append(tupla)
        return lista