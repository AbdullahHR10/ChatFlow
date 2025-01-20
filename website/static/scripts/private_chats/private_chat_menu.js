document.addEventListener('DOMContentLoaded', function () {
  /**
   * Opens the chat user menu when the settings icon is clicked.
   *
   * @listens click
   *
   * When a user clicks on the chat settings icon, this function retrieves the
   * associated chat window and user menu by their unique chat ID. It then adds
   * the 'active' class to both the chat window and the user menu to display them.
   */
  document.querySelectorAll('.chat-settings').forEach(function (settingsIcon) {
    settingsIcon.addEventListener('click', function (event) {
      event.preventDefault(); // Prevent default behavior of the link

      // Extract the chatId from the clicked settings icon's ID
      const chatId = this.id.replace('chat-settings-', '');
      const chatWindow = document.getElementById('chat-window-' + chatId); // Find the associated chat window
      const chatUserMenu = document.querySelector('.chat-user-menu[data-conversation-id="' + chatId + '"]'); // Find the associated user menu

      // Ensure both the chat window and user menu are found
      if (chatWindow && chatUserMenu) {
        // Add 'active' class to show the chat user menu and shrink the chat window
        chatWindow.classList.add('active'); // Shrink chat window
        chatUserMenu.classList.add('active'); // Show user menu
      }
    });
  });

  /**
   * Closes the chat user menu when the close icon is clicked.
   *
   * @listens click
   *
   * When a user clicks on the close icon in the user menu, this function retrieves
   * the associated chat window and user menu by their unique chat ID. It then removes
   * the 'active' class from both elements to hide the user menu and restore the chat window size.
   */
  document.querySelectorAll('.chat-user-menu-icon').forEach(function (closeIcon) {
    closeIcon.addEventListener('click', function (event) {
      // Get the chatId of the conversation this user menu belongs to
      const chatId = this.closest('.chat-user-menu').getAttribute('data-conversation-id');
      const chatWindow = document.getElementById('chat-window-' + chatId); // Find the associated chat window
      const chatUserMenu = document.querySelector('.chat-user-menu[data-conversation-id="' + chatId + '"]'); // Find the associated user menu

      // Ensure both the chat window and user menu are found
      if (chatUserMenu && chatWindow) {
        // Remove 'active' class to close the user menu and restore the chat window
        chatUserMenu.classList.remove('active'); // Hide user menu
        chatWindow.classList.remove('active'); // Restore chat window size
      }
    });
  });
});

document.addEventListener('DOMContentLoaded', function () {
  /**
   * Opens the group menu when the settings icon is clicked.
   *
   * @listens click
   *
   * When a user clicks on the group settings icon, this function retrieves the
   * associated group window and menu by their unique group ID. It then adds
   * the 'active' class to both the group window and the group menu to display them.
   */
  document.querySelectorAll('.group-settings').forEach(function (settingsIcon) {
    settingsIcon.addEventListener('click', function (event) {
      event.preventDefault(); // Prevent default behavior of the link

      // Extract the groupId from the clicked settings icon's ID
      const groupId = this.id.replace('group-settings-', '');
      const groupWindow = document.getElementById('group-window-' + groupId); // Find the associated group window
      const groupMenu = document.querySelector('.group-menu[data-conversation-id="' + groupId + '"]'); // Find the associated group menu

      // Ensure both the group window and group menu are found
      if (groupWindow && groupMenu) {
        // Add 'active' class to show the group menu and shrink the group window
        groupWindow.classList.add('active'); // Shrink group window
        groupMenu.classList.add('active'); // Show group menu
      } else {
        console.error("Group window or menu not found:", groupId);
      }
    });
  });

  /**
   * Closes the group menu when the close icon is clicked.
   *
   * @listens click
   *
   * When a user clicks on the close icon in the group menu, this function retrieves
   * the associated group window and menu by their unique group ID. It then removes
   * the 'active' class from both elements to hide the group menu and restore the group window size.
   */
  document.querySelectorAll('.group-menu-icon').forEach(function (closeIcon) {
    closeIcon.addEventListener('click', function (event) {
      // Get the groupId of the conversation this group menu belongs to
      const groupId = this.closest('.group-menu').getAttribute('data-conversation-id');
      const groupWindow = document.getElementById('group-window-' + groupId); // Find the associated group window
      const groupMenu = document.querySelector('.group-menu[data-conversation-id="' + groupId + '"]'); // Find the associated group menu

      // Ensure both the group window and group menu are found
      if (groupMenu && groupWindow) {
        // Remove 'active' class to close the group menu and restore the group window
        groupMenu.classList.remove('active'); // Hide group menu
        groupWindow.classList.remove('active'); // Restore group window size
      } else {
        console.error("Group window or menu not found:", groupId);
      }
    });
  });
});
