// === Canvas Espacial ===
const canvas = document.getElementById("spaceCanvas");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

window.addEventListener("resize", () => {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
});

// === Workspace dinámico ===
const workspace = document.getElementById("workspace");

// Función para mostrar contenido en el workspace y ocultar canvas
function showContent(section) {
  // Ocultar canvas
  canvas.style.display = "none";

  // Limpiar workspace
  workspace.innerHTML = "";

  switch(section) {
    case "newCandidate":
      workspace.innerHTML = `
        <h2 class="text-2xl font-bold mb-4">New Candidate</h2>
        <p>No hay datos para mostrar</p>
      `;
      break;
    case "manageCandidate":
      workspace.innerHTML = `
        <h2 class="text-2xl font-bold mb-4">Manage Candidates</h2>
        <p>No hay datos para mostrar</p>
      `;
      break;
    case "newTable":
      workspace.innerHTML = `
        <h2 class="text-2xl font-bold mb-4">New Table</h2>
        <p>No hay datos para mostrar</p>
      `;
      break;
    case "manageTable":
      workspace.innerHTML = `
        <h2 class="text-2xl font-bold mb-4">Manage Tables</h2>
        <p>No hay datos para mostrar</p>
      `;
      break;
    default:
      // Mostrar el canvas nuevamente y contenido inicial
      canvas.style.display = "block";
      workspace.innerHTML = `
        <h1 class="text-3xl font-bold text-rocket flex items-center">
          🚀 Welcome to ExoFinder
        </h1>
        <p class="mt-2 text-space-star">
          Select an option from the sidebar menu to continue.
        </p>
      `;
  }
}

// === Manejo de submenus y enlaces ===
function toggleMenu(id) {
  // Ocultar todos los submenus
  const allMenus = document.querySelectorAll('nav ul[id$="Menu"]');
  allMenus.forEach(menu => {
    if (menu.id !== id) menu.classList.add("hidden");
  });

  // Alterna el submenu seleccionado
  const menu = document.getElementById(id);
  menu.classList.toggle("hidden");
}

// === Configurar eventos de los links del menú ===
document.addEventListener("DOMContentLoaded", () => {
  // Candidate Menu
  document.querySelectorAll("#candidateMenu a").forEach(link => {
    link.addEventListener("click", e => {
      e.preventDefault();
      const section = link.textContent.replace(/\s+/g, "").toLowerCase();
      if(section.includes("newcandidate")) showContent("newCandidate");
      if(section.includes("managecandidates") || section.includes("managecandidate")) showContent("manageCandidate");
    });
  });

  // Tables Menu
  document.querySelectorAll("#tablesMenu a").forEach(link => {
    link.addEventListener("click", e => {
      e.preventDefault();
      const section = link.textContent.replace(/\s+/g, "").toLowerCase();
      if(section.includes("newtable")) showContent("newTable");
      if(section.includes("managetables") || section.includes("managetable")) showContent("manageTable");
    });
  });

  // Dashboard button: recarga y muestra planetas
  const dashboardBtn = document.querySelector('button[onclick="location.reload()"]');
  dashboardBtn.addEventListener("click", () => showContent("default"));
});

// === Clase Planeta ===
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

    if (this.img.src.includes("saturn")) {
      ctx.ellipse(this.x, this.y, this.radius * 1.8, this.radius, 0, 0, Math.PI * 2);
      ctx.clip();
      ctx.drawImage(this.img, this.x - this.radius * 1.8, this.y - this.radius, this.radius * 3.6, this.radius * 2);
    } else {
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.clip();
      ctx.drawImage(this.img, this.x - this.radius, this.y - this.radius, this.radius * 2, this.radius * 2);
    }

    ctx.restore();
  }

  update(planets) {
    this.x += this.dx;
    this.y += this.dy;

    if (this.x - this.radius < 0 || this.x + this.radius > canvas.width) this.dx *= -1;
    if (this.y - this.radius < 0 || this.y + this.radius > canvas.height) this.dy *= -1;

    for (let other of planets) {
      if (other !== this) {
        const dx = this.x - other.x;
        const dy = this.y - other.y;
        const dist = Math.hypot(dx, dy);
        const minDist = this.radius + other.radius;
        if (dist < minDist) {
          const midX = (this.x + other.x) / 2;
          const midY = (this.y + other.y) / 2;
          createExplosion(midX, midY);

          const angle = Math.atan2(dy, dx);
          const overlap = (minDist - dist) / 2;

          this.x += Math.cos(angle) * overlap;
          this.y += Math.sin(angle) * overlap;
          other.x -= Math.cos(angle) * overlap;
          other.y -= Math.sin(angle) * overlap;

          const tempDx = this.dx;
          const tempDy = this.dy;
          this.dx = other.dx;
          this.dy = other.dy;
          other.dx = tempDx;
          other.dy = tempDy;
        }
      }
    }

    this.draw();
  }
}

// === Sistema de explosiones ===
let particles = [];

class Particle {
  constructor(x, y, color) {
    this.x = x;
    this.y = y;
    this.radius = Math.random() * 3;
    this.color = color;
    this.dx = (Math.random() - 0.5) * 6;
    this.dy = (Math.random() - 0.5) * 6;
    this.life = 100;
  }

  draw() {
    ctx.globalAlpha = this.life / 100;
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
    ctx.fillStyle = this.color;
    ctx.shadowBlur = 10;
    ctx.shadowColor = this.color;
    ctx.fill();
    ctx.globalAlpha = 1;
  }

  update() {
    this.x += this.dx;
    this.y += this.dy;
    this.life--;
    this.draw();
  }
}

function createExplosion(x, y) {
  for (let i = 0; i < 40; i++) {
    const colors = ["orange", "yellow", "red", "white"];
    const color = colors[Math.floor(Math.random() * colors.length)];
    particles.push(new Particle(x, y, color));
  }
}

// === Crear planetas ===
const planets = [
  new Planet(200, 200, 40, "/img/earth.png", 0.5, 0.4),
  new Planet(600, 400, 60, "/img/mars.png", -0.5, 0.5),
  new Planet(1000, 300, 50, "/img/jupiter.png", 0.4, -0.5),
  new Planet(400, 600, 30, "/img/venus.png", -0.4, -0.5),
  new Planet(800, 500, 70, "/img/saturn.png", 0.5, -0.4)
];

// === Animación ===
function animate() {
  if(canvas.style.display !== "none") {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    planets.forEach(p => p.update(planets));
    particles = particles.filter(p => p.life > 0);
    particles.forEach(p => p.update());
  }
  requestAnimationFrame(animate);
}

animate();
