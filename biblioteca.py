import threading
from datetime import datetime


class Biblioteca:
    def __init__(self):
        self.inventario = {}           # dict[str, int] → recurso compartido
        self.historial = []            # list[dict] → recurso compartido
        self.lock = threading.Lock()   # mutex
        self.contadorUsuarios = 0

    def agregarLibro(self, libro):
        self.inventario[libro.titulo] = libro.copiasDisponibles
        print(f"Libro agregado: {libro.titulo} ({libro.copiasDisponibles} copias)")

    def registrarBitacora(self, evento, usuario_nombre, titulo, copiasAntes=None, copiasDespues=None):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        linea = f"{ts} | {evento:14} | {usuario_nombre:15} | {titulo:35}"

        if copiasAntes is not None:
            linea += f" | antes: {copiasAntes:2}"
        if copiasDespues is not None:
            linea += f" | después: {copiasDespues:2}"

        linea += "\n"

        with open("bitacora.log", "a", encoding="utf-8") as f:
            f.write(linea)

    def prestarLibro(self, usuario, titulo):
        with self.lock:
            self.registrarBitacora("ADQUIERE_LOCK", usuario.nombre, titulo)

            if titulo not in self.inventario:
                print(f"✗ '{titulo}' no existe.")
                self.registrarBitacora("NO_EXISTE", usuario.nombre, titulo)
                self.registrarBitacora("LIBERA_LOCK", usuario.nombre, titulo)
                return

            copiasAntes = self.inventario[titulo]

            if copiasAntes > 0:
                self.inventario[titulo] -= 1
                usuario.librosPrestados.append(titulo)

                self.historial.append({
                    "usuario": usuario.nombre,
                    "libro": titulo,
                    "accion": "préstamo",
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

                print(f"✓ {usuario.nombre} tomó '{titulo}'")
                self.registrarBitacora("PRESTAMO_OK", usuario.nombre, titulo, copiasAntes, self.inventario[titulo])

            else:
                print(f"✗ Sin copias de '{titulo}'")
                self.registrarBitacora("SIN_COPIAS", usuario.nombre, titulo, copiasAntes)

            self.registrarBitacora("LIBERA_LOCK", usuario.nombre, titulo)

    def devolverLibro(self, usuario, titulo):
        with self.lock:
            self.registrarBitacora("ADQUIERE_LOCK", usuario.nombre, titulo)

            if titulo not in usuario.librosPrestados:
                print(f"✗ {usuario.nombre} no tiene '{titulo}'")
                self.registrarBitacora("NO_PRESTADO", usuario.nombre, titulo)
                self.registrarBitacora("LIBERA_LOCK", usuario.nombre, titulo)
                return

            copiasAntes = self.inventario.get(titulo, 0)

            self.inventario[titulo] = copiasAntes + 1
            usuario.librosPrestados.remove(titulo)

            self.historial.append({
                "usuario": usuario.nombre,
                "libro": titulo,
                "accion": "devolución",
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            print(f"↩ {usuario.nombre} devolvió '{titulo}'")
            self.registrarBitacora("DEVOLUCION_OK", usuario.nombre, titulo, copiasAntes, self.inventario[titulo])

            self.registrarBitacora("LIBERA_LOCK", usuario.nombre, titulo)

    def mostrarHistorial(self):
        print("\n=== HISTORIAL ===")
        for h in self.historial:
            print(f"{h['fecha']} | {h['usuario']} | {h['accion']} | {h['libro']}")

    def mostrarInventario(self):
        print("\n=== INVENTARIO ===")
        for titulo, copias in self.inventario.items():
            print(f"{titulo}: {copias} copias")