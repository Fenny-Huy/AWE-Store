let CUSTOMER_ID = null;
const BASE = "http://127.0.0.1:5000/api";

document.addEventListener("DOMContentLoaded", () => {
  loadCustomers();
});

function loadCustomers() {
  fetch(`${BASE}/customers`)
    .then(res => res.json())
    .then(customers => {
      const select = document.getElementById("customer-select");
      select.innerHTML = "";

      if (customers.length === 0) {
        // if no carts yet, create a default guest
        customers = ["guest"];
      }

      customers.forEach(id => {
        const opt = document.createElement("option");
        opt.value = id;
        opt.textContent = id;
        select.appendChild(opt);
      });

      // set initial customer and load data
      CUSTOMER_ID = select.value;
      select.addEventListener("change", () => {
        CUSTOMER_ID = select.value;
        loadCart();
      });

      // now load products and cart
      loadProducts();
      loadCart();
    });
}

function loadProducts() {
  fetch(`${BASE}/products`)
    .then(res => res.json())
    .then(products => {
      const container = document.getElementById("product-list");
      container.innerHTML = "";
      products.forEach(p => {
        const div = document.createElement("div");
        div.className = "product";
        div.innerHTML = `
          <strong>${p.name}</strong> - $${p.price} - productID${p.id}<br>
          <small>${p.description}</small><br>
          <button onclick="addToCart('${p.id}')">Add to Cart</button>
        `;
        container.appendChild(div);
      });
    });
}

function loadCart() {
  fetch(`${BASE}/cart/${CUSTOMER_ID}`)
    .then(res => res.json())
    .then(items => {
      const cart = document.getElementById("cart-list");
      cart.innerHTML = "";
      if (items.length === 0) {
        cart.innerHTML = "<em>Your cart is empty.</em>";
        return;
      }
      items.forEach(item => {
        const div = document.createElement("div");
        div.className = "cart-item";
        div.innerHTML = `
          <strong>${item.name}</strong> - $${item.price} × ${item.quantity}
        `;
        cart.appendChild(div);
      });
    });
}

function addToCart(productId) {
  fetch(`${BASE}/cart/${CUSTOMER_ID}/add`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ product_id: productId, quantity: 1 })
  })
    .then(res => {
      if (!res.ok) throw new Error("Failed to add to cart.");
      return res.json();
    })
    .then(() => {
      alert("Product added to cart!");
      loadCart();
    })
    .catch(err => alert(err.message));
}

function goToCheckout() {
    const customerId = document.getElementById("customer-select").value;
    window.location.href = `checkout.html?customer_id=${customerId}`;
  }