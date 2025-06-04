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

// Handle payment
async function payment(method) {
    if (!customerId || !window.cartTotal) {
        alert('Cannot process payment: Missing customer or cart information');
        return;
    }

    try {
        const orderId = `${Date.now()}-${customerId}`;
        
        const response = await fetch(`${BASE_URL}/payment`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                customerId: customerId,
                orderId: orderId,
                totalCost: window.cartTotal,
                paymentMethod: method
            })
        });

        const result = await response.json();
        
        if (response.ok) {
            alert(`Payment successful!\nOrder ID: ${orderId}\nMethod: ${method}`);
            // Show invoice details if available
            if (result.invoice) {
                console.log('Invoice:', result.invoice);
            }
            // Return to home page after successful payment
            goToHome();
        } else {
            alert(`Payment failed: ${result.message}`);
        }
    } catch (error) {
        console.error('Error processing payment:', error);
        alert('An error occurred while processing payment. Please try again.');
    }
}
