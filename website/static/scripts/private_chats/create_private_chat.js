/**
 * Creates a private chat with another user.
 *
 * This function sends a POST request to create a private chat with a specified user.
 * If a chat already exists, it does nothing. Otherwise, it adds the new chat to the UI.
 *
 * @param {string} chatUserId - The ID of the user with whom the chat is being created.
 */
function createChat (chatUserId) {
  // Send a POST request to create a private chat with the specified user
  fetch('/create_private_chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json' // Set the content type to JSON
    },
    body: JSON.stringify({
      chat_user_id: chatUserId // Send the friend's ID to create the chat
    })
  })
    .then(response => response.json()) // Parse the response as JSON
    .then(data => {
      if (data.chat_id) {
        // If a new chat is created, add it to the UI
        addChatToUI(data.chat_id, chatUserId);
      } else {
        // If there's an error or unexpected response, show an alert
        alert('Error: ' + (data.error || 'Unexpected error'));
      }
    })
    .catch(error => {
      // If there is a network or other error, show an alert with the error message
      alert('Error: ' + error.message || error);
    });
}

/**
 * Adds a new chat to the UI, including creating a chat item and a corresponding chat window.
 *
 * @param {string} chatId - The ID of the new chat.
 * @param {string} chatUserId - The ID of the user with whom the chat is created.
 */
function addChatToUI (chatId, chatUserId) {
  const chatList = document.getElementById('chats-list');

  // Check if the chat list element exists in the DOM
  if (!chatList) {
    console.error('Chat list element not found.');
    return;
  }

  // Check if the chat already exists in the list, to avoid duplicates
  if (!document.getElementById(`chat-item-${chatId}`)) {
    // Create a new chat item and add it to the chat list
    const chatItem = document.createElement('div');
    chatItem.id = `chat-item-${chatId}`;
    chatItem.classList.add('chat-item');
    chatItem.setAttribute('onclick', `selectChat('${chatId}')`);
    chatItem.textContent = `Chat with user ${chatUserId}`; // Chat label (dynamic later)

    chatList.appendChild(chatItem);
  }

  // Create a new chat window for the chat
  const chatWindow = document.createElement('div');
  chatWindow.id = `chat-window-${chatId}`;
  chatWindow.classList.add('chat-window');
  chatWindow.setAttribute('data-conversation-id', chatId);
  chatWindow.style.display = 'none'; // Hide chat window initially

  // Set up the HTML structure for the chat window
  chatWindow.innerHTML = `
      <div class="chat-header">
          <span>Chat with user ${chatUserId}</span> 
      </div>
      <div class="chat-messages"></div>
      <div class="chat-footer">
          <input type="text" id="message-input-${chatId}" placeholder="Type a message" />
          <button class="send-button" data-conversation-id="${chatId}" data-user-id="${chatUserId}">Send</button>
      </div>
  `;

  // Append the newly created chat window to the document body
  document.body.appendChild(chatWindow);

  // Add an event listener to the send button to handle message sending
  const sendButton = chatWindow.querySelector('.send-button');
  sendButton.addEventListener('click', function () {
    sendMessage(chatId, chatUserId); // Call function to send message
  });
  location.reload();
}
