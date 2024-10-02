// Function to toggle password visibility
function togglePassword() {
    const passwordField = document.querySelector('input[type="password"]');
    if (passwordField === 'password') {
        passwordField = 'text';
    }
    else if (passwordField === 'text') {
        passwordField = 'password';
    }
  }