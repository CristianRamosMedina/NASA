// upload.js - Manejo de subida de archivos
document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const uploadProgress = document.getElementById('uploadProgress');
    const uploadStatus = document.getElementById('uploadStatus');
    const previewContainer = document.getElementById('previewContainer');

    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            previewContainer.innerHTML = '';
            
            Array.from(e.target.files).forEach(file => {
                if (file.type.startsWith('image/')) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        const preview = document.createElement('div');
                        preview.className = 'file-preview';
                        preview.innerHTML = `
                            <img src="${e.target.result}" alt="${file.name}">
                            <span>${file.name}</span>
                        `;
                        previewContainer.appendChild(preview);
                    };
                    reader.readAsDataURL(file);
                } else {
                    const preview = document.createElement('div');
                    preview.className = 'file-preview';
                    preview.innerHTML = `
                        <div class="file-icon">📄</div>
                        <span>${file.name}</span>
                    `;
                    previewContainer.appendChild(preview);
                }
            });
        });
    }

    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData();
            Array.from(fileInput.files).forEach(file => {
                formData.append('files', file);
            });

            const xhr = new XMLHttpRequest();
            
            xhr.upload.addEventListener('progress', function(e) {
                if (e.lengthComputable) {
                    const percentComplete = (e.loaded / e.total) * 100;
                    uploadProgress.value = percentComplete;
                }
            });

            xhr.addEventListener('load', function() {
                if (xhr.status === 200) {
                    uploadStatus.innerHTML = '<span style="color: #4ade80;">✅ Upload successful!</span>';
                    setTimeout(() => {
                        window.location.href = '/galeria';
                    }, 1500);
                } else {
                    uploadStatus.innerHTML = '<span style="color: #ef4444;">❌ Upload failed!</span>';
                }
            });

            xhr.addEventListener('error', function() {
                uploadStatus.innerHTML = '<span style="color: #ef4444;">❌ Upload error!</span>';
            });

            xhr.open('POST', '/api/upload');
            xhr.send(formData);
            
            uploadStatus.innerHTML = '<span style="color: #409cff;">🚀 Uploading files to space...</span>';
        });
    }
});