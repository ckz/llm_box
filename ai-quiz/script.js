const questions = [
    {
        question: "What is Machine Learning?",
        options: [
            "A type of computer hardware",
            "The ability of computers to learn without explicit programming",
            "A programming language",
            "A type of computer virus"
        ],
        correct: 1
    },
    {
        question: "What is React.js?",
        options: [
            "A database management system",
            "A JavaScript library for building user interfaces",
            "A programming language",
            "A web server"
        ],
        correct: 1
    },
    {
        question: "What is JSX in React?",
        options: [
            "A JavaScript XML syntax extension",
            "A Java programming extension",
            "A JSON format",
            "A JavaScript testing framework"
        ],
        correct: 0
    },
    {
        question: "Which hook is used for side effects in React?",
        options: [
            "useState",
            "useEffect",
            "useContext",
            "useReducer"
        ],
        correct: 1
    },
    {
        question: "What is D3.js primarily used for?",
        options: [
            "Database management",
            "Data visualization and manipulation of documents based on data",
            "3D gaming",
            "Server-side rendering"
        ],
        correct: 1
    },
    {
        question: "What is a React component?",
        options: [
            "A JavaScript function or class that returns HTML elements",
            "A CSS stylesheet",
            "A database table",
            "A testing framework"
        ],
        correct: 0
    },
    {
        question: "What is the Virtual DOM in React?",
        options: [
            "A real DOM element",
            "A lightweight copy of the real DOM for performance optimization",
            "A virtual reality interface",
            "A browser extension"
        ],
        correct: 1
    },
    {
        question: "Which library is commonly used for state management in React?",
        options: [
            "jQuery",
            "Redux",
            "Lodash",
            "Moment.js"
        ],
        correct: 1
    },
    {
        question: "What is Three.js used for?",
        options: [
            "3D graphics and animations in the browser",
            "Server-side rendering",
            "Database management",
            "API testing"
        ],
        correct: 0
    },
    {
        question: "What is WebGL?",
        options: [
            "A web browser",
            "A JavaScript library",
            "A 3D graphics API for the web",
            "A testing framework"
        ],
        correct: 2
    }
];

let currentQuestionIndex = 0;
let score = 0;

const startButton = document.getElementById('start-btn');
const nextButton = document.getElementById('next-btn');
const questionContainer = document.getElementById('question-container');
const questionElement = document.getElementById('question');
const optionsContainer = document.getElementById('options-container');
const scoreContainer = document.getElementById('score-container');
const scoreElement = document.getElementById('score');
const totalElement = document.getElementById('total');
const restartButton = document.getElementById('restart-btn');
const progressBar = document.getElementById('progress');
const scoreMessage = document.getElementById('score-message');

startButton.addEventListener('click', startQuiz);
nextButton.addEventListener('click', () => {
    currentQuestionIndex++;
    setNextQuestion();
});
restartButton.addEventListener('click', startQuiz);

function startQuiz() {
    startButton.classList.add('hide');
    questionContainer.classList.remove('hide');
    scoreContainer.classList.add('hide');
    currentQuestionIndex = 0;
    score = 0;
    updateProgressBar();
    setNextQuestion();
}

function setNextQuestion() {
    resetState();
    if (currentQuestionIndex < questions.length) {
        showQuestion(questions[currentQuestionIndex]);
        updateProgressBar();
    } else {
        showScore();
    }
}

function showQuestion(question) {
    questionElement.innerText = question.question;
    question.options.forEach((option, index) => {
        const button = document.createElement('button');
        button.innerText = option;
        button.classList.add('option');
        button.addEventListener('click', () => selectAnswer(index));
        optionsContainer.appendChild(button);
    });
}

function resetState() {
    nextButton.classList.add('hide');
    while (optionsContainer.firstChild) {
        optionsContainer.removeChild(optionsContainer.firstChild);
    }
}

function selectAnswer(index) {
    const correct = questions[currentQuestionIndex].correct === index;
    const buttons = optionsContainer.getElementsByClassName('option');
    
    Array.from(buttons).forEach(button => {
        button.disabled = true;
    });

    if (correct) {
        buttons[index].classList.add('correct');
        score++;
    } else {
        buttons[index].classList.add('wrong');
        buttons[questions[currentQuestionIndex].correct].classList.add('correct');
    }

    if (currentQuestionIndex < questions.length - 1) {
        nextButton.classList.remove('hide');
    } else {
        showScore();
    }
}

function updateProgressBar() {
    const progress = ((currentQuestionIndex) / questions.length) * 100;
    progressBar.style.width = `${progress}%`;
}

function getScoreMessage(score, total) {
    const percentage = (score / total) * 100;
    if (percentage === 100) {
        return "Perfect score! You're a web development expert! 🏆";
    } else if (percentage >= 80) {
        return "Excellent work! You have a strong understanding of web development! 🌟";
    } else if (percentage >= 60) {
        return "Good job! Keep learning and practicing! 📚";
    } else if (percentage >= 40) {
        return "Not bad! There's room for improvement. Keep studying! 💪";
    } else {
        return "Time to hit the books! Don't give up! 📖";
    }
}

function showScore() {
    questionContainer.classList.add('hide');
    scoreContainer.classList.remove('hide');
    scoreElement.textContent = score;
    totalElement.textContent = questions.length;
    scoreMessage.textContent = getScoreMessage(score, questions.length);
    progressBar.style.width = '100%';
}