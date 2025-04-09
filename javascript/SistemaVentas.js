// Clase padre
class DispositivoEntrada {
    constructor(tipoEntrada, marca) {
        this._tipoEntrada = tipoEntrada;
        this._marca = marca;
    }

    get tipoEntrada() {
        return this._tipoEntrada;
    }

    set tipoEntrada(tipoEntrada) {
        this._tipoEntrada = tipoEntrada;
    }

    get marca() {
        return this._marca;
    }

    set marca(marca) {
        this._marca = marca;
    }

    toString() {
        return `Tipo de entrada: ${this._tipoEntrada}, Marca: ${this._marca}`;
    }
}

class Raton extends DispositivoEntrada {
    static contadorRatones = 0;

    constructor(tipoEntrada, marca) {
        super(tipoEntrada, marca);
        this._idRaton = ++Raton.contadorRatones;
    }

    toString() {
        return `Raton [ID: ${this._idRaton}, Tipo Entrada: ${this.tipoEntrada}, Marca: ${this.marca}]`;
    }
}

class Teclado extends DispositivoEntrada {
    static contadorTeclado = 0;

    constructor(tipoEntrada, marca) {
        super(tipoEntrada, marca);
        this._idTeclado = ++Teclado.contadorTeclado;
    }

    toString() {
        return `Teclado [ID: ${this._idTeclado}, Tipo Entrada: ${this.tipoEntrada}, Marca: ${this.marca}]`;
    }
}

// Clase Monitor
class Monitor {
    static contadorMonitores = 0;

    constructor(marca, tamaño) {
        this._idMonitor = ++Monitor.contadorMonitores;
        this._marca = marca;
        this._tamaño = tamaño;
    }

    get idMonitor() {
        return this._idMonitor;
    }

    toString() {
        return `Monitor [ID: ${this._idMonitor}, Marca: ${this._marca}, Tamaño: ${this._tamaño}]`;
    }
}

// Clase Computadora
class Computadora {
    static contadorComputadoras = 0;

    constructor(nombre, monitor, teclado, raton) {
        this._idComputadora = ++Computadora.contadorComputadoras;
        this._nombre = nombre;
        this._monitor = monitor;
        this._teclado = teclado;
        this._raton = raton;
    }

    get idComputadora() {
        return this._idComputadora;
    }

    toString() {
        return `Computadora [ID: ${this._idComputadora}], Nombre: ${this._nombre},\n  ${this._monitor.toString()},\n  ${this._teclado.toString()},\n  ${this._raton.toString()}`;
    }
}

// Clase Orden
class Orden {
    static contadorOrdenes = 0;

    constructor() {
        this._idOrden = ++Orden.contadorOrdenes;
        this._computadoras = [];
    }

    agregarComputadora(computadora) {
        this._computadoras.push(computadora);
    }

    mostrarOrden() {
        let computadorasListadas = '';
        for (let computadora of this._computadoras) {
            computadorasListadas += `\n${computadora.toString()}`;
        }
        return `Orden [ID: ${this._idOrden}], Computadoras:${computadorasListadas}`;
    }

    get idOrden() {
        return this._idOrden;
    }
}

// PRUEBAS
const monitor1 = new Monitor("Samsung", "24 pulgadas");
const teclado1 = new Teclado("USB", "Logitech");
const raton1 = new Raton("Óptico", "HP");
const computadora1 = new Computadora("PC Gamer", monitor1, teclado1, raton1);
console.log(computadora1.toString());

const monitor2 = new Monitor("LG", "27 pulgadas");
const teclado2 = new Teclado("Bluetooth", "Corsair");
const raton2 = new Raton("Inalámbrico", "Razer");
const computadora2 = new Computadora("Laptop Office", monitor2, teclado2, raton2);
console.log(computadora2.toString());

const orden1 = new Orden();
orden1.agregarComputadora(computadora1);
orden1.agregarComputadora(computadora2);
console.log(orden1.mostrarOrden());

console.log(`Total de computadoras creadas: ${Computadora.contadorComputadoras}`);
console.log(`Total de ratones creados: ${Raton.contadorRatones}`);
console.log(`Total de teclados creados: ${Teclado.contadorTeclado}`);
console.log(`Total de monitores creados: ${Monitor.contadorMonitores}`);