document.addEventListener('DOMContentLoaded', function () {
  // Select all the checkboxes with the 'switch' class
  document.querySelectorAll('.switch input').forEach(function (toggle) {
      toggle.addEventListener('change', function () {
          const settingName = toggle.closest('.privacy').classList[0]; // Get the setting name (e.g., 'friend')
          const settingValue = toggle.checked;  // Get the value as true or false based on checked state

          // Send the data to the backend using fetch
          const formData = new FormData();
          formData.append(settingName, settingValue); // Append the setting name and its value (true/false)

          fetch('/update-privacy-settings', {
              method: 'POST',
              body: formData,
          })
          .then(response => response.json())
          .then(data => {
              if (data.success) {
                  console.log('Privacy setting updated successfully!');
              } else {
                  console.error('Failed to update privacy setting');
              }
          })
          .catch(error => console.error('Error:', error));
      });
  });
});
