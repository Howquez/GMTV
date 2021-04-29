console.log("engines running: clicktracking");

function countClicks(button){
	var element = "id_review_" + button
	var oldValue = parseInt(document.getElementById(element).value);
	var newValue = oldValue+1;
	document.getElementById(element).value = newValue;
}

document.getElementById("contact_icon").addEventListener("click", function() {
    countClicks("contact");
}, false);

document.getElementById("instructions_icon").addEventListener("click", function() {
    countClicks("instructions");
}, false);

document.getElementById("instructions_text").addEventListener("click", function() {
    countClicks("instructions");
}, false);

