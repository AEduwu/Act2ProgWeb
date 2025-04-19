$(document).ready(function () {
    $("#forgotForm").submit(function (event) {
        event.preventDefault();
        let isValid = true;

        $(".error-message").hide();
        $(".form-control").removeClass("is-invalid");

        const correo = $("#correo").val().trim();
        if (correo === "") {
            $("#correo").addClass("is-invalid");
            $("#correo").next(".error-message").text("El correo es obligatorio.").show();
            isValid = false;
        }

        if (isValid) {
            $.ajax({
                url: "/recuperar/",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify({ correo: correo }), 
                success: function(response) {
                    alert(response.mensaje || "Se ha enviado un enlace de recuperación al correo ingresado.");
                    $("#recuperarForm")[0].reset();
                },
                error: function(xhr) {
                    const res = xhr.responseJSON;
                    alert(res?.error || "Error al enviar el enlace.");
                }
            });
        }
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
