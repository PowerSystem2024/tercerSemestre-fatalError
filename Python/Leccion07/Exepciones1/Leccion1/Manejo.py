from NumerosIgualesEx import NumerosIgualesEx
resultado = None
try:
    a = int(input('Digite el primer número: '))
    b = int(input('Digite el segundo número: '))
    if a == b:
        raise NumerosIgualesEx('son numeros iguales')
    resultado = a / b
except TypeError as e: 
    print(f'TypeError - Ocurrió un error: {type(e)}')
except ZeroDivisionError as e: 
    print(f'ZeroDivisionError - Ocurrió un error: {type(e)}')
except Exception as e: 
    print(f'Exception - Ocurrió un error: {type(e)}')
else: 
    print("No se arrojó ninguna excepción")
finally:
    print("Ejecución de este bloque finally")

print(f'El resultado es: {resultado}')
print('Seguimos...')