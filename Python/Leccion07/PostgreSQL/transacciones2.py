import psycopg2 as bd

conexion = bd.connect(
    user='postgres',
    password='admin',
    host='127.0.0.1',
    port='5432',
    database='test_bd'
)

try:
    conexion.autocommit = False
    cursor = conexion.cursor()
    sentencia = "INSERT INTO persona(nombre, apellido, email)VALUES(%s,%s,%s)"  # <-- corregido aquí
    valores = ("Jorge", "Prol", "jprol@gmail.com")
    cursor.execute(sentencia, valores)
    
    sentencia = "UPDATE persona SET nombre=%s, apellido=%s, email=%s WHERE id_persona=%s"
    valores = ("Juan Carlos", "Perez", "jcperez@gmail.com", 1)
    cursor.execute(sentencia, valores)
    
    
    conexion.commit() #se hace el commit de manera manual
    print("Termina la transaccion")
    
except Exception as e:
    conexion.rollback()
    print(f"Ocurrió un error, se hizo un RollBack {e}")
finally:
    conexion.close()