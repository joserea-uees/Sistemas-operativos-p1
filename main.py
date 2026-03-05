from info_estudiantes import nombres_estudiantes
from info_proyecto import descripcion_proyecto

def main():
    while True:
        print("\n" + "="*40)
        print("          MENÚ PRINCIPAL")
        print("="*40)
        print("1. Mostrar nombres de los estudiantes")
        print("2. Mostrar descripción del proyecto")
        print("3. Salir")
        
        opcion = input("\nIngrese una opción: ").strip()
        
        if opcion == "1":
            nombres_estudiantes()
        elif opcion == "2":
            descripcion_proyecto()
        elif opcion == "3":
            break
        else:
            print("Opción no válida, intente nuevamente.")

if __name__ == "__main__":
    main()