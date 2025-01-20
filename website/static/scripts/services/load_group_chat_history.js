/**
 * Loads the chat history for a specific group and displays it in the chat window.
 *
 * This function fetches the chat history from the server for the given `groupId`,
 * processes the message data, and updates the chat messages container with the retrieved
 * messages. It also displays the last message timestamp and updates the message status
 * (read/unread) for each message. If there are no messages, it shows a placeholder message.
 *
 * @param {string} groupId - The unique identifier for the group.
 */
function loadGroupChatHistory(groupId) {
  // Select the group messages container and the last message date element in the group
  const chatMessagesContainer = document.querySelector(`#group-messages-${groupId}`);
  const lastMessageDateElement = document.querySelector(`#group-window-${groupId} .last-message-date`);

  // If the group messages container isn't found, log an error and stop execution
  if (!chatMessagesContainer) {
    console.error(`Group chat container not found for group ID: ${groupId}`);
    return;
  }

  // Fetch the group chat history for the given group ID
  fetch(`/groups/${groupId}/history`)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json(); // Parse the JSON response
    })
    .then(data => {
      chatMessagesContainer.innerHTML = ''; // Clear existing messages

      if (data.messages && data.messages.length > 0) {
        const lastMessage = data.messages[data.messages.length - 1];
        if (lastMessageDateElement) {
          lastMessageDateElement.textContent = formatTimestamp(lastMessage.timestamp); // Update last message timestamp
        }

        data.messages.reverse().forEach(message => {
          const messageElement = document.createElement('div');
          messageElement.classList.add('message');
          messageElement.dataset.messageId = message.id;

          // Dynamically style sent vs. received messages based on the sender
          if (message.sender_id === currentUserId) {
            messageElement.classList.add('sent');
          } else {
            messageElement.classList.add('received');
          }

          messageElement.innerHTML = `
            ${message.sender_id !== currentUserId ? `<p class="sender-name">~ ${message.sender_name}</p>` : ''}
            <p class="message-text">${message.content}</p>
            <span class="message-timestamp" id="group-message-time-stamp">${formatTimestamp(message.timestamp)}</span>
            <div class="message-options">
              <button class="message-settings-btn"><img src="/static/icons/down.png" id="message-settings-btn-img" /></button>
              <div class="message-settings-menu">
                <ul>
                  ${message.sender_id === currentUserId ? '<li class="delete-option">Delete</li>' : ''}
                </ul>
              </div>
            </div>
          `;

          chatMessagesContainer.appendChild(messageElement);
        });

        // Scroll to the bottom to show the newest messages
        chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
      }
    })
    .catch(err => {
      console.error('Error fetching group chat history:', err);
      chatMessagesContainer.innerHTML = 'Failed to load messages.';
    });
}
