/**
 * Function to handle sending a message in a conversation.
 *
 * @param {string} conversationId - The ID of the conversation to send the message in.
 */
function sendMessage(conversationId) {
  // Get the message input field for the current conversation and retrieve the message content
  const messageInput = document.getElementById(`message-input-${conversationId}`);

  // Check if the input field exists before proceeding
  if (!messageInput) {
    console.error(`Message input field with ID "message-input-${conversationId}" not found.`);
    return; // Exit the function if the input field is not found
  }

  const messageContent = messageInput.value.trim();

  // If no message content, do not proceed
  if (!messageContent) return;

  // Get the sender ID from the send button's data attributes
  const sendButton = document.querySelector(`button[data-conversation-id="${conversationId}"]`);
  const senderId = sendButton.getAttribute('data-sender-id');

  // Determine if this is a group conversation by checking if the receiver_id is available
  const receiverId = sendButton.getAttribute('data-receiver-id') || null;

  // Disable the send button temporarily to prevent multiple sends
  sendButton.disabled = true;

  // Emit the message via Socket.IO to the server
  socket.emit('send_message', {
    conversation_id: conversationId, // The current conversation ID
    sender_id: senderId, // The sender's user ID
    receiver_id: receiverId, // The receiver's user ID (null for group chats)
    message: messageContent // The actual message content
  });

  // Clear the input field after sending the message
  messageInput.value = '';

  // Re-enable the send button after a short delay to allow for another send
  setTimeout(() => {
    sendButton.disabled = false;
  }, 1000);

  // Reload chat history to include the newly sent message
}

/**
 * Event listener for the send button
 * This listens for a click on any send button and sends the message to the server for the respective conversation.
 */
document.querySelectorAll('.send-button').forEach(button => {
  button.addEventListener('click', (event) => {
    // Get the conversation ID associated with the clicked button from its 'data-conversation-id' attribute.
    const conversationId = event.target.getAttribute('data-conversation-id');

    // Call the sendMessage function with the conversationId to send the message.
    sendMessage(conversationId);
  });
});

/**
 * Event listener for the Enter key press
 * This listens for a keydown event and sends a message when the Enter key is pressed inside the active chat window.
 */
document.addEventListener('keydown', function (event) {
  // Check if the pressed key is the Enter key (keyCode 13 or 'Enter' key).
  if (event.key === 'Enter') {
    // Find the currently active chat window that is displayed (its style contains 'display: block').
    const activeChatWindow = document.querySelector('.chat-window[style*="display: block;"]');

    // If an active chat window is found
    if (activeChatWindow) {
      // Get the conversation ID associated with the active chat window from its 'data-conversation-id' attribute.
      const conversationId = activeChatWindow.getAttribute('data-conversation-id');

      // If a conversation ID exists, call sendMessage with it to send the message.
      if (conversationId) {
        sendMessage(conversationId);
      }
    }
  }
});



/**
 * Function to handle sending a group message in a conversation.
 *
 * @param {string} conversationId - The ID of the conversation to send the message in.
 */
function sendGroupMessage(groupId) {
  const messageInput = document.getElementById(`group-message-input-${groupId}`);
  const messageContent = messageInput.value.trim();

  if (!messageContent) return;

  // Disable the send button temporarily
  const sendButton = document.querySelector(`button.send-button-group[data-group-id="${groupId}"]`);
  sendButton.disabled = true;

  // Emit message to the server for this group
  socket.emit('send_group_message', {
    conversation_id: groupId,
    group_id: groupId,
    sender_id: sendButton.getAttribute('data-sender-id'),
    content: messageContent
  });

  // Clear the input and re-enable the send button
  messageInput.value = '';
  sendButton.disabled = false;
}

// Add an event listener for the Enter key to send the message
document.querySelectorAll('.group-message-input').forEach(input => {
  input.addEventListener('keydown', function(event) {

      if (event.key === 'Enter') {
          event.preventDefault(); // Prevent default Enter behavior (form submission or new line)

          // Use a more robust method to extract the group ID from the input ID
          const groupId = input.id.replace('group-message-input-', '');
          sendGroupMessage(groupId); // Send the message for this group
      }
  });
});
