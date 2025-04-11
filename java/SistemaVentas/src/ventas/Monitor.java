package ventas;

public class Monitor {
    private final int idMonitor;
    private String marca;
    private String tamano;
    private static int contadorMonitores;

    public Monitor(String marca, String tamano) {
        this.idMonitor = ++contadorMonitores;
        this.marca = marca;
        this.tamano = tamano;
    }

    public int getIdMonitor() {
        return idMonitor;
    }

    @Override
    public String toString() {
        return "Monitor{" + "idMonitor=" + idMonitor + ", marca=" + marca + ", tamano=" + tamano + '}';
    }
}