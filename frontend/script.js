document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const chatStatus = document.getElementById('chatStatus');
    const loadingModal = document.getElementById('loadingModal');
    
    // Backend URL - Change this to your Render backend URL when deployed
    // For local development: "http://localhost:8000"
    // For production: "https://your-backend-app.onrender.com"
    const BACKEND_URL = "http://localhost:8000";
    
    // Example symptoms for quick testing
    const exampleSymptoms = [
        "fever and sore throat",
        "headache with dizziness",
        "stomach pain after eating",
        "chest pain and shortness of breath",
        "back pain that radiates to leg"
    ];
    
    // Initialize chat with a random example
    showExampleHint();
    
    // Event Listeners
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Auto-resize textarea
    userInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
    
    // Functions
    function showExampleHint() {
        const randomExample = exampleSymptoms[Math.floor(Math.random() * exampleSymptoms.length)];
        userInput.placeholder = `Describe your symptoms here (e.g., "I have ${randomExample}")...`;
    }
    
    async function sendMessage() {
        const message = userInput.value.trim();
        
        // Validate input
        if (!message) {
            alert("Please describe your symptoms");
            userInput.focus();
            return;
        }
        
        if (message.length > 500) {
            alert("Please keep your message under 500 characters");
            return;
        }
        
        // Disable send button and show loading
        sendButton.disabled = true;
        sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
        userInput.disabled = true;
        
        // Add user message to chat
        addMessageToChat(message, 'user');
        
        // Clear input
        userInput.value = '';
        userInput.style.height = 'auto';
        
        // Show loading modal
        loadingModal.style.display = 'flex';
        
        try {
            // Call backend API
            const response = await fetch(`${BACKEND_URL}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Add AI response to chat
            addMessageToChat(data.response, 'ai');
            
            // Update chat status
            updateChatStatus('success');
            
        } catch (error) {
            console.error('Error:', error);
            
            // Show error message
            const errorMessage = "I'm having trouble connecting to the AI service. This might be due to high demand or temporary service issues. Please try again in a moment, or contact Suwa Setha Hospital directly for medical advice.";
            addMessageToChat(errorMessage, 'ai');
            
            // Update chat status
            updateChatStatus('error');
            
            // Show example in placeholder
            showExampleHint();
        } finally {
            // Re-enable UI
            sendButton.disabled = false;
            sendButton.innerHTML = '<i class="fas fa-paper-plane"></i> Send';
            userInput.disabled = false;
            userInput.focus();
            
            // Hide loading modal
            loadingModal.style.display = 'none';
            
            // Scroll to bottom of chat
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
    
    function addMessageToChat(message, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        let headerIcon, headerText;
        
        if (sender === 'user') {
            headerIcon = '<i class="fas fa-user"></i>';
            headerText = 'You';
        } else {
            headerIcon = '<i class="fas fa-robot"></i>';
            headerText = 'AI Assistant';
        }
        
        messageDiv.innerHTML = `
            <div class="message-header">
                ${headerIcon}
                <span>${headerText}</span>
            </div>
            <div class="message-content">
                ${formatMessage(message)}
            </div>
            <div class="message-timestamp">${timestamp}</div>
        `;
        
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function formatMessage(text) {
        // Convert markdown-like formatting to HTML
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
            .replace(/\*(.*?)\*/g, '<em>$1</em>') // Italic
            .replace(/\n\n/g, '</p><p>') // Paragraphs
            .replace(/\n/g, '<br>') // Line breaks
            .replace(/•(.*?)(?=\n|$)/g, '<br>• $1') // Bullet points
            .replace(/(\d+\.\s.*?)(?=\n|$)/g, '<br>$1') // Numbered lists
            .replace(/^(.+)$/m, '<p>$1</p>'); // Wrap in paragraph
    }
    
    function updateChatStatus(status) {
        const statusIcon = chatStatus.querySelector('i');
        const statusText = chatStatus.querySelector('span') || document.createElement('span');
        
        if (status === 'success') {
            statusIcon.className = 'fas fa-circle online';
            statusIcon.style.color = '#2ecc71';
            statusText.textContent = 'AI response received';
        } else if (status === 'error') {
            statusIcon.className = 'fas fa-circle';
            statusIcon.style.color = '#e74c3c';
            statusText.textContent = 'Connection issue - using fallback response';
        } else {
            statusIcon.className = 'fas fa-circle online';
            statusIcon.style.color = '#2ecc71';
            statusText.textContent = 'Ready to assist';
        }
        
        if (!chatStatus.contains(statusText)) {
            chatStatus.appendChild(statusText);
        }
        
        // Reset status after 5 seconds
        setTimeout(() => {
            statusIcon.className = 'fas fa-circle online';
            statusIcon.style.color = '#2ecc71';
            statusText.textContent = 'Ready to assist';
        }, 5000);
    }
    
    // Add click handler for example symptoms in placeholder (for UX)
    userInput.addEventListener('focus', function() {
        this.placeholder = "Describe your symptoms in detail...";
    });
    
    userInput.addEventListener('blur', function() {
        if (!this.value) {
            showExampleHint();
        }
    });
    
    // Emergency notice
    console.log("%c⚠️ IMPORTANT SAFETY NOTICE ⚠️", "color: #e74c3c; font-size: 16px; font-weight: bold;");
    console.log("This is an academic project for educational purposes only.");
    console.log("This AI does not provide medical diagnosis or treatment.");
    console.log("In case of medical emergency, call your local emergency number.");
});
