async function api(url, options = {}) {
  const res = await fetch(url, { credentials: "same-origin", ...options });
  let data = {};
  try {
    data = await res.json();
  } catch {}
  if (!res.ok) throw new Error(data.detail || data.message || "Request failed");
  return data;
}

function bindAuthForm(id, url, redirect) {
  const form = document.getElementById(id);
  if (!form) return;
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const msg = document.getElementById("formMsg");
    msg.textContent = "Please wait...";
    const payload = Object.fromEntries(new FormData(form).entries());
    try {
      await api(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      location.href = redirect;
    } catch (err) {
      msg.textContent = err.message;
    }
  });
}

async function updateNav() {
  try {
    const data = await api("/api/session-info");
    const login = document.getElementById("loginLink");
    const logout = document.getElementById("logoutBtn");
    if (data.logged_in) {
      login?.classList.add("hidden");
      logout?.classList.remove("hidden");
      logout.onclick = async () => {
        await api("/api/logout", { method: "POST" });
        location.href = "/";
      };
    }
  } catch {}
}

function renderResult(data) {
  const result = document.getElementById("result");
  result.innerHTML = `
    <p class="eyebrow">${data.mode === "gemini" ? "GEMINI AI" : "DEMO FALLBACK"}</p>
    <h2>${escapeHtml(data.summary || "Your recommendation plan")}</h2>
    <div class="allocation">${(data.budget_allocation || []).map((x) => `<div><small>${escapeHtml(x.category)}</small><br><b>₹${Number(x.amount).toLocaleString("en-IN")}</b></div>`).join("")}</div>
    <h3>Suggestions</h3>
    ${(data.recommendations || []).map((x) => `<div class="rec"><div><b>${escapeHtml(x.name)}</b><br><small>${escapeHtml(x.category || "")} · ${escapeHtml(x.platform || "")}</small></div><div><b>₹${Number(x.price || 0).toLocaleString("en-IN")}</b><br>${x.url ? `<a href="${x.url}" target="_blank" rel="noopener">Open platform</a>` : ""}</div></div>`).join("")}
    <h3>Tips</h3><ul>${(data.tips || []).map((x) => `<li>${escapeHtml(x)}</li>`).join("")}</ul>`;
}

function bindPlanner(id) {
  const form = document.getElementById(id);
  if (!form) return;
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const planner = form.dataset.planner,
      msg = document.getElementById("formMsg");
    msg.textContent = "Generating your plan...";
    try {
      let data;
      if (planner === "jewelry") {
        data = await api("/api/generate-jewelry", {
          method: "POST",
          body: new FormData(form),
        });
      } else {
        const fd = new FormData(form),
          payload = Object.fromEntries(fd.entries());
        if (planner === "home") payload.rooms = fd.getAll("rooms");
        payload.budget = Number(payload.budget);
        if (planner === "party") payload.guests = Number(payload.guests);
        data = await api(`/api/generate-${planner}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
      }
      renderResult(data);
      msg.textContent = "";
    } catch (err) {
      msg.textContent = err.message;
    }
  });
}

async function loadDashboard() {
  try {
    const session = await api("/api/session-data");
    document.getElementById("welcome").textContent =
      `Welcome, ${session.user.name}`;
    document.getElementById("stats").innerHTML =
      `<div class="stat"><small>Saved plans</small><b>${session.recommendation_count}</b></div><div class="stat"><small>Email</small><b style="font-size:15px">${escapeHtml(session.user.email)}</b></div>`;

    const history = await api("/api/history");
    document.getElementById("history").innerHTML = history.length
      ? history
          .map(
            (x) =>
              `<div class="history-item"><b>${escapeHtml(x.planner)} planner</b><br><small>${escapeHtml(x.created_at)}</small><br><a href="/api/recommendations-details/${x.id}" target="_blank">View JSON</a>
            <button class="btn" onclick="deletePlan(${x.id})">🗑️ Delete</button>
            </div>`,
          )
          .join("")
      : "<p>No saved plans yet.</p>";
  } catch (e) {
    location.href = "/login";
  }
}

function escapeHtml(v) {
  return String(v ?? "").replace(
    /[&<>"']/g,
    (m) =>
      ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;",
      })[m],
  );
}
document.addEventListener("DOMContentLoaded", updateNav);

async function deletePlan(id) {
  if (!confirm("Are you sure you want to delete this plan?")) return;

  try {
    await api(`/api/recommendations/${id}`, {
      method: "DELETE",
    });

    alert("Plan deleted successfully!");
    loadDashboard();
  } catch (err) {
    alert(err.message);
  }
}
