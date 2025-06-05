const BASE_URL = "http://127.0.0.1:5000/api";

document.addEventListener("DOMContentLoaded", () => {
  loadAnalytics();
});

function loadAnalytics() {
  // 1. Fetch sales summary
  fetch(`${BASE_URL}/admin/sales`)
    .then(res => {
      if (!res.ok) throw new Error("Failed to fetch sales summary");
      return res.json();
    })
    .then(summary => {
      document.getElementById("total-orders").textContent = summary.total_orders;
      document.getElementById("total-revenue").textContent = summary.total_revenue.toFixed(2);
      // Now load product names so we can show them next to IDs
      loadProductNames(summary.product_sales);
    })
    .catch(err => {
      console.error("Error loading sales summary:", err);
      alert("Could not load sales analytics. Check console for details.");
    });
}

function loadProductNames(productSales) {
  // Fetch all products to build a map: product_id → name
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
      // Still render with IDs only
      renderProductSales(productSales, {});
    });
}

function renderProductSales(productSales, nameMap) {
  const tbody = document.querySelector("#product-sales-table tbody");
  tbody.innerHTML = "";

  // productSales is an object: { product_id: total_quantity, … }
  // Convert to array of [product_id, qty], sort by qty descending if you like
  const entries = Object.entries(productSales); // [ [pid, qty], … ]
  entries.sort((a, b) => b[1] - a[1]); // Sort from highest qty to lowest

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
