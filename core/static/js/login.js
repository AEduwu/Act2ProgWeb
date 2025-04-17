document.addEventListener("DOMContentLoaded", () => {
    const loginForm     = document.getElementById("loginForm");
    const userInput     = document.getElementById("user");
    const passwordInput = document.getElementById("password");
    const errorUser     = document.getElementById("errorUser");
    const errorPassword = document.getElementById("errorPassword");
  
    if (!loginForm || !userInput || !passwordInput) {
      console.error("Faltan IDs en el DOM: verifica #loginForm, #user, #password");
      return;
    }
  
    loginForm.addEventListener("submit", (event) => {
      event.preventDefault();
      console.log("Submit capturado");
  
      errorUser.textContent = "";
      errorPassword.textContent = "";
  
      const email    = userInput.value.trim();
      const password = passwordInput.value.trim();
  
      let isValid = true;
      if (!email) {
        errorUser.textContent = "El usuario es obligatorio.";
        isValid = false;
      }
      if (!password) {
        errorPassword.textContent = "La contraseña es obligatoria.";
        isValid = false;
      }
      if (!isValid) return;
  
      console.log("Enviando login:", { email, password });
  
      fetch("/user_login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      })
      .then(res => {
        console.log("Status:", res.status);
        return res.json();
      })
      .then(data => {
        console.log("Respuesta JSON:", data);
        if (data.mensaje) {
          alert(data.mensaje);
          window.location.href = "/profile/";
        } else if (data.error) {
          if (data.error.toLowerCase().includes("usuario")) {
            errorUser.textContent = data.error;
          } else {
            errorPassword.textContent = data.error;
          }
        }
      })
      .catch(err => {
        console.error("Error en fetch:", err);
        alert("Ocurrió un error al intentar iniciar sesión.");
      });
    });
  });