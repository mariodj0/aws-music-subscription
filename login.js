// Select HTML elements
const form = document.querySelector('#login-form');
const emailInput = document.querySelector('#email');
const passwordInput = document.querySelector('#password');
const errorText = document.querySelector('#error-message');

// Add event listener to the form submit event
// References: [1]
form.addEventListener('submit', async (event) => {
    event.preventDefault();

    // Get email and password values
    const email = emailInput.value;
    const password = passwordInput.value;

    // Prepare request body
    const requestBody = {
        email:email,
        password:password
    }

    // Send login request
    // References: [2]
    try {
        const response = await fetch('http://ec2-35-168-99-197.compute-1.amazonaws.com:8000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });

        // Handle response
        if (response.status === 200){
            localStorage.setItem("email", email); //[3]
            window.location.href = '/main.html'; //[4]
        }else if (response.status === 401){
            errorText.innerText = 'Email or password is invalid.';
            errorText.style.display = 'block';
        }
        else if (response.status === 404){
            errorText.innerText = 'User not found.';
            errorText.style.display = 'block';
        }
        else {
            throw new Error('An error occurred.');
        }

    } catch (error) {
        errorText.innerText = error.message;
        errorText.style.display = 'block';
    }
});

// Bibliography:
// [1] MDN Web Docs, "EventTarget.addEventListener() - Web APIs", Mozilla, 2021. [Online]. Available: https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener. [Accessed April 7, 2023].
// [2] MDN Web Docs, "Fetch API - Web APIs", Mozilla, 2021. [Online]. Available: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API. [Accessed April 7, 2023].
// [3] MDN Web Docs, "Web Storage API - Web APIs", Mozilla, 2021. [Online]. Available: https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API. [Accessed April 7, 2023].
// [4] MDN Web Docs, "Window.location - Web APIs", Mozilla, 2021. [Online]. Available: https://developer.mozilla.org/en-US/docs/Web/API/Window/location. [Accessed April 7, 2023].