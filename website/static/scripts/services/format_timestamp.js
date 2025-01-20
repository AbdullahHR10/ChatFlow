/**
 * Formats the given timestamp into a human-readable format, such as "Yesterday 10:30 AM" or "Mon 3:15 PM".
 *
 * @param {string} lastMessageDate - The timestamp of the message.
 * @returns {string} The formatted timestamp.
 */
function formatTimestamp (lastMessageDate) {
  const now = new Date(); // Get the current date and time
  const messageDate = new Date(lastMessageDate); // Convert the message timestamp into a Date object

  // Normalize to midnight to compare dates without the time component
  const today = new Date(now); // Clone the current date to avoid modifying it
  today.setHours(0, 0, 0, 0); // Set time to 00:00:00 for today
  const yesterday = new Date(today); // Copy today's date and subtract 1 day for yesterday
  yesterday.setDate(today.getDate() - 1); // Subtract 1 day to get yesterday's date

  // Define the array of abbreviated day names
  const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  // Check if the message was sent yesterday
  if (messageDate >= yesterday && messageDate < today) {
    const hours = messageDate.getHours() % 12 || 12; // Convert to 12-hour format
    const minutes = messageDate.getMinutes().toString().padStart(2, '0'); // Format minutes with leading zero
    const period = messageDate.getHours() >= 12 ? 'PM' : 'AM'; // Determine AM/PM
    return `Yesterday ${hours}:${minutes} ${period}`; // Return formatted date for "Yesterday"
  }

  // Calculate the difference in time between now and the message date
  const diffInMilliseconds = now - messageDate;
  const diffInMinutes = diffInMilliseconds / (1000 * 60); // Convert milliseconds to minutes
  const diffInHours = diffInMinutes / 60; // Convert minutes to hours
  const diffInDays = diffInHours / 24; // Convert hours to days

  // Format the time depending on how recent the message is
  if (diffInDays < 1) {
    // If the message was sent today, show the time in 12-hour format
    const hours = messageDate.getHours() % 12 || 12; // Convert to 12-hour format
    const minutes = messageDate.getMinutes().toString().padStart(2, '0'); // Format minutes with leading zero
    const period = messageDate.getHours() >= 12 ? 'PM' : 'AM'; // Determine AM/PM
    return `${hours}:${minutes} ${period}`; // Return formatted time for today
  } else if (diffInDays < 7) {
    // If the message was sent within the last 7 days, show the day of the week
    return dayNames[messageDate.getDay()]; // Return the abbreviated day name (e.g., "Mon")
  } else {
    // If the message is older than 7 days, show the full date (e.g., Jan 6)
    const options = { month: 'short', day: 'numeric' }; // Format as 'Jan 6'
    return messageDate.toLocaleDateString('en-US', options); // Return formatted date (e.g., "Jan 6")
  }
}

// Format the time for the chats list
document.addEventListener('DOMContentLoaded', () => {
  // Loop through each chat date element and format the timestamp
  const chatDateElements = document.querySelectorAll('.chat-date');

  chatDateElements.forEach(chatDateElement => {
    const lastMessageDate = chatDateElement.dataset.lastMessageDate;

    if (lastMessageDate) {
      // Format the last message date here using a suitable date format
      chatDateElement.textContent = formatTimestamp(lastMessageDate);
    }
  });
});
