-- Crud: create(insertar), read(leer), update(actualizar), delete(eliminar)
-- Listar los estudiantes (read)
SELECT * FROM estudiantes2025;
-- Insertar estudiante
INSERT INTO estudiantes2025 (nombre, apellido, telefono, email) VALUES ("Juan", "Perez", "123456789", "Juan@gmail.com");
-- Update(modificar)
UPDATE estudiantes2025 set nombre= "Juan Carlos", apellido="Garcia" WHERE id= 1;
-- Delete(eliminar)
delete from estudiantes2025 where id = 2;
-- Para modificar el id y comience en 1
alter table estudiantes2025 auto_increment = 1;