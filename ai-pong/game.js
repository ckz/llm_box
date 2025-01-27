class AIPong {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        
        // Set canvas size
        this.canvas.width = 750;
        this.canvas.height = 400;
        
        // Game objects
        this.ball = {
            x: this.canvas.width / 2,
            y: this.canvas.height / 2,
            radius: 8,
            speed: 5,
            dx: 5,
            dy: 5
        };
        
        this.paddleHeight = 80;
        this.paddleWidth = 10;
        this.playerPaddle = {
            y: this.canvas.height / 2 - this.paddleHeight / 2,
            score: 0
        };
        this.aiPaddle = {
            y: this.canvas.height / 2 - this.paddleHeight / 2,
            score: 0,
            predictions: [],
            accuracy: 0
        };
        
        // Game state
        this.isRunning = false;
        this.difficulty = 'medium';
        
        // Event listeners
        this.canvas.addEventListener('mousemove', (e) => this.movePlayerPaddle(e));
        document.getElementById('startBtn').addEventListener('click', () => this.toggleGame());
        document.getElementById('resetBtn').addEventListener('click', () => this.resetGame());
        document.getElementById('aiDifficulty').addEventListener('change', (e) => {
            this.difficulty = e.target.value;
            this.resetGame();
        });
    }
    
    movePlayerPaddle(e) {
        const rect = this.canvas.getBoundingClientRect();
        const mouseY = e.clientY - rect.top;
        this.playerPaddle.y = Math.max(0, Math.min(mouseY - this.paddleHeight / 2, 
            this.canvas.height - this.paddleHeight));
    }
    
    predictBallPosition() {
        // AI prediction logic
        let futureY = this.ball.y;
        let tempX = this.ball.x;
        let tempDx = this.ball.dx;
        let tempDy = this.ball.dy;
        
        // Simulate ball movement to predict where it will intersect with AI paddle
        while (tempX < this.canvas.width - this.paddleWidth) {
            tempX += tempDx;
            futureY += tempDy;
            
            // Account for bounces
            if (futureY <= 0 || futureY >= this.canvas.height) {
                tempDy = -tempDy;
            }
        }
        
        // Add some uncertainty based on difficulty
        const uncertainty = {
            easy: 0.3,
            medium: 0.15,
            hard: 0.05
        }[this.difficulty];
        
        futureY += (Math.random() - 0.5) * this.canvas.height * uncertainty;
        
        // Record prediction for accuracy calculation
        this.aiPaddle.predictions.push({
            predicted: futureY,
            actual: this.ball.y
        });
        
        return futureY;
    }
    
    moveAIPaddle() {
        if (this.ball.dx > 0) { // Ball moving towards AI
            const predictedY = this.predictBallPosition();
            const targetY = predictedY - this.paddleHeight / 2;
            
            // Movement speed based on difficulty
            const speed = {
                easy: 3,
                medium: 5,
                hard: 7
            }[this.difficulty];
            
            if (this.aiPaddle.y < targetY) {
                this.aiPaddle.y = Math.min(this.aiPaddle.y + speed, 
                    this.canvas.height - this.paddleHeight);
            } else if (this.aiPaddle.y > targetY) {
                this.aiPaddle.y = Math.max(this.aiPaddle.y - speed, 0);
            }
        }
    }
    
    updateBall() {
        this.ball.x += this.ball.dx;
        this.ball.y += this.ball.dy;
        
        // Wall collisions
        if (this.ball.y <= 0 || this.ball.y >= this.canvas.height) {
            this.ball.dy = -this.ball.dy;
        }
        
        // Paddle collisions
        if (this.ball.dx < 0) { // Moving left
            if (this.ball.x <= this.paddleWidth &&
                this.ball.y >= this.playerPaddle.y &&
                this.ball.y <= this.playerPaddle.y + this.paddleHeight) {
                this.ball.dx = -this.ball.dx;
                this.adjustBallAngle(this.playerPaddle.y);
            }
        } else { // Moving right
            if (this.ball.x >= this.canvas.width - this.paddleWidth &&
                this.ball.y >= this.aiPaddle.y &&
                this.ball.y <= this.aiPaddle.y + this.paddleHeight) {
                this.ball.dx = -this.ball.dx;
                this.adjustBallAngle(this.aiPaddle.y);
            }
        }
        
        // Scoring
        if (this.ball.x <= 0) {
            this.aiPaddle.score++;
            this.resetBall();
        } else if (this.ball.x >= this.canvas.width) {
            this.playerPaddle.score++;
            this.resetBall();
        }
        
        // Update scores
        document.getElementById('playerScore').textContent = this.playerPaddle.score;
        document.getElementById('aiScore').textContent = this.aiPaddle.score;
        
        // Calculate and update AI accuracy
        if (this.aiPaddle.predictions.length > 0) {
            const accuracy = this.aiPaddle.predictions.reduce((acc, pred) => {
                const diff = Math.abs(pred.predicted - pred.actual);
                return acc + (1 - Math.min(diff / this.canvas.height, 1));
            }, 0) / this.aiPaddle.predictions.length * 100;
            
            document.getElementById('aiAccuracy').textContent = 
                Math.round(accuracy) + '%';
        }
    }
    
    adjustBallAngle(paddleY) {
        // Change ball angle based on where it hits the paddle
        const relativeIntersectY = 
            (paddleY + (this.paddleHeight / 2)) - this.ball.y;
        const normalizedIntersectY = 
            relativeIntersectY / (this.paddleHeight / 2);
        const bounceAngle = normalizedIntersectY * Math.PI / 4;
        
        const speed = Math.sqrt(this.ball.dx * this.ball.dx + 
            this.ball.dy * this.ball.dy);
        const direction = this.ball.dx > 0 ? -1 : 1;
        
        this.ball.dx = direction * speed * Math.cos(bounceAngle);
        this.ball.dy = speed * -Math.sin(bounceAngle);
    }
    
    resetBall() {
        this.ball.x = this.canvas.width / 2;
        this.ball.y = this.canvas.height / 2;
        this.ball.dx = (Math.random() > 0.5 ? 1 : -1) * this.ball.speed;
        this.ball.dy = (Math.random() * 2 - 1) * this.ball.speed;
    }
    
    draw() {
        // Clear canvas
        this.ctx.fillStyle = '#000';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw center line
        this.ctx.setLineDash([5, 15]);
        this.ctx.beginPath();
        this.ctx.moveTo(this.canvas.width / 2, 0);
        this.ctx.lineTo(this.canvas.width / 2, this.canvas.height);
        this.ctx.strokeStyle = '#333';
        this.ctx.stroke();
        this.ctx.setLineDash([]);
        
        // Draw ball
        this.ctx.beginPath();
        this.ctx.arc(this.ball.x, this.ball.y, this.ball.radius, 0, Math.PI * 2);
        this.ctx.fillStyle = '#fff';
        this.ctx.fill();
        
        // Draw paddles
        this.ctx.fillStyle = '#4CAF50';
        this.ctx.fillRect(0, this.playerPaddle.y, 
            this.paddleWidth, this.paddleHeight);
        this.ctx.fillRect(this.canvas.width - this.paddleWidth, 
            this.aiPaddle.y, this.paddleWidth, this.paddleHeight);
    }
    
    gameLoop() {
        if (!this.isRunning) return;
        
        this.moveAIPaddle();
        this.updateBall();
        this.draw();
        
        requestAnimationFrame(() => this.gameLoop());
    }
    
    toggleGame() {
        this.isRunning = !this.isRunning;
        const btn = document.getElementById('startBtn');
        if (this.isRunning) {
            btn.textContent = 'Pause Game';
            btn.style.backgroundColor = '#f44336';
            this.gameLoop();
        } else {
            btn.textContent = 'Start Game';
            btn.style.backgroundColor = '#4CAF50';
        }
    }
    
    resetGame() {
        this.isRunning = false;
        this.playerPaddle.score = 0;
        this.aiPaddle.score = 0;
        this.aiPaddle.predictions = [];
        this.resetBall();
        this.playerPaddle.y = this.canvas.height / 2 - this.paddleHeight / 2;
        this.aiPaddle.y = this.canvas.height / 2 - this.paddleHeight / 2;
        
        const btn = document.getElementById('startBtn');
        btn.textContent = 'Start Game';
        btn.style.backgroundColor = '#4CAF50';
        
        document.getElementById('playerScore').textContent = '0';
        document.getElementById('aiScore').textContent = '0';
        document.getElementById('aiAccuracy').textContent = '0%';
        
        this.draw();
    }
}

// Initialize game when page loads
window.addEventListener('load', () => {
    new AIPong();
});