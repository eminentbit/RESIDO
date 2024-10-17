// Function to toggle password visibility
function togglePassword() {
    passwordField = document.querySelector('.password');
    let passwordType = passwordField.type
    if (passwordType === 'password') {
        passwordType = 'text';
        passwordField.type = passwordType;
    }
    else {
        passwordType = 'password';
        passwordField.type = passwordType;
    }
    this.querySelector('i').classList.toggle('fa-eye-slash');
}

toggleBtn = document.getElementById('togglePassword');
toggleBtn.addEventListener('click', togglePassword);

let email;

function showPasswordStep() {
// Hide email step and show password step
let nextBtn = document.getElementById('nextButton')
email = document.querySelector('.email');
console.log(email.value, 'ShowPassword');
document.getElementById('emailStep').style.display = 'none';
document.getElementById('passwordStep').style.display = 'block';
}

// Function to check email input and enable/disable Next button
function checkEmailInput() {
const emailInput = document.querySelector('input[name="email"]');
const nextButton = document.getElementById('nextButton');

// Enable the Next button if the email input is not empty
if (emailInput.value.trim() !== '') {
    nextButton.disabled = false;
} else {
    nextButton.disabled = true;
}
}

// Attach the input event listener to the email input
document.querySelector('input[name="email"]').addEventListener('input', checkEmailInput);
