#un error o una excepcion es cuando nuestro programa termina de manera abrupta
#ver clases de excepciones ya definidas en python para el manejo de excepciones
#con esto podemos capturar la excepcion en un objeto para que el programa no finalice ante un error
#que pueda cometer un usuario
from NumerosIgualesException import NumerosIgualesException
resultado = None

try:
    a = int(input('Digite un número: ')) #modificamos 10
    b = int(input('Digite otro número: '))
    if a == b:
        raise NumerosIgualesException('Son números iguales')
    #raise nos permite enviar una excepcion
    resultado = a / b # modificamos 10/0
    
except TypeError as e:
    print(f'TypeError - Ocurrió un error: {type(e)}')
except ZeroDivisionError as e:
    print(f'ZeroDivisionError - Ocurrió un error: {type(e)}')
except Exception as e:
    print(f'Exception - Ocurrió un error: {type(e)}')
else:
    print('No se arrojó ninguna excepción')
finally:
    print('Ejecución de este bloque finally') #siempre se va a ejecutar
    
print(f'El resultado es: {resultado}')
print('seguimos...')

#haciendo las cosas mal o haciendo las cosas mal, nuestro programa va a seguir funcionando 
#porque hicimos una "prevencion" de errores