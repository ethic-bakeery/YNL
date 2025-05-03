// Add typing status
document.querySelector("#id_message_send_input").addEventListener('input', function() {
    chatSocket.send(JSON.stringify({
        type: 'typing',
        username: "{{ request.user.username }}",
        is_typing: this.value.length > 0
    }));
});

// Handle incoming messages
chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const messageContainer = document.querySelector("#id_chat_item_container");
    const typingStatus = document.querySelector("#typing_status");
    
    if (data.type === 'message') {
        var div = document.createElement("div");
        div.className = (data.username === "{{ request.user.username }}") ? "chat-message right" : "chat-message left";
        div.innerHTML = `<div class="message-content">
            <span class="message-username">${data.username.charAt(0).toUpperCase() + data.username.slice(1)}</span>
            <span class="message-text">${data.message}</span>
            <span class="message-timestamp">${data.time}</span>
        </div>`;
        messageContainer.appendChild(div);
        messageContainer.scrollTop = messageContainer.scrollHeight;

    } else if (data.type === 'user_status') {
        // Handle user status updates
        console.log(`${data.username} is ${data.status}`);
        // Optionally, update the user list or status display on the page

    } else if (data.type === 'typing') {
        // Handle typing notifications
        if (data.is_typing) {
            typingStatus.textContent = `${data.username} is typing...`;
        } else {
            typingStatus.textContent = ''; // Clear typing notification
        }

    } else if (data.type === 'voice') {
        // Handle voice messages
        var div = document.createElement("div");
        div.className = (data.username === "{{ request.user.username }}") ? "chat-message right" : "chat-message left";
        div.innerHTML = `<div class="message-content">
            <span class="message-username">${data.username.charAt(0).toUpperCase() + data.username.slice(1)}</span>
            <audio controls>
                <source src="${data.voice_url}" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
            <span class="message-timestamp">${data.time}</span>
        </div>`;
        messageContainer.appendChild(div);
        messageContainer.scrollTop = messageContainer.scrollHeight;
    }
};

// Handle form submission and typing
const form = document.querySelector("#message-form");
form.addEventListener("submit", function(e) {
    e.preventDefault();
    const input = document.querySelector("#id_message_send_input");
    const message = input.value;
    chatSocket.send(JSON.stringify({
        type: 'message',
        message: message,
        username: "{{ request.user.username }}",
        time: new Date().toLocaleTimeString()
    }));
    input.value = '';
});
