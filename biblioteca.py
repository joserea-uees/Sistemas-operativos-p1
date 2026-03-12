import threading
import time
from datetime import datetime


class Libro:
    def __init__(self, titulo: str, autor: str, copiasDisponibles: int):
        self.titulo = titulo
        self.autor = autor
        self.copiasDisponibles = copiasDisponibles


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
        self.inventario = {}           # Recurso compartido: dict[str, int]
        self.historial = []            # Recurso compartido: list[dict]
        self.lock = threading.Lock()   # Mutex para proteger secciones críticas

    def agregarLibro(self, libro: Libro):
        self.inventario[libro.titulo] = libro.copiasDisponibles

    def prestarLibro(self, usuario: Usuario, titulo: str):
        with self.lock:
            if titulo in self.inventario and self.inventario[titulo] > 0:
                self.inventario[titulo] -= 1
                usuario.librosPrestados.append(titulo)
                self.historial.append({
                    "usuario": usuario.nombre,
                    "libro": titulo,
                    "accion": "préstamo",
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                print(f"{usuario.nombre} tomó prestado '{titulo}'. Copias restantes: {self.inventario[titulo]}")
            else:
                print(f"{usuario.nombre} no pudo prestar '{titulo}': No disponible")

    def devolverLibro(self, usuario: Usuario, titulo: str):
        with self.lock:
            if titulo in usuario.librosPrestados:
                self.inventario[titulo] += 1
                usuario.librosPrestados.remove(titulo)
                self.historial.append({
                    "usuario": usuario.nombre,
                    "libro": titulo,
                    "accion": "devolución",
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                print(f"{usuario.nombre} devolvió '{titulo}'. Copias ahora: {self.inventario[titulo]}")
            else:
                print(f"{usuario.nombre} no tiene '{titulo}' para devolver")

    def mostrarHistorial(self):
        if not self.historial:
            print("No hay registros en el historial aún.")
            return
        
        print("Historial de movimientos:")
        print("-" * 60)
        for entrada in self.historial:
            print(f"{entrada['fecha']} | {entrada['usuario']:12} | {entrada['accion']:10} | {entrada['libro']}")
        print("-" * 60)


def main():
    print("=== SISTEMA DE BIBLIOTECA DIGITAL - Préstamos concurrentes ===\n")
    
    biblioteca = Biblioteca()
    
    # Libros de ejemplo
    libros = [
        Libro("El Quijote Digital", "Miguel de Cervantes", 3),
        Libro("Cien Años de Soledad Digital", "Gabriel García Márquez", 2),
        Libro("1984 Digital", "George Orwell", 1),
        Libro("Rayuela Digital", "Julio Cortázar", 4)
    ]
    
    for libro in libros:
        biblioteca.agregarLibro(libro)
        print(f"Libro agregado: {libro.titulo} ({libro.copiasDisponibles} copias)")
    
    print("\nUsuarios registrados:")
    usuarios = [
        Usuario("José Rea", 1),
        Usuario("Cristhian Guaman", 2),
        Usuario("Enma Castelo", 3),
        Usuario("Allan Avendaño", 4)
    ]
    
    for u in usuarios:
        print(f"(ID: {u.idUsuario}) {u.nombre} ")
    
    print("\nSimulación concurrente\n")
    
    # Acciones para cada usuario
    acciones = {
        "José Rea": [
            {"tipo": "prestamo", "titulo": "El Quijote Digital"},
            {"tipo": "prestamo", "titulo": "Cien Años de Soledad Digital"},
            {"tipo": "devolucion", "titulo": "El Quijote Digital"}
        ],
        "Cristhian Guaman": [
            {"tipo": "prestamo", "titulo": "El Quijote Digital"},
            {"tipo": "prestamo", "titulo": "1984 Digital"}
        ],
        "Enma Castelo": [
            {"tipo": "prestamo", "titulo": "Rayuela Digital"}
        ],
        "Allan Avendaño": [
            {"tipo": "devolucion", "titulo": "El Quijote Digital"}  # Intento de devolución sin haberlo prestado
        ]
    }
    
    # Hilos
    hilos = []
    for usuario in usuarios:
        nombre = usuario.nombre
        if nombre in acciones and acciones[nombre]:
            hilo = threading.Thread(
                target=lambda u=usuario, acc=acciones[nombre]: 
                    [u.solicitarPrestamo(biblioteca, a["titulo"]) if a["tipo"] == "prestamo" else 
                     u.devolverLibro(biblioteca, a["titulo"]) or time.sleep(0.4) 
                     for a in acc]
            )
            hilos.append(hilo)
    
    # Iniciar todos los hilos
    for hilo in hilos:
        hilo.start()
    
    # Esperar a que terminen
    for hilo in hilos:
        hilo.join()
    
    # Resultados finales
    print("\n" + "="*70)
    print("                      SIMULACIÓN FINALIZADA")
    print("="*70)
    
    biblioteca.mostrarHistorial()
    
    print("\nInventario final:")
    print("-" * 50)
    for titulo, copias in biblioteca.inventario.items():
        print(f"{titulo:35} : {copias:2} copias disponibles")
    print("-" * 50)

if __name__ == "__main__":
    main()