document.addEventListener("DOMContentLoaded", function () {
  if (typeof paypal !== "undefined") {
    paypal.Buttons({
      style: { color: 'blue', shape: 'pill', label: 'pay' },
      createOrder: function(data, actions) {
        const totalCLP = parseFloat(document.getElementById('carrito-total').textContent.replace(/\./g, '').replace(',', '.'));
        const totalUSD = (totalCLP / 938).toFixed(2);
        localStorage.setItem('totalPagadoUSD', totalUSD);
        return actions.order.create({ purchase_units: [{ amount: { value: totalUSD } }] });
      },
      onApprove: function(data, actions) {
        return actions.order.capture().then(function(detalles) {
          localStorage.setItem('transaccionID', detalles.id || 'N/A');
          window.location.href = 'gracias.html';
        });
      },
      onCancel: function(data) {
        alert('Pago cancelado');
      },
      onError: function(err) {
        console.error('Error al procesar el pago:', err);
        alert('Error al procesar el pago.');
      }
    }).render('#paypal-button-container');
  }
});