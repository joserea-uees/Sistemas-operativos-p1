from biblioteca import Biblioteca
from usuario import Usuario
from libro import Libro
from simulacion import simularConcurrencia

from info_estudiantes import nombres_estudiantes
from info_proyecto import descripcion_proyecto


def main():
    biblioteca = Biblioteca()

    libros = [
        Libro("El Quijote Digital", "Miguel de Cervantes", 3),
        Libro("Cien Años de Soledad Digital", "Gabriel García Márquez", 2),
        Libro("1984 Digital", "George Orwell", 1),
        Libro("Rayuela Digital", "Julio Cortázar", 4)
    ]

    for libro in libros:
        biblioteca.agregarLibro(libro)

    usuarios = [
        Usuario("José Rea", 1),
        Usuario("Cristhian Guaman", 2),
        Usuario("Enma Castelo", 3),
        Usuario("Allan Avendaño", 4)
    ]

    while True:
        print("\n" + "="*50)
        print("        SISTEMA BIBLIOTECA DIGITAL")
        print("="*50)
        print("1. Ver estudiantes")
        print("2. Ver descripción del proyecto")
        print("3. Simulación automática")
        print("4. Prestar libro")
        print("5. Devolver libro")
        print("6. Ver historial")
        print("7. Ver inventario")
        print("8. Crear usuario")
        print("9. Limpiar bitácora")
        print("0. Salir")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            nombres_estudiantes()

        elif opcion == "2":
            descripcion_proyecto()

        elif opcion == "3":
            simularConcurrencia(biblioteca, usuarios)

        elif opcion in ["4", "5"]:
            print("\nUsuarios disponibles:")
            for i, u in enumerate(usuarios, 1):
                print(f"{i}. {u.nombre}")

            try:
                idx = int(input("Seleccione usuario: ")) - 1
                usuario = usuarios[idx]
            except:
                print("Usuario inválido")
                continue

            titulo = input("Título del libro: ").strip()

            if opcion == "4":
                usuario.solicitarPrestamo(biblioteca, titulo)
            else:
                usuario.devolverLibro(biblioteca, titulo)

        elif opcion == "6":
            biblioteca.mostrarHistorial()

        elif opcion == "7":
            biblioteca.mostrarInventario()

        elif opcion == "8":
            nombre = input("Nombre del nuevo usuario: ").strip()
            if nombre:
                nuevo = Usuario(nombre, len(usuarios) + 1)
                usuarios.append(nuevo)
                print("Usuario creado correctamente")
            else:
                print("Nombre inválido")

        elif opcion == "9":
            confirmar = input("¿Seguro que deseas borrar la bitácora? (s/n): ").lower()
            if confirmar == "s":
                open("bitacora.log", "w").close()
                print("Bitácora limpiada")

        elif opcion == "0":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción no válida")


if __name__ == "__main__":
    main()