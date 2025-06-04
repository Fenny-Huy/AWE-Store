const BASE_URL = "http://127.0.0.1:5000/api";

let currentCustomer = null;
let currentCatalogue = null;  // will hold the selected catalogue_id

document.addEventListener("DOMContentLoaded", init);

function init() {
  loadCustomers();
  loadCatalogues();

  // Bind checkout button
  const checkoutBtn = document.getElementById("checkout-button");
    if (checkoutBtn) {
      checkoutBtn.addEventListener("click", () => {
        if (!currentCustomer) {
          alert("Please select a customer before checking out.");
          return;
        }

        // Simply redirect — do NOT create an order yet
        window.location.href = `checkout.html?customer_id=${currentCustomer}`;
      });
    }
  }

// ─────────────────────────────────────────────────────────────
// 1. Load and build the “Active Customer” dropdown
// ─────────────────────────────────────────────────────────────
function loadCustomers() {
  fetch(`${BASE_URL}/customers`)
    .then(res => res.json())
    .then(customers => {
      const select = document.getElementById("customer-select");
      select.innerHTML = "";

      if (!Array.isArray(customers) || customers.length === 0) {
        customers = ["guest"];
      }

      customers.forEach(custId => {
        const opt = document.createElement("option");
        opt.value = custId;
        opt.textContent = custId;
        select.appendChild(opt);
      });

      // Set initial customer
      currentCustomer = select.value;
      document.getElementById("current-customer").textContent = currentCustomer;

      select.addEventListener("change", () => {
        currentCustomer = select.value;
        document.getElementById("current-customer").textContent = currentCustomer;
        loadCart();
      });

      // Initial load of cart
      loadCart();
    })
    .catch(err => {
      console.error("Error loading customers:", err);
      currentCustomer = "guest";
      document.getElementById("current-customer").textContent = currentCustomer;
      loadCart();
    });
}

// ─────────────────────────────────────────────────────────────
// 2. Load and build the “Choose Catalogue” dropdown
// ─────────────────────────────────────────────────────────────
function loadCatalogues() {
  fetch(`${BASE_URL}/catalogues`)
    .then(res => res.json())
    .then(catalogues => {
      const select = document.getElementById("catalogue-select");
      select.innerHTML = "";

      // Add an “All Products” option
      const allOpt = document.createElement("option");
      allOpt.value = "ALL";
      allOpt.textContent = "All Products";
      select.appendChild(allOpt);

      // Populate with each catalogue
      catalogues.forEach(cat => {
        const opt = document.createElement("option");
        opt.value = cat.catalogue_id;
        opt.textContent = cat.name;
        select.appendChild(opt);
      });

      // Set initial catalogue to “All”
      currentCatalogue = "ALL";

      select.addEventListener("change", () => {
        currentCatalogue = select.value;
        loadProducts();
      });

      // Initial load of products
      loadProducts();
    })
    .catch(err => {
      console.error("Error loading catalogues:", err);
      // If error, default to “All Products”
      currentCatalogue = "ALL";
      loadProducts();
    });
}

// ─────────────────────────────────────────────────────────────
// 3. Load products for the chosen catalogue (or all if “ALL”)
// ─────────────────────────────────────────────────────────────
function loadProducts() {
  let url;
  if (currentCatalogue === "ALL") {
    url = `${BASE_URL}/products`;
  } else {
    url = `${BASE_URL}/catalogues/${currentCatalogue}/products`;
  }

  fetch(url)
    .then(res => res.json())
    .then(products => {
      const container = document.getElementById("product-list");
      container.innerHTML = "";

      if (!Array.isArray(products) || products.length === 0) {
        container.innerHTML = "<p>No products available in this catalogue.</p>";
        return;
      }

      products.forEach(p => {
        const div = document.createElement("div");
        div.className = "product";

        const info = document.createElement("div");
        info.innerHTML = `
          <strong>${p.name}</strong> – $${p.price.toFixed(2)}<br>
          <small>${p.description}</small>
        `;

        const btn = document.createElement("button");
        btn.type = "button";
        btn.textContent = "Add to Cart";
        btn.addEventListener("click", evt => {
          evt.preventDefault();
          addToCart(p.product_id);
        });

        div.appendChild(info);
        div.appendChild(btn);
        container.appendChild(div);
      });
    })
    .catch(err => {
      console.error("Error loading products:", err);
      document.getElementById("product-list").innerHTML =
        "<p>Failed to load products.</p>";
    });
}

// ─────────────────────────────────────────────────────────────
// 4. Load the current customer’s cart items
// ─────────────────────────────────────────────────────────────
function loadCart() {
  if (!currentCustomer) return;
  fetch(`${BASE_URL}/cart/${currentCustomer}`)
    .then(res => {
      if (!res.ok) throw new Error("Failed to fetch cart");
      return res.json();
    })
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

// ─────────────────────────────────────────────────────────────
// 5. Add a product to the current customer’s cart
// ─────────────────────────────────────────────────────────────
function addToCart(productId) {
  if (!currentCustomer) {
    return alert("Please select a customer first.");
  }

  fetch(`${BASE_URL}/cart/${currentCustomer}/add`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ product_id: productId, quantity: 1 })
  })
    .then(res => {
      if (!res.ok) throw new Error("Failed to add to cart");
      return res.json();
    })
    .then(() => {
      loadCart();
    })
    .catch(err => {
      console.error("Error adding to cart:", err);
      alert("Could not add to cart. See console for details.");
    });
}