class Usuario:

    def __init__(self, userId, session):
        self.user_id = userId
        self.session = session
        self.user = self.obtenerNodo()
        if self.user is not None:
            self.name = self.user.get("name")
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
        query = "MATCH (u:Usuario{user_id: '" + self.user_id + "'})-[:FRIEND]->(a) RETURN a"
        result = self.session.run(query)
        while result.peek():
            record = result.__next__()
            node = record["a"]
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

    def existeUsuario(self):
        return self.user is not None