/**
 * This script handles the functionality of loading and displaying the
 * friend list content in the middle bar when the 'Friends' link is clicked.
 * It fetches the content from the server and injects it into the page.
 * In case of an error during the fetch, an error message is displayed.
 */
document.addEventListener('DOMContentLoaded', function () {
  // Add event listener for the 'Friends' link to load friend list content
  document.querySelector('a[data-tooltip="Friends"]').addEventListener('click', function (e) {
    e.preventDefault();

    // Fetch the friend list content from the server
    fetch('/friends')
      .then(response => {
        // Check if the response is successful
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.text();
      })
      .then(html => {
        // Inject the loaded HTML into the middle bar
        document.querySelector('.middle-bar').innerHTML = html;
      })
      .catch(error => {
        // Log error and display error message if the request fails
        console.error('Error loading friend list:', error);
        document.querySelector('.middle-bar').innerHTML = '<p>Error loading friend list content.</p>';
      });
  });
});
