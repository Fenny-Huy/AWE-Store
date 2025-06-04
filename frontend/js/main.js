// API endpoints
const API_BASE_URL = 'http://localhost:5000/api';
const ENDPOINTS = {
    products: `${API_BASE_URL}/products`,
    customers: `${API_BASE_URL}/customers`,
    cart: `${API_BASE_URL}/cart`,
    checkout: `${API_BASE_URL}/checkout`,
    catalogues: `${API_BASE_URL}/catalogues`
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
    try {
        await Promise.all([
            loadCustomers(),
            loadProducts()
        ]);
        setupEventListeners();
    } catch (error) {
        console.error('Error initializing app:', error);
    }
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
        
        if (Array.isArray(customers)) {
            customerSelect.innerHTML = '<option value="">Select a customer...</option>' +
                customers.map(customer => `<option value="${customer}">${customer}</option>`).join('');
        } else {
            throw new Error('Invalid customer data received');
        }
    } catch (error) {
        console.error('Error loading customers:', error);
        console.error('Error details:', {
            message: error.message,
            stack: error.stack
        });
        showError('Failed to load customers. Please try refreshing the page.');
    }
}

// Load products from the API
async function loadProducts() {
    try {
        const response = await fetch(ENDPOINTS.products);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const products = await response.json();
        
        if (!Array.isArray(products)) {
            throw new Error('Invalid product data received');
        }
        
        productList.innerHTML = products.map(product => `
            <div class="product-card" data-product-id="${product.product_id}">
                <img src="${product.image || 'https://via.placeholder.com/150'}" alt="${product.name}">
                <h3>${product.name}</h3>
                <p>${product.description || 'No description available'}</p>
                <div class="price">$${Number(product.price).toFixed(2)}</div>
                <button class="add-to-cart" onclick="addToCart('${product.product_id}')">
                    Add to Cart
                </button>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading products:', error);
        showError('Failed to load products. Please try refreshing the page.');
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

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to add item to cart');
        }
        
        await updateCart();
        showSuccess('Item added to cart');
    } catch (error) {
        console.error('Error adding to cart:', error);
        showError(error.message);
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
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to fetch cart');
        }
        
        const cartItems = await response.json();
        cart = cartItems;

        if (cartItems.length === 0) {
            cartList.innerHTML = '<p>Your cart is empty</p>';
            cartTotal.textContent = '0.00';
            return;
        }

        let total = 0;
        cartList.innerHTML = cartItems.map(item => {
            const itemTotal = item.price * item.quantity;
            total += itemTotal;
            return `
                <div class="cart-item">
                    <div class="cart-item-details">
                        <h4>${item.name}</h4>
                        <p>$${item.price.toFixed(2)} × ${item.quantity}</p>
                    </div>
                    <div class="cart-item-total">
                        $${itemTotal.toFixed(2)}
                    </div>
                </div>
            `;
        }).join('');

        cartTotal.textContent = total.toFixed(2);
    } catch (error) {
        console.error('Error updating cart:', error);
        showError(error.message);
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

// Handle checkout
async function checkout() {
    if (!currentCustomer) {
        showError('Please select a customer first');
        return;
    }

    try {
        const response = await fetch(`${ENDPOINTS.checkout}/${currentCustomer}`, {
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
        await updateCart();
    } catch (error) {
        console.error('Error during checkout:', error);
        showError(error.message || 'Checkout failed');
    }
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
