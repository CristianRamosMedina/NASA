console.log("[Dashboard.js] Loading...");

// === Canvas Espacial ===
const canvas = document.getElementById("spaceCanvas");
const ctx = canvas.getContext("2d");

console.log("[Dashboard.js] Canvas:", canvas);

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

window.addEventListener("resize", () => {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
});

// === Workspace dinámico ===
const workspace = document.getElementById("workspace");
console.log("[Dashboard.js] Workspace:", workspace);

// === Mostrar contenido dinámico ===
function showContent(section) {
  console.log("[Dashboard.js] showContent called with:", section);
  if (section !== "default") canvas.style.display = "none";
  else canvas.style.display = "block";

  workspace.innerHTML = "";

  switch (section) {
    case "newCandidate":
      console.log("[Dashboard.js] Rendering New Candidate form...");
      workspace.innerHTML = `
        <div class="bg-space-dark bg-opacity-80 p-6 rounded-xl shadow-lg">
          <h2 class="text-2xl font-bold text-nasa mb-4">🪐 New Candidate</h2>

          <!-- Contenedor doble -->
          <div class="grid grid-cols-2 gap-4 overflow-y-auto max-h-[600px] border border-planet rounded-lg p-4">
            
            <!-- Tabla izquierda -->
            <div class="overflow-y-auto max-h-[550px] border border-planet rounded-lg p-2">
              <table class="min-w-full text-space-star text-sm">
                <thead class="bg-space-darker text-left sticky top-0">
                  <tr><th class="py-2 text-nasa">Left Attributes</th></tr>
                </thead>
                <tbody id="tableLeftBody" class="divide-y divide-planet">
                  ${[
                    "koi_score",
                    "koi_fwm_stat_sig",
                    "koi_srho_err2",
                    "koi_dor_err2",
                    "koi_dor_err1",
                    "koi_incl",
                    "koi_prad_err1",
                    "koi_count",
                    "koi_dor",
                    "koi_dikco_mdec_err"
                  ]
                    .map(
                      (attr) => `
                    <tr>
                      <td class="py-1 flex items-center gap-2">
                        <span class="w-48 text-space-star">${attr}</span>
                        <input type="number" placeholder="-" class="cell-input flex-1" />
                      </td>
                    </tr>`
                    )
                    .join("")}
                </tbody>
              </table>
            </div>

            <!-- Tabla derecha -->
            <div class="overflow-y-auto max-h-[550px] border border-planet rounded-lg p-2">
              <table class="min-w-full text-space-star text-sm">
                <thead class="bg-space-darker text-left sticky top-0">
                  <tr><th class="py-2 text-nasa">Right Attributes</th></tr>
                </thead>
                <tbody id="tableRightBody" class="divide-y divide-planet">
                  ${[
                    "koi_period_err1",
                    "koi_period_err2",
                    "koi_dikco_mra_err",
                    "koi_prad_err2_continuous",
                    "koi_dikco_msky_err",
                    "koi_max_sngle_ev",
                    "koi_prad_continuous",
                    "koi_dicco_mdec_err",
                    "koi_model_snr",
                    "koi_dicco_mra_err"
                  ]
                    .map(
                      (attr) => `
                    <tr>
                      <td class="py-1 flex items-center gap-2">
                        <span class="w-48 text-space-star">${attr}</span>
                        <input type="number" placeholder="-" class="cell-input flex-1" />
                      </td>
                    </tr>`
                    )
                    .join("")}
                </tbody>
              </table>
            </div>
          </div>

          <!-- Botón de envío -->
          <div class="mt-4 flex justify-end">
            <button id="submitBtn" class="px-4 py-2 bg-nasa text-space-dark font-bold rounded hover:bg-rocket transition-colors">
              Submit
            </button>
          </div>

          <!-- Contenedor del planeta -->
          <div id="planetContainer" class="flex justify-center mt-8"></div>
        </div>

        <style>
          .cell-input {
            background-color: #0b0c10;
            color: #00eaff;
            border: 1px solid #00eaff55;
            border-radius: 4px;
            padding: 2px 4px;
            font-size: 0.8rem;
            text-align: center;
            appearance: textfield;
          }

          /* Ocultar flechas de los inputs tipo number */
          .cell-input::-webkit-outer-spin-button,
          .cell-input::-webkit-inner-spin-button {
            -webkit-appearance: none;
            margin: 0;
          }

          .cell-input:focus {
            outline: none;
            border-color: #00eaff;
          }

          .overflow-y-auto {
            scrollbar-width: thin;
            scrollbar-color: #00eaff #0b0c10;
          }

          .overflow-y-auto::-webkit-scrollbar {
            width: 8px;
          }

          .overflow-y-auto::-webkit-scrollbar-track {
            background: #0b0c10;
            border-radius: 8px;
          }

          .overflow-y-auto::-webkit-scrollbar-thumb {
            background-color: #00eaff;
            border-radius: 8px;
          }
        </style>
      `;

      // === Lógica para mostrar el planeta y predecir ===
      const submitBtn = document.getElementById("submitBtn");
      const planetContainer = document.getElementById("planetContainer");

      console.log("[Dashboard.js] Submit button:", submitBtn);
      console.log("[Dashboard.js] Planet container:", planetContainer);

      submitBtn.addEventListener("click", async () => {
        console.log("[Dashboard.js] Submit button clicked!");
        // Obtener valores de ambas tablas
        const leftInputs = Array.from(document.querySelectorAll("#tableLeftBody input"));
        const rightInputs = Array.from(document.querySelectorAll("#tableRightBody input"));
        const leftLabels = Array.from(document.querySelectorAll("#tableLeftBody span"));
        const rightLabels = Array.from(document.querySelectorAll("#tableRightBody span"));

        const data = [];
        const features = {};

        leftInputs.forEach((input, i) => {
          const featureName = leftLabels[i].textContent;
          const value = input.value.trim();
          features[featureName] = value !== "" ? parseFloat(value) : "";
          if (value !== "") {
            data.push({ name: featureName, value: value });
          }
        });

        rightInputs.forEach((input, i) => {
          const featureName = rightLabels[i].textContent;
          const value = input.value.trim();
          features[featureName] = value !== "" ? parseFloat(value) : "";
          if (value !== "") {
            data.push({ name: featureName, value: value });
          }
        });

        if (data.length === 0) {
          alert("Please fill at least one value before submitting.");
          return;
        }

        // Mostrar loading
        planetContainer.innerHTML = '<div class="text-center text-nasa text-lg animate-pulse">Analyzing candidate...</div>';

        console.log("[Dashboard.js] Features to send:", features);
        console.log("[Dashboard.js] Calling API...");

        try {
          // Call prediction API
          const response = await fetch('http://localhost:5000/api/predict', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ features })
          });

          const result = await response.json();

          console.log("[Dashboard.js] API Response:", response.status, result);

          if (!response.ok) {
            console.error("[Dashboard.js] API Error:", result);
            throw new Error(result.error || 'Prediction failed');
          }

          console.log("[Dashboard.js] Prediction successful:", result.prediction);

          // Mostrar el planeta con el resultado
          planetContainer.innerHTML = "";

          const exoplanets = ["e1.png", "e2.png", "e3.png", "e4.png"];
          const randomImg = exoplanets[Math.floor(Math.random() * exoplanets.length)];

          const planetDiv = document.createElement("div");
          planetDiv.classList.add("flex", "flex-col", "items-center", "justify-center", "gap-4", "mt-8");

          const planetImg = document.createElement("img");
          planetImg.src = \`/img/exoplanet/\${randomImg}\`;
          planetImg.alt = "Exoplanet";
          planetImg.classList.add(
            "rounded-full",
            "object-cover",
            "border-4",
            "border-space-star",
            "shadow-lg",
            "w-48",
            "h-48",
            "animate-spin-slow"
          );

          // Prediction result
          const predictionColor = {
            'CONFIRMED': 'text-green-400',
            'CANDIDATE': 'text-yellow-400',
            'FALSE POSITIVE': 'text-red-400'
          }[result.prediction] || 'text-space-star';

          const resultDiv = document.createElement("div");
          resultDiv.classList.add("bg-space-darker", "p-6", "rounded-lg", "w-full", "max-w-md", "border-2", "border-nasa");
          resultDiv.innerHTML = \`
            <div class="text-center mb-4">
              <h3 class="text-xl font-bold text-nasa mb-2">PREDICTION RESULT</h3>
              <div class="text-3xl font-bold \${predictionColor} mb-2">
                \${result.prediction}
              </div>
              <div class="text-sm text-space-star">
                Confidence: \${(result.confidence * 100).toFixed(1)}%
              </div>
            </div>

            <div class="border-t border-planet pt-4 mt-4">
              <h4 class="text-sm font-bold text-nasa mb-2">PROBABILITIES</h4>
              <div class="space-y-2">
                \${Object.entries(result.probabilities).map(([cls, prob]) => \`
                  <div class="flex justify-between items-center">
                    <span class="text-space-star text-sm">\${cls}</span>
                    <div class="flex items-center gap-2">
                      <div class="w-24 bg-space-dark rounded-full h-2">
                        <div class="bg-nasa h-2 rounded-full" style="width: \${prob * 100}%"></div>
                      </div>
                      <span class="text-space-star text-sm w-12 text-right">\${(prob * 100).toFixed(1)}%</span>
                    </div>
                  </div>
                \`).join('')}
              </div>
            </div>

            <div class="border-t border-planet pt-4 mt-4">
              <h4 class="text-sm font-bold text-nasa mb-2">MODEL INFO</h4>
              <div class="text-xs text-space-star space-y-1">
                <div>Model: \${result.model}</div>
                <div>Accuracy: \${(result.accuracy * 100).toFixed(2)}%</div>
                <div>Features analyzed: \${data.length}/20</div>
              </div>
            </div>
          \`;

          const attrDiv = document.createElement("div");
          attrDiv.classList.add(
            "flex",
            "flex-col",
            "items-start",
            "gap-2",
            "bg-space-darker",
            "p-4",
            "rounded-lg",
            "w-full",
            "max-w-md",
            "overflow-y-auto",
            "max-h-40"
          );
          attrDiv.innerHTML = '<h4 class="text-sm font-bold text-nasa mb-2">INPUT FEATURES</h4>';

          data.forEach((item) => {
            const row = document.createElement("div");
            row.classList.add("flex", "items-center", "gap-2", "text-space-star", "text-xs");
            row.innerHTML = \`<span>\${item.name}: \${item.value}</span>\`;
            attrDiv.appendChild(row);
          });

          planetDiv.appendChild(planetImg);
          planetDiv.appendChild(resultDiv);
          planetDiv.appendChild(attrDiv);

          planetContainer.appendChild(planetDiv);

        } catch (error) {
          planetContainer.innerHTML = \`
            <div class="text-center text-red-400 p-4 bg-red-900 bg-opacity-30 rounded-lg">
              <div class="font-bold mb-2">Error</div>
              <div class="text-sm">\${error.message}</div>
              <div class="text-xs mt-2">Make sure the API server is running on port 5000</div>
            </div>
          \`;
          console.error('Prediction error:', error);
        }
      });

      break;

    default:
      workspace.innerHTML = `
        <h1 class="text-3xl font-bold text-rocket flex items-center">
          🚀 Welcome to ExoFinder
        </h1>
        <p class="mt-2 text-space-star">
          Select an option from the sidebar menu to continue.
        </p>
      `;
      break;
  }
}

// === Clase Planet + animación ===
class Planet {
  constructor(x, y, radius, imgSrc, dx, dy) {
    this.x = x;
    this.y = y;
    this.radius = radius;
    this.dx = dx;
    this.dy = dy;
    this.img = new Image();
    this.img.src = imgSrc;
  }

  draw() {
    ctx.save();
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
    ctx.clip();
    ctx.drawImage(
      this.img,
      this.x - this.radius,
      this.y - this.radius,
      this.radius * 2,
      this.radius * 2
    );
    ctx.restore();
  }

  update() {
    this.x += this.dx;
    this.y += this.dy;
    if (this.x - this.radius < 0 || this.x + this.radius > canvas.width)
      this.dx *= -1;
    if (this.y - this.radius < 0 || this.y + this.radius > canvas.height)
      this.dy *= -1;
    this.draw();
  }
}

const planets = [
  new Planet(200, 200, 40, "/img/earth.png", 0.5, 0.4),
  new Planet(600, 400, 60, "/img/mars.png", -0.5, 0.5),
  new Planet(1000, 300, 50, "/img/jupiter.png", 0.4, -0.5),
  new Planet(400, 600, 30, "/img/venus.png", -0.4, -0.5),
  new Planet(800, 500, 70, "/img/saturn.png", 0.5, -0.4),
];

console.log("[Dashboard.js] Planets created:", planets.length);

function animate() {
  if (canvas.style.display !== "none") {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    planets.forEach((p) => p.update());
  }
  requestAnimationFrame(animate);
}

console.log("[Dashboard.js] Starting animation...");
animate();
console.log("[Dashboard.js] Dashboard.js loaded successfully!");
