// API Configuration
const API_URL = 'http://localhost:8000';

// Card interaction
document.querySelectorAll('.card').forEach(card => {
  card.addEventListener('click', () => {
    const message = card.querySelector('h3').textContent;
    document.getElementById('userInput').value = message;
    document.getElementById('userInput').focus();
  });
});

// Send message to backend
async function sendMessage() {
  const input = document.getElementById('userInput');
  const message = input.value.trim();

  if (!message) return;

  try {
    // Show loading state
    console.log('Sending to AI:', message);

    const response = await fetch(`${API_URL}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, history: [] })
    });

    if (!response.ok) {
      throw new Error('API request failed');
    }

    const data = await response.json();

    // Display response
    console.log('AI Response:', data.response);
    alert(`AI Counsellor: ${data.response}`);

  } catch (error) {
    console.error('Error:', error);
    alert('Error connecting to AI. Make sure the backend is running on port 8000.');
  }

  input.value = '';
}

// Event listeners
document.getElementById('sendBtn').addEventListener('click', sendMessage);

document.getElementById('userInput').addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    sendMessage();
  }
});

// Microphone button (placeholder)
document.querySelector('.mic-btn').addEventListener('click', () => {
  alert('Voice input feature coming soon! 🎤');
});