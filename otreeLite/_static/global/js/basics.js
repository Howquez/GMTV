console.log("basics ready!")

// variables from python
let template = js_vars.template || 0;
let endowments = js_vars.endowments || 0;
let current_round  = js_vars.current_round || 0;
let timeout  = js_vars.timeout || 999999999999;

// tooltip
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
})

// popover
var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl)
})

// reverse the table's order
$(function(){
if (template == "results"){ //
    $("tbody").each(function(elem,index){
      var arr = $.makeArray($("tr",this).detach());
      arr.reverse();
        $(this).append(arr);
    });
}
});

// timer & alert
setTimeout(
    function () {
        if (template == "decision"){
            document.getElementById("timeoutModal").classList.add("show")
        }
    },
    (timeout - 0.5) * 60 * 1000
);