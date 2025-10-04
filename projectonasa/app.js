const express = require("express");
const path = require("path");

const app = express();
const PORT = 3000;

const viewsPath = path.join(__dirname, "views");
const publicPath = path.join(__dirname, "public");

// Configuración de EJS
app.set("view engine", "ejs");
app.set("views", viewsPath);

// Archivos estáticos (CSS, JS, imágenes)
app.use(express.static(publicPath));

// Rutas
app.get("/", (req, res) => {
  res.render("dashboard"); // Renderiza views/dashboard.ejs
});

// Iniciar servidor
app.listen(PORT, () => {
  console.log(`🚀 Servidor corriendo en http://localhost:${PORT}`);
});
