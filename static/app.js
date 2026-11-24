const form = document.querySelector("#client-form");
const message = document.querySelector("#form-message");
const list = document.querySelector("#client-list");

function showClients(clients) {
  list.replaceChildren();
  if (!clients.length) {
    list.innerHTML = "<li>No clients yet.</li>";
    return;
  }
  clients.forEach((client) => {
    const item = document.createElement("li");
    const name = document.createElement("strong");
    const email = document.createElement("span");
    const goal = document.createElement("small");
    name.textContent = client.name;
    email.textContent = client.email;
    goal.textContent = client.goal || "Goal not set";
    item.append(name, email, goal);
    list.append(item);
  });
}

async function loadClients() {
  const response = await fetch("/api/clients");
  const body = await response.json();
  showClients(body.clients || []);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = Object.fromEntries(new FormData(form).entries());
  const response = await fetch("/api/clients", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const body = await response.json();
  message.textContent = response.ok ? "Client added." : body.error;
  if (response.ok) {
    form.reset();
    await loadClients();
  }
});

document.querySelector("#refresh").addEventListener("click", loadClients);
loadClients();

