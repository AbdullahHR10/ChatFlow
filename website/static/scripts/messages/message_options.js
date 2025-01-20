/**
 * Handles the message options dropdown for showing and hiding settings.
 *
 * Listens for click events to toggle the visibility of the message options dropdown menu.
 * If the user clicks outside the dropdown, it will close any open dropdown menus.
 */
document.addEventListener('click', function (event) {
  const isSettingsBtn = event.target.closest('.message-settings-btn');
  const messageOptions = event.target.closest('.message-options');

  // Toggle the active class to show/hide the dropdown menu when clicking on the settings button
  if (isSettingsBtn) {
    messageOptions.classList.toggle('active');
  } else {
    // Close the dropdown if clicking outside of the message options menu
    document.querySelectorAll('.message-options').forEach(option => {
      option.classList.remove('active');
    });
  }
});

/**
* Handles the delete option for messages.
*
* This function listens for the 'delete' option click event, retrieves the message ID,
* and triggers the deletion of the message.
*
* @param {Event} event - The click event triggered by the user selecting the delete option.
*/
document.addEventListener('click', function (event) {
  const deleteOption = event.target.closest('.delete-option');

  // If delete option is clicked, delete the message
  if (deleteOption) {
    const messageId = deleteOption.closest('.message').dataset.messageId;
    console.log('Delete message:', messageId); // Log the message ID (optional for debugging)
    deleteMessage(messageId); // Call the function to delete the message
  }
});

/**
* Ensures that the settings button for each message can toggle the visibility of the options menu.
*
* When clicked, it prevents event bubbling to the parent message and toggles the visibility of
* the dropdown menu for settings. The visibility of the menu is toggled between 'block' and 'none'.
*/
document.querySelectorAll('.message-settings-btn').forEach(btn => {
  btn.addEventListener('click', function (e) {
    e.stopPropagation(); // Prevent click from bubbling to the parent message

    const messageOptions = this.closest('.message-options');
    const menu = messageOptions.querySelector('.message-settings-menu');

    // Debugging: Check if the menu exists (remove in production)
    console.log('Clicked on settings button, menu:', menu);

    // Toggle the visibility of the settings menu
    menu.style.display = menu.style.display === 'block' ? 'none' : 'block';

    // Add active class to show the dropdown menu
    messageOptions.classList.toggle('active');
  });
});

/**
* Closes the settings menu if a click is detected outside of the active menu.
*
* This function listens for any click events outside the active message options menu
* and closes the menu if the user clicks outside of it.
*/
document.addEventListener('click', function (e) {
  const activeMenu = document.querySelector('.message-options.active');

  // If there is an active menu and the click is outside, close the menu
  if (activeMenu && !activeMenu.contains(e.target)) {
    activeMenu.classList.remove('active');
    activeMenu.querySelector('.message-settings-menu').style.display = 'none';
  }
});
