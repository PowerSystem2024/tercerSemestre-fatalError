import java.util.Scanner;

public class CalculadoraUTN {
    public static void main(String[] args) {
        Scanner entrada = new Scanner(System.in);
        while (true){
            System.out.println("********* Aplicacion Calculadora *******");
            mostrarMenu();
            try {
                var operacion = Integer.parseInt(entrada.nextLine());
                if (operacion >= 1 && operacion <= 4) {
                    ejecutarOperacion(operacion, entrada);
                }//fin del if
                else if (operacion == 5) {
                    System.out.println("Hasta pronto");
                    break;
                } else {
                    System.out.println("opcion erronea" + operacion);
                }
                //Imprimijmimos un salto de linea antes de repetir el menu
                System.out.println();
            } catch (Exception e){ // fin del try , comienzo del catch
                System.out.println("Ocurrio un error" + e.getMessage());

            }
        } //fin ciclo while
    } // fin main

    private static void mostrarMenu(){
        //mostramos el menu
        System.out.println("""
                    1. Suma
                    2. Resta
                    3. Multiplicacion
                    4. Division
                    5. Salir
                 
                    """);
        System.out.println("Operacion a realizar?");

    }// fin metodoo mostrarMenu

    private static void  ejecutarOperacion(int operacion, Scanner entrada){
        System.out.println("digite el valor para operando 1");
        var operando1 = Double.parseDouble(entrada.next());
        System.out.println("digite el valor para operando 2");
        var operando2 = Double.parseDouble(entrada.next());
        Double resultado;
        switch (operacion) {
            case 1 -> {
                resultado = operando1 + operando2;
                System.out.println("resultado = " + resultado);
            }
            case 2 -> {
                resultado = operando1 - operando2;
                System.out.println("resultado = " + resultado);
            }

            case 3 -> {
                resultado = operando1 * operando2;
                System.out.println("resultado = " + resultado);
            }

            case 4 -> {
                resultado = operando1 / operando2;
                System.out.println("resultado = " + resultado);
            }
            default -> System.out.println("opcion erronea" + operacion);
        }//fin switch
    } // fin metodo ejecturarOperacion

}// fin clase
