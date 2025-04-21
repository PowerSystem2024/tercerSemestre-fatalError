# test_catalogo_peliculas.py

from dominio.pelicula import Pelicula
from servicio.catalogo_peliculas import CatalogoPeliculas

def menu():
    opcion = -1
    while opcion != 4:
        print('\nMenú del Catálogo de Películas')
        print('1. Agregar película')
        print('2. Listar películas')
        print('3. Eliminar archivo de películas')
        print('4. Salir')
        try:
            opcion = int(input('Elige una opción (1-4): '))
        except ValueError:
            print("Por favor, ingresa un número válido.")
            continue

        if opcion == 1:
            nombre = input('Nombre de la película: ')
            pelicula = Pelicula(nombre)
            CatalogoPeliculas.agregar_pelicula(pelicula)
        elif opcion == 2:
            CatalogoPeliculas.listar_peliculas()
        elif opcion == 3:
            CatalogoPeliculas.eliminar()
        elif opcion == 4:
            print('Saliendo del programa...')
        else:
            print('Opción no válida.')

if __name__ == '__main__':
    menu()
