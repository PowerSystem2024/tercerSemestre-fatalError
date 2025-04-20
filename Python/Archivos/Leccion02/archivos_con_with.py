from ManejoArchivos import ManejoArchivos
#MANEJO DE CONTEXTO WITH: Sintaxis simplificada, abre y cierra el archivo
#with open('prueba.txt','r',encoding='utf8') as archivo: #al archivo.txt le vamos a decir 'archivo
 #   print(archivo.read())

#no hace falta ni el try ni el finally
#en el contexto de with lo que se ejecuta de manera automática
#Utiliza diferentes metodos:  __enter__ este es el que abre
#Ahora el siguiente metodo es el que cierra: __exit__
#nosotros tambien podemos programar nuestros propios manejos de recursos

with ManejoArchivos('prueba.txt') as archivo:
    print(archivo.read())