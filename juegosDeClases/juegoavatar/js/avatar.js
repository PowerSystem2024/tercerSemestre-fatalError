let ataqueJugador
let ataqueEnemigo

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



function seleccionarPersonajeEnemigo() {
    const personajes = ["Zuko (Fuego)", "Katara (Agua)", "Aang (Aire)", "Toph (Tierra)"];
    const numeroAleatorio = Math.floor(Math.random() * personajes.length);
    const personajeEnemigo = personajes[numeroAleatorio];

    let spanPersonajeEnemigo = document.getElementById('personaje-enemigo');
    spanPersonajeEnemigo.innerHTML = personajeEnemigo;

    console.log("El enemigo eligió a: " + personajeEnemigo);
}

function ataquePunio(){
    ataqueJugador = 'Punio'
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

    if(ataqueAleatorio == 1){
        ataqueEnemigo == 'Punio'
    }else if(ataqueAleatorio == 2){
        ataqueEnemigo = 'Patada'
    }else {
        ataqueEnemigo = 'Barrida'
    
    }
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

    // Elegir personaje enemigo
    seleccionarPersonajeEnemigo();
}
