/**
 * Function to select a specific group chat window and display it,
 * while hiding all other chat and group windows. 
 * Also highlights the selected group item in the list and 
 * loads the group chat history for the selected group.
 * 
 * @param {string} groupId - The ID of the selected group.
 */
function selectGroup(groupId) {
  // Select all chat windows, group windows, and group menus.
  const chatWindows = document.querySelectorAll('.chat-window');
  const groupWindows = document.querySelectorAll('.group-window');
  const groupMenus = document.querySelectorAll('.group-menu'); // Add any group-specific menu if needed
  const chatMenus = document.querySelectorAll('.chat-user-menu');

  // Hide all chat windows by default.
  chatWindows.forEach(chatWindow => {
    chatWindow.style.display = 'none';   // Hide the chat window.
    chatWindow.classList.remove('active'); // Remove 'active' class (optional, used for styling).
  });

  // Hide all group windows as we're selecting a specific group.
  groupWindows.forEach(groupWindow => {
    groupWindow.style.display = 'none';
    groupWindow.classList.remove('active');
  });


  // Deactivate all group menus.
  groupMenus.forEach(groupMenu => {
    groupMenu.classList.remove('active');
  });

    // Deactivate all chat menus.
    chatMenus.forEach(chatMenu => {
      chatMenu.classList.remove('active');
    });
  
  // Show the selected group chat window.
  const selectedGroup = document.getElementById(`group-window-${groupId}`);
  if (selectedGroup) {
    selectedGroup.style.display = 'block'; // Display the selected group window.
  } else {
    console.error(`Group window with ID ${groupId} not found`); // Log error if the group window is not found.
  }

  // Highlight the selected group item in the group list by adding 'selected' class.
  const allGroups = document.querySelectorAll('.group-item');
  allGroups.forEach(groupItem => {
    groupItem.classList.remove('selected'); // Remove 'selected' class from all group items.
  });

  // Find the group item that matches the selected group and add the 'selected' class.
  const selectedGroupItem = document.querySelector(`.group-item[onclick="selectGroup('${groupId}')"]`);
  if (selectedGroupItem) {
    selectedGroupItem.classList.add('selected'); // Add the 'selected' class to highlight the item.
  } else {
    console.error(`Group item for ${groupId} not found`); // Log error if the group item is not found.
  }
  const allChats = document.querySelectorAll('.chat-item');
  allChats.forEach(chatItem => {
    chatItem.classList.remove('selected'); // Deselect all group items.
  });
  // Optional: Load group-specific chat history.
  loadGroupChatHistory(groupId); // Function to load the group chat history, needs to be implemented.
}
