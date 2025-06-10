#with open('prueba.txt', 'r', encoding='utf8') as archivo:
#    print(archivo.read())

from ManejoArchivo2 import ManejoArchivos2

with ManejoArchivos2('prueba.txt') as archivo:
    print(archivo.read())
