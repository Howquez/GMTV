console.log("basics ready!")

// variables from python
let template = js_vars.template || 0;
let endowments = js_vars.endowments || 0;
let current_round  = js_vars.current_round || 0;

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
if (template != "decision"){
    $("tbody").each(function(elem,index){
      var arr = $.makeArray($("tr",this).detach());
      arr.reverse();
        $(this).append(arr);
    });
}
});

// change button text on input
if (document.getElementById("id_contribution")){
    document.getElementById("id_contribution").addEventListener('input', () => {
    input = parseInt(document.getElementById("id_contribution").value) || 0;
    if (input > 0){
        document.getElementById("submit_button").innerHTML = "Weiter";
    } else {
        document.getElementById("submit_button").innerHTML = "<small>Weiter ohne Investition</small>";
        document.getElementById("id_contribution").value = 0;
    }
});
}

// submit in case you don't use buttons
function submitPage() {
    document.forms[0].submit()
}