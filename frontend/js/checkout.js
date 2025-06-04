const BASE_URL = "http://127.0.0.1:5000/api";

let currentCustomer = null;

document.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  currentCustomer = params.get("customer_id");

  if (!currentCustomer) {
    alert("No customer selected.");
    return;
  }

  document.getElementById("current-customer").textContent = currentCustomer;
  loadCart();
});

function loadCart() {
  fetch(`${BASE_URL}/cart/${currentCustomer}`)
    .then(res => res.json())
    .then(items => {
      const cartDiv = document.getElementById("cart-list");
      cartDiv.innerHTML = "";

      if (!Array.isArray(items) || items.length === 0) {
        cartDiv.innerHTML = "<p>Your cart is empty.</p>";
        return;
      }

      items.forEach(item => {
        const div = document.createElement("div");
        div.className = "cart-item";
        div.innerHTML = `
          <strong>${item.name}</strong> – $${item.price.toFixed(2)} × ${item.quantity}
        `;
        cartDiv.appendChild(div);
      });
    })
    .catch(err => {
      console.error("Error loading cart:", err);
      document.getElementById("cart-list").innerHTML =
        "<p>Failed to load cart.</p>";
    });
}

function payment(method) {
  const params = new URLSearchParams(window.location.search);
  const customerId = params.get("customer_id");

  if (!customerId) {
    alert("Customer ID not found.");
    return;
  }

  // First, fetch the cart and calculate total
  fetch(`${BASE_URL}/cart/${customerId}`)
    .then(res => res.json())
    .then(cartItems => {
      if (cartItems.length === 0) {
        alert("Cart is empty.");
        return;
      }

      let totalCost = 0;
      cartItems.forEach(item => {
        totalCost += item.price * item.quantity;
      });

      // Generate a new orderId
      const orderId = `O${Math.random().toString(36).substring(2, 8).toUpperCase()}`;

      // Now send payment request
      return fetch(`${BASE_URL}/payment`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          customerId: customerId,
          orderId: orderId,
          paymentMethod: method,
          totalCost: totalCost.toFixed(2)
        })
      });
    })
    .then(res => {
      if (!res) return;
      return res.json().then(data => {
        if (res.ok) {
          alert("Payment successful!");
          window.location.href = "index.html";
          loadCart();
        } else {
          alert("Payment failed: " + data.message);
        }
      });
    })
    .catch(err => {
      console.error("Payment error:", err);
      alert("Something went wrong during payment.");
    });

  
}


function goToHome() {
  window.location.href = `index.html`;
}
