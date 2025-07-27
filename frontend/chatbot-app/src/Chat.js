// frontend/src/Chat.js

import React, { useState, useRef, useEffect, forwardRef, useImperativeHandle } from 'react';
import './Chat.css'; // Import the CSS for styling

// Use forwardRef to allow parent components (App.js) to access methods of Chat
const Chat = forwardRef(({ onSendMessage }, ref) => {
  const [messages, setMessages] = useState([]); // Stores chat messages
  const [input, setInput] = useState(''); // Stores current user input
  const messagesEndRef = useRef(null); // Ref to scroll to the bottom of messages
  const [isTyping, setIsTyping] = useState(false); // State to show typing indicator

  // Expose a method to parent component (App.js) via ref
  useImperativeHandle(ref, () => ({
    sendSpecificMessage(message) {
      // This method will be called by App.js when a cloud is clicked
      // It directly initiates the message sending process
      sendMessage(null, message); // Pass null for event, and the specific message
    }
  }));

  // Scroll to the latest message whenever messages state changes
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Single sendMessage function to handle both input and specific messages (from clouds)
  const sendMessage = async (e, questionToSubmit = null) => {
    if (e && typeof e.preventDefault === 'function') {
      e.preventDefault();
    }

    const messageToSend = questionToSubmit || input;
    if (messageToSend.trim() === '') return;

    setMessages((prevMessages) => [...prevMessages, { text: messageToSend, sender: 'user' }]);
    setInput(''); // Clear input field only if it was from the input box
    setIsTyping(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_message: messageToSend }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`HTTP error! status: ${response.status}, detail: ${errorData.detail || response.statusText}`);
      }

      const data = await response.json();
      setMessages((prevMessages) => [...prevMessages, { text: data.response, sender: 'bot' }]);

    } catch (error) {
      console.error("Error sending message to backend:", error);
      setMessages((prevMessages) => [...prevMessages, { text: "Error: Could not connect to the chatbot. Please ensure the backend server is running.", sender: 'bot', isError: true }]);
    } finally {
      setIsTyping(false);
      if (onSendMessage) {
        onSendMessage(); // Notify parent (App.js) that a message was sent
      }
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h1>Cloud Services Chatbot</h1>
      </div>
      <div className="messages-display">
        {messages.length === 0 && (
          <div className="welcome-message">
            <p>👋 Welcome! Ask me anything about cloud services.</p>
            <p>Or click on a floating cloud to ask a suggested question!</p>
          </div>
        )}
        {messages.map((msg, index) => (
          <div key={index} className={`message-bubble ${msg.sender} ${msg.isError ? 'error-message' : ''}`}>
            {msg.text}
          </div>
        ))}
        {isTyping && (
          <div className="message-bubble bot typing-indicator">
            <span className="dot"></span>
            <span className="dot"></span>
            <span className="dot"></span>
          </div>
        )}
        <div ref={messagesEndRef} /> {/* Element to scroll to */}
      </div>
      <form className="message-input-form" onSubmit={sendMessage}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your question here..."
          aria-label="Type your message"
        />
        <button type="submit" aria-label="Send message">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="feather feather-send">
            <line x1="22" y1="2" x2="11" y2="13"></line>
            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
          </svg>
        </button>
      </form>
    </div>
  );
});

export default Chat;
