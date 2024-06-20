import mainCodigo
from Usuario import Usuario

def comprobarId(idUsuario, session):
    idCorrecto = False
    user = Usuario(idUsuario, session)
    if(user.existeUsuario() == True):
        idCorrecto = True
    return idCorrecto

def obtenerAmigos (user_id, session):
    amigos = mainCodigo.obtenerAmigos(user_id, session)
    return amigos

def obtenerCiudades(user_id, session):
    ciudades = mainCodigo.obtenerCiudades(user_id, session)
    return ciudades

def obtenerRestaurantes(amigos, user_id, ciudad, session):
    amigos.append(user_id)
    restaurantes = mainCodigo.generarRecomendacion(amigos, ciudad, session)
    return restaurantes