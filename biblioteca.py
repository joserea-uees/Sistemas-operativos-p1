import threading
import time
import random
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
        self.contadorUsuarios = 0      # Para IDs automáticos de nuevos usuarios

    def agregarLibro(self, libro: Libro):
        self.inventario[libro.titulo] = libro.copiasDisponibles
        print(f"Libro agregado: {libro.titulo} ({libro.copiasDisponibles} copias)")

    def registrarBitacora(self, evento: str, usuario_nombre: str, titulo: str, copiasAntes=None, copiasDespues=None):
        """Registra eventos solo dentro de secciones críticas (con lock)"""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # con milisegundos
        linea = f"{ts} | {evento:14} | {usuario_nombre:15} | {titulo:35}"
        if copiasAntes is not None:
            linea += f" | antes: {copiasAntes:2}"
        if copiasDespues is not None:
            linea += f" | después: {copiasDespues:2}"
        linea += "\n"

        with open("bitacora.log", "a", encoding="utf-8") as f:
            f.write(linea)

    def prestarLibro(self, usuario: Usuario, titulo: str):
        with self.lock:
            self.registrarBitacora("ADQUIERE_LOCK", usuario.nombre, titulo)

            if titulo not in self.inventario:
                print(f"✗ '{titulo}' no existe en la biblioteca.")
                self.registrarBitacora("PRÉSTAMO_FALLIDO_NO_EXISTE", usuario.nombre, titulo)
                self.registrarBitacora("LIBERA_LOCK", usuario.nombre, titulo)
                return

            copiasAntes = self.inventario[titulo]
            self.registrarBitacora("COPIAS_ANTES", usuario.nombre, titulo, copiasAntes=copiasAntes)

            if copiasAntes > 0:
                self.inventario[titulo] -= 1
                usuario.librosPrestados.append(titulo)
                self.historial.append({
                    "usuario": usuario.nombre,
                    "libro": titulo,
                    "accion": "préstamo",
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                print(f"✓ {usuario.nombre} tomó prestado '{titulo}'. Copias restantes: {self.inventario[titulo]}")
                self.registrarBitacora("PRÉSTAMO_OK", usuario.nombre, titulo, copiasAntes, self.inventario[titulo])
            else:
                print(f"✗ {usuario.nombre} no pudo prestar '{titulo}': sin copias disponibles.")
                self.registrarBitacora("PRÉSTAMO_FALLIDO_SIN_COPIAS", usuario.nombre, titulo, copiasAntes)

            self.registrarBitacora("LIBERA_LOCK", usuario.nombre, titulo)

    def devolverLibro(self, usuario: Usuario, titulo: str):
        with self.lock:
            self.registrarBitacora("ADQUIERE_LOCK", usuario.nombre, titulo)

            if titulo not in usuario.librosPrestados:
                print(f"✗ {usuario.nombre} no tiene '{titulo}' prestado.")
                self.registrarBitacora("DEVOLUCIÓN_FALLIDA_NO_PRESTADO", usuario.nombre, titulo)
                self.registrarBitacora("LIBERA_LOCK", usuario.nombre, titulo)
                return

            copiasAntes = self.inventario.get(titulo, 0)
            self.registrarBitacora("COPIAS_ANTES", usuario.nombre, titulo, copiasAntes=copiasAntes)

            self.inventario[titulo] = copiasAntes + 1
            usuario.librosPrestados.remove(titulo)
            self.historial.append({
                "usuario": usuario.nombre,
                "libro": titulo,
                "accion": "devolución",
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            print(f"↩ {usuario.nombre} devolvió '{titulo}'. Copias ahora: {self.inventario[titulo]}")
            self.registrarBitacora("DEVOLUCIÓN_OK", usuario.nombre, titulo, copiasAntes, self.inventario[titulo])

            self.registrarBitacora("LIBERA_LOCK", usuario.nombre, titulo)

    def mostrarHistorial(self):
        if not self.historial:
            print("No hay registros en el historial aún.")
            return
        
        print("Historial de movimientos:")
        print("-" * 80)
        for entrada in self.historial:
            print(f"{entrada['fecha']} | {entrada['usuario']:18} | {entrada['accion']:10} | {entrada['libro']}")
        print("-" * 80)

    def mostrarInventario(self):
        if not self.inventario:
            print("No hay libros en el inventario.")
            return
        print("\nInventario actual:")
        print("-" * 60)
        for titulo, copias in sorted(self.inventario.items()):
            print(f"{titulo:40} : {copias:2} copias disponibles")
        print("-" * 60)


def simularConcurrencia(biblioteca, usuarios):
    print("\n=== Simulación concurrente iniciada ===\n")

    def acciones_usuario(u, secuencia):
        for accion, titulo in secuencia:
            if accion == "prestamo":
                u.solicitarPrestamo(biblioteca, titulo)
            else:
                u.devolverLibro(biblioteca, titulo)
            time.sleep(random.uniform(0.2, 0.7))  # variabilidad para mejor concurrencia

    hilos = []
    secuencias = [
        (usuarios[0], [("prestamo", "El Quijote Digital"), ("prestamo", "Cien Años de Soledad Digital"), ("devolucion", "El Quijote Digital")]),
        (usuarios[1], [("prestamo", "El Quijote Digital"), ("prestamo", "1984 Digital")]),
        (usuarios[2], [("prestamo", "Rayuela Digital")]),
        (usuarios[3], [("prestamo", "El Quijote Digital"), ("devolucion", "El Quijote Digital")])
    ]

    for u, seq in secuencias:
        if seq:  # solo si hay acciones
            h = threading.Thread(target=acciones_usuario, args=(u, seq))
            hilos.append(h)

    for h in hilos:
        h.start()
    for h in hilos:
        h.join()

    print("\n=== Simulación concurrente finalizada ===\n")


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
    
    print("\nUsuarios registrados inicialmente:")
    usuarios = [
        Usuario("José Rea", 1),
        Usuario("Cristhian Guaman", 2),
        Usuario("Enma Castelo", 3),
        Usuario("Allan Avendaño", 4)
    ]
    biblioteca.contadorUsuarios = 4
    
    for u in usuarios:
        print(f"(ID: {u.idUsuario}) {u.nombre}")
    
    
    while True:
        print("\n" + "="*60)
        print("         MENÚ PRINCIPAL - BIBLIOTECA DIGITAL")
        print("="*60)
        print("1. Simulación automática")
        print("2. Prestar libro ")
        print("3. Devolver libro ")
        print("4. Ver historial de movimientos")
        print("5. Ver inventario actual")
        print("6. Crear nuevo usuario")
        print("7. Limpiar bitácora.log")
        print("0. Salir")
        print("="*60)
        
        opcion = input("").strip()
        
        if opcion == "0":
            print("\n¡Gracias por usar el sistema!")
            break
        
        elif opcion == "1":
            simularConcurrencia(biblioteca, usuarios)
        
        elif opcion in ["2", "3"]:
            print("\nUsuarios disponibles:")
            for i, u in enumerate(usuarios, 1):
                print(f"  {i}. {u.nombre} (ID {u.idUsuario})")
            try:
                idx = int(input("Número de usuario → ")) - 1
                if idx < 0 or idx >= len(usuarios):
                    raise ValueError
                usuario = usuarios[idx]
            except:
                print("Selección inválida.")
                continue
            
            titulo = input("Título del libro → ").strip()
            if not titulo:
                print("Título requerido.")
                continue
            
            if opcion == "2":
                usuario.solicitarPrestamo(biblioteca, titulo)
            else:
                usuario.devolverLibro(biblioteca, titulo)
        
        elif opcion == "4":
            biblioteca.mostrarHistorial()
        
        elif opcion == "5":
            biblioteca.mostrarInventario()
        
        elif opcion == "6":
            nombre = input("Nombre del nuevo usuario → ").strip()
            if not nombre:
                print("Nombre requerido.")
                continue
            biblioteca.contadorUsuarios += 1
            nuevo = Usuario(nombre, biblioteca.contadorUsuarios)
            usuarios.append(nuevo)
            print(f"Usuario creado: {nuevo.nombre} (ID {nuevo.idUsuario})")
        
        elif opcion == "7":
            confirmar = input("¿Realmente quieres borrar bitacora.log? (s/n): ").lower()
            if confirmar == 's':
                try:
                    open("bitacora.log", "w", encoding="utf-8").close()
                    print("Bitácora limpiada exitosamente.")
                except Exception as e:
                    print(f"No se pudo limpiar: {e}")
            else:
                print("Operación cancelada.")
        
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()