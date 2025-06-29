package UTN.datos;

import UTN.dominio.Estudiante;

import static UTN.conexion.Conexion.getConexion;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.List;

public class EstudianteDAO {

    // Método Listar Estudiantes
    public List<Estudiante> ListarEstudiantes() {
        List<Estudiante> Estudiantes = new ArrayList<>();
        PreparedStatement ps = null;
        ResultSet rs = null;
        Connection con = getConexion();
        String sql = "SELECT * FROM estudiantes2025 ORDER BY id";

        try {
            ps = con.prepareStatement(sql);
            rs = ps.executeQuery();

            while (rs.next()) {
                var estudiante = new Estudiante();
                estudiante.setIdEstudiante(rs.getInt("id"));
                estudiante.setNombre(rs.getString("nombre"));
                estudiante.setApellido(rs.getString("apellido"));
                estudiante.setTelefono(rs.getString("telefono"));
                estudiante.setEmail(rs.getString("email"));
                Estudiantes.add(estudiante);
            }
        } catch (Exception e) {
            System.out.println("Error al seleccionar datos: " + e.getMessage());
        } finally {
            try {
                if (rs != null) rs.close();
                if (ps != null) ps.close();
                if (con != null) con.close();
            } catch (Exception e) {
                System.out.println("Error al cerrar recursos: " + e.getMessage());
            }
        }
        return Estudiantes;
    }

    // Método buscar Estudiante por Id
    public boolean buscarEstudiantePorId(Estudiante estudiante) {
        PreparedStatement ps = null;
        ResultSet rs = null;
        Connection con = getConexion();
        String sql = "SELECT * FROM estudiantes2025 WHERE id = ?";

        try {
            ps = con.prepareStatement(sql);
            ps.setInt(1, estudiante.getIdEstudiante());
            rs = ps.executeQuery();

            if (rs.next()) {
                estudiante.setNombre(rs.getString("nombre"));
                estudiante.setApellido(rs.getString("apellido"));
                estudiante.setTelefono(rs.getString("telefono"));
                estudiante.setEmail(rs.getString("email"));
                return true;
            } else {
                return false; // No se encontró el estudiante
            }
        } catch (Exception e) {
            System.out.println("Ocurrio un error al buscar estudiante: " + e.getMessage());
            return false;
        } finally {
            try {
                if (rs != null) rs.close();
                if (ps != null) ps.close();
                if (con != null) con.close();
            } catch (Exception e) {
                System.out.println("Error al cerrar recursos: " + e.getMessage());
            }
        }
    }

    public boolean agregarEstudiante(Estudiante estudiante) {
        PreparedStatement ps;
        Connection con = getConexion();
        String sql = "INSERT INTO estudiantes2025 (nombre, apellido, telefono, email) VALUES (?, ?, ?, ?)";

        try {
            ps = con.prepareStatement(sql);
            ps.setString(1, estudiante.getNombre());
            ps.setString(2, estudiante.getApellido());
            ps.setString(4, estudiante.getEmail());
            ps.setString(3, estudiante.getTelefono());

            ps.execute();
            return true;
        } catch(Exception e) {
            System.out.println("Ocurrio un error al agregar estudiante: " + e.getMessage());
        }
        finally {
            try {
                con.close();
            }catch(Exception e){
                System.out.println("Error al cerrar la conexion: " + e.getMessage());
            }
        }
        return false;
    }

    public static void main(String[] args) {
        var estudianteDAO = new EstudianteDAO();
        //modificar estudiante
        var estudianteModificado = new Estudiante(8,"Juan Carlos","Juarez","123456789", "JuanCarlos@gmail.com");
        var modificado = estudianteDAO.buscarEstudiantePorId(estudianteModificado);
        if (modificado)
            System.out.println("Estudiante modificado correctamente");
        else
            System.out.println("No se modifico el estudiante");


        //agregar estudiante
        // var nuevoEstudiante = new Estudiante("Carlos","Lara","123456789", "Laura@gmail.com");
        //var agregado = estudianteDAO.agregarEstudiante(nuevoEstudiante);
        //if (agregado) {
        // System.out.println("Estudiante agregado"+nuevoEstudiante);
        // } else {
        //     System.out.println("Estudiante no agregado"+nuevoEstudiante);
        // }

        System.out.println("Listado de Estudiantes");
        List<Estudiante> estudiantes = estudianteDAO.ListarEstudiantes();
        estudiantes.forEach(System.out::println);
    }

    //Metodo para modificar estudiante
    public boolean modificarEstudiante(Estudiante estudiante) {
        PreparedStatement ps;
        Connection con = getConexion();
        String sql = "UPDATE estudiantes SET nombre=?, apellido=?, telefono=?, email=? WHERE id=?";
        try{
            ps = con.prepareStatement(sql);
            ps.setString(1,estudiante.getNombre());
            ps.setString(2, estudiante.getApellido());
            ps.setString(3, estudiante.getEmail());
            ps.setString(4, estudiante.getTelefono());
            ps.setInt(5, estudiante.getIdEstudiante());
            ps.execute();
            return true;

        }catch(Exception e){
            System.out.println("Error al modificar estudiante: " + e.getMessage());
        }
        finally {
            try {
                con.close();
            }catch(Exception e){
                System.out.println("Error al cerrar la conexion: " + e.getMessage());

            }//fin

        }//fin
        return false;
    }



        //buscar por id
       // var estudiante1 = new Estudiante(1);
       // System.out.println("Estudiantes antes de la busqueda:  "+estudiante1);
       // var encontrado = estudianteDAO.buscarEstudiantePorId(estudiante1);
       // if(encontrado)
      //      System.out.println("Estudiante encontrado"+estudiante1);
      //  else
     //       System.out.println("Estudiante no encontrado"+estudiante1.getIdEstudiante());
      //  }
}
