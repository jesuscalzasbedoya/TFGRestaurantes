import math

class Algoritmo:

    def __init__(self):
        pass

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
        p = similitud * (usuario.getValoracion(restaurante) - usuario.valoracionMedia)
        return grupo.mediaValoracciones + p

    def jaccard(self,grupo, usuario):
        iguales = 0
        total = len(grupo.listaFinal) + len(usuario.listaReviews)
        for r in grupo.listaFinal:
            if (usuario.restauranteReseniado(r.restaurante_id)):
                iguales += 1
        total = total - iguales
        return iguales/total
