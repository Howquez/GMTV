console.log("join ready!")

// Join the club?

function changeJoinButtonText() {
    btn = document.getElementById("join_id")
    if (btn.innerHTML == "Join") {
        btn.innerHTML = "I'm in!"
    }
    if (btn.innerHTML == "I'm in!") {
            btn.innerHTML = "Join"
        }
}

function changeLeaveButtonText() {
    console.log("hi")
    btn = document.getElementById("leave_id")
    if (btn.innerHTML == "Leave") {
        btn.innerHTML = "I'm out!"
    }
    if (btn.innerHTML == "I'm out!") {
            btn.innerHTML = "Leave"
        }
}
