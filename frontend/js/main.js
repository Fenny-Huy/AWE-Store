const BASE_URL = "http://127.0.0.1:5000/api";

let currentCustomer = null;

document.addEventListener("DOMContentLoaded", init);

function init() {
  console.log("[DEBUG] init() called");
  loadCustomers();
}

function loadCustomers() {
  console.log("[DEBUG] loadCustomers()");
  fetch(`${BASE_URL}/customers`)
    .then((res) => res.json())
    .then((customers) => {
      console.log("[DEBUG] fetched customers:", customers);
      const select = document.getElementById("customer-select");
      // Preserve the previously selected customer
      const prevCustomer = select.value || currentCustomer;

      select.innerHTML = "";

      if (!Array.isArray(customers) || customers.length === 0) {
        customers = ["guest"];
      }

      customers.forEach((custId) => {
        const opt = document.createElement("option");
        opt.value = custId;
        opt.textContent = custId;
        select.appendChild(opt);
      });

      // Restore previous selection if possible
      if (prevCustomer && customers.includes(prevCustomer)) {
        select.value = prevCustomer;
      }

      currentCustomer = select.value;
      document.getElementById("current-customer").textContent = currentCustomer;

      // Remove previous event listeners before adding a new one
      select.onchange = null;
      select.addEventListener("change", () => {
        currentCustomer = select.value;
        console.log("[DEBUG] customer changed to", currentCustomer);
        document.getElementById("current-customer").textContent = currentCustomer;
        loadProducts();
        loadCart();
      });

      loadProducts();
      loadCart();
    })
    .catch((err) => {
      console.error("[ERROR] failed to load customers:", err);
      // Fallback
      currentCustomer = "guest";
      document.getElementById("current-customer").textContent = currentCustomer;
      loadProducts();
      loadCart();
    });
}

function loadProducts() {
  console.log("[DEBUG] loadProducts() for customer", currentCustomer);
  fetch(`${BASE_URL}/products`)
    .then((res) => res.json())
    .then((products) => {
      const container = document.getElementById("product-list");
      container.innerHTML = "";

      if (!Array.isArray(products) || products.length === 0) {
        container.innerHTML = "<p>No products available.</p>";
        return;
      }

      products.forEach((p) => {
        // Create a container div
        const div = document.createElement("div");
        div.className = "product";

        // Create the name/price/description
        const info = document.createElement("div");
        info.innerHTML = `
          <strong>${p.name}</strong> – $${p.price.toFixed(2)}<br>
          <small>${p.description}</small>
        `;

        // Create the “Add to Cart” button
        const btn = document.createElement("button");
        btn.type = "button"; // ensure it's never treated as a submit
        btn.textContent = "Add to Cart";
        btn.addEventListener("click", (evt) => {
          // Prevent default behavior (shouldn't be needed, but safe)
          evt.preventDefault();
          console.log(
            "[DEBUG] addToCart() called, customer=",
            currentCustomer,
            "productId=",
            p.product_id
          );
          addToCart(p.product_id);
        });

        // Append info and button to the product div
        div.appendChild(info);
        div.appendChild(btn);

        // Add the product div to the container
        container.appendChild(div);
      });
    })
    .catch((err) => {
      console.error("[ERROR] failed to load products:", err);
      document.getElementById("product-list").innerHTML =
        "<p>Failed to load products.</p>";
    });
}

function loadCart() {
  console.log("[DEBUG] loadCart() for customer", currentCustomer);
  if (!currentCustomer) return;

  fetch(`${BASE_URL}/cart/${currentCustomer}`)
    .then((res) => {
      if (!res.ok) throw new Error("Failed to fetch cart");
      return res.json();
    })
    .then((items) => {
      const cartDiv = document.getElementById("cart-list");
      cartDiv.innerHTML = "";

      if (!Array.isArray(items) || items.length === 0) {
        cartDiv.innerHTML = "<p>Your cart is empty.</p>";
        return;
      }

      items.forEach((item) => {
        const div = document.createElement("div");
        div.className = "cart-item";
        div.innerHTML = `
          <strong>${item.name}</strong> – $${item.price.toFixed(
          2
        )} × ${item.quantity}
        `;
        cartDiv.appendChild(div);
      });
    })
    .catch((err) => {
      console.error("[ERROR] failed to load cart:", err);
      document.getElementById("cart-list").innerHTML =
        "<p>Failed to load cart.</p>";
    });
}

function addToCart(productId) {
  if (!currentCustomer) {
    alert("Please select a customer first.");
    return;
  }

  fetch(`${BASE_URL}/cart/${currentCustomer}/add`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ product_id: productId, quantity: 1 }),
  })
    .then((res) => {
      if (!res.ok) throw new Error("Failed to add to cart");
      return res.json();
    })
    .then(() => {
      console.log(
        "[DEBUG] successfully added to cart for",
        currentCustomer
      );
      // Only reload the cart—do NOT reload customers or products
      loadCart();
    })
    .catch((err) => {
      console.error("[ERROR] failed to add to cart:", err);
      alert("Could not add to cart. See console for details.");
    });
}
