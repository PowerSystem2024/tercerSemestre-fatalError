import psycopg2  # Esto es para poder conectarnos a Postgre

conexion = psycopg2.connect(
    user='postgres1', 
    password='admin', 
    host='127.0.0.1', 
    port='5432', 
    database='test_bd'
)

try:
    with conexion:
        with conexion.cursor() as cursor:
            sentencia = 'INSERT INTO persona (nombre, apellido, email) VALUES (%s, %s, %s)' 
            valores = (('Carlos', 'Lara', 'clara@mail.com'),) # esta es una tupla 
            cursor.execute(sentencia, valores)  # De esta manera ejecutamos la sentencia
            # conexion.commit()  # Hacemos el commit manualmente para guardar en la db 
            registros_insertados = cursor.rowcount
            print(f'Los registros insertados son: {registros_insertados}')
        
        
except Exception as e:
    print(f'Ocurrió un error: {e}')
finally:
    conexion.close()