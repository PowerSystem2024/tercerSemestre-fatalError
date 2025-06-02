import aritmetica.Aritmetica;

public class TestExcepciones {
    public static void main(String[] args) {
        int resultado = 0;
        try {
            resultado = Aritmetica.division(10, 0);
        }catch(OperacionExcepcion e){
            System.out.println("Ocurrio un error de tipo OperacionExcepcion");
            System.out.println(e.getMessage());
        }
        } catch (Exception e){
            System.out.println("ocurrio un error");
            e.printStackTrace(e.getMessage()); // se conoce como pila de excepciones
        System.out.println(e.getMessage());
        }
        finally{
            System.out.println("Se reviso la division entre  cero");
        }
        System.out.println("La variable de resultado tieene como valor: " + resultado);


    }
}
