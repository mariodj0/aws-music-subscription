// Get form and input elements from the DOM
const form = document.querySelector('#register-form');
const usernameInput = document.querySelector('#username');
const emailInput = document.querySelector('#email');
const passwordInput = document.querySelector('#password');
const confirmPasswordInput = document.querySelector('#confirm_password');
const errorText = document.querySelector('#error-message');

// Add event listener for form submit
form.addEventListener('submit', async (event) => {
    event.preventDefault();
    // Get input values
    const username = usernameInput.value;
    const email = emailInput.value;
    const password = passwordInput.value;
    const confirmPassword = confirmPasswordInput.value;

    // Check if passwords match
    if (password !== confirmPassword) {
        errorText.innerText = 'Passwords do not match.';
        errorText.style.display = 'block';
        return;
    }

    // Create request body object
    const requestBody = {
        username: username,
        email: email,
        password: password
    };

    try {
        // Send a request to the server to register the user
        const response = await fetch('http://ec2-35-168-99-197.compute-1.amazonaws.com:8000/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });

        if (response.status === 201) {
            errorText.innerText = 'Registration successful.';
            errorText.style.color = 'green';
            errorText.style.display = 'block';
            setTimeout(() => {
                window.location.href = '/index.html';
            }, 3000);
        } else if(response.status === 409) {
            throw new Error('User already exists.');
        } else {
            throw new Error('An error occurred.');
        }
    } catch (error) {
        errorText.innerText = error.message;
        errorText.style.color = 'red';
        errorText.style.display = 'block';
    }
});
