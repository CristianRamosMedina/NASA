// Toggle sidebar y funcionalidad New Candidate - Versión Unificada
document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('toggleBtn');
    const mainContent = document.getElementById('mainContent');
    const container = document.querySelector('.container');

    // ===========================
    // Variables para New Candidate
    // ===========================
    const newCandidateBtn = document.getElementById('newCandidateBtn');
    const backToDashboardBtn = document.getElementById('backToDashboard');
    const clearFormBtn = document.getElementById('clearForm');
    const dashboardSection = document.getElementById('dashboardSection');
    const newCandidateSection = document.getElementById('newCandidateSection');
    const candidateForm = document.getElementById('candidateForm');

    // ===========================
    // Variables para Manage Candidate
    // ===========================
    const manageCandidateBtn = document.getElementById('manageCandidateBtn');
    const manageCandidateSection = document.getElementById('manageCandidateSection');
    const backToDashboardFromManageBtn = document.getElementById('backToDashboardFromManage');
    const clearAllDataBtn = document.getElementById('clearAllData');
    const exportExcelBtn = document.getElementById('exportExcel');
    const candidateTableBody = document.getElementById('candidateTableBody');
    const recordCount = document.getElementById('recordCount');

    // ===========================
    // Variables para New Table y Manage Table
    // ===========================
    const newTableBtn = document.getElementById('newTableBtn');
    const manageTableBtn = document.getElementById('manageTableBtn');
    const newTableSection = document.getElementById('newTableSection');
    const manageTableSection = document.getElementById('manageTableSection');
    const backToDashboardFromNewTableBtn = document.getElementById('backToDashboardFromNewTable');
    const backToDashboardFromManageTableBtn = document.getElementById('backToDashboardFromManageTable');
    const csvFileInput = document.getElementById('csvFile');
    const uploadBtn = document.getElementById('uploadBtn');
    const uploadArea = document.getElementById('uploadArea');
    const uploadPreview = document.getElementById('uploadPreview');
    const previewTableContainer = document.getElementById('previewTableContainer');
    const confirmUploadBtn = document.getElementById('confirmUpload');
    const cancelUploadBtn = document.getElementById('cancelUpload');
    const exoplanetTableBody = document.getElementById('exoplanetTableBody');
    const exoplanetTableHead = document.getElementById('exoplanetTableHead');
    const exoplanetRecordCount = document.getElementById('exoplanetRecordCount');
    const downloadProcessedCsvBtn = document.getElementById('downloadProcessedCsv');
    const clearExoplanetDataBtn = document.getElementById('clearExoplanetData');

    // ===========================
    // Variables para Statistics y Documentation
    // ===========================
    const statisticsBtn = document.querySelector('a[data-tooltip="Statistics"]');
    const documentationBtn = document.querySelector('a[data-tooltip="Documentation"]');
    const statisticsSection = document.getElementById('statisticsSection');
    const documentationSection = document.getElementById('documentationSection');
    const backToDashboardFromStatisticsBtn = document.getElementById('backToDashboardFromStatistics');
    const backToDashboardFromDocumentationBtn = document.getElementById('backToDashboardFromDocumentation');
    const imagesContainer = document.getElementById('imagesContainer');
    const csvFilesContainer = document.getElementById('csvFilesContainer');

    // ===========================
    // Toggle sidebar
    // ===========================
    function ensureToggleVisibility() {
        if (toggleBtn) {
            toggleBtn.style.display = 'flex';
            toggleBtn.style.visibility = 'visible';
            toggleBtn.style.opacity = '1';
            toggleBtn.style.zIndex = '1001';
        }
    }

    function initSidebar() {
        ensureToggleVisibility();
        if (window.innerWidth <= 768) {
            sidebar.classList.add('collapsed');
            if (toggleBtn) {
                toggleBtn.textContent = '☰';
                toggleBtn.style.fontSize = '3rem';
            }
        } else {
            sidebar.classList.remove('collapsed');
            if (toggleBtn) {
                toggleBtn.textContent = '✕';
                toggleBtn.style.fontSize = '4rem';
            }
        }
    }

    if (toggleBtn) {
        toggleBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            sidebar.classList.toggle('collapsed');

            if (sidebar.classList.contains('collapsed')) {
                toggleBtn.textContent = '☰';
                toggleBtn.style.fontSize = '3rem';
                toggleBtn.style.transform = 'rotate(0deg)';
                createParticles();
                showNotification('Menu collapsed!', 'info');
            } else {
                toggleBtn.textContent = '✕';
                toggleBtn.style.fontSize = '4rem';
                toggleBtn.style.transform = 'rotate(180deg)';
                showNotification('Menu expanded!', 'success');
            }

            setTimeout(() => ensureToggleVisibility(), 500);
        });
    }

    // Mobile menu functionality
    function handleMobileMenu() {
        if (window.innerWidth <= 768) {
            sidebar.classList.remove('collapsed');
            if (sidebar.classList.contains('active')) {
                container.classList.add('sidebar-active');
                document.body.style.overflow = 'hidden';
            } else {
                container.classList.remove('sidebar-active');
                document.body.style.overflow = 'auto';
            }
        } else {
            sidebar.classList.remove('active');
            container.classList.remove('sidebar-active');
            document.body.style.overflow = 'auto';
        }
        ensureToggleVisibility();
    }

    // Initialize sidebar
    initSidebar();
    handleMobileMenu();
    ensureToggleVisibility();

    // Handle window resize
    window.addEventListener('resize', function () {
        initSidebar();
        handleMobileMenu();
        ensureToggleVisibility();
    });

    // Add click outside to close mobile menu
    document.addEventListener('click', function (event) {
        if (window.innerWidth <= 768 &&
            sidebar &&
            !sidebar.contains(event.target) &&
            toggleBtn &&
            !toggleBtn.contains(event.target) &&
            sidebar.classList.contains('active')) {
            sidebar.classList.remove('active');
            container.classList.remove('sidebar-active');
            document.body.style.overflow = 'auto';
        }
    });

    // Mobile menu toggle
    if (toggleBtn) {
        toggleBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            if (window.innerWidth <= 768) {
                if (sidebar.classList.contains('active')) {
                    sidebar.classList.remove('active');
                    container.classList.remove('sidebar-active');
                    document.body.style.overflow = 'auto';
                } else {
                    sidebar.classList.add('active');
                    container.classList.add('sidebar-active');
                    document.body.style.overflow = 'hidden';
                }
            }
        });
    }

    // ===========================
    // Cards hover & click
    // ===========================
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-8px)';
            card.style.zIndex = '10';
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0) scale(1)';
            card.style.zIndex = '1';
        });

        card.addEventListener('click', () => {
            card.style.transform = 'scale(0.95)';
            setTimeout(() => {
                card.style.transform = 'translateY(-8px)';
            }, 200);
        });
    });

    // ===========================
    // Activity animation
    // ===========================
    const activityItems = document.querySelectorAll('.activity-item');
    activityItems.forEach((item, index) => {
        item.style.animationDelay = `${index * 0.1}s`;
        item.classList.add('fade-in');
    });

    // ===========================
    // New Candidate Form Functionality
    // ===========================

    // Show New Candidate Form
    if (newCandidateBtn) {
        newCandidateBtn.addEventListener('click', function (e) {
            e.preventDefault();
            if (dashboardSection) dashboardSection.classList.add('hidden');
            if (newCandidateSection) newCandidateSection.classList.remove('hidden');
            if (manageCandidateSection) manageCandidateSection.classList.add('hidden');
            if (newTableSection) newTableSection.classList.add('hidden');
            if (manageTableSection) manageTableSection.classList.add('hidden');

            // Close sidebar on mobile
            if (window.innerWidth <= 768 && sidebar) {
                sidebar.classList.remove('active');
                if (container) container.classList.remove('sidebar-active');
                document.body.style.overflow = 'auto';
            }

            showNotification('🚀 Kepler Candidate Data Form Opened!', 'info');

            // Add table info
            addTableInfo();
        });
    }

    // Back to Dashboard
    if (backToDashboardBtn) {
        backToDashboardBtn.addEventListener('click', function () {
            if (dashboardSection) dashboardSection.classList.remove('hidden');
            if (newCandidateSection) newCandidateSection.classList.add('hidden');
            if (manageCandidateSection) manageCandidateSection.classList.add('hidden');
            if (newTableSection) newTableSection.classList.add('hidden');
            if (manageTableSection) manageTableSection.classList.add('hidden');
            showNotification('📊 Returning to dashboard...', 'info');
        });
    }

    // Clear Form
    if (clearFormBtn) {
        clearFormBtn.addEventListener('click', function () {
            if (confirm('Are you sure you want to clear all form data?')) {
                if (candidateForm) candidateForm.reset();
                showNotification('🧹 Form cleared successfully!', 'warning');

                // Reset input styles
                const inputs = document.querySelectorAll('.table-input');
                inputs.forEach(input => {
                    input.style.borderColor = 'rgba(64, 156, 255, 0.3)';
                    input.style.boxShadow = 'none';
                });
            }
        });
    }

    // Form Submission - ACTUALIZADO para guardar en localStorage
    if (candidateForm) {
        candidateForm.addEventListener('submit', function (e) {
            e.preventDefault();

            // Validate required fields
            if (!validateForm()) {
                showNotification('⚠️ Please fill in all required fields correctly!', 'error');
                return;
            }

            // Collect form data
            const formData = new FormData(candidateForm);
            const candidateData = {};
            let filledFields = 0;

            for (let [key, value] of formData.entries()) {
                if (value.trim() !== '') {
                    candidateData[key] = value;
                    filledFields++;
                }
            }

            // Save to localStorage
            const saveSuccess = saveCandidateData(candidateData);

            if (saveSuccess) {
                // Show success message with stats
                showNotification(`✅ Candidate data saved! (${filledFields}/30 fields filled)`, 'success');

                // Reset form and return to dashboard after delay
                setTimeout(() => {
                    if (candidateForm) candidateForm.reset();
                    if (dashboardSection) dashboardSection.classList.remove('hidden');
                    if (newCandidateSection) newCandidateSection.classList.add('hidden');

                    // Update dashboard with new activity
                    updateRecentActivity(`New candidate added with ${filledFields} fields`);
                }, 2500);
            } else {
                showNotification('❌ Error saving candidate data!', 'error');
            }
        });
    }

    // Enhanced input validation for new data types
    const numberInputs = document.querySelectorAll('.table-input');
    numberInputs.forEach(input => {
        input.addEventListener('blur', function () {
            validateInput(this);
        });

        input.addEventListener('input', function () {
            // Real-time validation feedback
            if (this.value.trim() !== '') {
                validateInput(this);
            }
        });
    });

    // Input validation function - ACTUALIZADO para nuevos tipos
    function validateInput(input) {
        const value = input.value.trim();
        const fieldName = input.name;

        // Get the data type from the corresponding data-type span
        const dataTypeElement = input.closest('tr').querySelector('.data-type');
        const dataType = dataTypeElement ? dataTypeElement.textContent.toLowerCase().trim() : 'number';

        if (value === '') {
            input.style.borderColor = 'rgba(64, 156, 255, 0.3)';
            input.style.boxShadow = 'none';
            return true; // Empty is allowed
        }

        // Boolean fields (0 or 1)
        if (dataType === 'boolean') {
            if (value === '0' || value === '1') {
                input.style.borderColor = '#4ade80';
                input.style.boxShadow = '0 0 10px rgba(74, 222, 128, 0.3)';
                // Update data type color
                dataTypeElement.className = 'data-type boolean';
                return true;
            } else {
                input.style.borderColor = '#ef4444';
                input.style.boxShadow = '0 0 10px rgba(239, 68, 68, 0.3)';
                dataTypeElement.className = 'data-type boolean';
                return false;
            }
        }

        // Integer fields
        if (dataType === 'integer') {
            if (Number.isInteger(Number(value)) && !isNaN(value) && value !== '') {
                input.style.borderColor = '#4ade80';
                input.style.boxShadow = '0 0 10px rgba(74, 222, 128, 0.3)';
                dataTypeElement.className = 'data-type integer';
                return true;
            } else {
                input.style.borderColor = '#ef4444';
                input.style.boxShadow = '0 0 10px rgba(239, 68, 68, 0.3)';
                dataTypeElement.className = 'data-type integer';
                return false;
            }
        }

        // Number fields (including decimals)
        if (dataType === 'number') {
            if (!isNaN(value) && value !== '') {
                input.style.borderColor = '#4ade80';
                input.style.boxShadow = '0 0 10px rgba(74, 222, 128, 0.3)';
                dataTypeElement.className = 'data-type number';
                return true;
            } else {
                input.style.borderColor = '#ef4444';
                input.style.boxShadow = '0 0 10px rgba(239, 68, 68, 0.3)';
                dataTypeElement.className = 'data-type number';
                return false;
            }
        }

        // Default case for unknown types
        input.style.borderColor = 'rgba(64, 156, 255, 0.3)';
        input.style.boxShadow = 'none';
        return true;
    }

    // Form validation
    function validateForm() {
        let isValid = true;
        const inputs = document.querySelectorAll('.table-input');

        inputs.forEach(input => {
            if (input.value.trim() !== '' && !validateInput(input)) {
                isValid = false;
                // Scroll to first invalid input
                if (isValid) { // This will only be true for the first invalid input
                    input.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    input.focus();
                }
            }
        });

        return isValid;
    }

    // Add table information - ACTUALIZADO
    function addTableInfo() {
        const formContainer = document.querySelector('.form-container');
        if (!formContainer) return;

        let tableInfo = document.querySelector('.table-info');

        if (!tableInfo) {
            tableInfo = document.createElement('div');
            tableInfo.className = 'table-info';
            formContainer.insertBefore(tableInfo, formContainer.firstChild);
        }

        const totalFields = document.querySelectorAll('.table-input').length;
        const numberFields = document.querySelectorAll('.data-type.number').length;
        const integerFields = document.querySelectorAll('.data-type.integer').length;
        const booleanFields = document.querySelectorAll('.data-type.boolean').length;

        tableInfo.innerHTML = `
            📊 <strong>Kepler Object of Interest (KOI) Data Table</strong> | 
            Total Fields: ${totalFields} | 
            Types: Number (${numberFields}), Integer (${integerFields}), Boolean (${booleanFields})
        `;
    }

    // Update recent activity
    function updateRecentActivity(activityText) {
        const activityList = document.querySelector('.activity-list');
        if (activityList) {
            const newActivity = document.createElement('div');
            newActivity.className = 'activity-item fade-in';
            newActivity.innerHTML = `
                <span class="activity-icon">👤</span>
                <div class="activity-details">
                    <p>${activityText}</p>
                    <span class="activity-time">Just now</span>
                </div>
            `;
            activityList.insertBefore(newActivity, activityList.firstChild);

            // Limit to 5 activities
            const activities = activityList.querySelectorAll('.activity-item');
            if (activities.length > 5) {
                activities[activities.length - 1].remove();
            }
        }
    }

    // Handle menu item clicks
    const menuItems = document.querySelectorAll('.menu-items a');
    menuItems.forEach(item => {
        item.addEventListener('click', function (e) {
            // Remove active class from all items
            menuItems.forEach(i => i.classList.remove('active'));
            // Add active class to clicked item
            this.classList.add('active');

            // Add click effect
            this.style.transform = 'scale(0.9)';
            setTimeout(() => {
                this.style.transform = '';
            }, 300);

            // Close sidebar on mobile after selection
            if (window.innerWidth <= 768 && sidebar) {
                sidebar.classList.remove('active');
                if (container) container.classList.remove('sidebar-active');
                document.body.style.overflow = 'auto';
            }

            // If it's a link to another page, allow normal navigation
            if (this.getAttribute('href') && this.getAttribute('href') !== '#') {
                return true;
            }

            // Prevent default for # links
            e.preventDefault();

            // Show loading state with fun animation
            const originalText = this.querySelector('.menu-text').textContent;
            const originalIcon = this.querySelector('.menu-icon').textContent;

            this.querySelector('.menu-text').textContent = 'LOADING...';
            this.querySelector('.menu-icon').textContent = '⏳';
            this.querySelector('.menu-icon').style.animation = 'spin 1s linear infinite';

            setTimeout(() => {
                this.querySelector('.menu-text').textContent = originalText;
                this.querySelector('.menu-icon').textContent = originalIcon;
                this.querySelector('.menu-icon').style.animation = '';
                showNotification(`Navigating to ${originalText}`, 'info');
            }, 1500);
        });
    });

    // ===========================
    // Manage Candidate Functionality
    // ===========================

    // Show Manage Candidate Section
    if (manageCandidateBtn) {
        manageCandidateBtn.addEventListener('click', function (e) {
            e.preventDefault();
            if (dashboardSection) dashboardSection.classList.add('hidden');
            if (newCandidateSection) newCandidateSection.classList.add('hidden');
            if (manageCandidateSection) manageCandidateSection.classList.remove('hidden');
            if (newTableSection) newTableSection.classList.add('hidden');
            if (manageTableSection) manageTableSection.classList.add('hidden');

            // Close sidebar on mobile
            if (window.innerWidth <= 768 && sidebar) {
                sidebar.classList.remove('active');
                if (container) container.classList.remove('sidebar-active');
                document.body.style.overflow = 'auto';
            }

            // Load and display saved candidate data
            loadCandidateData();

            showNotification('📊 Managing candidate data...', 'info');
        });
    }

    // Back to Dashboard from Manage Candidate
    if (backToDashboardFromManageBtn) {
        backToDashboardFromManageBtn.addEventListener('click', function () {
            if (dashboardSection) dashboardSection.classList.remove('hidden');
            if (manageCandidateSection) manageCandidateSection.classList.add('hidden');
            showNotification('📊 Returning to dashboard...', 'info');
        });
    }

    // Clear All Data
    if (clearAllDataBtn) {
        clearAllDataBtn.addEventListener('click', function () {
            if (confirm('Are you sure you want to delete ALL candidate data? This action cannot be undone.')) {
                localStorage.removeItem('candidateData');
                loadCandidateData();
                showNotification('🗑️ All candidate data cleared!', 'warning');
            }
        });
    }

    // Export to Excel
    if (exportExcelBtn) {
        exportExcelBtn.addEventListener('click', function () {
            exportToExcel();
        });
    }

    // ===========================
    // Local Storage Management
    // ===========================

    // Save candidate data to localStorage
    function saveCandidateData(formData) {
        try {
            // Get existing data or initialize empty array
            const existingData = JSON.parse(localStorage.getItem('candidateData')) || [];

            // Create new candidate object with ID and timestamp
            const newCandidate = {
                id: Date.now(), // Simple unique ID
                timestamp: new Date().toISOString(),
                ...formData
            };

            // Add to existing data
            existingData.push(newCandidate);

            // Save back to localStorage
            localStorage.setItem('candidateData', JSON.stringify(existingData));

            return true;
        } catch (error) {
            console.error('Error saving candidate data:', error);
            return false;
        }
    }

    // Load candidate data from localStorage
    function loadCandidateData() {
        try {
            const candidateData = JSON.parse(localStorage.getItem('candidateData')) || [];
            displayCandidateData(candidateData);
            updateRecordCount(candidateData.length);
            return candidateData;
        } catch (error) {
            console.error('Error loading candidate data:', error);
            displayCandidateData([]);
            updateRecordCount(0);
            return [];
        }
    }

    // Display candidate data in the table
    function displayCandidateData(data) {
        if (!candidateTableBody) return;

        candidateTableBody.innerHTML = '';

        if (data.length === 0) {
            candidateTableBody.innerHTML = `
                <tr>
                    <td colspan="11" class="empty-state">
                        <div class="empty-icon">📭</div>
                        <p>No candidate data saved yet</p>
                        <p style="font-size: 0.9rem; margin-top: 10px;">Go to "New Candidate" to add data</p>
                    </td>
                </tr>
            `;
            return;
        }

        // Sort by timestamp (newest first)
        const sortedData = data.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

        sortedData.forEach((candidate, index) => {
            const row = document.createElement('tr');
            if (index === 0) row.classList.add('new-row');

            row.innerHTML = `
                <td>${candidate.id}</td>
                <td>${candidate.koi_period || ''}</td>
                <td>${candidate.koi_sma || ''}</td>
                <td>${candidate.koi_eccen || ''}</td>
                <td>${candidate.koi_incl || ''}</td>
                <td>${candidate.koi_prad || ''}</td>
                <td>${candidate.koi_duration || ''}</td>
                <td>${candidate.koi_depth || ''}</td>
                <td>${candidate.koi_ror || ''}</td>
                <td>${candidate.koi_impact || ''}</td>
                <td class="actions-cell">
                    <button class="btn btn-small edit-btn" data-id="${candidate.id}">Edit</button>
                    <button class="btn btn-small delete-btn" data-id="${candidate.id}">Delete</button>
                </td>
            `;

            candidateTableBody.appendChild(row);
        });

        // Add event listeners for action buttons
        addTableActionListeners();
    }

    // Update record count display
    function updateRecordCount(count) {
        if (recordCount) {
            recordCount.textContent = count;
            recordCount.style.background = count > 0 ?
                'rgba(34, 197, 94, 0.3)' : 'rgba(64, 156, 255, 0.3)';
            recordCount.style.color = count > 0 ? '#22c55e' : '#409cff';
        }
    }

    // Add event listeners for table action buttons
    function addTableActionListeners() {
        // Edit buttons
        document.querySelectorAll('.edit-btn').forEach(btn => {
            btn.addEventListener('click', function () {
                const candidateId = this.getAttribute('data-id');
                editCandidate(candidateId);
            });
        });

        // Delete buttons
        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', function () {
                const candidateId = this.getAttribute('data-id');
                deleteCandidate(candidateId);
            });
        });
    }

    // Edit candidate function
    function editCandidate(candidateId) {
        const candidateData = JSON.parse(localStorage.getItem('candidateData')) || [];
        const candidate = candidateData.find(c => c.id == candidateId);

        if (candidate) {
            showNotification('✏️ Edit functionality coming soon!', 'info');
            // Here you would populate the form with candidate data
            // and switch to the New Candidate section for editing
        }
    }

    // Delete candidate function
    function deleteCandidate(candidateId) {
        if (confirm('Are you sure you want to delete this candidate?')) {
            const candidateData = JSON.parse(localStorage.getItem('candidateData')) || [];
            const updatedData = candidateData.filter(c => c.id != candidateId);

            localStorage.setItem('candidateData', JSON.stringify(updatedData));
            loadCandidateData();
            showNotification('🗑️ Candidate deleted successfully!', 'warning');
        }
    }

    // Export to Excel function
    function exportToExcel() {
        const candidateData = JSON.parse(localStorage.getItem('candidateData')) || [];

        if (candidateData.length === 0) {
            showNotification('📭 No data to export!', 'warning');
            return;
        }

        // Create CSV content
        const headers = ['ID', 'Orbital Period', 'Semi-major Axis', 'Eccentricity', 'Inclination',
            'Planet Radius', 'Transit Duration', 'Transit Depth', 'Radius Ratio', 'Impact Parameter', 'Date Added'];

        let csvContent = headers.join(',') + '\n';

        candidateData.forEach(candidate => {
            const row = [
                candidate.id,
                candidate.koi_period || '',
                candidate.koi_sma || '',
                candidate.koi_eccen || '',
                candidate.koi_incl || '',
                candidate.koi_prad || '',
                candidate.koi_duration || '',
                candidate.koi_depth || '',
                candidate.koi_ror || '',
                candidate.koi_impact || '',
                new Date(candidate.timestamp).toLocaleDateString()
            ];
            csvContent += row.join(',') + '\n';
        });

        // Create and download file
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);

        link.setAttribute('href', url);
        link.setAttribute('download', `candidate_data_${new Date().toISOString().split('T')[0]}.csv`);
        link.style.visibility = 'hidden';

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        showNotification('📥 Data exported successfully!', 'success');
    }

    // ===========================
    // New Table & Manage Table Functionality
    // ===========================

    // Show New Table Section
    if (newTableBtn) {
        newTableBtn.addEventListener('click', function (e) {
            e.preventDefault();
            if (dashboardSection) dashboardSection.classList.add('hidden');
            if (newCandidateSection) newCandidateSection.classList.add('hidden');
            if (manageCandidateSection) manageCandidateSection.classList.add('hidden');
            if (newTableSection) newTableSection.classList.remove('hidden');
            if (manageTableSection) manageTableSection.classList.add('hidden');

            // Close sidebar on mobile
            if (window.innerWidth <= 768 && sidebar) {
                sidebar.classList.remove('active');
                if (container) container.classList.remove('sidebar-active');
                document.body.style.overflow = 'auto';
            }

            showNotification('📁 Ready to upload exoplanet CSV file!', 'info');
        });
    }

    // Show Manage Table Section
    if (manageTableBtn) {
        manageTableBtn.addEventListener('click', function (e) {
            e.preventDefault();
            if (dashboardSection) dashboardSection.classList.add('hidden');
            if (newCandidateSection) newCandidateSection.classList.add('hidden');
            if (manageCandidateSection) manageCandidateSection.classList.add('hidden');
            if (newTableSection) newTableSection.classList.add('hidden');
            if (manageTableSection) manageTableSection.classList.remove('hidden');

            // Close sidebar on mobile
            if (window.innerWidth <= 768 && sidebar) {
                sidebar.classList.remove('active');
                if (container) container.classList.remove('sidebar-active');
                document.body.style.overflow = 'auto';
            }

            // Load and display saved exoplanet data
            loadExoplanetData();

            showNotification('📊 Managing exoplanet data...', 'info');
        });
    }

    // Back to Dashboard from New Table
    if (backToDashboardFromNewTableBtn) {
        backToDashboardFromNewTableBtn.addEventListener('click', function () {
            if (dashboardSection) dashboardSection.classList.remove('hidden');
            if (newTableSection) newTableSection.classList.add('hidden');
            showNotification('📊 Returning to dashboard...', 'info');
        });
    }

    // Back to Dashboard from Manage Table
    if (backToDashboardFromManageTableBtn) {
        backToDashboardFromManageTableBtn.addEventListener('click', function () {
            if (dashboardSection) dashboardSection.classList.remove('hidden');
            if (manageTableSection) manageTableSection.classList.add('hidden');
            showNotification('📊 Returning to dashboard...', 'info');
        });
    }

    // CSV File Upload Handling
    if (csvFileInput) {
        csvFileInput.addEventListener('change', function (e) {
            const file = e.target.files[0];
            if (file) {
                if (file.type !== 'text/csv' && !file.name.toLowerCase().endsWith('.csv')) {
                    showNotification('❌ Please upload a valid CSV file!', 'error');
                    return;
                }

                // Show upload button
                if (uploadBtn) uploadBtn.style.display = 'block';
                if (uploadArea) uploadArea.classList.add('file-selected');

                // Read and preview CSV
                const reader = new FileReader();
                reader.onload = function (e) {
                    const csvData = e.target.result;
                    previewCSVData(csvData);
                };
                reader.readAsText(file);
            }
        });
    }

    // Upload button click
    if (uploadBtn) {
        uploadBtn.addEventListener('click', function () {
            const file = csvFileInput.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    const csvData = e.target.result;
                    previewCSVData(csvData);
                };
                reader.readAsText(file);
            }
        });
    }

    // Cancel upload
    if (cancelUploadBtn) {
        cancelUploadBtn.addEventListener('click', function () {
            resetUploadForm();
        });
    }

    // Confirm upload and save data
    if (confirmUploadBtn) {
        confirmUploadBtn.addEventListener('click', function () {
            saveExoplanetData();
        });
    }

    // Download processed CSV
    if (downloadProcessedCsvBtn) {
        downloadProcessedCsvBtn.addEventListener('click', function () {
            exportExoplanetToCSV();
        });
    }

    // Clear exoplanet data
    if (clearExoplanetDataBtn) {
        clearExoplanetDataBtn.addEventListener('click', function () {
            if (confirm('Are you sure you want to delete ALL exoplanet data? This action cannot be undone.')) {
                localStorage.removeItem('exoplanetData');
                loadExoplanetData();
                showNotification('🗑️ All exoplanet data cleared!', 'warning');
            }
        });
    }

    // Drag and drop functionality
    if (uploadArea) {
        uploadArea.addEventListener('dragover', function (e) {
            e.preventDefault();
            uploadArea.classList.add('drag-over');
        });

        uploadArea.addEventListener('dragleave', function () {
            uploadArea.classList.remove('drag-over');
        });

        uploadArea.addEventListener('drop', function (e) {
            e.preventDefault();
            uploadArea.classList.remove('drag-over');

            const files = e.dataTransfer.files;
            if (files.length > 0) {
                const file = files[0];
                if (file.type === 'text/csv' || file.name.toLowerCase().endsWith('.csv')) {
                    csvFileInput.files = files;

                    // Show upload button
                    if (uploadBtn) uploadBtn.style.display = 'block';
                    uploadArea.classList.add('file-selected');

                    // Read and preview CSV
                    const reader = new FileReader();
                    reader.onload = function (e) {
                        const csvData = e.target.result;
                        previewCSVData(csvData);
                    };
                    reader.readAsText(file);
                } else {
                    showNotification('❌ Please drop a valid CSV file!', 'error');
                }
            }
        });

        // Click to browse
        uploadArea.addEventListener('click', function () {
            csvFileInput.click();
        });
    }

    // Preview CSV data
    function previewCSVData(csvData) {
        try {
            const rows = csvData.split('\n').filter(row => row.trim() !== '');
            if (rows.length === 0) {
                showNotification('❌ CSV file is empty!', 'error');
                return;
            }

            const headers = rows[0].split(',').map(header => header.trim());
            const previewData = rows.slice(1, 6).map(row => {
                const values = row.split(',').map(value => value.trim());
                return headers.reduce((obj, header, index) => {
                    obj[header] = values[index] || '';
                    return obj;
                }, {});
            });

            // Create preview table
            let previewHTML = `
                <div class="preview-info">
                    <p><strong>File Preview:</strong> Showing first 5 rows</p>
                    <p><strong>Columns detected:</strong> ${headers.length}</p>
                </div>
                <table class="preview-table">
                    <thead>
                        <tr>
                            ${headers.map(header => `<th>${header}</th>`).join('')}
                            <th>Resultado</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            previewData.forEach(row => {
                previewHTML += '<tr>';
                headers.forEach(header => {
                    previewHTML += `<td>${row[header] || ''}</td>`;
                });
                previewHTML += '<td><em>Pending</em></td>';
                previewHTML += '</tr>';
            });

            previewHTML += '</tbody></table>';

            if (previewTableContainer) {
                previewTableContainer.innerHTML = previewHTML;
            }
            if (uploadPreview) uploadPreview.style.display = 'block';
            if (uploadArea) uploadArea.style.display = 'none';

        } catch (error) {
            console.error('Error parsing CSV:', error);
            showNotification('❌ Error parsing CSV file!', 'error');
        }
    }

    // Reset upload form
    function resetUploadForm() {
        if (csvFileInput) csvFileInput.value = '';
        if (uploadBtn) uploadBtn.style.display = 'none';
        if (uploadPreview) uploadPreview.style.display = 'none';
        if (uploadArea) {
            uploadArea.style.display = 'block';
            uploadArea.classList.remove('file-selected', 'drag-over');
        }
    }

    // Save exoplanet data to localStorage
    function saveExoplanetData() {
        try {
            const file = csvFileInput.files[0];
            const reader = new FileReader();

            reader.onload = function (e) {
                const csvData = e.target.result;
                const rows = csvData.split('\n').filter(row => row.trim() !== '');
                const headers = rows[0].split(',').map(header => header.trim());

                const exoplanetData = rows.slice(1).map((row, index) => {
                    const values = row.split(',').map(value => value.trim());
                    const rowData = headers.reduce((obj, header, i) => {
                        obj[header] = values[i] || '';
                        return obj;
                    }, {});

                    // Add resultado column
                    rowData['Resultado'] = 'Pending Analysis';
                    rowData.id = index + 1;

                    return rowData;
                });

                // Save to localStorage
                localStorage.setItem('exoplanetData', JSON.stringify({
                    headers: [...headers, 'Resultado'],
                    data: exoplanetData,
                    timestamp: new Date().toISOString(),
                    fileName: file.name
                }));

                showNotification('✅ Exoplanet data uploaded successfully!', 'success');
                resetUploadForm();

                // Switch to manage table section
                if (dashboardSection) dashboardSection.classList.add('hidden');
                if (newTableSection) newTableSection.classList.add('hidden');
                if (manageTableSection) manageTableSection.classList.remove('hidden');

                loadExoplanetData();
            };

            reader.readAsText(file);
        } catch (error) {
            console.error('Error saving exoplanet data:', error);
            showNotification('❌ Error saving exoplanet data!', 'error');
        }
    }

    // Load exoplanet data from localStorage
    function loadExoplanetData() {
        try {
            const savedData = JSON.parse(localStorage.getItem('exoplanetData'));

            if (!savedData || !savedData.data || savedData.data.length === 0) {
                displayEmptyExoplanetState();
                return;
            }

            displayExoplanetData(savedData);
            updateExoplanetRecordCount(savedData.data.length);

        } catch (error) {
            console.error('Error loading exoplanet data:', error);
            displayEmptyExoplanetState();
        }
    }

    // Display exoplanet data in table
    function displayExoplanetData(savedData) {
        if (!exoplanetTableBody || !exoplanetTableHead) return;

        const { headers, data } = savedData;

        // Create table header
        exoplanetTableHead.innerHTML = `
            <tr>
                ${headers.map(header =>
            `<th class="excel-header">${header}</th>`
        ).join('')}
            </tr>
        `;

        // Create table body
        exoplanetTableBody.innerHTML = '';

        data.forEach((row, index) => {
            const tr = document.createElement('tr');
            if (index === 0) tr.classList.add('new-row');

            tr.innerHTML = headers.map(header =>
                `<td>${row[header] || ''}</td>`
            ).join('');

            exoplanetTableBody.appendChild(tr);
        });
    }

    // Display empty state for exoplanet data
    function displayEmptyExoplanetState() {
        if (exoplanetTableBody && exoplanetTableHead) {
            exoplanetTableHead.innerHTML = `
                <tr>
                    <th class="excel-header" colspan="10" style="text-align: center; background: rgba(64, 156, 255, 0.1);">
                        Upload a CSV file to see data
                    </th>
                </tr>
            `;

            exoplanetTableBody.innerHTML = `
                <tr>
                    <td colspan="10" class="empty-state">
                        <div class="empty-icon">📊</div>
                        <p>No exoplanet data available</p>
                        <p style="font-size: 0.9rem; margin-top: 10px;">Go to "New Table" to upload a CSV file</p>
                    </td>
                </tr>
            `;
        }
        updateExoplanetRecordCount(0);
    }

    // Update exoplanet record count
    function updateExoplanetRecordCount(count) {
        if (exoplanetRecordCount) {
            exoplanetRecordCount.textContent = count;
            exoplanetRecordCount.style.background = count > 0 ?
                'rgba(34, 197, 94, 0.3)' : 'rgba(64, 156, 255, 0.3)';
            exoplanetRecordCount.style.color = count > 0 ? '#22c55e' : '#409cff';
        }
    }

    // Export exoplanet data to CSV
    function exportExoplanetToCSV() {
        const savedData = JSON.parse(localStorage.getItem('exoplanetData'));

        if (!savedData || !savedData.data || savedData.data.length === 0) {
            showNotification('📭 No exoplanet data to export!', 'warning');
            return;
        }

        const { headers, data } = savedData;

        // Create CSV content
        let csvContent = headers.join(',') + '\n';

        data.forEach(row => {
            const rowData = headers.map(header => row[header] || '');
            csvContent += rowData.join(',') + '\n';
        });

        // Create and download file
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);

        link.setAttribute('href', url);
        link.setAttribute('download', `exoplanet_data_${new Date().toISOString().split('T')[0]}.csv`);
        link.style.visibility = 'hidden';

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        showNotification('📥 Exoplanet data exported successfully!', 'success');
    }

    // Add keyboard shortcut for toggling sidebar (Ctrl + B)
    document.addEventListener('keydown', function (e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'b') {
            e.preventDefault();
            if (toggleBtn) {
                toggleBtn.click();

                // Add visual feedback
                toggleBtn.style.background = 'rgba(64, 156, 255, 0.9)';
                setTimeout(() => {
                    toggleBtn.style.background = '';
                }, 500);
            }
        }
    });

    // Add spin animation for loading
    const style = document.createElement('style');
    style.textContent = `
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(style);

    // Force toggle button to be always visible
    setInterval(ensureToggleVisibility, 1000);

    // Add welcome message in console
    console.log(`
    🚀 EXO(0)PLORER - Space Management System Activated!
    ⭐ Welcome to the interstellar candidate management system!
    📏 Everything is optimized for maximum visibility!
    🎮 Controls: 
       - Ctrl+B to toggle sidebar 
       - Click cards for fun effects!
       - Hover menu items for tooltips!
    🎉 Enjoy the space exploration!
    `);

    // Initial notification
    setTimeout(() => {
        showNotification('🚀 EXO(0)PLORER System Ready!', 'success');
    }, 1000);
});

// ===========================
// Notification & Particles Systems
// ===========================

// Notification system
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }

    const notification = document.createElement('div');
    const colors = {
        info: '#409cff',
        success: '#4ade80',
        warning: '#f59e0b',
        error: '#ef4444'
    };

    notification.className = 'notification';
    notification.style.cssText = `
        position: fixed;
        top: 30px;
        right: 30px;
        background: ${colors[type]};
        color: white;
        padding: 20px 25px;
        border-radius: 12px;
        font-size: 1.1rem;
        font-weight: bold;
        z-index: 10000;
        box-shadow: 0 8px 25px rgba(0,0,0,0.4);
        transform: translateX(400px);
        transition: transform 0.4s ease;
        max-width: 400px;
        text-align: center;
        backdrop-filter: blur(10px);
    `;

    notification.textContent = message;
    document.body.appendChild(notification);

    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);

    // Remove after 4 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 400);
    }, 4000);
}

// Particle effect function
function createParticles() {
    const toggleBtn = document.getElementById('toggleBtn');
    if (!toggleBtn) return;

    const particles = document.createElement('div');
    particles.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 10000;
    `;
    document.body.appendChild(particles);

    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.style.cssText = `
            position: absolute;
            width: 15px;
            height: 15px;
            background: radial-gradient(circle, #409cff, #7e57c2);
            border-radius: 50%;
            pointer-events: none;
            left: ${toggleBtn.getBoundingClientRect().left + 40}px;
            top: ${toggleBtn.getBoundingClientRect().top + 40}px;
            animation: particleMove 1s ease-out forwards;
        `;

        const angle = Math.random() * Math.PI * 2;
        const distance = 100 + Math.random() * 150;
        const size = 10 + Math.random() * 20;

        particle.style.setProperty('--angle', angle);
        particle.style.setProperty('--distance', distance);
        particle.style.setProperty('--size', size);

        particles.appendChild(particle);
    }

    // Add particle animation
    const particleStyle = document.createElement('style');
    particleStyle.textContent = `
        @keyframes particleMove {
            0% {
                transform: translate(0, 0) scale(1);
                opacity: 1;
            }
            100% {
                transform: translate(
                    calc(cos(var(--angle)) * var(--distance) * 1px),
                    calc(sin(var(--angle)) * var(--distance) * 1px)
                ) scale(0);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(particleStyle);

    setTimeout(() => {
        particles.remove();
        particleStyle.remove();
    }, 1000);
}

if (statisticsBtn) {
    statisticsBtn.addEventListener('click', function (e) {
        e.preventDefault();
        showSection(statisticsSection);
        loadStatisticsImages();
        showNotification('📈 Loading statistics images...', 'info');
    });
}

// Show Documentation Section
if (documentationBtn) {
    documentationBtn.addEventListener('click', function (e) {
        e.preventDefault();
        showSection(documentationSection);
        loadDocumentationCSVs();
        showNotification('📚 Loading documentation files...', 'info');
    });
}

// Back to Dashboard from Statistics
if (backToDashboardFromStatisticsBtn) {
    backToDashboardFromStatisticsBtn.addEventListener('click', function () {
        showSection(dashboardSection);
    });
}

// Back to Dashboard from Documentation
if (backToDashboardFromDocumentationBtn) {
    backToDashboardFromDocumentationBtn.addEventListener('click', function () {
        showSection(dashboardSection);
    });
}

// Función auxiliar para mostrar secciones
function showSection(sectionToShow) {
    // Ocultar todas las secciones
    const sections = [
        dashboardSection, 
        newCandidateSection, 
        manageCandidateSection, 
        newTableSection, 
        manageTableSection, 
        statisticsSection, 
        documentationSection
    ];
    
    sections.forEach(section => {
        if (section) section.classList.add('hidden');
    });
    
    // Mostrar la sección deseada
    if (sectionToShow) sectionToShow.classList.remove('hidden');
    
    // Close sidebar on mobile
    if (window.innerWidth <= 768 && sidebar) {
        sidebar.classList.remove('active');
        if (container) container.classList.remove('sidebar-active');
        document.body.style.overflow = 'auto';
    }
}

// Load Statistics Images
function loadStatisticsImages() {
    if (!imagesContainer) return;
    
    imagesContainer.innerHTML = `
        <div class="loading-state">
            <div class="loading-icon">🔄</div>
            <p>Loading statistics images from appnasa/utils/estadisticas/</p>
        </div>
    `;
    
    // Simulamos la carga de imágenes (en un caso real, harías una petición al servidor)
    setTimeout(() => {
        // Lista de imágenes de ejemplo - en tu caso real, obtendrías esta lista del servidor
        const imageFiles = [
            'statistics_chart_1.png',
            'data_analysis_2.jpg',
            'performance_graph.png',
            'usage_statistics.jpg'
        ];
        
        if (imageFiles.length === 0) {
            imagesContainer.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">🖼️</div>
                    <p>No statistics images found</p>
                    <p style="font-size: 0.9rem; margin-top: 10px;">Place your images in appnasa/utils/estadisticas/</p>
                </div>
            `;
            return;
        }
        
        let imagesHTML = '<div class="images-grid">';
        
        imageFiles.forEach((imageFile, index) => {
            imagesHTML += `
                <div class="image-card">
                    <div class="image-wrapper">
                        <img src="appnasa/utils/estadisticas/${imageFile}" 
                             alt="${imageFile}" 
                             onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjE1MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjMWEyYjM2Ii8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzY0OWNmZiIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPkltYWdlIE5vdCBGb3VuZDwvdGV4dD48L3N2Zz4='">
                        <div class="image-overlay">
                            <button class="btn btn-small view-image-btn" data-image="appnasa/utils/estadisticas/${imageFile}">View</button>
                        </div>
                    </div>
                    <div class="image-info">
                        <h4>${imageFile}</h4>
                        <p>Statistical chart #${index + 1}</p>
                    </div>
                </div>
            `;
        });
        
        imagesHTML += '</div>';
        imagesContainer.innerHTML = imagesHTML;
        
        // Add event listeners for view buttons
        document.querySelectorAll('.view-image-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const imageUrl = this.getAttribute('data-image');
                viewImageModal(imageUrl);
            });
        });
        
    }, 1500);
}

// Load Documentation CSVs
function loadDocumentationCSVs() {
    if (!csvFilesContainer) return;
    
    csvFilesContainer.innerHTML = `
        <div class="loading-state">
            <div class="loading-icon">🔄</div>
            <p>Loading documentation files from appnasa/utils/documentation/</p>
        </div>
    `;
    
    // Simulamos la carga de archivos CSV (en un caso real, harías una petición al servidor)
    setTimeout(() => {
        // Lista de archivos CSV de ejemplo - en tu caso real, obtendrías esta lista del servidor
        const csvFiles = [
            { name: 'user_guide.csv', description: 'Complete user guide and documentation' },
            { name: 'api_reference.csv', description: 'API endpoints and parameters' },
            { name: 'data_format.csv', description: 'Data format specifications' },
            { name: 'troubleshooting.csv', description: 'Common issues and solutions' }
        ];
        
        if (csvFiles.length === 0) {
            csvFilesContainer.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">📄</div>
                    <p>No documentation files found</p>
                    <p style="font-size: 0.9rem; margin-top: 10px;">Place your CSV files in appnasa/utils/documentation/</p>
                </div>
            `;
            return;
        }
        
        let csvsHTML = '<div class="csv-files-grid">';
        
        csvFiles.forEach((csvFile, index) => {
            csvsHTML += `
                <div class="csv-file-card">
                    <div class="csv-file-header">
                        <div class="csv-icon">📊</div>
                        <h4>${csvFile.name}</h4>
                    </div>
                    <div class="csv-file-body">
                        <p>${csvFile.description}</p>
                        <div class="csv-file-actions">
                            <button class="btn btn-small view-csv-btn" data-file="appnasa/utils/documentation/${csvFile.name}">View Content</button>
                            <button class="btn btn-small download-csv-btn" data-file="appnasa/utils/documentation/${csvFile.name}">Download</button>
                        </div>
                    </div>
                </div>
            `;
        });
        
        csvsHTML += '</div>';
        csvFilesContainer.innerHTML = csvsHTML;
        
        // Add event listeners for CSV buttons
        document.querySelectorAll('.view-csv-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const fileUrl = this.getAttribute('data-file');
                viewCSVContent(fileUrl);
            });
        });
        
        document.querySelectorAll('.download-csv-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const fileUrl = this.getAttribute('data-file');
                downloadCSVFile(fileUrl);
            });
        });
        
    }, 1500);
}

// View Image in Modal
function viewImageModal(imageUrl) {
    // Create modal
    const modal = document.createElement('div');
    modal.className = 'image-modal';
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.9);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 10000;
        backdrop-filter: blur(10px);
    `;
    
    modal.innerHTML = `
        <div class="modal-content" style="max-width: 90%; max-height: 90%; position: relative;">
            <img src="${imageUrl}" alt="Statistics Image" style="max-width: 100%; max-height: 100%; border-radius: 10px;">
            <button class="close-modal-btn" style="position: absolute; top: 10px; right: 10px; background: #ef4444; color: white; border: none; border-radius: 50%; width: 40px; height: 40px; font-size: 1.5rem; cursor: pointer;">×</button>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Close modal functionality
    const closeBtn = modal.querySelector('.close-modal-btn');
    closeBtn.addEventListener('click', () => {
        document.body.removeChild(modal);
    });
    
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            document.body.removeChild(modal);
        }
    });
}

// View CSV Content
function viewCSVContent(fileUrl) {
    // Simulamos la carga del contenido CSV
    showNotification('📖 Loading CSV content...', 'info');
    
    // En un caso real, harías fetch(fileUrl) para obtener el contenido
    setTimeout(() => {
        // Contenido de ejemplo
        const csvContent = `Name,Description,Version,Last Updated
User Guide,Complete system documentation,2.1,2024-01-15
API Reference,All API endpoints and parameters,1.4,2024-01-10
Data Format,Input/output specifications,3.2,2024-01-08
Troubleshooting,Common issues and solutions,1.1,2024-01-05`;
        
        const modal = document.createElement('div');
        modal.className = 'csv-modal';
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 10000;
            backdrop-filter: blur(10px);
        `;
        
        const rows = csvContent.split('\n');
        let tableHTML = '<table class="csv-preview-table"><thead>';
        
        // Header
        const headers = rows[0].split(',');
        tableHTML += '<tr>';
        headers.forEach(header => {
            tableHTML += `<th>${header}</th>`;
        });
        tableHTML += '</tr></thead><tbody>';
        
        // Rows
        for (let i = 1; i < rows.length; i++) {
            if (rows[i].trim()) {
                const cells = rows[i].split(',');
                tableHTML += '<tr>';
                cells.forEach(cell => {
                    tableHTML += `<td>${cell}</td>`;
                });
                tableHTML += '</tr>';
            }
        }
        
        tableHTML += '</tbody></table>';
        
        modal.innerHTML = `
            <div class="modal-content" style="background: #0d111c; padding: 30px; border-radius: 15px; max-width: 80%; max-height: 80%; overflow: auto; position: relative;">
                <h3 style="color: #409cff; margin-bottom: 20px;">CSV Content Preview</h3>
                ${tableHTML}
                <button class="close-modal-btn" style="position: absolute; top: 15px; right: 15px; background: #ef4444; color: white; border: none; border-radius: 50%; width: 40px; height: 40px; font-size: 1.5rem; cursor: pointer;">×</button>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Close modal functionality
        const closeBtn = modal.querySelector('.close-modal-btn');
        closeBtn.addEventListener('click', () => {
            document.body.removeChild(modal);
        });
        
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                document.body.removeChild(modal);
            }
        });
        
    }, 1000);
}

// Download CSV File
function downloadCSVFile(fileUrl) {
    showNotification('📥 Downloading CSV file...', 'info');
    
    // En un caso real, crearías un enlace de descarga
    setTimeout(() => {
        showNotification('✅ File download started!', 'success');
    }, 500);
}