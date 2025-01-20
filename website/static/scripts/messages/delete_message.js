/**
 * Deletes a message by sending a DELETE request to the server.
 *
 * This function takes a message ID as an argument, sends a DELETE request to the server to
 * delete the message, and handles the server's response. If the deletion is successful,
 * no further action is taken. In case of an error, the error message will be logged to the console.
 *
 * @param {string} messageId - The ID of the message to be deleted.
 * @returns {void}
 */
async function deleteMessage (messageId) {
  try {
    // Send DELETE request to the server to delete the message
    const response = await fetch(`/messages/${messageId}/delete`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    // Parse the server's response
    const result = await response.json();

    // Handle any server-side message (success or error)
    if (result.error) {
      // Log error if the message deletion failed
      console.error(result.error);
    }
  } catch (error) {
    // Log any error that occurs during the fetch operation
    console.error('An error occurred while deleting the message:', error);
  }
}
