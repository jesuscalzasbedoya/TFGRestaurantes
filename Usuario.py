from UsuarioAux import UsuarioAux 
from Review import Review

class Usuario:

    def __init__(self, userId, session):
        self.user_id = userId
        self.session = session
        user = self.obtenerNodo()
        if user != None:
            self.name = user.get("name")
            self.friends = self.getAmigos()
            self.valoracionMedia = self.getValoracionMedia()

    def obtenerNodo(self):
        query = "MATCH (u:Usuario{user_id:'" + self.user_id + "'}) RETURN u"
        result = self.session.run(query)
        record = result.single()
        if record:
            nodo = record["u"]
        else:
            nodo = None
        return nodo

    def getAmigos(self):
        lista = []
        query = "MATCH (u:Usuario{user_id: '" + self.user_id + "'})-[r:Reviews]->() RETURN r"
        result = self.session.run(query)
        while result.peek():
            record = result.__next__()
            node = record["r"]
            lista.append(node)
        return lista
    
    def getValoracionMedia(self):
        media = 0
        query = "MATCH (u:Usuario{user_id: '" + self.user_id + "'})-[r:Reviews]->() RETURN avg(toInteger(r.stars)) as a"
        result = self.session.run(query)
        while result.peek():
            record = result.__next__()
            node = record["a"]
            media = node
        return media



    def getReviews(self, userId):
        reviews = []
        if(self.name != None):
            query = "MATCH (u:Usuario{user_id: '" + userId + "'})-[:Escribe]->(r) return r.review_id"
            resultado = self.session.run(query)
            if (resultado.peek() is None):
                pass
            else:
                for i in resultado:
                    i = str(i)
                    i = i[21:-2]
                    review = Review(i, self.session)
                    reviews.append(i)
                    self.listaReviewsInicializadas.append(review)
        return reviews
    
    def getValoracion(self, restaurante_id):
        encontrado = False
        i = 0
        while(encontrado == False & i<len(self.listaReviews)):
            if(self.listaReviews[i].restaurante_id == restaurante_id):
                encontrado = True
            else: 
                i+=1
        return self.listaReviews[i].stars
    
    def existeUsuario(self):
        existe = False
        if (self.name != None):
            existe = True
        return existe