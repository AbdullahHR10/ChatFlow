/**
 * Waits for the DOM content to be loaded and then fades out alert messages after 5 seconds.
 * This function is triggered once the DOM is fully loaded.
 */
document.addEventListener('DOMContentLoaded', function () {
  // Set a delay of 5 seconds before hiding the alert messages
  setTimeout(function () {
    const alerts = document.querySelectorAll('.alert');

    // Iterate over each alert and apply fade-out effect
    alerts.forEach(function (alert) {
      fadeOutAlert(alert);
    });
  }, 5000);
});

/**
 * Fades out an alert by changing its opacity and visibility.
 * The alert will gradually fade away and then be hidden from the page.
 *
 * @param {HTMLElement} alert - The alert element to fade out.
 */
function fadeOutAlert (alert) {
  // Set the transition effect for fading the alert
  alert.style.transition = 'opacity 0.6s';

  // Set the opacity to 0 to initiate fading out
  alert.style.opacity = '0';

  // Once the transition is complete, hide the alert element
  setTimeout(function () {
    // Make the alert invisible
    alert.style.visibility = 'hidden';
    // Remove it from the layout
    alert.style.display = 'none';
  }, 600); // Delay matches the duration of the fade-out effect
}
