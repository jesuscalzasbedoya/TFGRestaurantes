class Review:
    
    def __init__(self, reviewId, session):
        self.review_id = reviewId
        self.session = session
        self.user_id = self.getUserId(self.review_id) 
        self.restaurante_id = self.getRestauranteId(self.reviewId) 
        self.stars = self.getStars(self.reviewId)

    #Obtener review.user_id de la BBDD
    def getUserId(self, reviewId):
        query = "MATCH (r:Review{review_id:'" + reviewId + "'}) RETURN r.user_id"
        result = self.session.run(query)
        if (result.peek() is None):
            userid = None
        else:
            for i in result:
                i = str(i)
                userid = i[19:-2]
        return userid

    #Obtener review.user_id de la BBDD
    def getRestauranteId(self, reviewId):
        query = "MATCH (r:Review{review_id:'" + reviewId + "'}) RETURN r.business_id"
        result = self.session.run(query)
        if (result.peek() is None):
            restauranteid = None
        else:
            for i in result:
                i = str(i)
                restauranteid = i[23:-2]
        return restauranteid

    #Obtener review.business_id de la BBDD
    def getStars(self, reviewId):
        query = "MATCH (r:Review{review_id:'" + reviewId + "'}) RETURN r.stars"
        result = self.session.run(query)
        if (result.peek() is None):
            stars = None
        else:
            for i in result:
                i = str(i)
                estrellas = i[17:-2]
                stars = int(estrellas)
        return stars
                

    