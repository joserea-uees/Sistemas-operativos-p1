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

    def agregarLibro(self, libro: Libro):
        self.inventario[libro.titulo] = libro.copiasDisponibles

    def prestarLibro(self, usuario: Usuario, titulo: str):
        with self.lock:  # Sección crítica protegida
            if titulo in self.inventario and self.inventario[titulo] > 0:
                self.inventario[titulo] -= 1
                usuario.librosPrestados.append(titulo)
                self.historial.append({
                    "usuario": usuario.nombre,
                    "libro": titulo,
                    "accion": "prestamo",
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                print(f"{usuario.nombre} prestó {titulo}. Copias restantes: {self.inventario[titulo]}")
            else:
                print(f"{usuario.nombre} no pudo prestar {titulo}: No disponible.")