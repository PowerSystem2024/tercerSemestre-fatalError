#Declaramos una variable

try:
    archivo = open('prueba.txt','w',encoding='utf8') #si este archivo no existe lo va a crear, de lo contrario va a buscar este archivo. w de write. - llegado al caso que no lea las tildes colocar encoding='utf8' 
#es recomendable que esta sentencia esté dentro de un bloque de excepcion try catch porque puede tirar errores
    archivo.write('Programamos con diferentes tipos de archivos, ahora en txt.\n')
    archivo.write('Los acentos son importantes para las palabras\n')
    archivo.write('Como por ejemplo: acción, ejecución y programación\n')
    archivo.write('Saludos a todos los alumnos de la tecnicatura\n')
    archivo.write('Con esto terminamos')
    #escribe dentro del archivo
except Exception as e:
    print(e)
finally: #Siempre se ejecuta
    archivo.close() # Con esto se debe cerrar el archivo
archivo.write('todo quedó perfecto')