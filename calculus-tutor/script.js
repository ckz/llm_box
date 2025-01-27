// Track current section and progress
let currentSection = 0;
const sections = document.querySelectorAll('section');
let score = 0;

// Initialize Plotly graphs
document.addEventListener('DOMContentLoaded', () => {
    initializeGraphs();
    updateProgress();
});

function initializeGraphs() {
    // Basic function graph
    const x = Array.from({length: 1000}, (_, i) => i * 0.01 - 5);
    const y = x.map(val => Math.sin(val));

    Plotly.newPlot('basicGraph', [{
        x: x,
        y: y,
        type: 'scatter',
        mode: 'lines',
        name: 'f(x) = sin(x)',
        line: {color: '#2196F3'}
    }], {
        title: 'Interactive Function Visualization',
        xaxis: {title: 'x'},
        yaxis: {title: 'f(x)'},
        showlegend: true
    });

    // Part 1 graph - Area under curve
    initializePart1Graph();

    // Part 2 graph - Derivative of integral
    initializePart2Graph();
}

function initializePart1Graph() {
    const x = Array.from({length: 100}, (_, i) => i * 0.1);
    const y = x.map(val => Math.pow(val, 2));

    Plotly.newPlot('part1Graph', [{
        x: x,
        y: y,
        type: 'scatter',
        mode: 'lines',
        name: 'f(x) = x²',
        line: {color: '#2196F3'}
    }], {
        title: 'Area Under the Curve',
        xaxis: {title: 'x', range: [0, 10]},
        yaxis: {title: 'f(x)', range: [0, 100]},
        shapes: []
    });

    // Add event listeners for sliders
    document.getElementById('aValue').addEventListener('input', updateArea);
    document.getElementById('bValue').addEventListener('input', updateArea);
}

function updateArea() {
    const a = parseFloat(document.getElementById('aValue').value);
    const b = parseFloat(document.getElementById('bValue').value);
    
    const x = Array.from({length: 100}, (_, i) => i * 0.1);
    const y = x.map(val => Math.pow(val, 2));
    
    const fillX = x.filter(val => val >= a && val <= b);
    const fillY = fillX.map(val => Math.pow(val, 2));

    const update = {
        shapes: [{
            type: 'path',
            path: `M ${a},0 L ${fillX.map((x, i) => `${x},${fillY[i]}`).join(' L')} L ${b},0 Z`,
            fillcolor: 'rgba(33, 150, 243, 0.3)',
            line: {width: 0},
        }]
    };

    Plotly.relayout('part1Graph', update);
}

function initializePart2Graph() {
    const x = Array.from({length: 100}, (_, i) => i * 0.1 - 5);
    const y = x.map(val => Math.sin(val));

    Plotly.newPlot('part2Graph', [{
        x: x,
        y: y,
        type: 'scatter',
        mode: 'lines',
        name: 'f(x) = sin(x)',
        line: {color: '#2196F3'}
    }], {
        title: 'Derivative of Integral Visualization',
        xaxis: {title: 'x'},
        yaxis: {title: 'f(x)'},
        annotations: []
    });
}

function showFunction(type) {
    const x = Array.from({length: 1000}, (_, i) => i * 0.01 - 5);
    let y;

    switch(type) {
        case 'sin':
            y = x.map(val => Math.sin(val));
            break;
        case 'quadratic':
            y = x.map(val => Math.pow(val, 2));
            break;
        case 'linear':
            y = x.map(val => 2 * val + 1);
            break;
    }

    Plotly.update('basicGraph', {
        'y': [y]
    });
}

function animateIntegral() {
    const x = Array.from({length: 100}, (_, i) => i * 0.1 - 5);
    const y = x.map(val => Math.sin(val));
    let currentX = -5;
    
    function frame() {
        if (currentX >= 5) return;
        
        const area = {
            type: 'path',
            path: `M ${-5},0 L ${x.filter(val => val <= currentX).map((x, i) => 
                `${x},${y[i]}`).join(' L')} L ${currentX},0 Z`,
            fillcolor: 'rgba(33, 150, 243, 0.3)',
            line: {width: 0},
        };

        Plotly.relayout('part2Graph', {
            shapes: [area],
            annotations: [{
                x: currentX,
                y: Math.sin(currentX),
                text: 'f(x)',
                showarrow: true,
                arrowhead: 2
            }]
        });

        currentX += 0.2;
        requestAnimationFrame(frame);
    }

    requestAnimationFrame(frame);
}

// Navigation functions
function navigate(direction) {
    sections[currentSection].classList.remove('active');
    currentSection = Math.max(0, Math.min(sections.length - 1, currentSection + direction));
    sections[currentSection].classList.add('active');
    updateProgress();
    updateNavigationButtons();
}

function updateProgress() {
    const progress = (currentSection / (sections.length - 1)) * 100;
    document.getElementById('progress').style.width = `${progress}%`;
}

function updateNavigationButtons() {
    document.getElementById('prevBtn').disabled = currentSection === 0;
    document.getElementById('nextBtn').disabled = currentSection === sections.length - 1;
}

// Quiz functions
function checkAnswer(problemNum, choice) {
    const explanation = document.getElementById(`explanation${problemNum}`);
    explanation.classList.add('show');

    if ((problemNum === 1 && choice === 'A') || (problemNum === 2 && choice === 'B')) {
        explanation.innerHTML = '<span style="color: green;">✓ Correct!</span> ' + 
            getExplanation(problemNum);
        if (!document.querySelector(`#problem${problemNum} .correct`)) {
            score++;
            updateScore();
        }
        document.querySelector(`#problem${problemNum}`).classList.add('correct');
    } else {
        explanation.innerHTML = '<span style="color: red;">✗ Incorrect.</span> ' + 
            getExplanation(problemNum);
    }
}

function getExplanation(problemNum) {
    if (problemNum === 1) {
        return 'For f(x) = x², the antiderivative is F(x) = x³/3. ' +
            'Therefore, ∫₀² x²dx = [x³/3]₀² = 8/3 - 0 = 8/3';
    } else {
        return 'Using the Second Fundamental Theorem, we know that ' +
            '∫₀ᵖⁱ sin(x)dx = [-cos(x)]₀ᵖⁱ = -cos(π) - (-cos(0)) = -(-1) - (-1) = 2';
    }
}

function updateScore() {
    document.getElementById('scoreDisplay').textContent = `${score}/2 Problems Completed`;
}

function resetQuiz() {
    score = 0;
    updateScore();
    document.querySelectorAll('.problem').forEach(problem => {
        problem.classList.remove('correct');
        const explanation = problem.querySelector('.explanation');
        explanation.classList.remove('show');
        explanation.innerHTML = '';
    });
}

// Initialize navigation state
updateNavigationButtons();