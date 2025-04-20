package test;

public class TestArgumentosVariables {
    public static void main(String[] args) {
        imprimirNumeros(3,4,5);
        imprimirNumeros(13,14,15);
        variosParametros("Juan","Perez", 7,8,9);
    }
    
    private static void variosParametros(String nombre,String apellido, int ...numeros){
        System.out.println("Nombre " + nombre + " Apellido: " + apellido);
        imprimirNumeros(numeros);
   
    }
    //los ... nos dice que son argumentos variables y la cantidad de argumentos va a ser indefinida
    private static void imprimirNumeros(int ...numeros){
        for (int i = 0; i < numeros.length; i++){
            System.out.println("Elementos: " + numeros[i]);
        }
    }
}
