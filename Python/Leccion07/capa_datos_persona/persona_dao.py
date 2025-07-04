from Leccion07.capa_datos_persona.cursor_del_pool import (CursorDelPool)
from Leccion07.capa_datos_persona.conexion import Conexion
from Leccion07.capa_datos_persona.Persona import Persona
from logger_base import log

class PersonaDao:
    """
    DAO significa: Data Access Object
    CRUD significa:
                    Create -> Insertar
                    Read   -> Seleccionar
                    Update -> Actualizar
                    Delete -> Eliminar
    """
    _SELECCIONAR = "SELECT * FROM persona ORDER BY id_persona"
    _INSERTAR = "INSERT INTO persona(nombre, apellido, email) VALUES (%s, %s, %s)"
    _ACTUALIZAR = "UPDATE persona SET nombre=%s, apellido=%s, email=%s WHERE id_persona=%s"
    _ELIMINAR = "DELETE FROM persona WHERE id_persona=%s"

    @classmethod
    def seleccionar(cls):
        with CursorDelPool() as cursor:
            cursor.execute(cls._SELECCIONAR)
            registros = cursor.fetchall()
            personas = []
            for registro in registros:
                persona = Persona(registro[0], registro[1], registro[2], registro[3])
                personas.append(persona)
            return personas

    @classmethod
    def insertar(cls, persona):
        with CursorDelPool() as cursor:
            valores = (persona.nombre, persona.apellido, persona.email)
            cursor.execute(cls._INSERTAR, valores)
            log.debug(f'Persona insertada: {persona}')
            return cursor.rowcount

    @classmethod
    def actualizar(cls, persona):
        with CursorDelPool() as cursor:
            valores = (persona.nombre, persona.apellido, persona.email, persona.id_persona)
            cursor.execute(cls._ACTUALIZAR, valores)
            log.debug(f'Persona actualizada: {persona}')
            return cursor.rowcount

    @classmethod
    def eliminar(cls, persona):
        with CursorDelPool() as cursor:
            valores = (persona.id_persona,)
            cursor.execute(cls._ELIMINAR, valores)
            log.debug(f'Persona eliminada: {persona}')
            return cursor.rowcount


if __name__ == '__main__':
    # INSERTAR un registro 
    persona1 = Persona(nombre='Marcos', apellido='Tejada', email='tejadam@mail.com')
    personas_insertadas = PersonaDao.insertar(persona1)
    log.debug(f'Personas insertadas: {personas_insertadas}')

    # ELIMINAR un registro 
    persona1 = Persona(id_persona=18)
    personas_eliminadas = PersonaDao.eliminar(persona1)
    log.debug(f'Personas eliminadas: {personas_eliminadas}')

    # ACTUALIZAR un registro 
    persona1 = Persona(id_persona=1, nombre='Homero', apellido='Simpson', email='homero@springfield.com')
    personas_actualizadas = PersonaDao.actualizar(persona1)
    log.debug(f'Personas actualizadas: {personas_actualizadas}')

    # SELECCIONAR objetos 
    personas = PersonaDao.seleccionar()
    for persona in personas:
        log.debug(persona)
