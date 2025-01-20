/**
 * Loads the list of friends from the server and displays their profile pictures and names.
 * If no friends are found, a message will be displayed indicating that the user has no friends.
 * In case of an error during the fetch, an error message will be shown.
 *
 * @returns {void}
 */
function loadFriends () {
  fetch('/api/friends')
    .then(response => {
      if (response.ok) {
        return response.json(); // Parse response as JSON
      } else {
        return response.text().then(text => { // Parse error response as text
          throw new Error('Server error: ' + text);
        });
      }
    })
    .then(data => {
      const friendListContainer = document.getElementById('friend-list-container');
      friendListContainer.innerHTML = ''; // Clear previous content

      if (data.friends && data.friends.length > 0) {
        // Loop through each friend and create a button
        data.friends.forEach(friend => {
          const friendButton = document.createElement('button');
          friendButton.classList.add('friend-button');

          // Create the profile picture image
          const profilePic = document.createElement('img');
          profilePic.classList.add('modal-friend-pfp');

          // Check if the friend has a valid profile picture
          if (friend.profile_picture) {
            profilePic.src = `${friend.profile_picture}`; // Adjust path as needed
          } else {
            profilePic.src = '/static/default_profile_picture.png'; // Fallback image
          }

          profilePic.alt = `${friend.name}'s profile picture`;

          // Create the friend's name text
          const friendName = document.createElement('h3');
          friendName.textContent = friend.name;
          friendName.classList.add('modal-friend-name');

          // Append profile picture and name to the button
          friendButton.appendChild(profilePic);
          friendButton.appendChild(friendName);

          // Add a click event to start a chat with this friend
          friendButton.onclick = function () {
            createChat(friend.id); // Use friend's ID to create chat
          };

          // Append the button to the friend list container
          friendListContainer.appendChild(friendButton);
        });
      } else {
        // If all friends are added, show a message indicating the user can start chatting
        friendListContainer.innerHTML = '<p>You have added all your friends. You can now start chatting!</p>';
      }
    })
    .catch(error => {
      console.error('Error loading friends:', error);
      const friendListContainer = document.getElementById('friend-list-container');
      friendListContainer.innerHTML = '<p>You have no friends yet.</p>';
    });
}
