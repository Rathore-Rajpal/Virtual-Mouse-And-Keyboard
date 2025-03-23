const API_ENDPOINT = 'http://localhost:5000/generate';
const userInput = document.getElementById('user-input');
const generateBtn = document.getElementById('generate-btn');
const imageGrid = document.getElementById('image-grid');
const loader = document.getElementById('loader');
const toast = document.getElementById('toast');
const historyList = document.getElementById('history-list');

// Initialize history with maximum 10 items
let generationHistory = JSON.parse(localStorage.getItem('imageHistory')) || [];
generationHistory = generationHistory.slice(0, 10); // Keep only latest 10 items

// Load history in correct order (newest first)
generationHistory.reverse().forEach(item => addToHistory(item.imageData, item.prompt));

async function generateImage(event) {
    event.preventDefault();
    const prompt = userInput.value.trim();

    if (!prompt) {
        showToast('Please enter an image description', 'error');
        return;
    }

    try {
        loader.style.display = 'flex';
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Image generation failed');
        }

        const { image } = await response.json();
        displayImageCard(image, prompt);
        userInput.value = '';
        showToast('Image generated successfully!', 'success');
        
        // Add to history and update storage
        addToHistory(image, prompt);
        updateLocalStorage();

    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        loader.style.display = 'none';
    }
}

function updateLocalStorage() {
    // Keep only latest 10 items
    generationHistory = generationHistory.slice(0, 10);
    localStorage.setItem('imageHistory', JSON.stringify(generationHistory));
}

function addToHistory(imageData, prompt) {
    // Create history item
    const historyItem = document.createElement('div');
    historyItem.className = 'history-item';
    historyItem.innerHTML = `
        <img src="${imageData}" alt="${prompt}">
    `;
    historyItem.dataset.prompt = prompt;
    
    // Add click handler for preview
    historyItem.addEventListener('click', () => {
        showImageModal(imageData, prompt);
    });

    // Add to beginning of history
    historyList.insertBefore(historyItem, historyList.firstChild);
    
    // Add to memory array
    generationHistory.unshift({ prompt, imageData });
    
    // Remove excess items from DOM
    if (historyList.children.length > 10) {
        historyList.removeChild(historyList.lastChild);
    }
}

// Rest of the code (displayImageCard, showImageModal, downloadImage, etc) remains the same

function displayImageCard(imageData, prompt) {
    const card = document.createElement('div');
    card.className = 'image-card';
    card.innerHTML = `
        <img src="${imageData}" class="generated-image" alt="${prompt}">
        <div class="image-overlay">
            <button class="download-btn" onclick="downloadImage('${imageData}', '${prompt}')">
                <i class="fas fa-download"></i>
            </button>
        </div>
    `;
    
    // Add click handler for zoom
    card.querySelector('.generated-image').addEventListener('click', () => {
        showImageModal(imageData, prompt);
    });
    
    imageGrid.insertBefore(card, imageGrid.firstChild);
}

function addToHistory(imageData, prompt) {
    const historyItem = document.createElement('div');
    historyItem.className = 'history-item';
    historyItem.innerHTML = `
        <img src="${imageData}" alt="${prompt}">
    `;
    historyItem.dataset.prompt = prompt;
    
    historyItem.addEventListener('click', () => {
        showImageModal(imageData, prompt);
    });

    historyList.insertBefore(historyItem, historyList.firstChild);
    
    // Update localStorage (keep only last 10 items)
    generationHistory.unshift({ prompt, imageData });
    if (generationHistory.length > 10) generationHistory.pop();
    localStorage.setItem('imageHistory', JSON.stringify(generationHistory));
}

function showImageModal(imageData, prompt) {
    const modal = document.createElement('div');
    modal.className = 'image-modal';
    modal.innerHTML = `
        <span class="close-btn" onclick="this.parentElement.remove()">&times;</span>
        <img class="modal-content" src="${imageData}">
        <div class="modal-prompt">${prompt}</div>
    `;
    document.body.appendChild(modal);
}

function downloadImage(imageData, prompt) {
    const link = document.createElement('a');
    link.href = imageData;
    link.download = `generated-${prompt.slice(0, 20)}-${Date.now()}.jpg`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showToast('Image downloaded!', 'success');
}

function showToast(message, type = 'info') {
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    setTimeout(() => toast.classList.remove('show'), 3000);
}

// Event listeners
generateBtn.addEventListener('click', generateImage);
userInput.addEventListener('input', () => {
    document.getElementById('char-count').textContent = userInput.value.length;
});
userInput.addEventListener('keypress', (e) => e.key === 'Enter' && generateImage(e));