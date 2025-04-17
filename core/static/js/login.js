loginForm.addEventListener("submit", function (event) {
    event.preventDefault();
    let isValid = true;

    errorUser.textContent = "";
    errorPassword.textContent = "";

    const email = userInput.value.trim();
    const password = passwordInput.value.trim();

    if (email === "") {
        errorUser.textContent = "El usuario es obligatorio.";
        isValid = false;
    }

    if (password === "") {
        errorPassword.textContent = "La contraseña es obligatoria.";
        isValid = false;
    }

    if (isValid) {
        fetch("/user_login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.mensaje) {
                alert(data.mensaje);
                window.location.href = "/profile/"; 
            } else if (data.error) {
                if (data.error.includes("Usuario")) {
                    errorUser.textContent = data.error;
                } else {
                    errorPassword.textContent = data.error;
                }
            }
        })
        .catch(error => {
            console.error("Error en login:", error);
            alert("Ocurrió un error al intentar iniciar sesión.");
        });
    }
});