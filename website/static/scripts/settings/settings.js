document.addEventListener('DOMContentLoaded', function () {
  // Open the settings section when settings icon is clicked
  document.getElementById('settings-icon').addEventListener('click', function (e) {
    e.preventDefault();

    fetch('/settings')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.text();
      })
      .then(html => {
        document.querySelector('.middle-bar').innerHTML = html;

        // Rebind the file input change event after loading content
        bindImagePreview();
      })
      .catch(error => {
        console.error('Error loading settings:', error);
        document.querySelector('.middle-bar').innerHTML = '<p>Error loading settings content.</p>';
      });
  });

  // Handle section navigation within settings
  document.addEventListener('click', function (e) {
    if (e.target && e.target.matches('a[data-section]')) {
      e.preventDefault();
      const section = e.target.getAttribute('data-section');

      fetch(`/settings/${section}`)
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.text();
        })
        .then(html => {
          document.querySelector('.middle-bar').innerHTML = html;

          // Rebind the file input change event after loading content
          bindImagePreview();
        })
        .catch(error => {
          console.error('Error loading section:', error);
          document.querySelector('.middle-bar').innerHTML = '<p>Error loading section content.</p>';
        });
    }
  });

  // Back to settings functionality
  document.addEventListener('click', function (e) {
    const backToSettingsButton = e.target.closest('#back-to-settings');
    if (backToSettingsButton) {
      e.preventDefault();
      console.log('Back to Settings button clicked.');

      fetch('/settings')
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          console.log('Settings content fetched successfully.');
          return response.text();
        })
        .then(html => {
          console.log('Replacing middle-bar content with settings content.');
          document.querySelector('.middle-bar').innerHTML = html;

          // Rebind the file input change event after content is loaded
          bindImagePreview();
        })
        .catch(error => {
          console.error('Error loading settings:', error);
          document.querySelector('.middle-bar').innerHTML = '<p>Error loading settings content.</p>';
        });
    }
  });
});
