console.log("calculator ready!")

function calculate() {
    yourContribution = parseInt(document.getElementById("yourContribution").value)
    othersContributions = parseInt(document.getElementById("othersContributions").value)
    var yourReturn = Math.ceil((othersContributions * (num_players - 1) + yourContribution) * factor) - yourContribution
    var futureEndowment = endowment + yourReturn

    document.getElementById("yourContributionTable").innerHTML = yourContribution;
    document.getElementById("othersContributionsTable").innerHTML = othersContributions;
    document.getElementById("yourReturnTable").innerHTML = yourReturn;
    document.getElementById("yourReturn").value = yourReturn;
    document.getElementById("yourEndowmentTable").innerHTML = futureEndowment;

    document.getElementById("calculator_button").innerHTML = "Re-calculate";
}

