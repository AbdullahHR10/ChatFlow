/**
 * Fetches the current user's ID from the server and stores it in the `currentUserId` variable.
 * If the fetch request fails, an error message is logged in the console.
 *
 * @returns {void}
 */
let currentUserId = null;

// Fetch the current user ID from the server
fetch('/api/current_user_id')
  .then(response => {
    if (!response.ok) {
      // If the response is not successful, throw an error
      throw new Error('Failed to fetch current user ID');
    }
    // Parse the JSON response body
    return response.json();
  })
  .then(data => {
    // Assign the current user's ID from the response data to the `currentUserId` variable
    currentUserId = data.user_id;
  })
  .catch(error => {
    // If an error occurs during the fetch, log it to the console
    console.error('Error fetching current user ID:', error);
  });
