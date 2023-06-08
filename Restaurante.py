from UsuarioAux import UsuarioAux

class Restaurante:
        
    def __init__(self, restauranteId, session):
        self.Restaurante_id = restauranteId
        self.session = session
        self.name = self.getName(self.Restaurante_id)
        self.listaUsuarios = self.obtenerUsuarios(self.Restaurante_id)
        
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
    
    def obtenerUsuarios(self, restaurante_id):
        usuarios = []
        if(self.name != None):
            query = "MATCH (r:Review{business_id: '" + restaurante_id + "'})-[:Propietario]->(u) return r.user_id, apoc.agg.maxItems(r.stars, 5)"
            resultado = self.session.run(query)
            if (resultado.peek() is None):
                pass
            else:
                for i in resultado:
                    i = str(i)
                    i = i[19:41]
                    userAux = UsuarioAux(i, self.session)
                    if(userAux.existeUsuario):
                        usuarios.append(userAux)
        return usuarios
