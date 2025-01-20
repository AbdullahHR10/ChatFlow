/**
 * Marks a message as read by emitting a 'mark_message_read' event through the socket.
 *
 * This function is triggered when a message is marked as read by the user.
 * It sends the message ID to the server via a Socket.IO event to update its status in the backend.
 *
 * @param {number} messageId - The unique identifier of the message to be marked as read.
 */
function markMessageAsRead (messageId) {
  // Emit the 'mark_message_read' event with the message ID to notify the server
  socket.emit('mark_message_read', { message_id: messageId });
}
