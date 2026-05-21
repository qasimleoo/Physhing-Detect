// Input validation before submit
document.querySelector("form")
.addEventListener("submit", function(e) {

    let username = document.querySelector(
        "input[name='username']"
    ).value.trim();
    
    let password = document.querySelector(
        "input[name='password']"
    ).value.trim();

    // Check empty fields
    if (username === "" || password === "") {
        e.preventDefault();
        alert("Please fill in all fields!");
        return;
    }

    // Check minimum length
    if (password.length < 3) {
        e.preventDefault();
        alert("Password too short!");
        return;
    }
});