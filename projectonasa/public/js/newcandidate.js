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
    "koi_period_err1", "koi_period_err2", "koi_dikco_mra_err", "koi_prad_err2,continuous",
    "koi_dikco_msky_err", "koi_max_sngle_ev", "koi_prad,continuous",
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

  // 🚀 Evento Submit
  submitBtn.addEventListener("click", () => {
    const rows = Array.from(tableBody.querySelectorAll("tr"));
    const data = rows.map(row => {
      const inputs = row.querySelectorAll("input");
      return columns.map((col, i) => inputs[i] ? inputs[i].value.trim() : "");
    }).filter(row => row.some(v => v !== ""));

    if (data.length === 0) {
      alert("🚫 Agrega al menos una fila antes de enviar.");
      return;
    }

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

    // 📊 Crear y mostrar los datos del candidato (DERECHA)
    const candidateData = document.createElement("div");
    candidateData.classList.add("candidate-data");

    // Encabezado
    const header = document.createElement("div");
    header.textContent = "🌌 Exoplanet Candidate Data";
    header.classList.add("data-header");
    candidateData.appendChild(header);

    // Contenedor de contenido
    const content = document.createElement("div");
    content.classList.add("data-content");

    // Datos
    data[0].forEach((val, i) => {
      if (val) {
        const rowDiv = document.createElement("div");
        rowDiv.classList.add("data-row");

        const attrName = document.createElement("span");
        attrName.textContent = columns[i];
        attrName.classList.add("attr-name");

        const attrValue = document.createElement("span");
        attrValue.textContent = val || "N/A";
        attrValue.classList.add("attr-value");

        rowDiv.appendChild(attrName);
        rowDiv.appendChild(attrValue);
        content.appendChild(rowDiv);
      }
    });

    candidateData.appendChild(content);

    // Mensaje de éxito
    const success = document.createElement("div");
    success.textContent = "✅ Candidate Successfully Created - Ready for Analysis";
    success.classList.add("success-message");
    candidateData.appendChild(success);

    // 🔄 Cambiar de tabla a resultados
    resultSection.innerHTML = "";
    resultSection.appendChild(candidateData);

    // Ocultar tabla y mostrar resultados
    tableSection.classList.add("hidden");
    resultSection.classList.remove("hidden");

    // Limpiar tabla para futuros usos
    setTimeout(() => {
      tableBody.innerHTML = `<tr><td colspan="20" class="text-center py-4 text-gray-500">No hay datos</td></tr>`;
    }, 500);
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