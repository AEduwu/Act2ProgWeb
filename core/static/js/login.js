document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");
    const userInput = document.getElementById("user");
    const passwordInput = document.getElementById("password");
    const errorUser = document.getElementById("errorUser");
    const errorPassword = document.getElementById("errorPassword");

    loginForm.addEventListener("submit", function (event) {
        let isValid = true;
        
        errorUser.textContent = "";
        errorPassword.textContent = "";

        if (userInput.value.trim() === "") {
            errorUser.textContent = "El usuario es obligatorio.";
            isValid = false;
        }

        if (passwordInput.value.trim() === "") {
            errorPassword.textContent = "La contraseña es obligatoria.";
            isValid = false;
        }

        if (!isValid) {
            event.preventDefault();
        } else {
            window.location.href = "profile.html";
            event.preventDefault();
        }
    });
});
