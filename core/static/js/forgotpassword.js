document.addEventListener("DOMContentLoaded", function () {
    const registroForm = document.getElementById("registroForm");
    const emailInput = document.getElementById("email");
    const errorEmail = document.getElementById("errorEmail");

    registroForm.addEventListener("submit", function (event) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        errorEmail.textContent = "";

        if (!emailRegex.test(emailInput.value.trim())) {
            errorEmail.textContent = "Ingrese un correo electrónico válido.";
            event.preventDefault();
        }
    });
});