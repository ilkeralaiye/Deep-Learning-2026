const FEATURES = [
    { id: "sepal_length", label: "Sepal Length", unit: "cm", min: 4.0, max: 8.0, step: 0.1, default: 5.8 },
    { id: "sepal_width",  label: "Sepal Width",  unit: "cm", min: 2.0, max: 5.0, step: 0.1, default: 3.0 },
    { id: "petal_length", label: "Petal Length", unit: "cm", min: 1.0, max: 7.0, step: 0.1, default: 4.0 },
    { id: "petal_width",  label: "Petal Width",  unit: "cm", min: 0.1, max: 2.6, step: 0.1, default: 1.2 },
];

const SPECIES_META = {
    setosa:     { emoji: "🌸", color: "setosa",     label: "Iris Setosa" },
    versicolor: { emoji: "🌼", color: "versicolor", label: "Iris Versicolor" },
    virginica:  { emoji: "🌺", color: "virginica",  label: "Iris Virginica" },
};

// ── Build slider UI ──────────────────────────────────────────────────────────
function buildSliders() {
    const container = document.getElementById("sliders-container");
    FEATURES.forEach(f => {
        const group = document.createElement("div");
        group.className = "feature-group";
        group.innerHTML = `
            <div class="feature-label">
                <span class="feature-name">${f.label} <span style="color:var(--text-muted);font-size:0.75rem">(${f.unit})</span></span>
                <span class="feature-value" id="val-${f.id}">${f.default.toFixed(1)}</span>
            </div>
            <div class="slider-wrapper">
                <input type="range" id="slider-${f.id}"
                    min="${f.min}" max="${f.max}" step="${f.step}" value="${f.default}" />
            </div>
            <div class="range-limits">
                <span>${f.min.toFixed(1)}</span>
                <span>${f.max.toFixed(1)}</span>
            </div>
        `;
        container.appendChild(group);

        const slider = group.querySelector(`#slider-${f.id}`);
        const valEl  = group.querySelector(`#val-${f.id}`);

        updateSliderGradient(slider);

        slider.addEventListener("input", () => {
            const v = parseFloat(slider.value).toFixed(1);
            valEl.textContent = v;
            document.getElementById(`num-${f.id}`).value = v;
            updateSliderGradient(slider);
        });
    });
}

function updateSliderGradient(slider) {
    const pct = ((slider.value - slider.min) / (slider.max - slider.min)) * 100;
    slider.style.background = `linear-gradient(to right, var(--accent-violet) ${pct}%, rgba(255,255,255,0.08) ${pct}%)`;
}

// ── Build number inputs ──────────────────────────────────────────────────────
function buildNumberInputs() {
    const container = document.getElementById("number-inputs-container");
    FEATURES.forEach(f => {
        const wrap = document.createElement("div");
        wrap.className = "input-field";
        wrap.innerHTML = `
            <label for="num-${f.id}">${f.label} (${f.unit})</label>
            <input type="number" id="num-${f.id}"
                min="${f.min}" max="${f.max}" step="${f.step}" value="${f.default}" />
        `;
        container.appendChild(wrap);

        const numInput = wrap.querySelector(`#num-${f.id}`);
        numInput.addEventListener("input", () => {
            let v = parseFloat(numInput.value);
            if (isNaN(v)) return;
            v = Math.min(Math.max(v, f.min), f.max);
            const slider = document.getElementById(`slider-${f.id}`);
            slider.value = v;
            document.getElementById(`val-${f.id}`).textContent = v.toFixed(1);
            updateSliderGradient(slider);
        });
    });
}

// ── Get current feature values ───────────────────────────────────────────────
function getValues() {
    return FEATURES.map(f => parseFloat(document.getElementById(`slider-${f.id}`).value));
}

// ── Predict ──────────────────────────────────────────────────────────────────
async function predict() {
    const btn = document.getElementById("predict-btn");
    const btnContent = btn.querySelector(".btn-content");

    btn.disabled = true;
    btnContent.innerHTML = `<div class="spinner"></div> Tahmin ediliyor…`;

    const [sepal_length, sepal_width, petal_length, petal_width] = getValues();

    try {
        const res = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ sepal_length, sepal_width, petal_length, petal_width }),
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || "Sunucu hatası");
        }

        const data = await res.json();
        renderResult(data);

    } catch (err) {
        showError(err.message || "Bağlantı hatası. Sunucunun çalıştığından emin olun.");
    } finally {
        btn.disabled = false;
        btnContent.innerHTML = `<span>🔮</span> Tahmin Et`;
    }
}

// ── Render prediction result ─────────────────────────────────────────────────
function renderResult(data) {
    const placeholder = document.getElementById("result-placeholder");
    const resultEl    = document.getElementById("prediction-result");

    placeholder.style.display = "none";
    resultEl.classList.add("visible");

    const key  = data.predicted_class.toLowerCase();
    const meta = SPECIES_META[key] || { emoji: "🌿", color: "setosa", label: data.predicted_class };

    // Species display
    const speciesDisplay = document.getElementById("species-display");
    speciesDisplay.className = `species-display ${meta.color}`;

    document.getElementById("species-emoji").textContent = meta.emoji;
    document.getElementById("species-name-text").className = `species-name ${meta.color}`;
    document.getElementById("species-name-text").textContent = meta.label;

    const confBadge = document.getElementById("confidence-badge");
    confBadge.className = `confidence-badge ${meta.color}`;
    confBadge.innerHTML = `✦ Güven: ${(data.confidence * 100).toFixed(1)}%`;

    // Probability bars
    const barsContainer = document.getElementById("prob-bars");
    barsContainer.innerHTML = "";

    const classNames = ["setosa", "versicolor", "virginica"];
    const probs = data.probabilities;

    classNames.forEach((cls, i) => {
        const pct = (probs[i] * 100).toFixed(1);
        const row = document.createElement("div");
        row.className = "prob-row";
        row.innerHTML = `
            <div class="prob-meta">
                <span class="prob-species">${SPECIES_META[cls].emoji} Iris ${cls.charAt(0).toUpperCase() + cls.slice(1)}</span>
                <span class="prob-pct ${cls}">${pct}%</span>
            </div>
            <div class="prob-bar-track">
                <div class="prob-bar-fill ${cls}" data-width="${pct}"></div>
            </div>
        `;
        barsContainer.appendChild(row);
    });

    // Animate bars
    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            document.querySelectorAll(".prob-bar-fill").forEach(bar => {
                bar.style.width = bar.dataset.width + "%";
            });
        });
    });
}

// ── Error toast ──────────────────────────────────────────────────────────────
function showError(msg) {
    const toast = document.getElementById("error-toast");
    document.getElementById("error-message").textContent = msg;
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 4500);
}

// ── Reset ────────────────────────────────────────────────────────────────────
function resetForm() {
    FEATURES.forEach(f => {
        const slider = document.getElementById(`slider-${f.id}`);
        const numInput = document.getElementById(`num-${f.id}`);
        slider.value = f.default;
        numInput.value = f.default.toFixed(1);
        document.getElementById(`val-${f.id}`).textContent = f.default.toFixed(1);
        updateSliderGradient(slider);
    });
    document.getElementById("result-placeholder").style.display = "";
    document.getElementById("prediction-result").classList.remove("visible");
}

// ── Init ─────────────────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
    buildSliders();
    buildNumberInputs();

    document.getElementById("predict-btn").addEventListener("click", predict);
    document.getElementById("reset-btn").addEventListener("click", resetForm);
});
