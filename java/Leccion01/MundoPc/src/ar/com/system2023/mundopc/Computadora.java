package ar.com.system2023.mundopc;

//Clase
public class Computadora {
    //Atributos
    private final int idComputadora;
    private String nombre;
    private Monitor monitor;
    private Teclado teclado;
    private Raton raton;
    private static int contadorComputadoras;
    
    //constructor vacío
    private Computadora(){
        //incrementa el numero de id por cada nueva computadora
        this.idComputadora = ++Computadora.contadorComputadoras;
    }
    
    //Constructor 2
    public Computadora(String nombre, Monitor monitor,Teclado teclado, Raton raton){
        this(); //llamamos al constructor vacío
        this.nombre = nombre;
        this.monitor = monitor;
        this.teclado = teclado;
        this.raton = raton;
    }
    
    public int getIdComputadora(){
        return this.idComputadora;
    }

    public String getNombre() {
        return this.nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public Monitor getMonitor() {
        return this.monitor;
    }

    public void setMonitor(Monitor monitor) {
        this.monitor = monitor;
    }

    public Teclado getTeclado() {
        return this.teclado;
    }

    public void setTeclado(Teclado teclado) {
        this.teclado = teclado;
    }

    public Raton getRaton() {
        return this.raton;
    }

    public void setRaton(Raton raton) {
        this.raton = raton;
    }

    @Override
    public String toString() {
        return "Computadora{" + "idComputadora=" + idComputadora + ", nombre=" + nombre + ", monitor=" + monitor + ", teclado=" + teclado + ", raton=" + raton + '}';
    }
    
}
