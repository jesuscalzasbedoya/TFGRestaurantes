from UsuarioAux import UsuarioAux

class Restaurante:
        
    def __init__(self, restauranteId, session):
        self.restaurante_id = restauranteId
        self.session = session
        restaurante = self.obtenerNodo()
        if restaurante != None:
            self.name = restaurante.get("name")
            self.ciudad = restaurante.get("city")
            self.direccion = restaurante.get("address")

    def obtenerNodo(self):
        query = "MATCH (r:Restaurante{business_id:'" + self.restaurante_id + "'}) RETURN r"
        result = self.session.run(query)
        record = result.single()
        if record:
            nodo = record["r"]
        else:
            nodo = None
        return nodo