// Variables globales
let tablero = [];
let movimientos = [];
let posicionActual = { x: 0, y: 0 };
let contadorMovimientos = 0;
let tiempoEspera = 500;
let tourEnProgreso = false;
let tourPausado = false;
let pasoActual = 0;
let proximoMovimiento = null;

// Posibles movimientos del caballo
const movimientosPosibles = [
    { x: 2, y: 1 },
    { x: 1, y: 2 },
    { x: -1, y: 2 },
    { x: -2, y: 1 },
    { x: -2, y: -1 },
    { x: -1, y: -2 },
    { x: 1, y: -2 },
    { x: 2, y: -1 }
];

// Inicializar el tablero
function inicializarTablero() {
    const contenedorTablero = document.getElementById('tablero');
    contenedorTablero.innerHTML = '';
    tablero = [];
    
    for (let fila = 0; fila < 8; fila++) {
        tablero[fila] = [];
        for (let columna = 0; columna < 8; columna++) {
            const casilla = document.createElement('div');
            casilla.className = `casilla ${(fila + columna) % 2 === 0 ? 'blanca' : 'negra'}`;
            casilla.id = `casilla-${fila}-${columna}`;
            contenedorTablero.appendChild(casilla);
            tablero[fila][columna] = 0;
        }
    }
}

// Verificar si una posición es válida
function esPosicionValida(x, y) {
    return x >= 0 && x < 8 && y >= 0 && y < 8 && tablero[x][y] === 0;
}

// Obtener movimientos válidos desde una posición
function obtenerMovimientosValidos(x, y) {
    return movimientosPosibles
        .map(mov => ({ x: x + mov.x, y: y + mov.y }))
        .filter(pos => esPosicionValida(pos.x, pos.y));
}

// Heurística de Warnsdorff: ordenar movimientos por número de opciones futuras
function ordenarPorWarnsdorff(movimientos, x, y) {
    return movimientos.sort((a, b) => {
        const opcionesA = obtenerMovimientosValidos(a.x, a.y).length;
        const opcionesB = obtenerMovimientosValidos(b.x, b.y).length;
        return opcionesA - opcionesB;
    });
}

// Actualizar la visualización del tablero
function actualizarTablero() {
    for (let fila = 0; fila < 8; fila++) {
        for (let columna = 0; columna < 8; columna++) {
            const casilla = document.getElementById(`casilla-${fila}-${columna}`);
            if (tablero[fila][columna] > 0) {
                if (tablero[fila][columna] === pasoActual) {
                    casilla.innerHTML = '<span class="caballo">♞</span>';
                } else {
                    casilla.innerHTML = '<span style="color: #666; font-weight: bold;">X</span>';
                }
                casilla.classList.add('visitada');
            } else {
                casilla.innerHTML = '';
                casilla.classList.remove('visitada');
            }
        }
    }
}

// Función principal de backtracking
async function resolverTour(x, y, paso) {
    if (paso === 64) {
        return true;
    }

    let movimientosValidos = obtenerMovimientosValidos(x, y);
    movimientosValidos = ordenarPorWarnsdorff(movimientosValidos, x, y);
    
    for (const mov of movimientosValidos) {
        if (tourPausado) {
            proximoMovimiento = { x: mov.x, y: mov.y, paso: paso };
            return false;
        }

        tablero[mov.x][mov.y] = paso + 1;
        pasoActual = paso + 1;
        actualizarTablero();
        
        if (!tourPausado) {
            await new Promise(resolve => setTimeout(resolve, tiempoEspera));
        }

        if (await resolverTour(mov.x, mov.y, paso + 1)) {
            return true;
        }

        tablero[mov.x][mov.y] = 0;
        pasoActual = paso;
        actualizarTablero();
        
        if (!tourPausado) {
            await new Promise(resolve => setTimeout(resolve, tiempoEspera));
        }
    }

    return false;
}

// Iniciar el tour del caballo
async function iniciarTour() {
    if (tourEnProgreso) return;
    
    tourEnProgreso = true;
    tourPausado = false;
    actualizarBotones();
    
    inicializarTablero();
    tablero[0][0] = 1;
    pasoActual = 1;
    actualizarTablero();
    
    if (await resolverTour(0, 0, 1)) {
        alert('¡Tour completado con éxito!');
    } else if (!tourPausado) {
        alert('No se encontró una solución.');
    }
    
    tourEnProgreso = false;
    actualizarBotones();
}

// Pausar el tour
function pausarTour() {
    if (!tourEnProgreso) return;
    
    tourPausado = !tourPausado;
    document.getElementById('btnPausar').textContent = tourPausado ? 'Continuar' : 'Pausar';
    document.getElementById('btnPaso').disabled = !tourPausado;
}

// Avanzar paso a paso
async function pasoSiguiente() {
    if (!tourPausado || !proximoMovimiento) return;
    
    const { x, y, paso } = proximoMovimiento;
    tablero[x][y] = paso + 1;
    pasoActual = paso + 1;
    actualizarTablero();
    
    proximoMovimiento = null;
    await resolverTour(x, y, paso + 1);
}

// Reiniciar el tablero
function reiniciar() {
    tourEnProgreso = false;
    tourPausado = false;
    proximoMovimiento = null;
    actualizarBotones();
    inicializarTablero();
}

// Actualizar estado de los botones
function actualizarBotones() {
    document.getElementById('btnIniciar').disabled = tourEnProgreso;
    document.getElementById('btnPausar').disabled = !tourEnProgreso;
    document.getElementById('btnPaso').disabled = !tourPausado;
    document.getElementById('btnReiniciar').disabled = tourEnProgreso && !tourPausado;
}

// Actualizar velocidad
document.getElementById('velocidad').addEventListener('input', function(e) {
    tiempoEspera = parseInt(e.target.value);
    document.getElementById('velocidad-valor').textContent = tiempoEspera + 'ms';
});

// Inicializar el tablero al cargar la página
window.onload = inicializarTablero; 