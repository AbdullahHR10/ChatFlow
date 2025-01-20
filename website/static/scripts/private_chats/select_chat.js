/**
 * Function to select a specific chat window and display it, 
 * while hiding all other chat and group windows. 
 * Also highlights the selected chat item in the list and 
 * loads the chat history for the selected chat.
 * 
 * @param {string} chatId - The ID of the selected chat.
 */
function selectChat(chatId) {
  // Select all chat windows, group windows, and chat menus.
  const chatWindows = document.querySelectorAll('.chat-window');
  const groupWindows = document.querySelectorAll('.group-window');
  const chatMenus = document.querySelectorAll('.chat-user-menu');
  const groupMenus = document.querySelectorAll('.group-menu');

  // Hide all chat windows by default.
  chatWindows.forEach(chatWindow => {
    chatWindow.style.display = 'none';   // Hide the chat window.
    chatWindow.classList.remove('active'); // Remove 'active' class (optional, used for styling).
  });

  // Hide all group windows as we're selecting a specific chat.
  groupWindows.forEach(groupWindow => {
    groupWindow.style.display = 'none';
  });

  // Deactivate all chat menus.
  chatMenus.forEach(chatMenu => {
    chatMenu.classList.remove('active');
  });

  // Deactivate all group menus.
  groupMenus.forEach((groupMenu =>
    groupMenu.classList.remove('active')
  ))

  // Show the selected chat window.
  const selectedChat = document.getElementById(`chat-window-${chatId}`);
  if (selectedChat) {
    selectedChat.style.display = 'block'; // Display the selected chat window.
  } else {
    console.error(`Chat window with ID ${chatId} not found`); // Log error if the chat window is not found.
  }

  // Highlight the selected chat item in the chat list by adding 'selected' class.
  const allChats = document.querySelectorAll('.chat-item');
  allChats.forEach(chatItem => {
    chatItem.classList.remove('selected'); // Remove 'selected' class from all chat items.
  });

  // Find the chat item that matches the selected chat and add the 'selected' class.
  const selectedChatItem = document.querySelector(`.chat-item[onclick="selectChat('${chatId}')"]`);
  if (selectedChatItem) {
    selectedChatItem.classList.add('selected'); // Add the 'selected' class to highlight the item.
  } else {
    console.error(`Chat item for ${chatId} not found`); // Log error if the chat item is not found.
  }

  // Optionally, deselect group items (if needed).
  const allGroups = document.querySelectorAll('.group-item');
  allGroups.forEach(groupItem => {
    groupItem.classList.remove('selected'); // Deselect all group items.
  });

  // Load the chat history for the selected chat.
  loadChatHistory(chatId); // Function to load the chat history, needs to be implemented.
}
