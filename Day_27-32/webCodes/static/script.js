// ============================================================
// Crop emoji mapping
// ============================================================
const CROP_EMOJI = {
    Rice:         "🌾", Maize:       "🌽", ChickPea:    "🫘",
    KidneyBeans:  "🫘", PigeonPeas:  "🌿", MothBeans:   "🌱",
    MungBean:     "🌱", Blackgram:   "🫘", Lentil:      "🫘",
    Pomegranate:  "🍎", Banana:      "🍌", Mango:       "🥭",
    Grapes:       "🍇", Watermelon:  "🍉", Muskmelon:   "🍈",
    Apple:        "🍎", Orange:      "🍊", Papaya:      "🍈",
    Coconut:      "🥥", Cotton:      "☁️", Jute:        "🌿",
    Coffee:       "☕"
};

// ============================================================
// DOM references
// ============================================================
const form        = document.getElementById("predict-form");
const submitBtn   = document.getElementById("submit-btn");
const btnText     = document.getElementById("btn-text");
const btnSpinner  = document.getElementById("btn-spinner");
const resultSec   = document.getElementById("result-section");
const errBanner   = document.getElementById("error-banner");
const errBannerMsg= document.getElementById("error-banner-msg");
const fillBtn     = document.getElementById("fill-sample-btn");

const fields = ["nitrogen","phosphorus","potassium","temperature","humidity","ph_value","rainfall"];

// ============================================================
// Fill sample data
// ============================================================
fillBtn.addEventListener("click", () => {
    const sample = { nitrogen:90, phosphorus:42, potassium:43, temperature:20.88, humidity:82.00, ph_value:6.50, rainfall:202.94 };
    fields.forEach(f => {
        document.getElementById(f).value = sample[f];
        clearError(f);
    });
});

// ============================================================
// Validation
// ============================================================
function showError(id, msg) {
    const input = document.getElementById(id);
    const errEl = document.getElementById(`err-${id}`);
    input.classList.add("invalid");
    if (errEl) errEl.textContent = msg;
}

function clearError(id) {
    const input = document.getElementById(id);
    const errEl = document.getElementById(`err-${id}`);
    input.classList.remove("invalid");
    if (errEl) errEl.textContent = "";
}

function validateForm() {
    let valid = true;
    const limits = {
        nitrogen:    [0, 200],
        phosphorus:  [0, 200],
        potassium:   [0, 200],
        temperature: [-10, 60],
        humidity:    [0, 100],
        ph_value:    [0, 14],
        rainfall:    [0, 500],
    };

    fields.forEach(f => {
        clearError(f);
        const val = parseFloat(document.getElementById(f).value);
        if (isNaN(val)) {
            showError(f, "This field is required.");
            valid = false;
        } else if (val < limits[f][0] || val > limits[f][1]) {
            showError(f, `Must be between ${limits[f][0]} and ${limits[f][1]}.`);
            valid = false;
        }
    });

    return valid;
}

// ============================================================
// Form submit
// ============================================================
form.addEventListener("submit", async (e) => {
    e.preventDefault();

    if (!validateForm()) return;

    // Show spinner
    btnText.classList.add("hidden");
    btnSpinner.classList.remove("hidden");
    submitBtn.disabled = true;
    resultSec.classList.add("hidden");
    errBanner.classList.add("hidden");

    const payload = {};
    fields.forEach(f => { payload[f] = parseFloat(document.getElementById(f).value); });

    try {
        const res = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        if (!res.ok) {
            const errData = await res.json().catch(() => ({}));
            throw new Error(errData.detail || `Server error: ${res.status}`);
        }

        const data = await res.json();
        renderResult(data);

    } catch (err) {
        errBannerMsg.textContent = err.message || "An unexpected error occurred.";
        errBanner.classList.remove("hidden");
    } finally {
        btnText.classList.remove("hidden");
        btnSpinner.classList.add("hidden");
        submitBtn.disabled = false;
    }
});

// ============================================================
// Render result
// ============================================================
function renderResult(data) {
    document.getElementById("result-emoji").textContent      = CROP_EMOJI[data.crop] || "🌾";
    document.getElementById("result-crop-name").textContent  = data.crop;
    document.getElementById("result-confidence").textContent = data.confidence.toFixed(1);

    // Sort probabilities descending, show top 6
    const sorted = Object.entries(data.probabilities)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 6);

    const container = document.getElementById("prob-bars");
    container.innerHTML = "";

    sorted.forEach(([crop, pct], idx) => {
        const isTop = idx === 0;
        const row = document.createElement("div");
        row.className = "prob-row";

        // Delay each bar slightly
        const delay = `${idx * 0.07}s`;

        row.innerHTML = `
            <div class="prob-label" title="${crop}">${crop}</div>
            <div class="prob-bar-bg">
                <div class="prob-bar-fill ${isTop ? "top" : ""}"
                     style="width:${Math.max(pct, 0.5)}%; animation-delay:${delay}"></div>
            </div>
            <div class="prob-pct">${pct.toFixed(1)}%</div>
        `;
        container.appendChild(row);
    });

    resultSec.classList.remove("hidden");
    resultSec.scrollIntoView({ behavior: "smooth", block: "nearest" });
}
