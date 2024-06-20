class Grupo:

    def __init__(self, listaUsuarios, session):
        self.listaUsuarios = listaUsuarios
        self.session = session
        self.valoracionMedia = self.obtenerValoracionMedia()       #Obtener valoracion media de $seed
        self.grupo_id = self.crearId()
        self.crearNodo()


    def obtenerValoracionMedia(self):          
        query = "MATCH (u:Usuario)-[rev:Reviews]->(r:Restaurante) WHERE u.user_id in $listaUsuarios RETURN avg(rev.stars) as mediaGrupo"
        result = self.session.run(query, listaUsuarios = self.listaUsuarios)
        record = result.single()
        return float(record.get("mediaGrupo"))
    
    def crearId(self):
        id = ""
        for i in self.listaUsuarios:
            id += str(i)
        return id
        
    def crearNodo(self):
        query = "MERGE (g:Grupo{grupo_id: '" + self.grupo_id + "'})"
        self.session.run(query)
        query = "MATCH (s:Usuario)-[rev:Reviews]->(r:Restaurante) WHERE s.user_id IN $listaUsuarios AND rev.stars <= 2 WITH collect(r.business_id) AS restaurantes1 MATCH (s:Usuario)-[rev:Reviews]->(r:Restaurante) WHERE s.user_id IN $listaUsuarios AND NOT r.business_id IN restaurantes1 WITH r.business_id AS restaurante_id, avg(rev.stars) AS media WITH collect({restaurante_id: restaurante_id, media: media}) AS restaurantesFinales MATCH (g:Grupo {grupo_id: '" + self.grupo_id + "'}) UNWIND restaurantesFinales AS r MATCH (rest:Restaurante) WHERE rest.business_id = r.restaurante_id MERGE (g)-[:GReviews {stars: r.media}]->(rest)"
        self.session.run(query, listaUsuarios = self.listaUsuarios)
        query = "MATCH (g:Grupo {grupo_id: '" + self.grupo_id + "'})-[:GReviews]->(rrev:Restaurante) WITH g, collect(rrev.business_id) AS restaurantesRevision MATCH (s:Usuario)-[:Reviews]->(r:Restaurante) WHERE s.user_id IN $listaUsuarios AND NOT r.business_id IN restaurantesRevision MERGE (g)-[:GDescartados]->(r)"
        self.session.run(query, listaUsuarios = self.listaUsuarios)

    def obtenerRestaurantes(self):
        restaurantes = []
        query = "MATCH (g:Grupo {grupo_id: '" + self.grupo_id + "'})-[:GReviews]->(rrev:Restaurante) RETURN rrev.business_id as restaurante_id, rrev.city as ciudad"
        result = self.session.run(query)
        while result.peek():
            record = result.__next__()
            id = record["restaurante_id"]
            ciudad = record["ciudad"]
            restaurantes.append((id, ciudad))
        return restaurantes
