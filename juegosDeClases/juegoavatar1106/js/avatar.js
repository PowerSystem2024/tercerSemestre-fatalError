let ataqueJugador
let ataqueEnemigo

window.addEventListener('load', iniciarJuego)

function iniciarJuego(){
    let botonPersonajeJugador = document.getElementById('boton-personaje');
    botonPersonajeJugador.addEventListener('click', seleccionarPersonajeJugador);
    
    let botonPunio = document.getElementById('boton-punio')
    botonPunio.addEventListener('click', ataquePunio)

    let botonPatada = document.getElementById('boton-patada')
    botonPatada.addEventListener('click', ataquePatada)

    let botonBarrida = document.getElementById('boton-barrida')
    botonBarrida.addEventListener('click', ataqueBarrida)
}

function seleccionarPersonajeJugador() {
    let personajeSeleccionado = "";
    let spanPersonajeJugador = document.getElementById('personaje-jugador');

    if (document.getElementById('zuko').checked) {
        personajeSeleccionado = "Zuko (Fuego)";
    } else if (document.getElementById('katara').checked) {
        personajeSeleccionado = "Katara (Agua)";
    } else if (document.getElementById('aang').checked) {
        personajeSeleccionado = "Aang (Aire)";
    } else if (document.getElementById('toph').checked) {
        personajeSeleccionado = "Toph (Tierra)";
    } else {
        alert("Por favor, selecciona un personaje");
        return;
    }

    spanPersonajeJugador.innerHTML = personajeSeleccionado;
    alert("Has seleccionado a " + personajeSeleccionado);

    seleccionarPersonajeEnemigo();
}

function seleccionarPersonajeEnemigo() {
    const personajes = ["Zuko (Fuego)", "Katara (Agua)", "Aang (Aire)", "Toph (Tierra)"];
    const numeroAleatorio = Math.floor(Math.random() * personajes.length);
    const personajeEnemigo = personajes[numeroAleatorio];

    let spanPersonajeEnemigo = document.getElementById('personaje-enemigo');
    spanPersonajeEnemigo.innerHTML = personajeEnemigo;
}

function ataquePunio(){
    ataqueJugador = 'Puño'
    ataqueAleatorioEnemigo()
}

function ataquePatada(){
    ataqueJugador = 'Patada'
    ataqueAleatorioEnemigo()
}

function ataqueBarrida(){
    ataqueJugador = 'Barrida'
    ataqueAleatorioEnemigo()
}

function ataqueAleatorioEnemigo(){
    let ataqueAleatorio = aleatorio(1, 3)

    if(ataqueAleatorio === 1){
        ataqueEnemigo = 'Puño'
    } else if(ataqueAleatorio === 2){
        ataqueEnemigo = 'Patada'
    } else {
        ataqueEnemigo = 'Barrida'
    }

    combate()  // Ahora se ejecuta el combate luego de elegir ataque enemigo
}

function combate(){
    let resultado = ""

    if(ataqueEnemigo === ataqueJugador){
        resultado = "EMPATE"
    } else if(ataqueJugador === 'Puño' && ataqueEnemigo === 'Barrida'){
        resultado = "GANASTE"
    } else if(ataqueJugador === 'Patada' && ataqueEnemigo === 'Puño'){
        resultado = "GANASTE"
    } else if(ataqueJugador === 'Barrida' && ataqueEnemigo === 'Patada'){
        resultado = "GANASTE"
    } else {
        resultado = "PERDISTE"
    }

    crearMensaje(resultado)
}

function crearMensaje(resultado){
    let sectionMensaje = document.getElementById('mensajes')
    let parrafo = document.createElement('p')

    parrafo.innerHTML = `Tu personaje atacó con <strong>${ataqueJugador}</strong>, el personaje del enemigo atacó con <strong>${ataqueEnemigo}</strong> → <strong>${resultado}</strong>`
    sectionMensaje.appendChild(parrafo)
}

function aleatorio(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}
