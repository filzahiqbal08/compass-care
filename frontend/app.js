// Compass Care front end
//
// This file's only job is to call your running API (api.py / finder.py /
// compass_care.db) and draw whatever it sends back. It has no clinic
// logic of its own -- all the real work (distance, filtering, fallback)
// already happened on the backend, verified against the Excel Answer_Key.
//
// IMPORTANT: change API_BASE_URL below once you know where the API is
// actually running (see README.md in this folder).

const API_BASE_URL = "http://127.0.0.1:8000";

const form = document.getElementById("searchForm");
const searchBtn = document.getElementById("searchBtn");
const statusMessage = document.getElementById("statusMessage");
const resultsList = document.getElementById("resultsList");

showEmptyState();

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const zip = document.getElementById("zip").value.trim();
  const siteGroup = document.getElementById("siteGroup").value;
  const service = document.getElementById("service").value;
  const language = document.getElementById("language").value;

  if (!/^\d{5}$/.test(zip)) {
    showError("Please enter a valid 5-digit ZIP code.");
    return;
  }

  await runSearch({ zip, siteGroup, service, language });
});

async function runSearch({ zip, siteGroup, service, language }) {
  setLoading(true);
  hideStatus();
  resultsList.innerHTML = "";

  const params = new URLSearchParams({
    zip,
    site_group: siteGroup,
    service,
    language,
  });

  let data;
  try {
    const response = await fetch(`${API_BASE_URL}/sites?${params.toString()}`);
    if (!response.ok) {
      throw new Error(`Server responded with status ${response.status}`);
    }
    data = await response.json();
  } catch (err) {
    setLoading(false);
    showError(
      "Couldn't reach the Compass Care server. Make sure the API is " +
      "running (see README.md), and that API_BASE_URL in app.js matches " +
      "where it's running."
    );
    console.error(err);
    return;
  }

  setLoading(false);
  renderResults(data);
}

function renderResults(data) {
  if (data.status === "ZIP not found in the list") {
    showError(`We don't recognize ZIP code ${data.zip}. Double check the ZIP and try again.`);
    return;
  }

  if (data.status === "Outside San Diego County: out of scope") {
    showError(`ZIP code ${data.zip} is outside San Diego County, which is the only area Compass Care currently covers.`);
    return;
  }

  if (data.message) {
    showWarning(data.message);
  }

  if (!data.results || data.results.length === 0) {
    resultsList.innerHTML = `<div class="empty-state">No sites found for this search. Try widening your filters.</div>`;
    return;
  }

  resultsList.innerHTML = data.results.map(renderCard).join("");
}

function renderCard(site) {
  const isFallback = site.result_type === "Fallback";
  const services = (site.services && site.services.length)
    ? site.services.map(s => `<span class="meta-chip">${escapeHtml(s)}</span>`).join("")
    : "";

  const languageNote = site.languages
    ? `<p class="result-note"><strong>Languages:</strong> ${escapeHtml(site.languages)}</p>`
    : "";

  const insuranceNote = site.insurance_note
    ? `<p class="result-note"><strong>Insurance:</strong> ${escapeHtml(site.insurance_note)}</p>`
    : "";

  return `
    <article class="result-card ${isFallback ? "fallback" : ""}">
      <div class="result-top">
        <h3 class="result-name">${escapeHtml(site.name)}</h3>
        <span class="result-distance">${site.distance_miles.toFixed(1)} mi</span>
      </div>
      ${isFallback ? `<span class="fallback-tag">Nearest alternative</span>` : ""}
      <p class="result-address">${escapeHtml(site.address)}, ${escapeHtml(site.city)} ${escapeHtml(site.zip5)}</p>
      ${site.phone ? `<p class="result-phone">${escapeHtml(site.phone)}</p>` : ""}
      <div class="result-meta">${services}</div>
      ${languageNote}
      ${insuranceNote}
    </article>
  `;
}

function setLoading(isLoading) {
  searchBtn.disabled = isLoading;
  searchBtn.textContent = isLoading ? "Searching…" : "Search";
  if (isLoading) {
    resultsList.innerHTML = `<div class="loading-state">Looking for clinics near you…</div>`;
  }
}

function showEmptyState() {
  resultsList.innerHTML = `<div class="empty-state">Enter a ZIP code to find nearby clinics.</div>`;
}

function showError(msg) {
  statusMessage.textContent = msg;
  statusMessage.className = "status-message error";
  statusMessage.hidden = false;
}

function showWarning(msg) {
  statusMessage.textContent = msg;
  statusMessage.className = "status-message";
  statusMessage.hidden = false;
}

function hideStatus() {
  statusMessage.hidden = true;
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str ?? "";
  return div.innerHTML;
}
