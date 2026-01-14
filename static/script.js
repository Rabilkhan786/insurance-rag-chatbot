document.addEventListener('DOMContentLoaded', () => {
    // --- DOM ELEMENTS ---
    const chatForm = document.getElementById('chatForm');
    const userInput = document.getElementById('userInput');
    const messagesContainer = document.getElementById('messagesContainer');
    const typingIndicator = document.getElementById('typingIndicator');
    const sendBtn = document.querySelector('.send-btn');
    const micBtn = document.querySelector('.mic-btn'); 
    const chatArea = document.getElementById('chatArea');

    // --- STATE MANAGEMENT ---
    let isProcessing = false;
    let sessionId = localStorage.getItem('session_id') || generateUUID();
    
    // Save session ID if new
    if (!localStorage.getItem('session_id')) {
        localStorage.setItem('session_id', sessionId);
    }

    // --- SPEECH RECOGNITION SETUP ---
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;

    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false; 
        recognition.lang = 'en-US';
        recognition.interimResults = false;

        // 1. When speech starts
        recognition.onstart = () => {
            micBtn.classList.add('recording'); 
            micBtn.style.color = '#ef4444'; 
            userInput.placeholder = "Listening...";
        };

        // 2. When speech ends
        recognition.onend = () => {
            micBtn.classList.remove('recording');
            micBtn.style.color = ''; 
            userInput.placeholder = "Type your question here...";
        };

        // 3. When text is captured
        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            userInput.value = transcript;
            
            // Trigger auto-resize logic
            userInput.style.height = 'auto';
            userInput.style.height = (userInput.scrollHeight) + 'px';
            
            // Enable send button
            sendBtn.removeAttribute('disabled');
            
            // Focus input so user can edit if needed
            userInput.focus();
        };

        recognition.onerror = (event) => {
            console.error("Speech Error:", event.error);
            micBtn.style.color = '';
            userInput.placeholder = "Error hearing audio.";
        };

        // 4. Attach Click Event
        micBtn.addEventListener('click', () => {
            if (micBtn.classList.contains('recording')) {
                recognition.stop();
            } else {
                recognition.start();
            }
        });

    } else {
        console.log("Speech Recognition not supported.");
        micBtn.style.display = 'none'; 
    }


    // --- HELPER FUNCTIONS ---
    
    function generateUUID() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    function scrollToBottom() {
        chatArea.scrollTo({
            top: chatArea.scrollHeight,
            behavior: 'smooth'
        });
    }

    function createMessageElement(text, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'assistant'}`;

        if (!isUser) {
            const avatarDiv = document.createElement('div');
            avatarDiv.className = 'avatar';
            // UPDATED: Uses the Shield Icon instead of the Robot
            avatarDiv.innerHTML = '<i class="fa-solid fa-user-shield"></i>';
            messageDiv.appendChild(avatarDiv);
        }

        const bubbleDiv = document.createElement('div');
        bubbleDiv.className = 'bubble';
        bubbleDiv.textContent = text;
        
        messageDiv.appendChild(bubbleDiv);
        return messageDiv;
    }

    // --- EVENT LISTENERS ---

    userInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
        
        if (this.value.trim().length > 0) {
            sendBtn.removeAttribute('disabled');
        } else {
            sendBtn.setAttribute('disabled', 'true');
        }
    });

    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (!sendBtn.disabled) {
                chatForm.dispatchEvent(new Event('submit'));
            }
        }
    });

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const question = userInput.value.trim();
        if (!question || isProcessing) return;

        isProcessing = true;
        userInput.value = '';
        userInput.style.height = 'auto';
        sendBtn.setAttribute('disabled', 'true');

        messagesContainer.appendChild(createMessageElement(question, true));
        scrollToBottom();

        typingIndicator.classList.remove('hidden');
        scrollToBottom();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-session-id': sessionId 
                },
                body: JSON.stringify({ 
                    question: question,
                    session_id: sessionId 
                })
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const data = await response.json();

            typingIndicator.classList.add('hidden');

            if (data.answer) {
                messagesContainer.appendChild(createMessageElement(data.answer, false));
            } else if (data.error) {
                messagesContainer.appendChild(createMessageElement("Error: " + data.error, false));
            } else {
                messagesContainer.appendChild(createMessageElement("I'm not sure how to answer that.", false));
            }

        } catch (error) {
            console.error("Fetch error:", error);
            typingIndicator.classList.add('hidden');
            messagesContainer.appendChild(createMessageElement("Sorry, server error.", false));
        } finally {
            isProcessing = false;
            scrollToBottom();
            userInput.focus();
        }
    });
});