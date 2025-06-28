from Persona import Persona
from conexion import conexion
from logger_base import log 


class PersonaDAO:
    _SELECCIONAR = 'SELECT * FROM persona ORDER BY id_persona'
    _INSERTAR = 'INSERT INTO persona(nombre, apellido, email) VALUES (%s, %s, %s)'
    _ACTUALIZAR = 'UPDATE persona SET nombre=%s, apellido=%s, email=%s WHERE id_persona=%s'
    _ELIMINAR = 'DELETE FROM persona WHERE id_persona=%s'
    
    @classmethod
    def seleccionar(cls):
        personas = []
        conexion_bd = conexion.obtenerConexion()
        with conexion_bd.cursor() as cursor:
            cursor.execute(cls._SELECCIONAR)
            registros = cursor.fetchall()
            for registro in registros:
                persona = Persona(registro[0], registro[1], registro[2], registro[3])
                personas.append(persona)
        conexion_bd.commit()
        return personas

    @classmethod
    def insertar(cls, persona):
        conexion_bd = conexion.obtenerConexion()
        with conexion_bd.cursor() as cursor:
            valores = (persona.nombre, persona.apellido, persona.email)
            cursor.execute(cls._INSERTAR, valores)
            log.debug(f'Persona insertada: {persona}')
            conexion_bd.commit()
            return cursor.rowcount

    @classmethod
    def actualizar(cls, persona):
        conexion_bd = conexion.obtenerConexion()
        with conexion_bd.cursor() as cursor:
            valores = (persona.nombre, persona.apellido, persona.email, persona.id_persona)
            cursor.execute(cls._ACTUALIZAR, valores)
            log.debug(f'Persona actualizada: {persona}')
            conexion_bd.commit()
            return cursor.rowcount

    @classmethod
    def eliminar(cls, persona):
        conexion_bd = conexion.obtenerConexion()
        with conexion_bd.cursor() as cursor:
            valores = (persona.id_persona,)
            cursor.execute(cls._ELIMINAR, valores)
            log.debug(f'Persona eliminada: {persona}')
            conexion_bd.commit()
            return cursor.rowcount


"""if __name__ == '__main__':
    Persona1 = Persona(id_persona=8)
    Personas_eliminadas = PersonaDAO.eliminar(Persona1)
    log.debug(f'Personas eliminadas: {Personas_eliminadas}')
"""
