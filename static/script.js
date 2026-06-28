// ===================== TAB NAVIGATION =====================
document.querySelectorAll(".tab-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
    document.querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById(btn.dataset.tab).classList.add("active");
    if (btn.dataset.tab === "dashboard") loadDashboard();
  });
});

// ===================== CHAT =====================
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const chatWindow = document.getElementById("chat-window");

function appendMessage(sender, text) {
  const wrap = document.createElement("div");
  wrap.className = `msg ${sender}`;
  const bubble = document.createElement("span");
  bubble.className = "msg-bubble";
  bubble.textContent = text;
  wrap.appendChild(bubble);
  chatWindow.appendChild(wrap);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

async function sendMessage(message) {
  appendMessage("user", message);
  chatInput.value = "";
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });
    const data = await res.json();
    appendMessage("bot", data.reply || "Sorry, I didn't catch that.");
  } catch (err) {
    appendMessage("bot", "I'm having trouble connecting right now. Please try again.");
  }
}

chatForm.addEventListener("submit", e => {
  e.preventDefault();
  const message = chatInput.value.trim();
  if (message) sendMessage(message);
});

document.querySelectorAll(".chip").forEach(chip => {
  chip.addEventListener("click", () => sendMessage(chip.dataset.msg));
});

// ===================== RISK PREDICTION =====================
const riskForm = document.getElementById("risk-form");
const riskResult = document.getElementById("risk-result");

riskForm.addEventListener("submit", async e => {
  e.preventDefault();
  const formData = new FormData(riskForm);
  const payload = Object.fromEntries(formData.entries());

  const res = await fetch("/api/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  if (data.error) { alert(data.error); return; }

  riskResult.classList.remove("hidden");
  document.getElementById("risk-score-value").textContent = data.risk_score + "%";
  document.getElementById("risk-label-text").textContent = data.risk_label;

  const ring = document.querySelector(".risk-score-ring");
  ring.style.setProperty("--pct", data.risk_score + "%");

  const colorMap = { "Low Risk": "#1F6F62", "Moderate Risk": "#D9A441", "High Risk": "#E2784F" };
  document.getElementById("risk-label-text").style.color = colorMap[data.risk_label] || "#E2784F";

  const list = document.getElementById("risk-factors-list");
  list.innerHTML = "";
  data.top_factors.forEach(f => {
    const li = document.createElement("li");
    li.textContent = f;
    list.appendChild(li);
  });
});

// ===================== DASHBOARD =====================
let riskChartInstance, vitalsChartInstance, adherenceChartInstance;

async function loadDashboard() {
  const [history, reminders, adherence] = await Promise.all([
    fetch("/api/history").then(r => r.json()),
    fetch("/api/reminders").then(r => r.json()),
    fetch("/api/adherence").then(r => r.json())
  ]);

  renderRiskChart(history);
  renderVitalsChart(history);
  renderAdherence(adherence);
  renderReminders(reminders);
}

function renderRiskChart(history) {
  const ctx = document.getElementById("riskChart");
  const labels = history.map(h => h.entry_date);
  const scores = history.map(h => h.risk_score);

  if (riskChartInstance) riskChartInstance.destroy();
  riskChartInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: "Risk Score (%)",
        data: scores,
        borderColor: "#E2784F",
        backgroundColor: "rgba(226,120,79,0.12)",
        tension: 0.35,
        fill: true,
        pointBackgroundColor: "#E2784F",
        pointRadius: 4
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true, max: 100 } }
    }
  });
}

function renderVitalsChart(history) {
  const ctx = document.getElementById("vitalsChart");
  const labels = history.map(h => h.entry_date);

  if (vitalsChartInstance) vitalsChartInstance.destroy();
  vitalsChartInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [
        { label: "Glucose (mg/dL)", data: history.map(h => h.glucose), borderColor: "#1F6F62", tension: 0.35, pointRadius: 3 },
        { label: "BMI", data: history.map(h => h.bmi), borderColor: "#D9A441", tension: 0.35, pointRadius: 3 }
      ]
    },
    options: { responsive: true, plugins: { legend: { position: "bottom" } } }
  });
}

function renderAdherence(adherence) {
  const ctx = document.getElementById("adherenceChart");
  document.getElementById("adherence-pct").textContent = adherence.percentage + "%";

  if (adherenceChartInstance) adherenceChartInstance.destroy();
  adherenceChartInstance = new Chart(ctx, {
    type: "doughnut",
    data: {
      datasets: [{
        data: [adherence.percentage, 100 - adherence.percentage],
        backgroundColor: ["#1F6F62", "#E4F0E9"],
        borderWidth: 0
      }]
    },
    options: { cutout: "75%", plugins: { legend: { display: false }, tooltip: { enabled: false } } }
  });
}

function renderReminders(reminders) {
  const list = document.getElementById("reminders-list");
  list.innerHTML = "";

  if (reminders.length === 0) {
    list.innerHTML = `<li class="empty-state">No reminders yet — add one above.</li>`;
    return;
  }

  reminders.forEach(r => {
    const li = document.createElement("li");
    li.innerHTML = `
      <div class="reminder-meta">
        <strong>${r.med_name}</strong>
        <span>${r.reminder_time} · ${r.frequency}</span>
      </div>
      <button class="take-btn" data-id="${r.id}">Mark as taken</button>
    `;
    list.appendChild(li);
  });

  document.querySelectorAll(".take-btn").forEach(btn => {
    btn.addEventListener("click", async () => {
      await fetch(`/api/reminders/${btn.dataset.id}/taken`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ taken: true })
      });
      btn.textContent = "Taken ✓";
      btn.classList.add("taken");
      const adherence = await fetch("/api/adherence").then(r => r.json());
      renderAdherence(adherence);
    });
  });
}

// Reminder form
document.getElementById("reminder-form").addEventListener("submit", async e => {
  e.preventDefault();
  const formData = new FormData(e.target);
  const payload = Object.fromEntries(formData.entries());

  await fetch("/api/reminders", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  e.target.reset();
  loadDashboard();
});
