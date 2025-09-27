// BookVana JavaScript Functions
document.addEventListener('DOMContentLoaded', function() {
    // Initialize mobile navigation
    initMobileNav();
    
    // Initialize sound settings
    initSoundSettings();
    
    // Add click sound to all buttons and links
    addClickSounds();
    
    // Initialize tooltips and animations
    initAnimations();
    
    console.log('🌿 BookVana Library System Loaded! 📚');
});

// Mobile Navigation
function initMobileNav() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
        
        // Close mobile menu when clicking on a link
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', function() {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            });
        });
    }
}

// Sound Management
let soundEnabled = true;

function initSoundSettings() {
    const savedSound = localStorage.getItem('soundEnabled');
    soundEnabled = savedSound === null ? true : savedSound === 'true';
    
    // Create sound elements if they don't exist
    createSoundElements();
}

function createSoundElements() {
    if (!document.getElementById('clickSound')) {
        const clickSound = document.createElement('audio');
        clickSound.id = 'clickSound';
        clickSound.preload = 'auto';
        clickSound.innerHTML = `
            <source src="data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmceBy2Gyff=" type="audio/wav">
        `;
        document.body.appendChild(clickSound);
    }
    
    if (!document.getElementById('successSound')) {
        const successSound = document.createElement('audio');
        successSound.id = 'successSound';
        successSound.preload = 'auto';
        successSound.innerHTML = `
            <source src="data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmceBy2Gyff=" type="audio/wav">
        `;
        document.body.appendChild(successSound);
    }
    
    if (!document.getElementById('errorSound')) {
        const errorSound = document.createElement('audio');
        errorSound.id = 'errorSound';
        errorSound.preload = 'auto';
        errorSound.innerHTML = `
            <source src="data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmceBy2Gyff=" type="audio/wav">
        `;
        document.body.appendChild(errorSound);
    }
}

function playSound(type) {
    if (!soundEnabled) return;
    
    const sound = document.getElementById(type + 'Sound');
    if (sound) {
        sound.currentTime = 0;
        sound.play().catch(e => console.log('Sound play failed:', e));
    }
}

// Add click sounds to interactive elements
function addClickSounds() {
    // Add to buttons
    document.querySelectorAll('button, .btn-primary, .btn-secondary, .btn-danger').forEach(button => {
        button.addEventListener('click', () => playSound('click'));
    });
    
    // Add to navigation links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => playSound('click'));
    });
    
    // Add to action cards
    document.querySelectorAll('.action-card, .stat-card').forEach(card => {
        card.addEventListener('click', () => playSound('click'));
    });
}

// Navigation with sound
function navigateWithSound(url) {
    playSound('click');
    setTimeout(() => {
        window.location.href = url;
    }, 100);
}

// Modal Management
function closeModal(modalId) {
    playSound('click');
    document.getElementById(modalId).style.display = 'none';
}

// Close modals when clicking outside
window.addEventListener('click', function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
});

// Notification System
function showNotification(message, type = 'info', duration = 5000) {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notif => notif.remove());
    
    // Create new notification
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    // Add icon based on type
    const icons = {
        success: '✅',
        error: '❌',
        info: 'ℹ️',
        warning: '⚠️'
    };
    
    notification.innerHTML = `${icons[type] || icons.info} ${message}`;
    
    document.body.appendChild(notification);
    
    // Auto remove
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.animation = 'slideOutRight 0.5s ease';
            setTimeout(() => notification.remove(), 500);
        }
    }, duration);
    
    // Click to dismiss
    notification.addEventListener('click', () => {
        notification.style.animation = 'slideOutRight 0.5s ease';
        setTimeout(() => notification.remove(), 500);
    });
}

// Form Validation
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhone(phone) {
    const re = /^[0-9]{10}$/;
    return re.test(phone.replace(/\D/g, ''));
}

function validateISBN(isbn) {
    const cleanISBN = isbn.replace(/[\s-]/g, '');
    return cleanISBN.length === 10 || cleanISBN.length === 13;
}

// Data Loading and Management
async function loadData(endpoint) {
    try {
        const response = await fetch(endpoint);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Error loading data from ${endpoint}:`, error);
        showNotification('Error loading data. Please try again.', 'error');
        return [];
    }
}

async function saveData(endpoint, data, method = 'POST') {
    try {
        const response = await fetch(endpoint, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error(`Error saving data to ${endpoint}:`, error);
        showNotification('Error saving data. Please try again.', 'error');
        return { success: false, message: 'Network error' };
    }
}

// Search and Filter Functions
function initSearch(tableId, searchInputId) {
    const searchInput = document.getElementById(searchInputId);
    const table = document.getElementById(tableId);
    
    if (!searchInput || !table) return;
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');
        
        Array.from(rows).forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchTerm) ? '' : 'none';
        });
        
        // Add search animation
        table.style.opacity = '0.7';
        setTimeout(() => {
            table.style.opacity = '1';
        }, 150);
    });
}

function initFilter(selectId, tableId, columnIndex) {
    const filterSelect = document.getElementById(selectId);
    const table = document.getElementById(tableId);
    
    if (!filterSelect || !table) return;
    
    filterSelect.addEventListener('change', function() {
        const filterValue = this.value.toLowerCase();
        const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');
        
        Array.from(rows).forEach(row => {
            const cell = row.getElementsByTagName('td')[columnIndex];
            if (!cell) return;
            
            const cellText = cell.textContent.toLowerCase();
            row.style.display = !filterValue || cellText.includes(filterValue) ? '' : 'none';
        });
        
        playSound('click');
    });
}

// Animation and Visual Effects
function initAnimations() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe elements for scroll animations
    document.querySelectorAll('.action-card, .stat-card, .activity-item').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
    
    // Add hover effects to interactive elements
    addHoverEffects();
}

function addHoverEffects() {
    // Enhanced hover effects for cards
    document.querySelectorAll('.action-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-15px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Ripple effect for buttons
    document.querySelectorAll('.btn-primary, .btn-secondary, .btn-danger').forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255, 255, 255, 0.6)';
            ripple.style.transform = 'scale(0)';
            ripple.style.animation = 'ripple 0.6s linear';
            ripple.style.left = e.offsetX - 10 + 'px';
            ripple.style.top = e.offsetY - 10 + 'px';
            ripple.style.width = '20px';
            ripple.style.height = '20px';
            
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

// Utility Functions
function formatCurrency(amount) {
    return `₹${parseFloat(amount).toFixed(2)}`;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN');
}

function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('en-IN');
}

function generateTransactionId() {
    return 'TXN' + Date.now() + Math.random().toString(36).substr(2, 5).toUpperCase();
}

// Export/Import Functions
function exportToCSV(data, filename) {
    const csvContent = convertToCSV(data);
    downloadFile(csvContent, filename + '.csv', 'text/csv');
    playSound('success');
    showNotification('Data exported successfully!', 'success');
}

function convertToCSV(data) {
    if (!data.length) return '';
    
    const headers = Object.keys(data[0]);
    const csvHeaders = headers.join(',');
    
    const csvRows = data.map(row => {
        return headers.map(header => {
            const value = row[header];
            return `"${value}"`;
        }).join(',');
    });
    
    return csvHeaders + '\n' + csvRows.join('\n');
}

function downloadFile(content, filename, contentType) {
    const blob = new Blob([content], { type: contentType });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
}

// Print Functions
function printTable(tableId) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <html>
        <head>
            <title>BookVana - Library Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #2d5016; text-align: center; margin-bottom: 30px; }
                table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
                th { background-color: #4a7c59; color: white; }
                tr:nth-child(even) { background-color: #f9f9f9; }
                .footer { margin-top: 40px; text-align: center; color: #666; }
            </style>
        </head>
        <body>
            <h1>🌿 BookVana Library Report 📚</h1>
            ${table.outerHTML}
            <div class="footer">
                <p>Generated on ${new Date().toLocaleString('en-IN')}</p>
                <p>Made with ❤️ by Saket</p>
            </div>
        </body>
        </html>
    `);
    
    printWindow.document.close();
    printWindow.print();
    
    playSound('success');
    showNotification('Report sent to printer!', 'success');
}

// Error Handling
window.addEventListener('error', function(event) {
    console.error('Global error:', event.error);
    showNotification('An unexpected error occurred. Please refresh the page.', 'error');
});

// CSS Animations (add to existing CSS)
const additionalCSS = `
@keyframes ripple {
    to { transform: scale(4); opacity: 0; }
}

@keyframes slideOutRight {
    to { transform: translateX(100%); opacity: 0; }
}

.loading-spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #4a7c59;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 20px auto;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.fade-in {
    animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.slide-up {
    animation: slideUp 0.5s ease-out;
}

@keyframes slideUp {
    from { transform: translateY(30px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

.pulse {
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}
`;

// Add additional CSS to document
const styleSheet = document.createElement('style');
styleSheet.textContent = additionalCSS;
document.head.appendChild(styleSheet);

// Initialize tooltips
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = element.getAttribute('data-tooltip');
        
        element.addEventListener('mouseenter', function() {
            document.body.appendChild(tooltip);
            const rect = element.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
            tooltip.style.opacity = '1';
        });
        
        element.addEventListener('mouseleave', function() {
            if (tooltip.parentNode) {
                tooltip.parentNode.removeChild(tooltip);
            }
        });
    });
}

// Performance monitoring
function monitorPerformance() {
    if ('performance' in window) {
        window.addEventListener('load', function() {
            setTimeout(function() {
                const perfData = performance.getEntriesByType('navigation')[0];
                console.log(`🌿 BookVana loaded in ${Math.round(perfData.loadEventEnd - perfData.fetchStart)}ms`);
            }, 0);
        });
    }
}

// Initialize performance monitoring
monitorPerformance();

// Service worker registration (for future PWA features)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // Uncomment when service worker is implemented
        // navigator.serviceWorker.register('/sw.js')
        //     .then(registration => console.log('SW registered'))
        //     .catch(error => console.log('SW registration failed'));
    });
}

console.log('🦋 BookVana JavaScript loaded successfully! 🌿');