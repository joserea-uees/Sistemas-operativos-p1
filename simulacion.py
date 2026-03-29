import threading
import time
import random

def simularConcurrencia(biblioteca, usuarios):
    print("\nSIMULACION INICIADA\n")

    def acciones(u, libro):
        u.solicitarPrestamo(biblioteca, libro)
        time.sleep(random.uniform(0.5, 1.5))
        u.devolverLibro(biblioteca, libro)

    libros = list(biblioteca.inventario.keys())

    hilos = []
    for i, u in enumerate(usuarios):
        libro = libros[i % len(libros)]
        h = threading.Thread(target=acciones, args=(u, libro))
        hilos.append(h)

    for h in hilos:
        h.start()
    for h in hilos:
        h.join()

    print("\nSIMULACION FINALIZADA\n")