// Initialize syntax highlighting
hljs.highlightAll();

// Theme Management
function toggleTheme() {
    const body = document.body;
    const themeToggle = document.querySelector('.theme-toggle i');
    const isDark = body.getAttribute('data-theme') !== 'light';
    
    body.setAttribute('data-theme', isDark ? 'light' : '');
    themeToggle.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
    localStorage.setItem('theme', isDark ? 'light' : 'dark');
}

// Initialize theme
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.body.setAttribute('data-theme', savedTheme);
    document.querySelector('.theme-toggle i').className = 
        savedTheme === 'light' ? 'fas fa-sun' : 'fas fa-moon';
}

// Enhanced History Management
let chatHistory = JSON.parse(localStorage.getItem('codingHistory')) || [];

function updateHistoryDisplay(filter = '') {
    const filtered = chatHistory.filter(entry => 
        entry.prompt.toLowerCase().includes(filter.toLowerCase()) ||
        entry.code.toLowerCase().includes(filter.toLowerCase())
    );
    
    const historyList = document.getElementById('history-list');
    historyList.innerHTML = filtered.map((entry, index) => `
        <div class="history-item" onclick="loadHistory(${index})">
            <div class="history-prompt">${entry.prompt}</div>
            <div class="history-code">${entry.code.substring(0, 50)}...</div>
            <div class="history-time">${new Date(entry.timestamp).toLocaleString()}</div>
        </div>
    `).join('');
}

function showToast(message, duration = 3000) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.style.display = 'block';
    setTimeout(() => toast.style.display = 'none', duration);
}

// Enhanced Copy Functionality
function copyCode(button) {
    const code = button.closest('.code-block').querySelector('code').textContent;
    navigator.clipboard.writeText(code).then(() => {
        showToast('Code copied to clipboard!');
    }).catch(err => {
        showToast('Failed to copy code', 5000);
    });
}

// Code Suggestions
const suggestions = [
    'Python function to reverse a string',
    'JavaScript class for HTTP requests',
    'Java program to calculate factorial',
    'React component for login form',
    'SQL query to find duplicate records'
];

function showSuggestions(value) {
    const suggestionsDiv = document.getElementById('suggestions');
    if (!value) {
        suggestionsDiv.style.display = 'none';
        return;
    }
    
    const filtered = suggestions.filter(s => 
        s.toLowerCase().includes(value.toLowerCase())
    );
    
    suggestionsDiv.innerHTML = filtered.map(s => `
        <div class="suggestion-item" onclick="selectSuggestion('${s}')">${s}</div>
    `).join('');
    suggestionsDiv.style.display = 'block';
}

function selectSuggestion(suggestion) {
    document.getElementById('user-input').value = suggestion;
    document.getElementById('suggestions').style.display = 'none';
}

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    updateHistoryDisplay();
    
    document.getElementById('history-search').addEventListener('input', (e) => {
        updateHistoryDisplay(e.target.value);
    });
    
    // Keyboard Shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            generateCode(e);
        }
    });
});

        
// Initialize history display
function updateHistoryDisplay() {
    const historyList = document.getElementById('history-list');
    historyList.innerHTML = chatHistory.map((entry, index) => `
        <div class="history-item" onclick="loadHistory(${index})">
            <div class="history-prompt">${entry.prompt}</div>
            <div class="history-code">${entry.code}</div>
        </div>
    `).join('');
}

function saveToHistory(prompt, code) {
    chatHistory.unshift({ prompt, code });
    if (chatHistory.length > 20) chatHistory.pop(); // Keep last 20 entries
    localStorage.setItem('codingHistory', JSON.stringify(chatHistory));
    updateHistoryDisplay();
}

function clearHistory() {
    chatHistory = [];
    localStorage.removeItem('codingHistory');
    updateHistoryDisplay();
}

function loadHistory(index) {
    const entry = chatHistory[index];
    userInput.value = entry.prompt;
    displayCode(entry.code);
}

function toggleHistory() {
    document.querySelector('.history-panel').classList.toggle('active');
}

// Modified displayCode function to save history
function displayCode(code) {
    const prompt = userInput.value.trim();
    const codeBlock = document.createElement('div');
    codeBlock.className = 'code-output';
    codeBlock.innerHTML = `
        <div class="code-header">
            <span>Generated Code</span>
            <button class="copy-btn" onclick="copyCode(this)">Copy</button>
        </div>
        <pre>${code}</pre>
    `;
    messageContainer.appendChild(codeBlock);
    messageContainer.scrollTop = messageContainer.scrollHeight;
    
    // Save to history
    saveToHistory(prompt, code);
}

// Initial history load
updateHistoryDisplay();

// Rest of your existing JavaScript code remains the same
const generateBtn = document.getElementById('generate-btn');
const userInput = document.getElementById('user-input');
const messageContainer = document.getElementById('message-container');
const loader = document.getElementById('loader');

async function generateCode(event) {
    event.preventDefault();  
    const prompt = userInput.value.trim();
    if (!prompt) {
        displayError('Please enter a coding prompt');
        return;
    }

    loader.style.display = 'block';
    let responseClone = null;

    try {
        const response = await fetch('http://localhost:5000/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt }),
        });

        responseClone = response.clone();
        const data = await response.json();

        if (!response.ok || data.error) {
            throw new Error(data.error || 'Generation failed');
        }

        if (data.code && data.code.trim()) {
            displayCode(data.code);
        } else {
            throw new Error('Received empty code');
        }

    } catch (error) {
        try {
            const errorData = await responseClone?.json();
            displayError(errorData?.error || error.message);
        } catch {
            displayError(error.message);
        }
    } finally {
        loader.style.display = 'none';
        userInput.value = '';
    }
}

function displayError(message) {
    const errorBlock = document.createElement('div');
    errorBlock.className = 'code-output';
    errorBlock.innerHTML = `
        <div class="code-header" style="color: #e74c3c;">
            <span>Error</span>
        </div>
        <pre>${message}</pre>
    `;
    messageContainer.appendChild(errorBlock);
    messageContainer.scrollTop = messageContainer.scrollHeight;
}

function copyCode(button) {
    const code = button.parentElement.nextElementSibling.textContent;
    navigator.clipboard.writeText(code).then(() => {
        button.textContent = 'Copied!';
        setTimeout(() => {
            button.textContent = 'Copy';
        }, 2000);
    });
}

generateBtn.addEventListener('click', generateCode);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') generateCode(e);
});