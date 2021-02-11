console.log("decision ready!")

// form validation
var current_endowment = endowments[current_round - 1]
console.log(current_endowment)

document.getElementById("id_contribution").addEventListener('input', () => {
    input = parseInt(document.getElementById("id_contribution").value) || 0;
    if (input > current_endowment){
        document.getElementById("id_contribution").className = "form-control border border-danger float-right";
    } else {
        document.getElementById("id_contribution").className = "form-control border border-success float-right";
    }
});

// change button on input
document.getElementById("id_contribution").addEventListener('input', () => {
    input = parseInt(document.getElementById("id_contribution").value) || 0;
    document.getElementById("submit_button").className = "btn-primary btn float-left"
    if (input > 0){
        document.getElementById("submit_button").innerHTML = "Absenden";
    } else {
        document.getElementById("submit_button").innerHTML = "Alles Sparen";
        document.getElementById("id_contribution").value = 0;
    }
});

// submit Form after validation
function submitForm() {
    input = document.getElementById("id_contribution").value
    if (input == "") {
        document.getElementById("id_contribution").value = 0;
    }
    if (input <= current_endowment){
        document.forms[0].submit()
    }
}