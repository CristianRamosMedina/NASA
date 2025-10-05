/**
 * EXO Chat Widget
 * Connects to Flask API for AI-powered exoplanet assistance
 */

console.log("[EXO Chat] Loading...");

const API_URL = 'http://localhost:5000/api';
let chatHistory = [];

document.addEventListener('DOMContentLoaded', () => {
  console.log("[EXO Chat] DOM Content Loaded");
  const chatBtn = document.getElementById('exoChatBtn');
  const chatPanel = document.getElementById('exoChatPanel');
  const closeBtn = document.getElementById('exoCloseBtn');
  const chatForm = document.getElementById('exoChatForm');
  const chatInput = document.getElementById('exoInput');
  const messagesContainer = document.getElementById('exoMessages');

  // Toggle chat panel
  chatBtn.addEventListener('click', () => {
    chatPanel.classList.toggle('hidden');
    if (!chatPanel.classList.contains('hidden')) {
      chatInput.focus();
    }
  });

  closeBtn.addEventListener('click', () => {
    chatPanel.classList.add('hidden');
  });

  // Send message
  chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const message = chatInput.value.trim();
    if (!message) return;

    // Add user message to UI
    addMessage(message, 'user');
    chatInput.value = '';

    // Add to history
    chatHistory.push({ role: 'user', content: message });

    // Show typing indicator
    const typingId = addTypingIndicator();

    try {
      // Call API
      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message: message,
          history: chatHistory
        })
      });

      const data = await response.json();

      // Remove typing indicator
      removeTypingIndicator(typingId);

      if (response.ok) {
        // Add assistant message
        addMessage(data.response, 'assistant');
        chatHistory.push({ role: 'assistant', content: data.response });
      } else {
        // Show error
        addMessage(`Error: ${data.error || 'Could not connect to EXO'}`, 'error');
      }
    } catch (error) {
      removeTypingIndicator(typingId);
      addMessage('Error: Could not connect to EXO API. Make sure the server is running on port 5000.', 'error');
      console.error('EXO API Error:', error);
    }
  });

  // Add message to chat
  function addMessage(text, type = 'assistant') {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `message-${type}`);

    if (type === 'user') {
      messageDiv.innerHTML = `
        <div class="flex justify-end">
          <div class="bg-nasa text-space-dark px-4 py-2 rounded-lg max-w-[80%]">
            ${escapeHtml(text)}
          </div>
        </div>
      `;
    } else if (type === 'error') {
      messageDiv.innerHTML = `
        <div class="bg-red-900 text-red-200 px-4 py-2 rounded-lg text-sm">
          ${escapeHtml(text)}
        </div>
      `;
    } else {
      messageDiv.innerHTML = `
        <div class="flex justify-start">
          <div class="bg-space-dark border border-planet text-space-star px-4 py-2 rounded-lg max-w-[80%]">
            ${escapeHtml(text)}
          </div>
        </div>
      `;
    }

    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  // Add typing indicator
  function addTypingIndicator() {
    const id = 'typing-' + Date.now();
    const typingDiv = document.createElement('div');
    typingDiv.id = id;
    typingDiv.classList.add('message-typing');
    typingDiv.innerHTML = `
      <div class="flex justify-start">
        <div class="bg-space-dark border border-planet text-space-star px-4 py-2 rounded-lg">
          <div class="flex gap-1">
            <div class="w-2 h-2 bg-nasa rounded-full animate-bounce" style="animation-delay: 0s"></div>
            <div class="w-2 h-2 bg-nasa rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
            <div class="w-2 h-2 bg-nasa rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
          </div>
        </div>
      </div>
    `;
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return id;
  }

  // Remove typing indicator
  function removeTypingIndicator(id) {
    const typingDiv = document.getElementById(id);
    if (typingDiv) {
      typingDiv.remove();
    }
  }

  // Escape HTML to prevent XSS
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
});
