package UTN.datos;

import UTN.dominio.Estudiante;

import static UTN.conexion.Conexion.getConnection;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLOutput;
import java.util.ArrayList;
import java.util.List;

//DAO = DATA ACCES OBJECT
public class EstudianteDAO {

    //metodo listar
    List<Estudiante> listarEstudiantes(){
        List<Estudiante> estudiantes = new ArrayList<>();
        //creamos algunos objetos que son necesarios para comunicarnos con la base de datos
        PreparedStatement ps; //envía sentencia a la base de datos
        ResultSet rs; //obtenemos resultado desde la base de datos

        //Creamos un objeto de tipo conexion
        Connection con = getConnection();
        String sql = "SELECT * FROM estudiantes2022 ORDER BY idestudiantes2022";
        try{
            ps = con.prepareStatement(sql);
            rs = ps.executeQuery();
            while(rs.next()){
                var estudiante = new Estudiante();
                estudiante.setIdEstudiante(rs.getInt("idestudiantes2022"));
                estudiante.setNombre(rs.getString("nombre"));
                estudiante.setApellido(rs.getString("apellido"));
                estudiante.setTelefono(rs.getString("telefono"));
                estudiante.setMail(rs.getString("mail"));
                //falta agregarlo a la lista
                estudiantes.add(estudiante);
            }
        }catch(Exception e){
            System.out.println("Ocurrió un error al seleccionar datos: " +e.getMessage());
        }
        finally{
            try{
                con.close();
            }catch(Exception e){
                System.out.println("Ocurrió un error al cerrar la conexion: " +e.getMessage());
            }
        }//fin del finally
        return estudiantes;
    }//fin del metodo listar

    //Metodo por id -> find by id
    public boolean buscarEstudiantePorId(Estudiante estudiante) {
        PreparedStatement ps;
        ResultSet rs;
        Connection con = getConnection();
        String sql = "SELECT * FROM estudiantes2022 WHERE idestudiantes2022=?";
        try {
            ps = con.prepareStatement(sql);
            ps.setInt(1, estudiante.getIdEstudiante());
            rs = ps.executeQuery();
            if (rs.next()) {
                estudiante.setNombre(rs.getString("nombre"));
                estudiante.setApellido(rs.getString("apellido"));
                estudiante.setTelefono(rs.getString("telefono"));
                estudiante.setMail(rs.getString("mail"));
                return true;//se encontró un registro
            }
        } catch (Exception e) {
            System.out.println("Ocurrió un error al bustar estudiante " + e.getMessage());
        }
        finally {
            try {
                con.close();
            } catch (Exception e) {
                System.out.println("Ocurrió un error al cerrar la conexion: " + e.getMessage());
            }
        }
        return false;
    }

    //Metodo agregar un nuevo estudiante
    public boolean agregarEstudiante(Estudiante estudiante){
        PreparedStatement ps;
        Connection con = getConnection();
        String sql = "INSERT INTO estudiantes2022(nombre, apellido, telefono, mail) VALUES (?, ?, ?, ?)";
        try{
            ps = con.prepareStatement(sql);
            ps.setString(1, estudiante.getNombre());
            ps.setString(2, estudiante.getApellido());
            ps.setString(3, estudiante.getTelefono());
            ps.setString(4, estudiante.getMail());
            ps.execute();
            return true;
        }catch(Exception e){
            System.out.println("Ocurrió un error al agregar estudiante: " + e.getMessage());
        }
        finally{
            try {
                con.close();
            } catch (Exception e) {
                System.out.println("Error al cerrar la conexion: " + e.getMessage());
            }
        }
        return false;
    }//fin de agregar estudiante


    //MODIFICAR ESTUDIANTE
    public boolean modificarEstudiante(Estudiante estudiante){
        PreparedStatement ps;
        Connection con = getConnection();
        String sql = "UPDATE estudiantes2022 SET nombre=?, apellido=?, telefono=?, mail=? WHERE idestudiantes2022=?";
        try{
            ps = con.prepareStatement(sql);
            ps.setString(1,estudiante.getNombre());
            ps.setString(2, estudiante.getApellido());
            ps.setString(3, estudiante.getTelefono());
            ps.setString(4, estudiante.getMail());
            ps.setInt(5,estudiante.getIdEstudiante());
            ps.execute();
            return true;
        }catch(Exception e){
            System.out.println("Error al modificar estudiante: " + e.getMessage());
        }//Fin catch
        finally{
            try {
                con.close();
            } catch (Exception e) {
                System.out.println("Error al cerrar la conexion: " + e.getMessage());
            }
        }
        return false;
    }


    public static void main(String[] args) {
        var estudianteDao = new EstudianteDAO();
        //MODIFICAR ESTUDIANTE
        var estudianteModificado = new Estudiante(2, "Esteban","Kito","666136147","ekito@mail.com");
        var modificado = estudianteDao.modificarEstudiante(estudianteModificado);
        if(modificado)
            System.out.println("Estudiante modificado: "+estudianteModificado);
        else
            System.out.println("No se modificó el estudiante: " +  estudianteModificado);

        /*
        //Agregar estudiante
        var nuevoEstudiante = new Estudiante("Carlos","Lara","448856747","carlosl@mail.com");
        var agregado = estudianteDao.agregarEstudiante(nuevoEstudiante);
        if (agregado)
            System.out.println("Estudiante agregado correctamente: " + nuevoEstudiante);
        else
            System.out.println("No se agregó al estudiante: " +  nuevoEstudiante);
*/
        //Listar los estudiantes
        System.out.println("Listado de estudiantes: ");
        List<Estudiante> estudiantes = estudianteDao.listarEstudiantes();
        estudiantes.forEach(System.out::println); //funcion lambda para imprimir
/*
        //Buscar por id
        var estudiante1 = new Estudiante(2);
        System.out.println("Estudiantes antes de la busqueda: " + estudiante1);
        var encontrado = estudianteDao.buscarEstudiantePorId(estudiante1);
        if(encontrado)
            System.out.println("Estudiante encontrado:" +  estudiante1);
        else
            System.out.println("No se encontró el estudiante" + estudiante1.getIdEstudiante());
*/

    }
}
