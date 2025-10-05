document.addEventListener("DOMContentLoaded", () => {
  const tableBody = document.getElementById("manageCandidatesBody");
  const tempData = localStorage.getItem("tempCandidates");

  if (!tempData) return; // No hay datos enviados

  const candidates = JSON.parse(tempData);
  tableBody.innerHTML = ""; // Limpiar tabla

  candidates.forEach(candidate => {
    const tr = document.createElement("tr");
    candidate.forEach(value => {
      const td = document.createElement("td");
      td.textContent = value || "-";
      td.classList.add("px-2", "py-1", "border-b", "border-planet", "text-space-star");
      tr.appendChild(td);
    });
    tableBody.appendChild(tr);
  });

  // 🧹 Eliminar datos al recargar la página
  window.addEventListener("beforeunload", () => {
    localStorage.removeItem("tempCandidates");
  });
});
