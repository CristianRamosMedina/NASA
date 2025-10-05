function initNewCandidate() {
  const workspace = document.getElementById("workspace");
  const submitBtn = document.getElementById("submitBtn");
  const planetContainer = document.getElementById("planetContainer");

  if (!workspace || !submitBtn || !planetContainer) {
    console.error("⚠️ Elementos no encontrados en el DOM. Verifica los IDs en newcandidate.ejs o dashboard.js.");
    return;
  }

  submitBtn.addEventListener("click", () => {
    const leftInputs = workspace.querySelectorAll("#tableLeftBody input");
    const rightInputs = workspace.querySelectorAll("#tableRightBody input");

    const attributes = [
      "koi_score","koi_fwm_stat_sig","koi_srho_err2","koi_dor_err2",
      "koi_dor_err1","koi_incl","koi_prad_err1","koi_count",
      "koi_dor","koi_dikco_mdec_err","koi_period_err1","koi_period_err2",
      "koi_dikco_mra_err","koi_prad_err2,continuous","koi_dikco_msky_err",
      "koi_max_sngle_ev","koi_prad,continuous","koi_dicco_mdec_err",
      "koi_model_snr","koi_dicco_mra_err"
    ];

    const values = [...leftInputs, ...rightInputs].map(i => i.value.trim());

    if (values.every(v => v === "")) {
      alert("🚫 Ingresa al menos un valor antes de mostrar el planeta.");
      return;
    }

    // Mostrar planeta e info
    const exoplanets = ["e1.png", "e2.png", "e3.png", "e4.png"];
    const randomImg = exoplanets[Math.floor(Math.random() * exoplanets.length)];

    planetContainer.innerHTML = "";

    const planetDiv = document.createElement("div");
    planetDiv.classList.add("flex", "flex-col", "items-center", "justify-center", "gap-4");

    const planetImg = document.createElement("img");
    planetImg.src = `/img/exoplanet/${randomImg}`;
    planetImg.alt = "Exoplanet";
    planetImg.classList.add("rounded-full", "object-cover", "w-48", "h-48", "border-4", "border-space-star", "animate-spin-slow");

    const attrDiv = document.createElement("div");
    attrDiv.classList.add("flex", "flex-col", "gap-2", "bg-space-darker", "p-4", "rounded-lg", "max-h-64", "overflow-y-auto");

    values.forEach((val, i) => {
      if (val !== "") {
        const row = document.createElement("div");
        row.classList.add("flex", "items-center", "gap-2", "text-space-star");
        row.innerHTML = `➡️ <span>${attributes[i]}: ${val}</span>`;
        attrDiv.appendChild(row);
      }
    });

    const success = document.createElement("div");
    success.textContent = "✅ Candidato exitoso";
    success.classList.add("text-green-400", "font-semibold", "animate-pulse");

    planetDiv.appendChild(planetImg);
    planetDiv.appendChild(attrDiv);
    planetDiv.appendChild(success);

    planetContainer.appendChild(planetDiv);
  });
}

document.addEventListener("DOMContentLoaded", initNewCandidate);
