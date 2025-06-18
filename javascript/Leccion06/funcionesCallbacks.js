miFuncion1();
miFuncion2();


function miFuncion1() {
    console.log("Mi función 1");
}
function miFuncion2() {
    console.log("Mi función 2");
}

//funcion de tipo callback
let imp = function imprimir(mensaje) {
    console.log(mensaje);
}

function sumar(op1, op2, funcionCallback) {
    let res = op1 + op2;
    funcionCallback(`Resultado: ${res}`);
}

sumar(5, 3, imp);

//llamadas asincronas con uso de setTimeout
function miFuncionCallback() {
    setTimeout(function() {
        console.log("Saludo asincrono despues de 5 segundos");
})
}
setTimeout(miFuncionCallback, 5000);

setTimeout(function() {
    console.log("Saludo asincrono despues de 2 ");
}, 3000);

setTimeout(function() {
    console.log("Saludo asincrono "), 4000});
