
miFuncion();

function miFuncion(){
    console.log("Saluditos desde mi funcion") 
} 

miFuncion();

let myFuncion = function (){
    console.log("Saluditos desde la funcion anonima")
}

//creamos funcion flecha
let miFuncionFlecha = () => {
    console.log("Saluditos desde mi funcion flecha");
}
//Hay mas variantes para las funciones flechas
miFuncionFlecha();

//en una linea
const saludar = () => console.log("Saluditos a todos desde la funcion flecha");

saludar();

//otro ejemplo
const saludar2 = () => {
    return "Saluditos desde la funcion flecha dos"
}

console.log(saludar2());

//simplificamos la funcion anterior
const saludar3 = () => "Saluditos desde la funcion flecha tres";

console.log(saludar3());

//otro ejemplo
const regresaObjeto = () => ({nombre: "Morena", apellido: "Ruiz"});

console.log(regresaObjeto());

//funciones flecha que reciben parametros 
const funcionParametros = (mensaje) => console.log (mensaje);

funcionParametros("Saluditos desde la funcion con parametros");

//funcion clasica
const funcionParametrosClasica = function (mensaje) {
    console.log (mensaje);
}

funcionParametrosClasica("Saluditos desde la funcion clasica");

//se pueden omitir parentesis en la funcion flecha asi:
const funcionConParametros = mensaje => console.log (mensaje);

funcionConParametros("Otra forma de trabajar con la funcion flecha");

//funciones flecha con varios parametros
//podemos abrir la funcion y tener mas cosas dentro de ella
const funcionConParametros2 = (op1, op2) => {
    let resultado = op1 + op2;
    return resultado;
}
console.log(funcionConParametros2(3,5));