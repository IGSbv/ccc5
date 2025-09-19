// src/App.js
import React, { useState } from 'react';
import axios from 'axios'; // Make sure axios is imported
import './App.css';

function App() {
  const [messages, setMessages] = useState([
    { sender: 'ai', text: 'Hello! I am connected to the backend. Ask me anything.' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = { sender: 'user', text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput(''); // Clear input immediately
    setIsLoading(true);
    
    try {
      // THIS IS THE REAL API CALL
      const response = await axios.post('http://localhost:8000/chat', {
        text: input,
      });
      
      setMessages((prev) => [...prev, response.data]);

    } catch (error) {
      console.error("Error fetching response:", error);
      const errorMessage = { sender: 'ai', text: 'Sorry, I could not connect to the backend.' };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="chat-window">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            <p>{msg.text}</p>
          </div>
        ))}
        {isLoading && <p className="message ai">...</p>}
      </div>
      <form onSubmit={handleSubmit} className="chat-input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about your project..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>Send</button>
      </form>
    </div>
  );
}

export default App;