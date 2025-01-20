// Connect to the socket
const socket = io.connect();

// Listen for chat history updates
// Listening for new private chat messages
socket.on('new_message', function (data) {
  const chatWindow = document.getElementById(`chat-messages-${data.conversation_id}`);
  if (chatWindow) {
    // Create new message element
    const msgElement = document.createElement('div');
    msgElement.classList.add('message');
    msgElement.dataset.messageId = data.message_id;  // Retain the message ID

    // Dynamically style sent vs. received messages based on the sender
    if (data.sender_id === currentUserId) {
      msgElement.classList.add('sent');
    } else {
      msgElement.classList.add('received');
    }

    // Set inner HTML with message content, timestamp, and options
    msgElement.innerHTML = `
      <p class="message-text">${data.message}</p>
      <span class="message-timestamp">${formatTimestamp(data.timestamp)}</span>
      <div class="message-status">
        <span class="seen-icon">${data.isRead ? '<img src="/static/icons/seen.png" />' : ''}</span>
        <span class="unseen-icon">${!data.isRead ? '<img src="/static/icons/unseen.png" />' : ''}</span>
      </div>
      <div class="message-options">
        <button class="message-settings-btn"><img id="message-settings-btn-img" src="/static/icons/down.png"></button>
        <div class="message-settings-menu">
          <ul id="message-menu-${data.message_id}">
            ${data.sender_id === currentUserId ? '<li class="delete-option">Delete</li>' : ''}
          </ul>
        </div>
      </div>
    `;

    // Append the new message to the chat window
    chatWindow.prepend(msgElement);

    // Scroll to the bottom to show the newest message
    chatWindow.scrollTop = chatWindow.scrollHeight;
  } else {
    console.error(`Chat window not found for conversation ${data.conversation_id}`);
  }
});


// Listening for new group chat messages
socket.on('new_group_message', function (data) {
  const groupChatWindow = document.getElementById(`group-messages-${data.group_id}`);
  console.log('Group ID:', data.group_id);
  console.log('Group Chat Window:', groupChatWindow);
  const lastMessageDateElement = document.querySelector(`#group-window-${data.group_id} .last-message-date`);

  if (groupChatWindow) {
    // Create new message element for group
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.dataset.messageId = data.message_id;  // Retain the message ID

    // Dynamically style sent vs. received messages based on the sender
    if (data.sender_id === currentUserId) {
      messageElement.classList.add('sent');
    } else {
      messageElement.classList.add('received');
    }

    // Set inner HTML with message content, timestamp, and options
    messageElement.innerHTML = `
      ${data.sender_id !== currentUserId ? `<p class="sender-name">~ ${data.sender_name}</p>` : ''}
      <p class="message-text">${data.content}</p>
      <span class="message-timestamp" id="group-message-time-stamp">${formatTimestamp(data.timestamp)}</span>
      <div class="message-options">
        <button class="message-settings-btn"><img src="/static/icons/down.png" id="message-settings-btn-img" /></button>
        <div class="message-settings-menu">
          <ul>
            ${data.sender_id === currentUserId ? '<li class="delete-option">Delete</li>' : ''}
          </ul>
        </div>
      </div>
    `;
    // Append the new message to the group chat window
    groupChatWindow.prepend(messageElement);

    // Update last message timestamp
    if (lastMessageDateElement) {
      lastMessageDateElement.textContent = formatTimestamp(data.timestamp);
    }

    // Scroll to the bottom to show the newest message
    groupChatWindow.scrollTop = groupChatWindow.scrollHeight;
  } else {
    console.error(`Group chat window not found for group ${data.group_id}`);
  }
});