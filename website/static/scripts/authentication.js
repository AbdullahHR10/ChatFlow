// Get references to the login and signup sections of the page
const loginSection = document.getElementById('login-section');
const signupSection = document.getElementById('signup-section');

// Get references to the buttons that switch between login and signup views
const switchToSignup = document.getElementById('switch-to-signup');
const switchToLogin = document.getElementById('switch-to-login');

/**
 * Event listener to switch to the signup section.
 * Hides the login section and displays the signup section when the
 * "switch-to-signup" button is clicked.
 */
switchToSignup.addEventListener('click', (event) => {
  event.preventDefault(); // Prevents the default link behavior
  loginSection.style.display = 'none'; // Hide the login section
  signupSection.style.display = 'flex'; // Show the signup section
});

/**
 * Event listener to switch to the login section.
 * Hides the signup section and displays the login section when the
 * "switch-to-login" button is clicked.
 */
switchToLogin.addEventListener('click', (event) => {
  event.preventDefault(); // Prevents the default link behavior
  signupSection.style.display = 'none'; // Hide the signup section
  loginSection.style.display = 'flex'; // Show the login section
});
