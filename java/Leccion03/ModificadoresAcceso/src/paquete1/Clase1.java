package paquete1;

public class Clase1 {
    public String atributoPublic = "Valor atributo public";
    protected String atributoProtected = "Valor atributo protected";
    
    public Clase1(){
        System.out.println("Constructor Public");
    }
    protected Clase1(String atributoPublic){
        System.out.println("Constructor protected");
    }
    public void metodoPublico(){
        System.out.println("Metodo Public");
    }
    
    protected void metodoProtected(){
        System.out.println("Metodo protected");
    }
}
