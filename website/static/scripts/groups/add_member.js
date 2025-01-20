// Reuse loadFriends to populate group member selection
function loadFriendsForGroup() {
  fetch('/api/friends?exclude_chats=false')
    .then(response => response.json())
    .then(data => {
      const memberSelectionContainer = document.getElementById('member-selection-container');
      memberSelectionContainer.innerHTML = ''; // Clear any previous content

      if (data.friends && data.friends.length > 0) {
        data.friends.forEach(friend => {
          // Create a button for each friend
          const memberButton = document.createElement('button');
          memberButton.classList.add('member-button');
          memberButton.dataset.userId = friend.id;

          // Add profile picture and name
          const profilePic = document.createElement('img');
          profilePic.src = friend.profile_picture || '/static/default_profile_picture.png';
          profilePic.alt = `${friend.name}'s profile picture`;

          const memberName = document.createElement('span');
          memberName.textContent = friend.name;

          // Append children to the button
          memberButton.appendChild(profilePic);
          memberButton.appendChild(memberName);

          // Toggle selection on click
          memberButton.addEventListener('click', function () {
            memberButton.classList.toggle('selected');
          });

          // Add to the container
          memberSelectionContainer.appendChild(memberButton);
        });
      } else {
        memberSelectionContainer.innerHTML = '<p>No friends available to add to the group.</p>';
      }
    })
    .catch(error => {
      console.error('Error loading friends:', error);
      const memberSelectionContainer = document.getElementById('member-selection-container');
      memberSelectionContainer.innerHTML = '<p>Error loading friends.</p>';
    });
}

// Confirms the selected members and sends them to the server
function confirmAddMembers() {
  const modal = document.getElementById('add-members-modal');
  const groupId = modal.getAttribute('data-group-id'); // Get the group ID from the modal

  const selectedMembers = Array.from(document.querySelectorAll('.member-button.selected'))
    .map(button => button.dataset.userId);

  if (selectedMembers.length === 0) {
    return; // Prevent further action if no members are selected
  }

  fetch(`/group/${groupId}/add_member`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ members: selectedMembers }),
  })
    .then(response => response.json())
    .then(data => {
      if (data.message) {
        closeAddMembersModal();
        location.reload(); // Reload the page to reflect the changes
      }
    })
    .catch(error => {
      console.error('Error adding members:', error);
      location.reload(); // Reload the page in case of an error as well
    });
}


// Event listeners for buttons
document.getElementById('confirm-add-members').addEventListener('click', confirmAddMembers);
document.getElementById('close-add-members').addEventListener('click', closeAddMembersModal);


// Function to kick a member from the group
function kickMember(groupId, memberId) {
  const data = {
      member_id: memberId
  };

  // Make a POST request to kick the member
  fetch(`/group/${groupId}/kick_member`, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(data => {
      if (data.message) {
          const memberElement = document.getElementById(`member-${memberId}`);
          if (memberElement) {
              memberElement.remove();
          }
        location.reload();
      } else if (data.error) {
          // Show an error message if there is an issue
          alert(data.error);  // Replace with custom error UI feedback if needed
      }
  })
  .catch(error => {
      // Handle any fetch errors
      alert('An unexpected error occurred. Please try again later.');
  });
}


function leaveGroup(groupId) {
  // Send a request to the server to leave the group
  fetch(`/group/${groupId}/leave`, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
  })
  .then(response => response.json())
  .then(data => {
      if (data.message) {
          location.reload();
      } else if (data.error) {
          alert(data.error);  // Handle errors
      }
  })
  .catch(error => {
      console.error('Error leaving group:', error);
  });
}

