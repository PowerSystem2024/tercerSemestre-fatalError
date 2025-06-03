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
            sentencia = 'UDPATE persona SET nombre = %s, apellido = %s, email = %s WHERE id_persona = %s'
            valores = ('Juan Carlos', 'Perez', 'jcperez@mail.com', 4),
            ('Carlos', 'Lara', 'clara@mail.com', 5)  # esta es una tupla de tuplas
            cursor.executemany(sentencia, valores)  # De esta manera ejecutamos la sentencia
            # conexion.commit()  # Hacemos el commit manualmente para guardar en la db 
            registros_actualizados = cursor.rowcount
            print(f'Los registros actualizados son: {registros_actualizados}')
        
        
except Exception as e:
    print(f'Ocurrió un error: {e}')
finally:
    conexion.close()