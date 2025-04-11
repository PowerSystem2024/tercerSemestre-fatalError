package ventas;

public class Main {
    public static void main(String[] args) {
        Monitor monitor1 = new Monitor("Samsung", "27 pulgadas");
        Teclado teclado1 = new Teclado("USB", "Logitech");
        Raton raton1 = new Raton("USB", "Logitech");

        Computadora compu1 = new Computadora("PC Gamer", monitor1, teclado1, raton1);

        Monitor monitor2 = new Monitor("LG", "24 pulgadas");
        Teclado teclado2 = new Teclado("Bluetooth", "Genius");
        Raton raton2 = new Raton("Bluetooth", "Genius");

        Computadora compu2 = new Computadora("Workstation", monitor2, teclado2, raton2);

        Orden orden1 = new Orden();
        orden1.agregarComputadora(compu1);
        orden1.agregarComputadora(compu2);

        orden1.mostrarOrden();
    }
}