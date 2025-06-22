document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('form-envio');
    const paypalContainer = document.getElementById('paypal-button-container');

    if (form && paypalContainer) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            if (form.checkValidity()) {
                form.classList.remove('was-validated');
                form.style.display = 'none';
                paypalContainer.style.display = '';

                // Renderiza el botón de PayPal SOLO cuando el formulario es válido
                if (typeof paypal !== "undefined") {
                    paypal.Buttons({
                        style: { color: 'blue', shape: 'pill', label: 'pay' },
                        createOrder: function(data, actions) {
                            const total = parseFloat(document.getElementById('carrito-total').textContent.replace(/\./g, '').replace(',', '.'));
                            return actions.order.create({ purchase_units: [{ amount: { value: total } }] });
                        },
                        onApprove: function(data, actions) {
                            return actions.order.capture().then(function(detalles) {
                                // Recoge los datos del formulario
                                const datosEnvio = {
                                    nombre: document.getElementById('nombre').value,
                                    correo: document.getElementById('correo').value,
                                    telefono: document.getElementById('telefono').value,
                                    region: document.getElementById('region').value,
                                    comuna: document.getElementById('comuna').value,
                                    direccion: document.getElementById('direccion').value,
                                    total: document.getElementById('carrito-total').textContent,
                                    items: JSON.parse(localStorage.getItem('carrito') || '[]')
                                };
                                fetch('/registrar-compra/', {
                                    method: 'POST',
                                    credentials: 'same-origin',
                                    headers: {
                                        'Content-Type': 'application/json',
                                        'X-CSRFToken': (document.querySelector('[name=csrfmiddlewaretoken]') || {}).value
                                    },
                                    body: JSON.stringify(datosEnvio)
                                }).then(() => {
                                    localStorage.removeItem('carrito');
                                    window.location.href = "/perfil/";
                                });
                            });
                        },
                        onCancel: function(data) {
                            alert('Pago cancelado');
                        },
                        onError: function(err) {
                            alert('Error al procesar el pago.');
                        }
                    }).render('#paypal-button-container');
                }
            } else {
                form.classList.add('was-validated');
            }
        });
    }
});

