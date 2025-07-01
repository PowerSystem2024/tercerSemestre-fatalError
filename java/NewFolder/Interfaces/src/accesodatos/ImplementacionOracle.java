
package accesodatos;

 
public class ImplementacionOracle implements IAccesoDatos {

    @Override
    public void instertar() {
        System.out.println("insertar desde Oracle");
    }

    @Override
    public void listar() {
        System.out.println("Listar desde Oracle");
           }

    @Override
    public void actualizar() {
      System.out.println("actualizar desde Oracle");
    }

    @Override
    public void eliminar() {
        System.out.println("eliminar desde Oracle");
}
}