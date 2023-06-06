class Review:
    
    def __init__(self, review_id, session):
        self.review_id = review_id
        self.session = session
        self.user_id = self.getUserId(self.review_id) 
        self.restaurante_id = self.getRestauranteId(self.review_id) 
        self.stars = self.getStars(self.review_id)

    #Obtener review.user_id de la BBDD
    def getUserId(self, review_id):
        query = "MATCH (r:Review{review_id:'" + review_id + "'}) RETURN r.user_id"
        result = self.session.run(query)
        if (result.peek() is None):
            userid = None
        else:
            for i in result:
                i = str(i)
                userid = i[19:-2]
        return userid

    #Obtener review.user_id de la BBDD
    def getRestauranteId(self, review_id):
        query = "MATCH (r:Review{review_id:'" + review_id + "'}) RETURN r.business_id"
        result = self.session.run(query)
        if (result.peek() is None):
            restauranteid = None
        else:
            for i in result:
                i = str(i)
                restauranteid = i[23:-2]
        return restauranteid

    #Obtener review.business_id de la BBDD
    def getStars(self, review_id):
        query = "MATCH (r:Review{review_id:'" + review_id + "'}) RETURN r.stars"
        result = self.session.run(query)
        if (result.peek() is None):
            stars = None
        else:
            for i in result:
                i = str(i)
                estrellas = i[17:-2]
                stars = int(estrellas)
        return stars
                

    