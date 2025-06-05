const BASE_URL = "http://127.0.0.1:5000/api";

let currentCustomer = null;

// Get customer ID from URL parameters
const urlParams = new URLSearchParams(window.location.search);
const customerId = urlParams.get('customerId');

// Load customer's cart when page loads
document.addEventListener('DOMContentLoaded', async () => {
    if (!customerId) {
        alert('No customer selected');
        goToHome();
        return;
    }
    await loadCart();
});

// Function to return to home page
function goToHome() {
    window.location.href = 'index.html';
}

// Load and display cart contents
async function loadCart() {
    try {
        const response = await fetch(`${BASE_URL}/cart/${customerId}`);
        const cartItems = await response.json();
        
        // Display customer ID
        document.getElementById('current-customer').textContent = `Customer ${customerId}`;
        
        // Calculate total
        let total = 0;
        const cartList = document.getElementById('cart-list');
        cartList.innerHTML = ''; // Clear existing items

        // Display cart items
        cartItems.forEach(item => {
            const itemTotal = item.price * item.quantity;
            total += itemTotal;
            
            cartList.innerHTML += `
                <div class="cart-item">
                    <span>${item.name}</span>
                    <span>$${item.price} x ${item.quantity} = $${itemTotal.toFixed(2)}</span>
                </div>
            `;
        });

        // Add total
        cartList.innerHTML += `
            <div class="cart-total">
                <strong>Total: $${total.toFixed(2)}</strong>
            </div>
        `;

        // Store total for payment processing
        window.cartTotal = total;
    } catch (error) {
        console.error('Error loading cart:', error);
        alert('Error loading cart. Please try again.');
    }
}

function payment(method) {
  const form = document.getElementById("payment-form");
  const submitBtn = document.getElementById("submit-payment");

  form.innerHTML = "";  // Clear previous inputs
  submitBtn.style.display = "block";  // Show the submit button

  let inputsHTML = "";
  if (method === "credit") {
    inputsHTML = `
      <label>Card Number: <input type="text" id="card-number" /></label><br>
      <label>Expiry Date: <input type="text" id="expiry-date" /></label><br>
      <label>CVV: <input type="text" id="cvv" /></label><br>
    `;
  } else if (method === "bank") {
    inputsHTML = `
      <label>Account Number: <input type="text" id="account-number" /></label><br>
      <label>BSB: <input type="text" id="bsb" /></label><br>
    `;
  } else if (method === "thirdparty") {
    inputsHTML = `
      <label>Select Provider:
        <select id="thirdparty-provider">
          <option>PayPal</option>
          <option>AfterPay</option>
          <option>Stripe</option>
        </select>
      </label><br>
    `;
  }

  form.innerHTML = `<h3>${method.toUpperCase()} Payment</h3>` + inputsHTML;

  submitBtn.onclick = () => submitPayment(method);
}

// Handle payment
function submitPayment(method) {
  const params = new URLSearchParams(window.location.search);
  const customerId = params.get("customerId");

  const payload = {
    customerId,
    paymentMethod: method,
  };

  if (method === "credit") {
    payload.payment_details = {
      cardNumber: document.getElementById("card-number").value,
      expiryDate: document.getElementById("expiry-date").value,
      cvv: document.getElementById("cvv").value,
    };
  } else if (method === "bank") {
    payload.payment_details = {
      accountNumber: document.getElementById("account-number").value,
      bsb: document.getElementById("bsb").value,
    };
  } else if (method === "thirdparty") {
    payload.payment_details = {
      provider: document.getElementById("thirdparty-provider").value,
    };
  }

  fetch(`${BASE_URL}/payment`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
    .then(res => res.json())
    .then(data => {
      if (data.status === "success") {
        alert("Payment successful!");
        window.location.href = "index.html";
      } else {
        alert("Payment failed.");
      }
    })
    .catch(err => {
      console.error("Error processing payment:", err);
      alert("An error occurred.");
    });
}
