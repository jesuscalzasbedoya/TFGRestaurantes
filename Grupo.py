from Usuario import Usuario
from Review import Review

class Grupo:

    def __init__(self, listaUsuarios, session):
        self.listaUsuarios = listaUsuarios
        self.session = session
        self.valoracionMedia = self.obtenerValoracionMedia()       #Obtener valoracion media de $seed


    def obtenerValoracionMedia(self):           #Modificar
        query = "MATCH (u:Usuario)-[rev:Reviews]->(r:Restaurante) WHERE u.user_id in $listaUsuarios RETURN avg(rev.stars) as mediaGrupo"
        result = self.session.run(query, listaUsuarios = self.listaUsuarios)
        record = result.single()
        return float(record.get("mediaGrupo"))
        




    def inicializarReviews(self):
        lista = []
        for u in self.listaUsuarios:
            for r in u.listaReviews:
                review = Review(r, self.session)
                lista.append(review)
        return lista
        
    
    def actualizarRestaurantes(self, review):
        val = review.stars
        self.listaReviews += review
        self.valoracionMedia = (self.valoracionMedia*((len(self.listaReviews))-1)/len(self.listaReviews)) + val*(1/len(self.listaReviews))

    def eliminarDuplicados(self, lista, review, repeticiones):
        valoracionAux = 0
        contador = 0
        indice = 0
        indice1 = 0
        rep = repeticiones
        while (repeticiones > 1):
            if(lista[indice].restaurante_id == review.restaurante_id):
                if(contador == 0):
                    contador += 1
                    indice1 = indice
                else:
                    r = lista.pop(indice)
                    valoracionAux += r.stars
                    repeticiones -= 1
            indice += 1
        valoracionAux += lista[indice1].stars
        lista[indice1].stars = (valoracionAux/rep)
        return lista


    def sanearRestaurantes(self):
        listaNegra = []
        listaAux = self.listaReviews
        lista = []
        contador = 0
        for r in self.listaReviews:
            if (r.stars<=2):
                if(listaNegra.count(r.restaurante_id)==0):
                    listaNegra.append(r.restaurante_id)
        for i in listaNegra:
            n = 0
            for j in listaAux:
                if(j.restaurante_id == i):
                    listaAux.pop(n)
                n += 1
        for i in listaAux:
            n = 0
            contadorAux = 0
            for j in listaAux:
                if(j.restaurante_id == i.restaurante_id):
                    contadorAux += 1
            if(contadorAux==1):
                lista.append(i)
            else:
                listaAux = self.eliminarDuplicados(listaAux, i, contadorAux)
                lista.append(listaAux[contador])
            contador += 1
        return lista
    
