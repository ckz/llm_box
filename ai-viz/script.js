let chart;
let animationId;
let dataPoints = [];
let labels = [];
let isRunning = false;

// Initialize the chart
function initChart() {
    const ctx = document.getElementById('aiChart').getContext('2d');
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'AI Predictions',
                data: dataPoints,
                borderColor: '#3498db',
                backgroundColor: 'rgba(52, 152, 219, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            animation: {
                duration: 0
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    min: -100
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

// Generate AI prediction based on selected pattern
function generatePrediction(pattern) {
    const time = dataPoints.length;
    let value;
    
    switch(pattern) {
        case 'sine':
            value = 50 * Math.sin(time / 5) + Math.random() * 10;
            break;
        case 'random':
            value = Math.random() * 200 - 100;
            break;
        case 'trend':
            value = 30 * Math.sin(time / 10) + time * 2 + Math.random() * 10;
            if (value > 100) value = 100;
            if (value < -100) value = -100;
            break;
        default:
            value = 0;
    }
    
    return value;
}

// Update stats display
function updateStats(pattern) {
    const confidence = Math.abs(Math.sin(dataPoints.length / 10) * 100).toFixed(1);
    document.getElementById('confidenceScore').textContent = `${confidence}%`;
    document.getElementById('predictionCount').textContent = dataPoints.length;
    document.getElementById('patternType').textContent = pattern.charAt(0).toUpperCase() + pattern.slice(1);
}

// Update chart with new data
function updateChart() {
    if (!isRunning) return;

    const pattern = document.getElementById('predictionType').value;
    const prediction = generatePrediction(pattern);
    
    dataPoints.push(prediction);
    labels.push('');
    
    if (dataPoints.length > 50) {
        dataPoints.shift();
        labels.shift();
    }
    
    chart.update();
    updateStats(pattern);
    animationId = requestAnimationFrame(updateChart);
}

// Event Listeners
document.getElementById('startBtn').addEventListener('click', function() {
    if (!isRunning) {
        isRunning = true;
        this.textContent = 'Stop AI Simulation';
        this.style.backgroundColor = '#e74c3c';
        updateChart();
    } else {
        isRunning = false;
        this.textContent = 'Start AI Simulation';
        this.style.backgroundColor = '#2ecc71';
        cancelAnimationFrame(animationId);
    }
});

document.getElementById('resetBtn').addEventListener('click', function() {
    dataPoints = [];
    labels = [];
    chart.data.labels = labels;
    chart.data.datasets[0].data = dataPoints;
    chart.update();
    document.getElementById('confidenceScore').textContent = '0%';
    document.getElementById('predictionCount').textContent = '0';
    document.getElementById('patternType').textContent = '-';
});

document.getElementById('predictionType').addEventListener('change', function() {
    dataPoints = [];
    labels = [];
    chart.data.labels = labels;
    chart.data.datasets[0].data = dataPoints;
    chart.update();
});

// Initialize the chart when the page loads
window.addEventListener('load', initChart);