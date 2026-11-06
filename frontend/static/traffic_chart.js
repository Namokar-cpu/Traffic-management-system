// ============================================
// LIVE TRAFFIC CHART (Chart.js)
// ============================================

let trafficChart;

// Initialize the chart
function initTrafficChart() {
    const ctx = document.getElementById('trafficChart').getContext('2d');
    
    // Set default font color for Chart.js
    Chart.defaults.color = '#ffffff';

    trafficChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['North', 'South', 'East', 'West'],
            datasets: [{
                label: 'Total Vehicles',
                data: [0, 0, 0, 0],
                backgroundColor: [
                    'rgba(0, 245, 255, 0.7)', // North (Cyan)
                    'rgba(255, 0, 255, 0.7)', // South (Magenta)
                    'rgba(0, 255, 136, 0.7)', // East (Green)
                    'rgba(255, 255, 0, 0.7)'  // West (Yellow)
                ],
                borderColor: [
                    '#00f5ff',
                    '#ff00ff',
                    '#00ff88',
                    '#ffff00'
                ],
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(255, 255, 255, 0.1)' },
                    ticks: { precision: 0 } // whole numbers only
                },
                x: {
                    grid: { display: false }
                }
            },
            animation: {
                duration: 500
            },
            plugins: {
                legend: {
                    display: false // Hide legend to save space
                }
            }
        }
    });
}

// Update the chart with new data
function updateTrafficChart(direction, totalVehicles) {
    if (!trafficChart) return;

    const dirMap = { 'north': 0, 'south': 1, 'east': 2, 'west': 3 };
    const index = dirMap[direction.toLowerCase()];
    
    if (index !== undefined) {
        trafficChart.data.datasets[0].data[index] = totalVehicles;
        trafficChart.update();
    }
}

// Initialize on load
window.addEventListener('load', function () {
    if(document.getElementById('trafficChart')) {
        initTrafficChart();
    }
});
