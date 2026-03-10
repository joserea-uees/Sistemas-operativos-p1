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
                print(f"{usuario.nombre} tomo prestado {titulo}. Copias restantes: {self.inventario[titulo]}")
            else:
                print(f"{usuario.nombre} no pudo prestar {titulo}: No disponible.")

    def devolverLibro(self, usuario: Usuario, titulo: str):
        with self.lock:  # Sección crítica protegida
            if titulo in usuario.librosPrestados:
                self.inventario[titulo] += 1
                usuario.librosPrestados.remove(titulo)
                self.historial.append({
                    "usuario": usuario.nombre,
                    "libro": titulo,
                    "accion": "devolucion",
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                print(f"{usuario.nombre} devolvió {titulo}. Copias ahora: {self.inventario[titulo]}")
            else:
                print(f"{usuario.nombre} no tiene {titulo} para devolver.")

    def mostrarHistorial(self):
        for entrada in self.historial:
            print(entrada)


def main():
    biblioteca = Biblioteca()
    
    # Agregar libros de ejemplo
    libro1 = Libro("El Quijote Digital", "Cervantes", 3)
    libro2 = Libro("Cien Años de Soledad Digital", "García Márquez", 2)
    biblioteca.agregarLibro(libro1)
    biblioteca.agregarLibro(libro2)
    
    # Crear usuarios
    usuario1 = Usuario("José Rea", 1)
    usuario2 = Usuario("Cristhian Guaman", 2)
    usuario3 = Usuario("Enma Castelo", 3)
    
    # Simular concurrencia con hilos
    def hiloUsuario1():
        usuario1.solicitarPrestamo(biblioteca, "El Quijote Digital")
        time.sleep(0.5)
        usuario1.devolverLibro(biblioteca, "El Quijote Digital")
    
    def hiloUsuario2():
        usuario2.solicitarPrestamo(biblioteca, "El Quijote Digital")
        usuario2.solicitarPrestamo(biblioteca, "Cien Años de Soledad Digital")
    
    def hiloUsuario3():
        usuario3.solicitarPrestamo(biblioteca, "El Quijote Digital")
    
    threads = [
        threading.Thread(target=hiloUsuario1),
        threading.Thread(target=hiloUsuario2),
        threading.Thread(target=hiloUsuario3)
    ]
    
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()
    
    print("\nHistorial final de la biblioteca:")
    biblioteca.mostrarHistorial()
    
    print("\nInventario final:")
    for titulo, copias in biblioteca.inventario.items():
        print(f"{titulo}: {copias} copias disponibles")


if __name__ == "__main__":
    main()