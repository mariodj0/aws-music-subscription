// Event listener for when the DOM has been loaded
document.addEventListener('DOMContentLoaded', async () => {
    // URL with endpoint for user_details
    const userDetailUrl = 'http://ec2-35-168-99-197.compute-1.amazonaws.com:8000/user_details';

    // Get the user's email from localStorage
    const userEmail = localStorage.getItem('email');

    try {
        // Fetch user details from the server
        const response = await fetch(userDetailUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email: userEmail })
        });
        const data = await response.json();

        // Populate user_name
        const userNameElement = document.getElementById('user-name');
        userNameElement.textContent += data.user_name;

        // Populate subscribed music
        const subscriptionList = document.getElementById('subscription-list');
        data.music_details.forEach(music => {
            // Create and configure elements for each music item
            const li = document.createElement('li');
            li.className = 'subscription-item';

            const img = document.createElement('img');
            img.src = music.img_url;

            const div = document.createElement('div');
            div.className = 'subscription-info';
            div.innerHTML = `<strong>Title:</strong> ${music.title}<br>
                            <strong>Artist:</strong> ${music.artist}<br>
                            <strong>Year:</strong> ${music.year}`;

            const removeBtn = document.createElement('button');
            removeBtn.className = 'remove-btn';
            removeBtn.textContent = 'Remove';

            // Add event listener for remove button
            removeBtn.addEventListener('click', async () => {
                // remove logic
                await removeSubscription(userEmail, music.title)
            });

            li.appendChild(img);
            li.appendChild(div);
            li.appendChild(removeBtn);

            subscriptionList.appendChild(li);
        });
    } catch (error) {
        console.error('Error fetching user details:', error);
    }
});

// Function to remove a subscription
async function removeSubscription(email, title) {
    try {
        const requestBody = {
            email: email,
            title: title
        };

        const response = await fetch('http://ec2-35-168-99-197.compute-1.amazonaws.com:8000/remove_subscription', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });

        if (response.status === 200) {
            // Subscription successfully removed
            alert('Subscription removed successfully.');
            location.reload();
        } else {
            throw new Error('An error occurred while removing the subscription.');
        }
    } catch (error) {
        alert(error.message);
    }
}

// Event listener for query button click
document.getElementById('query-btn').addEventListener('click', async (event) => {
    event.preventDefault();

    // Get query values from input elements
    const title = document.getElementById('title').value;
    const year = document.getElementById('year').value;
    const artist = document.getElementById('artist').value;
    //  Send query to the server
    const response = await fetch('http://ec2-35-168-99-197.compute-1.amazonaws.com:8000/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            title: title,
            year: year,
            artist: artist,
        }),
    });

    const data = await response.json();
    const queryResults = document.getElementById('queryResults');
    queryResults.innerHTML = '';
    if (data.results.length === 0){
        queryResults.innerHTML = '<h2 style="color: red">No result is retrieved. Please query again</h2>'
    }else{
    data.results.forEach((result) => {
        // Create and configure elements for each result item
        const resultDiv = document.createElement('div');
        resultDiv.classList.add('result-item');

        const resultTitle = document.createElement('h3');
        resultTitle.textContent = `${result.title} (${result.year})`;
        resultDiv.appendChild(resultTitle);

        const resultArtist = document.createElement('p');
        resultArtist.textContent = result.artist;
        resultDiv.appendChild(resultArtist);

        const resultImg = document.createElement('img');
        resultImg.src = result.img_url;
        resultImg.alt = `${result.artist} image`;
        resultDiv.appendChild(resultImg);

        const subscribeButton = document.createElement('button');
        subscribeButton.textContent = 'Subscribe';
        subscribeButton.classList.add('subscribe-button');

        subscribeButton.classList.add('subscribe-button');
        subscribeButton.textContent = 'Subscribe';
        subscribeButton.setAttribute('data-title', result.title);
        resultDiv.appendChild(subscribeButton);

        queryResults.appendChild(resultDiv);
    });}
});

// Event listener for subscribe button click
document.addEventListener('click', async (event) => {
    if (event.target && event.target.classList.contains('subscribe-button')) {
        const title = event.target.getAttribute('data-title');
        const email = localStorage.getItem('email');

        // Send a request to the server to add the subscription
        const response = await fetch('http://ec2-35-168-99-197.compute-1.amazonaws.com:8000/add_subscription', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, title })
        });

        const data = await response.json();

        if (response.ok) {
            alert(data.message);
            location.reload()
        } else {
            alert(`Error: ${data.message}`);
        }
    }
});
