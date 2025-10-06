const express = require('express');
const path = require('path');
const fs = require('fs');
const router = express.Router();

// Controlador simple (sin modelo para mantenerlo simple)
const archivosController = {
    // Mostrar página de subida
    showUpload: (req, res) => {
        res.sendFile(path.join(__dirname, '../views/subir.html'));
    },

    // Mostrar galería
    showGallery: (req, res) => {
        res.sendFile(path.join(__dirname, '../views/galeria.html'));
    },

    // Subir archivo
    uploadFile: (req, res) => {
        if (!req.file) {
            return res.status(400).json({ error: 'No file uploaded' });
        }

        res.json({
            message: 'File uploaded successfully!',
            file: {
                filename: req.file.filename,
                originalname: req.file.originalname,
                size: req.file.size,
                path: `/uploads/${req.file.filename}`
            }
        });
    },

    // Obtener lista de archivos
    getFiles: (req, res) => {
        const uploadsDir = path.join(__dirname, '../public/uploads');
        
        fs.readdir(uploadsDir, (err, files) => {
            if (err) {
                return res.status(500).json({ error: 'Unable to read uploads directory' });
            }

            const fileList = files.map(file => {
                const filePath = path.join(uploadsDir, file);
                const stats = fs.statSync(filePath);
                const isImage = /\.(jpg|jpeg|png|gif|webp)$/i.test(file);
                
                return {
                    name: file,
                    path: `/uploads/${file}`,
                    size: stats.size,
                    isImage: isImage,
                    uploadDate: stats.birthtime
                };
            });

            res.json(fileList);
        });
    },

    // Eliminar archivo
    deleteFile: (req, res) => {
        const filename = req.params.filename;
        const filePath = path.join(__dirname, '../public/uploads', filename);

        fs.unlink(filePath, (err) => {
            if (err) {
                return res.status(500).json({ error: 'Unable to delete file' });
            }
            res.json({ message: 'File deleted successfully' });
        });
    }
};

// Rutas
router.get('/subir', archivosController.showUpload);
router.get('/galeria', archivosController.showGallery);
router.post('/api/upload', (req, res) => {
    // Usar el middleware de multer para subir un solo archivo
    req.upload.single('file')(req, res, (err) => {
        if (err) {
            return res.status(400).json({ error: err });
        }
        archivosController.uploadFile(req, res);
    });
});
router.get('/api/files', archivosController.getFiles);
router.delete('/api/files/:filename', archivosController.deleteFile);

module.exports = router;