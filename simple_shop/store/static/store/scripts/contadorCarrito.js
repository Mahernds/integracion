function actualizarContadorCarrito(refrescar) {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    let total = carrito.reduce((acc, prod) => acc + prod.cantidad, 0);

    let badge = document.getElementById('contador-carrito');
    if (!badge) {
        // Si no existe el badge, lo crea al lado del botón Carrito
        let btn = document.querySelector('a[href*="carrito"]');
        if (btn) {
            badge = document.createElement('span');
            badge.id = 'contador-carrito';
            badge.className = 'badge bg-danger ms-1';
            btn.appendChild(badge);
        }
    }
    if (badge) {
        badge.textContent = total > 0 ? total : '';
    }
    // Opcional: refresca la página del carrito si se agrega/elimina producto
    if (refrescar && window.location.pathname.includes('carrito')) {
        window.location.reload();
    }
}

// Llama al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    actualizarContadorCarrito(false);
    // Permite que otros scripts llamen a esta función
    window.actualizarContadorCarrito = actualizarContadorCarrito;
});