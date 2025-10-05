function initNewCandidate() {
  const planetDisplay = document.getElementById("planetDisplay");
  const inputContainer = document.getElementById("inputContainer");
  const resultContainer = document.getElementById("resultContainer");
  const addRowBtn = document.getElementById("addRowBtn");

  const leftColumns = [
    "koi_score", "koi_fwm_stat_sig", "koi_srho_err2", "koi_dor_err2",
    "koi_dor_err1", "koi_incl", "koi_prad_err1", "koi_count",
    "koi_dor", "koi_dikco_mdec_err"
  ];

  const rightColumns = [
    "koi_period_err1", "koi_period_err2", "koi_dikco_mra_err",
    "koi_prad_err2,continuous", "koi_dikco_msky_err", "koi_max_sngle_ev",
    "koi_prad,continuous", "koi_dicco_mdec_err", "koi_model_snr",
    "koi_dicco_mra_err"
  ];

  let currentData = {};

  // 🔹 Inicializa formulario
  function initInputForm() {
    inputContainer.innerHTML = `
      <div class="bg-space-dark bg-opacity-80 rounded-xl p-4">
        <h2 class="text-xl font-bold text-nasa mb-4">📊 Enter Candidate Data</h2>
        
        <div class="grid grid-cols-2 gap-4 max-h-[500px] border border-planet rounded-lg p-4">
          <!-- Tabla izquierda -->
          <div class="overflow-y-auto max-h-[450px] border border-planet rounded-lg p-2">
            <table class="w-full text-space-star text-sm">
              <thead class="bg-space-darker text-left">
                <tr><th class="py-2 text-nasa px-2">Left Attributes</th></tr>
              </thead>
              <tbody id="tableLeftBody" class="divide-y divide-planet">
                ${leftColumns.map(attr => `
                  <tr>
                    <td class="py-2 px-2 flex items-center gap-2">
                      <span class="w-40 text-space-star text-xs">${attr}</span>
                      <input type="text" placeholder="-" class="cell-input flex-1" data-attribute="${attr}" />
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>

          <!-- Tabla derecha -->
          <div class="overflow-y-auto max-h-[450px] border border-planet rounded-lg p-2">
            <table class="w-full text-space-star text-sm">
              <thead class="bg-space-darker text-left">
                <tr><th class="py-2 text-nasa px-2">Right Attributes</th></tr>
              </thead>
              <tbody id="tableRightBody" class="divide-y divide-planet">
                ${rightColumns.map(attr => `
                  <tr>
                    <td class="py-2 px-2 flex items-center gap-2">
                      <span class="w-40 text-space-star text-xs">${attr}</span>
                      <input type="text" placeholder="-" class="cell-input flex-1" data-attribute="${attr}" />
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>

        <div class="mt-4 flex justify-end">
          <button id="submitBtn" class="px-4 py-2 bg-nasa text-space-dark font-bold rounded hover:bg-rocket transition-colors">Submit</button>
        </div>
      </div>
    `;

    const submitBtn = document.getElementById("submitBtn");
    submitBtn.addEventListener("click", handleSubmit);
  }

  // 🔹 Maneja envío de formulario
  function handleSubmit() {
    const inputs = document.querySelectorAll(".cell-input");
    const data = {};
    inputs.forEach(input => {
      const attr = input.getAttribute("data-attribute");
      const value = input.value.trim();
      if (value) data[attr] = value;
    });

    if (Object.keys(data).length === 0) {
      alert("🚫 Ingresa al menos un valor antes de continuar.");
      return;
    }

    currentData = data;

    // Mostrar planeta
    const exoplanets = ["e1.png", "e2.png", "e3.png", "e4.png"];
    const randomImg = exoplanets[Math.floor(Math.random() * exoplanets.length)];
    planetDisplay.innerHTML = `
      <div class="absolute inset-0 flex items-center justify-center">
        <div class="w-64 h-64 border border-planet rounded-full animate-spin-slow relative flex items-center justify-center">
          <img src="/img/exoplanet/${randomImg}" alt="Exoplanet" class="absolute w-16 h-16 rounded-full shadow-lg animate-orbit object-cover">
        </div>
      </div>
    `;

    // Ocultar formulario y mostrar resultados
    inputContainer.style.display = "none";
    resultContainer.style.display = "block";

    showResults(data);
  }

  // 🔹 Mostrar resultados
  function showResults(data) {
    resultContainer.innerHTML = "";

    const resultsDiv = document.createElement("div");
    resultsDiv.classList.add("bg-space-dark", "bg-opacity-80", "rounded-xl", "p-6", "border", "border-planet");

    const title = document.createElement("h2");
    title.textContent = "🌌 Candidate Results";
    title.classList.add("text-xl", "font-bold", "text-nasa", "mb-4");
    resultsDiv.appendChild(title);

    const dataDiv = document.createElement("div");
    dataDiv.classList.add("grid", "grid-cols-2", "gap-4", "max-h-[400px]", "overflow-y-auto");

    const leftData = document.createElement("div");
    leftData.classList.add("space-y-2");
    leftColumns.forEach(attr => {
      if (data[attr]) {
        const item = document.createElement("div");
        item.classList.add("flex", "justify-between", "text-space-star", "text-sm", "py-1");
        item.innerHTML = `<span class="text-space-accent">${attr}:</span><span class="bg-space-darker px-2 py-1 rounded">${data[attr]}</span>`;
        leftData.appendChild(item);
      }
    });

    const rightData = document.createElement("div");
    rightData.classList.add("space-y-2");
    rightColumns.forEach(attr => {
      if (data[attr]) {
        const item = document.createElement("div");
        item.classList.add("flex", "justify-between", "text-space-star", "text-sm", "py-1");
        item.innerHTML = `<span class="text-space-accent">${attr}:</span><span class="bg-space-darker px-2 py-1 rounded">${data[attr]}</span>`;
        rightData.appendChild(item);
      }
    });

    dataDiv.appendChild(leftData);
    dataDiv.appendChild(rightData);
    resultsDiv.appendChild(dataDiv);

    const success = document.createElement("div");
    success.textContent = "✅ Candidate Successfully Created!";
    success.classList.add("text-green-400", "font-bold", "text-center", "mt-4", "p-3", "bg-green-900", "rounded", "text-sm");
    resultsDiv.appendChild(success);

    const newRowBtn = document.createElement("button");
    newRowBtn.textContent = "🆕 New Candidate";
    newRowBtn.classList.add("bg-blue-600", "px-4", "py-2", "rounded", "mt-4", "w-full", "text-white", "hover:bg-blue-700", "transition-colors");
    newRowBtn.addEventListener("click", resetToInput);
    resultsDiv.appendChild(newRowBtn);

    resultContainer.appendChild(resultsDiv);
  }

  // 🔹 Resetear formulario
  function resetToInput() {
    resultContainer.style.display = "none";
    inputContainer.style.display = "flex";

    planetDisplay.innerHTML = `
      <div class="absolute inset-0 flex items-center justify-center">
        <div class="w-64 h-64 border border-planet rounded-full animate-spin-slow relative">
          <div class="absolute w-8 h-8 bg-space-accent rounded-full shadow-lg animate-orbit"></div>
        </div>
      </div>
    `;

    currentData = {};
    initInputForm();
  }

  // 🔹 Inicializar formulario al cargar
  initInputForm();

  // 🔹 Botón externo para nuevo candidato
  addRowBtn.addEventListener("click", resetToInput);
}

// ✅ Inicializar cuando el DOM esté listo
document.addEventListener("DOMContentLoaded", initNewCandidate);
