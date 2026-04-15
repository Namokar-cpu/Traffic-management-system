// ============================================
// ANIMATE NUMBER CHANGES
// ============================================
function animateNumber(elementId, newValue) {
    const element = document.getElementById(elementId);
    const currentValue = parseInt(element.innerText) || 0;

    if (currentValue !== newValue) {
        element.style.transform = 'scale(1.3)';
        element.style.color = '#00ff00';

        element.innerText = newValue;

        setTimeout(() => {
            element.style.transform = 'scale(1)';
            element.style.color = '';
        }, 300);
    }
}

// ============================================
// UPDATE SIGNAL LIGHTS WITH COUNTDOWN
// ============================================
function updateSignalLight(direction, status, timeRemaining) {
    const signalElement = document.getElementById(`${direction}Signal`);

    signalElement.classList.remove('RED', 'GREEN', 'YELLOW');
    signalElement.classList.add(status);
    
    // Display signal status with countdown
    signalElement.innerText = `${status} (${timeRemaining}s)`;
}

// ============================================
// UPTIME COUNTER
// ============================================
let uptimeSeconds = 0;

function updateUptime() {
    uptimeSeconds++;

    const hours = Math.floor(uptimeSeconds / 3600);
    const minutes = Math.floor((uptimeSeconds % 3600) / 60);
    const seconds = uptimeSeconds % 60;

    const uptimeString =
        String(hours).padStart(2, '0') + ':' +
        String(minutes).padStart(2, '0') + ':' +
        String(seconds).padStart(2, '0');

    document.getElementById('uptime').innerText = uptimeString;
}

// ============================================
// INITIALIZE
// ============================================
window.addEventListener('load', function () {

    // Start uptime
    setInterval(updateUptime, 1000);

    console.log('🚦 Traffic System Started (WebSocket Mode)');
});

// ============================================
// WEBSOCKET CONNECTION
// ============================================
const socket = io();

// Receive real-time traffic data
socket.on('traffic_update', function (data) {

    const direction = data.direction;
    const cars = data.cars;
    const trucks = data.trucks;
    const bikes = data.bikes;
    const signal = data.signal;
    const timeRemaining = data.time_remaining || 0;

    console.log(`${direction}: ${cars} cars, ${trucks} trucks, ${bikes} bikes | Signal: ${signal} (${timeRemaining}s)`);

    // Update vehicle counts with animation
    animateNumber(direction + "Cars", cars);
    animateNumber(direction + "Trucks", trucks);
    animateNumber(direction + "Bikes", bikes);
    
    // Update live graph
    if (typeof updateTrafficChart === 'function') {
        updateTrafficChart(direction, cars + trucks + bikes);
    }
    
    // Update signal lights with countdown
    updateSignalLight(direction, signal, timeRemaining);
    
    // Update active direction
    if (signal === "GREEN") {
        document.getElementById('activeDirection').innerText = direction.toUpperCase();
    }
    
    // Update total vehicles
    const total = document.querySelectorAll('[id$="Cars"]').length;
    let totalCount = 0;
    document.querySelectorAll('[id$="Cars"]').forEach(el => {
        totalCount += parseInt(el.innerText) || 0;
    });
    document.getElementById('totalVehicles').innerText = totalCount;
});

// ============================================
// KEYBOARD SHORTCUT (OPTIONAL)
// ============================================
document.addEventListener('keydown', function (event) {

    if (event.key === 'r' || event.key === 'R') {
        console.log('🔄 WebSocket auto-updating, no manual refresh needed');
    }
});