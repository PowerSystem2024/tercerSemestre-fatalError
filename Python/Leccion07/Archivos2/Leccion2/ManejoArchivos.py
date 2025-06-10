try: 
    archivo = open('prueba.txt', 'w', encoding='utf8')  
    archivo.write('Programamos con diferentes tipos de archivos, ahora en txt.\n') 
    archivo.write('Los acentos son importantes para las palabras\n') 
    archivo.write('como por ejemplo: acción, ejecución y producción\n')
    archivo.write('las letras son:\nr read leer, \na append anexa, \nw write escribe, \nx crea un archivo\n')
    archivo.write("\nt esta es para texto o text, \nb archivos binarios, \nw+ Lee y escribe son iguales r+\n") 
    archivo.write('Saludos a todos los alumnos de la tecnicatura\n') 
    archivo.write('Con esto terminamos') 
except Exception as e: 
    print(e) 
finally:  
    archivo.close()
