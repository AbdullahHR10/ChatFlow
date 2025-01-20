/**
 * Loads the chat history for a specific conversation and displays it in the chat window.
 *
 * This function fetches the chat history from the server for the given `conversationId`,
 * processes the message data, and updates the chat messages container with the retrieved
 * messages. It also displays the last message timestamp and updates the message status
 * (read/unread) for each message. If there are no messages, it shows a placeholder message.
 *
 * @param {string} conversationId - The unique identifier for the conversation.
 */
function loadChatHistory (conversationId) {
  // Select the chat messages container and the last message date element in the conversation
  const chatMessagesContainer = document.querySelector(`#chat-window-${conversationId} .chat-messages`);
  const lastMessageDateElement = document.querySelector(`#chat-window-${conversationId} .last-message-date`);

  // If the chat messages container isn't found, log an error and stop execution
  if (!chatMessagesContainer) {
    console.error(`Chat container not found for conversation ID: ${conversationId}`);
    return;
  }

  // Fetch the chat history for the given conversation ID
  fetch(`/chats/${conversationId}/history`)
    .then(response => {
      // If the network response isn't okay, throw an error
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json(); // Parse the JSON response
    })
    .then(data => {
      // Clear the existing messages in the chat container
      chatMessagesContainer.innerHTML = '';

      // Check if there are messages to display
      if (data.messages && data.messages.length > 0) {
        // Show the timestamp of the last message
        const lastMessage = data.messages[data.messages.length - 1]; // Get the last message
        if (lastMessageDateElement) {
          lastMessageDateElement.textContent = formatTimestamp(lastMessage.timestamp);
        }

        // Loop through the messages, reverse them for chronological order, and display them
        data.messages.reverse().forEach(message => {
          const messageElement = document.createElement('div');
          const isRead = message.is_read; // Check if the message is read
          messageElement.classList.add('message'); // Add the 'message' class to the message element

          // Add the data-message-id attribute to the message element for later reference
          messageElement.dataset.messageId = message.id;

          // Dynamically style sent vs. received messages based on the sender
          if (message.sender_id === currentUserId) {
            messageElement.classList.add('sent');
          } else {
            messageElement.classList.add('received');
          }

          // Set the inner HTML for the message element, including message text, timestamp, and options
          messageElement.innerHTML = `
                  <p class="message-text">${message.content}</p>
                  <span class="message-timestamp">${formatTimestamp(message.timestamp)}</span>
                  <div class="message-status">
                      <span class="seen-icon">${isRead ? '<img src="/static/icons/seen.png" />' : ''}</span>
                      <span class="unseen-icon">${!isRead ? '<img src="/static/icons/unseen.png" />' : ''}</span>
                  </div>
                  <div class="message-options">
                      <button class="message-settings-btn"><img id="message-settings-btn-img" src="/static/icons/down.png"></button>
                      <div class="message-settings-menu">
                          <ul id="message-menu-${message.id}">
                              ${message.sender_id === currentUserId ? '<li class="delete-option">Delete</li>' : ''}
                          </ul>
              `;

          // Append the message element to the chat messages container
          chatMessagesContainer.appendChild(messageElement);
        });

        // Scroll to the bottom of the chat container to show the newest messages
        chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
      }
    })
    .catch(err => {
      // Log any errors that occur during the fetch operation
      console.error('Error fetching chat history:', err);
      chatMessagesContainer.innerHTML = 'Failed to load messages.'; // Show a failure message
    });
}
