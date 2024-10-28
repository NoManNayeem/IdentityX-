// static/js/scripts.js

// Function to automatically hide flash messages after a few seconds
function hideFlashMessages() {
    const flashMessages = document.querySelectorAll('.flashes li');
    flashMessages.forEach((message) => {
        setTimeout(() => {
            message.style.display = 'none';
        }, 5000); // Hide after 5 seconds
    });
}

// Function to display the recognized user details in the info card
function showUserCard(name, details) {
    const userInfoCard = document.getElementById("user-info-card");
    const userNameElement = document.getElementById("user-name");
    const userDetailsElement = document.getElementById("user-details");

    userNameElement.textContent = name;
    userDetailsElement.textContent = details;

    userInfoCard.style.display = "block"; // Show the card
    userInfoCard.classList.add("show"); // Add class for animation (if desired)

    // Hide the card after a timeout (e.g., 5 seconds)
    setTimeout(() => {
        userInfoCard.style.display = "none"; // Hide after 5 seconds
        userInfoCard.classList.remove("show"); // Remove class for animation (if desired)
    }, 5000);
}

// Add event listener to hide flash messages on window load
window.addEventListener('load', () => {
    hideFlashMessages(); // Call the function to hide flash messages
});
