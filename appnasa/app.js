const express = require('express');
const path = require('path');
const multer = require('multer');

// Importar rutas
const archivosRoutes = require('./routes/archivosRoutes');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware para archivos estáticos
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.static(path.join(__dirname, 'views')));

// Middleware para parsear JSON y form data
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Configuración de Multer para subida de archivos
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, path.join(__dirname, 'public/uploads'));
    },
    filename: function (req, file, cb) {
        // Guardar con nombre original y timestamp para evitar duplicados
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
        cb(null, uniqueSuffix + '-' + file.originalname);
    }
});

const upload = multer({ 
    storage: storage,
    limits: {
        fileSize: 10 * 1024 * 1024 // 10MB límite
    },
    fileFilter: function (req, file, cb) {
        // Permitir solo imágenes y algunos tipos de archivos
        const allowedTypes = /jpeg|jpg|png|gif|pdf|txt|doc|docx/;
        const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase());
        const mimetype = allowedTypes.test(file.mimetype);

        if (mimetype && extname) {
            return cb(null, true);
        } else {
            cb('Error: Solo se permiten archivos de imagen y documentos');
        }
    }
});

// Middleware para hacer disponible 'upload' en las rutas
app.use((req, res, next) => {
    req.upload = upload;
    next();
});

// Configurar EJS como motor de vistas (opcional, pero útil para MVC)
app.set('view engine', 'html');
app.engine('html', require('fs').readFileSync);

// Rutas
app.use('/', archivosRoutes);

// Ruta para servir el index.html principal
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'views', 'index.html'));
});

// Manejo de errores 404
app.use((req, res) => {
    res.status(404).send(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>404 - Page Not Found</title>
            <link rel="stylesheet" href="/css/style.css">
        </head>
        <body>
            <div class="container">
                <div style="text-align: center; padding: 100px;">
                    <h1>🚀 404 - Lost in Space</h1>
                    <p>The page you're looking for is in another galaxy.</p>
                    <a href="/" style="color: #409cff;">Return to Home Base</a>
                </div>
            </div>
        </body>
        </html>
    `);
});

// Manejo de errores global
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).send(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>500 - Server Error</title>
            <link rel="stylesheet" href="/css/style.css">
        </head>
        <body>
            <div class="container">
                <div style="text-align: center; padding: 100px;">
                    <h1>🛰️ 500 - System Malfunction</h1>
                    <p>Our systems are experiencing technical difficulties.</p>
                    <a href="/" style="color: #409cff;">Return to Home Base</a>
                </div>
            </div>
        </body>
        </html>
    `);
});

// Iniciar servidor
app.listen(PORT, () => {
    console.log(`🚀 EXO(0)PLORER server launched on port ${PORT}`);
    console.log(`🌐 Visit: http://localhost:${PORT}`);
    console.log(`📁 Uploads folder: ${path.join(__dirname, 'public/uploads')}`);
});

module.exports = app;