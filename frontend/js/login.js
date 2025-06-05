const BASE_URL = "http://127.0.0.1:5000/api";

document.addEventListener("DOMContentLoaded", () => {
  document
    .getElementById("login-form")
    .addEventListener("submit", (evt) => {
      evt.preventDefault();
      attemptLogin();
    });
});

function attemptLogin() {
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!email || !password) {
    showError("Both fields are required.");
    return;
  }

  fetch(`${BASE_URL}/admin/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  })
    .then((res) => {
      if (!res.ok) {
        if (res.status === 401) {
          throw new Error("Invalid email or password.");
        } else {
          throw new Error("Login request failed.");
        }
      }
      return res.json();
    })
    .then(() => {
      // On success, set a “logged in” flag
      localStorage.setItem("isAdminLoggedIn", "true");
      window.location.href = "admin.html";
    })
    .catch((err) => {
      showError(err.message);
    });
}

function showError(msg) {
  document.getElementById("login-error").textContent = msg;
}
