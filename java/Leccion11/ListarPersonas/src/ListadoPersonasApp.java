import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

//TIP To <b>Run</b> code, press <shortcut actionId="Run"/> or
// click the <icon src="AllIcons.Actions.Execute"/> icon in the gutter.
public class ListadoPersonasApp {
    public static void main(String[] args) {
        Scanner entrada = new Scanner(System.in);
        // definimos la lista fuera del ciclo while
        List<Persona> personas = new ArrayList<>();
        //empezamos con el menu
        var salir = false;
        while(!salir){
            mostrarMenu();
            try{
                salir = ejecutarOperacion(entrada, personas);
            } catch (Exception
             e){
                System.out.println("Ocurrio un error:"+ e.getMessage());
            }
        } // fin metodo while
    }// fin del metodo main

    private static void mostrarMenu(){
        //mostrar las opciones
        System.out.print("""
                ***Listado de personas***
                1. agregar
                2. listar
                3. salir
                
                """);
        System.out.println("Digite una de las opciones: ");
    } // fin del metodo mostrarMenu

    private static boolean ejecutarOperacion(Scanner entrada , List<Persona>personas){
        var opcion = Integer.parseInt(entrada.nextLine());
        var salir = false;
        //revisamos la opcion digitada a traves de un switch
        switch (opcion) {
            case 1 -> { // AGREGAR UNA PERSONA A LA LISTA
                System.out.print("Digite el nombre: ");
                var nombre = entrada.nextLine();
                System.out.print("Digite el telefono");
                var tel = entrada.nextLine();
                System.out.print("Digite el correo");
                var email = entrada.nextLine();
                //creamos el objeto persona
                var persona = new Persona(nombre, tel, email);
                //agregamos la persona a la lista
                personas.add(persona);
                System.out.println("La lista tiene: " + personas.size() + "elementos");
            } // fin del caso 1
            case 2 -> { // LISTAR A LAS PERSONAS
                System.out.println("Listado de personas");
                //mejoras con lambda y el metodo de referencia
                //personas.forEach((persona)-> System.out.println(persona));
                personas.forEach(System.out::println);
            }//fin caso 2
            case 3 -> { //SALIR DEL CICLO
                System.out.println("Hasta pronto...");
                salir = true;
            } // fin del caso 3
            default -> System.out.println(" opcion incorrecta: " + opcion);
        }// FION DEL SWITCH
        return salir;
    } // fin del metodo ejecutar ejecutarOeracion
} // fin de la clase LIstadoPersonaApp

