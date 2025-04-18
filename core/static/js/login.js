  $(document).ready(function () {
    $("#loginForm").submit(function (event) {
        event.preventDefault();
        let isValid = true;

        $(".error-message").hide();
        $(".form-control").removeClass("is-invalid");

        if ($("#user").val().trim() === "") {
            $("#user").addClass("is-invalid");
            $("#user").next(".error-message").text("El correo es obligatorio.").show();
            isValid = false;
        }

        if ($("#password").val().trim() === "") {
            $("#password").addClass("is-invalid");
            $("#password").next(".error-message").text("La contraseña es obligatoria.").show();
            isValid = false;
        }

        if (isValid) {

            const datos = {
                correo: $("#user").val(),
                clave: $("#password").val()
            };
        
            $.ajax({
                url: "/user_login/",
                type: "POST",
                data: JSON.stringify(datos),
                contentType: "application/json",
                success: function (response) {
                    alert(response.mensaje);
                    $("#loginForm")[0].reset();
                     window.location.href = "/catalogo/";
                },
                error: function (xhr) {
                    const res = xhr.responseJSON;
                    alert(res?.error || "Error al iniciar sesión.");
                }
            });


        }
    });
});

