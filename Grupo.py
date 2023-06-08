from Usuario import Usuario
from Review import Review

class Grupo:

    def __init__(self, listaUsuarios, session):
        self.listaUsuarios = listaUsuarios
        self.session = session
        self.listaReviews = []
        self.listaFinal = []
        self.listaReviews = self.inicializarReviews()
        self.listaFinal = self.sanearRestaurantes()                 #lista final de reviews
        self.valoracionMedia = self.calcularValoracionMedia()

        """
        Inicializar en un método diferente la lista de reviews
         - Obtener todas las reviews
         - Quitar las peores
         - Devolver la lista saneada
        Establecer la valoración media
        """
    
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
    
    def calcularValoracionMedia(self):
        valor = 0
        for r in self.listaFinal:
            valor += r.stars
        if(len(self.listaFinal) != 0):
            valor = valor/len(self.listaFinal)
        return valor