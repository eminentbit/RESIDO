// Function to toggle password visibility
function togglePassword() {
    let passwordField = document.querySelector('.password');
    let passwordType = passwordField.type
    console.log('type: ', passwordType);
    console.log('testtype', passwordField['type']);
    if (passwordType === 'password') {
        passwordType = 'text';
        passwordField.type = passwordType
    }
    else {
        passwordType = 'password'
        passwordField.type = passwordType
    }
  }