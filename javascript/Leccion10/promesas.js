let miPromesa = new Promise((resolver,rechazar) => {
    let expresion = true;
    if(expresion){
        resolver("Se resolvio correctamente");
    } else{
        rechazar("Se produjo un error");
    }
});

/*
miPromesa.then(
    valor => console.log(valor),
    error => console.log(error)
); 
*/

// miPromesa.then(valor => console.log(valor).catch(error => console.log(error)));

let promesa = new Promise((resolver ) => {
    //console.log("Inicio promesa");
    setTimeout( ()=> resolver("Saluditos desde promesa, callback, funcion flecha y setTimeout"),3000);
    //console.log("Final promesa");
});

/*
llamado a promesa
promesa.then(valor => console.log(valor));
*/

//async indica que la funcion regresa una promesa
async function miFuncionConPromesa() {
    return "Saluditos con promesas y async";
}

// miFuncionConPromesa().then(valor => console.log(valor));

//async/await
async function miFuncionConPromesaYAwait() {
    let miPromesa = new Promise(resolver => {
        resolver("Promesa con await");
    });
    console.log(await miPromesa);
}

// miFuncionConPromesaYAwait();

//promesas, await, async y setTimeout
async function miFuncionConPromesaAwaitTimeout() {
    let miPromesa = new Promise(resolver => {
        console.log("Inicia la funcion");
        setTimeout(() => resolver("Promesa con await y Timeout"),3000);
        console.log("Finaliza la funcion");
    });
    console.log(await miPromesa);
}
//llamamos a la funcion
miFuncionConPromesaAwaitTimeout();