console.log("basics ready!")

// tooltip
$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

// popover
$(function () {
  $('[data-toggle="popover"]').popover()
})

// reverse the table's order
$(function(){
$("tbody").each(function(elem,index){
  var arr = $.makeArray($("tr",this).detach());
  arr.reverse();
    $(this).append(arr);
});
});

// change button text on input
document.getElementById("id_contribution").addEventListener('input', () => {
    input = parseInt(document.getElementById("id_contribution").value) || 0;
    if (input > 0){
        document.getElementById("submit_button").innerHTML = "Weiter";
    } else {
        document.getElementById("submit_button").innerHTML = "<small>Weiter ohne Investition</small>";
        document.getElementById("id_contribution").value = 0;
    }
});