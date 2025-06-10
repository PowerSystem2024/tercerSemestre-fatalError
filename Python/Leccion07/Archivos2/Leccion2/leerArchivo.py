archivo = open('prueba.txt', 'r', encoding='utf8')  # Corregí la asignación con "=" y las comillas
print(archivo.read()) 
#print(archivo.read(16)) 
#print(archivo.read(10)) 
# Continuamos desde la linea anterior 
#print(archivo.readline()) 
#print(archivo.readline()) 
#vamos a iterar el archivo, cada una de las lineas 
#for linea in archivo: 
#print(linea): iteramos todos los elementos del archivo 
#print(archivo.readlines()[11]) 

archivo2 = open('copia.txt', 'w', encoding="utf8")  # Corregí la asignación con "="
archivo2.write(archivo.read()) 
archivo.close()  # Cerramos el primer archivo
archivo2.close()  # Cerramos el segundo archivo

print('Se ha terminado el proceso de leer y copiar archivos')