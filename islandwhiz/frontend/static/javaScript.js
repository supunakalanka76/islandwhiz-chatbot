// DOM elements
const userInput = document.getElementById('userInput');
const chatContainer = document.getElementById('chatContainer');
const sendBtn = document.getElementById('sendBtn');
const voiceBtn = document.getElementById('voiceBtn');

// Send message function
// Replace inside sendMessage()

function sendMessage() {
  const message = userInput.value.trim();
  if (message === '') return;

  addChatBubble(message, 'user');
  userInput.value = '';
  showTypingIndicator();

  fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: message })
  })
    .then((res) => res.json())
    .then((data) => {
      removeTypingIndicator();
      addChatBubble(data.response, 'bot');
    })
    .catch((err) => {
      removeTypingIndicator();
      addChatBubble("Oops! Something went wrong. Please try again.", 'bot');
      console.error(err);
    });
}


// Add chat bubble to the container
function addChatBubble(message, sender) {
  const chatDiv = document.createElement('div');
  chatDiv.className = `chat ${sender} animate__animated animate__fadeIn`;

  const avatarDiv = document.createElement('div');
  avatarDiv.className = 'avatar';

  // Set appropriate avatar icon based on sender
  if (sender === 'bot') {
    avatarDiv.innerHTML = '<i class="fa-solid fa-umbrella-beach"></i>';
  } else {
    avatarDiv.innerHTML = '<i class="fa-solid fa-user"></i>';
  }

  const bubbleDiv = document.createElement('div');
  bubbleDiv.className = 'bubble';
  bubbleDiv.innerHTML = message.replace(/\n/g, '<br>');

  chatDiv.appendChild(avatarDiv);
  chatDiv.appendChild(bubbleDiv);
  chatContainer.appendChild(chatDiv);

  // Scroll to the bottom
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Show typing indicator
function showTypingIndicator() {
  const typingDiv = document.createElement('div');
  typingDiv.className = 'chat bot typing-indicator';
  typingDiv.id = 'typingIndicator';

  const avatarDiv = document.createElement('div');
  avatarDiv.className = 'avatar';
  avatarDiv.innerHTML = '<i class="fa-solid fa-umbrella-beach"></i>';

  const bubbleDiv = document.createElement('div');
  bubbleDiv.className = 'bubble typing-bubble';

  for (let i = 0; i < 3; i++) {
    const dot = document.createElement('div');
    dot.className = 'typing-dot';
    bubbleDiv.appendChild(dot);
  }

  typingDiv.appendChild(avatarDiv);
  typingDiv.appendChild(bubbleDiv);
  chatContainer.appendChild(typingDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Remove typing indicator
function removeTypingIndicator() {
  const typingIndicator = document.getElementById('typingIndicator');
  if (typingIndicator) {
    typingIndicator.remove();
  }
}

// Toggle theme
function toggleTheme() {
  document.body.classList.toggle('dark-mode');

  // Save preference to localStorage
  const isDarkMode = document.body.classList.contains('dark-mode');
  localStorage.setItem('darkMode', isDarkMode);
}

// Insert quick question into input
function insertQuestion(element) {
  userInput.value = element.textContent;
  userInput.focus();
}

// Check for saved theme preference
function checkSavedTheme() {
  const savedTheme = localStorage.getItem('darkMode');
  if (savedTheme === 'true') {
    document.body.classList.add('dark-mode');
  }
}

// Event listeners
userInput.addEventListener('keydown', function (event) {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    sendMessage();
  }
});


// Initialize
checkSavedTheme();

// Make functions available globally
window.sendMessage = sendMessage;
window.toggleTheme = toggleTheme;
window.toggleVoiceRecognition = toggleVoiceRecognition;