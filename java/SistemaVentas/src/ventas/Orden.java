package ventas;

public class Orden {
    private int idOrden;
    private Computadora[] computadoras;
    private static int contadorOrdenes;
    private static final int MAX_COMPUTADORAS = 10;
    private int contadorComputadoras;

    public Orden() {
        this.idOrden = ++contadorOrdenes;
        computadoras = new Computadora[MAX_COMPUTADORAS];
    }

    public void agregarComputadora(Computadora computadora) {
        if (contadorComputadoras < MAX_COMPUTADORAS) {
            computadoras[contadorComputadoras++] = computadora;
        } else {
            System.out.println("No se pueden agregar más computadoras a esta orden.");
        }
    }

    public void mostrarOrden() {
        System.out.println("Orden #" + idOrden);
        for (int i = 0; i < contadorComputadoras; i++) {
            System.out.println(computadoras[i]);
        }
    }
}