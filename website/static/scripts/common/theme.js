/**
 * Sets the saved theme on page load.
 * This function runs when the DOM content is fully loaded. It retrieves the saved theme
 * from local storage and applies it to the document's body by updating its class.
 */
document.addEventListener('DOMContentLoaded', () => {
  // Retrieve the theme stored in localStorage
  const savedTheme = localStorage.getItem('theme');

  // If a theme is saved, reset the body's class list and apply the saved theme
  if (savedTheme) {
    document.body.className = ''; // Clear any existing classes
    document.body.classList.add(savedTheme); // Apply the saved theme
  }
});

/**
   * Handles theme changes when a theme option is clicked.
   * This function listens for clicks on elements with the class 'theme-option'.
   * When clicked, it extracts the theme from the element's 'data-theme' attribute,
   * applies it to the document's body, and stores the selected theme in local storage.
   */
document.addEventListener('click', (event) => {
  // Check if the clicked element has the 'theme-option' class
  if (event.target.classList.contains('theme-option')) {
    // Retrieve the theme name from the clicked element's data attribute
    const selectedTheme = event.target.getAttribute('data-theme');

    // Clear existing classes from the body
    document.body.className = '';

    // If a theme is selected, construct the theme class and apply it to the body
    if (selectedTheme) {
      const themeClass = `${selectedTheme}-theme`; // E.g., 'dark-theme' or 'light-theme'
      document.body.classList.add(themeClass); // Apply the new theme class
      localStorage.setItem('theme', themeClass); // Save the theme to localStorage
    }
  }
});
