function initNewCandidate() {
  const tableBody = document.getElementById("candidateTableBody");
  const addRowBtn = document.getElementById("addRowBtn");
  const submitBtn = document.getElementById("submitBtn");
  const planetDisplay = document.getElementById("planetDisplay");
  const tableSection = document.getElementById("tableSection");
  const resultSection = document.getElementById("resultSection");

  // ✅ Verificación de elementos del DOM
  if (!tableBody || !addRowBtn || !submitBtn || !planetDisplay || !tableSection || !resultSection) {
    console.error("⚠️ Elementos no encontrados en el DOM.");
    return;
  }

  // ✅ Columnas del formulario
  const columns = [
    "koi_score", "koi_fwm_stat_sig", "koi_srho_err2", "koi_dor_err2", "koi_dor_err1",
    "koi_incl", "koi_prad_err1", "koi_count", "koi_dor", "koi_dikco_mdec_err",
    "koi_period_err1", "koi_period_err2", "koi_dikco_mra_err", "koi_prad_err2_continuous",
    "koi_dikco_msky_err", "koi_max_sngle_ev", "koi_prad_continuous",
    "koi_dicco_mdec_err", "koi_model_snr", "koi_dicco_mra_err"
  ];

  // 🔹 Crear fila editable
  function createRow() {
    if (tableBody.children.length === 1 && tableBody.children[0].textContent.includes("No hay datos")) {
      tableBody.innerHTML = "";
    }

    const tr = document.createElement("tr");
    columns.forEach((col) => {
      const td = document.createElement("td");
      td.classList.add("px-4", "py-2", "border-b", "border-planet");

      const input = document.createElement("input");
      input.type = "text";
      input.placeholder = col;
      input.classList.add("w-full", "bg-space-dark", "text-space-star", "border", "border-planet", "rounded", "px-2", "py-1");
      td.appendChild(input);
      tr.appendChild(td);
    });

    tableBody.appendChild(tr);
  }

  // 🧩 Agregar filas
  addRowBtn.addEventListener("click", createRow);

  // 🚀 Evento Submit con integración de API de predicción
  submitBtn.addEventListener("click", async () => {
    console.log("[New Candidate] Submit button clicked");

    const rows = Array.from(tableBody.querySelectorAll("tr"));
    const data = rows.map(row => {
      const inputs = row.querySelectorAll("input");
      return columns.map((col, i) => inputs[i] ? inputs[i].value.trim() : "");
    }).filter(row => row.some(v => v !== ""));

    if (data.length === 0) {
      alert("🚫 Agrega al menos una fila antes de enviar.");
      return;
    }

    console.log("[New Candidate] Data collected:", data);

    // Guardar temporalmente
    localStorage.setItem("tempCandidates", JSON.stringify(data));

    // 🪐 Actualizar el planeta con una imagen aleatoria (IZQUIERDA)
    const exoplanets = ["e1.png", "e2.png", "e3.png", "e4.png"];
    const randomImg = exoplanets[Math.floor(Math.random() * exoplanets.length)];

    planetDisplay.innerHTML = `
      <div class="absolute inset-0 flex items-center justify-center">
        <div class="w-64 h-64 border border-planet rounded-full animate-spin-slow relative flex items-center justify-center">
          <img src="/img/exoplanet/${randomImg}" alt="Exoplanet"
               class="absolute w-24 h-24 rounded-full shadow-lg animate-orbit object-cover">
        </div>
      </div>
    `;

    // Show loading state
    resultSection.innerHTML = '<div class="text-center text-nasa text-lg animate-pulse p-8">Analyzing candidate with Kepler model...</div>';
    tableSection.classList.add("hidden");
    resultSection.classList.remove("hidden");

    // Convert data to features object for API
    const features = {};
    data[0].forEach((val, i) => {
      features[columns[i]] = val !== "" ? parseFloat(val) : "";
    });

    console.log("[New Candidate] Features for API:", features);

    try {
      // Call Kepler prediction API
      console.log("[New Candidate] Calling prediction API...");
      const response = await fetch('http://localhost:5000/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ features })
      });

      const result = await response.json();
      console.log("[New Candidate] API Response:", response.status, result);

      if (!response.ok) {
        console.error("[New Candidate] API Error:", result);
        throw new Error(result.error || 'Prediction failed');
      }

      console.log("[New Candidate] Prediction successful:", result.prediction);

      // Prediction result colors
      const predictionColor = {
        'CONFIRMED': 'text-green-400',
        'CANDIDATE': 'text-yellow-400',
        'FALSE POSITIVE': 'text-red-400'
      }[result.prediction] || 'text-space-star';

      const predictionBg = {
        'CONFIRMED': 'bg-green-900 border-green-400',
        'CANDIDATE': 'bg-yellow-900 border-yellow-400',
        'FALSE POSITIVE': 'bg-red-900 border-red-400'
      }[result.prediction] || 'bg-space-darker border-nasa';

      // Create prediction result display
      const resultDiv = document.createElement("div");
      resultDiv.classList.add("candidate-data");

      resultDiv.innerHTML = `
        <div class="${predictionBg} bg-opacity-30 p-6 rounded-lg border-2 mb-4">
          <div class="text-center mb-4">
            <h3 class="text-2xl font-bold text-nasa mb-2">KEPLER PREDICTION RESULT</h3>
            <div class="text-4xl font-bold ${predictionColor} mb-2">
              ${result.prediction}
            </div>
            <div class="text-lg text-space-star">
              Confidence: ${(result.confidence * 100).toFixed(1)}%
            </div>
          </div>

          <div class="border-t border-planet pt-4 mt-4">
            <h4 class="text-sm font-bold text-nasa mb-3">CLASS PROBABILITIES</h4>
            <div class="space-y-3">
              ${Object.entries(result.probabilities).map(([cls, prob]) => `
                <div class="flex justify-between items-center">
                  <span class="text-space-star font-medium">${cls}</span>
                  <div class="flex items-center gap-3 flex-1 ml-4">
                    <div class="flex-1 bg-space-dark rounded-full h-3">
                      <div class="bg-nasa h-3 rounded-full transition-all duration-500" style="width: ${prob * 100}%"></div>
                    </div>
                    <span class="text-space-star w-16 text-right">${(prob * 100).toFixed(1)}%</span>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>

          <div class="border-t border-planet pt-4 mt-4">
            <h4 class="text-sm font-bold text-nasa mb-2">MODEL INFORMATION</h4>
            <div class="grid grid-cols-2 gap-2 text-sm text-space-star">
              <div>Model: <span class="text-white">${result.model}</span></div>
              <div>Accuracy: <span class="text-white">${(result.accuracy * 100).toFixed(2)}%</span></div>
              <div>Features analyzed: <span class="text-white">${Object.values(features).filter(v => v !== "").length}/20</span></div>
            </div>
          </div>
        </div>

        <div class="bg-space-darker bg-opacity-50 p-4 rounded-lg border border-planet">
          <h4 class="text-sm font-bold text-nasa mb-3">INPUT FEATURES</h4>
          <div class="grid grid-cols-2 gap-2 max-h-60 overflow-y-auto text-xs">
            ${data[0].map((val, i) => val ? `
              <div class="flex justify-between items-center py-1 border-b border-planet border-opacity-30">
                <span class="text-space-star">${columns[i]}:</span>
                <span class="text-white font-mono">${val}</span>
              </div>
            ` : '').join('')}
          </div>
        </div>

        <button id="newAnalysisBtn" class="mt-4 w-full bg-nasa text-space-dark font-bold py-2 px-4 rounded hover:bg-rocket transition-colors">
          Analyze Another Candidate
        </button>
      `;

      resultSection.innerHTML = "";
      resultSection.appendChild(resultDiv);

      // Add event listener to "Analyze Another" button
      document.getElementById("newAnalysisBtn").addEventListener("click", () => {
        tableSection.classList.remove("hidden");
        resultSection.classList.add("hidden");
        planetDisplay.innerHTML = `
          <div class="absolute inset-0 flex items-center justify-center">
            <div class="w-64 h-64 border border-planet rounded-full animate-spin-slow relative">
              <div class="absolute w-8 h-8 bg-space-accent rounded-full shadow-lg animate-orbit"></div>
            </div>
          </div>
        `;
        tableBody.innerHTML = `<tr><td colspan="20" class="text-center py-4 text-gray-500">No hay datos</td></tr>`;
      });

    } catch (error) {
      console.error('[New Candidate] Prediction error:', error);
      resultSection.innerHTML = `
        <div class="text-center text-red-400 p-6 bg-red-900 bg-opacity-30 rounded-lg border-2 border-red-400">
          <div class="text-2xl font-bold mb-3">⚠️ Error</div>
          <div class="text-lg mb-2">${error.message}</div>
          <div class="text-sm mt-3">Make sure the API server is running on port 5000</div>
          <button id="retryBtn" class="mt-4 bg-nasa text-space-dark font-bold py-2 px-6 rounded hover:bg-rocket transition-colors">
            Back to Form
          </button>
        </div>
      `;

      document.getElementById("retryBtn").addEventListener("click", () => {
        tableSection.classList.remove("hidden");
        resultSection.classList.add("hidden");
      });
    }
  });

  // 🔄 Función para volver a modo edición (opcional - puedes agregar un botón)
  function switchToEditMode() {
    tableSection.classList.remove("hidden");
    resultSection.classList.add("hidden");

    // Restaurar planeta inicial
    planetDisplay.innerHTML = `
      <div class="absolute inset-0 flex items-center justify-center">
        <div class="w-64 h-64 border border-planet rounded-full animate-spin-slow relative">
          <div class="absolute w-8 h-8 bg-space-accent rounded-full shadow-lg animate-orbit"></div>
        </div>
      </div>
    `;
  }
}

// ✅ Inicializar cuando el DOM esté listo
document.addEventListener("DOMContentLoaded", initNewCandidate);
