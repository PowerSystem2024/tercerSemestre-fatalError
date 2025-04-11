package ventas;

public class Raton extends DispositivoEntrada {
    private static int contadorRatones;
    private int idRaton;

    public Raton(String tipoEntrada, String marca) {
        super(tipoEntrada, marca);
        this.idRaton = ++contadorRatones;
    }

    @Override
    public String toString() {
        return "Raton{" + "idRaton=" + idRaton + ", tipoEntrada=" + tipoEntrada + ", marca=" + marca + '}';
    }
}