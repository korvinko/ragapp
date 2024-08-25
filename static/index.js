const endpointURL = "http://localhost:8000/ask"

function sendQuery() {
    const queryText = document.getElementById('query').value;

    // Add user message to the dialog
    const dialog = document.getElementById('dialog');
    const userMessage = document.createElement('div');
    userMessage.classList.add('message', 'user-message');
    userMessage.innerText = queryText;
    dialog.appendChild(userMessage);
    dialog.scrollTop = dialog.scrollHeight;  // Auto-scroll to the latest message

    // Clear input field
    document.getElementById('query').value = '';

    // Send the query to the server
    fetch(endpointURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: queryText })
    })
        .then(response => response.json())
        .then(data => {
            const botMessage = document.createElement('div');
            botMessage.classList.add('message', 'bot-message');

            // Render the result as Markdown
            botMessage.innerHTML = marked.parse(data.answer.result);
            dialog.appendChild(botMessage);

            // Ensure the dialog scrolls to the bottom
            setTimeout(() => {
                dialog.scrollTop = dialog.scrollHeight;
            }, 1000);
        })
        .catch(error => {
            const botMessage = document.createElement('div');
            botMessage.classList.add('message', 'bot-message');
            botMessage.innerText = 'Error: ' + error;
            dialog.appendChild(botMessage);
            // Ensure the dialog scrolls to the bottom
            setTimeout(() => {
                dialog.scrollTop = dialog.scrollHeight;
            }, 1000);
        });
}

// Add event listener for Ctrl + Enter
document.getElementById('query').addEventListener('keydown', function (event) {
    if (event.ctrlKey && event.key === 'Enter') {
        sendQuery();
    }
});