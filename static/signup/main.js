document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent default form submission

    // Retrieve form data elements
    let fName = document.getElementById('first_name');
    let lName = document.getElementById('last_name');
    let email = document.getElementById('email');
    let password = document.getElementById('password');
    let re_password = document.getElementById('re_password');
    let isRealtor = document.getElementById('is_realtor');

    // Create the formData object with actual values
    const formData = {
        first_name: fName.value, // Extracting values directly
        last_name: lName.value,
        email: email.value,
        password: password.value,
        re_password: re_password.value,
        is_realtor: isRealtor.value
    };


    // Get the CSRF token from the hidden input field
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Send the POST request to the API
    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken // Use the correct token
        },
        body: JSON.stringify(formData)  // Convert formData object to JSON string
    })
    .then(response => {
        // Log the response for debugging
        console.log("Response Status:", response.status);
        // Check if the response is okay (status code 200-299)
        if (!response.ok) {
            return response.json().then(err => {
                console.log("Error Response:", err); // Log the error response
                const messageDiv = document.querySelector('.error-message');
                messageDiv.innerHTML = `<p>${err.error || "An unknown error occurred."}</p>`;
                throw new Error('Network response was not ok');
            });
        }
        return response.json();  // Ensure we parse response as JSON
    })
    .then(data => {
        // Log the parsed data for debugging
        console.log("Parsed Data:", data);
        // Check if data is defined before accessing properties
        if (data && data.success) {
            // If registration is successful, redirect
            window.location.href = '/location/';
        } else {
            // Display error message on the same page
            const messageDiv = document.querySelector('.error-message');
            messageDiv.innerHTML = `<p>${data.error || "An error occurred."}</p>`;
        }
    })
    .catch(error => {
        // Display generic error message without showing API page
        console.error('There was a problem with the fetch operation:', error);
        document.getElementById('response-message').innerHTML = `<p>${error.message}</p>`;
    });
});