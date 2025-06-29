package UTN;


import UTN.conexion.Conexion;

public class Main {
    public static void main(String[] args) {
        var Conexion = UTN.conexion.Conexion.getConexion();
        if (Conexion != null) {
            System.out.println("Conexion exitosa" + Conexion);
        }else{
                System.out.println("Error al conectarse");
        }
    }
    }
