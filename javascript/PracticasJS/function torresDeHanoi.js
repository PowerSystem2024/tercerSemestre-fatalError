function torresDeHanoi(n, origen, destino, auxiliar) {
    if (n === 1) {
        console.log(`Mover disco 1 de ${origen} a ${destino}`);
        return;
    }

    // Mover n-1 discos desde origen a auxiliar
    torresDeHanoi(n - 1, origen, auxiliar, destino);

    // Mover el disco restante a destino
    console.log(`Mover disco ${n} de ${origen} a ${destino}`);

    // Mover los n-1 discos desde auxiliar a destino
    torresDeHanoi(n - 1, auxiliar, destino, origen);
}

// Ejecutar la función con 3 discos
let numeroDeDiscos = 3;
torresDeHanoi(numeroDeDiscos, 'A', 'C', 'B');

