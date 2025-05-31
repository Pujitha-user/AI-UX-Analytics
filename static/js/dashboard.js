// Dashboard JavaScript functionality
let currentData = null;
let charts = {};

// Initialize dashboard
function initializeDashboard(analytics) {
    currentData = analytics;
    setupNavigation();
    setupCharts();
    loadHeatmapData();
    loadScrollData();
    loadSuggestions();
    
    // Set up auto-refresh
    setInterval(refreshData, 30000); // Refresh every 30 seconds
}

// Navigation setup
function setupNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    const sections = document.querySelectorAll('.content-section');
    
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Remove active class from all items
            navItems.forEach(nav => nav.classList.remove('active'));
            sections.forEach(section => section.classList.remove('active'));
            
            // Add active class to clicked item
            item.classList.add('active');
            
            // Show corresponding section
            const sectionId = item.dataset.section + '-section';
            const targetSection = document.getElementById(sectionId);
            if (targetSection) {
                targetSection.classList.add('active');
            }
        });
    });
}

// Setup charts
function setupCharts() {
    // Event distribution chart
    const eventCtx = document.getElementById('eventChart');
    if (eventCtx && currentData && currentData.event_types) {
        const eventData = currentData.event_types;
        const labels = Object.keys(eventData);
        const data = Object.values(eventData);
        
        charts.eventChart = new Chart(eventCtx, {
            type: 'doughnut',
            data: {
                labels: labels.map(label => label.charAt(0).toUpperCase() + label.slice(1)),
                datasets: [{
                    data: data,
                    backgroundColor: [
                        'hsl(220, 100%, 50%)',
                        'hsl(45, 100%, 50%)',
                        'hsl(120, 100%, 35%)',
                        'hsl(35, 100%, 50%)',
                        'hsl(0, 100%, 50%)'
                    ],
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true
                        }
                    }
                }
            }
        });
    }
    
    // Timeline chart (placeholder)
    const timelineCtx = document.getElementById('timelineChart');
    if (timelineCtx) {
        charts.timelineChart = new Chart(timelineCtx, {
            type: 'line',
            data: {
                labels: ['6h ago', '5h ago', '4h ago', '3h ago', '2h ago', '1h ago', 'Now'],
                datasets: [{
                    label: 'Events',
                    data: [0, 0, 0, 0, 0, 0, currentData?.total_events || 0],
                    borderColor: 'hsl(220, 100%, 50%)',
                    backgroundColor: 'hsl(220, 100%, 50%, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
}

// Load heatmap data
async function loadHeatmapData() {
    try {
        const response = await fetch('/api/heatmap-data');
        if (!response.ok) throw new Error('Failed to load heatmap data');
        
        const heatmapData = await response.json();
        renderHeatmap(heatmapData);
        
        // Update stats
        document.getElementById('total-clicks').textContent = heatmapData.total_clicks || 0;
        document.getElementById('click-clusters').textContent = heatmapData.clusters || 0;
        
    } catch (error) {
        console.error('Error loading heatmap data:', error);
        renderEmptyHeatmap();
    }
}

// Render heatmap
function renderHeatmap(data) {
    const canvas = document.getElementById('heatmapCanvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    // Set canvas size
    canvas.width = 800;
    canvas.height = 600;
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw background
    ctx.fillStyle = '#f8f9fa';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    if (!data.points || data.points.length === 0) {
        // Draw empty state
        ctx.fillStyle = '#6b7280';
        ctx.font = '16px -apple-system, BlinkMacSystemFont, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('No click data available', canvas.width / 2, canvas.height / 2);
        return;
    }
    
    // Draw heatmap points
    data.points.forEach(point => {
        const radius = 30;
        const gradient = ctx.createRadialGradient(point.x, point.y, 0, point.x, point.y, radius);
        
        // Color based on intensity
        const alpha = point.intensity;
        if (alpha > 0.7) {
            gradient.addColorStop(0, `rgba(255, 51, 51, ${alpha})`);
            gradient.addColorStop(1, `rgba(255, 51, 51, 0)`);
        } else if (alpha > 0.4) {
            gradient.addColorStop(0, `rgba(255, 187, 0, ${alpha})`);
            gradient.addColorStop(1, `rgba(255, 187, 0, 0)`);
        } else {
            gradient.addColorStop(0, `rgba(0, 102, 255, ${alpha})`);
            gradient.addColorStop(1, `rgba(0, 102, 255, 0)`);
        }
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(point.x, point.y, radius, 0, Math.PI * 2);
        ctx.fill();
    });
}

// Render empty heatmap
function renderEmptyHeatmap() {
    const canvas = document.getElementById('heatmapCanvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    canvas.width = 800;
    canvas.height = 600;
    
    ctx.fillStyle = '#f8f9fa';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = '#6b7280';
    ctx.font = '16px -apple-system, BlinkMacSystemFont, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('No click data available yet', canvas.width / 2, canvas.height / 2);
    ctx.fillText('Start tracking to see heatmap visualization', canvas.width / 2, canvas.height / 2 + 30);
}

// Load scroll data
async function loadScrollData() {
    try {
        const response = await fetch('/api/scroll-data');
        if (!response.ok) throw new Error('Failed to load scroll data');
        
        const scrollData = await response.json();
        renderScrollAnalytics(scrollData);
        
    } catch (error) {
        console.error('Error loading scroll data:', error);
        renderEmptyScrollAnalytics();
    }
}

// Render scroll analytics
function renderScrollAnalytics(data) {
    // Update metrics
    document.getElementById('avg-scroll-depth').textContent = `${data.average_depth}%`;
    document.getElementById('max-scroll-depth').textContent = `${data.max_depth}%`;
    document.getElementById('bounce-rate').textContent = `${data.bounce_rate}%`;
    
    // Render scroll chart
    const scrollCtx = document.getElementById('scrollChart');
    if (scrollCtx && data.depth_distribution) {
        if (charts.scrollChart) {
            charts.scrollChart.destroy();
        }
        
        charts.scrollChart = new Chart(scrollCtx, {
            type: 'bar',
            data: {
                labels: ['0-10%', '10-20%', '20-30%', '30-40%', '40-50%', '50-60%', '60-70%', '70-80%', '80-90%', '90-100%'],
                datasets: [{
                    label: 'Sessions',
                    data: data.depth_distribution,
                    backgroundColor: 'hsl(220, 100%, 50%, 0.7)',
                    borderColor: 'hsl(220, 100%, 50%)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
}

// Render empty scroll analytics
function renderEmptyScrollAnalytics() {
    document.getElementById('avg-scroll-depth').textContent = '0%';
    document.getElementById('max-scroll-depth').textContent = '0%';
    document.getElementById('bounce-rate').textContent = '0%';
    
    const scrollCtx = document.getElementById('scrollChart');
    if (scrollCtx) {
        if (charts.scrollChart) {
            charts.scrollChart.destroy();
        }
        
        charts.scrollChart = new Chart(scrollCtx, {
            type: 'bar',
            data: {
                labels: ['0-10%', '10-20%', '20-30%', '30-40%', '40-50%', '50-60%', '60-70%', '70-80%', '80-90%', '90-100%'],
                datasets: [{
                    label: 'Sessions',
                    data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    backgroundColor: 'hsl(220, 100%, 50%, 0.3)',
                    borderColor: 'hsl(220, 100%, 50%)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
}

// Load AI suggestions
async function loadSuggestions() {
    const container = document.getElementById('suggestions-container');
    if (!container) return;
    
    container.innerHTML = '<div class="loading-suggestions"><i class="fas fa-spinner fa-spin"></i> Analyzing user behavior patterns...</div>';
    
    try {
        const response = await fetch('/api/suggestions');
        if (!response.ok) throw new Error('Failed to load suggestions');
        
        const data = await response.json();
        renderSuggestions(data.suggestions);
        
    } catch (error) {
        console.error('Error loading suggestions:', error);
        container.innerHTML = '<div class="loading-suggestions">No suggestions available yet. Collect more data to get AI-powered insights.</div>';
    }
}

// Render suggestions
function renderSuggestions(suggestions) {
    const container = document.getElementById('suggestions-container');
    if (!container) return;
    
    if (!suggestions || suggestions.length === 0) {
        container.innerHTML = '<div class="loading-suggestions">No specific suggestions available yet. Continue collecting data for more insights.</div>';
        return;
    }
    
    const suggestionsHTML = suggestions.map(suggestion => `
        <div class="suggestion-card ${suggestion.priority}-priority">
            <div class="suggestion-header">
                <h4>${suggestion.title}</h4>
                <span class="priority-badge ${suggestion.priority}">${suggestion.priority}</span>
            </div>
            <p>${suggestion.description}</p>
            <ul class="suggestion-tips">
                ${suggestion.actionable_tips.map(tip => `<li>${tip}</li>`).join('')}
            </ul>
        </div>
    `).join('');
    
    container.innerHTML = suggestionsHTML;
}

// Generate new suggestions
function generateSuggestions() {
    loadSuggestions();
}

// Refresh all data
async function refreshData() {
    const refreshBtn = document.querySelector('.refresh-btn i');
    if (refreshBtn) {
        refreshBtn.classList.add('fa-spin');
    }
    
    try {
        // Reload page data
        window.location.reload();
    } catch (error) {
        console.error('Error refreshing data:', error);
    } finally {
        if (refreshBtn) {
            refreshBtn.classList.remove('fa-spin');
        }
    }
}

// Export data functionality
async function exportData(format) {
    const loadingOverlay = document.getElementById('loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.style.display = 'flex';
    }
    
    try {
        const response = await fetch('/api/export-data');
        if (!response.ok) throw new Error('Failed to export data');
        
        const data = await response.json();
        
        // Create and download file
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `ux-analytics-data-${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
    } catch (error) {
        console.error('Error exporting data:', error);
        alert('Failed to export data. Please try again.');
    } finally {
        if (loadingOverlay) {
            loadingOverlay.style.display = 'none';
        }
    }
}

// Generate report
function generateReport() {
    alert('Report generation feature coming soon!');
}

// Toggle heatmap mode
function toggleHeatmapMode() {
    // This could toggle between different visualization modes
    loadHeatmapData();
}

// Copy to clipboard functionality
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        // Show success feedback
        const button = event.target;
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-check"></i> Copied';
        button.style.background = 'hsl(120, 100%, 35%)';
        
        setTimeout(() => {
            button.innerHTML = originalText;
            button.style.background = '';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy: ', err);
        alert('Failed to copy to clipboard');
    });
}

// Utility functions
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', function() {
    // Any additional initialization that doesn't require server data
    console.log('Dashboard loaded');
});
