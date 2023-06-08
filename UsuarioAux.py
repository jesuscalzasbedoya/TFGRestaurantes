from Review import Review
class UsuarioAux:

    def __init__(self, userId, session):
        self.user_id = userId
        self.session = session
        self.listaReviewsInicializadas = []
        self.name = self.getName(self.user_id)
        self.listaReviews = self.getReviews(self.user_id)


    def getName(self, userId):
        query = "MATCH (u:Usuario{user_id:'" + userId + "'}) RETURN u.name"
        result = self.session.run(query)
        if (result.peek() is None):
            name = None
        else:
            for i in result:
                i = str(i)
                name = i[16:-2]
        return name
    
    
    def existeUsuario(self):
        existe = True
        if (self.name == None):
            existe = False
        return existe
    
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
    
    def perteneceReview(self,review):
        pertenece = False
        i=0
        while((pertenece == False) and (i<len(self.listaReviews))):
            if((self.listaReviews[i] == review)):
                pertenece = True
            i += 1
        return pertenece
    
    def restauranteReseniado(self, restauranteId):
        pertenece = False
        i=0
        while((pertenece == False) and (i<len(self.listaReviews))):
            if((self.listaReviewsInicializadas[i].restaurante_id == restauranteId)):
                pertenece = True
            i += 1
        return pertenece