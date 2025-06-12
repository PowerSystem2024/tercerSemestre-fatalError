const numDiscos = 4; // Cambia este número para más discos
const torres = {
  A: document.getElementById("A"),
  B: document.getElementById("B"),
  C: document.getElementById("C")
};

// Crear discos y agregarlos a la torre A
const discos = [];
for (let i = numDiscos; i >= 1; i--) {
  const disco = document.createElement("div");
  disco.className = "disk";
  disco.style.width = `${i * 25}px`;
  disco.style.zIndex = i;
  disco.setAttribute("data-size", i);
  torres.A.appendChild(disco);
  discos[i] = disco;
}

let pasos = [];

function torresDeHanoi(n, origen, destino, auxiliar) {
  if (n === 1) {
    pasos.push([origen, destino]);
    return;
  }
  torresDeHanoi(n - 1, origen, auxiliar, destino);
  pasos.push([origen, destino]);
  torresDeHanoi(n - 1, auxiliar, destino, origen);
}

torresDeHanoi(numDiscos, "A", "C", "B");

async function animarMovimientos() {
  for (let [origen, destino] of pasos) {
    await new Promise(resolve => setTimeout(resolve, 600));
    const torreOrigen = torres[origen];
    const torreDestino = torres[destino];
    const disco = torreOrigen.querySelector(".disk:last-child");
    if (disco) {
      torreDestino.appendChild(disco);
    }
  }
}

animarMovimientos();