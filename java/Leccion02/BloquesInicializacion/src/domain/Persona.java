package domain;

public class Persona {

    private final int idPersona;
    private static int contadorPersonas;

    static { //bloque de inicialización estatico - solo se ejecuta 1 vez 
        System.out.println("Ejecucion del bloque estatico");
        ++Persona.contadorPersonas;
    }

    {
        //bloque de inicializacion dinamico - No estatico
        System.out.println("Ejecucion de bloque NO estatico");
        this.idPersona = Persona.contadorPersonas++; //Incrementamos el atributo
    }

    //Los bloques de inicializacion se ejecutan antes del constructor
    public Persona() {
        System.out.println("Ejecucion del constructor");
    }

    public int getIdPersona() {
        return this.idPersona;
    }

    @Override
    public String toString() {
        return "Persona{" + "idPersona=" + idPersona + '}';
    }

}
