import threading
import time
import random

def simularConcurrencia(biblioteca, usuarios):
    print("\n=== Simulación concurrente iniciada ===\n")

    def acciones_usuario(u, secuencia):
        for accion, titulo in secuencia:
            if accion == "prestamo":
                u.solicitarPrestamo(biblioteca, titulo)
            else:
                u.devolverLibro(biblioteca, titulo)
            time.sleep(random.uniform(0.2, 0.7))

    hilos = []

    secuencias = [
        (usuarios[0], [("prestamo", "El Quijote Digital"), ("prestamo", "Cien Años de Soledad Digital"), ("devolucion", "El Quijote Digital")]),
        (usuarios[1], [("prestamo", "El Quijote Digital"), ("prestamo", "1984 Digital")]),
        (usuarios[2], [("prestamo", "Rayuela Digital")]),
        (usuarios[3], [("prestamo", "El Quijote Digital"), ("devolucion", "El Quijote Digital")])
    ]

    for u, seq in secuencias:
        h = threading.Thread(target=acciones_usuario, args=(u, seq))
        hilos.append(h)

    for h in hilos:
        h.start()
    for h in hilos:
        h.join()

    print("\n=== Simulación concurrente finalizada ===\n")