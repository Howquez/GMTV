console.log("engines running: donation calculations");

// variables from python
let exchange_rate = js_vars.exchange_rate || 0;

// change content on input
document.getElementById("id_donation").addEventListener('input', () => {
    tokens = parseInt(document.getElementById("id_donation").value) || 0;
    tonsPerToken = 0.01666 * exchange_rate;
    console.log(tonsPerToken)
    kg = tokens * tonsPerToken * 1000

    if(kg<=0){
        document.getElementById("CO2kg").innerHTML = `<small> <br> <br></small>`;
    } else {
        document.getElementById("CO2kg").innerHTML = `<small>Mit einer Spende in Höhe von ${tokens} Punkten würden Sie die europäischen Emissionen um ca. ${Math.floor(kg)} kg verringern.</small>`;
    }
});