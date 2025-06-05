// frontend/js/admin.js

const BASE_URL = "http://127.0.0.1:5000/api";

document.addEventListener("DOMContentLoaded", () => {
  // 1) Check again in case the user removed localStorage manually
  const loggedIn = localStorage.getItem("isAdminLoggedIn");
  if (loggedIn !== "true") {
    window.location.href = "login.html";
    return;
  }

  setupLogoutButton();
  loadAnalytics();
});

function setupLogoutButton() {
  const btn = document.getElementById("logout-button");
  btn.addEventListener("click", () => {
    localStorage.removeItem("isAdminLoggedIn");
    window.location.href = "login.html";
  });
}

function loadAnalytics() {
  fetch(`${BASE_URL}/admin/sales`)
    .then(res => {
      if (!res.ok) throw new Error("Failed to fetch sales summary");
      return res.json();
    })
    .then(summary => {
      document.getElementById("total-orders").textContent = summary.total_orders;
      document.getElementById("total-revenue").textContent = summary.total_revenue.toFixed(2);
      loadProductNames(summary.product_sales);
    })
    .catch(err => {
      console.error("Error loading sales summary:", err);
      alert("Could not load sales analytics. Check console.");
    });
}

function loadProductNames(productSales) {
  fetch(`${BASE_URL}/products`)
    .then(res => {
      if (!res.ok) throw new Error("Failed to fetch product list");
      return res.json();
    })
    .then(products => {
      const nameMap = {};
      products.forEach(p => {
        nameMap[p.product_id] = p.name;
      });
      renderProductSales(productSales, nameMap);
    })
    .catch(err => {
      console.error("Error loading products for analytics:", err);
      renderProductSales(productSales, {});
    });
}

function renderProductSales(productSales, nameMap) {
  const tbody = document.querySelector("#product-sales-table tbody");
  tbody.innerHTML = "";

  const entries = Object.entries(productSales);
  entries.sort((a, b) => b[1] - a[1]);

  entries.forEach(([pid, qty]) => {
    const tr = document.createElement("tr");
    const name = nameMap[pid] || "(unknown)";

    tr.innerHTML = `
      <td>${pid}</td>
      <td>${name}</td>
      <td>${qty}</td>
    `;
    tbody.appendChild(tr);
  });

  if (entries.length === 0) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td colspan="3"><em>No products sold yet.</em></td>`;
    tbody.appendChild(tr);
  }
}
