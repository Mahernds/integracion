function agregarAlCarrito(producto) {
  let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
  const idx = carrito.findIndex(p => p.id == producto.id);
  if (idx !== -1) {
    carrito[idx].cantidad += 1;
  } else {
    carrito.push({ ...producto, cantidad: 1 });
  }
  localStorage.setItem('carrito', JSON.stringify(carrito));
  if (window.actualizarContadorCarrito) window.actualizarContadorCarrito(true);
}

document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.agregar-carrito-btn').forEach(btn => {
    btn.addEventListener('click', function () {
      agregarAlCarrito({
        id: this.dataset.id,
        nombre: this.dataset.nombre,
        precio: parseInt(this.dataset.precio),
        imagen: this.dataset.imagen
      });
      mostrarAlertaCarrito('Producto agregado al carrito');
    });
  });
});

function mostrarAlertaCarrito(mensaje) {
  const alerta = document.getElementById('alerta-carrito');
  const mensajeSpan = document.getElementById('alerta-carrito-mensaje');
  if (alerta && mensajeSpan) {
    mensajeSpan.textContent = mensaje;
    alerta.style.display = '';
    alerta.classList.add('show');
    setTimeout(() => {
      alerta.classList.remove('show');
      alerta.style.display = 'none';
    }, 2000);
  }
}

function renderizarCarrito() {
  const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
  const tbody = document.getElementById('carrito-items');
  const vacio = document.getElementById('carrito-vacio');
  const contenido = document.getElementById('carrito-contenido');
  const totalSpan = document.getElementById('carrito-total');
  let total = 0;

  if (!tbody || !vacio || !contenido || !totalSpan) return;

  tbody.innerHTML = '';
  if (carrito.length === 0) {
    vacio.style.display = '';
    contenido.style.display = 'none';
    totalSpan.textContent = '0';
    return;
  }

  vacio.style.display = 'none';
  contenido.style.display = '';

  carrito.forEach((prod, idx) => {
    const subtotal = prod.precio * prod.cantidad;
    total += subtotal;
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>
        <img src="${prod.imagen}" alt="${prod.nombre}" style="width:60px; height:60px; object-fit:cover; border-radius:8px; margin-right:8px;">
        ${prod.nombre}
      </td>
      <td>$${prod.precio}</td>
      <td>
        <input type="number" min="1" value="${prod.cantidad}" data-idx="${idx}" class="form-control form-control-sm cantidad-carrito" style="width:70px;">
      </td>
      <td>$${subtotal}</td>
      <td>
        <button class="btn btn-danger btn-sm eliminar-item-carrito" data-idx="${idx}">Eliminar</button>
      </td>
    `;
    tbody.appendChild(tr);
  });

  totalSpan.textContent = total;

  // Eliminar producto
  document.querySelectorAll('.eliminar-item-carrito').forEach(btn => {
    btn.onclick = function () {
      const idx = this.dataset.idx;
      carrito.splice(idx, 1);
      localStorage.setItem('carrito', JSON.stringify(carrito));
      if (window.actualizarContadorCarrito) window.actualizarContadorCarrito(true);
      renderizarCarrito();
    };
  });

  // Cambiar cantidad
  document.querySelectorAll('.cantidad-carrito').forEach(input => {
    input.onchange = function () {
      const idx = this.dataset.idx;
      let val = parseInt(this.value);
      if (val < 1) val = 1;
      carrito[idx].cantidad = val;
      localStorage.setItem('carrito', JSON.stringify(carrito));
      if (window.actualizarContadorCarrito) window.actualizarContadorCarrito(true);
      renderizarCarrito();
    };
  });
}

// Renderiza el carrito al cargar la página del carrito
document.addEventListener('DOMContentLoaded', function () {
  if (document.getElementById('carrito-items')) {
    renderizarCarrito();
  }
});