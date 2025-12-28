let isFirstMessage = true;

function send() {
  let input = document.getElementById("input");
  let msg = input.value.trim();
  if (!msg) return;
  
  let chat = document.getElementById("chat");
  
  // Remove empty state on first message
  if (isFirstMessage) {
    chat.innerHTML = '';
    isFirstMessage = false;
  }
  
  // Add user message
  chat.innerHTML += `<div class='message user-message'>${escapeHtml(msg)}</div>`;
  
  // Add thinking indicator
  const thinkingId = 'thinking-' + Date.now();
  chat.innerHTML += `
    <div class='message thinking' id='${thinkingId}'>
      <div class="typing-indicator">
        <span></span>
        <span></span>
        <span></span>
      </div>
      AI is analyzing...
    </div>
  `;
  
  chat.scrollTop = chat.scrollHeight;
  input.value = "";
  
  // Fetch response from Django backend - FIXED THIS LINE
  fetch(`/chat/?message=${encodeURIComponent(msg)}`)
    .then(res => res.json())
    .then(data => {
      // Remove thinking indicator
      const thinkingElement = document.getElementById(thinkingId);
      if (thinkingElement) {
        thinkingElement.remove();
      }
      
      // Add AI response
      chat.innerHTML += `<div class='message bot-message'>${escapeHtml(data.reply)}</div>`;
      chat.scrollTop = chat.scrollHeight;
    })
    .catch(error => {
      // Remove thinking indicator
      const thinkingElement = document.getElementById(thinkingId);
      if (thinkingElement) {
        thinkingElement.remove();
      }
      
      // Show error message
      chat.innerHTML += `<div class='message bot-message' style='color: #e74c3c; border-left-color: #e74c3c;'>Sorry, something went wrong. Please try again.</div>`;
      chat.scrollTop = chat.scrollHeight;
      console.error('Error:', error);
    });
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}