// Core application state
const state = {
    currentMode: 'chat',
    context: {
        messages: [],
        tokenCount: 0,
        maxTokens: 4096
    }
};

// UI Elements
const elements = {
    modeBtns: document.querySelectorAll('.mode-btn'),
    containers: {
        chat: document.querySelector('.chat-container'),
        code: document.querySelector('.code-container'),
        knowledge: document.querySelector('.knowledge-container')
    },
    messageInput: document.querySelector('.message-input'),
    sendBtn: document.querySelector('.send-btn'),
    messagesContainer: document.querySelector('.messages'),
    tokenFill: document.querySelector('.token-fill'),
    historyList: document.querySelector('.history-list'),
    connectionStatus: document.querySelector('.connection-status')
};

// Event Handlers
function initializeEventListeners() {
    // Mode switching
    elements.modeBtns.forEach(btn => {
        btn.addEventListener('click', () => switchMode(btn.dataset.mode));
    });

    // Message sending
    elements.sendBtn.addEventListener('click', handleSendMessage);
    elements.messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    });
}

// Mode Switching
function switchMode(mode) {
    if (mode === state.currentMode) return;

    // Update UI
    elements.modeBtns.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.mode === mode);
    });

    // Hide all containers
    Object.values(elements.containers).forEach(container => {
        container.classList.add('hidden');
    });

    // Show selected container
    elements.containers[mode].classList.remove('hidden');

    // Update state
    state.currentMode = mode;
}

// Message Handling
async function handleSendMessage() {
    const message = elements.messageInput.value.trim();
    if (!message) return;

    // Clear input
    elements.messageInput.value = '';

    // Add message to UI
    appendMessage('user', message);

    try {
        // Update connection status
        elements.connectionStatus.textContent = 'Processing...';

        // Process based on current mode
        let response;
        switch (state.currentMode) {
            case 'chat':
                response = await processChat(message);
                break;
            case 'code':
                response = await processCode(message);
                break;
            case 'knowledge':
                response = await processKnowledge(message);
                break;
        }

        // Add response to UI
        appendMessage('assistant', response);

        // Update context
        updateContext(message, response);

    } catch (error) {
        console.error('Error processing message:', error);
        appendMessage('system', 'An error occurred while processing your message.');
    } finally {
        elements.connectionStatus.textContent = 'Connected';
    }
}

// Message Display
function appendMessage(role, content) {
    const messageElement = document.createElement('div');
    messageElement.className = `message ${role}-message`;
    
    const timestamp = new Date().toLocaleTimeString();
    messageElement.innerHTML = `
        <div class="message-header">
            <span class="message-role">${role}</span>
            <span class="message-time">${timestamp}</span>
        </div>
        <div class="message-content">${formatMessage(content)}</div>
    `;

    elements.messagesContainer.appendChild(messageElement);
    elements.messagesContainer.scrollTop = elements.messagesContainer.scrollHeight;
}

// Message Formatting
function formatMessage(content) {
    // Basic markdown-like formatting
    return content
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/\*\*([^\*]+)\*\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br>');
}

// Context Management
function updateContext(message, response) {
    // Add to context
    state.context.messages.push(
        { role: 'user', content: message },
        { role: 'assistant', content: response }
    );

    // Simple token estimation (can be replaced with more accurate counting)
    const estimatedTokens = (message.length + response.length) / 4;
    state.context.tokenCount += estimatedTokens;

    // Update token display
    const tokenPercentage = (state.context.tokenCount / state.context.maxTokens) * 100;
    elements.tokenFill.style.width = `${Math.min(tokenPercentage, 100)}%`;

    // Trim context if needed
    if (state.context.tokenCount > state.context.maxTokens) {
        trimContext();
    }
}

// Context Management
function trimContext() {
    while (state.context.tokenCount > state.context.maxTokens * 0.8) {
        const [removed1, removed2] = state.context.messages.splice(0, 2);
        state.context.tokenCount -= (removed1.content.length + removed2.content.length) / 4;
    }
}

// Mode-specific processing (placeholder implementations)
async function processChat(message) {
    // Implement actual API call here
    return "This is a placeholder response for the chat mode. In a real implementation, this would connect to an AI service.";
}

async function processCode(message) {
    // Implement actual code processing here
    return "This is a placeholder response for the code mode. In a real implementation, this would process code-related queries.";
}

async function processKnowledge(message) {
    // Implement actual knowledge base query here
    return "This is a placeholder response for the knowledge mode. In a real implementation, this would query a knowledge base.";
}

// Initialize application
function initialize() {
    initializeEventListeners();
    elements.connectionStatus.textContent = 'Connected';
}

// Start the application
document.addEventListener('DOMContentLoaded', initialize);