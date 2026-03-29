import threading
from datetime import datetime


class Biblioteca:
    def __init__(self):
        self.inventario = {}
        self.historial = []
        self.lock = threading.Lock()
        self.semaforo = threading.Semaphore(3)  #MAX 3 USUARIOS

    def agregarLibro(self, libro):
        self.inventario[libro.titulo] = libro.copiasDisponibles
        print(f"Libro agregado / {libro.titulo} / {libro.copiasDisponibles} copias")

    def registrarBitacora(self, evento, usuario_nombre, titulo, antes=None, despues=None):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        linea = f"{ts} / {evento} / {usuario_nombre} / {titulo}"

        if antes is not None:
            linea += f" / antes:{antes}"
        if despues is not None:
            linea += f" / despues:{despues}"

        linea += "\n"

        with open("bitacora.log", "a", encoding="utf-8") as f:
            f.write(linea)

    def prestarLibro(self, usuario, titulo):

        print(f"{usuario.nombre} intenta entrar a leer / {titulo}")

        self.semaforo.acquire()
        print(f"{usuario.nombre} ENTRA a la biblioteca")

        try:
            with self.lock:
                self.registrarBitacora("ADQUIERE_LOCK", usuario.nombre, titulo)

                if usuario.librosPrestados:
                    print(f"✗ {usuario.nombre} ya tiene un libro")
                    self.registrarBitacora("YA_TIENE_LIBRO", usuario.nombre, titulo)
                    return

                if titulo not in self.inventario:
                    print(f"✗ Libro no existe / {titulo}")
                    self.registrarBitacora("NO_EXISTE", usuario.nombre, titulo)
                    return

                antes = self.inventario[titulo]

                if antes > 0:
                    self.inventario[titulo] -= 1
                    usuario.librosPrestados.append(titulo)

                    print(f"✓ {usuario.nombre} tomó / {titulo}")

                    self.registrarBitacora("PRESTAMO_OK", usuario.nombre, titulo, antes, self.inventario[titulo])
                else:
                    print(f"✗ Sin copias / {titulo}")
                    self.registrarBitacora("SIN_COPIAS", usuario.nombre, titulo, antes)

                self.registrarBitacora("LIBERA_LOCK", usuario.nombre, titulo)

        except Exception as e:
            print(f"Error: {e}")

            # SI FALLA, LIBERA
            self.semaforo.release()
            return
    def devolverLibro(self, usuario, titulo):

        with self.lock:
            self.registrarBitacora("ADQUIERE_LOCK", usuario.nombre, titulo)

            if titulo not in usuario.librosPrestados:
                print(f"✗ {usuario.nombre} no tiene / {titulo}")
                self.registrarBitacora("NO_PRESTADO", usuario.nombre, titulo)
                self.registrarBitacora("LIBERA_LOCK", usuario.nombre, titulo)
                return

            antes = self.inventario.get(titulo, 0)

            self.inventario[titulo] += 1
            usuario.librosPrestados.remove(titulo)

            print(f"↩ {usuario.nombre} devolvió / {titulo}")

            self.registrarBitacora("DEVOLUCION_OK", usuario.nombre, titulo, antes, self.inventario[titulo])

            self.registrarBitacora("LIBERA_LOCK", usuario.nombre, titulo)

        # LIBERA CUPO
        print(f"{usuario.nombre} SALE de la biblioteca")
        self.semaforo.release()
    def mostrarInventario(self):
        print("\nINVENTARIO")
        for t, c in self.inventario.items():
            print(f"{t} / {c} copias")