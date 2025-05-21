const BASE_URL = "http://127.0.0.1:5000/api";

document.addEventListener("DOMContentLoaded", () => {
    loadProducts();
    loadCart();
});

function loadProducts() {
    fetch(`${BASE_URL}/products`)
        .then(res => res.json())
        .then(products => {
            const container = document.getElementById("product-list");
            container.innerHTML = "";
            products.forEach(p => {
                const div = document.createElement("div");
                div.className = "product";
                div.innerHTML = `
                    <strong>${p.name}</strong> - $${p.price}<br>
                    <small>${p.description}</small><br>
                    <button onclick="addToCart('${p.id}')">Add to Cart</button>
                `;
                container.appendChild(div);
            });
        });
}

function loadCart() {
    fetch(`${BASE_URL}/cart`)
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
    fetch(`${BASE_URL}/cart/add/${productId}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ quantity: 1 })
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
