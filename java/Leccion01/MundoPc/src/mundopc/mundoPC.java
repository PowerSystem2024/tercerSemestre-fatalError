package mundopc;

import ar.com.system2023.mundopc.*;

public class mundoPC {
    public static void main(String[] args) {
        
        Monitor monitorHP = new Monitor("HP",13); //Importamos la clase
        Monitor monitorGamer = new Monitor("Gamer",32); //Importamos la clase
        Monitor monitorCami = new Monitor("Cami",52);
        Monitor monitorLili = new Monitor("Lili",32);
        Monitor monitorSanti = new Monitor("Santi",24);
        
        Teclado tecladoGamer = new Teclado("Bluetooth","Gamer");
        Teclado tecladoHP = new Teclado("Bluetooth","HP");
        Teclado tecladoCami = new Teclado("Cable","Cami");
        Teclado tecladoLili = new Teclado("Cable","Lili");
        Teclado tecladoSanti = new Teclado("Cable","Santi");
        
        Raton ratonGamer = new Raton("Bluetooth", "Gamer");
        Raton ratonHP = new Raton("Bluetooth", "HP");
        Raton ratonCami = new Raton("Cable","Cami");
        Raton ratonLili = new Raton("Cable","Lili");
        Raton ratonSanti = new Raton("Cable","Santi");
        
        Computadora computadoraHP = new Computadora("Computadora HP",monitorHP,tecladoHP,ratonHP);
        Computadora computadoraGamer = new Computadora("Computadora Gamer",monitorGamer,tecladoGamer,ratonGamer);
        Computadora computadorasVarias = new Computadora("Computadoras de diferentes marcas", monitorHP, tecladoGamer, ratonHP);
        Computadora computadoraCami = new Computadora("computadora de Cami", monitorCami, tecladoCami, ratonCami);
        Computadora computadoraLili = new Computadora("computadora de Lili", monitorLili, tecladoLili, ratonLili);
        Computadora computadoraSanti = new Computadora("Computadoras computadora de Santi", monitorSanti, tecladoSanti, ratonSanti);
        
        Orden orden1 = new Orden();
        Orden orden2 = new Orden();
        Orden orden3 = new Orden();
        Orden orden4 = new Orden();
        Orden orden5 = new Orden();
        Orden orden6 = new Orden();
        Orden orden7 = new Orden();
        Orden orden8 = new Orden();
        Orden orden9 = new Orden();
        Orden orden10 = new Orden();
        Orden orden11 = new Orden();
        
        orden1.agregarComputadora(computadoraHP);
        orden1.agregarComputadora(computadoraGamer);
        orden2.agregarComputadora(computadorasVarias);
        orden3.agregarComputadora(computadoraCami);
        orden3.agregarComputadora(computadorasVarias);
        orden3.agregarComputadora(computadoraHP);
        orden3.agregarComputadora(computadoraGamer);
        orden3.agregarComputadora(computadoraLili);
        orden3.agregarComputadora(computadoraHP);
        orden3.agregarComputadora(computadoraSanti);
        orden3.agregarComputadora(computadoraHP);
        orden3.agregarComputadora(computadoraCami);
        orden3.agregarComputadora(computadoraCami);
        orden3.agregarComputadora(computadoraCami);
        orden3.agregarComputadora(computadoraSanti);
        orden3.agregarComputadora(computadoraSanti);
        
        orden1.mostrarOrden();
        orden2.mostrarOrden();
        orden3.mostrarOrden();
        orden4.mostrarOrden();
        orden5.mostrarOrden();
        orden6.mostrarOrden();
        orden7.mostrarOrden();
        orden8.mostrarOrden();
        orden9.mostrarOrden();
        orden10.mostrarOrden();
        orden11.mostrarOrden();
    }
}
