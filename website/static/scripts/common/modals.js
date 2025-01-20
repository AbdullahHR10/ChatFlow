/**
 * Opens the "Create Group" modal.
 */
function openCreateGroupModal () {
  const groupModal = document.getElementById('create-group-modal');
  if (groupModal) {
    groupModal.style.display = 'block'; // Display the create group modal
  } else {
    console.error('Group modal element not found.'); // Log an error if the modal is not found
  }
}

/**
 * Closes the "Create Group" modal.
 */
function closeCreateGroupModal () {
  const groupModal = document.getElementById('create-group-modal');
  if (groupModal) {
    groupModal.style.display = 'none'; // Hide the create group modal
  } else {
    console.error('Group modal element not found.'); // Log an error if the modal is not found
  }
}

/**
 * Opens the "Create Chat" modal and initializes the loading of friends.
 */
function openCreateChatModal () {
  const chatModal = document.getElementById('create-chat-modal');
  if (chatModal) {
    chatModal.style.display = 'block'; // Display the create chat modal
    loadFriends(); // Load the list of friends when the modal is opened.
  } else {
    console.error('Chat modal element not found.'); // Log an error if the modal is not found
  }
}

/**
 * Closes a modal based on the given modal ID.
 * @param {string} modalId - The ID of the modal to be closed.
 */
function closeCreateChatModal (modalId) {
  const chatModal = document.getElementById(modalId);
  if (chatModal) {
    chatModal.style.display = 'none'; // Hide the create chat modal
  } else {
    console.error('Chat modal element not found.'); // Log an error if the modal is not found
  }
}

/**
 * Closes any modal when clicking outside of it.
 * This function listens for clicks on the window and checks if the clicked element has the 'modal' class.
 * If so, it hides the modal by setting its display property to 'none'.
 */
window.onclick = function (event) {
  if (event.target.classList.contains('modal')) {
    event.target.style.display = 'none'; // Hide the modal
  }
};

// Set the group ID when opening the modal
function openAddMembersModal(groupId) {
  const modal = document.getElementById('add-members-modal');
  modal.setAttribute('data-group-id', groupId); // Set the group ID dynamically
  modal.style.display = 'block'; // Open the modal
  loadFriendsForGroup();
}

// Closes the modal
function closeAddMembersModal() {
  document.getElementById('add-members-modal').style.display = 'none';
}