Estas líneas muestran la cantidad de vidas de cada personaje y utilizan etiquetas <span> con identificadores (id) para insertar dinámicamente el nombre del personaje elegido por el jugador y el enemigo.

El span con id="personaje-jugador" se actualiza automáticamente con el nombre del personaje que el jugador selecciona.

El span con id="personaje-enemigo" se completa con el nombre del personaje que la computadora elige aleatoriamente.

De esta forma, el jugador puede ver de manera clara qué personaje está usando y contra quién está luchando, junto con sus respectivas vidas.

📜 Explicación del Código JavaScript
🔹 seleccionarPersonajeJugador()
javascript

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
Esta función se ejecuta cuando el jugador hace clic en el botón "Seleccionar personaje".

Revisa cuál de los personajes fue seleccionado usando inputs tipo radio.

Asigna el nombre del personaje elegido a una variable y lo muestra en pantalla dentro del span con id="personaje-jugador".

Si no se selecciona ninguno, muestra un alert pidiendo que se elija uno.

Finalmente, llama a la función seleccionarPersonajeEnemigo() para que la computadora elija un personaje rival.

🔹 seleccionarPersonajeEnemigo()
javascript

function seleccionarPersonajeEnemigo() {
    const personajes = ["Zuko (Fuego)", "Katara (Agua)", "Aang (Aire)", "Toph (Tierra)"];
    const numeroAleatorio = Math.floor(Math.random() * personajes.length);
    const personajeEnemigo = personajes[numeroAleatorio];

    let spanPersonajeEnemigo = document.getElementById('personaje-enemigo');
    spanPersonajeEnemigo.innerHTML = personajeEnemigo;

    console.log("El enemigo eligió a: " + personajeEnemigo);
}
Esta función selecciona aleatoriamente uno de los personajes disponibles para la computadora.

Usa Math.random() para obtener un índice aleatorio y selecciona un personaje del array personajes.

Luego actualiza el contenido del span con id="personaje-enemigo" para mostrar el personaje enemigo en pantalla.

También lo imprime por consola para fines de prueba o depuración.