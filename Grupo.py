from Usuario import Usuario
from Review import Review

class Grupo:

    def __init__(self, listaUsuarios, session):
        self.listaUsuarios = listaUsuarios
        self.session = session
        self.listaReviews = []
        for u in self.listaUsuarios:
            usuario = Usuario(u, self.session)
            for r in usuario.listaReviews:
                review = Review(r, session)
                self.listaReviews += review
                self.valoracionMedia += review.stars
        self.valoracionMedia = self.valoracionMedia/len(self.listaReviews)
    
    def actualizarRestaurantes(self, review):
        val = review.stars
        self.listaReviews += review
        self.valoracionMedia = (self.valoracionMedia*((len(self.listaReviews))-1)/len(self.listaReviews)) + val*(1/len(self.listaReviews))