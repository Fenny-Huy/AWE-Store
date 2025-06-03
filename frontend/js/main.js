// API endpoints
const API_BASE_URL = 'http://localhost:5000/api';
const ENDPOINTS = {
    products: `${API_BASE_URL}/products`,
    customers: `${API_BASE_URL}/customers`,
    cart: `${API_BASE_URL}/cart`,
    checkout: `${API_BASE_URL}/checkout`
};

// State management
let currentCustomer = null;
let cart = [];

// DOM Elements
const customerSelect = document.getElementById('customer-select');
const productList = document.getElementById('product-list');
const cartList = document.getElementById('cart-list');
const cartTotal = document.getElementById('cart-total');
const checkoutBtn = document.getElementById('checkout-btn');

// Initialize the application
async function init() {
    await loadCustomers();
    await loadProducts();
    setupEventListeners();
}

// Load customers from the API
async function loadCustomers() {
    try {
        console.log('Fetching customers from:', ENDPOINTS.customers);
        const response = await fetch(ENDPOINTS.customers);
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const customers = await response.json();
        console.log('Received customers:', customers);
        
        customerSelect.innerHTML = '<option value="">Select a customer...</option>' +
            customers.map(customer => `<option value="${customer}">${customer}</option>`).join('');
    } catch (error) {
        console.error('Error loading customers:', error);
        console.error('Error details:', {
            message: error.message,
            stack: error.stack
        });
        showError('Failed to load customers');
    }
}

// Load products from the API
async function loadProducts() {
    try {
        const response = await fetch(ENDPOINTS.products);
        const products = await response.json();
        
        productList.innerHTML = products.map(product => `
            <div class="product-card" data-product-id="${product.id}">
                <img src="${product.image || 'https://via.placeholder.com/150'}" alt="${product.name}">
                <h3>${product.name}</h3>
                <p>${product.description || 'No description available'}</p>
                <div class="price">$${product.price.toFixed(2)}</div>
                <button class="add-to-cart" onclick="addToCart('${product.id}')">
                    Add to Cart
                </button>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading products:', error);
        showError('Failed to load products');
    }
}

// Add item to cart
async function addToCart(productId) {
    if (!currentCustomer) {
        showError('Please select a customer first');
        return;
    }

    try {
        const response = await fetch(`${ENDPOINTS.cart}/${currentCustomer}/add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                product_id: productId,
                quantity: 1
            })
        });

        if (!response.ok) throw new Error('Failed to add item to cart');
        
        await updateCart();
        showSuccess('Item added to cart');
    } catch (error) {
        console.error('Error adding to cart:', error);
        showError('Failed to add item to cart');
    }
}

// Update cart display
async function updateCart() {
    if (!currentCustomer) {
        cartList.innerHTML = '<p>Please select a customer</p>';
        cartTotal.textContent = '0.00';
        return;
    }

    try {
        const response = await fetch(`${ENDPOINTS.cart}/${currentCustomer}`);
        if (!response.ok) throw new Error('Failed to fetch cart');
        
        const cartItems = await response.json();
        cart = cartItems;

        if (cartItems.length === 0) {
            cartList.innerHTML = '<p>Your cart is empty</p>';
            cartTotal.textContent = '0.00';
            return;
        }

        let total = 0;
        cartList.innerHTML = cartItems.map(item => {
            total += item.price * item.quantity;
            return `
                <div class="cart-item">
                    <div class="cart-item-details">
                        <h4>${item.name}</h4>
                        <p>$${item.price.toFixed(2)} × ${item.quantity}</p>
                    </div>
                    <div class="cart-item-total">
                        $${(item.price * item.quantity).toFixed(2)}
                    </div>
                </div>
            `;
        }).join('');

        cartTotal.textContent = total.toFixed(2);
    } catch (error) {
        console.error('Error updating cart:', error);
        showError('Failed to update cart');
    }
}

// Remove item from cart
async function removeFromCart(productId) {
    try {
        const response = await fetch(`${ENDPOINTS.cart}/${currentCustomer}/${productId}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Failed to remove item from cart');
        
        await updateCart();
    } catch (error) {
        console.error('Error removing from cart:', error);
        showError('Failed to remove item from cart');
    }
}

// Handle checkout
async function checkout() {
    if (!currentCustomer) {
        showError('Please select a customer first');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/checkout/${currentCustomer}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'Checkout failed');
        }

        showSuccess(`Checkout successful! Order ID: ${result.order_id}`);
        await updateCart(); // Refresh the cart after successful checkout
    } catch (error) {
        console.error('Error during checkout:', error);
        showError(error.message || 'Checkout failed');
    }
}

// Setup event listeners
function setupEventListeners() {
    customerSelect.addEventListener('change', async (e) => {
        currentCustomer = e.target.value;
        await updateCart();
    });

    checkoutBtn.addEventListener('click', checkout);
}

// Utility functions for showing messages
function showError(message) {
    alert(`Error: ${message}`);
}

function showSuccess(message) {
    alert(message);
}

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', init);
