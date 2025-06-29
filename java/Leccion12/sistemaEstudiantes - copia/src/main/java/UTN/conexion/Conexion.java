package UTN.conexion;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class Conexion {
    public static Connection getConexion(){
        Connection conexion = null;
        var baseDatos = "estudiantes";
        var url = "jdbc:mysql://localhost:3306/" + baseDatos + "?useSSL=false&serverTimezone=UTC";
        var usuario = "root";
        var password = "4575";

        try {
            Class.forName("com.mysql.cj.jdbc.Driver"); // ✅ ESTA ES LA CLASE CORRECTA
            conexion = DriverManager.getConnection(url, usuario, password);
        } catch (ClassNotFoundException | SQLException e){
            System.out.println("Error al conectar: " + e.getMessage());
        }
        return conexion;
    }
}
