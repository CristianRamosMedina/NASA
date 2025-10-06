// Toggle sidebar y tabla New Candidate
document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('toggleBtn');
    const mainContent = document.getElementById('mainContent');
    const container = document.querySelector('.container');

    // ===========================
    // Toggle sidebar
    // ===========================
    function ensureToggleVisibility() {
        toggleBtn.style.display = 'flex';
        toggleBtn.style.visibility = 'visible';
        toggleBtn.style.opacity = '1';
        toggleBtn.style.zIndex = '1001';
    }

    function initSidebar() {
        ensureToggleVisibility();
        if (window.innerWidth <= 768) {
            sidebar.classList.add('collapsed');
            toggleBtn.textContent = '☰';
            toggleBtn.style.fontSize = '3rem';
        } else {
            sidebar.classList.remove('collapsed');
            toggleBtn.textContent = '✕';
            toggleBtn.style.fontSize = '4rem';
        }
    }

    toggleBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        sidebar.classList.toggle('collapsed');
        if (sidebar.classList.contains('collapsed')) {
            toggleBtn.textContent = '☰';
            toggleBtn.style.fontSize = '3rem';
            createParticles();
            showNotification('Menu collapsed!', 'info');
        } else {
            toggleBtn.textContent = '✕';
            toggleBtn.style.fontSize = '4rem';
            showNotification('Menu expanded!', 'success');
        }
        setTimeout(() => ensureToggleVisibility(), 500);
    });

    window.addEventListener('resize', initSidebar);
    initSidebar();
    ensureToggleVisibility();

    // ===========================
    // Cards hover & click
    // ===========================
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-20px) scale(1.08)';
            card.style.zIndex = '100';
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0) scale(1)';
            card.style.zIndex = '1';
        });
        card.addEventListener('click', () => {
            card.style.transform = 'scale(0.95)';
            setTimeout(() => card.style.transform = 'translateY(-20px) scale(1.08)', 200);
        });
    });

    // ===========================
    // Activity animation
    // ===========================
    const activityItems = document.querySelectorAll('.activity-item');
    activityItems.forEach((item, index) => {
        item.style.animationDelay = `${index * 0.3}s`;
        item.classList.add('fade-in');
    });

    // ===========================
    // New Candidate Table
    // ===========================
    const newCandidateContainer = document.getElementById('newCandidateContainer');
    const tableHeader = document.getElementById('tableHeader');
    const tableBody = document.getElementById('tableBody');
    const addRowBtn = document.getElementById('addRowBtn');

    const columns = [
        "koi_score","koi_fwm_stat_sig","koi_srho_err2","koi_dor_err2","koi_dor_err1",
        "koi_incl","koi_prad_err1","koi_count","koi_dor","koi_dikco_mdec_err",
        "koi_period_err1","koi_period_err2","koi_dikco_mra_err","koi_prad_err2,continuous",
        "koi_dikco_msky_err","koi_max_sngle_ev","koi_prad,continuous","koi_dicco_mdec_err",
        "koi_model_snr","koi_dicco_mra_err"
    ];

    columns.forEach(col => {
        const th = document.createElement('th');
        th.textContent = col;
        tableHeader.appendChild(th);
    });

    function addRow() {
        const tr = document.createElement('tr');
        columns.forEach(() => {
            const td = document.createElement('td');
            const input = document.createElement('input');
            input.type = 'text';
            input.style.width = '100%';
            td.appendChild(input);
            tr.appendChild(td);
        });
        tableBody.appendChild(tr);
    }

    addRowBtn.addEventListener('click', addRow);
    addRow(); // Fila inicial

    const newCandidateMenu = document.querySelector('a[data-tooltip="New Candidate"]');
    newCandidateMenu.addEventListener('click', function(e) {
        e.preventDefault();
        document.querySelector('.content-grid').style.display = 'none';
        document.querySelector('.recent-activity').style.display = 'none';
        newCandidateContainer.style.display = 'block';
    });

    // ===========================
    // Notification & particles
    // ===========================
    function showNotification(message, type='info') {
        const notification = document.createElement('div');
        const colors = { info:'#409cff', success:'#4ade80', warning:'#f59e0b', error:'#ef4444' };
        notification.style.cssText = `
            position: fixed; top: 30px; right: 30px;
            background: ${colors[type]}; color: white;
            padding: 25px 35px; border-radius: 15px;
            font-size: 1.4rem; font-weight: bold;
            z-index: 10000; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            transform: translateX(400px); transition: transform 0.5s ease;
            max-width: 400px; text-align: center;
        `;
        notification.textContent = message;
        document.body.appendChild(notification);
        setTimeout(() => notification.style.transform = 'translateX(0)', 100);
        setTimeout(() => {
            notification.style.transform = 'translateX(400px)';
            setTimeout(() => notification.remove(), 500);
        }, 3000);
    }

    function createParticles() {
        const particles = document.createElement('div');
        particles.style.cssText = 'position: fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:10000;';
        document.body.appendChild(particles);
        for (let i=0;i<25;i++){
            const particle = document.createElement('div');
            particle.style.cssText = `
                position:absolute;width:20px;height:20px;
                background: radial-gradient(circle, #409cff,#7e57c2,#ff6b6b,#4ade80);
                border-radius:50%; pointer-events:none;
                left:${toggleBtn.getBoundingClientRect().left+50}px;
                top:${toggleBtn.getBoundingClientRect().top+50}px;
                animation: particleMove 1.5s ease-out forwards;
            `;
            const angle=Math.random()*Math.PI*2;
            const distance=150+Math.random()*200;
            particle.style.setProperty('--angle', angle);
            particle.style.setProperty('--distance', distance);
            particles.appendChild(particle);
        }
        const particleStyle = document.createElement('style');
        particleStyle.textContent = `
            @keyframes particleMove {
                0%{transform:translate(0,0) scale(1); opacity:1;}
                100%{transform:translate(
                    calc(cos(var(--angle))*var(--distance)*1px),
                    calc(sin(var(--angle))*var(--distance)*1px)
                ) scale(0); opacity:0;}
            }
        `;
        document.head.appendChild(particleStyle);
        setTimeout(() => {particles.remove(); particleStyle.remove();},1500);
    }
});


// New Candidate Form Functionality
document.addEventListener('DOMContentLoaded', function() {
    const newCandidateBtn = document.getElementById('newCandidateBtn');
    const backToDashboardBtn = document.getElementById('backToDashboard');
    const dashboardSection = document.getElementById('dashboardSection');
    const newCandidateSection = document.getElementById('newCandidateSection');
    const candidateForm = document.getElementById('candidateForm');

    // Show New Candidate Form
    if (newCandidateBtn) {
        newCandidateBtn.addEventListener('click', function(e) {
            e.preventDefault();
            dashboardSection.classList.add('hidden');
            newCandidateSection.classList.remove('hidden');
            
            // Close sidebar on mobile
            if (window.innerWidth <= 768) {
                sidebar.classList.remove('active');
                container.classList.remove('sidebar-active');
                document.body.style.overflow = 'auto';
            }
            
            showNotification('🚀 New Candidate form opened!', 'info');
        });
    }

    // Back to Dashboard
    if (backToDashboardBtn) {
        backToDashboardBtn.addEventListener('click', function() {
            dashboardSection.classList.remove('hidden');
            newCandidateSection.classList.add('hidden');
            showNotification('📊 Returning to dashboard...', 'info');
        });
    }

    // Form Submission
    if (candidateForm) {
        candidateForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Collect form data
            const formData = new FormData(candidateForm);
            const candidateData = {};
            
            for (let [key, value] of formData.entries()) {
                candidateData[key] = value;
            }
            
            // Simulate saving data
            console.log('Candidate data:', candidateData);
            
            // Show success message
            showNotification('✅ Candidate data saved successfully!', 'success');
            
            // Reset form and return to dashboard
            setTimeout(() => {
                candidateForm.reset();
                dashboardSection.classList.remove('hidden');
                newCandidateSection.classList.add('hidden');
            }, 2000);
        });
    }

    // Add input validation
    const numberInputs = document.querySelectorAll('input[type="text"]');
    numberInputs.forEach(input => {
        input.addEventListener('blur', function() {
            const value = this.value.trim();
            if (value && !isNaN(value) && value !== '') {
                this.style.borderColor = '#4ade80';
                this.style.boxShadow = '0 0 10px rgba(74, 222, 128, 0.3)';
            } else if (value !== '') {
                this.style.borderColor = '#ef4444';
                this.style.boxShadow = '0 0 10px rgba(239, 68, 68, 0.3)';
            } else {
                this.style.borderColor = 'rgba(64, 156, 255, 0.3)';
                this.style.boxShadow = 'none';
            }
        });
    });
});

// Notification system (if not already present)
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