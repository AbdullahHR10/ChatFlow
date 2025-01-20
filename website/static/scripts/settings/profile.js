function enableEditing (fieldId, fieldName) {
  const field = document.getElementById(fieldId);
  field.setAttribute('contenteditable', 'true');
  field.focus();
  const range = document.createRange();
  const sel = window.getSelection();
  range.selectNodeContents(field);
  range.collapse(false);
  sel.removeAllRanges();
  sel.addRange(range);
  field.addEventListener('blur', () => {
    const newValue = field.innerText.trim();
    if (!newValue) {
      alert(`${fieldName} cannot be empty!`);
      field.innerText = '{{ user.' + fieldName + ' }}';
    } else {
      updateField(fieldName, newValue);
    }
    field.removeAttribute('contenteditable');
  }, { once: true });
}

function updateField (fieldName, newValue) {
  // Check if newValue is empty or 'None' and set to null
  if (newValue === '' || newValue.toLowerCase() === 'none') {
    newValue = null;
  }

  fetch('/update_profile', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ field: fieldName, value: newValue })
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        console.log(`${fieldName} updated successfully.`);
      } else {
        alert(`Error updating ${fieldName}: ${data.message}`);
      }
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

const form = document.getElementById('upload-form');
form.addEventListener('submit', function (event) {
  event.preventDefault();
  const formData = new FormData(form);

  fetch('/upload_profile_picture', {
    method: 'POST',
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert('File uploaded successfully');
        // Update the image preview
        const imagePreview = document.getElementById('image-preview');
        imagePreview.src = '/static/profile_pics/' + data.filename; // Assuming filename is returned
        imagePreview.style.display = 'block'; // Show the image preview
      } else {
        alert('Error: ' + data.message);
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('An error occurred while uploading the file');
    });
});

function openModal () {
  const modal = document.getElementById('modal');
  if (modal) {
    modal.style.display = 'block'; // Open modal by setting the display to block
  } else {
    console.error('Modal not found!');
  }
}

function closeModal () {
  const modal = document.getElementById('modal');
  if (modal) {
    modal.style.display = 'none'; // Close modal by setting the display to none
  } else {
    console.error('Modal not found!');
  }
}

function bindImagePreview () {
  const fileInput = document.getElementById('file-input');
  const imagePreview = document.getElementById('image-preview');

  if (fileInput) {
    fileInput.addEventListener('change', function (event) {
      const file = event.target.files[0];
      const reader = new FileReader();

      reader.onload = function (e) {
        imagePreview.src = e.target.result;
        imagePreview.style.display = 'block';
      };

      reader.readAsDataURL(file);
    });
  }
}
// Function to toggle the edit input visibility
function toggleEdit (pElementId, inputElementId) {
  const pElement = document.getElementById(pElementId);
  const inputElement = document.getElementById(inputElementId);

  // If the input is hidden, show it, otherwise hide it
  if (inputElement.style.display === 'none') {
    pElement.style.display = 'none'; // Hide <p> text
    inputElement.style.display = 'block'; // Show <input> field
    inputElement.focus(); // Focus the input field
  } else {
    inputElement.style.display = 'none'; // Hide <input> field
    pElement.style.display = 'block'; // Show <p> text
  }
}

// Close input field if clicking outside the editable container
document.addEventListener('click', function (event) {
  const editableContainer = document.getElementById('editable-container');
  const inputField = editableContainer.querySelector('input[type="date"]');
  const pElement = editableContainer.querySelector('p');

  // Check if the click happened outside the editable container and if the input is visible
  if (!editableContainer.contains(event.target) && inputField.style.display === 'block') {
    inputField.style.display = 'none'; // Hide input field
    pElement.style.display = 'block'; // Show <p> text
  }
});

// Function to save updated field (could be extended to API call)
function saveUpdatedField (fieldName) {
  const inputElement = document.getElementById('edit-birthdate');
  const newValue = inputElement.value;
  updateField(fieldName, newValue);
}
