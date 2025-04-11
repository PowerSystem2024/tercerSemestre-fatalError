package ventas;

public class Teclado extends DispositivoEntrada {
    private static int contadorTeclados;
    private int idTeclado;

    public Teclado(String tipoEntrada, String marca) {
        super(tipoEntrada, marca);
        this.idTeclado = ++contadorTeclados;
    }

    @Override
    public String toString() {
        return "Teclado{" + "idTeclado=" + idTeclado + ", tipoEntrada=" + tipoEntrada + ", marca=" + marca + '}';
    }
}