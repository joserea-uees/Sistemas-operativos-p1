class Usuario:
    def __init__(self, nombre: str, idUsuario: int):
        self.nombre = nombre
        self.idUsuario = idUsuario
        self.librosPrestados = []

    def solicitarPrestamo(self, biblioteca, tituloLibro: str):
        biblioteca.prestarLibro(self, tituloLibro)

    def devolverLibro(self, biblioteca, tituloLibro: str):
        biblioteca.devolverLibro(self, tituloLibro)