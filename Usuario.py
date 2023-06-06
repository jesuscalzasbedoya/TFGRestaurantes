from UsuarioAux import UsuarioAux 

class Usuario:

    def __init__(self, userId, session):
        self.user_id = userId
        self.session = session
        self.name = self.getName(self.user_id)
        self.friends = self.getAmigos(self.user_id)
        self.listaReviews = self.getReviews(self.user_id)
        #self.valoracionMedia = self.getValoracionMedia()
        self.listaUsuarios = self.getUsuarios()
        
        """
        for r in "" :     
            pass   
        
            Inicializar listaRestaurantes
            Obtener reviews de la BBDD
            De cada review hay que obtener el restaurante al que se refiere
            Tras eso, se añade a la lista de restaurantes


            Dudo que sea necesario, ¡¡¡REVISAR!!!
        """

    def perteneceReview(self,review):
        pertenece = False
        i=0
        while(pertenece == False):
            pertenece = self.listaReviews[i].equals(review)
            i += 1
        return pertenece
    
    def getReview(self, review_id):
        encontrado = False
        i = 0
        while(encontrado == False & i<len(self.listaReviews)):
            if(self.listaReviews[i].review_id.equals(review_id)):
                encontrado = True
            else: i+=1
        return self.listaReviews[i]
        
    def getValoracion(self, restaurante_id):
        encontrado = False
        i = 0
        while(encontrado == False & i<len(self.listaReviews)):
            if(self.listaReviews[i].restaurante_id.equals(restaurante_id)):
                encontrado = True
            i+=1
        return self.listaReviews[i].stars

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

    def getAmigos(self, userId):
        amigos = []
        fin = False
        query = "MATCH (u:Usuario{user_id:'" + userId + "'}) RETURN u.friends"
        resultado = self.session.run(query)
        if (resultado.peek() is None):
            pass
        else:
            usuarios = ""
            for i in resultado:
                i = str(i)
                i = i[19:-2]
                usuarios += i

            while(fin == False):
                aux = usuarios[:22]
                userAux = UsuarioAux(aux, self.session)
                if(userAux.existeUsuario() == True):
                    amigos.append(aux)
                if(len(usuarios)-24 >= 22):
                    usuarios = usuarios[24:]
                else:
                    fin = True
        return amigos
    
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
                    reviews.append(i)
        return reviews
    
    def getValoracionMedia(self):
        valoracionTotal = 0
        if(self.name != None):
            for review in self.listaReviews:
                valoracionTotal += review.stars
            if (len(self.listaReviews) != 0):
                valoracionTotal = valoracionTotal/len(self.listaReviews)
        return valoracionTotal
    
    def existeUsuario(self):
        existe = False
        if (self.name != None):
            existe = True
        return existe
    
    def escribir(self):
        print(self.name)
        print(self.listaReviews)
        print(self.friends)
        print(self.user_id)
        print(self.valoracionMedia)
    
    def getUsuarios(self):
        usuarios = []
        for u in self.friends:
            aux = UsuarioAux(u, self.session)
            usuarios.append(aux)
        return usuarios