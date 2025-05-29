const BASE = "http://127.0.0.1:5000/api";

const urlParams = new URLSearchParams(window.location.search);
const CUSTOMER_ID = urlParams.get("customer_id");
document.getElementById("cart-header").textContent = `Shopping cart for: ${CUSTOMER_ID}`;


document.addEventListener("DOMContentLoaded", () => {
  if (!CUSTOMER_ID) {
    document.body.innerHTML = "<p>Error: No customer selected.</p>";
    return;
  }

  loadCart();
});

function loadCart() {
  fetch(`${BASE}/cart/${CUSTOMER_ID}`)
    .then(res => res.json())
    .then(items => {
      const cart = document.getElementById("cart-list");
      cart.innerHTML = "";

      if (!items || items.length === 0) {
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
    })
    .catch(err => {
      console.error("Error loading cart:", err);
    });
}

function payment(method) {
    fetch(`${BASE}/payment`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            orderId: "A123",
            customerId: CUSTOMER_ID,
            totalCost: 199.99,
            paymentMethod: method
        })
    })
    .then(response => response.json())
    .then(data => alert(data.message));
}

function goToHome() {
    window.location.href = `index.html`;
  }
