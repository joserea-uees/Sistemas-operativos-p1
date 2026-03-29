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
        Usuario("Allan Avendaño", 4),
        Usuario("Max Rivas", 5),
        Usuario("Diana Briones", 6),
        Usuario("Danae Granizo", 7),
        Usuario("Juan Pérez", 8)

    ]

    while True:
        print("\n" + "/"*50)
        print("        SISTEMA BIBLIOTECA DIGITAL")
        print("/"*50)
        print("1. Ver estudiantes")
        print("2. Ver descripción del proyecto")
        print("3. Simulación automática")
        print("4. Ver inventario")
        print("0. Salir")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            nombres_estudiantes()

        elif opcion == "2":
            descripcion_proyecto()

        elif opcion == "3":
            simularConcurrencia(biblioteca, usuarios)

        elif opcion == "4":
            biblioteca.mostrarInventario()

     
        elif opcion == "0":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción no válida")


if __name__ == "__main__":
    main()