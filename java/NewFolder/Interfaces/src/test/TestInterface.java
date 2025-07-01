
package test;

import accesodatos.IAccesoDatos;
import accesodatos.ImplementacionMysql;
import accesodatos.ImplementacionOracle;


public class TestInterface {

    public static void main(String[] args) {
        
        IAccesoDatos datos = new ImplementacionMysql();
       // datos.listar();
        //imprimir(datos);
        datos = new ImplementacionOracle();
        //datos.listar();
        imprimir(datos);

    }

public static void imprimir(IAccesoDatos datos) {
datos.listar();
}
    }


