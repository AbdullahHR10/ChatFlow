/**
 * This script handles the functionality of loading and displaying notifications
 * when the "Notifications" link is clicked. It fetches the notifications content
 * from the server, formats timestamps, and attaches event listeners for deleting
 * notifications and marking them as read.
 */
document.addEventListener('DOMContentLoaded', function () {
  /**
     * Adds an event listener to the "Notifications" link to fetch and display the
     * notifications content in the middle bar of the page.
     * If an error occurs during the fetch, it displays an error message.
     */
  document.querySelector('a[data-tooltip="Notifications"]').addEventListener('click', function (e) {
    e.preventDefault();

    // Fetch the notifications content from the server
    fetch('/notifications')
      .then(response => {
        // Check if the response is successful
        if (!response.ok) {
          throw new Error('Failed to fetch notifications');
        }
        return response.text(); // Convert response to text (HTML content)
      })
      .then(html => {
        const middleBar = document.querySelector('.middle-bar');
        middleBar.innerHTML = html; // Insert the HTML content into the middle bar

        // Format timestamps for each notification after loading the HTML
        middleBar.querySelectorAll('#notification-timestamp').forEach(element => {
          const rawTimestamp = element.getAttribute('data-timestamp');
          element.textContent = formatTimestamp(rawTimestamp);
        });

        // Attach delete listeners to the "Delete" buttons
        attachDeleteListeners();
      })
      .catch(error => {
        // Log the error and display an error message if fetch fails
        console.error('Error loading notifications:', error);
        document.querySelector('.middle-bar').innerHTML = '<p>Error loading notifications.</p>';
      });
  });

  /**
     * Attaches click event listeners to each "Delete" button for the notifications.
     * When a "Delete" button is clicked, it sends a DELETE request to the server
     * to remove the notification.
     */
  function attachDeleteListeners () {
    const deleteButtons = document.querySelectorAll('.delete-notification');

    // Iterate over each "Delete" button and add a click listener
    deleteButtons.forEach(button => {
      button.addEventListener('click', function () {
        const notificationId = this.getAttribute('data-id');
        console.log(`Delete clicked for notification ID: ${notificationId}`);

        // Send a DELETE request to the server to remove the notification
        fetch(`/notifications/${notificationId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json'
          }
        })
          .then(response => response.json()) // Parse response as JSON
          .then(data => {
            console.log(data); // Log the server response
            if (data.success) {
              this.closest('li').remove(); // Remove the notification from the DOM
            } else {
              alert('Error deleting notification'); // Show error if deletion fails
            }
          })
          .catch(error => {
            // Log any errors and show an alert if something goes wrong
            console.error('Error:', error);
            alert('Error deleting notification');
          });
      });
    });
  }

  /**
     * Attaches event listeners to the "Mark as Read" buttons. When clicked,
     * it sends a POST request to the server to mark the notification as read.
     * If the request is successful, it updates the UI to reflect the change.
     */
  document.querySelector('.middle-bar').addEventListener('click', function (event) {
    // Check if the clicked element is a "Mark as Read" button
    if (event.target && event.target.classList.contains('mark-read')) {
      const notificationId = event.target.getAttribute('data-id');

      // Ensure notification ID is valid and present
      if (!notificationId) {
        console.error('Notification ID is missing.');
        return;
      }

      const url = `/notifications/${notificationId}/read`; // URL to mark the notification as read

      // Send POST request to mark the notification as read
      fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      })
        .then(response => {
          // Check if response is successful
          if (!response.ok) {
            return response.text().then(text => {
              throw new Error(`Error response: ${text}`);
            });
          }
          return response.json(); // Parse response as JSON if it's valid
        })
        .then(data => {
          if (data.success) {
            const notificationItem = event.target.closest('.notification-item');
            notificationItem.classList.remove('unread'); // Mark the notification as read
            event.target.remove(); // Optionally remove the "Mark as Read" button
          } else {
            console.error('Failed to mark notification as read:', data.message);
          }
        })
        .catch(error => {
          // Log any errors encountered while marking the notification as read
          console.error('Error marking notification as read:', error);
        });
    }
  });
});
