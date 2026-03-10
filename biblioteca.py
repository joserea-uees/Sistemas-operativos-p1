import threading
import time
from datetime import datetime

class Libro:
    def __init__(self, titulo: str, autor: str, copiasDisponibles: int):
        self.titulo = titulo
        self.autor = autor
        self.copiasDisponibles = copiasDisponibles  # Recurso básico compartido

class Usuario:
    def __init__(self, nombre: str, idUsuario: int):
        self.nombre = nombre
        self.idUsuario = idUsuario
        self.librosPrestados = []  # Lista personal, no compartida

    def solicitarPrestamo(self, biblioteca, tituloLibro: str):
        biblioteca.prestarLibro(self, tituloLibro)

    def devolverLibro(self, biblioteca, tituloLibro: str):
        biblioteca.devolverLibro(self, tituloLibro)

class Biblioteca:
    def __init__(self):
        self.inventario = {}           # dict[str, int]
        self.historial = []            # list[dict]
        self.lock = threading.Lock()   # Protección de secciones críticas
