
package accesodatos;
 
public class ImplementacionMysql  implements IAccesoDatos {

    @Override
    public void instertar() {
        System.out.println("insertar desde Mysql");
    }

    @Override
    public void listar() {
        System.out.println("Listar desde Mysql");
           }

    @Override
    public void actualizar() {
      System.out.println("actualizar desde Mysql");
    }

    @Override
    public void eliminar() {
        System.out.println("eliminar desde Mysql");
    }

}
