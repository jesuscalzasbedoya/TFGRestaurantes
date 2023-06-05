class Restaurante:
        
    def __init__(self, restauranteId, session):
        self.Restaurante_id = restauranteId
        self.session = session
        self.name = self.getName(self.Restaurante_id)
        
    def getName(self, restauranteId):
        query = "MATCH (r:Restaurante{business_id:'" + restauranteId + "'}) RETURN r.name"
        result = self.session.run(query)
        if (result.peek() is None):
            name = None
        else:
            for i in result:
                i = str(i)
                name = i[16:-2]
        return name

