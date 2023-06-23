import math

class Algoritmo:

    def __init__(self, session):
        self.session = session

    def similitud(self, grupo, usuario):
        arriba = 0
        abajo1 = 0
        abajo2 = 0

        for r in grupo.listaFinal:
            if (usuario.restauranteReseniado(r.restaurante_id)):
                a = r.stars - grupo.valoracionMedia
                b = usuario.getReview(r.restaurante_id).stars - usuario.valoracionMedia    #Si las estrellas y la valoración media es la misma, se divide entre 0
                if(a == 0):
                    a = 0.01
                if(b == 0):
                    b = 0.01
                arriba += a*b

                abajo1 += pow(a,2)
                abajo2 += pow(b,2)
        
        abajo1 = math.sqrt(abajo1)*math.sqrt(abajo2)

        return arriba/abajo1

    def prediccion(self, grupo, usuario, restaurante, similitud):
        valoracion = usuario.getReview(restaurante.restaurante_id).stars - usuario.valoracionMedia
        if(valoracion == 0):
            valoracion = 0.01
        p = similitud * valoracion    #Que pasaria si la valoracion del restaurante y la valoracion media es la misma
        return grupo.valoracionMedia + p

    def usuariosAfines(self,grupo):
        lista = []
        query = "MATCH (s:Usuario)-[rev:Reviews]->(r:Restaurante) WHERE s.user_id in " + str(grupo.listaUsuarios) + " AND rev.stars <= 2 WITH collect(r.business_id) as restaurantes1 MATCH (s:Usuario)-[rev:Reviews]->(r:Restaurante) WHERE s.user_id in " + str(grupo.listaUsuarios) + " AND NOT r.business_id in restaurantes1 WITH collect(r.business_id) as restaurantes2, restaurantes1 as rDescartados MATCH(r1:Restaurante)<-[:Reviews]-(u)-[:Reviews]->(r2:Restaurante) WHERE r1.business_id in restaurantes2 AND (NOT r2.business_id in restaurantes2 AND NOT r2.business_id in rDescartados) WITH  u.user_id as user_id , count(r1) as rComun, count(r2) as rDif ORDER BY rComun DESC, rDif DESC LIMIT 20 RETURN user_id"
        result = self.session.run(query)
        while result.peek():
            record = result.__next__()
            user_id = record["user_id"]
            lista.append(user_id)
        return lista
